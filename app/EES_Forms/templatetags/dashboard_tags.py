from django import template # type: ignore

register = template.Library()

@register.filter(name="append_list")
def appending(var_list, form_letter):
    if form_letter not in var_list:
        var_list.append(form_letter)

@register.filter(name="rangeFrom1")
def rangeFrom1(number):
    if number == 'eleven':
        return range(1,12)
    
    
