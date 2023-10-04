from django import template

register = template.Library()

@register.filter(name="append_list")
def appending(var_list, form_letter):
    if form_letter not in var_list:
        var_list.append(form_letter)
    
    
