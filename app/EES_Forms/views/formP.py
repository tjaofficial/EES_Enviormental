from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
import datetime
from ..models import Forms, issues_model, user_profile_model, daily_battery_profile_model, form25_model, bat_info_model
from ..forms import formP_form
from ..utils import getFacSettingsInfo, checkIfFacilitySelected, issueForm_picker, updateSubmissionForm, setUnlockClientSupervisor, createNotification
import calendar
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formP(request, facility, fsID, selector, weekend_day):
    formName = 25
    freq = getFacSettingsInfo(fsID)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    now = datetime.datetime.now().date()
    profile = user_profile_model.objects.all()
    today = datetime.date.today()
    full_name = request.user.get_full_name()
    options = bat_info_model.objects.all().filter(facility_name=facility)[0]
    month_name = calendar.month_name[today.month]
    picker = issueForm_picker(facility, selector, fsID)
    org = form25_model.objects.all().order_by('-date')

    if weekend_day == 'saturday':
        ss_filler = 5
    elif weekend_day == 'sunday':
        ss_filler = 6
    else:
        ss_filler = ''

    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector != 'form':
            for x in org:
                if str(x.date) == str(selector):
                    database_model = x
            data = database_model
            existing = True
            search = True
        elif org.exists():
            database_form = org[0]
            if database_form.date == today:
                existing = True
        if search:
            database_form = ''
        else:
            if existing:
                initial_data = {
                    'observer': database_form.observer,
                    'month': database_form.month,
                    'date': database_form.date,
                    'weekend_day': database_form.weekend_day,
                    'Q_1': database_form.Q_1,
                    'Q_2': database_form.Q_2,
                    'Q_3': database_form.Q_3,
                    'Q_4': database_form.Q_4,
                    'Q_5': database_form.Q_5,
                    'Q_6': database_form.Q_6,
                    'Q_7': database_form.Q_7,
                    'Q_8': database_form.Q_8,
                    'Q_9': database_form.Q_9,
                    'comments': database_form.comments,
                    'actions_taken': database_form.actions_taken,
                }
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
                finder = issues_model.objects.filter(date=A.date, form=fsID).exists()
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
