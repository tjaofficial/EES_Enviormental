from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from datetime import datetime,date
from ..models import Forms, issues_model, user_profile_model, daily_battery_profile_model, form22_model, form22_readings_model, bat_info_model, paved_roads, unpaved_roads, parking_lots
from ..forms import formM_form, formM_readings_form
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import get_initial_data, getFacSettingsInfo, checkIfFacilitySelected, issueForm_picker,updateSubmissionForm, setUnlockClientSupervisor, createNotification

lock = login_required(login_url='Login')


def showName(code):
    for pair in paved_roads:
        if pair[0] == code:
            return pair[1]

@lock
def formM(request, facility, fsID, selector):
    formName = 22
    freq = getFacSettingsInfo(fsID)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    now = datetime.now().date()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.all().filter(facility_name=facility)[0]
    submitted_forms = form22_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
    THEmonth = False
    profile = user_profile_model.objects.filter(user__exact=request.user.id)
    today = date.today()
    today_number = today.weekday()
    org2 = form22_readings_model.objects.all().order_by('-form')
    full_name = request.user.get_full_name()
    picker = issueForm_picker(facility, selector, fsID)
    print(freq)

    if profile.exists():
        cert_date = request.user.user_profile_model.cert_date
    else:
        return redirect('IncompleteForms', facility)
    
    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector != 'form':
            form_query = submitted_forms.filter(date=datetime.strptime(selector, "%Y-%m-%d").date())
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
        elif now == todays_log.date_save:
            if submitted_forms.exists() or org2.exists():
                database_form = submitted_forms[0]
                database_form2 = org2[0]
                if selector == 'form':
                    if today_number in {0, 1, 2, 3, 4}:
                        if todays_log.date_save == database_form.date:
                            existing = True
        else:
            batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
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
                    'date': now,
                    'observer': full_name,
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
                A.facilityChoice = options
                B.form = A
                A.save()
                B.save()

                issueFound = False
                if not existing:
                    database_form = A
                finder = issues_model.objects.filter(date=A.date, form=fsID).exists()
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
                createNotification(facility, request, fsID, now, 'submitted', False)
                updateSubmissionForm(fsID, True, todays_log.date_save)
                #updateSubmissionForm(facility, 23, True, todays_log.date_save)
                return redirect('IncompleteForms', facility)
    else:
        batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    return render(request, "shared/forms/daily/formM.html", {
        'fsID': fsID, 
        'picker': picker, 
        "existing": existing, 
        'facility': facility, 
        'notifs': notifs,
        'freq': freq,
        "client": client, 
        'unlock': unlock, 
        'supervisor': supervisor, 
        'now': todays_log, 
        'form': form, 
        'selector': selector, 
        'profile': profile, 
        'read': form2, 
        'formName': formName, 
        'search': search, 
        'THEmonth': THEmonth, 
        'paved_roads': paved_roads, 
        'unpaved_roads': unpaved_roads, 
        'parking_lots': parking_lots,
    })
