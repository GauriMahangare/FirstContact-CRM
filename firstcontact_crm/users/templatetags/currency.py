from datetime import datetime
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter('convert_to_money')
def convert_to_money(amount):
    return int(amount)/100