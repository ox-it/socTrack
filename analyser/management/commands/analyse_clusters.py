from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import MultiPoint
from django.contrib.gis.measure import Distance

from geopy import geocoders

from analyser.models import Cluster
from analyser.haversine import haversine
from logger.models import Location
from manager.models import Device

from datetime import datetime, timedelta

THRESHOLD_DISTANCE = 0.1 # The radius points are allowed to be from each other to
                        # be considered as part of a cluster
THRESHOLD_TIME = 5 # How many minutes in the same place for this to be a cluster
THRESHOLD_ACCURACY = 6 # Only consider GPS points below this level of accuracy
GOOGLE_KEY = 'ABQIAAAAlUxesxSydOb_SQF6o594BBSpsA0gLz9oElZerpIFXY4w7Ru4MRQhVheUH73nj1uBq3KJqJnU6tGCYw'

class Command(BaseCommand):
    args = ''
    help = 'Analyses location data and creates clusters'

    def handle(self, *args, **options):
        
        # Consider each device one at a time
        for device in Device.objects.all():
            current_cluster_locations = set()
            last_chance = False
            for location in Location.objects.filter(device=device, analysed=False, sent_date_time__lt=datetime.now() - timedelta(hours=-1), accuracy__lt=THRESHOLD_ACCURACY).order_by('sent_date_time'):
                
                location.analysed = True
                
                # Start a new cluster to be considered if the current one is empty
                if len(current_cluster_locations) == 0:
                    current_cluster_locations.add(location)
                
                else:
                    
                    # Check whether this point could be considered to be a member of this cluster
                    current_cluster = MultiPoint([l.location for l in current_cluster_locations])
                    distance = haversine(current_cluster.centroid, location.location)
                    if distance < THRESHOLD_DISTANCE:
                        # Good, our cluster just got bigger
                        current_cluster_locations.add(location)
                        last_chance = True
                    else:
                        # If this is the first outlier, then just move on to the next one
                        if not last_chance:
                            last_chance = False
                        # If we've no more chances, and we haven't had a point in
                        # this cluster for THRESHOLD_TIME minutes, then give it up
                        elif max([l.sent_date_time for l in current_cluster_locations]) + timedelta(minutes=THRESHOLD_TIME) < location.sent_date_time:
                            # We've missed our chances, that's the end of this cluster
                            # Figure out if we've stayed in this spot long enough
                            start = min([l.sent_date_time for l in current_cluster_locations])
                            end = max([l.sent_date_time for l in current_cluster_locations])
                            if end - start > timedelta(minutes=THRESHOLD_TIME):
                                # We've got a cluster - geocode it
                                geocoder = geocoders.Google(GOOGLE_KEY)
                                (new_place, new_point) = geocoder.reverse((current_cluster.centroid[1], current_cluster.centroid[0]))
                                
                                c = Cluster(geocoded=new_place, device=device)
                                c.save()
                                c.locations = current_cluster_locations
                                c.save()
                                print "Identified a cluster as", new_place
                            
                            # Clear and go on to our next cluster
                            current_cluster_locations = set((location,))
                            print location.sent_date_time
                            print "New cluster!"
                            last_chance = True
                    
                location.save()
            
            # Mark the currently considered cluster as unanalysed, because it
            # may continue into the future past what's currently being analysed
            for location in current_cluster_locations:
                location.analysed = False
                location.save()