from django import template # type: ignore

register = template.Library()

@register.filter
def get_item(dictionary, key):
    print('hello')
    print(dictionary)
    return dictionary.get(key)

@register.filter
def get_list_item(lst, index):
    try:
        return lst[index]
    except (IndexError, KeyError):
        return ''
