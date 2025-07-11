from django.shortcuts import redirect # type: ignore
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from channels.layers import get_channel_layer # type: ignore
from asgiref.sync import async_to_sync # type: ignore
from django.contrib.sites.shortcuts import get_current_site   # type: ignore
from django.template.loader import render_to_string  # type: ignore
from django.utils.html import strip_tags, escape # type: ignore
from django.core.mail import send_mail # type: ignore
from django.conf import settings # type: ignore
from django.contrib import messages # type: ignore
from django.db.models import Field, Min # type: ignore
from django.contrib.contenttypes.models import ContentType # type: ignore
from ..utils.twilio_verify import send_sms_message
from datetime import datetime, timedelta
from calendar import HTMLCalendar
from django.utils.timezone import localtime # type: ignore
from ..models import *
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
import re

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
        'compliance': {'methodplus': True, 'email': False, 'sms': False},
        'deviations': {'methodplus': True, 'email': False, 'sms': False},
        'submitted': {'methodplus': True, 'email': False, 'sms': False},
        '10_day_pt': {'methodplus': False, 'email': False, 'sms': False},
        '5_day_pt': {'methodplus': False, 'email': False, 'sms': False}
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
defaultGlobalFormSettingsDict = {"active": True, "packets": False, "settings":{}}
defaultPacketSettings = {
    'formsList': False,
    'settings': {
        'weekly_start_day': 'saturday',
        'frequency': 'weekly',
        'active': True
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
dashDict = {
    'dashboard': "Default", 
    'settings': {},
    'notifications': {}
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
        "status": "item", # selected, canceled, active
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
    allFormData = form17_model.objects.all()   
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

def parse_form17_oven_dict(reading_data, ovens_data):
    inspecType = ovens_data["PEC_type"]
    ovens = {}
    ovens.update({"PEC_type": inspecType})
    if inspecType == "meth9":
        for key1, oven in ovens_data[inspecType].items():
            if key1 == "readings":
                pecStart =  "PEC_read_"
                for i in range(1,25):
                    ovens.update({pecStart + str(i): oven[pecStart + str(i)]})
            else:
                ovens.update({key1: oven})
    else:
        for key1, oven in ovens_data[inspecType].items():
            ovens.update({key1: oven})

    readings = {}
    for key2, reading in reading_data.items():
        readings.update({key2: reading})
    return json.loads(json.dumps(readings)), json.loads(json.dumps(ovens))

def parse_form7_oven_dict(area_json_1, area_json_2, area_json_3, area_json_4):
    ovens = {}
    print(area_json_1)
    ovens.update({key: value for key, value in area_json_1.items() if key != 'readings'})
    ovens.update({f"1Read_{key}": value for key, value in area_json_1.get('readings', {}).items()})
    ovens.update({key: value for key, value in area_json_2.items() if key != 'readings'})
    ovens.update({f"2Read_{key}": value for key, value in area_json_2.get('readings', {}).items()})
    ovens.update({key: value for key, value in area_json_3.items() if key != 'readings'})
    ovens.update({f"3Read_{key}": value for key, value in area_json_3.get('readings', {}).items()})
    ovens.update({key: value for key, value in area_json_4.items() if key != 'readings'})
    ovens.update({f"4Read_{key}": value for key, value in area_json_4.get('readings', {}).items()})

    return json.loads(json.dumps(ovens))


def parse_form5_oven_dict(reading_data, ovens_data):
    ovens = {}
    for key1, oven in ovens_data.items():
        id_sec_1 =  "o" + key1[4:]
        ovens.update({
            id_sec_1: oven['oven_number'], 
            id_sec_1 + "_start": oven['start'], 
            id_sec_1 + "_stop": oven['stop'],
            id_sec_1 + "_highest_opacity": oven['highest_opacity'],
            id_sec_1 + "_instant_over_20": oven['opacity_over_20'],
            id_sec_1 + "_average_6": oven['average_6_opacity'],
            id_sec_1 + "_average_6_over_35": oven['average_6_over_35'],
        })
        y=1
        z=9
        for x in range(1,9):
            ovens.update({id_sec_1 + "_" + str(y) + "_reads": oven['readings']['push'][str(x)]})
            ovens.update({id_sec_1 + "_" + str(z) + "_reads": oven['readings']['travel'][str(x)]})
            y += 1
            z += 1

    readings = {}
    for key2, reading in reading_data.items():
        readings.update({key2: reading})
    return json.loads(json.dumps(readings)), json.loads(json.dumps(ovens))

def parse_form1_oven_dict(ovens_data):
    ovens = {}
    for key, oven in ovens_data.items():
        print()
        if "charge" in key:
            charges =  f"c{key[7:]}"
            ovens.update({
                f"{charges}_no": oven[f"{charges}_no"], 
                f"{charges}_start": oven[f"{charges}_start"], 
                f"{charges}_stop": oven[f"{charges}_stop"],
                f"{charges}_sec": oven[f"{charges}_sec"],
                f"{charges}_comments": oven[f"{charges}_comments"]
            })
        else:
            ovens.update({
                key: oven
            })
    print(ovens)
    return json.loads(json.dumps(ovens))

def form19_ovens_data_build(requestPOST):
    ovens_data = {
        "comb_formL": requestPOST['comb_formL'], 
        **{f"comb_read_{i}": requestPOST[f"comb_read_{i}"] if f"comb_read_{i}" in requestPOST else False for i in range(1,61)},
        "comb_start": requestPOST['comb_start'], 
        "comb_stop": requestPOST['comb_stop'], 
        "comb_average": requestPOST['comb_average']
    }
    return json.loads(json.dumps(ovens_data))

def form18_ovens_data_build(requestPOST):
    ovens_data = {
        "PEC_average_main": requestPOST['PEC_average_main'], 
        "oven_a": {
            "PEC_oven_a": requestPOST['PEC_oven_a'],
            "PEC_start_a": requestPOST['PEC_start_a'],
            "PEC_average_a": requestPOST['PEC_average_a'],
            "readings": {
                "PEC_read_a_1": requestPOST['PEC_read_a_1'], 
                "PEC_read_a_2": requestPOST['PEC_read_a_2'], 
                "PEC_read_a_3": requestPOST['PEC_read_a_3'], 
                "PEC_read_a_4": requestPOST['PEC_read_a_4'], 
                "PEC_read_a_5": requestPOST['PEC_read_a_5'], 
                "PEC_read_a_6": requestPOST['PEC_read_a_6'], 
                "PEC_read_a_7": requestPOST['PEC_read_a_7'], 
                "PEC_read_a_8": requestPOST['PEC_read_a_8']
            }
        }, 
        "oven_b": {
            "PEC_oven_b": requestPOST['PEC_oven_b'], 
            "PEC_start_b": requestPOST['PEC_start_b'], 
            "PEC_average_b": requestPOST['PEC_average_b'], 
            "readings": {
                "PEC_read_b_1": requestPOST['PEC_read_b_1'], 
                "PEC_read_b_2": requestPOST['PEC_read_b_2'], 
                "PEC_read_b_3": requestPOST['PEC_read_b_3'], 
                "PEC_read_b_4": requestPOST['PEC_read_b_4'], 
                "PEC_read_b_5": requestPOST['PEC_read_b_5'], 
                "PEC_read_b_6": requestPOST['PEC_read_b_6'], 
                "PEC_read_b_7": requestPOST['PEC_read_b_7'], 
                "PEC_read_b_8": requestPOST['PEC_read_b_8']
            }
        }, 
        "oven_c": {
            "PEC_oven_c": requestPOST['PEC_oven_c'], 
            "PEC_start_c": requestPOST['PEC_start_c'], 
            "PEC_average_c": requestPOST['PEC_average_c'], 
            "readings": {
                "PEC_read_c_1": requestPOST['PEC_read_c_1'], 
                "PEC_read_c_2": requestPOST['PEC_read_c_2'], 
                "PEC_read_c_3": requestPOST['PEC_read_c_3'], 
                "PEC_read_c_4": requestPOST['PEC_read_c_4'], 
                "PEC_read_c_5": requestPOST['PEC_read_c_5'], 
                "PEC_read_c_6": requestPOST['PEC_read_c_6'], 
                "PEC_read_c_7": requestPOST['PEC_read_c_7'], 
                "PEC_read_c_8": requestPOST['PEC_read_c_8']
            }
        }
    }
    return json.loads(json.dumps(ovens_data))

def form17_ovens_data_build(requestPOST):
    ovens_data = {}
    ovens_data['PEC_type'] = requestPOST['PEC_type']
    if requestPOST['PEC_type'] == "meth9":
        meth9_dict = {
            "PEC_oven1": requestPOST['PEC_oven1'],
            "PEC_oven2": requestPOST['PEC_oven2'],
            "PEC_time1": str(requestPOST['PEC_time1']),
            "PEC_time2": str(requestPOST['PEC_time2']),
            "PEC_start": str(requestPOST['PEC_start']),
            "PEC_stop": str(requestPOST['PEC_stop']),
            "PEC_average": requestPOST['PEC_average'], 
            "readings": {
                "PEC_read_1": requestPOST['PEC_read_1'], 
                "PEC_read_2": requestPOST['PEC_read_2'], 
                "PEC_read_3": requestPOST['PEC_read_3'], 
                "PEC_read_4": requestPOST['PEC_read_4'], 
                "PEC_read_5": requestPOST['PEC_read_5'], 
                "PEC_read_6": requestPOST['PEC_read_6'], 
                "PEC_read_7": requestPOST['PEC_read_7'], 
                "PEC_read_8": requestPOST['PEC_read_8'], 
                "PEC_read_9": requestPOST['PEC_read_9'], 
                "PEC_read_10": requestPOST['PEC_read_10'], 
                "PEC_read_11": requestPOST['PEC_read_11'],
                "PEC_read_12": requestPOST['PEC_read_12'], 
                "PEC_read_13": requestPOST['PEC_read_13'], 
                "PEC_read_14": requestPOST['PEC_read_14'], 
                "PEC_read_15": requestPOST['PEC_read_15'], 
                "PEC_read_16": requestPOST['PEC_read_16'], 
                "PEC_read_17": requestPOST['PEC_read_17'], 
                "PEC_read_18": requestPOST['PEC_read_18'], 
                "PEC_read_19": requestPOST['PEC_read_19'], 
                "PEC_read_20": requestPOST['PEC_read_20'], 
                "PEC_read_21": requestPOST['PEC_read_21'], 
                "PEC_read_22": requestPOST['PEC_read_22'], 
                "PEC_read_23": requestPOST['PEC_read_23'], 
                "PEC_read_24": requestPOST['PEC_read_24']
            }
        } 

        nonCert_dict = {
            "PEC_push_oven": None, 
            "PEC_push_time": None, 
            "PEC_observe_time": None, 
            "PEC_emissions_present": None
        }
    else:
        meth9_dict = {
            "PEC_oven1": None,
            "PEC_oven2": None,
            "PEC_time1": None,
            "PEC_time2": None,
            "PEC_start": None,
            "PEC_stop": None,
            "PEC_average": None, 
            "readings": {
                "PEC_read_1": None, 
                "PEC_read_2": None, 
                "PEC_read_3": None, 
                "PEC_read_4": None, 
                "PEC_read_5": None, 
                "PEC_read_6": None, 
                "PEC_read_7": None, 
                "PEC_read_8": None, 
                "PEC_read_9": None, 
                "PEC_read_10": None, 
                "PEC_read_11": None,
                "PEC_read_12": None, 
                "PEC_read_13": None, 
                "PEC_read_14": None, 
                "PEC_read_15": None, 
                "PEC_read_16": None, 
                "PEC_read_17": None, 
                "PEC_read_18": None, 
                "PEC_read_19": None, 
                "PEC_read_20": None, 
                "PEC_read_21": None, 
                "PEC_read_22": None, 
                "PEC_read_23": None, 
                "PEC_read_24": None
            }
        } 

        nonCert_dict = {
            "PEC_push_oven": requestPOST['PEC_push_oven'], 
            "PEC_push_time": str(requestPOST['PEC_push_time']), 
            "PEC_observe_time": str(requestPOST['PEC_observe_time']), 
            "PEC_emissions_present": requestPOST['PEC_emissions_present']
        }
    ovens_data['meth9'] = meth9_dict
    ovens_data['non'] = nonCert_dict
    return json.loads(json.dumps(ovens_data))

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

def method9_reading_data_build(requestPOST):
    reading_data = {
        'process_equip1': requestPOST['process_equip1'], 
        'process_equip2': requestPOST['process_equip2'], 
        'op_mode1': requestPOST['op_mode1'], 
        'op_mode2': requestPOST['op_mode2'], 
        'background_color_start': requestPOST['background_color_start'], 
        'background_color_stop': requestPOST['background_color_stop'], 
        'sky_conditions': requestPOST['sky_conditions'], 
        'wind_speed_start': requestPOST['wind_speed_start'], 
        'wind_speed_stop': requestPOST['wind_speed_stop'], 
        'wind_direction': requestPOST['wind_direction'], 
        'emission_point_start': requestPOST['emission_point_start'], 
        'emission_point_stop': requestPOST['emission_point_stop'], 
        'ambient_temp_start': requestPOST['ambient_temp_start'], 
        'ambient_temp_stop': requestPOST['ambient_temp_stop'], 
        'humidity': requestPOST['humidity'], 
        'height_above_ground': requestPOST['height_above_ground'], 
        'height_rel_observer': requestPOST['height_rel_observer'], 
        'distance_from': requestPOST['distance_from'], 
        'direction_from': requestPOST['direction_from'], 
        'describe_emissions_start': requestPOST['describe_emissions_start'], 
        'describe_emissions_stop': requestPOST['describe_emissions_stop'], 
        'emission_color_start': requestPOST['emission_color_start'], 
        'emission_color_stop': requestPOST['emission_color_stop'], 
        'plume_type': requestPOST['plume_type'], 
        'water_drolet_present': requestPOST['water_drolet_present'], 
        'water_droplet_plume': requestPOST['water_droplet_plume'], 
        'plume_opacity_determined_start': requestPOST['plume_opacity_determined_start'], 
        'plume_opacity_determined_stop': requestPOST['plume_opacity_determined_stop'], 
        'describe_background_start': requestPOST['describe_background_start'], 
        'describe_background_stop': requestPOST['describe_background_stop'],
    }
    return json.loads(json.dumps(reading_data))

def form1_json_build(requestPOST):
    ovens_data = {
        "charge_1": {
            'c1_no': requestPOST['c1_no'],
            'c1_start': requestPOST['c1_start'],
            'c1_stop': requestPOST['c1_stop'],
            'c1_sec': requestPOST['c1_sec'],
            'c1_comments': requestPOST['c1_comments'],
        },
        "charge_2": {
            'c2_no': requestPOST['c2_no'],
            'c2_start': requestPOST['c2_start'],
            'c2_stop': requestPOST['c2_stop'],
            'c2_sec': requestPOST['c2_sec'],
            'c2_comments': requestPOST['c2_comments'],
        },
        "charge_3": {
            'c3_no': requestPOST['c3_no'],
            'c3_start': requestPOST['c3_start'],
            'c3_stop': requestPOST['c3_stop'],
            'c3_sec': requestPOST['c3_sec'],
            'c3_comments': requestPOST['c3_comments'],
        },
        "charge_4": {
            'c4_no': requestPOST['c4_no'],
            'c4_start': requestPOST['c4_start'],
            'c4_stop': requestPOST['c4_stop'],
            'c4_sec': requestPOST['c4_sec'],
            'c4_comments': requestPOST['c4_comments'],
        },
        "charge_5": {
            'c5_no': requestPOST['c5_no'],
            'c5_start': requestPOST['c5_start'],
            'c5_stop': requestPOST['c5_stop'],
            'c5_sec': requestPOST['c5_sec'],
            'c5_comments': requestPOST['c5_comments'],
        },
        'comments': requestPOST['comments'],
        'larry_car': requestPOST['larry_car'],
        'total_seconds': requestPOST['total_seconds']
    }
    return json.loads(json.dumps(ovens_data))
        
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

        allDayEvents = events_from_day.filter(allDay=True)
        add_day_event_data = [
            {
                "title": event.title,
                "url": event.get_absolute_url(),
                "observer": event.observer,
                'allDay': event.allDay,
                'notes': event.notes,
                'id': event.id
            }
            for event in allDayEvents
        ]

        otherEvents = events_from_day.filter(~Q(allDay=True))
        add_other_event_data = [
            {
                "title": event.title,
                "url": event.get_absolute_url(),
                "observer": event.observer,
                'start_time': str(event.start_time),
                'end_time': str(event.end_time),
                'allDay': event.allDay,
                'notes': event.notes,
                'id': event.id
            }
            for event in otherEvents
        ]

        safe_json_allDay = escape(json.dumps(add_day_event_data))
        safe_json_other = escape(json.dumps(add_other_event_data))

        events_html = "<ul>"
        for event in events_from_day:
            events_html += event.get_absolute_url() + "<br>"
        events_html += "</ul>"

        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return f'<td id="day-{day}" class="{self.cssclasses[weekday]}" data-allday="{safe_json_allDay}" data-other="{safe_json_other}">{day}{events_html}</td>'

 
    def formatweek(self, theweek, events, year):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events, year) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s
        
        
 
    def formatmonth(self, theyear, themonth, year, user_prof, withyear=True):
        """
        Return a formatted month as a table.
        """
        # if user_prof.position == "supervisor":
        #     events = Event.objects.filter(date__month=themonth, date__year=year, personal=True)
        # else:
        events = Event.objects.filter(date__month=themonth, date__year=year, userProf__company=user_prof.company)
 
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
                           
                            forms_html += "<a href='../../../../../print-index/" + type + "/Daily/" + str(selectedForm) + "-" + str(label) + "/" + str(selectedFormDate.date.year) + "-" + formatTheDayNumber(selectedFormDate.date.month) +"-"+ formatTheDayNumber(selectedFormDate.date.day) +"' target='_blank'>Submitted Packet</a><br>"
                        else:
                            forms_html += "<a href='../../../../../print-index/" + type + "/Daily/" + str(selectedForm) + "/" + str(selectedFormDate.date.year) + "-" + formatTheDayNumber(selectedFormDate.date.month) +"-"+ formatTheDayNumber(selectedFormDate.date.day) +"' target='_blank'>Submitted Packet</a><br>"
                        
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
                        forms_html += "<a href='../../../../../print-index/" + type + "/" + packFreq + "/"+ str(selectedForm) + "/" + str(selectedFormDate.year) + "-"+ formatTheDayNumber(selectedFormDate.month) +"-"+ formatTheDayNumber(selectedFormDate.day) +"' target='_blank'>Submitted Packet</a><br>"
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
                            forms_html += "<a href='../../../../../print-index/" + type + "/Daily/" + str(selectedForm[0]) + "-" + str(label) + "/" + str(form.date.year) + "-"+ formatTheDayNumber(form.date.month) +"-"+ formatTheDayNumber(form.date.day) +"' target='_blank'>Submitted Form</a><br>"
                        else:
                            forms_html += "<a href='../../../../../print-index/" + type + "/Daily/" + str(selectedForm[0]) + "-" + str(label) + "/" + str(form.date.year) + "-"+ formatTheDayNumber(form.date.month) +"-"+ formatTheDayNumber(form.date.day) +"' target='_blank'>Submitted Form</a><br>"
                        eventCell = True
            else:
                forms_from_day = forms.filter(week_start__day=day)
                for form in forms_from_day:
                    if form.week_start.year == year:
                        forms_html += "<a href='../../../../../print-index/" + type + "/Daily/" + str(selectedForm[0]) + "-" + str(label) + "/" + str(form.week_start.year) + "-"+ formatTheDayNumber(form.week_start.month) +"-"+ formatTheDayNumber(form.week_start.day) +"' target='_blank'>Submitted Form</a><br>"
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
                    chk_database = form22_model.objects.filter(date__year=year, date__month=themonth, formSettings__id=iFormSettings.id)
                else:
                    try:#### ----- Set up a code to switch over to a number based model instead of labels
                        chk_database = apps.get_model('EES_Forms', name_of_model).objects.filter(date__year=year, date__month=themonth, formSettings__id=iFormSettings.id)
                    except:
                        chk_database = apps.get_model('EES_Forms', name_of_model).objects.filter(week_start__year=year, week_start__month=themonth, formSettings__id=iFormSettings.id)
                
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
                chk_database = apps.get_model('EES_Forms', "form22_model").objects.filter(date__year=year, date__month=themonth, formSettings__id=fsEntry.id)
                print(form22_model.objects.all())
                originalStyle = True
            else:
                try:
                    print("CHECK 1.1")
                    chk_database = apps.get_model('EES_Forms', name_of_model).objects.filter(date__year=year, date__month=themonth, formSettings__id=fsEntry.id)
                    originalStyle = True
                except:
                    print("CHECK 1.2")
                    chk_database = apps.get_model('EES_Forms', name_of_model).objects.filter(week_start__year=year, week_start__month=themonth, formSettings__id=fsEntry.id)
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
            return redirect('sup_dashboard')

def sendToDash(user):
    userGroup = str(user.groups.all()[0])
    if userGroup == OBSER_VAR:
        return redirect('facilitySelect', 'observer')
    elif userGroup == CLIENT_VAR:
        userProfile = user_profile_model.objects.get(user=user)
        print('doskdhjflksdjflksfj')
        return redirect('c_dashboard', userProfile.facilityChoice.facility_name)
    elif userGroup == SUPER_VAR:
        return redirect('sup_dashboard')

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
    formSettingsQuery = form_settings_model.objects.filter(facilityChoice=facility, formChoice__frequency=frequency)
    count_total = formSettingsQuery.count()
    count_comp = formSettingsQuery.filter(subChoice__submitted=True).count()
    if count_total == 0:
        percent_completed = False
    else:
        percent_completed = (count_comp / count_total) * 100
    print(percent_completed)
    return percent_completed 

def ninetyDayPushTravels(facility):
    today = datetime.datetime.now().date()
    batInfo = facility
    most_recent_dates = {}
    all_records = form5_model.objects.filter(formSettings__facilityChoice=facility)
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
        
        totalOvens = int(batInfo.total_ovens)
        for i in range(1,totalOvens+1):
            already_exists = False
            for pt_oven in od_90:
                if i == int(pt_oven['oven_number']):
                    already_exists = True
            if not already_exists:
                ovenDictBuild = {
                    "oven_number": i,
                    "most_recent_date": "-",
                    "deadline": "-",
                    "days_left": "-",
                }
                od_90.append(ovenDictBuild)


        od_90 = sorted(od_90, key=lambda x: x["oven_number"])
        od_30 = sorted(od_30, key=lambda x: x["oven_number"])
        od_10 = sorted(od_10, key=lambda x: x["oven_number"])
        od_5 = sorted(od_5, key=lambda x: x["oven_number"])
        min_days_left = min(item['days_left'] for item in od_90 if isinstance(item['days_left'], int))
        od_closest = [entry for entry in od_90 if entry["days_left"] == min_days_left]
    
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

def notificationCalc(user, facility):
    userProfile = user.user_profile
    notifications = notifications_model.objects.filter(facilityChoice__facility_name=facility)
    newNotifs = notifications.filter(clicked=False, hovered=False, user=userProfile)
    if newNotifs.exists():
        notifCount = len(newNotifs)
    else:
        notifCount = 0

    #print(notifCount)
    return notifCount
    
def displayNotifications(user, facility):
    notifCount = notificationCalc(user, facility)
    nUserProfile = user.user_profile
    
    allNotifs = notifications_model.objects.filter(facilityChoice__facility_name=facility, user=nUserProfile).order_by('-created_at')
    
    unReadNotifs = allNotifs.filter(clicked=False, hovered=False)       
    readNotifs = allNotifs.filter(clicked=True)
    #print('-------Notifications have been processed------')
    return {'notifCount': notifCount, 'unRead': unReadNotifs, "read": readNotifs}

def distributeNotifications(facility, request, fsID, date, notifKeywordList, issueID, savedForm):
    #print(f"Start Notification Process for {facility} fsID {fsID}")
    #print(f"Notifications types: {notifKeywordList}")
    print(savedForm)
    userProf = request.user.user_profile
    formSettings = form_settings_model.objects.get(id=fsID)
    companyUsers = user_profile_model.objects.filter(company__company_name=userProf.company.company_name, user__is_active=True)
    #print(f"Users who will be receiving notifications: {companyUsers}")

    def createMethodPlusNotif(notifCategory, sendingUser, receivingUser, date, savedForm):
        #print(f"Creating 'Method Plus' Notification for {facility} fsID {fsID}")
        todayName = False
        todayNumb = datetime.date.today().weekday()
        if notifCategory == 'submitted':
            if todayNumb in {5,6}:
                if todayNumb == 5:
                    todayName = 'Saturday'
                else:
                    todayName = 'Sunday'
            print(f'This is the date right now: {date}')
            newNotifData = {'settingsID': fsID, 'date': str(date), 'weekend': todayName}
            print(savedForm)
            if savedForm.formSettings.formChoice.form == "26":
                newNotifData['spillKitID'] = savedForm.skID
            newNote = "Submitted by " + sendingUser.first_name + " " + sendingUser.last_name + ". "
        elif notifCategory in ['deviations', 'compliance']:
            newNotifData = {'settingsID': fsID, 'date': str(date)}
            newNote = "Submitted by " + sendingUser.first_name + " " + sendingUser.last_name + ". "
        elif notifCategory in ['10_day_pt', '5_day_pt']:
            formID = formSettings.formChoice.id
            newNotifData = {'ovenNumber': formID, 'date': str(date)}
            ten_day_note = "Oven has reach the 10 day warning."
            five_day_note = "Oven has reach the 5 day warning."
            newNote = ten_day_note if notifCategory == "10_day_pt" else five_day_note
        elif notifCategory == 'messages':
            #print('Inbox Messages: TBA')
            newNote = "newMessage sent."

        N = notifications_model(
            facilityChoice=formSettings.facilityChoice,
            formSettings=formSettings,
            user = receivingUser,
            clicked = False,
            hovered = False,
            formData = newNotifData,
            header = notifCategory,
            body = "Click here to view.",
            notes = newNote
        )
        return(N)
    
    def sendMethodPlusNotif(newNotification):
        notifQuery = notifications_model.objects.all()
        variables = {}
        variables['notif'] = newNotification
        variables['facility'] = facility
        if newNotification not in notifQuery:
            newNotification.save()
            #print(f"Notfiication for '{newNotification.header}' has succesfully been created within MethodPlus Database")
            clean_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', userProf.company.company_name)[:90]
            companyParse = f'notifications_{clean_name}'
            #notifCount = len(notifQuery.filter(user=receivingUser, hovered=False, clicked=False, facilityChoice__company=userProf.company))
            channel_layer = get_channel_layer()

            if newNotification.formSettings.formChoice.form in ['26']:
                variables['month'] = date.month
                variables['skNumber'] = savedForm.skID
            
            notif_html = render_to_string("shared/components/notification_item.html", variables)

            async_to_sync(channel_layer.group_send)(
                companyParse, {
                    'type': 'notification',
                    'notif_type': newNotification.header,
                    #'count': notifCount,
                    'facility': facility,
                    'facID': str(formSettings.facilityChoice.id),
                    'html': notif_html
                }
            )
            #print(f"Notfiication for '{newNotification.header}' has succesfully been sent to update the notif counter for the current user")

    def sendEmailNotif(notifCategory, receivingUser):
        #print(f"Creating 'Email' Notification for {facility} fsID {fsID}")
        header_dict = dict(notification_header_choices)
        header_dict.get(notifCategory, "Unknown Header")
        mail_subject = f'MethodPlus: {header_dict.get(notifCategory, "Unknown Header")}'
        current_site = get_current_site(request)

        html_message = render_to_string(f'email/{notifCategory}_email.html', {  
            'user': receivingUser,  
            'domain': current_site.domain,
            'form': formSettings,
            'issue': issueID
        })
        plain_message = strip_tags(html_message)
        to_email = receivingUser.user.email 
        #print(to_email)
        send_mail(
            mail_subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            [to_email],
            html_message=html_message,
            fail_silently=False
        )
        #print(f"Sending a '{notifCategory}' notifications to email")

    def sendSMSNotif(notifCategory, receivingUser):
        #print(f"Sending a '{notifCategory}' notifications to SMS")

        number = receivingUser.phone
        if notifCategory == 'compliance':
            message = f"Notice: A form recently submitted is out of compliance for {facility}. Log in to MethodPlus+ to review review the details."
        elif notifCategory == 'deviations':
            message = f"Notice: A corrective action has been submitted for {facility}. Please log in to your MethodPlus+ account to review the details."
        elif notifCategory == 'submitted':
            message = f"Update: A new form has been submitted. Please log in to your MethodPlus+ account to review the details."
        elif notifCategory == '10_day_pt':
            message = f"Reminder: A Push Travel oven reading is due in 10 days. Log in to your MethodPlus+ account for more information."
        elif notifCategory == '5_day_pt':
            message = f"Reminder: A Push Travel oven reading is due in 5 days. Log in to your MethodPlus+ account for more information."
        elif notifCategory == 'schedule':
            message = f"More words"

        try:
            sid = send_sms_message(number, message)
            print(f"Message sent! User: {receivingUser.user.first_name}")
        except Exception as e:
            print(f"Failed to send SMS: {e}")
    
    newNotifList = []
    for notifCategory in notifKeywordList:
        setter = 0
        for users in companyUsers:
            #print(f"Sending Notifications to {users.user.first_name} {users.user.last_name}")
            userNotifSettings = users.settings['facilities'][str(formSettings.facilityChoice.id)]['notifications']
            for nKey, notifMedium in userNotifSettings[notifCategory].items():
                if nKey == "methodplus" and notifMedium:
                    newNotif = createMethodPlusNotif(notifCategory, userProf.user, users, date, savedForm)
                    if setter == 0:
                        newNotifList.append(newNotif)
                    setter += 1
                if nKey == "email" and notifMedium:
                    sendEmailNotif(notifCategory, users)
                if nKey == "sms" and notifMedium:
                    sendSMSNotif(notifCategory, users)

    for newNotification in newNotifList:
        sendMethodPlusNotif(newNotification)

def createNotification(facility, request, fsID, date, notifSelector, issueID, savedForm):
    #print(f"Start Notification Process for {facility} fsID {fsID}")
    print(savedForm)
    if not isinstance(notifSelector, list):
        notifSelector = [notifSelector]
    savedForm = False if not savedForm else savedForm
    distributeNotifications(facility, request, fsID, date, notifSelector, issueID, savedForm)
    #print("_________________________________")
    
def checkIfFacilitySelected(user):
    if user.user_profile.position not in ['observer']:
        notifDict = {}
        sortedFacilityData = getCompanyFacilities(user.user_profile.company.company_name)
        for fac in sortedFacilityData:
            notifDict[fac.facility_name] = {'facName': fac, "notifData": displayNotifications(user, fac)}
        notifs = notifDict
        totalNotifs = sum([facil['notifData']['notifCount'] for key, facil in notifDict.items()])
        notifDict['notifCount'] = totalNotifs
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

def getCompanyFacilities(company_name):
    sortedFacilityData = facility_model.objects.filter(company__company_name=company_name)
    return sortedFacilityData

def checkIfMoreRegistrations(user):
    profileData = user.user_profile
    subscriptionData = profileData.company.subscription
    userCompany = profileData.company
    active_registrations = len(user_profile_model.objects.filter(~Q(position="client"), company=userCompany, user__is_active=True))
    if not subscriptionData:
        print('There is no Stripe entry in database for this Company/User.')
        return False

    if subscriptionData.settings['extra_users']:
        total_registrations = int(subscriptionData.settings['extra_users'])+2
    else:
        print('There is no Extra User Data in the database entry for this Company/User.')
        return False

    print(f"Active: {active_registrations}, Allowed: {total_registrations}")
    if active_registrations >= total_registrations:
        addMore = False
    else:
        addMore = True

    return (total_registrations, addMore)

def issueForm_picker(facility, date, fsID):
    fsIDChoice = form_settings_model.objects.get(id=fsID)
    if date == 'form' or date == 'edit':
        return False
    parsedDate = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    issueData = issues_model.objects.filter(date__exact=parsedDate, formChoice=fsIDChoice)
    if issueData.exists():
        issueData = issues_model.objects.get(date__exact=parsedDate, formChoice=fsIDChoice)
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
    print(type(time))
    if time:
        if isinstance(time, str):
            print(time)
            try:
                time = datetime.datetime.strptime(time, "%H:%M")
            except:
                time = datetime.datetime.strptime(time, "%H:%M:%S")
        time = time.strftime("%I:%M %p")
        print(time)
        return time
    else:
        return False
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
        )
        A2 = Forms(
            form=2,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form2",
            header="Method 303",
            title="Doors",
        )
        A3 = Forms(
            form=3,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form3",
            header="Method 303",
            title="Lids and Offtakes",
        )
        A4 = Forms(
            form=4,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form4",
            header="Method 303",
            title="Collection Main",
        )
        A5 = Forms(
            form=5,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form5",
            header="Method 9B",
            title="Push Travels",
        )
        B = Forms(
            form=6,
            frequency="Daily",
            day_freq='Weekdays',
            weekdays_only=True,
            weekend_only=False,
            link="form6",
            header="Method 9",
            title="Fugitive Dust Inspection",
        )
        C = Forms(
            form=7,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form7",
            header="Method 9D",
            title="Fugitive Dust Inspection Form",
        )
        D = Forms(
            form=8,
            frequency="Weekly",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form8",
            header="Method 9",
            title="Random Truck Inspection",
        )
        E = Forms(
            form=9,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form9",
            header="Method 9",
            title="Gooseneck Inspection",
        )
        F1 = Forms(
            form=10,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="form10",
            header="Waste Weekly Inspections",
            title="SIF / K087 Process Area (Satellite)",
        )
        F2 = Forms(
            form=11,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="form11",
            header="Waste Weekly Inspections",
            title="#1 Shop (Satellite Accumulation)",
        )
        F3 = Forms(
            form=12,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="form12",
            header="Waste Weekly Inspections",
            title="#2 Shop (Satellite Accumulation)",
        )
        F4 = Forms(
            form=13,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="form13",
            header="Waste Weekly Inspections",
            title="Battery (Satellite Accumulation)",
        )
        F5 = Forms(
            form=14,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="form14",
            header="Waste Weekly Inspections",
            title="Bio Plant (Satellite Accumulation)",
        )
        F6 = Forms(
            form=15,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="form15",
            header="Waste Weekly Inspections",
            title="No. 8 Tank Area (Satellite Accumulation)",
        )
        F7 = Forms(
            form=16,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="form16",
            header="Waste Weekly Inspections",
            title="Booster Pad (90-Day Accumulation)",
        )
        G1 = Forms(
            form=17,
            frequency="Weekly",
            day_freq='Weekdays',
            weekdays_only=False,
            weekend_only=False,
            link="form17",
            header="PECS Baghouse Stack",
            title="Method 9/Non-Certified Observations",
        )
        G2 = Forms(
            form=18,
            frequency="Monthly",
            day_freq='Weekdays',
            weekdays_only=False,
            weekend_only=False,
            link="form18",
            header="PECS Baghouse Stack",
            title="Method 9B",
        )
        H = Forms(
            form=19,
            frequency="Weekly",
            day_freq='Weekdays',
            weekdays_only=False,
            weekend_only=False,
            link="form19",
            header="Method 9",
            title="Method 9 - Combustion Stack",
        )
        I = Forms(
            form=20,
            frequency="Daily",
            day_freq='Weekdays',
            weekdays_only=True,
            weekend_only=False,
            link="form20",
            header="Sampling",
            title="Quench Water Sampling Form",
        )
        L = Forms(
            form=21,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form21",
            header="Method 9",
            title="Visual Emissions Observations",
        )
        M = Forms(
            form=22,
            frequency="Daily",
            day_freq='Weekdays',
            weekdays_only=True,
            weekend_only=False,
            link="form22",
            header="Method 9D",
            title="Method 9D Observation",
        )
        N = Forms(
            form=23,
            frequency="Monthly",
            day_freq='Weekdays',
            weekdays_only=False,
            weekend_only=False,
            link="form23",
            header="Fugitive Dust Inspection",
            title="Method 9D Monthly Checklist",
        )
        O = Forms(
            form=24,
            frequency="Weekly",
            day_freq='Daily',
            weekdays_only=False,
            weekend_only=True,
            link="form24",
            header="Stormwater Observation Form",
            title="MP 108A",
        )
        P = Forms(
            form=25,
            frequency="Daily",
            day_freq='Weekends',
            weekdays_only=False,
            weekend_only=True,
            link="form25",
            header="Outfall Observation Form",
            title="Outfall 008",
        )
        spill_kits_inventory = Forms(
            form=26,
            frequency="Monthly",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form26",
            header="Spill Kit Inventory Form",
            title="Inspection Check List",
        )
        quarterly_trucks = Forms(
            form=27,
            frequency="Quarterly",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form27",
            header="Quarterly Trucks Form",
            title="Inspection Check List",
        )
        STI_SP001_monthly_inspection = Forms(
            form=28,
            frequency="Monthly",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form28",
            header="STI SP001",
            title="Monthly Tank Inspection Checklist",
        )
        form29 = Forms(
            form=29,
            frequency="Monthly",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form29",
            header="Spill Kits Form",
            title="Inspection Check List",
        )
        form30 = Forms(
            form=30,
            frequency="Weekly",
            day_freq='Wednesday',
            weekdays_only=False,
            weekend_only=False,
            link="form30",
            header="Facility Waste Weekly",
            title="Inspection Form",
        )
        form31 = Forms(
            form=31,
            frequency="Monthly",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form31",
            header="Monthly Tank Inspection",
            title="Tank Inspection Form (Multiple)",
        )

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
        form29.save()
        form30.save()
        form31.save()
        
def updateAllFormSubmissions(facility):
    facFormsSettingsModel = form_settings_model.objects.filter(facilityChoice=facility)
    today = datetime.date.today()
    todays_num = today.weekday()
    weekday_fri = today + datetime.timedelta(days=4 - todays_num)
    for fsForm in facFormsSettingsModel:
        sub = fsForm.subChoice
        formChoice = fsForm.formChoice
        if formChoice.frequency == 'Monthly':
            numbOfDaysInMonth = calendar.monthrange(today.year, today.month)[1]
            lastDayOfMonth = str(today.year) + '-' + str(today.month) + '-' + str(numbOfDaysInMonth)
            sub.dueDate = datetime.datetime.strptime(lastDayOfMonth, "%Y-%m-%d").date()
            dueDate = sub.dueDate
            if sub.dateSubmitted.year != dueDate.year or sub.dateSubmitted.month != dueDate.month:
                sub.submitted = False
            sub.save()
        elif formChoice.frequency == 'Quarterly':
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
        elif formChoice.frequency == 'Weekly':
            if todays_num in {0, 1, 2, 3, 4}:
                if formChoice.day_freq == 'Weekends':
                    sub.dueDate = weekday_fri - datetime.timedelta(days=5)
                start_sat = weekday_fri - datetime.timedelta(days=6)
                sub.dueDate = weekday_fri
            else:
                start_sat = today - datetime.timedelta(days= todays_num - 5)
                sub.dueDate = start_sat + datetime.timedelta(days=11 - todays_num)
            A = sub.dateSubmitted
            B = sub.dueDate
            if formChoice.day_freq == 'Weekends' and A != B:
                sub.submitted = False   
            elif A < start_sat or A > sub.dueDate:
                sub.submitted = False
            sub.save()
        elif formChoice.frequency == 'Daily':
            if formChoice.weekend_only and todays_num not in {5,6}:
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

def change_dashboard_setting(dashChoice, position):
    if dashChoice == 'Default':
        setSettings = {}
        setNotifications = {}
    elif dashChoice == "Battery":
        if position == OBSER_VAR:
            setSettings = {}
        else:
            setSettings = defaultBatteryDashSettings
        setNotifications = defaultNotifications
    
    setFacilityDash = {
        'dashboard': dashChoice, 
        'settings': setSettings,
        'notifications': setNotifications
    }
    return setFacilityDash

def setDefaultSettings(profile):
    today = datetime.datetime.now()
    createSettings = {'facilities': {}, 'profile': {}, 'calendar': {}}
    try:
        companyFacilities = getCompanyFacilities(profile.company.company_name)
        for facility in companyFacilities:
            createSettings['facilities'][str(facility.id)] = dashDict
            if facility.is_battery == 'Yes':
                dashChoice = 'Battery'
            else:
                dashChoice = 'Default'
            createSettings['facilities'][str(facility.id)] = change_dashboard_setting(dashChoice, profile.position)
    except:
        createSettings['facilities'] = {}
    
    ## SET SETTINGS FOR PROFILE
    createSettings['profile'] = {
        'notifications': {
            'certification_exp': {
                'methodplus': True, 
                'email': False, 
                'sms': False
            }
        },
        'first_login': False,
        'position': profile.position,
        'two_factor_enabled': True
    }

    ## SET SETTINGS FOR CALENDAR
    createSettings['calendar'] = {
        "notifications": {
            "event_added": {
                "methodplus": True, 
                "email": False, 
                "sms": False
            }
        },
        "calendars": {
            "default": [
                {
                    "name": "personal", 
                    "color": "#ff000082"
                }    
            ],
            "custom": []
        }
    }
    return createSettings

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

# def get_initial_data(modelName, modelInstance):
#     def get_field_value(fieldName, modelList):
#         for source in modelList:
#             if hasattr(source, fieldName):  # Check if the field exists
#                 return getattr(source, fieldName)
#         return None  # Fallback value if neither has the attribute

#     allModelFields = [
#         field.name for field in modelName._meta.get_fields() 
#         if isinstance(field, Field) and field.name not in ["id","facilityChoice"]
#     ]
#     modelList = [modelInstance]
#     try:
#         model_name = modelName._meta.object_name.replace("_model", "_readings_model")
#         content_type = ContentType.objects.get(model=model_name.lower())
#         modelInstance2 = content_type.model_class().objects.get(form=modelInstance)
#         model2Fields = [
#             field.name for field in modelInstance2._meta.get_fields() 
#             if isinstance(field, Field) and field.name not in ["id","form"]
#         ]
#         allModelFields = allModelFields + model2Fields
#         modelList.append(modelInstance2)
#     except:
#         print('only one model')
#     initial_data = {fieldName: get_field_value(fieldName, modelList) for fieldName in allModelFields}
#     return initial_data


def get_initial_data(modelName, modelInstance):
    def get_field_value(fieldName, modelList):
        for source in modelList:
            if hasattr(source, fieldName):  # Check if the field exists
                attrData = getattr(source, fieldName)
                if isinstance(attrData, dict):
                    inner_dict = { iFieldKey: iFieldValue for iFieldKey, iFieldValue in attrData.items() }
                    return inner_dict
                else:
                    return attrData
        return None  # Fallback value if neither has the attribute

    allModelFields = [
        field.name for field in modelName._meta.get_fields() 
        if isinstance(field, Field) and field.name not in ["id"]
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




def fix_data(fsID):
    freq = getFacSettingsInfo(fsID)
    selectedModel = apps.get_model('EES_Forms', freq.formChoice.link + "_model")
    modelAllQuery = selectedModel.objects.all()
    for x in modelAllQuery:
        x.formSettings = freq
        x.save()


happy = {
    "area1": {
        "options": {
            "1": "Contractor", 
            "2": "Truck #5", 
            "3": "Truck #6", 
            "4": "Truck #7", 
            "5": "Truck #9", 
            "6": "Dozer", 
            "7": "Water Truck"
        }, 
        "name": "Truck", 
        "number_of_options": 7
    }
}

packetList = [
    {
        "PACKET": "PACKET_SELECTED",
        "FORMS": {
            "COMPLETE": [
                "FSID_SELECTION",
                "FSID_SELECTION"
            ],
            "INCOMPLETE": [
                "FSID_SELECTION",
                "FSID_SELECTION"
            ]
        }
    },
    {
        "PACKET": "PACKET_SELECTED",
        "FORMS": {
            "COMPLETE": [
                "FSID_SELECTION",
                "FSID_SELECTION"
            ],
            "INCOMPLETE": [
                "FSID_SELECTION",
                "FSID_SELECTION"
            ]
        }
    },
]

user_prof_settings = {
    "facilities": {
        "6": {
            "dashboard": "Battery", 
            "settings": {
                "progressBar": {
                    "progressDaily": True, 
                    "progressWeekly": True, 
                    "progressMonthly": True, 
                    "progressQuarterly": True, 
                    "progressAnnually": False
                }, 
                "graphs": {
                    "graphFrequencyData": {
                        "frequency": "weekly", 
                        "dates": False
                    }, 
                    "dataChoice": {
                        "charges": {
                            "show": True, 
                            "type": "bar"
                        }, 
                        "doors": {
                            "show": True, 
                            "type": "bar"
                        }, 
                        "lids": {
                            "show": True, 
                            "type": "bar"
                        }, 
                        "graph90dayPT": {
                            "show": False, 
                            "type": "bar"
                        }
                    }
                }, 
                "correctiveActions": True, 
                "infoWeather": True, 
                "90dayPT": True, 
                "contacts": True
            }, 
            "notifications": {
                "compliance": {
                    "methodplus": True, 
                    "email": False, 
                    "sms": False
                }, 
                "deviations": {
                    "methodplus": True, 
                    "email": False, 
                    "sms": False
                }, 
                "submitted": {
                    "methodplus": True, 
                    "email": False, 
                    "sms": False
                }, 
                "10_day_pt": {
                    "methodplus": False, 
                    "email": False, 
                    "sms": False
                }, 
                "5_day_pt": {
                    "methodplus": False, 
                    "email": False, 
                    "sms": False
                }
            }
        }, 
        "7": {
            "dashboard": "Default", 
            "settings": {}, 
            "notifications": {}
        }, 
        "10": {
            "dashboard": "Default", 
            "settings": {}, 
            "notifications": {}
        }, 
        "11": {
            "dashboard": "Default", 
            "settings": {}, 
            "notifications": {}
        }
    }, 
    "profile": {
        "notifications": {
            "calendar": {
                "methodplus": True, 
                "email": False, 
                "sms": False
            }, 
            "certification_exp": {
                "methodplus": True, 
                "email": False, 
                "sms": False
            }
        }, 
        "first_login": True, 
        "position": "supervisor-m", 
        "two_factor_enabled": False,
    },
    "calendar": {
        "notifications": {
            "event_added": {
                "methodplus": True, 
                "email": False, 
                "sms": False
            }
        },
        "calendars": {
            "personal": {
                "name": "personal",
                "type": "default"
            },
            "company": {
                "name": "personal",
                "type": "default"
            },
            "facilities": [],
            "custom": []
        }
    }
}

defaultDataForm20 = {
    "Monday": False,
    "Tuesday": False,
    "Wednesday": False,
    "Thursday": False,
    "Friday": False,
    "Saturday": False,
    "Sunday": False
}

form24build = {
    "q1": "yes",
    "comments": "ceooments",
    "actions_taken": "blah blah blah"
}

def get_day_number_from_name(day_name):
    """
    Converts a weekday name (e.g. 'Monday') to its corresponding integer (0=Monday, ..., 6=Sunday).
    Returns -1 if the input is invalid or not a recognized day name.
    """
    weekday_map = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }

    # Normalize the input: strip whitespace and capitalize
    normalized = day_name.strip().capitalize() if isinstance(day_name, str) else ''
    return weekday_map.get(normalized, -1)

