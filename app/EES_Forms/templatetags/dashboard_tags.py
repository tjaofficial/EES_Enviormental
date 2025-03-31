from django import template # type: ignore

register = template.Library()

@register.filter(name="append_list")
def appending(var_list, form_letter):
    if form_letter not in var_list:
        var_list.append(form_letter)

@register.filter
def custom_range(item, numb):
    number = int(numb)
    return range(1, number)
    
    
