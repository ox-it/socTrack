from datetime import datetime

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
    
    actions = ['configure_device', 'stop_reporting', 'check_battery', 'reboot_device', 'locate_now',
               'configure_report_every_5s', 'configure_report_every_60s', 'configure_report_every_15m',
               'configure_walking_mode', 'configure_vehicle_mode'
              ]
    
    def configure_device(self, request, queryset):
        for deployment in queryset:
            deployment.configure_device()
    configure_device.short_description = "Send text message to configure the device"
    
    def _configure_report(self, queryset, interval):
        for deployment in queryset:
            deployment.send_device_message(','.join([
                    'AT+GTTRI=%s' % deployment.device.password,
                    '0000', # Reporting start time
                    '2359', # Reporting end time
                    '1' if interval < 60 else str(int(interval/60)), # Send interval, in minutes
                    str(interval), # Fix interval, in seconds
                    datetime.now().strftime('%Y%m%d%H%M%S')
                ]),
                'Configuring reporting at %d second intervals' % interval)
    
    def configure_report_every_5s(self, request, queryset):
        self._configure_report(queryset, 5)
    configure_report_every_5s.short_description = "Tell the device to report every 5 seconds"
    
    def configure_report_every_60s(self, request, queryset):
        self._configure_report(queryset, 60)
    configure_report_every_60s.short_description = "Tell the device to report every 60 seconds"
    
    def configure_report_every_15m(self, request, queryset):
        self._configure_report(queryset, 900)
    configure_report_every_15m.short_description = "Tell the device to report every 15 minutes"
    
    def stop_reporting(self, request, queryset):
        for deployment in queryset:
            deployment.send_device_message(','.join([
                    'AT+GTTRI=%s' % deployment.device.password,
                    '0000', # Reporting start time
                    '0001', # Reporting end time
                    '1', # Send interval, in minutes
                    '120', # Fix interval, in seconds
                    datetime.now().strftime('%Y%m%d%H%M%S')
                ]),
                'Stop reporting')
    stop_reporting.short_description = "Tell the device to stop reporting"
    
    def _send_rto(self, queryset, command, human_message):
        for deployment in queryset:
            deployment.send_device_message(','.join([
                    'AT+GTRTO=%s' % deployment.device.password,
                    command, # Information type
                    datetime.now().strftime('%Y%m%d%H%M%S')
                ]),
                human_message)
    
    def check_battery(self, request, queryset):
        self._send_rto(queryset, 'A', 'Send battery level information now')
    check_battery.short_description = "Ask the device to send battery level information now"
    
    def reboot_device(self, request, queryset):
        self._send_rto(queryset, '3', 'Reboot the device')
    reboot_device.short_description = "Reboot the device"
    
    def locate_now(self, request, queryset):
        self._send_rto(queryset, '1', 'Send location now')
    locate_now.short_description = "Ask to device to send a location update immediately"
    
    def _set_mode(self, queryset, a, b):
        for deployment in queryset:
            deployment.send_device_message(','.join([
                    'AT+GTSFR=%s' % deployment.device.password,
                    '1',
                    '1',
                    '1',
                    '1',
                    '1',
                    a,
                    b,
                    '0',
                    '0',
                    datetime.now().strftime('%Y%m%d%H%M%S')
                ]),
                'Changing device to %s mode' % 'walking' if a == 2 else 'vehicle')
    
    def configure_walking_mode(self, request, queryset):
        self._set_mode(queryset, '2', '100')
    configure_walking_mode.short_description = "Configure the device for walking mode"
    
    def configure_vehicle_mode(self, request, queryset):
        self._set_mode(queryset, '15', '200')
    configure_vehicle_mode.short_description = "Configure the device for vehicle mode"


class SMSAdmin(admin.ModelAdmin):
    pass

admin.site.register(Network, NetworkAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Sim, SimAdmin)
admin.site.register(Deployment, DeploymentAdmin)
admin.site.register(SMS, SMSAdmin)
