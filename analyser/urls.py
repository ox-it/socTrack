from django.conf.urls.defaults import *

urlpatterns = patterns('analyser',
    (r'^(?P<deployment>\d+)\.kml$', 'views.render_kml'),
    (r'^(?P<deployment>\d+)\.html$', 'views.render_report'),
)
