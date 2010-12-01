from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.gis.geos import MultiPoint, LineString
from django.template import RequestContext

from manager.models import Device
from analyser.models import Cluster
from analyser.management.commands.analyse_clusters import THRESHOLD_ACCURACY
from logger.models import Location

def render_kml(request, imei):
    
    #y, m, d = map(int, (y, m, d))
    #limit_l = datetime(y, m, d)
    #limit_h = datetime(y, m, d) + timedelta(days=1)
    
    device = get_object_or_404(Device, imei=imei)
    
    clusters = []
    for cluster in Cluster.objects.filter(device=device):
        youngest = min([l.sent_date_time for l in cluster.locations.all()])
        eldest = max([l.sent_date_time for l in cluster.locations.all()])
        #if youngest > limit_l and eldest < limit_h or (youngest < limit_l and eldest > limit_l) or (youngest < limit_h and eldest > limit_h):
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
    #for location in Location.objects.filter(device=device, sent_date_time__gt=limit_l, sent_date_time__lt=limit_h).order_by('sent_date_time'):
    for location in Location.objects.filter(device=device, accuracy__lt=THRESHOLD_ACCURACY).order_by('sent_date_time'):
        # Break up lines that have more than 30 minutes between points
        if last_point is not None and location.sent_date_time - last_point.sent_date_time > timedelta(minutes=30):
            lines.append(this_line)
            this_line = []
        
        this_line.append(location)
        last_point = location
    
    lines.append(this_line)
    lines = [LineString([l.location for l in line]) for line in lines]
    
    #locations = Location.objects.filter(device=device, sent_date_time__gt=limit_l, sent_date_time__lt=limit_h).order_by('sent_date_time')
    locations = []
    for location in Location.objects.filter(device=device, accuracy__lt=THRESHOLD_ACCURACY).order_by('sent_date_time'):
        location.next = location.sent_date_time + timedelta(minutes=30)
        locations.append(location)
    
    context = {
        'device': device,
        'clusters': clusters,
        'lines': lines,
        'locations': locations,
    }
    
    return render_to_response('analyser/clusters.kml', context, context_instance=RequestContext(request), mimetype='application/vnd.google-earth.kml+xml')