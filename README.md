# socTrack

A Django application which allows the management, deployment and non-real-time analysis of outputs from GPS devices (specifically GL-100 s).

## Requirements:

* South
* PostGIS / PostgreSQL
* GeoDjango
* Reverse Geocode branch of Geopy: pip install svn+http://geopy.googlecode.com/svn/branches/reverse-geocode
* matlibplot

## Log Server

### Requirements:

* Twisted

### log_server.py provides a Twisted server which listens for GPS logging data from
a GL-100 GPS tracker and imports it into the Django app.
