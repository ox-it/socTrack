from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import MultiPoint
from django.contrib.gis.measure import Distance

from geopy import geocoders

from secrets import secrets
from analyser.models import Cluster
from analyser.haversine import haversine
from logger.models import Location
from manager.models import Device

from datetime import datetime, timedelta

THRESHOLD_DISTANCE = 0.20 # The radius points are allowed to be from each other to
                        # be considered as part of a cluster
THRESHOLD_TIME = 480 # This is the max time interval in minutes between points to be considered the same place
THRESHOLD_MIN_TIME = 60 # Minimum number of seconds for a point to be considered a 'point'
THRESHOLD_ACCURACY = 10# Only consider GPS points below this level of accuracy (NEMA standard)
THRESHOLD_SPEED = 10  #KPH

class Command(BaseCommand):
    args = ''
    help = 'Analyses location data and creates clusters'

    def handle(self, *args, **options):
	# Remove existing clusters
        Cluster.objects.all().delete()
        
        # Consider each device one at a time
        for device in Device.objects.all():
            query = Location.objects.filter(device=device, sent_date_time__lt=datetime.now() - timedelta(hours=-1), accuracy__lt=THRESHOLD_ACCURACY, speed__lt=THRESHOLD_SPEED).order_by('sent_date_time')
            locations = [location for location in query]
           
	    # Set each potential cluster with a starting point of itself 
            for location in locations:
                location.points = [location]
		location.end_date_time = location.sent_date_time
               
	    # Keep iterating through gradually decreasing number of points until there has been no change since the last iteration  
	    points_merged = True 
	    iterations = 0
            while points_merged == True:
		points_merged = False
		iterations += 1
		j = 0
                while j < len(locations) -1:
                    # Calculate time delta between the two points
                    dTime = locations[j+1].sent_date_time - locations[j].end_date_time
                    
                    if dTime < timedelta(minutes=THRESHOLD_TIME):
                        # Find distance betweeen the two points                    
                        distance = haversine(locations[j].location, locations[j+1].location)
                        if distance < THRESHOLD_DISTANCE:
                            # Find average of the two points
                            locations[j].location = MultiPoint([locations[j].location, locations[j+1].location]).centroid
                            # Save average point and set the point end_time to the send time of the second point
                            locations[j].altitude = (locations[j].altitude + locations[j+1].altitude) / 2
                            locations[j].end_date_time = locations[j+1].end_date_time
                            locations[j].speed = (locations[j].speed + locations[j+1].speed) /2
			    # Add all the collected points to the new cluster
                            for point in locations[j+1].points:
                                locations[j].points.append(point)
                            # Remove the second location as it has been merged with the first    
                            del locations[j+1]
			    points_merged = True
                    j += 1
	   
	    locations = [location for location in locations if (location.end_date_time - location.sent_date_time) > timedelta(seconds=THRESHOLD_MIN_TIME)]
            	   
	    points_merged = True
            while points_merged == True:
                points_merged = False
		iterations +=1 
    	        j = 0 
	        while j < len(locations) - 1:
	    	    dTime = locations[j+1].sent_date_time - locations[j].end_date_time	
		    distance = haversine(locations[j].location, locations[j+1].location)
		    if dTime < timedelta(minutes=THRESHOLD_TIME) and distance < THRESHOLD_DISTANCE:
		 	locations[j].location = MultiPoint([locations[j].location, locations[j+1].location]).centroid
			locations[j].altitude = (locations[j].altitude + locations[j+1].altitude) /2
			locations[j].end_date_time = locations[j+1].end_date_time
			locations[j].speed = (locations[j].speed + locations[j+1].speed) /2
			for point in locations[j+1].points:
				locations[j].points.append(point)
			del locations[j+1]
			points_merged = True
		    j += 1
	    

            for location in locations:
                place = "Unknown location"
                """if len(location.points) > 1: 
                    geocoder = geocoders.Google(secrets['GOOGLE'])
                    try:
                        place, point = geocoder.reverse((location.location[1], location.location[0]))
                    except IndexError:
                        place = "Unable to geocode"
                """
                
                c = Cluster(geocoded=place, device=device, location=location.location, speed=location.speed, altitude=location.altitude)
                c.save()
                c.locations = location.points
                c.save()
		
            
            print device.local_id + " points created: " + str(len(locations)) + " iterations: " + str(iterations)
                
                
"""
    # Start a new cluster to be considered if the current one is empty
    if len(current_cluster_locations) == 0:
        current_cluster_locations.add(location)
        current_cluster = Point(location.location)
    
    else:
        
        # Check whether this point could be considered to be a member of this cluster
        distance = haversine(current_cluster.centroid, location.location)
        if distance < THRESHOLD_DISTANCE:
            # Good, our cluster just got bigger
            current_cluster_locations.add(location)
            current_cluster = MultiPoint([current_cluster, location.location])
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
                    geocoder = geocoders.Google(secrets['GOOGLE'])
                    (new_place, new_point) = geocoder.reverse((current_cluster.centroid[1], current_cluster.centroid[0]))
                    
                    c = Cluster(geocoded=new_place, device=device)
                    c.save()
                    c.locations = current_cluster_locations
                    c.save()
                    print "Identified a cluster as", new_place
           
                # Clear and go on to our next cluster
                current_cluster_locations = set((location,))
                current_cluster = Point(location.location)
                print location.sent_date_time
                print "New cluster!"
                last_chance = True
        
    location.save()

# Mark the currently considered cluster as unanalysed, because it
# may continue into the future past what's currently being analysed
for location in current_cluster_locations:
    location.analysed = False
    location.save()
"""
