from urllib2 import urlopen

import simplejson

from secrets import secrets

YAHOO_PLACEFINDER_URL = 'http://where.yahooapis.com/geocode?appid=%s&flags=GJTX&gflags=AR&location=%%f%%%%20%%f' % secrets['YAHOO']

def reverse_geocode(lat, lon):
    geocode = simplejson.load(urlopen(YAHOO_PLACEFINDER_URL % (lat, lon)))
    return '%s, %s%s, %s' % (
        geocode['ResultSet']['Results'][0]['line1'],
        (geocode['ResultSet']['Results'][0]['level4'] + ', ') if geocode['ResultSet']['Results'][0]['level4'] else '',
        geocode['ResultSet']['Results'][0]['level3'],
        geocode['ResultSet']['Results'][0]['level2'])
