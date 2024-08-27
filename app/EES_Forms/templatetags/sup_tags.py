from django import template
from ..models import the_packets_model
import json
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
    packetQuery = the_packets_model.objects.filter(facilityChoice__facility_name=facility)
    listOfPacketIDs = []
    for allPacs in packetQuery:
        listOfPacketIDs.append(allPacs.id)
    listOfPacketIDs = json.dumps(listOfPacketIDs)
    return listOfPacketIDs