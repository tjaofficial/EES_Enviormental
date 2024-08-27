from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import issues_model, daily_battery_profile_model, formA1_model, formA1_readings_model, Forms, bat_info_model, facility_forms_model, form1_model, form1_readings_model
from ..forms import form1_form, form1_readings_form
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import updateSubmissionForm, setUnlockClientSupervisor, createNotification, issueForm_picker, checkIfFacilitySelected
import ast

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formA1(request, facility, fsID, selector):
    formName = 1
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    existing = False
    search = False
    now = datetime.datetime.now().date()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.all().filter(facility_name=facility)[0]
    org = form1_model.objects.all().order_by('-date')
    org2 = form1_readings_model.objects.all().order_by('-form')
    full_name = request.user.get_full_name()
    picker = issueForm_picker(facility, selector, fsID)
    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector != 'form':
            for x in org:
                if str(x.date) == str(selector):
                    database_model = x
            data = database_model
            for x in org2:
                if str(x.form.date) == str(selector):
                    database_model2 = x
            readings = database_model2
            existing = True
            search = True
        elif now == todays_log.date_save:
            if org.exists() and org2.exists():
                database_form = org[0]
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
                initial_data = {
                    'date': database_form.date,
                    'observer': database_form.observer,
                    'crew': database_form.crew,
                    'foreman': database_form.foreman,
                    'start': database_form.start,
                    'stop': database_form.stop,
                    'c1_no': database_form2.c1_no,
                    'c2_no': database_form2.c2_no,
                    'c3_no': database_form2.c3_no,
                    'c4_no': database_form2.c4_no,
                    'c5_no': database_form2.c5_no,
                    'c1_start': database_form2.c1_start,
                    'c2_start': database_form2.c2_start,
                    'c3_start': database_form2.c3_start,
                    'c4_start': database_form2.c4_start,
                    'c5_start': database_form2.c5_start,
                    'c1_stop': database_form2.c1_stop,
                    'c2_stop': database_form2.c2_stop,
                    'c3_stop': database_form2.c3_stop,
                    'c4_stop': database_form2.c4_stop,
                    'c5_stop': database_form2.c5_stop,
                    'c1_sec': database_form2.c1_sec,
                    'c2_sec': database_form2.c2_sec,
                    'c3_sec': database_form2.c3_sec,
                    'c4_sec': database_form2.c4_sec,
                    'c5_sec': database_form2.c5_sec,
                    'c1_comments': database_form2.c1_comments,
                    'c2_comments': database_form2.c2_comments,
                    'c3_comments': database_form2.c3_comments,
                    'c4_comments': database_form2.c4_comments,
                    'c5_comments': database_form2.c5_comments,
                    'larry_car': database_form2.larry_car,
                    'comments': database_form2.comments,
                    'total_seconds': database_form2.total_seconds,
                }
                readings = form1_readings_form(initial=initial_data)
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name,
                    'crew': todays_log.crew,
                    'foreman': todays_log.foreman,
                    'facility_name': facility,
                }
                readings = form1_readings_form()

            data = form1_form(initial=initial_data)
        if request.method == "POST":
            if existing:
                form = form1_form(request.POST, instance=database_form)
                reads = form1_readings_form(request.POST, instance=database_form2)
            else:
                form = form1_form(request.POST)
                reads = form1_readings_form(request.POST)

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
                if B.total_seconds >= 55:
                    issueFound = True
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
                    return redirect('issues_view', facility, fsID, str(database_form.date), issue_page)
                createNotification(facility, request.user, formName, now, 'submitted')        
                updateSubmissionForm(fsID, True, todays_log.date_save)
                return redirect('IncompleteForms', facility)
    else:
        batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)

    return render(request, "shared/forms/daily/formA1.html", {
        'facility': facility,
        'notifs': notifs,
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


    # hourNum = int(str(time)[0:2])
    # minNum = str(time)[3:5]
    # timeLabel = 'AM'
    # if hourNum > 12:
    #     newHourNum = str(hourNum - 12)
    #     timeLabel = 'PM'
    #     newTime = newHourNum + ':' + minNum + ' ' + timeLabel
    # elif hourNum == 00:
    #     newHourNum = '12'
    #     newTime = newHourNum + ':' + minNum + ' ' + timeLabel
    # else:
    #     newTime = str(hourNum) + ':' + minNum + ' ' + timeLabel
    # return newTime