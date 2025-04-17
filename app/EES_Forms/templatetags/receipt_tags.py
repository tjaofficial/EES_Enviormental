from django import template # type: ignore
import json

register = template.Library()

@register.filter
def get_registration_cost(item):
    cost = int(item) * 75
    return cost 