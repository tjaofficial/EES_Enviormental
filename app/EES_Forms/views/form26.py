from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.http import HttpResponseRedirect # type: ignore
from ..models import form_settings_model, form29_model
from ..forms import form26_form
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
import ast

lock = login_required(login_url='Login')

@lock
def form26(request, facility, fsID, month, skNumber, selector):
    # -----SET MAIN VARIABLES------------
    form_variables = initiate_form_variables(fsID, request.user, facility, selector)
    attachedTo = form29_model.objects.filter(month=month)
    formAttached = attachedTo[0] if len(attachedTo) > 0 else "form"
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
            print('CHECK 1.1')
            database_form = ''
            data2 = {
                "counted_items": ast.literal_eval(data.counted_items),
                "missing_items": ast.literal_eval(data.missing_items)
            }
            print(data2)
        else:
            if existing:
                print('CHECK 2.1')
                initial_data = {
                    "date": database_form.date,
                    "inspector":  database_form.inspector,
                    'skID':  database_form.skID,
                    "type":  database_form.type,
                }
                data2 = {
                    "counted_items": ast.literal_eval(database_form.counted_items),
                    "missing_items": ast.literal_eval(database_form.missing_items)
                }
                print(data2['counted_items'][0])
                print(selector)
            else:
                print('CHECK 3')
                initial_data = {
                    "date": todays_log.date_save,
                    "inspector":  form_variables['full_name'],
                    'skID':  skNumber
                }
                data2 = ''
            data = form26_form(initial=initial_data, form_settings=form_variables['freq'])
    # -----IF REQUEST.POST------------
        if request.method == "POST":
    # -----CREATE COPYPOST FOR ANY ADDITIONAL INPUTS/VARIABLES------------
            dataPOST = request.POST
            if len(attachedTo) > 0:
                skSubmitted = attachedTo[0]
            copyData = request.POST.copy()
            if dataPOST['type'] == 'oil XL cart':
                copyData['counted_items'] = [
                    dataPOST['t1count1'],
                    dataPOST['t1count2'],
                    dataPOST['t1count3'],
                    dataPOST['t1count4'],
                    dataPOST['t1count5'],
                    dataPOST['t1count6'],
                    dataPOST['t1count7'],
                    dataPOST['t1count8'],
                    dataPOST['t1count9'],
                    dataPOST['t1count10']
                ]
                copyData['missing_items'] = [
                    dataPOST['t1miss1'],
                    dataPOST['t1miss2'],
                    dataPOST['t1miss3'],
                    dataPOST['t1miss4'],
                    dataPOST['t1miss5'],
                    dataPOST['t1miss6'],
                    dataPOST['t1miss7'],
                    dataPOST['t1miss8'],
                    dataPOST['t1miss9'],
                    dataPOST['t1miss10']
                ]
            else:
                copyData['counted_items'] = [
                    dataPOST['t2count1'],
                    dataPOST['t2count2'],
                    dataPOST['t2count3'],
                    dataPOST['t2count4'],
                    dataPOST['t2count5'],
                    dataPOST['t2count6'],
                    dataPOST['t2count7'],
                    dataPOST['t2count8'],
                    dataPOST['t2count9']
                ]
                copyData['missing_items'] = [
                    dataPOST['t2miss1'],
                    dataPOST['t2miss2'],
                    dataPOST['t2miss3'],
                    dataPOST['t2miss4'],
                    dataPOST['t2miss5'],
                    dataPOST['t2miss6'],
                    dataPOST['t2miss7'],
                    dataPOST['t2miss8'],
                    dataPOST['t2miss9']
                ]
            #copyData['spill_kit_submitted'] = skSubmitted
            print(copyData)
            copyData['facilityChoice'] = form_variables['freq'].facilityChoice

            try:
                form_settings = form_variables['freq']
            except form_settings_model.DoesNotExist:
                raise ValueError(f"Error: form_settings_model with ID {fsID} does not exist.")
    # -----SET FORM VARIABLE IN RESPONSE TO DECIDING VARIABLES------------
            if existing:
                form = form26_form(copyData, instance=database_form, form_settings=form_settings)
            else:
                form = form26_form(copyData, form_settings=form_settings)
    # -----VALIDATE, CHECK FOR ISSUES, CREATE NOTIF, UPDATE SUBMISSION FORM------------
            exportVariables = (request, selector, facility, database_form, fsID)
            return redirect(*template_validate_save(form, form_variables, *exportVariables))
    else:
        batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
                
    return render(request, "shared/forms/monthly/spillKits_inventoryForm.html",{
        'full_name': form_variables['full_name'],
        'skNumber': skNumber, 
        'facility': facility, 
        'supervisor': form_variables['supervisor'], 
        "client": form_variables['client'], 
        'unlock': form_variables['unlock'], 
        'formName': form_variables['formName'], 
        "data": data, 
        "search": search, 
        "existing": existing, 
        "data2": data2, 
        "selector": selector,
        'fsID': fsID,
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
    })