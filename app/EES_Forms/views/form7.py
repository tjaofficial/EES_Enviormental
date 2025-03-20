from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from datetime import datetime
from ..models import form_settings_model
from ..forms import form7_form
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
import json

lock = login_required(login_url='Login')

@lock
def form7(request, facility, fsID, selector):
    # -----SET MAIN VARIABLES------------
    form_variables = initiate_form_variables(fsID, request.user, facility, selector)
    cert_date = request.user.user_profile_model.cert_date if request.user.user_profile_model else False
    # -----CHECK DAILY_BATTERY_PROF OR REDIRECT------------
    if form_variables['daily_prof'].exists():
        todays_log = form_variables['daily_prof'][0]
    # -----SET DECIDING VARIABLES------------
        more_form_variables = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request) 
        if isinstance(more_form_variables, HttpResponseRedirect):
            return more_form_variables
        else:
            data, existing, search, database_form = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request)
    # -----SET RESPONSES TO DECIDING VARIABLES------------
        if search:
            database_form = ''
        else:
            areaFilled1 = []
            if existing:
                initial_areas = {}
                readsData = {}
                dataBaseInputList = data._meta.get_fields()
                for inputData in dataBaseInputList:
                    if inputData.name[:-1] == 'area_json_':
                        if getattr(data, inputData.name) != {}:
                            areaFilled1.append(inputData.name[10:])
                initial_data = {
                    'date': data.date.strftime("%Y-%m-%d"),
                    'observer': data.observer,
                    'cert_date': data.cert_date.strftime("%Y-%m-%d"),
                    'comments': data.comments
                }
                for x in areaFilled1:
                    x = str(x)
                    if x == "1":
                        area = data.area_json_1
                    elif x == "2":
                        area = data.area_json_2
                    elif x == "3":
                        area = data.area_json_3
                    elif x == "4":
                        area = data.area_json_4
                    intital_adding = {
                        x: {
                            'name': area['selection'],
                            'startTime': datetime.strptime(area['start_time'], "%H:%M").strftime("%H:%M"),
                            'stopTime': datetime.strptime(area['stop_time'], "%H:%M").strftime("%H:%M"),
                            'average': area['average'],
                        }
                    }
                    initial_data_dict = {
                        x: [
                            area['readings']['1'], 
                            area['readings']['2'], 
                            area['readings']['3'], 
                            area['readings']['3'], 
                            area['readings']['4'], 
                            area['readings']['5'], 
                            area['readings']['6'],
                            area['readings']['7'],
                            area['readings']['8'],
                            area['readings']['9'],
                            area['readings']['10'],
                            area['readings']['11']
                        ]
                    }
                    initial_areas.update(intital_adding)
                    readsData.update(initial_data_dict)
                allData = {"main": initial_data, "primary": initial_areas, "readings": readsData}
                print(allData["readings"])
            else:
                initial_data = {
                    'date': form_variables['now'].strftime("%Y-%m-%d"),
                    'observer': form_variables['full_name'],
                    'cert_date': cert_date.strftime("%Y-%m-%d"),
                }
                areaFilled1 += ["1","2","3","4"]
                allData = {"main": initial_data, "primary": {}, "readings": {}}
    # -----IF REQUEST.POST------------
        if request.method == "POST":
    # -----CREATE COPYPOST FOR ANY ADDITIONAL INPUTS/VARIABLES------------
            copyRequest = request.POST.copy()
            areaFilled = []
            for formKeys in request.POST.keys():
                if formKeys[:8] == 'areaName':
                    if request.POST["areaStartTime" + formKeys[8:]] != '':
                        areaFilled.append(formKeys[8:])
            for x in areaFilled:
                x = str(x)
                areaSetup= {
                    "selection": request.POST[f"areaName{x}"],
                    "start_time": request.POST[f"areaStartTime{x}"],
                    "stop_time": request.POST[f"areaStopTime{x}"],
                    "readings": {
                        "1": int(request.POST['area' + x + 'Read0']),
                        "2": int(request.POST['area' + x + 'Read1']),
                        "3": int(request.POST['area' + x + 'Read2']),
                        "4": int(request.POST['area' + x + 'Read3']),
                        "5": int(request.POST['area' + x + 'Read4']),
                        "6": int(request.POST['area' + x + 'Read5']),
                        "7": int(request.POST['area' + x + 'Read6']),
                        "8": int(request.POST['area' + x + 'Read7']),
                        "9": int(request.POST['area' + x + 'Read8']),
                        "10": int(request.POST['area' + x + 'Read9']),
                        "11": int(request.POST['area' + x + 'Read10']),
                        "12": int(request.POST['area' + x + 'Read11']),
                    },
                    "average": int(request.POST['areaAverage' + x])
                }
                areaSetup = json.loads(json.dumps(areaSetup))
                copyRequest[f'area_json_{x}'] = areaSetup

            try:
                form_settings = form_variables['freq']
            except form_settings_model.DoesNotExist:
                raise ValueError(f"Error: form_settings_model with ID {fsID} does not exist.")
    # -----SET FORM VARIABLE IN RESPONSE TO DECIDING VARIABLES------------
            if existing:
                form = form7_form(copyRequest, instance=database_form, form_settings=form_settings)
            else:
                form = form7_form(copyRequest, form_settings=form_settings)
    # -----VALIDATE, CHECK FOR ISSUES, CREATE NOTIF, UPDATE SUBMISSION FORM------------
            exportVariables = (request, selector, facility, database_form, fsID)
            return redirect(*template_validate_save(form, form_variables, *exportVariables))
    else:
        batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    return render(request, "shared/forms/daily/formC.html", {
        'fsID': fsID, 
        'picker': form_variables['picker'], 
        "search": search, 
        "client": form_variables['client'], 
        'unlock': form_variables['unlock'], 
        'supervisor': form_variables['supervisor'], 
        'selector': selector, 
        'formName': form_variables['formName'], 
        'facility': facility,
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
        'existing': existing,
        'allData': allData,
        "areaFilled1": areaFilled1,
    })
