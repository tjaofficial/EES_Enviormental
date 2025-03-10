from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from datetime import datetime
from ..models import issues_model, user_profile_model, daily_battery_profile_model, form7_model, Forms, bat_info_model
from ..forms import SubFormC1
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import getFacSettingsInfo, checkIfFacilitySelected, issueForm_picker,updateSubmissionForm, setUnlockClientSupervisor, createNotification
import json

lock = login_required(login_url='Login')



@lock
def formC(request, facility, fsID, selector):
    formName = 7
    freq = getFacSettingsInfo(fsID)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    now = datetime.now().date()
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.all().filter(facility_name=facility)[0]
    submitted_forms = form7_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
    full_name = request.user.get_full_name()
    picker = issueForm_picker(facility, selector, fsID)
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
                    data = database_form
        else:
            batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
            return redirect('daily_battery_profile', facility, "login", batt_prof_date)
        
        areaFilled1 = []
        if existing:
            initial_areas = {}
            readsData = {}
            dataBaseInputList = data._meta.get_fields()
            for inputData in dataBaseInputList:
                if inputData.name[:-1] == 'area_json_':
                    if getattr(data, inputData.name) != {}:
                        areaFilled1.append(inputData.name[10:])
            initial_data = {
                'date': data.date.strftime("%Y-%m-%d"),
                'observer': data.observer,
                'cert_date': data.cert_date.strftime("%Y-%m-%d"),
                'comments': data.comments
            }
            for x in areaFilled1:
                x = str(x)
                if x == "1":
                    area = data.area_json_1
                elif x == "2":
                    area = data.area_json_2
                elif x == "3":
                    area = data.area_json_3
                elif x == "4":
                    area = data.area_json_4
                intital_adding = {
                    x: {
                        'name': area['selection'],
                        'startTime': datetime.strptime(area['start_time'], "%H:%M").strftime("%H:%M"),
                        'stopTime': datetime.strptime(area['stop_time'], "%H:%M").strftime("%H:%M"),
                        'average': area['average'],
                    }
                }
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
            allData = {"main": initial_data, "primary": initial_areas, "readings": readsData}
            print(allData["readings"])
        else:
            initial_data = {
                'date': now.strftime("%Y-%m-%d"),
                'observer': full_name,
                'cert_date': cert_date.strftime("%Y-%m-%d"),
            }
            areaFilled1 += ["1","2","3","4"]
            allData = {"main": initial_data, "primary": {}, "readings": {}}
        
        print(existing)
        if request.method == "POST":
            copyRequest = request.POST.copy()
            areaFilled = []
            for formKeys in request.POST.keys():
                if formKeys[:8] == 'areaName':
                    if request.POST["areaStartTime" + formKeys[8:]] != '':
                        areaFilled.append(formKeys[8:])
            for x in areaFilled:
                x = str(x)
                areaSetup= {
                    "selection": request.POST[f"areaName{x}"],
                    "start_time": request.POST[f"areaStartTime{x}"],
                    "stop_time": request.POST[f"areaStopTime{x}"],
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

            if existing:
                CData = SubFormC1(copyRequest, instance=data)
            else:
                CData = SubFormC1(copyRequest)

            A_valid = CData.is_valid()

            if A_valid:
                A = CData.save(commit=False)
                A.facilityChoice = options
                for x in areaFilled:
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
                    data = A
                finder = issues_model.objects.filter(date=A.date, formChoice=A.formSettings).exists()
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
                    return redirect('issues_view', facility, fsID, str(data.date), issue_page)
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
         
        'profile': profile, 
        'selector': selector, 
        'formName': formName, 
        'facility': facility,
        'notifs': notifs,
        'freq': freq,
        'existing': existing,
        'allData': allData,
        "areaFilled1": areaFilled1,
    })
