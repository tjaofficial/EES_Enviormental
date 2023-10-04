from django import template

register = template.Library()

@register.filter(name="is_string")
def is_string(var):
    return isinstance(var, str)