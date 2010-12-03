from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from logger.models import Location, Log, BatteryCharge, DeviceEvent
from manager.models import Device, SMS, Sim, Deployment

@login_required
def render_device(request, device):
    
    device = get_object_or_404(Device, pk=device)
    
    context = {
        'device': device,
        'last_location': Location.objects.filter(device=device).order_by('-sent_date_time')[0].location.coords,
        'last_log': Log.objects.filter(device=device).order_by('-received_date_time')[0],
        'last_sms': SMS.objects.filter(device=device).order_by('-send_time')[0],
        'last_battery': BatteryCharge.objects.filter(device=device).order_by('-sent_date_time')[0],
        'device_events': DeviceEvent.objects.filter(device=device).order_by('-sent_date_time')
    }
    
    return render_to_response('manager/device.html', context, context_instance=RequestContext(request))

@login_required
def render_index(request):
    
    devices = []
    danger_devices = []
    for device in Device.objects.all():
        try:
            device.last_heard = Log.objects.filter(device=device).order_by('-received_date_time')[0].received_date_time
            if device.last_heard < datetime.now() - timedelta(hours=12):
                danger_devices.append(device)
        except IndexError:
            device.last_heard = 'Never'
            danger_devices.append(device)
        devices.append(device)
    
    context = {
        'danger_sim': Sim.objects.filter(data_plan_expiry__lt=datetime.now() - timedelta(days=3)),
        'danger_device': danger_devices,
        'deployments': Deployment.objects.all()
    }
    
    return render_to_response('manager/index.html', context, context_instance=RequestContext(request))