from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from ..forms import spill_kits_form, spill_kit_inventory_form
from ..models import daily_battery_profile_model, form29_model, bat_info_model, form26_model
from datetime import datetime, date
import calendar
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
import json
import ast
from ..utils import get_initial_data, getFacSettingsInfo, checkIfFacilitySelected, stringToDate, setUnlockClientSupervisor, updateSubmissionForm

lock = login_required(login_url='Login')

@lock
def spill_kits(request, facility, fsID, selector):
    formName = "29"
    freq = getFacSettingsInfo(fsID)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    now = datetime.now().date()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.all().filter(facility_name=facility)[0]
    submitted_forms = form29_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
    sk_form = spill_kits_form()
    full_name = request.user.get_full_name()
    today = date.today()
    month_name = calendar.month_name[today.month]
    
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
                datetime_object = datetime.strptime(database_form.month, "%B")
                month_number = datetime_object.month
                if now.month == month_number:
                    existing = True
        else:
            batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
            return redirect('daily_battery_profile', facility, "login", batt_prof_date)

        iFormList = {}
        if search:
            print('CHECK 1.2')
            database_form = ''
            month = database_model.month
            inventoryModel = form26_model.objects.filter(date__month=database_model.date.month)
            for subForm in inventoryModel:
                iFormList[subForm.skID] = [subForm.skID,stringToDate(subForm.date)]
            iFormList = json.dumps(iFormList)
        else:
            inventoryModel = form26_model.objects.filter(date__month=now.month)
            if inventoryModel.exists():
                for subForm in inventoryModel:
                    iFormList[subForm.skID] = [subForm.skID,stringToDate(subForm.date)]
                iFormList = json.dumps(iFormList)
            if existing:
                month = database_form.month
                initial_data = get_initial_data(form29_model, database_form)
            else:
                month = month_name
                initial_data = {
                    'observer': full_name,
                    'date': now,
                    'month': month_name,
                }
            data = spill_kits_form(initial=initial_data)
        
        if request.method == "POST":
            dataCopy = request.POST.copy()
            dataCopy["facilityChoice"] = options
            if existing:
                form = spill_kits_form(dataCopy, instance=database_form)
            else:
                form = spill_kits_form(dataCopy)
                
            if form.is_valid():
                form.save()
                
                new_latest_form = form29_model.objects.filter(month=month_name)[0]
                filled_out = True
                for items in new_latest_form.whatever().values():
                    print(items)
                    if items is None or items == '':
                        filled_out = False  # -change this back to false
                        break

                if filled_out:    
                    updateSubmissionForm(fsID, True, todays_log.date_save)
                    
                return redirect('IncompleteForms', facility)
    else:
        batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    return render(request, "shared/forms/monthly/spillkits_form.html", {
        'iFormList': iFormList, 
        'month': month, 
        'facility': facility, 
        'sk_form': data, 
        'selector': selector, 
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock, 
        'formName': formName, 
        'search': search, 
        'existing': existing,
        'fsID': fsID,
        'notifs': notifs,
        'freq': freq
    })

@lock
def spill_kits_inventory_form(request, facility, fsID, month, skNumber, selector):
    formName = "26"
    freq = getFacSettingsInfo(fsID)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    search = False
    existing = False
    options = bat_info_model.objects.all().filter(facility_name=facility)[0]
    count_bp = daily_battery_profile_model.objects.count()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    submitted_forms = form26_model.objects.all().order_by('-date')
    today = date.today()
    now = datetime.now().date()
    full_name = request.user.get_full_name()
    skForm = spill_kit_inventory_form()
    attachedTo = form29_model.objects.filter(month=month)
    
    if len(attachedTo) > 0:
        formAttached = attachedTo[0]
    else:
        formAttached = "form"
        
    if count_bp != 0:
        todays_log = daily_prof[0]
        if selector not in ['form','edit']:
            print('CHECK 1')
            for x in submitted_forms:
                if str(x.date) == str(selector) and x.skID == skNumber:
                    database_model = x
            data = database_model
            existing = True
            search = True
            print(data)
        elif len(submitted_forms) > 0:
            print('CHECK 2')
            if now == todays_log.date_save:
                filterByskID = form26_model.objects.filter(skID=skNumber).order_by('-date')
                if len(filterByskID) > 0:
                    database_form = filterByskID[0]
                    if todays_log.date_save.month == database_form.date.month:
                        existing = True
            else:
                batt_prof = '../../../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                return redirect(batt_prof)
        if search:
            print('CHECK 1.1')
            database_form = ''
            data2 = {
                    "counted_items": ast.literal_eval(data.counted_items),
                    "missing_items": ast.literal_eval(data.missing_items)
                }
            print(data2)
        else:
            if existing:
                print('CHECK 2.1')
                initial_data = {
                    "date": database_form.date,
                    "inspector":  database_form.inspector,
                    'skID':  database_form.skID,
                    "type":  database_form.type,
                }
                data2 = {
                    "counted_items": ast.literal_eval(database_form.counted_items),
                    "missing_items": ast.literal_eval(database_form.missing_items)
                }
                print(data2['counted_items'][0])
                print(selector)
            else:
                print('CHECK 3')
                initial_data = {
                    "date": todays_log.date_save,
                    "inspector":  full_name,
                    'skID':  skNumber
                }
                data2 = ''
                
            data = spill_kit_inventory_form(initial=initial_data)
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)
    
    if request.method == "POST":
        dataPOST = request.POST
        if len(attachedTo) > 0:
            skSubmitted = attachedTo[0]
        copyData = request.POST.copy()
        if dataPOST['type'] == 'oil XL cart':
            copyData['counted_items'] = [
                dataPOST['t1count1'],
                dataPOST['t1count2'],
                dataPOST['t1count3'],
                dataPOST['t1count4'],
                dataPOST['t1count5'],
                dataPOST['t1count6'],
                dataPOST['t1count7'],
                dataPOST['t1count8'],
                dataPOST['t1count9'],
                dataPOST['t1count10']
            ]
            copyData['missing_items'] = [
                dataPOST['t1miss1'],
                dataPOST['t1miss2'],
                dataPOST['t1miss3'],
                dataPOST['t1miss4'],
                dataPOST['t1miss5'],
                dataPOST['t1miss6'],
                dataPOST['t1miss7'],
                dataPOST['t1miss8'],
                dataPOST['t1miss9'],
                dataPOST['t1miss10']
            ]
        else:
            copyData['counted_items'] = [
                dataPOST['t2count1'],
                dataPOST['t2count2'],
                dataPOST['t2count3'],
                dataPOST['t2count4'],
                dataPOST['t2count5'],
                dataPOST['t2count6'],
                dataPOST['t2count7'],
                dataPOST['t2count8'],
                dataPOST['t2count9']
            ]
            copyData['missing_items'] = [
                dataPOST['t2miss1'],
                dataPOST['t2miss2'],
                dataPOST['t2miss3'],
                dataPOST['t2miss4'],
                dataPOST['t2miss5'],
                dataPOST['t2miss6'],
                dataPOST['t2miss7'],
                dataPOST['t2miss8'],
                dataPOST['t2miss9']
            ]
        #copyData['spill_kit_submitted'] = skSubmitted
        print(copyData)
        copyData['facilityChoice'] = options
        if existing:
            form = spill_kit_inventory_form(copyData, instance=database_form)
        else:
            form = spill_kit_inventory_form(copyData)
        if form.is_valid():
            form.save()
            
            return redirect('form29', facility, fsID, "form")
                
    return render(request, "shared/forms/monthly/spillKits_inventoryForm.html",{
        'full_name': full_name,
        'skNumber': skNumber, 
        'skForm': skForm, 
        'facility': facility, 
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock, 
        'formName': formName, 
        "data": data, 
        "search": search, 
        "existing": existing, 
        "data2": data2, 
        "formAttached": formAttached, 
        "selector": selector,
        'fsID': fsID,
        'notifs': notifs,
        'freq': freq,
    })