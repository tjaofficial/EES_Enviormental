from datetime import datetime
from django import template # type: ignore

register = template.Library()

# Example string
@register.filter
def parse_time(time_str):
    formatted_time = datetime.strptime(time_str, "%H:%M:%S").strftime("%I:%M %p")
    print(formatted_time)
    return formatted_time