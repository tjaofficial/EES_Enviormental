from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from ..models import form_settings_model, form29_model, form26_model
from ..forms import form29_form
from ..utils import createNotification, get_initial_data, stringToDate, updateSubmissionForm
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
import calendar
import json
from datetime import datetime

lock = login_required(login_url='Login')

@lock
def form29(request, facility, fsID, selector):
    # -----SET MAIN VARIABLES------------
    form_variables = initiate_form_variables(fsID, request.user, facility, selector)
    sk_form = form29_form(form_settings=form_variables['freq'])
    month_name = calendar.month_name[form_variables['now'].month]
    # -----CHECK DAILY_BATTERY_PROF OR REDIRECT------------
    if form_variables['daily_prof'].exists():
        todays_log = form_variables['daily_prof'][0]
    # -----SET DECIDING VARIABLES------------
        more_form_variables = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request, fsID) 
        if isinstance(more_form_variables, HttpResponseRedirect):
            return more_form_variables
        else:
            data, existing, search, database_form = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request, fsID)
    # -----SET RESPONSES TO DECIDING VARIABLES------------
        if selector != 'form':
            form_query = form_variables['submitted_forms'].filter(date=datetime.strptime(selector, "%Y-%m-%d").date())
            database_model = form_query[0] if form_query.exists() else print('no data found with this date')
            data = database_model
            existing = True
            search = True
        elif form_variables['now'] == todays_log.date_save:
            if form_variables['submitted_forms'].exists():
                database_form = form_variables['submitted_forms'][0]
                datetime_object = datetime.strptime(database_form.month, "%B")
                month_number = datetime_object.month
                if form_variables['now'].month == month_number:
                    existing = True
        else:
            batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
            return redirect('daily_battery_profile', facility, "login", batt_prof_date)

        iFormList = {}
        if search:
            print('CHECK 1.2')
            database_form = ''
            month = database_model.month
            inventoryModel = form26_model.objects.filter(date__month=database_model.date.month)
            for subForm in inventoryModel:
                iFormList[subForm.skID] = [subForm.skID,stringToDate(subForm.date)]
            iFormList = json.dumps(iFormList)
        else:
            inventoryModel = form26_model.objects.filter(date__month=form_variables['now'].month)
            if inventoryModel.exists():
                for subForm in inventoryModel:
                    iFormList[subForm.skID] = [subForm.skID,stringToDate(subForm.date)]
                iFormList = json.dumps(iFormList)
            if existing:
                month = database_form.month
                initial_data = get_initial_data(form29_model, database_form)
            else:
                month = month_name
                initial_data = {
                    'observer': form_variables['full_name'],
                    'date': form_variables['now'],
                    'month': month_name,
                }
            data = form29_form(initial=initial_data, form_settings=form_variables['freq'])
    # -----IF REQUEST.POST------------
        if request.method == "POST":
    # -----CREATE COPYPOST FOR ANY ADDITIONAL INPUTS/VARIABLES------------
            copyPOST = request.POST.copy()
            copyPOST["facilityChoice"] = form_variables['freq'].facilityChoice
            
            try:
                form_settings = form_variables['freq']
            except form_settings_model.DoesNotExist:
                raise ValueError(f"Error: form_settings_model with ID {fsID} does not exist.")
    # -----SET FORM VARIABLE IN RESPONSE TO DECIDING VARIABLES------------
            if existing:
                form = form29_form(copyPOST, instance=database_form, form_settings=form_settings)
            else:
                form = form29_form(copyPOST, form_settings=form_settings)
    # -----VALIDATE, CHECK FOR ISSUES, CREATE NOTIF, UPDATE SUBMISSION FORM------------
            exportVariables = (request, selector, facility, database_form, fsID)
            return redirect(*template_validate_save(form, form_variables, *exportVariables))
            if form.is_valid():
                form.save()
                
                new_latest_form = form29_model.objects.filter(month=month_name)[0]
                filled_out = True
                for items in new_latest_form.whatever().values():
                    print(items)
                    if items is None or items == '':
                        filled_out = False  # -change this back to false
                        break

                if filled_out:
                    createNotification(facility, request, fsID, form_variables['now'], 'submitted', False)    
                    updateSubmissionForm(fsID, True, todays_log.date_save)
                    
                return redirect('IncompleteForms', facility)
    else:
        batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    return render(request, "shared/forms/monthly/spillkits_form.html", {
        'iFormList': iFormList, 
        'month': month, 
        'facility': facility, 
        'sk_form': data, 
        'selector': selector, 
        'supervisor': form_variables['supervisor'], 
        "client": form_variables['client'], 
        'unlock': form_variables['unlock'], 
        'formName': form_variables['formName'], 
        'search': search, 
        'existing': existing,
        'fsID': fsID,
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq']
    })