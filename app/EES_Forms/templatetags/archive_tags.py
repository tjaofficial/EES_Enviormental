from django import template # type: ignore

register = template.Library()

@register.filter
def get_date_day(item, formID):
    if formID in ["24", "25"]:
        return item.weekend_day
    else:
        print("Not Needed")
    