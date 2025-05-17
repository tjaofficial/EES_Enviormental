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

@register.filter
def complete_check(item, selector):
    list = item['complete'] if selector == "true" else item['incomplete']
    print(selector)
    return list

@register.filter
def empty_check(item, selector):
    empty = len(item['complete']) if selector == "true" else len(item['incomplete'])
    return empty
    
    
