from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from manager.models import Device
from analyser.analyse import analyse

class Command(BaseCommand):
    args = ''
    help = 'Analyses location data and creates clusters'          
        
    def handle(self, *args, **options):
        
        # Consider each device one at a time
        for device in Device.objects.all():
            with transaction.commit_on_success():
                locations, passone, passtwo = analyse(device)

