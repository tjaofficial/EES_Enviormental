from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from ..models import issues_model, form22_model, form22_readings_model, paved_roads, unpaved_roads, parking_lots
from ..forms import formM_form, formM_readings_form
from ..utils import fix_data, get_initial_data,updateSubmissionForm, createNotification
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
from datetime import datetime,date

lock = login_required(login_url='Login')

def showName(code):
    for pair in paved_roads:
        if pair[0] == code:
            return pair[1]

@lock
def form22(request, facility, fsID, selector):
    fix_data(fsID)
    # -----SET MAIN VARIABLES------------
    form_variables = initiate_form_variables(fsID, request.user, facility, selector)
    cert_date = request.user.user_profile.cert_date if request.user.user_profile else False
    THEmonth = False
    today_number = form_variables['now'].weekday()
    org2 = form22_readings_model.objects.all().order_by('-form')
    
    if form_variables['daily_prof'].exists():
        todays_log = form_variables['daily_prof'][0]
        # -----SET DECIDING VARIABLES------------
        more_form_variables = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request, fsID) 
        if isinstance(more_form_variables, HttpResponseRedirect):
            return more_form_variables
        else:
            data, existing, search, database_form = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request, fsID)
        if selector != 'form':
            form_query = form_variables['submitted_forms'].filter(date=datetime.strptime(selector, "%Y-%m-%d").date())
            database_model = form_query[0] if form_query.exists() else print('no data found with this date')
            form = database_model

            for x in org2:
                if str(x.form) == str(selector):
                    database_model2 = x
                else:
                    print('Error - EES_00001')
            form2 = database_model2

            existing = True
            search = True
        elif form_variables['now'] == todays_log.date_save:
            if form_variables['submitted_forms'].exists() or org2.exists():
                database_form = form_variables['submitted_forms'][0]
                database_form2 = org2[0]
                if selector == 'form':
                    if today_number in {0, 1, 2, 3, 4}:
                        if todays_log.date_save == database_form.date:
                            existing = True
        else:
            batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
            return redirect('daily_battery_profile', facility, "login", batt_prof_date)
        
        if search:
            database_form = ''
            THEmonth = form.date.month
        else:
            if existing:
                initial_data = get_initial_data(form22_model, database_form)
                form2 = formM_readings_form(initial=initial_data)
                print(initial_data)
            else:
                initial_data = {
                    'date': form_variables['now'],
                    'observer': form_variables['full_name'],
                    'cert_date': cert_date
                }
                form2 = formM_readings_form()

            form = formM_form(initial=initial_data)
        if request.method == "POST":
            if existing:
                form = formM_form(request.POST, instance=database_form)
                reads = formM_readings_form(request.POST, instance=database_form2)
            else:
                form = formM_form(request.POST)
                reads = formM_readings_form(request.POST)

            A_valid = form.is_valid()
            B_valid = reads.is_valid()
            print(form.errors)
            print(reads.errors)
            if A_valid and B_valid:
                A = form.save(commit=False)
                B = reads.save(commit=False)
                A.formSettings = form_variables['freq']
                B.form = A
                A.save()
                B.save()

                issueFound = False
                if not existing:
                    database_form = A
                finder = issues_model.objects.filter(date=A.date, formChoice=A.formSettings).exists()
                if int(B.pav_total) > 5 or int(B.unp_total) > 5 or int(B.par_total) > 5 or A.comments not in {'-', 'n/a', 'N/A'}:
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
                #updateSubmissionForm(facility, 23, True, todays_log.date_save)
                return redirect('IncompleteForms', facility)
    else:
        batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    return render(request, "shared/forms/daily/formM.html", {
        'fsID': fsID, 
        'picker': form_variables['picker'], 
        "existing": existing, 
        'facility': facility, 
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
        "client": form_variables['client'], 
        'unlock': form_variables['unlock'], 
        'supervisor': form_variables['supervisor'], 
        'now': todays_log, 
        'form': form, 
        'selector': selector,
        'read': form2, 
        'formName': form_variables['formName'], 
        'search': search, 
        'THEmonth': THEmonth, 
        'paved_roads': paved_roads, 
        'unpaved_roads': unpaved_roads, 
        'parking_lots': parking_lots,
    })
