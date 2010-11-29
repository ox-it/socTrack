from django.contrib.gis.db import models
from manager.models import Device

class Log(models.Model):
    device = models.ForeignKey(Device)
    received_date_time = models.DateTimeField(help_text="Time and date that the message was received by us")
    message = models.TextField()
    
    def __unicode__ (self):
        return self.message[:11]
    
class Location(models.Model):
    # TODO Check if model field selections are sane - e.g. accuracy is never negative
    message = models.ForeignKey(Log)
    device = models.ForeignKey(Device)
    speed = models.DecimalField(max_digits=8, decimal_places=1, help_text = "Speed in km/h")
    heading = models.PositiveSmallIntegerField(help_text = "Heading in degrees, 0-359")
    altitude = models.FloatField(help_text = "Altitude in metres")
    accuracy = models.PositiveSmallIntegerField(help_text = "Unknown units")
    location = models.PointField()
    sent_date_time = models.DateTimeField(help_text="Time and date that the message was sent from the device")
    sos = models.BooleanField(help_text = "Whether this location data was sent as a result of the 'SOS' button being pressed")
    analysed = models.BooleanField(help_text = "Whether this location data has been analysed", default=False)
    objects = models.GeoManager()
    
    def __unicode__ (self):
        return str(self.sent_date_time)
    
class BatteryCharge(models.Model):
    message = models.ForeignKey(Log)
    device = models.ForeignKey(Device)
    battery_percentage = models.PositiveSmallIntegerField(help_text="0-100 battery value")
    sent_date_time = models.DateTimeField(help_text="Time and date that the message was sent from the device")
    
    def __unicode__ (self):
        return str(self.device) + " " + str(self.battery_percentage) + "% at: " + str(self.sent_date_time)

class DeviceEvent(models.Model):
    message = models.ForeignKey(Log)
    device = models.ForeignKey(Device)
    sent_date_time = models.DateTimeField(help_text="Time and date that the message was sent from the device")
    
    DEVICE_EVENTS = (("Power On Alarm", "Power On Alarm"), ("Power Off Alarm", "Power Off Alarm"), ("Power Low Alarm", "Power Low Alarm"))
    
    event = models.CharField(help_text = "A device event e.g. power on/off", max_length="50", choices=DEVICE_EVENTS)
    
    def __unicode__ (self):
        return str(self.device) + " " + self.event + " at: " + str(self.sent_date_time)
