from django.contrib import admin
from logger.models import BatteryCharge, DeviceEvent, Location, Log


class BatteryChargeAdmin(admin.ModelAdmin):
    date_hierarchy = 'sent_date_time'
    list_display = ('device', 'sent_date_time', 'battery_percentage') 
    list_filter = ('device', )
    ordering = ['-sent_date_time']

class DeviceEventAdmin(admin.ModelAdmin):
    date_hierarchy = 'sent_date_time'
    list_display = ('device', 'sent_date_time', 'event') 
    list_filter = ('device', 'event')
    ordering = ['-sent_date_time']

class LocationAdmin(admin.ModelAdmin):
    date_hierarchy = 'sent_date_time'
    list_display = ('device', 'sent_date_time', 'location', 'speed', 'heading', 'altitude') 
    list_filter = ('device',)
    ordering = ['-sent_date_time']

class LogAdmin(admin.ModelAdmin):
    date_hierarchy = 'received_date_time'
    list_display = ('device', 'received_date_time', '__unicode__')

admin.site.register(BatteryCharge, BatteryChargeAdmin)
admin.site.register(DeviceEvent, DeviceEventAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Log, LogAdmin)
