from django.db import models

from logger.models import Location
from manager.models import Device

class Cluster(models.Model):
    
    locations = models.ManyToManyField(Location, help_text="The location reports which make up this cluster")
    geocoded = models.TextField(help_text="A human readable name identifying the location of this cluster")
    device = models.ForeignKey(Device)
