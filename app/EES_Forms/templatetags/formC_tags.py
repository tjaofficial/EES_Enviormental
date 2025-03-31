from django import template # type: ignore
import json

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_list_item(lst, index):
    print(lst)
    try:
        return lst[index]
    except (IndexError, KeyError):
        return ''

@register.filter
def get_category(value, attr):
    return value[str(attr)]

@register.filter
def get_json_item(json_data, key):
    """Safely get an item from a JSONField or dictionary."""
    if isinstance(json_data, str):
        try:
            json_data = json.loads(json_data)  # Convert JSON string to a dictionary
        except json.JSONDecodeError:
            return ""  # Return empty if JSON is invalid
    
    if isinstance(json_data, dict):  
        return json_data.get(key, "")  # Get value or return empty string
    return ""  # If not a dict, return empty string

@register.filter
def get_attr(form, attr_name):
    if hasattr(form, 'cleaned_data') and attr_name in form.cleaned_data:
        return form.cleaned_data.get(attr_name)
    elif hasattr(form, 'initial') and attr_name in form.initial:
        return form.initial.get(attr_name)
    elif attr_name in form.data:  # Handles unvalidated POST data
        return form.data.get(attr_name)
    return None

@register.filter
def get_area_name(value, item):
    field_name = f"{item}_selection"
    print(item)
    try:
        return value[field_name] if field_name in value.fields else None
    except:
        return getattr(value, f"area_json_{item}")['selection']

@register.filter
def get_area_start(value, item):
    field_name = f"{item}_start"
    try:
        return value[field_name] if field_name in value.fields else None
    except:
        return getattr(value, f"area_json_{item}")['start_time']


@register.filter
def get_area_stop(value, item):
    field_name = f"{item}_stop"
    try:
        return value[field_name] if field_name in value.fields else None
    except:
        return getattr(value, f"area_json_{item}")['stop_time']



@register.simple_tag
def get_reading_input(value, areaNumb, readingNumb):
    field_name = f"{areaNumb}Read_{readingNumb}"
    try:
        return value[field_name] if field_name in value.fields else None
    except:
        return getattr(value, f"area_json_{areaNumb}")['readings'][str(readingNumb)] if getattr(value, f"area_json_{areaNumb}") != {} else ""

@register.simple_tag
def get_area_attr(value, areaNumb, attr):
    field_name = f"{areaNumb}_{attr}"
    try:
        return value[field_name] if field_name in value.fields else None
    except:
        return getattr(value, f"area_json_{areaNumb}")[attr] if getattr(value, f"area_json_{areaNumb}") != {} else ""








@register.filter
def area1_json(form, numb):
    field_name = f"1Read_{numb}"
    """Retrieve a form field dynamically by name"""
    return form[field_name] if field_name in form.fields else None

@register.filter
def area2_json(form, numb):
    field_name = f"2Read_{numb}"
    """Retrieve a form field dynamically by name"""
    return form[field_name] if field_name in form.fields else None