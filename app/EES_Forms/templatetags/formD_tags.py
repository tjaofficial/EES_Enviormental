from django import template # type: ignore

register = template.Library()

@register.filter
def get_category(value, attr):
    return value[str(attr)]

@register.filter
def addNum(value, number):
    return value + str(number)

@register.filter
def get_instance(value, instance):
    values = instance.split("-")
    print(values[0])
    if values[0] == 'observer':
        if int(values[1]) == 1:
            answer = value.observer1
        elif int(values[1]) == 2:
            answer = value.observer2
        elif int(values[1]) == 3:
            answer = value.observer3
        elif int(values[1]) == 4:
            answer = value.observer4
        elif int(values[1]) == 5:
            answer = value.observer5
    elif values[0] == 'time':
        if int(values[1]) == 1:
            answer = value.time1
        elif int(values[1]) == 2:
            answer = value.time2
        elif int(values[1]) == 3:
            answer = value.time3
        elif int(values[1]) == 4:
            answer = value.time4
        elif int(values[1]) == 5:
            answer = value.time5
    elif values[0] == 'date':
        if int(values[1]) == 1:
            answer = value.date1
        elif int(values[1]) == 2:
            answer = value.date2
        elif int(values[1]) == 3:
            answer = value.date3
        elif int(values[1]) == 4:
            answer = value.date4
        elif int(values[1]) == 5:
            answer = value.date5
    elif values[0] == 'freeboard':
        if int(values[1]) == 1:
            answer = value.freeboard1
        elif int(values[1]) == 2:
            answer = value.freeboard2
        elif int(values[1]) == 3:
            answer = value.freeboard3
        elif int(values[1]) == 4:
            answer = value.freeboard4
        elif int(values[1]) == 5:
            answer = value.freeboard5
    elif values[0] == 'comments':
        if int(values[1]) == 1:
            answer = value.comments1
        elif int(values[1]) == 2:
            answer = value.comments2
        elif int(values[1]) == 3:
            answer = value.comments3
        elif int(values[1]) == 4:
            answer = value.comments4
        elif int(values[1]) == 5:
            answer = value.comments5
    elif values[0] == 'truck_id':
        if int(values[1]) == 1:
            answer = value.truck_id1
        elif int(values[1]) == 2:
            answer = value.truck_id2
        elif int(values[1]) == 3:
            answer = value.truck_id3
        elif int(values[1]) == 4:
            answer = value.truck_id4
        elif int(values[1]) == 5:
            answer = value.truck_id5
    elif values[0] == 'contents':
        if int(values[1]) == 1:
            answer = value.contents1
        elif int(values[1]) == 2:
            answer = value.contents2
        elif int(values[1]) == 3:
            answer = value.contents3
        elif int(values[1]) == 4:
            answer = value.contents4
        elif int(values[1]) == 5:
            answer = value.contents5
    elif values[0] == 'wetted':
        if int(values[1]) == 1:
            answer = value.wetted1
        elif int(values[1]) == 2:
            answer = value.wetted2
        elif int(values[1]) == 3:
            answer = value.wetted3
        elif int(values[1]) == 4:
            answer = value.wetted4
        elif int(values[1]) == 5:
            answer = value.wetted5
    return answer