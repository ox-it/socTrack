from django.conf.urls.defaults import *

urlpatterns = patterns('analyser',
    (r'^(?P<deployment>\d+)\.kml$', 'views.render_kml'),
)
