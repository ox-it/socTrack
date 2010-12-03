from datetime import datetime, timedelta
from itertools import chain

from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.gis.geos import MultiPoint, LineString
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from manager.models import Deployment
from analyser.models import Cluster
from analyser.management.commands.analyse_clusters import THRESHOLD_ACCURACY
from logger.models import Location

@login_required
def render_kml(request, deployment):
    
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
    
    deployment = get_object_or_404(Deployment, pk=deployment)
    
    lines = []
    cluster_points = set([l for cluster in Cluster.for_deployment(deployment) for l in cluster.locations.all()])
    
    this_line = []
    for location in Location.for_deployment(deployment).filter(accuracy__lt=THRESHOLD_ACCURACY):
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
    
    context = {
        'clusters': Cluster.for_deployment(deployment),
        'cluster_points': [','.join(reversed([str(c) for c in MultiPoint([l.location for l in cluster.locations.all()]).centroid.coords])) for cluster in Cluster.for_deployment(deployment)],
        'lines': [[','.join(reversed([str(c) for c in l.location.coords])) for l in line] for line in lines]
    }
    
    return render_to_response('analyser/report.html', context, context_instance=RequestContext(request))