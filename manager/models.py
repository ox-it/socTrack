from datetime import datetime
import httplib
import urllib

from django.db import models
from django.conf import settings

from secrets import secrets

class Network(models.Model):
    name = models.CharField(max_length=30)
    apn = models.CharField(max_length=20,
                           default='',
                           help_text="The access point name for this network")
    apn_username = models.CharField(max_length=20,
                           default='',
                           blank=True,
                           help_text="The password for ")
    apn_password = models.CharField(max_length=20,
                           default='',
                           blank=True,
                           help_text="The access point name for this network")
    def __unicode__ (self):
        return self.name
    
class Device(models.Model):
    # IMEIs are variable length - max length should be 19 though
    imei = models.CharField(max_length=19, unique=True)
    local_id = models.CharField( 
        max_length=10,
        help_text = "An arbitrary local identifier (e.g. for labeling) up to ten characters long")
    received_date = models.DateField(
        help_text = "Date the device was received and ready for service (for purchase tracking)",
        null=True,
        blank=True)
    password = models.CharField(
        max_length=8,
        default='gl100',
        help_text='The default password for the device'
    )
    
    def __unicode__ (self):
        return self.local_id

class Sim(models.Model):
    sim_id = models.CharField(
        max_length = 50,
        help_text = "The SIM ID as usually printed on the back of the SIM card")
    # phone_number could build in some validation - max_length = 20 is not confirmed as always true internationally, but should be in the UK
    phone_number = models.CharField(max_length=20)
    network = models.ForeignKey(Network)
    data_plan_expiry = models.DateField(help_text = "Date the current data plan expires", null=True, blank=True)
    notes = models.TextField(help_text = "General notes about the SIM card e.g. it is blue", blank=True)
    contract = models.BooleanField(help_text = "Describes whether SIM is on PAYG (true), Contract (false)")
    local_id = models.CharField( 
        default="",
        max_length=10,
        help_text = "An arbitrary local identifier (e.g. for labeling) up to ten characters long")
    def __unicode__ (self):
        return self.local_id

class SMS(models.Model):
    sim = models.ForeignKey(Sim)
    device = models.ForeignKey(Device)
    message = models.CharField(max_length=160)
    response = models.CharField(max_length=160, null=True)
    send_time = models.DateTimeField()
    human_message = models.TextField(max_length=160, blank=True)
    
    def save(self, *args, **kwargs):
        conn = httplib.HTTPConnection('www.meercom1.co.uk', 80)
        conn.request("POST",
                     "/sendsms.asp",
                     urllib.urlencode({
                        'account': secrets['SMS_ACCOUNT'],
                        'password': secrets['SMS_PASSWORD'],
                        'message': self.message,
                        'phone': self.sim.phone_number,
                     }),
                     {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"})
        self.response = conn.getresponse().read()
        super(SMS, self).save(*args, **kwargs)

class Deployment(models.Model):
    device = models.ForeignKey(Device)
    sim = models.ForeignKey(Sim)
    post_out_date = models.DateField(help_text = "Date device was/is to be posted out to recipient", null=True, blank=True)
    
    # TODO Unsure about the use of this field
    received_back_date = models.DateField(help_text = "Date device was received back from recipient", null=True, blank=True)
    
    survey_start = models.DateField(help_text = "Date survey was/is due to start")
    survey_end = models.DateField(help_text = "Date survey was/is due to finish")
    
    def __unicode__ (self):
        return str(self.device) + " From: " + str(self.survey_start) + " To: " + str(self.survey_end)
    
    def configure_device(self):
        """
        Sends a message to the device in which it configures itself to use
        this server for location reporting
        """
        send_time = datetime.now()
        SMS(sim=self.sim,
            device=self.device,
            message=','.join([
                'AT+GTSRI=gl100',
                '1', # Force GPRS reporting (0 = GPRS with SMS fallback, 2 = SMS only)
                '0', # Close GPRS session after data sending, 1 = persistent
                self.sim.network.apn,
                self.sim.network.apn_username,
                self.sim.network.apn_password,
                settings.LOG_SERVER_IP,
                settings.LOG_SERVER_PORT,
                settings.FALLBACK_SMS,
                send_time.strftime('%Y%m%d%H%M%S')
            ]),
            send_time=send_time,
            human_message="Configuring device to use server: " + settings.LOG_SERVER_IP + ':' + settings.LOG_SERVER_PORT).save()
    
    def send_device_message(self, message, human_message):
        """
        Sends a message to the device
        """
        send_time = datetime.now()
        SMS(sim=self.sim,
            device=self.device,
            message=message,
            send_time=send_time,
            human_message=human_message).save()