from django import template
from..models import *

register = template.Library()


@register.simple_tag
def added_days(poop):
    form_date = poop.form.date
    year = form_date.year
    month = form_date.month
    day = form_date.day
    if len(str(day)) == 1 :
        day = "0" + str(day)
    if len(str(month)) == 1 :
        day = "0" + str(month)
    base_date = (str(year) + "/" + str(month) + "/" + str(day))
       
    added_date = poop.form.date + datetime.timedelta(days=91)
    year2 = added_date.year
    month2 = added_date.month
    day2 = added_date.day
    if len(str(day2)) == 1 :
        day = "0" + str(day2)
    if len(str(month2)) == 1 :
        day = "0" + str(month2)
    base_date2 = (str(year2) + "/" + str(month2) + "/" + str(day2))
    return base_date2
    