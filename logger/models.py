from datetime import datetime, time

from django.contrib.gis.db import models

from manager.models import Device, SMS

class Log(models.Model):
    device = models.ForeignKey(Device)
    received_date_time = models.DateTimeField(help_text="Time and date that the message was received by us")
    message = models.TextField()
    cause = models.ForeignKey(SMS, null=True)
    
    def __unicode__ (self):
        return self.message[:11]
    
    def for_deployment(deployment):
        start = datetime.combine(deployment.survey_start, time(0, 0, 0))
        end = datetime.combine(deployment.survey_end, time(23, 59, 59))
        return Log.objects.filter(device=deployment.device, received_date_time__gt=start, received_date_time__lt=end)
    
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
    """ Things that could be recorded
    mobile_country_code = models.PositiveSmallIntegerField(blank=True, null=True)
    mobile_network_code = models.PositiveSmallIntegerField(blank=True, null=True)
    location_area_code = models.CharField(blank=True, null=True, max_digits=8)
    # BOTH of the folling should be parsed from Hex into Integers.
    cell_id = models.PositiveIntegerField(blank=True, null=True)
    message_number = models.PositiveIntegerField(blank=True, null=True)
    """
    objects = models.GeoManager()
    
    def __unicode__ (self):
        return str(self.sent_date_time)
    
    @staticmethod
    def for_deployment(deployment):
        start = datetime.combine(deployment.survey_start, time(0, 0, 0))
        end = datetime.combine(deployment.survey_end, time(23, 59, 59))
        return Location.objects.filter(device=deployment.device, sent_date_time__gt=start, sent_date_time__lt=end)

    
class BatteryCharge(models.Model):
    message = models.ForeignKey(Log)
    device = models.ForeignKey(Device)
    battery_percentage = models.PositiveSmallIntegerField(help_text="0-100 battery value")
    sent_date_time = models.DateTimeField(help_text="Time and date that the message was sent from the device")
    
    def __unicode__ (self):
        return str(self.device) + " " + str(self.battery_percentage) + "% at: " + str(self.sent_date_time)
    
    @staticmethod
    def for_deployment(deployment):
        start = datetime.combine(deployment.survey_start, time(0, 0, 0))
        end = datetime.combine(deployment.survey_end, time(23, 59, 59))
        return BatteryCharge.objects.filter(device=deployment.device, received_date_time__gt=start, received_date_time__lt=end)


class DeviceEvent(models.Model):
    message = models.ForeignKey(Log)
    device = models.ForeignKey(Device)
    sent_date_time = models.DateTimeField(help_text="Time and date that the message was sent from the device")
    
    DEVICE_EVENTS = (("Power On Alarm", "Power On Alarm"), ("Power Off Alarm", "Power Off Alarm"), ("Power Low Alarm", "Power Low Alarm"), ("Start Charging Report", "Start Charging Report"), ("Finish charging report", "Finish charging report"))
    
    event = models.CharField(help_text = "A device event e.g. power on/off", max_length="50", choices=DEVICE_EVENTS)
    
    def __unicode__ (self):
        return str(self.device) + " " + self.event + " at: " + str(self.sent_date_time)
    
    @staticmethod
    def for_deployment(deployment):
        start = datetime.combine(deployment.survey_start, time(0, 0, 0))
        end = datetime.combine(deployment.survey_end, time(23, 59, 59))
        return DeviceEvent.objects.filter(device=deployment.device, received_date_time__gt=start, received_date_time__lt=end)

