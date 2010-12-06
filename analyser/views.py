from datetime import date, datetime, timedelta
from itertools import chain

from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.gis.geos import MultiPoint, LineString
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from manager.models import Deployment
from analyser.models import Cluster
from analyser.analyse import analyse, THRESHOLD_ACCURACY
from logger.models import Location

@login_required
def render_kml(request, deployment):
    # TODO - Use the new algorithm/method here.  
    deployment = get_object_or_404(Deployment, pk=deployment)
    
    clusters = []
    for cluster in Cluster.for_deployment(deployment):
        clusters.append({
            'geocoded': cluster.geocoded,
            'youngest': cluster.youngest(),
            'eldest': cluster.eldest(),
            'poly_kml': MultiPoint([l.location for l in cluster.locations.all()]).convex_hull.kml,
            'centre_kml': MultiPoint([l.location for l in cluster.locations.all()]).centroid.kml,
        })
    
    lines = []
    this_line = []
    last_point = None
    for location in Location.for_deployment(deployment).filter(accuracy__lt=THRESHOLD_ACCURACY).order_by('sent_date_time'):
        # Break up lines that have more than 30 minutes between points
        if last_point is not None and location.sent_date_time - last_point.sent_date_time > timedelta(minutes=30):
            if len(this_line) > 1:
                lines.append(this_line)
            this_line = []
        
        this_line.append(location)
        last_point = location
    
    lines.append(this_line)
    lines = [LineString([l.location for l in line]) for line in lines]
    
    locations = []
    for location in Location.for_deployment(deployment).filter(accuracy__lt=THRESHOLD_ACCURACY).order_by('sent_date_time'):
        location.next = location.sent_date_time + timedelta(minutes=30)
        locations.append(location)
    
    context = {
        'device': deployment.device,
        'clusters': clusters,
        'lines': lines,
        'locations': locations,
    }
    
    return render_to_response('analyser/clusters.kml', context, context_instance=RequestContext(request), mimetype='application/vnd.google-earth.kml+xml')

@login_required
def render_report(request, deployment):
    # Tim's new method
    deployment = get_object_or_404(Deployment, pk=deployment)
    view_date = request.GET.get('date')
    if view_date is not None:
        try:
            y, m, d = map(int, view_date.split('-'))
            dtl = datetime(y, m, d)
            dth = datetime(y, m, d) + timedelta(days=1)
        except ValueError, IndexError:
            view_date = None
    
    if request.GET.get('regenerate') is not None:
        analyse(deployment.device)
    
    lines = []
    cluster_points = set([l for cluster in Cluster.for_deployment(deployment) for l in cluster.locations.all()])
    dates = set()
    
    this_line = []
    for location in Location.for_deployment(deployment).filter(accuracy__lt=THRESHOLD_ACCURACY).order_by('sent_date_time'):
        dates.add(location.sent_date_time.date())
        if view_date is not None and (location.sent_date_time < dtl or location.sent_date_time > dth):
            continue
        if location in cluster_points:
            if len(this_line) > 2:
                lines.append(this_line)
            this_line = []
        else:
            if len(this_line) > 0:
                if location.sent_date_time - this_line[-1].sent_date_time > timedelta(minutes=30):
                    lines.append(this_line)
                    this_line = []
            this_line.append(location)    
    lines.append(this_line)
    
    clusters = []
    for cluster in Cluster.for_deployment(deployment):
        if view_date is None or ((cluster.eldest() < dth and cluster.eldest() > dtl) or (cluster.youngest() > dtl and cluster.youngest() < dth)):
            cluster.centre = str(cluster.location.coords[1]) + "," + str(cluster.location.coords[0])
            cluster.heat = "%02X" % max(255 - ((float((cluster.eldest() - cluster.youngest()).seconds) / 14400) * 256), 0)
            clusters.append(cluster)
    
    context = {
        'dates': sorted(dates),
        'view_date': view_date,
        'deployment': deployment,
        'clusters': sorted(clusters, key=lambda cluster: cluster.youngest()),
        'lines': [[','.join(reversed([str(c) for c in l.location.coords])) for l in line] for line in lines]
    }
    
    return render_to_response('analyser/report.html', context, context_instance=RequestContext(request))
