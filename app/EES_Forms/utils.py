from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import *
from django.db.models import Q # type: ignore
from django.apps import apps # type: ignore
import ast
import requests # type: ignore
import json
import braintree # type: ignore
import os
import calendar
import random
import string
import time
from django.shortcuts import redirect # type: ignore
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from channels.layers import get_channel_layer # type: ignore
from asgiref.sync import async_to_sync # type: ignore
from django.contrib.sites.shortcuts import get_current_site   # type: ignore
from django.template.loader import render_to_string  # type: ignore
from django.utils.html import strip_tags # type: ignore
from django.core.mail import send_mail # type: ignore
from django.conf import settings # type: ignore
from django.contrib import messages # type: ignore
from django.db.models import Field, Min # type: ignore
from django.contrib.contenttypes.models import ContentType # type: ignore

#from .admin import EventAdmin
parseFormList = [
    (1, "A1"),
    (2, "A2"),
    (3, "A3"),
    (4, "A4"),
    (5, "A5"),
    (6, "B"),
    (7, "C"),
    (8, "D"),
    (9, "E"),
    (10, "F1"),
    (11, "F2"),
    (12, "F3"),
    (13, "F4"),
    (14, "F5"),
    (15, "F6"),
    (16, "F7"),
    (17, "G1"),
    (18, "G1"),
    (19, "H"),
    (20, "I"),
    (21, "L"),
    (22, "M"),
    (23, "N"),
    (24, "O"),
    (25, "P"),
    (26, "R"),
    (27, "Q"),  
]
dashDict = {
    'formsDash': True, 
    'batteryDash': False
}
dashDictOptions = {
    'formsDash': 'Default', 
    'batteryDash': 'Battery'
}
defaultBatteryDashSettings = {
    'progressBar': {
        'progressDaily': True,
        'progressWeekly': True,
        'progressMonthly': True,
        'progressQuarterly': True,
        'progressAnnually': False,
    },
    'graphs': {
        'graphFrequencyData': {
            'frequency': 'weekly',
            'dates': False
        },
        'dataChoice': {
            'charges': {
                'show': True,
                'type': 'bar'
            },
            'doors': {
                'show': True,
                'type': 'bar'
            },
            'lids': {
                'show': True,
                'type': 'bar'
            },
            'graph90dayPT': {
                'show': False,
                'type': 'bar'
            },
        }
    },
    'correctiveActions': True,
    'infoWeather': True,
    '90dayPT': True,
    'contacts': True
}
defaultNotifications = {
        'compliance': True,
        'deviations': True,
        'submitted': True,
        '10_day_pt': False,
        '5_day_pt': False
}
defaultFacilitySettings = {
    'dashboard': {
        'formsDash': True,
        'batteryDash': False,
    },
    'notifications': defaultNotifications,
    'first_login': False
}
defaultFacilitySettingsParsed = json.loads(json.dumps(defaultFacilitySettings))
defaultUserSettings = {
    'colorMode': 'light',
    'landingDash': 'default'
}

defaultPacketSettings = {
    'formsList': False,
    'settings': {
        'weekly_start_day': 'saturday',
        'frequency': 'weekly'
    }
}

g1Settings = {
    'height_above_ground_level': 120,
    'describe_emissions_point_start': 'Above Stack',
    'describe_emissions_point_stop': 'Same',
    'process_equip1': "PECS Baghouse Stack",
    'operating_mode1': "normal",
    'process_equip2': "-",
    'operating_mode2': "-",
}

g2Settings = {
    'height_above_ground_level': 120,
    'describe_emissions_point_start': 'Above Stack',
    'describe_emissions_point_stop': 'Same',
    'process_equip1': "PECS Baghouse Stack",
    'operating_mode1': "normal",
    'process_equip2': "-",
    'operating_mode2': "-",
}

hDefaultSettings = {
    "custom_name": False, 
    'height_above_ground_level': 350,
    'describe_emissions_point_start': 'Above Stack',
    'describe_emissions_point_stop': 'Same',
    'process_equip1': "Combustion Stack",
    'operating_mode1': "normal",
    'process_equip2': "-",
    'operating_mode2': "-",
}
cDefaultSettings = {
    "custom_name": "Coal Field Inspections", 
    "number_of_areas": "4", 
    "area1": {
        "name": "Trucks",
        "number_of_options": 7,
        "options": {
            "Contractor": "meat",
            "#5": "meat",
            "#6": "meat",
            "#7": "meat",
            "#9": "meat",
            "Dozer": "meat",
            "Water Truck": "meat"
        }
    }, 
    "area2": {
        "name": "Coal Storage Areas",
        "number_of_options": 5,
        "options": {
            "Panther Eagle": "meat",
            "Kepler": "meat",
            "Rock Lick": "meat",
            "McClure": "meat",
            "Elk Valley": "meat"
        }
    }, 
    "area3": {
        "name": "Area B Coke Storage",
        "number_of_options": 0,
        "options": {}
    }, 
    "area4": {
        "name": "Salt Pile",
        "number_of_options": 0,
        "options": {}
    }
}
iDefaultSettings = {
    "custom_name": False,
    "days_weekly": 5,

}

braintreeSettings = {
    "account": {
        "customer_ID": "item",
        "status": "item",
    },
    "subscription": {
        "subscription_ID": "item",
        "plan_id": "item",
        "plan_name": "item",
        "price": "item",
        "registrations": "item",
        "next_billing_date": "item",
        "status": "item",
    },
    "payment_methods": {
        "default": {
            "type": "item",
            "card_name": "item",
            "payment_token": "item",
            "last_4": "item",
            "exp_month": "item",
            'exp_year': "item"
        }
    },
    "past_subscriptions": {
        "1": {
            "subscription_ID": "item",
            "start_date": "item",
            "end_date": "item"
        },
        "2": {
            "subscription_ID": "item",
            "start_date": "item",
            "end_date": "item"
        }
    }
}

def formA5_Model_Upadte():
    allFormData = form5_model.objects.all()   
    not_these_fields = [
        'date',
        'estab',
        'county',
        'estab_no',
        'equip_loc',
        'district',
        'city',
        'observer',
        'cert_date',
        'id',
        'facilityChoice',
        'notes',
        'canvas',
        'reading_data',
        'ovens_data',
        'formSettings'
    ]
    for record in allFormData:
        fieldsList = [field.name for field in record._meta.get_fields() if isinstance(field, Field) and field.name not in not_these_fields]
        finalJson = json.loads(json.dumps({fieldName: getattr(record, fieldName) for fieldName in fieldsList}))
        record.reading_data = finalJson
        record.save()
        

    
    print("hello")

def formA5_Readings_Upadte():
    allFormData = form5_readings_model.objects.all() 
    #not_these_fields = ['form']
    for record in allFormData:
        #fieldsList = [field.name for field in record._meta.get_fields() if isinstance(field, Field) and field.name not in not_these_fields]
        #print(fieldsList)
        formA5Ovens = {
            "oven1": {
                "oven_number": record.o1,
                "start": str(record.o1_start),
                "stop": str(record.o1_stop),
                "highest_opacity": record.o1_highest_opacity,
                "opacity_over_20": record.o1_instant_over_20,
                "average_6_opacity": record.o1_average_6,
                "average_6_over_35": record.o1_average_6_over_35,
                "readings": {
                    "push":{
                        "1": record.o1_1_reads,
                        "2": record.o1_2_reads,
                        "3": record.o1_3_reads,
                        "4": record.o1_4_reads,
                        "5": record.o1_5_reads,
                        "6": record.o1_6_reads,
                        "7": record.o1_7_reads,
                        "8": record.o1_8_reads,
                    },
                    "travel": {
                        "1": record.o1_9_reads,
                        "2": record.o1_10_reads,
                        "3": record.o1_11_reads,
                        "4": record.o1_12_reads,
                        "5": record.o1_13_reads,
                        "6": record.o1_14_reads,
                        "7": record.o1_15_reads,
                        "8": record.o1_16_reads,
                    }
                }
            },
            "oven2": {
                "oven_number": record.o2,
                "start": str(record.o2_start),
                "stop": str(record.o2_stop),
                "highest_opacity": record.o2_highest_opacity,
                "opacity_over_20": record.o2_instant_over_20,
                "average_6_opacity": record.o2_average_6,
                "average_6_over_35": record.o2_average_6_over_35,
                "readings": {
                    "push":{
                        "1": record.o2_1_reads,
                        "2": record.o2_2_reads,
                        "3": record.o2_3_reads,
                        "4": record.o2_4_reads,
                        "5": record.o2_5_reads,
                        "6": record.o2_6_reads,
                        "7": record.o2_7_reads,
                        "8": record.o2_8_reads,
                    },
                    "travel": {
                        "1": record.o2_9_reads,
                        "2": record.o2_10_reads,
                        "3": record.o2_11_reads,
                        "4": record.o2_12_reads,
                        "5": record.o2_13_reads,
                        "6": record.o2_14_reads,
                        "7": record.o2_15_reads,
                        "8": record.o2_16_reads,
                    }
                }
            },
            "oven3": {
                "oven_number": record.o3,
                "start": str(record.o3_start),
                "stop": str(record.o3_stop),
                "highest_opacity": record.o3_highest_opacity,
                "opacity_over_20": record.o3_instant_over_20,
                "average_6_opacity": record.o3_average_6,
                "average_6_over_35": record.o3_average_6_over_35,
                "readings": {
                    "push":{
                        "1": record.o3_1_reads,
                        "2": record.o3_2_reads,
                        "3": record.o3_3_reads,
                        "4": record.o3_4_reads,
                        "5": record.o3_5_reads,
                        "6": record.o3_6_reads,
                        "7": record.o3_7_reads,
                        "8": record.o3_8_reads,
                    },
                    "travel": {
                        "1": record.o3_9_reads,
                        "2": record.o3_10_reads,
                        "3": record.o3_11_reads,
                        "4": record.o3_12_reads,
                        "5": record.o3_13_reads,
                        "6": record.o3_14_reads,
                        "7": record.o3_15_reads,
                        "8": record.o3_16_reads,
                    }
                }
            },
            "oven4": {
                "oven_number": record.o4,
                "start": str(record.o4_start),
                "stop": str(record.o4_stop),
                "highest_opacity": record.o4_highest_opacity,
                "opacity_over_20": record.o4_instant_over_20,
                "average_6_opacity": record.o4_average_6,
                "average_6_over_35": record.o4_average_6_over_35,
                "readings": {
                    "push":{
                        "1": record.o4_1_reads,
                        "2": record.o4_2_reads,
                        "3": record.o4_3_reads,
                        "4": record.o4_4_reads,
                        "5": record.o4_5_reads,
                        "6": record.o4_6_reads,
                        "7": record.o4_7_reads,
                        "8": record.o4_8_reads,
                    },
                    "travel": {
                        "1": record.o4_9_reads,
                        "2": record.o4_10_reads,
                        "3": record.o4_11_reads,
                        "4": record.o4_12_reads,
                        "5": record.o4_13_reads,
                        "6": record.o4_14_reads,
                        "7": record.o4_15_reads,
                        "8": record.o4_16_reads,
                    }
                }
            }
        }
        #finalJson = json.loads(json.dumps({fieldName: getattr(record, fieldName) for fieldName in fieldsList}))
        record.form.ovens_data = json.loads(json.dumps(formA5Ovens))
        record.form.save()
        print("hello2")

def formA5_ovens_data_build(requestPOST):
    ovens_data = {
        "oven1": {
            "oven_number": requestPOST['o1'],
            "start": str(requestPOST['o1_start']),
            "stop": str(requestPOST['o1_stop']),
            "highest_opacity": requestPOST['o1_highest_opacity'],
            "opacity_over_20": requestPOST['o1_instant_over_20'],
            "average_6_opacity": requestPOST['o1_average_6'],
            "average_6_over_35": requestPOST['o1_average_6_over_35'],
            "readings": {
                "push":{
                    "1": requestPOST['o1_1_reads'],
                    "2": requestPOST['o1_2_reads'],
                    "3": requestPOST['o1_3_reads'],
                    "4": requestPOST['o1_4_reads'],
                    "5": requestPOST['o1_5_reads'],
                    "6": requestPOST['o1_6_reads'],
                    "7": requestPOST['o1_7_reads'],
                    "8": requestPOST['o1_8_reads'],
                },
                "travel": {
                    "1": requestPOST['o1_9_reads'],
                    "2": requestPOST['o1_10_reads'],
                    "3": requestPOST['o1_11_reads'],
                    "4": requestPOST['o1_12_reads'],
                    "5": requestPOST['o1_13_reads'],
                    "6": requestPOST['o1_14_reads'],
                    "7": requestPOST['o1_15_reads'],
                    "8": requestPOST['o1_16_reads'],
                }
            }
        },
        "oven2": {
            "oven_number": requestPOST['o2'],
            "start": str(requestPOST['o2_start']),
            "stop": str(requestPOST['o2_stop']),
            "highest_opacity": requestPOST['o2_highest_opacity'],
            "opacity_over_20": requestPOST['o2_instant_over_20'],
            "average_6_opacity": requestPOST['o2_average_6'],
            "average_6_over_35": requestPOST['o2_average_6_over_35'],
            "readings": {
                "push":{
                    "1": requestPOST['o2_1_reads'],
                    "2": requestPOST['o2_2_reads'],
                    "3": requestPOST['o2_3_reads'],
                    "4": requestPOST['o2_4_reads'],
                    "5": requestPOST['o2_5_reads'],
                    "6": requestPOST['o2_6_reads'],
                    "7": requestPOST['o2_7_reads'],
                    "8": requestPOST['o2_8_reads'],
                },
                "travel": {
                    "1": requestPOST['o2_9_reads'],
                    "2": requestPOST['o2_10_reads'],
                    "3": requestPOST['o2_11_reads'],
                    "4": requestPOST['o2_12_reads'],
                    "5": requestPOST['o2_13_reads'],
                    "6": requestPOST['o2_14_reads'],
                    "7": requestPOST['o2_15_reads'],
                    "8": requestPOST['o2_16_reads'],
                }
            }
        },
        "oven3": {
            "oven_number": requestPOST['o3'],
            "start": str(requestPOST['o3_start']),
            "stop": str(requestPOST['o3_stop']),
            "highest_opacity": requestPOST['o3_highest_opacity'],
            "opacity_over_20": requestPOST['o3_instant_over_20'],
            "average_6_opacity": requestPOST['o3_average_6'],
            "average_6_over_35": requestPOST['o3_average_6_over_35'],
            "readings": {
                "push":{
                    "1": requestPOST['o3_1_reads'],
                    "2": requestPOST['o3_2_reads'],
                    "3": requestPOST['o3_3_reads'],
                    "4": requestPOST['o3_4_reads'],
                    "5": requestPOST['o3_5_reads'],
                    "6": requestPOST['o3_6_reads'],
                    "7": requestPOST['o3_7_reads'],
                    "8": requestPOST['o3_8_reads'],
                },
                "travel": {
                    "1": requestPOST['o3_9_reads'],
                    "2": requestPOST['o3_10_reads'],
                    "3": requestPOST['o3_11_reads'],
                    "4": requestPOST['o3_12_reads'],
                    "5": requestPOST['o3_13_reads'],
                    "6": requestPOST['o3_14_reads'],
                    "7": requestPOST['o3_15_reads'],
                    "8": requestPOST['o3_16_reads'],
                }
            }
        },
        "oven4": {
            "oven_number": requestPOST['o4'],
            "start": str(requestPOST['o4_start']),
            "stop": str(requestPOST['o4_stop']),
            "highest_opacity": requestPOST['o4_highest_opacity'],
            "opacity_over_20": requestPOST['o4_instant_over_20'],
            "average_6_opacity": requestPOST['o4_average_6'],
            "average_6_over_35": requestPOST['o4_average_6_over_35'],
            "readings": {
                "push":{
                    "1": requestPOST['o4_1_reads'],
                    "2": requestPOST['o4_2_reads'],
                    "3": requestPOST['o4_3_reads'],
                    "4": requestPOST['o4_4_reads'],
                    "5": requestPOST['o4_5_reads'],
                    "6": requestPOST['o4_6_reads'],
                    "7": requestPOST['o4_7_reads'],
                    "8": requestPOST['o4_8_reads'],
                },
                "travel": {
                    "1": requestPOST['o4_9_reads'],
                    "2": requestPOST['o4_10_reads'],
                    "3": requestPOST['o4_11_reads'],
                    "4": requestPOST['o4_12_reads'],
                    "5": requestPOST['o4_13_reads'],
                    "6": requestPOST['o4_14_reads'],
                    "7": requestPOST['o4_15_reads'],
                    "8": requestPOST['o4_16_reads'],
                }
            }
        }
    }
    return json.loads(json.dumps(ovens_data))

def formA5_readings_data_Model_Upadte():
    allFormData = form5_model.objects.all()   
    not_these_fields = [
        'date',
        'estab',
        'county',
        'estab_no',
        'equip_loc',
        'district',
        'city',
        'observer',
        'cert_date',
        'id',
        'facilityChoice',
        'notes',
        'canvas',
        'reading_data',
        'ovens_data',
        'formSettings'
    ]
    for record in allFormData:
        fieldsList = [field.name for field in record._meta.get_fields() if isinstance(field, Field) and field.name not in not_these_fields]
        print(fieldsList)
        finalJson = json.loads(json.dumps({fieldName: getattr(record, fieldName) for fieldName in fieldsList}))
        record.reading_data = finalJson
        record.save()

# takes in the database array and returns wether it is empty True/False
def DBEmpty(DBArray):
    emptyDB = False
    if len(DBArray) == 0:
        emptyDB = True
    return emptyDB

class EventCalendar(HTMLCalendar):
    def __init__(self, events=None):
        super(EventCalendar, self).__init__()
        self.events = events
 
    def formatday(self, day, weekday, events, year):
        """
        Return a day as a table cell.
        """
        events_from_day = events.filter(date__day=day)
        events_html = "<ul>"
        for event in events_from_day:
            if event.date.year == year.year:
                events_html += event.get_absolute_url2() + "<br>"
        events_html += "</ul>"
 
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, events_html)
 
    def formatweek(self, theweek, events, year):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events, year) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s
 
    def formatmonth(self, theyear, themonth, year, withyear=True):
        """
        Return a formatted month as a table.
        """
        
        events = Event.objects.filter(date__month=themonth)
 
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events, year))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)
    
class Calendar(HTMLCalendar):
    def __init__(self, events=None):
        super(Calendar, self).__init__()
        self.events = events
 
    def formatday(self, day, weekday, events, year):
        """
        Return a day as a table cell.
        """        
        events_from_day = events.filter(date__day=day)
        events_html = "<ul>"
        for event in events_from_day:
            if event.date.year == year:
                events_html += event.get_absolute_url() + "<br>"
        events_html += "</ul>"

        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, events_html)

 
    def formatweek(self, theweek, events, year):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events, year) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s
        
        
 
    def formatmonth(self, theyear, themonth, year, facility, withyear=True):
        """
        Return a formatted month as a table.
        """
        if facility == "supervisor":
            events = Event.objects.filter(date__month=themonth, personal=True)
        else:
            events = Event.objects.filter(date__month=themonth, facilityChoice__facility_name=facility)
 
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events, year))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

class PrintCalendar(HTMLCalendar):
    def __init__(self, events=None):
        super(PrintCalendar, self).__init__()
        self.events = events
 
    def formatday(self, day, weekday, events, year, type, label, forms, selectedForm):
        """
        Return a day as a table cell.
        """    
        eventCell = False    
        def formatTheDayNumber(day):
            day = str(day)
            if len(day) == 1:
                newDay = "0" + day
                return newDay
            else:
                return day
        print("COntinued....")
        forms_html = "<ul>"
        print(selectedForm)
        print(forms)
        if isinstance(selectedForm, str):
            packetsEntry = the_packets_model.objects.get(id=int(selectedForm))
            packFreq = packetsEntry.formList['settings']['frequency'].capitalize()
            def day_name_to_number(day_name):
                # Convert the day name to a date object
                date_obj = time.strptime(day_name, "%A").tm_wday
                return date_obj
            if packFreq == 'Daily':
                print("Starting to find Forms that exist on this day for daily...")
                print(forms)
                aPacketFormList = []
                for iForms in forms:
                    print(iForms.date)
                    print(day)
                    if iForms.date.day == day:
                        print(iForms.date)
                        aPacketFormList.append(iForms)
                print(aPacketFormList)
                for h in aPacketFormList:
                    if h.date.year == year:
                        selectedFormDate = h
                        if type == 'single':
                            forms_html += "<a href='../../../../printIndex/" + type + "/Daily/" + str(selectedForm) + "-" + str(label) + "/" + str(selectedFormDate.date.year) + "-" + formatTheDayNumber(selectedFormDate.date.month) +"-"+ formatTheDayNumber(selectedFormDate.date.day) +"' target='_blank'>Submitted Packet</a><br>"
                        else:
                            forms_html += "<a href='../../../../printIndex/" + type + "/Daily/" + str(selectedForm) + "/" + str(selectedFormDate.date.year) + "-" + formatTheDayNumber(selectedFormDate.date.month) +"-"+ formatTheDayNumber(selectedFormDate.date.day) +"' target='_blank'>Submitted Packet</a><br>"
                        
                        eventCell = True
                        break
            elif packFreq == 'Weekly':
                packStartDayNumber = day_name_to_number(packetsEntry.formList['settings']['weekly_start_day'].capitalize())
                print("Starting to find Forms that exist on this day for weekly...")
                wPacketFormList = []
                for iForms in forms:
                    try:
                        theDate = iForms.date
                    except:
                        theDate = iForms.week_start
                    if packStartDayNumber == 5:
                        if theDate.weekday() in [5,6]:
                            weekEnd = theDate + datetime.timedelta(days=11 - theDate.weekday())
                        else:
                            weekEnd = theDate + datetime.timedelta(days=4 - theDate.weekday())
                    elif packStartDayNumber == 0:
                        weekEnd = theDate + datetime.timedelta(days=6 - theDate.weekday())
                    elif packStartDayNumber == 6:
                        if theDate.weekday() in [5,6]:
                            if theDate.weekday() == 5: 
                                weekEnd = theDate
                            else:
                                weekEnd = theDate + datetime.timedelta(days=12 - theDate.weekday())
                        else:
                            weekEnd = theDate + datetime.timedelta(days=5 - theDate.weekday())
                    if weekEnd not in wPacketFormList:
                        wPacketFormList.append(weekEnd)
                for h in wPacketFormList:
                    if h.year == year and h.day == day:
                        print('check 1')
                        selectedFormDate = h
                        forms_html += "<a href='../../../../printIndex/" + type + "/" + packFreq + "/"+ str(selectedForm) + "/" + str(selectedFormDate.year) + "-"+ formatTheDayNumber(selectedFormDate.month) +"-"+ formatTheDayNumber(selectedFormDate.day) +"' target='_blank'>Submitted Packet</a><br>"
                        eventCell = True
                        break
            elif packFreq == 'Monthly':
                print('Monthly')
        else:
            if selectedForm[1]:
                forms_from_day = forms.filter(date__day=day)
                for form in forms_from_day:
                    if form.date.year == year:
                        if type == 'single':
                            forms_html += "<a href='../../../../printIndex/" + type + "/Daily/" + str(selectedForm[0]) + "-" + str(label) + "/" + str(form.date.year) + "-"+ formatTheDayNumber(form.date.month) +"-"+ formatTheDayNumber(form.date.day) +"' target='_blank'>Submitted Form</a><br>"
                        else:
                            forms_html += "<a href='../../../../printIndex/" + type + "/Daily/" + str(selectedForm[0]) + "-" + str(label) + "/" + str(form.date.year) + "-"+ formatTheDayNumber(form.date.month) +"-"+ formatTheDayNumber(form.date.day) +"' target='_blank'>Submitted Form</a><br>"
                        eventCell = True
            else:
                forms_from_day = forms.filter(week_start__day=day)
                for form in forms_from_day:
                    if form.week_start.year == year:
                        forms_html += "<a href='../../../../printIndex/" + type + "/Daily/" + str(selectedForm[0]) + "-" + str(label) + "/" + str(form.week_start.year) + "-"+ formatTheDayNumber(form.week_start.month) +"-"+ formatTheDayNumber(form.week_start.day) +"' target='_blank'>Submitted Form</a><br>"
                        eventCell = True
        
        forms_html += "</ul>"
        
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            if eventCell:
                return '<td style="background:#517d8e70;" class="hover %s">%d%s</td>' % (self.cssclasses[weekday], day, forms_html)
            else:
                return '<td class="hover %s">%d%s</td>' % (self.cssclasses[weekday], day, forms_html)
            

 
    def formatweek(self, theweek, events, year, type, label, forms, selectedForm):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events, year, type, label, forms, selectedForm) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s
        
    def formatmonth(self, theyear, themonth, year, type, forms, facility, withyear=True):
        """
        Return a formatted month as a table.
        """
        formSettingsQuery = form_settings_model.objects.filter(facilityChoice__facility_name=facility)
        formList = get_facility_forms('facilityName', facility)
        #ogFormID = forms
        if type == 'single':
            formsList = forms.split('-')
            forms = int(formsList[0])
            formPacket = formsList[1]
        print("start")
        print(forms)
        if isinstance(forms, str) and type == 'group':
            label = False
            print("This is a Packet Print for packetID "+forms)
            packetsEntry = the_packets_model.objects.get(id=int(forms))
            allFormsSettingsList = []
            for pacForm in packetsEntry.formList["formsList"]:
                pacfsID = packetsEntry.formList["formsList"][pacForm]['settingsID']
                for settingsEntry in formSettingsQuery:
                    if pacfsID == settingsEntry.id:
                        allFormsSettingsList.append(settingsEntry)
            print(allFormsSettingsList)
            packetExists = []
            for iFormSettings in allFormsSettingsList:
                formID = iFormSettings.formChoice.id
                formInformation = iFormSettings.formChoice
                name_of_model = formInformation.link + "_model"
                if formID == 23:
                    chk_database = form22_model.objects.filter(date__year=year, date__month=themonth, facilityChoice__facility_name=facility)
                else:
                    try:#### ----- Set up a code to switch over to a number based model instead of labels
                        chk_database = apps.get_model('EES_Forms', name_of_model).objects.filter(date__year=year, date__month=themonth, facilityChoice__facility_name=facility)
                    except:
                        chk_database = apps.get_model('EES_Forms', name_of_model).objects.filter(week_start__year=year, week_start__month=themonth, facilityChoice__facility_name=facility)
                
                if chk_database.exists():
                    packetExists.extend(chk_database)
            selectedForm = forms
            chk_database = packetExists
        elif isinstance(forms, int) and type == "single":
            for x in formSettingsQuery:
                if x.id == forms:
                    fsEntry = x
                    label = formPacket
            name_of_model = fsEntry.formChoice.link + "_model"
            if fsEntry.formChoice.id == 23:
                chk_database = apps.get_model('EES_Forms', "form22_model").objects.filter(date__year=year, date__month=themonth, facilityChoice__facility_name=facility)
                print(form22_model.objects.all())
                originalStyle = True
            else:
                try:
                    print("CHECK 1.1")
                    chk_database = apps.get_model('EES_Forms', name_of_model).objects.filter(date__year=year, date__month=themonth, facilityChoice__facility_name=facility)
                    originalStyle = True
                except:
                    print("CHECK 1.2")
                    chk_database = apps.get_model('EES_Forms', name_of_model).objects.filter(week_start__year=year, week_start__month=themonth, facilityChoice__facility_name=facility)
                    originalStyle = False
            makeList = [forms]
            makeList.append(originalStyle)
            selectedForm = tuple(makeList)
        else:
            print("not a packet or form")
        print("<--------------------------")
        try:
            events = Event.objects.filter(date__month=themonth)
        except:
            events = Event.objects.filter(week_start__month=themonth)
        print(forms)
        # print(len(forms))
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events, year, type, label, chk_database, selectedForm))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

def stringToDate(date):
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
    
    if len(str(date.month)) == 2:
        month = str(date.month)
    else:
        month = '0'+str(date.month)
    if len(str(date.day)) == 2:
        day = str(date.day)
    else:
        day = '0'+str(date.day)
    parsed = str(date.year) + '-' + month + '-' + day
    return parsed

def updateSubmissionForm(fsID, submitted, date):
    formSettingsSub = form_settings_model.objects.get(id=int(fsID)).subChoice
    formSettingsSub.submitted = submitted
    formSettingsSub.dateSubmitted = date
    formSettingsSub.save()
    print("Updated Submission was saved...") 

def setUnlockClientSupervisor(requestUserData):
    unlock = False
    client = False
    supervisor = False
    if requestUserData.groups.filter(name=OBSER_VAR):
        unlock = True
    if requestUserData.groups.filter(name=CLIENT_VAR):
        client = True
    if requestUserData.groups.filter(name=SUPER_VAR) or requestUserData.is_superuser:
        supervisor = True
        
    return unlock, client, supervisor

def userGroupRedirect(user, permissions):
    userGroup = str(user.groups.all()[0])
    if userGroup not in permissions:
        if userGroup == OBSER_VAR:
            return redirect('facilitySelect', 'observer')
        elif userGroup == CLIENT_VAR:
            userProfile = user_profile_model.objects.get(user=user)
            return redirect('c_dashboard', userProfile.facilityChoice.facility_name)
        elif userGroup == SUPER_VAR:
            return redirect('sup_dashboard', SUPER_VAR)

def sendToDash(user):
    userGroup = str(user.groups.all()[0])
    if userGroup == OBSER_VAR:
        return redirect('facilitySelect', 'observer')
    elif userGroup == CLIENT_VAR:
        userProfile = user_profile_model.objects.get(user=user)
        print('doskdhjflksdjflksfj')
        return redirect('c_dashboard', userProfile.facilityChoice.facility_name)
    elif userGroup == SUPER_VAR:
        return redirect('sup_dashboard', SUPER_VAR)

def tryExceptFormDatabases(formID, model, facility):
    if len(model) > 0:
        return form_settings_model.objects.get(facilityChoice__facility_name=facility, formChoice=formID)
    else:
        return False
            
def weatherDict(city):
    # request the API data and convert the JSON to Python data types
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=435ac45f81f3f8d42d164add25764f3c'
    try:
        city_weather = requests.get(url.format(city)).json()
        sunrise = datetime.datetime.fromtimestamp(city_weather['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(city_weather['sys']['sunset'])
        weather = {
            'city': city,
            'temperature': round(city_weather['main']['temp'], 0),
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
            'wind_speed': round(city_weather['wind']['speed'], 0),
            'wind_direction': city_weather['wind']['deg'],
            'humidity': city_weather['main']['humidity'],
            'sunrise': str(sunrise.time().strftime("%I:%M %p")),
            'sunset': str(sunset.time().strftime("%I:%M %p"))
        }
        degree = weather['wind_direction']
        
        def toTextualDescription(degree):
            if degree > 337.5:
                return 'N'
            if degree > 292.5:
                return 'NW'
            if degree > 247.5:
                return 'W'
            if degree > 202.5:
                return 'SW'
            if degree > 157.5:
                return 'S'
            if degree > 122.5:
                return 'SE'
            if degree > 67.5:
                return 'E'
            if degree > 22.5:
                return 'NE'
            return 'N'
        wind_direction = toTextualDescription(degree)
        weather['wind_direction'] = wind_direction
    except:
        weather = {
            'error': "Please inform Supervisor '" + str(city) + "' is not a valid city.",
            'city': False
        }
    return weather

def calculateProgessBar(facility, frequency):
    formSubRecords = formSubmissionRecords_model.objects.filter(facilityChoice__facility_name=facility)
    forms_comp = [] 
    for formSub in formSubRecords.filter(submitted=True):
        if formSub.formID.frequency == frequency:
            forms_comp.append(formSub.formID.id)
    count_comp = len(forms_comp)
    count_total = len(formSubRecords.filter(formID__frequency=frequency))
    if count_total == 0:
        percent_completed = False
    else:
        percent_completed = (count_comp / count_total) * 100
    print(percent_completed)
    return percent_completed 

def ninetyDayPushTravels(facility):
    today = datetime.datetime.now().date()
    due_date_threshold = today + timedelta(days=30)
    most_recent_dates = {}
    all_records = form5_model.objects.filter(facilityChoice__facility_name=facility)
    if all_records.exists():
        for record in all_records:
            record_date = record.date  # The date the record was created
            ovens_data = record.ovens_data  # Parse the JSON data from ovens_data field

            # Iterate through each oven in the JSON data
            for oven_key in ["oven1", "oven2", "oven3", "oven4"]:  # Explicitly handle 4 ovens
                if oven_key in ovens_data:
                    oven_data = ovens_data[oven_key]
                    oven_number = oven_data.get("oven_number")
                    if oven_number:
                        # Update the most recent date for this oven
                        if oven_number not in most_recent_dates or record_date > most_recent_dates[oven_number]:
                            most_recent_dates[oven_number] = record_date
        
        # Calculate the 90-day deadlines and filter ovens due within 30 days
        print(most_recent_dates)
        od_90 = []
        od_30 = []
        od_10 = []
        od_5 = []
        for oven_number, most_recent_date in most_recent_dates.items():
            # Calculate the 90-day deadline
            deadline = most_recent_date + timedelta(days=90)
            difference = deadline-today
            ovenDict = {
                "oven_number": int(oven_number),
                "most_recent_date": most_recent_date,
                "deadline": deadline,
                "days_left": difference.days,
            }
            od_90.append(ovenDict)
            if difference.days <= 30:
                od_30.append(ovenDict)
            if difference.days <= 10:
                od_10.append(ovenDict)
            if difference.days <= 5:
                od_5.append(ovenDict)

        od_30 = sorted(od_30, key=lambda x: x["oven_number"])
        od_10 = sorted(od_10, key=lambda x: x["oven_number"])
        od_5 = sorted(od_5, key=lambda x: x["oven_number"])
        min_days_left = min(item['days_left'] for item in od_90) if len(od_5) > 0 else []
        od_closest = [entry for entry in od_5 if entry["days_left"] == min_days_left]
    
        return {'30days': od_30, '10days': od_10, '5days': od_5, 'closest': od_closest, 'all': od_90}
    else:
        return {'30days': [], '10days': [], '5days': [], 'closest': [], 'all': []}
    
def userColorMode(user):
    userProfile = user_profile_model.objects.filter(user__username=user.username)
    if userProfile.exists():
        userColorMode = userProfile[0].colorMode
    if userColorMode == 'light':
        return (False, 'lightMode')
    else:
        return (True, 'darkMode')
     
def colorModeSwitch(request):
    userProfile = user_profile_model.objects.filter(user__username=request.user.username)
    if userProfile.exists():
        userProfile = userProfile[0]
    if request.POST['colorMode'] == 'light':
        userProfile.colorMode = 'light'
    else:
        userProfile.colorMode = 'dark'
    print(userProfile.colorMode)
    userProfile.save()
    print(userProfile.colorMode)

    return redirect(request.META['HTTP_REFERER'])

def createNotificationDatabase(facility, user, fsID, date, notifSelector):
    print('notif - check 1')
    todayNumb = datetime.date.today().weekday()
    nFormSettings = form_settings_model.objects.get(id=fsID)
    nFacility = bat_info_model.objects.filter(facility_name=facility)
    if nFacility.exists():
        nFacility = nFacility[0]
    nUserProfile = user_profile_model.objects.filter(user__username=user.username)
    if nUserProfile.exists():
        nUserProfile = nUserProfile[0]
    companyUsers = user_profile_model.objects.filter(company__company_name=nUserProfile.company.company_name )
    # subForm = formSubmissionRecords_model.objects.filter(facilityChoice__facility_name=facility, formID__id=formID)
    # if subForm.exists():
    #     subForm = subForm[0]
    #     if subForm.formID.id not in {26,27}:
    #         ModelName =  'form' + subForm.formID.form.replace('-','') + '_model'
    #     else:
    #         ModelName = subForm.formID.form.replace(' ', '_').lower() + '_model'
    # modelData = apps.get_model('EES_Forms', ModelName).objects.all()
    newHeader =  notifSelector        
    if notifSelector == 'submitted':
        formID = nFormSettings.formChoice.id
        if todayNumb in {5,6}:
            if todayNumb == 5:
                todayName = 'Saturday'
            else:
                todayName = 'Sunday'
        else:
            todayName = False
        newNotifData = json.dumps({'settingsID': fsID, 'date': str(date), 'weekend': todayName})
    else:
        todayName = False
    if notifSelector in ['corrective', 'compliance']:
        newNotifData = json.dumps({'settingsID': fsID, 'date': str(date)})
    elif notifSelector == '90days':
        newNotifData = json.dumps({'ovenNumber': formID, 'date': str(date)})
    elif notifSelector == 'messages':
        print('Inbox Messages: TBA')

    for person in companyUsers:
        n = notifications_model(
            facilityChoice=nFacility,
            user = person,
            clicked = False,
            hovered = False,
            formData = newNotifData,
            header = newHeader,
            body = "Click here to view.",
            notes = "Submitted by " + user.first_name + " " + user.last_name + ". "
        )
        if n not in companyUsers:
            n.save()
    print("Form " + str(nFormSettings.id) + " notification was sent.")
   
def notificationCalc(user, facility):
    userProfile = user_profile_model.objects.filter(user__username=user.username)
    if userProfile.exists():
        userProfile = userProfile[0]
    notifications = notifications_model.objects.filter(facilityChoice__facility_name=facility)
    newNotifs = notifications.filter(clicked=False, hovered=False, user=userProfile)
    if newNotifs.exists():
        notifCount = len(newNotifs)
    else:
        notifCount = 0
    return notifCount
    
def displayNotifications(user, facility):
    notifCount = notificationCalc(user, facility)
    nUserProfile = user_profile_model.objects.filter(user__username=user.username)
    if nUserProfile.exists():
        nUserProfile = nUserProfile[0]
    allNotifs = notifications_model.objects.filter(facilityChoice__facility_name=facility, user=nUserProfile).order_by('-created_at')
    facForms = get_facility_forms('facilityName', facility)
    
    unReadList = []
    readList = []
    unReadNotifs = allNotifs.filter(clicked=False, hovered=False)
    readNotifs = allNotifs.filter(hovered=False)
    if unReadNotifs.exists():
        for unRead in unReadNotifs:
            notifFormData = json.loads(unRead.formData)
            for fsID in facForms:
                if int(notifFormData['settingsID']) == int(fsID):
                    settingEntry = form_settings_model.objects.get(id=int(fsID))
                    formPullData = (settingEntry, unRead, notifFormData, settingEntry.formChoice.link)
                    unReadList.append(formPullData)   
    print('______Notificitons______________________________________________')

    return {'notifCount': notifCount, 'unRead': unReadList, "read": readNotifs}
        
def createNotification(facility, request, fsID, date, notifSelector, issueID):
    print('notif1 - check 1')
    user = request.user
    createNotificationDatabase(facility, user, fsID, date, notifSelector)
    facilityParse = 'notifications_' + facility.replace(" ","_")
    notifCount = str(notificationCalc(user, facility))
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        facilityParse, {
            'type': 'notification',
            'count': notifCount,
            'facility': facility
        }
    )
    if notifSelector == 'compliance':
        print('mail check 1')
        fsEntry = form_settings_model.objects.get(id=issueID.form)
        userProfile = user_profile_model.objects.get(user=user)
        sendToList = []
        facProfileQuery = user_profile_model.objects.filter(facilityChoice__facility_name=facility)
        supProfileQuery = user_profile_model.objects.filter(company=userProfile.company, position='supervisor')
        for person in facProfileQuery:
            sendToList.append(person)
        for person in supProfileQuery:
            sendToList.append(person)
        print(sendToList)   
        mail_subject = 'MethodPlus: COMPLIANCE ISSUES'   
        current_site = get_current_site(request)
        for recipient in sendToList:
            html_message = render_to_string('email/compliance_email.html', {  
                'user': recipient,  
                'domain': current_site.domain,
                'form': fsEntry,
                'issue': issueID
            })
            plain_message = strip_tags(html_message)
            to_email = recipient.user.email 
            print(to_email)
            send_mail(
                mail_subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [to_email],
                html_message=html_message,
                fail_silently=False
            )
            print('mail check 2')
    
def checkIfFacilitySelected(user, facility):
    if facility not in ['supervisor', 'observer']:
        notifs = displayNotifications(user, facility)
    else:
        notifs = ''
    return notifs
    
def braintreeGateway():
    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            braintree.Environment.Sandbox,
            merchant_id=os.environ.get('BRAINTREE_MERCHANT_ID'),
            public_key=os.environ.get('BRAINTREE_PUBLIC_KEY'),
            private_key=os.environ.get('BRAINTREE_PRIVATE_KEY')
        )
    )
    return gateway

def getCompanyFacilities(username):
    thisProfileData = user_profile_model.objects.filter(user__username=username)[0]
    sortedFacilityData = bat_info_model.objects.filter(company__company_name=thisProfileData.company.company_name)
    
    return sortedFacilityData

def checkIfMoreRegistrations(user):
    profileData = user_profile_model.objects.get(user__id=user.id)
    braintreeData = braintree_model.objects.filter(user__id=user.id)
    userCompany = profileData.company
    listOfEmployees = user_profile_model.objects.filter(~Q(position="client"), company=userCompany, user__is_active=True)
    if braintreeData.exists():
        braintreeData = braintreeData.get(user__id=user.id)
    else:
        print('There is no braintree entry in database for this Company/User.')
        return False
    if braintreeData.settings['subscription']:
        if braintreeData.settings['subscription']['registrations']:
            total_registrations = braintreeData.settings['subscription']['registrations']
        else:
            print('There is no data in the database entry for this Company/User.')
            return False
    else:
        print('The data listed for Braintree-Subscription is False')
        return False
    active_registrations = len(listOfEmployees.filter(is_active=True))
    if active_registrations >= total_registrations:
        addMore = False
    else:
        addMore = True

    return (total_registrations, addMore)

def issueForm_picker(facility, date, fsID):
    if date == 'form' or date == 'edit':
        return False
    parsedDate = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    issueData = issues_model.objects.filter(date__exact=parsedDate, form=str(fsID))
    if issueData.exists():
        issueData = issues_model.objects.get(date__exact=parsedDate, form=str(fsID))
    else:
        issueData = False
    return issueData

def date_change(date):
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
    
    if len(str(date.month)) == 2:
        month = str(date.month)
    else:
        month = '0'+str(date.month)
    if len(str(date.day)) == 2:
        day = str(date.day)
    else:
        day = '0'+str(date.day)
    parsed = month + '-' + day + '-' + str(date.year)
    return parsed

def time_change(time):
    if isinstance(time, str):
        time = str(datetime.datetime.strptime(time, "%H:%M"))[11:]
    if time:
        hourNum = int(str(time)[0:2])
        minNum = str(time)[3:5]
        timeLabel = 'AM'
        if hourNum > 12:
            newHourNum = str(hourNum - 12)
            timeLabel = 'PM'
            newTime = newHourNum + ':' + minNum + ' ' + timeLabel
        elif hourNum == 12:
            newHourNum = str(time)[0:2]
            timeLabel = 'PM'
            newTime = newHourNum + ':' + minNum + ' ' + timeLabel
        elif hourNum == 00:
            newHourNum = '12'
            newTime = newHourNum + ':' + minNum + ' ' + timeLabel
        else:
            newTime = str(hourNum) + ':' + minNum + ' ' + timeLabel
        return newTime
    else:
        print('TIME_CHANGE ERROR: no time entered')
        print('ERROR TIME ENTERED: ' + str(time))
        print('RETURNING: "-" and moving on...')
        return '-'

def date_time_change(dateTime):
    if isinstance(dateTime, str):
        dateTime = datetime.datetime.strptime(dateTime, "%Y-%m-%dT%H:%M")
        
    date = date_change(dateTime.date())
    time = time_change(dateTime.time())
    return date + ', ' + time

def road_choices(input):
    paved_roads = {
        'p1': '#4 Booster Station',
        'p2': '#5 Battery Road',
        'p3': 'Coal Dump Horseshoe',
        'p4': 'Coal Handling Road (Partial)',
        'p5': 'Coke Plant Road',
        'p6': 'Coke Plant Mech Road',
        'p7': 'North Gate Area',
        'p8': 'Compund Road',
        'p9': 'D-4 Blast Furnace Road',
        'p10': 'Gap Gate Road',
        'p11': '#3 Ore Dock Road',
        'p12': 'River Road',
        'p13': 'Weigh Station Road',
        'p14': 'Zug Island Road'
    }
    unpaved_roads = {
        'unp1': 'North Gate Truck Turn',
        'unp2': 'Screening Station Road',
        'unp3': 'Coal Handling Road (Partial)',
        'unp4': 'Taj Mahal Road',
        'unp5': 'PECS Approach',
        'unp6': 'No. 2 Boilerhouse Road',
        'unp7': 'Bypass Route',
    }
    parking_lots = {
        'par1': 'Gap Gate Parking',
        'par2': 'Truck Garage Area',
        'par3': 'EES Coke Office Parking',
    }
    if input[1].isnumeric():
        answer = paved_roads[input]
    elif input[0] == 'u':
        answer = unpaved_roads[input]
    else:
        answer = parking_lots[input]
    return answer

def truck_choices(input):
    truck_choices = {
        '#5': 'Truck #5',
        '#6': 'Truck #6',
        '#7': 'Truck #7',
        '#9': 'Truck #9',
        'contractor': 'Contractor',
        'dozer': 'Dozer',
    }
    return truck_choices[input]
        
def area_choices(input):
    area_choices = {
        'panther eagle': 'Panther Eagle',
        'kepler': 'Kepler',
        'rock lick': 'Rock Lick',
        'mcclure': 'McClure',
        'elk valley': 'Elk Valley',
    }
    return area_choices[input]
    
def emptyInputs(input):
    if not input:
        this = 'N/A'
        return this
    else:
        return input
    
def quarterParse(input):
    if input == 1:
        return '1st Quarter'
    elif input == 2:
        return '2nd Quarter'
    elif input == 3:
        return '3rd Quarter'
    elif input == 4:
        return '4th Quarter'
    
def inventoryResponse(tagOn, sk):
    database = spill_kit_inventory_model.objects.filter(skID=sk)
    if tagOn == "No" and len(database) > 0:
        return "Yes"
    elif tagOn == "No" and len(database) == 0:
        return "No"
    else:
        return "N/A"      
    
def get_facility_forms(selector, facilityID):
    if selector == 'facilityName':
        facilityFormsString = facility_forms_model.objects.get(facilityChoice__facility_name=facilityID)
    elif selector == 'facilityID':
        facilityFormsString = facility_forms_model.objects.get(facilityChoice__id=facilityID)
    facilityFormsList = changeStringListIntoList(facilityFormsString.formData)
    return facilityFormsList

def create_starting_forms():
    # ADD IN THE FORMS IF DATABASE HAS LESS THAN 5----------
    today = datetime.date.today()
    if Forms.objects.count() <= 5:
        A1 = Forms(
            form=1,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form1",
            header="Method 303",
            title="Charging",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        A2 = Forms(
            form=2,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form2",
            header="Method 303",
            title="Doors",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        A3 = Forms(
            form=3,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form3",
            header="Method 303",
            title="Lids and Offtakes",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        A4 = Forms(
            form=4,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form4",
            header="Method 303",
            title="Collection Main",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        A5 = Forms(
            form=5,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form5",
            header="Method 9B",
            title="Push Travels",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        B = Forms(
            form=6,
            frequency="Daily",
            day_freq='Weekdays',
            weekdays_only=True,
            weekend_only=False,
            link="form6",
            header="Method 9",
            title="Fugitive Dust Inspection",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        C = Forms(
            form=7,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form7",
            header="Method 9",
            title="Method 9D - Coal Field",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        D = Forms(
            form=8,
            frequency="Weekly",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form8",
            header="Method 9",
            title="Random Truck Inspection",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        E = Forms(
            form=9,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form9",
            header="Method 9",
            title="Gooseneck Inspection",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F1 = Forms(
            form=10,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="form10",
            header="Waste Weekly Inspections",
            title="SIF / K087 Process Area (Satellite)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F2 = Forms(
            form=11,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="form11",
            header="Waste Weekly Inspections",
            title="#1 Shop (Satellite Accumulation)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F3 = Forms(
            form=12,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="form12",
            header="Waste Weekly Inspections",
            title="#2 Shop (Satellite Accumulation)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F4 = Forms(
            form=13,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="form13",
            header="Waste Weekly Inspections",
            title="Battery (Satellite Accumulation)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F5 = Forms(
            form=14,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="form14",
            header="Waste Weekly Inspections",
            title="Bio Plant (Satellite Accumulation)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F6 = Forms(
            form=15,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="form15",
            header="Waste Weekly Inspections",
            title="No. 8 Tank Area (Satellite Accumulation)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F7 = Forms(
            form=16,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="form16",
            header="Waste Weekly Inspections",
            title="Booster Pad (90-Day Accumulation)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        G1 = Forms(
            form=17,
            frequency="Weekly",
            day_freq='Weekdays',
            weekdays_only=False,
            weekend_only=False,
            link="form17",
            header="PECS Baghouse Stack",
            title="Method 9/Non-Certified Observations",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        G2 = Forms(
            form=18,
            frequency="Monthly",
            day_freq='Weekdays',
            weekdays_only=False,
            weekend_only=False,
            link="form18",
            header="PECS Baghouse Stack",
            title="Method 9B",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        H = Forms(
            form=19,
            frequency="Weekly",
            day_freq='Weekdays',
            weekdays_only=False,
            weekend_only=False,
            link="form19",
            header="Method 9",
            title="Method 9 - Combustion Stack",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        I = Forms(
            form=20,
            frequency="Daily",
            day_freq='Weekdays',
            weekdays_only=True,
            weekend_only=False,
            link="form20",
            header="Sampling",
            title="Quench Water Sampling Form",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        L = Forms(
            form=21,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form21",
            header="Method 9",
            title="Visual Emissions Observations",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        M = Forms(
            form=22,
            frequency="Daily",
            day_freq='Weekdays',
            weekdays_only=True,
            weekend_only=False,
            link="form22",
            header="Method 9D",
            title="Method 9D Observation",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        N = Forms(
            form=23,
            frequency="Monthly",
            day_freq='Weekdays',
            weekdays_only=False,
            weekend_only=False,
            link="form23",
            header="Fugitive Dust Inspection",
            title="Method 9D Monthly Checklist",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        O = Forms(
            form=24,
            frequency="Weekly",
            day_freq='Daily',
            weekdays_only=False,
            weekend_only=True,
            link="form24",
            header="Stormwater Observation Form",
            title="MP 108A",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        P = Forms(
            form=25,
            frequency="Daily",
            day_freq='Weekends',
            weekdays_only=False,
            weekend_only=True,
            link="form25",
            header="Outfall Observation Form",
            title="Outfall 008",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        spill_kits_inventory = Forms(
            form=26,
            frequency="Monthly",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form26",
            header="Spill Kit Inventory Form",
            title="Inspection Check List",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        quarterly_trucks = Forms(
            form=27,
            frequency="Quarterly",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form27",
            header="Quarterly Trucks Form",
            title="Inspection Check List",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        STI_SP001_monthly_inspection = Forms(
            form=28,
            frequency="Monthly",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form28",
            header="STI SP001",
            title="Monthly Tank Inspection Checklist",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False
        )
        spill_kits = Forms(
            form=29,
            frequency="Monthly",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form29",
            header="Spill Kits Form",
            title="Inspection Check List",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)

        A1.save()
        A2.save()
        A3.save()
        A4.save()
        A5.save()
        B.save()
        C.save()
        D.save()
        E.save()
        F1.save()
        F2.save()
        F3.save()
        F4.save()
        F5.save()
        F6.save()
        F7.save()
        G1.save()
        G2.save()
        H.save()
        I.save()
        L.save()
        M.save()
        N.save()
        O.save()
        P.save()
        spill_kits_inventory.save()
        quarterly_trucks.save()
        STI_SP001_monthly_inspection.save()
        spill_kits.save()
        
def updateAllFormSubmissions(facility):
    facFormsSettingsModel = form_settings_model.objects.filter(facilityChoice__facility_name=facility)
    today = datetime.date.today()
    todays_num = today.weekday()
    weekday_fri = today + datetime.timedelta(days=4 - todays_num)
    for fsForm in facFormsSettingsModel:
        sub = fsForm.subChoice
        if sub.formID.frequency == 'Monthly':
            numbOfDaysInMonth = calendar.monthrange(today.year, today.month)[1]
            lastDayOfMonth = str(today.year) + '-' + str(today.month) + '-' + str(numbOfDaysInMonth)
            sub.dueDate = datetime.datetime.strptime(lastDayOfMonth, "%Y-%m-%d").date()
            dueDate = sub.dueDate
            if sub.dateSubmitted.year != dueDate.year or sub.dateSubmitted.month != dueDate.month:
                sub.submitted = False
            sub.save()
        elif sub.formID.frequency == 'Quarterly':
            if what_quarter(today) == 1:
                monthDue = 3
                yearDue = today.year
                dayDue =  calendar.monthrange(yearDue, monthDue)[1]
            elif what_quarter(today) == 2:
                monthDue = 6
                yearDue = today.year
                dayDue =  calendar.monthrange(yearDue, monthDue)[1]
            elif what_quarter(today) == 3:
                monthDue = 9
                yearDue = today.year
                dayDue =  calendar.monthrange(yearDue, monthDue)[1]
            elif what_quarter(today) == 4:
                monthDue = 12
                yearDue = today.year
                dayDue =  calendar.monthrange(yearDue, monthDue)[1]
            dateBuild = str(yearDue) + '-' + monthDayAdjust(monthDue) + '-' + monthDayAdjust(dayDue)
            sub.dueDate = datetime.datetime.strptime(dateBuild, "%Y-%m-%d").date()
            A = sub.dateSubmitted
            B = sub.dueDate
            if what_quarter(A) != what_quarter(B):
                sub.submitted = False
            sub.save()
        elif sub.formID.frequency == 'Weekly':
            if todays_num in {0, 1, 2, 3, 4}:
                if sub.formID.day_freq == 'Weekends':
                    sub.dueDate = weekday_fri - datetime.timedelta(days=5)
                start_sat = weekday_fri - datetime.timedelta(days=6)
                sub.dueDate = weekday_fri
            else:
                start_sat = today - datetime.timedelta(days= todays_num - 5)
                sub.dueDate = start_sat + datetime.timedelta(days=11 - todays_num)
            A = sub.dateSubmitted
            B = sub.dueDate
            if sub.formID.day_freq == 'Weekends' and A != B:
                sub.submitted = False   
            elif A < start_sat or A > sub.dueDate:
                sub.submitted = False
            sub.save()
        elif sub.formID.frequency == 'Daily':
            if sub.formID.weekend_only and todays_num not in {5,6}:
                sub.save()
                continue
            else:    
                sub.dueDate = today
                A = sub.dateSubmitted
                B = sub.dueDate
                if today != A:
                    sub.submitted = False
                sub.save()
                
def what_quarter(input):
    if input.month in {1,2,3}:
        return 1
    if input.month in {4,5,6}:
        return 2
    if input.month in {7,8,9}:
        return 3
    if input.month in {10,11,12}:
        return 4

def monthDayAdjust(input):
    if len(str(input)) == 1:
        return '0'+str(input)
    else:
        return str(input)
    
def changeStringListIntoList(ffFormData):
    facilityForms = ffFormData
    if facilityForms:
        if facilityForms == '[]':
            returnList = []
        else:
            facilityForms = ast.literal_eval(facilityForms[1:-1])
            if str(facilityForms)[0] != "(":
                returnList = [facilityForms]
            else:
                returnList = []
                for x in facilityForms:
                    returnList.append(x)     
    else:
        returnList = []
        # messages.error(request,'ERROR: ID-11850003 Contact Support Team')
    
    return returnList

def getFacSettingsInfo(fsID):
    fsPull = form_settings_model.objects.get(id=int(fsID))
    return fsPull

def formBNone(input):
    if str(input) in ['none', False, '']:
        answer = 'none'
    else:
        answer = str(input) + ' mph'
    return answer

def generate_random_string(length=12):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def change_dashboard_setting(dashboard_pick, observer):
    profileSetDash = {
        'formsDash': True, 
        'batteryDash': False
    }
    for key in dashDict.keys():
        if dashboard_pick == key:
            if not observer:
                profileSetDash[key] = defaultBatteryDashSettings
            else:
                profileSetDash[key] = True
        else:
            profileSetDash[key] = False
    return profileSetDash

def setDefaultSettings(profile, superUsername):
    today = datetime.datetime.now()
    createSettings = {'dashboard':{}}
    try:
        companyFacilities = getCompanyFacilities(superUsername)
        for facility in companyFacilities:
            createSettings['dashboard'][str(facility.id)] = dashDict
            if facility.is_battery == 'Yes':
                if profile.position != OBSER_VAR:
                    createSettings['dashboard'][str(facility.id)] = change_dashboard_setting('batteryDash', False)
                else:
                    createSettings['dashboard'][str(facility.id)] = change_dashboard_setting('batteryDash', True)
    except:
        createSettings['dashboard'] = False
    createSettings['notifications'] = defaultNotifications
    createSettings['first_login'] = False
    createSettings['position'] = profile.position
    return createSettings

def get_braintree_query(user):
    profileData = user_profile_model.objects.get(user=user)
    brainTreeQuery = braintree_model.objects.all()
    if brainTreeQuery.exists():
        for btEntry in brainTreeQuery:
            leadSupervisor = user_profile_model.objects.get(user=btEntry.user)
            if leadSupervisor.company.id == profileData.company.id:
                return btEntry
    else:
        print('handle if there is zero braintree entries')
        return False

def parsePhone(phoneNumber):
    if phoneNumber[0] == "+":
        numWoAreaCode = phoneNumber[2:]
        first = numWoAreaCode[:3]
        second = numWoAreaCode[3:6]
        third = numWoAreaCode[6:]
        finalPhone = "(" + first + ") " + second + "-" + third
        print('parenthatses')
    else:
        finalPhone = '+1' + ''.join(filter(str.isdigit, phoneNumber))
    return finalPhone

def getActiveCompanyEmployees(company):
    userProfileQuery = user_profile_model.objects.filter(~Q(position="client"), company=company, user__is_active=True)
    return userProfileQuery

def get_list_of_braintree_status(sub_search, addOnSet):
    active_users = []
    past_due_list = []
    for sub in sub_search.items:
        if sub.status == "Active":
            if sub.transactions:
                transaction = sub.transactions[0]  # Take the first transaction
                customer = transaction.customer_details
                
                braintreeDict = {
                    "customer_id": customer.id,
                    "first_name": customer.first_name,
                    "last_name": customer.last_name,
                    "status": sub.status,
                    "email": customer.email,
                    "company": customer.company,
                    "subscription_id": sub.id,
                    "plan_id": sub.plan_id,
                    "price": sub.price,
                    "start_date": sub.created_at,
                    "next_billing_date": sub.next_billing_date,
                }
                if addOnSet:
                    # Extract add-on details
                    add_ons = [
                        {
                            "id": add_on.id,
                            "name": add_on.name,
                            "amount": add_on.amount,
                            "quantity": add_on.quantity,
                        }
                        for add_on in sub.add_ons
                    ]
                    braintreeDict['add_ons'] = add_ons

                user = braintree_model.objects.filter(settings__account__customer_ID=customer.id)
                if user.exists():
                    braintreeDict['last_login'] = user[0].user.last_login.date()
                else:
                    braintreeDict['last_login'] = "User not in system"
                
                # Append user details
                active_users.append(braintreeDict)
        elif sub.status == "Past Due":
            past_due_list.append(sub)
    return active_users, past_due_list

def get_initial_data(modelName, modelInstance):
    def get_field_value(fieldName, modelList):
        for source in modelList:
            if hasattr(source, fieldName):  # Check if the field exists
                return getattr(source, fieldName)
        return None  # Fallback value if neither has the attribute

    allModelFields = [
        field.name for field in modelName._meta.get_fields() 
        if isinstance(field, Field) and field.name not in ["id","facilityChoice"]
    ]
    modelList = [modelInstance]
    try:
        model_name = modelName._meta.object_name.replace("_model", "_readings_model")
        content_type = ContentType.objects.get(model=model_name.lower())
        modelInstance2 = content_type.model_class().objects.get(form=modelInstance)
        model2Fields = [
            field.name for field in modelInstance2._meta.get_fields() 
            if isinstance(field, Field) and field.name not in ["id","form"]
        ]
        allModelFields = allModelFields + model2Fields
        modelList.append(modelInstance2)
    except:
        print('only one model')
    initial_data = {fieldName: get_field_value(fieldName, modelList) for fieldName in allModelFields}
    return initial_data




