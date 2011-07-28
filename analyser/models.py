from datetime import datetime, time
from dateutil.tz import tzutc

from django.contrib.gis.db import models
from django.utils.timesince import timesince

from logger.models import Location
from manager.models import Device
from analyser.templatetags.dtlocalize import dtlocalize

class Cluster(models.Model):
    # The average speed, altitude and location between points - NOT the same as a centroid on locations
    speed = models.DecimalField(max_digits=8, decimal_places=1)
    altitude = models.FloatField()
    location = models.PointField()

    locations = models.ManyToManyField(Location, help_text="The location reports which make up this cluster")
    geocoded = models.TextField(help_text="A human readable name identifying the location of this cluster")
    device = models.ForeignKey(Device)
    
    @staticmethod
    def for_deployment(deployment, start=None, end=None):
        if start is None:
            start = datetime.combine(deployment.survey_start, time(0, 0, 0))
        if end is None:
            end = datetime.combine(deployment.survey_end, time(23, 59, 59))
        start = dtlocalize(start).astimezone(tzutc()).replace(tzinfo=None)
        end = dtlocalize(end).astimezone(tzutc()).replace(tzinfo=None)
        clusters = []
        for cluster in Cluster.objects.filter(device=deployment.device):
            try:
                if (cluster.youngest() > start and cluster.eldest() < end) or (cluster.youngest() < start and cluster.eldest() > start) or (cluster.youngest() < end and cluster.eldest() > end):
                    clusters.append(cluster)
            except ValueError:
                pass
        return clusters
    
    def youngest(self):
        try:
            return min([l.sent_date_time for l in self.locations.all()])
        except ValueError:
            return None
    
    def eldest(self):
        try:
            return max([l.sent_date_time for l in self.locations.all()])
        except ValueError:
            return None
    
    def duration(self):
        y = self.youngest()
        e = self.eldest()
        if y is not None and e is not None:
            return timesince(self.youngest(), self.eldest())
        else:
            return None

class GeocodeCache(models.Model):
    
    location = models.PointField()
    name = models.TextField()
    
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name
