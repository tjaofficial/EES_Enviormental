from django import template # type: ignore
from datetime import datetime

register = template.Library()

@register.filter
def str_to_time(value):
    try:
        return datetime.strptime(value, "%H:%M:%S").time()
    except ValueError:
        return value  # Return original if parsing fails