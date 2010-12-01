from django.contrib import admin
from manager.models import Network, Device, Sim, Deployment, SMS

"""
Iterates through models in an app and adds them to Admin UI
"""

class NetworkAdmin(admin.ModelAdmin):
    pass

class DeviceAdmin(admin.ModelAdmin):
    date_hierarchy = 'received_date'
    list_display = ('local_id', 'imei', 'received_date')
    ordering = ['-local_id']
    

class SimAdmin(admin.ModelAdmin):
    date_hierarchy = 'data_plan_expiry'
    list_display = ('phone_number', 'local_id', 'network', 'sim_id', 'contract', 'data_plan_expiry')
    ordering = ['-sim_id']
    
class DeploymentAdmin(admin.ModelAdmin):
    date_hierarchy = 'survey_start'
    list_display = ('device', 'sim', 'survey_start', 'survey_end')
    pass

class SMSAdmin(admin.ModelAdmin):
    pass

admin.site.register(Network, NetworkAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Sim, SimAdmin)
admin.site.register(SMS, SMSAdmin)
