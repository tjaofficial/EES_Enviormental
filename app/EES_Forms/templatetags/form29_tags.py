from django import template # type: ignore

register = template.Library()

@register.filter
def loop_range(value):
    return range(int(value))

@register.filter
def dynamic_attr(obj, attr_name):
    print(attr_name)
    print(obj)
    return getattr(obj, attr_name, "")