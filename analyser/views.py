from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.gis.geos import MultiPoint, LineString
from django.template import RequestContext

from manager.models import Deployment
from analyser.models import Cluster
from analyser.management.commands.analyse_clusters import THRESHOLD_ACCURACY
from logger.models import Location

def render_kml(request, deployment):
    
    deployment = get_object_or_404(Deployment, pk=deployment)
    
    clusters = []
    for cluster in Cluster.for_deployment(deployment):
        youngest = min([l.sent_date_time for l in cluster.locations.all()])
        eldest = max([l.sent_date_time for l in cluster.locations.all()])
        clusters.append({
            'geocoded': cluster.geocoded,
            'youngest': youngest,
            'eldest': eldest,
            'poly_kml': MultiPoint([l.location for l in cluster.locations.all()]).convex_hull.kml,
            'centre_kml': MultiPoint([l.location for l in cluster.locations.all()]).centroid.kml,
        })
    
    lines = []
    this_line = []
    last_point = None
    for location in Location.for_deployment(deployment).filter(accuracy__lt=THRESHOLD_ACCURACY).order_by('sent_date_time'):
        # Break up lines that have more than 30 minutes between points
        if last_point is not None and location.sent_date_time - last_point.sent_date_time > timedelta(minutes=30):
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
