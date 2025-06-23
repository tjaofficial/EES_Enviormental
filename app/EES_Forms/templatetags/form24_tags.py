from django import template # type: ignore

register = template.Library()

@register.filter
def getfield(form, field_name):
    try:
        item = form[field_name]
    except:
        dataAttr = getattr(form, 'data')
        item = dataAttr[field_name]
    return item