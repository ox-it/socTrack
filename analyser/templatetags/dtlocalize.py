from django import template
from dateutil.tz import tzutc, tzlocal

register = template.Library()

@register.filter
def dtlocalize(value):
    return value.replace(tzinfo=tzutc()).astimezone(tzlocal())

@register.filter
def dtkml(value):
    return dtlocalize(value).isoformat()