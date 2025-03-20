from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from ..models import form_settings_model, form20_model
from ..forms import form20_form
from ..utils import get_initial_data
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
from datetime import timedelta

lock = login_required(login_url='Login')

@lock
def form20(request, facility, fsID, selector):
    # -----SET MAIN VARIABLES------------
    form_variables = initiate_form_variables(fsID, request.user, facility, selector)
    week_start_dates = form_variables['submitted_forms']
    last_monday = form_variables['now'] - timedelta(days=form_variables['now'].weekday())
    one_week = timedelta(days=4)
    end_week = last_monday + one_week
    today_number = form_variables['now'].weekday()
    opened = True
    submit = True
    filled_in = False
    partial_form = False
    week = ''
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
        # if selector not in ('form', 'edit'):
        #     submit = False
        #     form_query = week_start_dates.filter(week_start=datetime.strptime(selector, "%Y-%m-%d").date())
        #     database_model = form_query[0] if form_query.exists() else print('no data found with this date')
        #     data = database_model
        #     existing = True
        #     search = True
        #     filled_in = True
        # elif week_start_dates.exists():
        #     print('CHECK 3')
        #     database_model = week_start_dates[0]
        #     week = database_model.week_start
        #     # ------- check if todays data has been filled in or not
        #     home = []

        #     for x in form20_model.objects.all():
        #         if x.week_start == last_monday:
        #             home.append((x.time_4, 4))
        #             home.append((x.time_3, 3))
        #             home.append((x.time_2, 2))
        #             home.append((x.time_1, 1))
        #             home.append((x.time_0, 0))
                    
        #     print(home)
        #     for days in home:
        #         if days[0]:
        #             partial_form = True
        #             if days[1] == today_number:
        #                 filled_in = True
        #     # -----check if today is a Weekday
        #     if today_number not in {5, 6}:
        #         print('CHECK 3.1')
        #         # --------FORM------------FORM----------FORM-------------
        #         if selector == 'form':
        #             print(week)
        #             print(last_monday)
        #             if week == last_monday:
        #                 if filled_in or partial_form:
        #                     data = database_model
        #                     submit = False
        #                     existing = True
        #         # --------EDIT------------EDIT----------EDIT-------------
        #         elif selector == 'edit':
        #             if week == last_monday:
        #                 filled_in = False
        #                 existing = True
        #     elif today_number == 5:
        #         print('CHECK 3.2')
        #         opened = False
        #         submit = False
        #         initial_data = {
        #             'week_start': form_variables['now'],
        #             'week_end': form_variables['now'] + one_week
        #         }
        #         data = form20_form(initial=initial_data)
        #     else:
        #         print('CHECK 3.3')
        #         opened = False
        #         submit = False
        #         initial_data = {
        #             'week_start': form_variables['now'] - datetime.timedelta(days=1),
        #             'week_end': form_variables['now'] + one_week
        #         }
        #         data = form20_form(initial=initial_data)
                
        if existing:
            print('Check 2.1')
            initial_data = get_initial_data(form20_model, database_form)
            if filled_in:
                data = database_form
            else:
                print('Check 2.2')
                data = form20_form(initial=initial_data, form_settings=form_variables['freq'])
        else:
            initial_data = {
                'week_start': last_monday,
                'week_end': end_week
            }
            data = form20_form(initial=initial_data, form_settings=form_variables['freq'])

        # -----IF REQUEST.POST------------
        if request.method == "POST":
    # -----CREATE COPYPOST FOR ANY ADDITIONAL INPUTS/VARIABLES------------
            try:
                form_settings = form_variables['freq']
            except form_settings_model.DoesNotExist:
                raise ValueError(f"Error: form_settings_model with ID {fsID} does not exist.")
    # -----SET FORM VARIABLE IN RESPONSE TO DECIDING VARIABLES------------
            if existing:
                form = form20_form(request.POST, instance=database_form, form_settings=form_settings)
            else:
                form = form20_form(request.POST, form_settings=form_settings)
    # -----VALIDATE, CHECK FOR ISSUES, CREATE NOTIF, UPDATE SUBMISSION FORM------------
            exportVariables = (request, selector, facility, database_form, fsID)
            return redirect(*template_validate_save(form, form_variables, *exportVariables))
            # A_valid = form.is_valid()
            # if A_valid:
            #     A = form.save(commit=False)
            #     A.formSettings = form_variables['freq']
            #     A.save()

            #     B = []
            #     for x in form_variables['submitted_forms']:
            #         if x.week_start == last_monday:
            #             B.append((4, x.time_4, x.obser_4))
            #             B.append((3, x.time_3, x.obser_3))
            #             B.append((2, x.time_2, x.obser_2))
            #             B.append((1, x.time_1, x.obser_1))
            #             B.append((0, x.time_0, x.obser_0))

            #     for days in B:
            #         if days[0] == today_number:
            #             if days[1] and days[2]:
            #                 filled_in = True
            #             else:
            #                 filled_in = False

            #     if filled_in:
            #         createNotification(facility, request, fsID, form_variables['now'], 'submitted', False)
            #         updateSubmissionForm(fsID, True, todays_log.date_save)

            #         return redirect('IncompleteForms', facility)
    else:
        batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    return render(request, "shared/forms/daily/formI.html", {
        'fsID': fsID, 
        'picker': form_variables['picker'], 
        'facility': facility, 
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
        "search": search, 
        'supervisor': form_variables['supervisor'], 
        'todays_log': todays_log, 
        'empty': data, 
        'week': week, 
        'opened': opened, 
        'end_week': end_week, 
        'selector': selector, 
        'submit': submit, 
        'filled_in': filled_in, 
        'formName': form_variables['formName'], 
        "client": form_variables['client'], 
        'unlock': form_variables['unlock'], 
        'partial': partial_form
    })
