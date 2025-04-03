from django import template # type: ignore

register = template.Library()

@register.filter
def get_category(value, attr):
    return value[str(attr)]

@register.filter
def exist(value, key):
    if key in value.keys():
        return True
    else:
        return False

@register.filter
def addNum(value, number):
    return value + str(number)

@register.simple_tag
def get_instance(form, label, numb, selector):
    inputOpts = ['observer', 'time', 'date', 'freeboard', 'comments', 'truck_id', 'contents', 'wetted']
    for iLabel in inputOpts:
        if label == iLabel:
            label_w_numb = f"{iLabel}{numb}"
            answer = getattr(form, label_w_numb) if selector != "form" else form[label_w_numb]
    print(answer)
    return answer