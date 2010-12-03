from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from matplotlib.ticker import FixedLocator
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from manager.models import Device
from logger.models import BatteryCharge

@login_required
def render_battery_chart(request, device):
    device = get_object_or_404(Device, pk=device)
    
    fig = Figure(figsize=(3,3))
    ax = fig.add_subplot(111)
    x = [b.sent_date_time for b in BatteryCharge.objects.filter(device=device)]
    y = [b.battery_percentage for b in BatteryCharge.objects.filter(device=device)]
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response