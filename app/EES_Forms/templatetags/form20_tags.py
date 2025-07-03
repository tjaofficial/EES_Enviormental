from django import template # type: ignore
from ..utils.main_utils import get_day_number_from_name
from django.forms import BaseForm # type: ignore
from datetime import datetime
register = template.Library()

@register.filter
def get_obser_input(obj, day_name):
    day_numb = get_day_number_from_name(day_name)
    attribute = f"obser_{day_numb}"
    if isinstance(obj, BaseForm):
        return obj[attribute]
    elif hasattr(obj, 'data') and isinstance(obj.data, dict):
        data = obj.data.get(day_name)
        if data:
            return data.get("observer", "")
        else:
            return ""
    else:
            return ""
        

@register.filter
def get_time_input(obj, day_name):
    day_numb = get_day_number_from_name(day_name)
    attribute = f"time_{day_numb}"
    if isinstance(obj, BaseForm):
        return obj[attribute]
    elif hasattr(obj, 'data') and isinstance(obj.data, dict):
        data = obj.data.get(day_name)
        if data:
            raw_time = data.get("time", "")
            if raw_time:
                try:
                    # Convert "14:30" → datetime object → "2:30 PM"
                    try:
                        dt = datetime.strptime(raw_time, "%H:%M:%S")
                    except ValueError:
                        dt = datetime.strptime(raw_time, "%H:%M")
                    return dt.strftime("%-I:%M %p")
                except ValueError:
                    return raw_time
        else:
            return ""
    else:
            return ""
