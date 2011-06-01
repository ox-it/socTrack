from django.contrib.gis.geos import MultiPoint

from geopy import geocoders

from secrets import secrets
from analyser.models import Cluster
from analyser.haversine import haversine
from logger.models import Location

from datetime import datetime, timedelta

THRESHOLD_DISTANCE = 0.20 # The radius points are allowed to be from each other to
                        # be considered as part of a cluster
THRESHOLD_TIME = 480 # This is the max time interval in minutes between points to be considered the same place
THRESHOLD_MIN_TIME = 61 # Minimum number of seconds for a point to be considered a 'point'
THRESHOLD_ACCURACY = 10# Only consider GPS points below this level of accuracy (NEMA standard)
THRESHOLD_SPEED = 10  #KPH

def merge_points(locations):
    # Assumes locations are in time order
    iterations = 0
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
    return locations, iterations

def analyse(device):
    Cluster.objects.filter(device=device).delete()
    query = Location.objects.filter(device=device, sent_date_time__lt=datetime.now() - timedelta(hours=-1), accuracy__lt=THRESHOLD_ACCURACY, speed__lt=THRESHOLD_SPEED).order_by('sent_date_time')
    locations = [location for location in query]
   
    # Set each potential cluster with a starting point of itself 
    for location in locations:
        location.points = [location]
        location.end_date_time = location.sent_date_time
       
    # Keep iterating through gradually decreasing number of points until there has been no change since the last iteration  
    locations, passone = merge_points(locations)
    locations = [location for location in locations if (location.end_date_time - location.sent_date_time) > timedelta(seconds=THRESHOLD_MIN_TIME)]
    locations = sorted(locations, key=lambda location: location.sent_date_time) 
    locations, passtwo = merge_points(locations) 
    
    for location in locations:
        geocoder = geocoders.Google(secrets['GOOGLE'])
        try:
            place, point = geocoder.reverse((location.location[1], location.location[0]))
        except IndexError:
            place = "Unknown location"
        
        if place is None:
            place = 'Unknown location'
    
        c = Cluster(geocoded=place, device=device, location=location.location, speed=location.speed, altitude=location.altitude)
        c.save()
        c.locations = location.points
        c.save()
    
    return locations, passone, passtwo