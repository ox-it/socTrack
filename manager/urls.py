from django.conf.urls.defaults import *

urlpatterns = patterns('manager',
    (r'^device/(?P<device>\d+)$', 'views.render_device'),
)
