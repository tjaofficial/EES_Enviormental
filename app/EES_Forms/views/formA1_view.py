from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from datetime import datetime
from ..models import issues_model, daily_battery_profile_model, form1_model, form1_readings_model, Forms, bat_info_model, facility_forms_model, form1_model, form1_readings_model
from ..forms import formA1_form, formA1_readings_form
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import updateSubmissionForm, setUnlockClientSupervisor, createNotification, issueForm_picker, checkIfFacilitySelected, getFacSettingsInfo, get_initial_data
import ast
from django.db.models import Field # type: ignore
from django.http import JsonResponse # type: ignore
from django.core.exceptions import ObjectDoesNotExist # type: ignore

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formA1(request, facility, fsID, selector):
    formName = 1
    notifs = checkIfFacilitySelected(request.user, facility)
    freq = getFacSettingsInfo(fsID)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    now = datetime.now().date()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.filter(facility_name=facility)[0]
    submitted_forms = form1_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
    org2 = form1_readings_model.objects.all().order_by('-form')
    full_name = request.user.get_full_name()
    picker = issueForm_picker(facility, selector, fsID)
    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector != 'form':
            form_query = submitted_forms.filter(date=datetime.strptime(selector, "%Y-%m-%d").date())
            database_model = form_query[0] if form_query.exists() else print('no data found with this date')
            data = database_model

            for x in org2:
                if str(x.form.date) == str(selector):
                    database_model2 = x
            readings = database_model2
            
            existing = True
            search = True
        elif now == todays_log.date_save:
            if submitted_forms.exists() and org2.exists():
                database_form = submitted_forms[0]
                database_form2 = org2[0]
                if todays_log.date_save == database_form.date:
                    existing = True
        else:
            batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
            return redirect('daily_battery_profile', facility, "login", batt_prof_date)
        
        if search:
            database_form = ''
        else:
            if existing:
                initial_data = get_initial_data(form1_model, database_form)
                readings = formA1_readings_form(initial=initial_data)
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name,
                    'crew': todays_log.crew,
                    'foreman': todays_log.foreman,
                    'facility_name': facility,
                }
                readings = formA1_readings_form()

            data = formA1_form(initial=initial_data)
        if request.method == "POST":
            if existing:
                form = formA1_form(request.POST, instance=database_form)
                reads = formA1_readings_form(request.POST, instance=database_form2)
            else:
                form = formA1_form(request.POST)
                reads = formA1_readings_form(request.POST)

            A_valid = form.is_valid()
            B_valid = reads.is_valid()
            finalFacility = options
            
            if A_valid and B_valid:
                A = form.save(commit=False)
                B = reads.save(commit=False)
                B.form = A
                A.facilityChoice = finalFacility
                A.save()
                B.save()
                
                if not existing:
                    database_form = A
                fsID = str(fsID)
                finder = issues_model.objects.filter(date=A.date, form=fsID).exists()
            #     if B.comments not in {'-', 'n/a', 'N/A'}:
            #         issue_page = '../../issues_view/A-1/' + str(database_form.date) + '/form'

            #         return redirect (issue_page)
                sec = {B.c1_sec, B.c2_sec, B.c3_sec, B.c4_sec, B.c5_sec}
                issueFound = False
                compliance = False
                if B.total_seconds >= 55:
                    issueFound = True
                    compliance = True
                else:
                    for x in sec:
                        if 10 <= x:
                            issueFound = True
                if issueFound:
                    if finder:
                        if selector == 'form':
                            issue_page = 'resubmit'
                        else:
                            issue_page = 'issue'
                    else:
                        issue_page = 'form'
                    
                    if compliance:
                        issue_page = issue_page + "-c"
                        
                    return redirect('issues_view', facility, fsID, str(database_form.date), issue_page)
                createNotification(facility, request, fsID, now, 'submitted', False)        
                updateSubmissionForm(fsID, True, todays_log.date_save)
                return redirect('IncompleteForms', facility)
    else:
        batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)

    return render(request, "shared/forms/daily/formA1.html", {
        'facility': facility,
        'notifs': notifs,
        'freq': freq,
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock, 
        'options': options, 
        "search": search, 
        "back": back, 
        'todays_log': todays_log, 
        'data': data, 
        'readings': readings, 
        'formName': formName, 
        'selector': selector,
        'picker': picker,
        'fsID': fsID
    })

def inop_check_form_1(request):  # Add request parameter
    today = datetime.now().date()
    try:
        dailyBatProf = daily_battery_profile_model.objects.get(date_save=today)

        # If `inop_numbs` is stored as a string like '44,45,54,62', split it into a list
        response_data = dailyBatProf.inop_numbs[1:-1].replace(" ", "").split(",") if dailyBatProf.inop_numbs != "[]" else []
    except ObjectDoesNotExist:
        response_data = []

    return JsonResponse(response_data, safe=False)

