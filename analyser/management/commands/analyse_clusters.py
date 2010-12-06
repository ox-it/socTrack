from django.core.management.base import BaseCommand, CommandError

from manager.models import Device
from analyser.analyse import analyse

class Command(BaseCommand):
    args = ''
    help = 'Analyses location data and creates clusters'          
        
    def handle(self, *args, **options):
        # Remove existing clusters
        Cluster.objects.all().delete()
        
        # Consider each device one at a time
        for device in Device.objects.all():
            locations, passone, passtwo = analyse(device)
            
            print device.local_id + " points created: " + str(len(locations)) + " pass one iterations: " + str(passone) + " pass two iterations: " + str(passtwo)