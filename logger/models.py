from django.contrib.gis.db import models
from socTrack.manager.models import Device

class Log(models.Model):
    device = models.ForeignKey(Device)
    received_date_time = models.DateTimeField(help_text="Time and date that the message was received by us")
    sent_date_time = models.DateTimeField(help_text="Time and date taht the message was sent from the device")
    message = models.TextField()
    
    def __unicode__ (self):
        return self.received_date_time + ":" + self.message[:11]
    
class Location(models.Model):
    # TODO Check if model field selections are sane - e.g. accuracy is never negative
    message = models.ForeignKey(Log)
    device = models.ForeignKey(Device)
    speed = models.DecimalField(max_digits=8, decimal_places=1, help_text = "Unknown units")
    heading = models.PositiveSmallIntegerField(help_text = "Heading in degrees, 0-359")
    altitude = models.IntegerField(help_text = "Unknown units")
    accuracy = models.PositiveSmallIntegerField(help_text = "Unknown units")
    location = models.PointField()
    
    def __unicode__ (self):
        return self.date
    
class BatteryCharge(models.Model):
    message = models.ForeignKey(Log)
    device = models.ForeignKey(Device)
    battery_percentage = models.PositiveSmallIntegerField(help_text="0-100 battery value")

class DeviceEvent(models.Model):
    message = models.ForeignKey(Log)
    device = models.ForeignKey(Device)
    
    DEVICE_EVENTS = ()
    
    event = models.CharField(help_text = "A device event e.g. power on/off", max_length="50", choices=DEVICE_EVENTS)
    