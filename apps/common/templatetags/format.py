from django import template

from common.format import currency

register = template.Library()

@register.filter
def currency_format(value):
    return currency(value)

