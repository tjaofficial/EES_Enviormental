from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from datetime import datetime
from ..models import issues_model, form25_model
from ..forms import formP_form
from ..utils import get_initial_data, updateSubmissionForm, createNotification
import calendar
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..initial_form_variables import initiate_form_variables, existing_or_new_form

lock = login_required(login_url='Login')

@lock
def form25(request, facility, fsID, selector, weekend_day):
    form_variables = initiate_form_variables(fsID, request.user, facility, selector)
    month_name = calendar.month_name[form_variables['now'].month]
    if weekend_day == 'saturday':
        ss_filler = 5
    elif weekend_day == 'sunday':
        ss_filler = 6
    else:
        ss_filler = ''

    if form_variables['daily_prof'].exists():
        todays_log = form_variables['daily_prof'][0]
        data, existing, search = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request)
        if search:
            database_form = ''
        else:
            if existing:
                initial_data = get_initial_data(form25_model, database_form)
            else:
                initial_data = {
                    'date': form_variables['now'],
                    'observer': form_variables['full_name'],
                    'month': month_name,
                    'weekend_day': ss_filler,
                }
            data = formP_form(initial=initial_data)

        if request.method == 'POST':
            if existing:
                data = formP_form(request.POST, instance=database_form)
            else:
                data = formP_form(request.POST)
            A_valid = data.is_valid()
            if A_valid:
                A = data.save(commit=False)
                A.formSettings = form_variables['freq']
                A.save()

                issueFound = False
                if not existing:
                    database_form = A
                finder = issues_model.objects.filter(date=A.date, formChoice=A.formSettings).exists()
                if 'Yes' in {A.Q_2,A.Q_3,A.Q_4,A.Q_5,A.Q_6,A.Q_7,A.Q_8,A.Q_9}:
                    issueFound = True
                if issueFound:
                    if finder:
                        if selector == 'form':
                            issue_page = 'resubmit'
                        else:
                            issue_page = 'issue'
                    else:
                        issue_page = 'form'
                    return redirect('issues_view', facility, fsID, str(database_form.date), issue_page)
                createNotification(facility, request, fsID, form_variables['now'], 'submitted', False)
                updateSubmissionForm(fsID, True, todays_log.date_save)
                return redirect('IncompleteForms', facility)
    else:
        batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
        return redirect('daily_battery_profile', 'login', batt_prof_date)
    return render(request, "shared/forms/weekly/formP.html", {
        'fsID': fsID, 
        'picker': form_variables['picker'], 
        'facility': facility, 
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
        'data': data, 
        "search": search, 
        "client": form_variables['client'], 
        'unlock': form_variables['unlock'], 
        'supervisor': form_variables['supervisor'], 
        'formName': form_variables['formName'], 
        'selector': selector, 
        'weekend_day': weekend_day
    })
