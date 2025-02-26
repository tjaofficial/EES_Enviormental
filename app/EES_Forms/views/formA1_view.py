from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from datetime import datetime
from ..models import form_settings_model, issues_model, daily_battery_profile_model, form1_model, form1_readings_model, Forms, bat_info_model, facility_forms_model, form1_model, form1_readings_model
from ..forms import formA1_form
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import form1_json_build, parse_form1_oven_dict, updateSubmissionForm, setUnlockClientSupervisor, createNotification, issueForm_picker, checkIfFacilitySelected, getFacSettingsInfo, get_initial_data
import ast
from django.db.models import Field # type: ignore
from django.http import JsonResponse # type: ignore
from django.core.exceptions import ObjectDoesNotExist # type: ignore

lock = login_required(login_url='Login')

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
    full_name = request.user.get_full_name()
    picker = issueForm_picker(facility, selector, fsID)
    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector != 'form':
            form_query = submitted_forms.filter(date=datetime.strptime(selector, "%Y-%m-%d").date())
            database_model = form_query[0] if form_query.exists() else print('no data found with this date')
            data = database_model
            existing = True
            search = True
        elif now == todays_log.date_save:
            if submitted_forms.exists():
                database_form = submitted_forms[0]
                if todays_log.date_save == database_form.date:
                    existing = True
        else:
            batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
            return redirect('daily_battery_profile', facility, "login", batt_prof_date)
        
        if search:
            database_form = ''
        else:
            if existing:
                unparsedData = get_initial_data(form1_model, database_form)
                ovens_data = parse_form1_oven_dict(unparsedData['ovens_data'])
                initial_data = unparsedData | ovens_data
                print(ovens_data)
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name,
                    'crew': todays_log.crew,
                    'foreman': todays_log.foreman,
                    'facility_name': facility,
                    'formSettings': form_settings_model.objects.get(id=int(fsID))
                }
            data = formA1_form(initial=initial_data)

        if request.method == "POST":
            dataCopy = request.POST.copy()
            dataCopy['ovens_data'] = form1_json_build(request.POST)
            if existing:
                form = formA1_form(dataCopy, instance=database_form)
            else:
                form = formA1_form(dataCopy)
            A_valid = form.is_valid()
            finalFacility = options
            print(form.errors)
            if A_valid:
                A = form.save(commit=False)
                A.formSettings = form_settings_model.objects.get(id=int(fsID))
                A.facilityChoice = finalFacility
                A.save()
                
                if not existing:
                    database_form = A
                fsID = str(fsID)
                finder = issues_model.objects.filter(date=A.date, form=fsID).exists()
                if A.ovens_data['comments'] not in {'-', 'n/a', 'N/A'}:
                    issue_page = '../../issues_view/A-1/' + str(database_form.date) + '/form'
                    return redirect (issue_page)
                sec = {int(A.ovens_data['charge_1']['c1_sec']), int(A.ovens_data['charge_2']['c2_sec']), int(A.ovens_data['charge_3']['c3_sec']), int(A.ovens_data['charge_4']['c4_sec']), int(A.ovens_data['charge_5']['c5_sec'])}
                issueFound = False
                compliance = False
                if int(A.ovens_data['total_seconds']) >= 55:
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
        'todays_log': todays_log, 
        'data': data, 
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

