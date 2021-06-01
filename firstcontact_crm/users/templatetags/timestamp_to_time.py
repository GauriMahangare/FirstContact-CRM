from datetime import datetime
from django import template

register = template.Library()

@register.filter('timestamp_to_time')
def convert_timestamp_to_time(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%d %B %Y')

@register.filter('convert_to_money')
def convert_to_money(amount):
    print(amount)
    return int(amount)/100