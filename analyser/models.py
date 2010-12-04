from datetime import datetime, time

from django.db import models

from logger.models import Location
from manager.models import Device

class Cluster(models.Model):
#    location = Location()
    locations = models.ManyToManyField(Location, help_text="The location reports which make up this cluster")
    geocoded = models.TextField(help_text="A human readable name identifying the location of this cluster")
    device = models.ForeignKey(Device)
    
    @staticmethod
    def for_deployment(deployment):
        start = datetime.combine(deployment.survey_start, time(0, 0, 0))
        end = datetime.combine(deployment.survey_end, time(23, 59, 59))
        clusters = []
        for cluster in Cluster.objects.filter(device=deployment.device):
            if (cluster.youngest() > start and cluster.eldest() < end) or (cluster.youngest() < start and cluster.eldest() > start) or (cluster.youngest() < end and cluster.eldest() > end):
                clusters.append(cluster)
        return clusters
    
    def youngest(self):
        return min([l.sent_date_time for l in self.locations.all()])
    
    def eldest(self):
        return max([l.sent_date_time for l in self.locations.all()])
