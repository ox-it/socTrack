from collections import deque
from datetime import datetime

from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

from django.contrib.gis.geos import Point

from manager.models import Device
from logger.models import Log, Location, DeviceEvent, BatteryCharge

LOG_PORT = 23456

class GL100(LineReceiver):
    """
    Implements the protocol that GL-100 devices send
    """
    
    delimiter = '\0'
    
    @staticmethod
    def dtstring_to_datetime(dtsring):
        """
        Takes the datetime string given by the GL-100 and converts it into
        Python datetime object
        """
        return datetime(int(dtsring[0:4]), int(dtsring[4:6]), int(dtsring[6:8]), int(dtsring[8:10]), int(dtsring[10:12]), int(dtsring[12:14]))
    
    @staticmethod
    def parse_data(raw):
        """
        Parse the data and return a dictionary
        """
        data = deque(raw.split(","))
        processed = dict()
        
        # Response types
        location_responses = {'GTLBC': "Location Base Call", 'GTTRI': "Timed Report Information",'GTSZI': "Safe Zone Information",'GTSOS': "Save Our Souls",'GTRTL': "Real Time Location"}
        power_responses = {'GTCBC': "Battery Check Response"}
        event_responses = {'GTPNA': "Power On Alarm",'GTPFA': "Power Off Alarm",'GTPLA': "Power Low Alarm"}
        general_information_responses = {'GTCID': "CID Info?",'GTHWV': "Hardware Information?", 'GTINF': "General Information?"}
        
        # Common header to all response types
        header_type, header_tail = data.popleft().split(":")
        processed.update({
            'imei': data.popleft(),
            'raw': raw
        })
        
        if header_type == '+RESP':
            
            # Location Responses 
            if header_tail in location_responses:
                processed['type'] = 'location'
                if header_tail == 'GTLBC': # Used as a response to when the device is rung
                    data.popleft() # Requesting phone number
                    processed['locations'] = [
                        {
                            'fix': data.popleft(), # GPS fix
                            'speed': data.popleft(), # Speed
                            'heading': data.popleft(), # Heading
                            'altitude': data.popleft(), # Altitude
                            'accuracy': data.popleft(), # GPS accuracy
                            'longitude': data.popleft(), # Longitude
                            'latitude': data.popleft(), # Latitude
                            'send_dt': GL100.dtstring_to_datetime(data.popleft()), # Send time
                            'is_sos': header_tail == 'GTSOS',
                        }
                    ]
                    data.popleft() # Unknown (234)
                    data.popleft() # Unknown 10
                    data.popleft() # Unknown (08d2)
                    data.popleft() # Unknown
                    data.popleft() # Unknown
                    
                else: # Possible to have a variable number of entries in this one packet (dependant on 'responses')
                    processed['locations'] = []
                    if header_tail == 'GTTRI':
                        responses = int(data.popleft())
                    else:
                        # GTRTL, GTSZI, GTSOS do not use the 'responses' field
                        data.popleft()
                        responses = 1
                    while responses > 0:
                        data.popleft() # Zone ID
                        data.popleft() # Zone alert
                        processed['locations'].append(
                            {
                                'fix': data.popleft(), # GPS fix
                                'speed': data.popleft(), # Speed
                                'heading': data.popleft(), # Heading
                                'altitude': data.popleft(), # Altitude
                                'accuracy': data.popleft(), # GPS accuracy
                                'longitude': data.popleft(), # Longitude
                                'latitude': data.popleft(), # Latitude
                                'send_dt': GL100.dtstring_to_datetime(data.popleft()), # Send time
                                'is_sos': False,
                            }
                        )
                        data.popleft() # Unknown (234)
                        data.popleft() # Unknown 10
                        data.popleft() # Unknown (08d2)
                        data.popleft() # Unknown
                        data.popleft() # Unknown
                        responses -= 1
            
            # Power Response
            elif header_tail in power_responses:
                processed.update({
                    'type': 'battery_charge',
                    'percentage': data.popleft(),
                    'send_dt': GL100.dtstring_to_datetime(data.popleft()),
                })
            
            # Events
            elif header_tail in event_responses:
                processed.update({
                    'type': 'event',
                    'event': event_responses[header_tail],
                    'send_dt': GL100.dtstring_to_datetime(data.popleft()),
                })
            
            else:
                processed['type'] = 'unknown'
            
        else:
            # Received Acknowledgement Message
            processed['type'] = 'response'
        
        return processed

    def lineReceived(self, line):
        print line
        data = self.parse_data(line)
        
        # First off, write this line to the log whole
        log = self.factory.record_log(data['imei'], data['raw'])
        
        # Now update our models as appropriate
        if data['type'] == 'location':
            for location in data['locations']:
                self.factory.record_location(log, data['imei'], **location)
        
        elif data['type'] == 'battery_charge':
            self.factory.record_battery_charge(log, **data)
        
        elif data['type'] == 'event':
            self.factory.record_event(log, **data)

class DjangoLoggingFactory(ServerFactory):
    """
    A factory which logs GPS location data to Django models
    """
    
    def __init__(self, protocol):
        self.protocol = protocol
    
    def record_log(self, imei, line):
        device, created = Device.objects.get_or_create(imei=imei)
        l = Log(device=device, received_date_time=datetime.now(), message=line)
        l.save()
        return l
    
    def record_location(self, log, imei, fix, speed, heading, altitude, accuracy, longitude, latitude, send_dt, is_sos, **kwargs):
        device, created = Device.objects.get_or_create(imei=imei)
        if int(fix) == 1:
            Location(device=device, message=log, speed=speed, heading=heading, altitude=altitude, accuracy=accuracy, location=Point(float(longitude), float(latitude)), sent_date_time=send_dt, sos=is_sos).save()

    def record_battery_charge(self, log, imei, percentage, send_dt, **kwargs):
        device, created = Device.objects.get_or_create(imei=imei)
        BatteryCharge(device=device, sent_date_time=send_dt, message=log, battery_percentage=percentage).save()
    
    def record_event(self, log, imei, event, send_dt, **kwargs):
        device, created = Device.objects.get_or_create(imei=imei)
        DeviceEvent(device=device, sent_date_time=send_dt, message=log, event=event).save()

if __name__ == '__main__':
    
    # Start the server
    reactor.listenTCP(LOG_PORT, DjangoLoggingFactory(GL100))
    reactor.run()