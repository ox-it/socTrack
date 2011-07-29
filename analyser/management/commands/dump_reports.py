import codecs
import os

from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string

from datetime import date, timedelta
from manager.models import Deployment
from analyser.views import context_for_kml

class Command(BaseCommand):
    args = 'PATH'
    help = 'Outputs KML files for the reports'
        
    def handle(self, dump_path, *args, **options):
        
        ddir = os.path.join(dump_path)
        if not os.path.exists(ddir):
            os.makedirs(ddir)
        
        for deployment in Deployment.objects.all():
            
            ddate = deployment.survey_start
            while ddate <= deployment.survey_end and ddate < date.today():
                dfile = "%s_%s.xml" % (deployment.name.strip(), ddate.strftime('%d%m%y'))
                with codecs.open(os.path.join(ddir, dfile), 'w', 'utf-8') as fd:
                    context = context_for_kml(deployment, ddate)
                    #context['locations'] = []
                    kml = render_to_string('analyser/clusters.kml', context)
                    fd.write(kml)
                ddate += timedelta(days=1)