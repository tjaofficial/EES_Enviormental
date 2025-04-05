from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from ..models import form8_model, form_settings_model
from ..forms import form8_form
from ..utils import get_initial_data
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
from datetime import timedelta

lock = login_required(login_url='Login')

@lock
def form8(request, facility, fsID, selector):
    # -----SET MAIN VARIABLES------------
    form_variables = initiate_form_variables(fsID, request.user, facility, selector)
    last_saturday = form_variables['now'] - timedelta(days=form_variables['now'].weekday() + 2)
    one_week = timedelta(days=6)
    end_week = last_saturday + one_week
    sunday = form_variables['now'] - timedelta(days=1)
    # -----CHECK DAILY_BATTERY_PROF OR REDIRECT------------
    if form_variables['daily_prof'].exists():
        todays_log = form_variables['daily_prof'][0]
    # -----SET DECIDING VARIABLES------------
        more_form_variables = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request) 
        if isinstance(more_form_variables, HttpResponseRedirect):
            return more_form_variables
        else:
            data, existing, search, database_form = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request)

        # if form_variables['submitted_forms'].exists():

        #     starting_saturday = database_form.week_start
        #     if form_variables['now'].weekday() not in {5, 6}:
        #         if starting_saturday == last_saturday:
        #             existing = True
        #     elif form_variables['now'].weekday() == 5:
        #         if starting_saturday == form_variables['now']:
        #             existing = True
        #     elif starting_saturday == sunday:
        #         existing = True
    # -----SET RESPONSES TO DECIDING VARIABLES------------    
        if search:
            database_form = ''
        else:
            if existing:
                # initial_data = {
                #     'week_start': database_form.week_start,
                #     'week_end': database_form.week_end,
                # }
                # attrList = [
                #     'observer',
                #     'truck_id',
                #     'time',
                #     'date',
                #     'contents',
                #     'freeboard',
                #     'wetted',
                #     'comments'
                # ]
                # for i in range(1, 6):
                #     for attLabel in attrList:
                #         item_value = getattr(database_form, f"{attLabel}{i}")
                #         if item_value and item_value != None:
                #             if attLabel == 'date':
                #                 initial_data[attLabel+str(i)] = item_value.strftime("%Y-%m-%d")
                #             elif attLabel == 'time':
                #                 initial_data[attLabel+str(i)] = item_value.strftime("%H:%M")
                #             else:
                #                 initial_data[attLabel+str(i)] = item_value
                initial_data = get_initial_data(form8_model, database_form)
                print(f"hello: {existing}")
            else:
                if form_variables['now'].weekday() == 5:
                    initial_data = {
                        'week_start': form_variables['now'],
                        'week_end': form_variables['now'] + timedelta(days=6)
                    }
                elif form_variables['now'].weekday() == 6:
                    initial_data = {
                        'week_start': form_variables['now'] - timedelta(days=1),
                        'week_end': form_variables['now'] + timedelta(days=5)
                    }
                else:
                    initial_data = {
                        'week_start': last_saturday,
                        'week_end': end_week
                    }
            data = form8_form(initial=initial_data, form_settings=form_variables['freq'])
    # -----IF REQUEST.POST------------
        if request.method == "POST":
    # -----CREATE COPYPOST FOR ANY ADDITIONAL INPUTS/VARIABLES------------
            try:
                form_settings = form_variables['freq']
            except form_settings_model.DoesNotExist:
                raise ValueError(f"Error: form_settings_model with ID {fsID} does not exist.")
    # -----SET FORM VARIABLE IN RESPONSE TO DECIDING VARIABLES------------
            if existing:
                print("check 2")
                form = form8_form(request.POST, instance=database_form, form_settings=form_settings)
            else:
                print("check 2.1")
                form = form8_form(request.POST, form_settings=form_settings)
    # -----VALIDATE, CHECK FOR ISSUES, CREATE NOTIF, UPDATE SUBMISSION FORM------------
            exportVariables = (request, selector, facility, database_form, fsID)
            return redirect(*template_validate_save(form, form_variables, *exportVariables))
    else:
        batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)

    return render(request, "shared/forms/weekly/form8.html", {
        'fsID': fsID, 
        'picker': form_variables['picker'], 
        "search": search, 
        "client": form_variables['client'], 
        'unlock': form_variables['unlock'], 
        'supervisor': form_variables['supervisor'], 
        'form': data, 

        'todays_log': todays_log, 
        'selector': selector, 
        'formName': form_variables['formName'], 
        'facility': facility,
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
        'amountOfTrucks': [1,2,3,4,5],
    })
