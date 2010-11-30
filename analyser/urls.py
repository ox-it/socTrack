from django.conf.urls.defaults import *

urlpatterns = patterns('analyser',
    (r'^(?P<imei>[^.]+)\.kml$', 'views.render_kml'),
)
