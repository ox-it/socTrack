import os

from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string

from datetime import date, timedelta
from manager.models import Deployment
from analyser.views import context_for_kml

DUMP_FOLDER = '/home/chris/tmp'

class Command(BaseCommand):
    args = ''
    help = 'Outputs KML files for the reports'
        
    def handle(self, *args, **options):
        
        for deployment in Deployment.objects.all():
            
            ddir = os.path.join(DUMP_FOLDER, str(deployment.pk))
            if not os.path.exists(ddir):
                os.makedirs(ddir)
            
            ddate = deployment.survey_start
            while ddate <= deployment.survey_end and ddate < date.today():
                with open(os.path.join(ddir, ddate.isoformat() + '.kml'), 'w') as fd:
                    kml = render_to_string('analyser/clusters.kml',
                                           context_for_kml(deployment, ddate))
                    fd.write(kml)
                ddate += timedelta(days=1)