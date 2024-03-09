from django import template

register = template.Library()

@register.filter(name="is_string")
def is_string(var):
    return isinstance(var, str)

@register.filter(name='get_range') 
def get_range(number):
    return range(1, number+1)

@register.filter(name='to_int') 
def to_int(number):
    return int(number)