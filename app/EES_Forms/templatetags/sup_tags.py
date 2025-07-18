from django import template # type: ignore
from ..models import the_packets_model, form_settings_model
import json
import datetime
register = template.Library()

@register.filter(name="is_string")
def is_string(var):
    return isinstance(var, str)

@register.filter(name='get_range') 
def get_range(number):
    return range(1, number+1)

@register.filter(name='to_int') 
def to_int(number):
    return int(number)

@register.filter(name='list_of_packets') 
def list_of_packets(facility):
    packetQuery = the_packets_model.objects.filter(facilityChoice__facility_name=facility, formList__settings__active=True)
    listOfPacketIDs = []
    for allPacs in packetQuery:
        listOfPacketIDs.append(allPacs.id)
    listOfPacketIDs = json.dumps(listOfPacketIDs)
    return listOfPacketIDs

@register.filter(name='string')
def string(item):
    return str(item)

@register.filter(name='dateParse')
def dateParse(string):
    parseDate = datetime.datetime.strptime(string, "%Y-%m-%d").date()
    return parseDate

@register.filter(name='dateCheck')
def dateCheck(string):
    parseDate = datetime.datetime.strptime(string, "%Y-%m-%d").date()
    if parseDate < datetime.datetime.today().date():
        return False
    else:
        return True
    
@register.filter
def total_active_packet_forms(formsList):
    newList = []
    for key, form in formsList.items(): 
        fsSelect = form_settings_model.objects.get(id=form['settingsID'])
        if form['active'] and fsSelect.settings['active']:
            newList.append(form)
    print(newList)
    total_forms = len(newList)
    return total_forms

@register.filter
def get_month_from_date_string(item):
    month = datetime.datetime.strptime(item, "%Y-%m-%d").month
    return month