from django.contrib import admin
from manager.models import Network, Device, Sim, Deployment

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
    list_display = ('network', 'phone_number', 'sim_id', 'contract')
    ordering = ['-sim_id']
    
class DeploymentAdmin(admin.ModelAdmin):
    date_hierarchy = 'survey_start'
    list_display = ('device', 'sim', 'survey_start', 'survey_end')
    pass
    
admin.site.register(Network, NetworkAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Sim, SimAdmin)
admin.site.register(Deployment, DeploymentAdmin)

"""

    


    class BatteryChargeAdmin(admin.ModelAdmin):
        date_hierarchy = 'sent_date_time'
        list_display = ('device', 'sent_date_time', 'battery_percentage') 
        list_filter = ('device', )
        ordering = ['-sent_date_time']
        pass

    class DeviceEventAdmin(admin.ModelAdmin):
        date_hierarchy = 'sent_date_time'
        list_display = ('device', 'sent_date_time', 'event') 
        list_filter = ('device', 'event')
        ordering = ['-sent_date_time']
        pass

    class LocationAdmin(admin.ModelAdmin):
        date_hierarchy = 'sent_date_time'
        list_display = ('device', 'sent_date_time', 'location', 'speed', 'heading', 'altitude') 
        list_filter = ('device',)
        ordering = ['-sent_date_time']
        pass

    
"""