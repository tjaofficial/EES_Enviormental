from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from datetime import datetime
from ..models import form27_model
from ..forms import quarterly_trucks_form
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import createNotification, get_initial_data, updateSubmissionForm
from ..initial_form_variables import initiate_form_variables, existing_or_new_form

lock = login_required(login_url='Login')

@lock
def form27(request, facility, fsID, selector):
    form_variables = initiate_form_variables(fsID, request.user, facility, selector)
    def what_quarter(input):
        if input.month in {1,2,3}:
            return 1
        if input.month in {4,5,6}:
            return 2
        if input.month in {7,8,9}:
            return 3
        if input.month in {10,11,12}:
            return 4
    
    if form_variables['daily_prof'].exists():
        todays_log = form_variables['daily_prof'][0]
        data, existing, search = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request)
        if selector != 'form':
            form_query = form_variables['submitted_forms'].filter(date=datetime.strptime(selector, "%Y-%m-%d").date())
            database_model = form_query[0] if form_query.exists() else print('no data found with this date')
            data = database_model
            existing = True
            search = True
            unlock = True
        elif form_variables['now'] == todays_log.date_save:
            if form_variables['submitted_forms'].exists():
                database_form = form_variables['submitted_forms'][0]
                if what_quarter(todays_log.date_save) == what_quarter(database_form.date) and todays_log.date_save.year == database_form.date.year:
                    existing = True
        else:
            batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
            return redirect('daily_battery_profile', facility, "login", batt_prof_date)
        
        if search:
            database_form = ''
        else:
            if existing:
                initial_data = get_initial_data(form27_model, database_form)
            else:
                initial_data = {
                    'quarter': what_quarter(form_variables['now']),
                    'date': form_variables['now'],
                }
            data = quarterly_trucks_form(initial=initial_data)
            
        if request.method == "POST":
            if existing:
                data = quarterly_trucks_form(request.POST, instance=database_form)
            else:
                data = quarterly_trucks_form(request.POST)
            A_valid = data.is_valid()
            print(data.errors)
            if A_valid:
                A = data.save(commit=False)
                A.formSettings = form_variables['freq']
                A.save()
                
                filled_out = True
                for items in A.whatever().values():
                    if items is None or items == '':
                        filled_out = False  # -change this back to false
                        break
                if filled_out:
                    ## if issue found find it here
                    createNotification(facility, request, fsID, form_variables['now'], 'submitted', False)
                    updateSubmissionForm(fsID, True, todays_log.date_save)
                return redirect('IncompleteForms', facility)
    else:
        batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
            
    return render(request, "shared/forms/quarterly/quarterly_trucks.html", {
        'picker': form_variables['picker'], 
        'facility': facility, 
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
        "search": search, 
        "client": form_variables['client'], 
        'unlock': unlock, 
        'supervisor': form_variables['supervisor'], 
        'formName': form_variables['formName'], 
        'selector': selector, 
        'data': data,
        'fsID': fsID,
    })