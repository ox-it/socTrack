from django import template
from dateutil.tz import tzutc, tzlocal
from datetime import datetime

register = template.Library()

@register.filter
def dtlocalize(value):
    if isinstance(value, datetime):
        return value.replace(tzinfo=tzutc()).astimezone(tzlocal())
    else:
        return value

@register.filter
def dtkml(value):
    return dtlocalize(value).isoformat()