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