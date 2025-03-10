from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from datetime import datetime,date,timedelta
from ..models import Forms, user_profile_model, daily_battery_profile_model, form20_model, bat_info_model
from ..forms import formI_form
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import getFacSettingsInfo, checkIfFacilitySelected, issueForm_picker,updateSubmissionForm, setUnlockClientSupervisor, createNotification

lock = login_required(login_url='Login')


@lock
def formI(request, facility, fsID, selector):
    formName = 20
    freq = getFacSettingsInfo(fsID)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    now = datetime.now().date()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.all().filter(facility_name=facility)[0]
    week_start_dates = form20_model.objects.filter(facilityChoice__facility_name=facility).order_by('-week_start')
    profile = user_profile_model.objects.all()
    today = date.today()
    last_monday = today - timedelta(days=today.weekday())
    one_week = timedelta(days=4)
    end_week = last_monday + one_week
    today_number = today.weekday()
    opened = True
    submit = True
    filled_in = False
    partial_form = False
    week = ''
    picker = issueForm_picker(facility, selector, fsID)
    
    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector not in ('form', 'edit'):
            submit = False
            form_query = week_start_dates.filter(week_start=datetime.strptime(selector, "%Y-%m-%d").date())
            database_model = form_query[0] if form_query.exists() else print('no data found with this date')
            data = database_model
            existing = True
            search = True
            filled_in = True
        elif week_start_dates.exists():
            print('CHECK 3')
            database_model = week_start_dates[0]
            week = database_model.week_start
            # ------- check if todays data has been filled in or not
            home = []

            for x in form20_model.objects.all():
                if x.week_start == last_monday:
                    home.append((x.time_4, 4))
                    home.append((x.time_3, 3))
                    home.append((x.time_2, 2))
                    home.append((x.time_1, 1))
                    home.append((x.time_0, 0))
                    
            print(home)
            for days in home:
                if days[0]:
                    partial_form = True
                    if days[1] == today_number:
                        filled_in = True
            # -----check if today is a Weekday
            if today_number not in {5, 6}:
                print('CHECK 3.1')
                # --------FORM------------FORM----------FORM-------------
                if selector == 'form':
                    print(week)
                    print(last_monday)
                    if week == last_monday:
                        if filled_in or partial_form:
                            data = database_model
                            submit = False
                            existing = True
                # --------EDIT------------EDIT----------EDIT-------------
                elif selector == 'edit':
                    if week == last_monday:
                        filled_in = False
                        existing = True
            elif today_number == 5:
                print('CHECK 3.2')
                opened = False
                submit = False
                initial_data = {
                    'week_start': today,
                    'week_end': today + one_week
                }
                data = formI_form(initial=initial_data)
            else:
                print('CHECK 3.3')
                opened = False
                submit = False
                initial_data = {
                    'week_start': today - datetime.timedelta(days=1),
                    'week_end': today + one_week
                }
                data = formI_form(initial=initial_data)
                
        if existing:
            print('Check 2.1')
            initial_data = {
                'week_start': database_model.week_start,
                'week_end': database_model.week_end,
                'time_0': database_model.time_0,
                'time_1': database_model.time_1,
                'time_2': database_model.time_2,
                'time_3': database_model.time_3,
                'time_4': database_model.time_4,
                'obser_0': database_model.obser_0,
                'obser_1': database_model.obser_1,
                'obser_2': database_model.obser_2,
                'obser_3': database_model.obser_3,
                'obser_4': database_model.obser_4,
            }
            if filled_in:
                data = database_model
            else:
                print('Check 2.2')
                data = formI_form(initial=initial_data)
        else:
            initial_data = {
                'week_start': last_monday,
                'week_end': end_week
            }
            data = formI_form(initial=initial_data)

        if request.method == "POST":
            if existing:
                form = formI_form(request.POST, instance=database_model)
            else:
                form = formI_form(request.POST)

            A_valid = form.is_valid()
            if A_valid:
                A = form.save(commit=False)
                A.facilityChoice = options
                A.save()

                B = []
                for x in form20_model.objects.all():
                    if x.week_start == last_monday:
                        B.append((4, x.time_4, x.obser_4))
                        B.append((3, x.time_3, x.obser_3))
                        B.append((2, x.time_2, x.obser_2))
                        B.append((1, x.time_1, x.obser_1))
                        B.append((0, x.time_0, x.obser_0))

                for days in B:
                    if days[0] == today_number:
                        if days[1] and days[2]:
                            filled_in = True
                        else:
                            filled_in = False

                if filled_in:
                    createNotification(facility, request, fsID, now, 'submitted', False)
                    updateSubmissionForm(fsID, True, todays_log.date_save)

                    return redirect('IncompleteForms', facility)
    else:
        batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    return render(request, "shared/forms/daily/formI.html", {
        'fsID': fsID, 
        'picker': picker, 
        'facility': facility, 
        'notifs': notifs,
        'freq': freq,
        "search": search, 
        'supervisor': supervisor, 
         
        'todays_log': todays_log, 
        'empty': data, 
        'week': week, 
        'opened': opened, 
        'end_week': end_week, 
        'selector': selector, 
        'profile': profile, 
        'submit': submit, 
        'filled_in': filled_in, 
        'formName': formName, 
        "client": client, 
        'unlock': unlock, 
        'partial': partial_form
    })
