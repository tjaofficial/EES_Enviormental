from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from datetime import datetime, date
from ..models import Forms, issues_model, user_profile_model, daily_battery_profile_model, form25_model, bat_info_model
from ..forms import formP_form
from ..utils import get_initial_data, getFacSettingsInfo, checkIfFacilitySelected, issueForm_picker, updateSubmissionForm, setUnlockClientSupervisor, createNotification
import calendar
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR

lock = login_required(login_url='Login')



@lock
def formP(request, facility, fsID, selector, weekend_day):
    formName = 25
    freq = getFacSettingsInfo(fsID)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    now = datetime.now().date()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.all().filter(facility_name=facility)[0]
    submitted_forms = form25_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
    profile = user_profile_model.objects.all()
    today = date.today()
    full_name = request.user.get_full_name()
    month_name = calendar.month_name[today.month]
    picker = issueForm_picker(facility, selector, fsID)

    if weekend_day == 'saturday':
        ss_filler = 5
    elif weekend_day == 'sunday':
        ss_filler = 6
    else:
        ss_filler = ''

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
                if database_form.date == today:
                    existing = True
        else:
            batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
            return redirect('daily_battery_profile', facility, "login", batt_prof_date)
        
        if search:
            database_form = ''
        else:
            if existing:
                initial_data = get_initial_data(form25_model, database_form)
            else:
                initial_data = {
                    'date': today,
                    'observer': full_name,
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
                A.facilityChoice = options
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
                createNotification(facility, request, fsID, now, 'submitted', False)
                updateSubmissionForm(fsID, True, todays_log.date_save)
                return redirect('IncompleteForms', facility)
    else:
        batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        return redirect('daily_battery_profile', 'login', batt_prof_date)
    return render(request, "shared/forms/weekly/formP.html", {
        'fsID': fsID, 
        'picker': picker, 
        'facility': facility, 
        'notifs': notifs,
        'freq': freq,
        'data': data, 
        "search": search, 
        "client": client, 
        'unlock': unlock, 
        'supervisor': supervisor, 
        'formName': formName, 
        'selector': selector, 
        'profile': profile, 
        'weekend_day': weekend_day
    })
