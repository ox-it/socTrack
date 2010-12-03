from django.conf.urls.defaults import *

urlpatterns = patterns('logger',
    (r'^battery-charge/(?P<device>\d+)\.png$', 'views.render_battery_chart'),
)
