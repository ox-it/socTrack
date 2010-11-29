from django.db import models

class Network(models.Model):
    name = models.CharField(max_length=30)

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
    
    def __unicode__ (self):
        return self.phone_number
        
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




