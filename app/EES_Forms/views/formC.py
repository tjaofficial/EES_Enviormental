from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
import datetime
from ..models import issues_model, user_profile_model, daily_battery_profile_model, form7_model, form7_readings_model, Forms, bat_info_model
from ..forms import SubFormC1, FormCReadForm
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import getFacSettingsInfo, checkIfFacilitySelected, issueForm_picker,updateSubmissionForm, setUnlockClientSupervisor, createNotification
import json

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formC(request, facility, fsID, selector):
    formName = 7
    freq = getFacSettingsInfo(fsID)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    now = datetime.datetime.now().date()
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.all().filter(facility_name=facility)[0]
    org = form7_model.objects.all().order_by('-date')
    #org2 = form7_readings_model.objects.all().order_by('-form')
    full_name = request.user.get_full_name()
    picker = issueForm_picker(facility, selector, fsID)
    areaCount = int(freq.settings['settings']['number_of_areas'])
    print(selector)
    if profile.exists():
        same_user = user_profile_model.objects.filter(user__exact=request.user.id)
        if same_user:
            cert_date = request.user.user_profile_model.cert_date
        else:
            return redirect('IncompleteForms', facility)
    else:
        return redirect('IncompleteForms', facility)

    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector != 'form':
            initial_data = ''
            readsData = {}
            for x in org:
                if str(x.date) == str(selector):
                    database_model = x
            form = database_model
            existing = True
            search = True
        # ------check if database is empty----------
        elif org.exists():
            database_form = org[0]
            # -------check if there is a daily battery profile
            if now == todays_log.date_save:
                if todays_log.date_save == database_form.date:
                    existing = True
        if search:
            database_form = ''
        else:
            if existing:
                print('check 1')
                initial_data = {
                    'date': database_form.date,
                    'observer': database_form.observer,
                    'cert_date': database_form.cert_date,
                    'comments': database_form.comments
                }
                initial_areas = {}
                readsData = {}
                for x in range(1, areaCount+1):
                    x = str(x)
                    if x == "1":
                        area = database_form.area_json_1
                    elif x == "2":
                        area = database_form.area_json_2
                    elif x == "3":
                        area = database_form.area_json_3
                    elif x == "4":
                        area = database_form.area_json_4
                    intital_adding = {
                        x: {
                            'name': area['selection'],
                            'startTime': area['start_time'],
                            'stopTime': area['stop_time'],
                            'average': area['average'],
                        }
                    }
                    print(intital_adding)
                    initial_data_dict = {
                        x: [
                            area['readings']['1'], 
                            area['readings']['2'], 
                            area['readings']['3'], 
                            area['readings']['3'], 
                            area['readings']['4'], 
                            area['readings']['5'], 
                            area['readings']['6'],
                            area['readings']['7'],
                            area['readings']['8'],
                            area['readings']['9'],
                            area['readings']['10'],
                            area['readings']['11']
                        ]
                    }
                    initial_areas.update(intital_adding)
                    readsData.update(initial_data_dict)
                print(initial_areas)
            else:
                print('check 2')
                initial_data = {
                    'date': now,
                    'observer': full_name,
                    'cert_date': cert_date,
                }
                readsData = {}
                intital_adding = {}
            form = SubFormC1(initial=initial_data)
        if request.method == "POST":
            copyRequest = request.POST.copy()
            for x in range(1,areaCount+1):
                x = str(x)
                areaSetup= {
                    "selection": request.POST['areaName' + x],
                    "start_time": request.POST['areaStartTime' + x],
                    "stop_time": request.POST['areaStopTime' + x],
                    "readings": {
                        "1": int(request.POST['area' + x + 'Read0']),
                        "2": int(request.POST['area' + x + 'Read1']),
                        "3": int(request.POST['area' + x + 'Read2']),
                        "4": int(request.POST['area' + x + 'Read3']),
                        "5": int(request.POST['area' + x + 'Read4']),
                        "6": int(request.POST['area' + x + 'Read5']),
                        "7": int(request.POST['area' + x + 'Read6']),
                        "8": int(request.POST['area' + x + 'Read7']),
                        "9": int(request.POST['area' + x + 'Read8']),
                        "10": int(request.POST['area' + x + 'Read9']),
                        "11": int(request.POST['area' + x + 'Read10']),
                        "12": int(request.POST['area' + x + 'Read11']),
                    },
                    "average": int(request.POST['areaAverage' + x])
                }
                areaSetup = json.loads(json.dumps(areaSetup))
                copyRequest['area_json_' + x] = areaSetup
            print(copyRequest)

            if existing:
                CData = SubFormC1(copyRequest, instance=database_form)
            else:
                CData = SubFormC1(copyRequest)

            A_valid = CData.is_valid()

            if A_valid:
                A = CData.save(commit=False)
                A.facilityChoice = options
                for x in range(1,areaCount+1):
                    x = str(x)
                    areaJson = copyRequest['area_json_' + x]
                    if x == "1":
                        A.area_json_1 = areaJson
                    elif x == "2":
                        A.area_json_2 = areaJson
                    elif x == "3":
                        A.area_json_3 = areaJson
                    elif x == "4":
                        A.area_json_4 = areaJson
                A.save()

                issueFound = False
                if not existing:
                    database_form = A
                finder = issues_model.objects.filter(date=A.date, form=fsID).exists()
                print(A.area_json_1)
                if A.area_json_1['average'] > 5 or A.area_json_2['average'] > 5 or A.comments not in {'-', 'n/a', 'N/A'}:
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
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    return render(request, "shared/forms/daily/formC.html", {
        'fsID': fsID, 
        'picker': picker, 
        "search": search, 
        "client": client, 
        'unlock': unlock, 
        'supervisor': supervisor, 
        'form': form,
        "back": back, 
        'profile': profile, 
        'selector': selector, 
        'formName': formName, 
        'facility': facility,
        'notifs': notifs,
        'freq': freq,
        'existing': existing,
        'initial_data': initial_data,
        'readsData': readsData,
        #'initial_areas': initial_areas
    })
