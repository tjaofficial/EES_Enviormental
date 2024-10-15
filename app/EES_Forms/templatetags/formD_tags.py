from django import template # type: ignore

register = template.Library()

@register.filter
def get_category(value, attr):
    return value[str(attr)]

@register.filter
def addNum(value, number):
    return value + str(number)