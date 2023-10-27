from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import spill_kits_form, spill_kit_inventory_form
from ..models import daily_battery_profile_model, Forms, spill_kits_model, bat_info_model, spill_kit_inventory_model
import datetime
import calendar
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
import json
import ast
from ..utils import stringToDate, setUnlockClientSupervisor, updateSubmissionForm

lock = login_required(login_url='Login')

@lock
def spill_kits(request, facility, selector):
    formName = "26"
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    existing = False
    search = False
    options = bat_info_model.objects.all().filter(facility_name=facility)[0]
    now = datetime.datetime.now()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    sk_form = spill_kits_form()
    full_name = request.user.get_full_name()
    today = datetime.date.today()
    org = spill_kits_model.objects.all().order_by('-date')
    month_name = calendar.month_name[today.month]
    
    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector != 'form':
            print('CHECK 1')
            for x in org:
                if str(x.date) == str(selector):
                    database_model = x
            data = database_model

            existing = True
            search = True
        elif len(org) > 0:
            print('CHECK 2')
            database_form = org[0]
            datetime_object = datetime.datetime.strptime(database_form.month, "%B")
            month_number = datetime_object.month

            if now.month == month_number:
                print('CHECK 3')
                existing = True
        iFormList = {}
        if search:
            print('CHECK 1.2')
            database_form = ''
            month = database_model.month
            inventoryModel = spill_kit_inventory_model.objects.filter(date__month=database_model.date.month)
            for subForm in inventoryModel:
                iFormList[subForm.skID] = [subForm.skID,stringToDate(subForm.date)]
            iFormList = json.dumps(iFormList)
        else:
            inventoryModel = spill_kit_inventory_model.objects.filter(date__month=now.month)
            if len(inventoryModel) > 0:
                for subForm in inventoryModel:
                    iFormList[subForm.skID] = [subForm.skID,stringToDate(subForm.date)]
                iFormList = json.dumps(iFormList)
            print(iFormList)
            if existing:
                month = database_form.month
                initial_data = {
                    'observer': database_form.observer,
                    'date': database_form.date,
                    'month': database_form.month,
                    'sk1_tag_on': database_form.sk1_tag_on,
                    'sk1_serial': database_form.sk1_serial,
                    'sk1_complete': database_form.sk1_complete,
                    'sk1_report': database_form.sk1_report,
                    'sk1_comment': database_form.sk1_comment,
                    
                    'sk2_tag_on': database_form.sk2_tag_on,
                    'sk2_serial': database_form.sk2_serial,
                    'sk2_complete': database_form.sk2_complete,
                    'sk2_report': database_form.sk2_report,
                    'sk2_comment': database_form.sk2_comment,
                    
                    'sk3_tag_on': database_form.sk3_tag_on,
                    'sk3_serial': database_form.sk3_serial,
                    'sk3_complete': database_form.sk3_complete,
                    'sk3_report': database_form.sk3_report,
                    'sk3_comment': database_form.sk3_comment,
                    
                    'sk4_tag_on': database_form.sk4_tag_on,
                    'sk4_serial': database_form.sk4_serial,
                    'sk4_complete': database_form.sk4_complete,
                    'sk4_report': database_form.sk4_report,
                    'sk4_comment': database_form.sk4_comment,
                    
                    'sk5_tag_on': database_form.sk5_tag_on,
                    'sk5_serial': database_form.sk5_serial,
                    'sk5_complete': database_form.sk5_complete,
                    'sk5_report': database_form.sk5_report,
                    'sk5_comment': database_form.sk5_comment,
                    
                    'sk6_tag_on': database_form.sk6_tag_on,
                    'sk6_serial': database_form.sk6_serial,
                    'sk6_complete': database_form.sk6_complete,
                    'sk6_report': database_form.sk6_report,
                    'sk6_comment': database_form.sk6_comment,
                    
                    'sk7_tag_on': database_form.sk7_tag_on,
                    'sk7_serial': database_form.sk7_serial,
                    'sk7_complete': database_form.sk7_complete,
                    'sk7_report': database_form.sk7_report,
                    'sk7_comment': database_form.sk7_comment,
                    
                    'sk8_tag_on': database_form.sk8_tag_on,
                    'sk8_serial': database_form.sk8_serial,
                    'sk8_complete': database_form.sk8_complete,
                    'sk8_report': database_form.sk8_report,
                    'sk8_comment': database_form.sk8_comment,
                    
                    'sk9_tag_on': database_form.sk9_tag_on,
                    'sk9_serial': database_form.sk9_serial,
                    'sk9_complete': database_form.sk9_complete,
                    'sk9_report': database_form.sk9_report,
                    'sk9_comment': database_form.sk9_comment,
                    
                    'sk10_tag_on': database_form.sk10_tag_on,
                    'sk10_serial': database_form.sk10_serial,
                    'sk10_complete': database_form.sk10_complete,
                    'sk10_report': database_form.sk10_report,
                    'sk10_comment': database_form.sk10_comment,
                    
                    'sk11_tag_on': database_form.sk11_tag_on,
                    'sk11_serial': database_form.sk11_serial,
                    'sk11_complete': database_form.sk11_complete,
                    'sk11_report': database_form.sk11_report,
                    'sk11_comment': database_form.sk11_comment,
                    
                    'sk12_tag_on': database_form.sk12_tag_on,
                    'sk12_serial': database_form.sk12_serial,
                    'sk12_complete': database_form.sk12_complete,
                    'sk12_report': database_form.sk12_report,
                    'sk12_comment': database_form.sk12_comment,
                    
                    'sk13_tag_on': database_form.sk13_tag_on,
                    'sk13_serial': database_form.sk13_serial,
                    'sk13_complete': database_form.sk13_complete,
                    'sk13_report': database_form.sk13_report,
                    'sk13_comment': database_form.sk13_comment,
                    
                    'sk14_tag_on': database_form.sk14_tag_on,
                    'sk14_serial': database_form.sk14_serial,
                    'sk14_complete': database_form.sk14_complete,
                    'sk14_report': database_form.sk14_report,
                    'sk14_comment': database_form.sk14_comment,
                    
                    'sk15_tag_on': database_form.sk15_tag_on,
                    'sk15_serial': database_form.sk15_serial,
                    'sk15_complete': database_form.sk15_complete,
                    'sk15_report': database_form.sk15_report,
                    'sk15_comment': database_form.sk15_comment,
                    
                    'sk16_tag_on': database_form.sk16_tag_on,
                    'sk16_serial': database_form.sk16_serial,
                    'sk16_complete': database_form.sk16_complete,
                    'sk16_report': database_form.sk16_report,
                    'sk16_comment': database_form.sk16_comment,
                    
                    'sk17_tag_on': database_form.sk17_tag_on,
                    'sk17_serial': database_form.sk17_serial,
                    'sk17_complete': database_form.sk17_complete,
                    'sk17_report': database_form.sk17_report,
                    'sk17_comment': database_form.sk17_comment,
                    
                    'sk18_tag_on': database_form.sk18_tag_on,
                    'sk18_serial': database_form.sk18_serial,
                    'sk18_complete': database_form.sk18_complete,
                    'sk18_report': database_form.sk18_report,
                    'sk18_comment': database_form.sk18_comment,
                    
                    'sk19_tag_on': database_form.sk19_tag_on,
                    'sk19_serial': database_form.sk19_serial,
                    'sk19_complete': database_form.sk19_complete,
                    'sk19_report': database_form.sk19_report,
                    'sk19_comment': database_form.sk19_comment,
                    
                    'sk20_tag_on': database_form.sk20_tag_on,
                    'sk20_serial': database_form.sk20_serial,
                    'sk20_complete': database_form.sk20_complete,
                    'sk20_report': database_form.sk20_report,
                    'sk20_comment': database_form.sk20_comment,
                    
                    'sk21_tag_on': database_form.sk21_tag_on,
                    'sk21_serial': database_form.sk21_serial,
                    'sk21_complete': database_form.sk21_complete,
                    'sk21_report': database_form.sk21_report,
                    'sk21_comment': database_form.sk21_comment,
                    
                    'skut22_tag_on': database_form.skut22_tag_on,
                    'skut22_serial': database_form.skut22_serial,
                    'skut22_complete': database_form.skut22_complete,
                    'skut22_report': database_form.skut22_report,
                    'skut22_comment': database_form.skut22_comment,
                    
                    'skut23_tag_on': database_form.skut23_tag_on,
                    'skut23_serial': database_form.skut23_serial,
                    'skut23_complete': database_form.skut23_complete,
                    'skut23_report': database_form.skut23_report,
                    'skut23_comment': database_form.skut23_comment,
                    
                    'skut24_tag_on': database_form.skut24_tag_on,
                    'skut24_serial': database_form.skut24_serial,
                    'skut24_complete': database_form.skut24_complete,
                    'skut24_report': database_form.skut24_report,
                    'skut24_comment': database_form.skut24_comment,
                    
                    'skut25_tag_on': database_form.skut25_tag_on,
                    'skut25_serial': database_form.skut25_serial,
                    'skut25_complete': database_form.skut25_complete,
                    'skut25_report': database_form.skut25_report,
                    'skut25_comment': database_form.skut25_comment,
                    
                    'skut26_tag_on': database_form.skut26_tag_on,
                    'skut26_serial': database_form.skut26_serial,
                    'skut26_complete': database_form.skut26_complete,
                    'skut26_report': database_form.skut26_report,
                    'skut26_comment': database_form.skut26_comment,
                }
            else:
                month = month_name
                initial_data = {
                    'observer': full_name,
                    'date': todays_log.date_save,
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
                
                new_latest_form = spill_kits_model.objects.filter(month=month_name)[0]
                filled_out = True
                for items in new_latest_form.whatever().values():
                    print(items)
                    if items is None or items == '':
                        filled_out = False  # -change this back to false
                        break

                if filled_out:    
                    updateSubmissionForm(facility, formName, True, todays_log.date_save)
                    
                return redirect('IncompleteForms', facility)
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Monthly/spillkits_form.html", {
        'iFormList': iFormList, 'month': month, 'facility': facility, 'sk_form': data, 'selector': selector, 'supervisor': supervisor, "client": client, 'unlock': unlock, 'formName': formName, 'search': search, 'existing': existing, 
    })

@lock
def spill_kits_inventory_form(request, facility, month, skNumber, selector):
    formName = "spill_kits_inventory"
    unlock = False
    client = False
    supervisor = False
    search = False
    existing = False
    if request.user.groups.filter(name=OBSER_VAR):
        unlock = True
    if request.user.groups.filter(name=CLIENT_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    
    count_bp = daily_battery_profile_model.objects.count()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    org = spill_kit_inventory_model.objects.all().order_by('-date')
    today = datetime.date.today()
    now = datetime.datetime.now()
    full_name = request.user.get_full_name()
    skForm = spill_kit_inventory_form()
    attachedTo = spill_kits_model.objects.filter(month=month)
    
    if len(attachedTo) > 0:
        formAttached = attachedTo[0]
    else:
        formAttached = "form"
        
    if count_bp != 0:
        todays_log = daily_prof[0]
        if selector not in ['form','edit']:
            print('CHECK 1')
            for x in org:
                if str(x.date) == str(selector) and x.skID == skNumber:
                    database_model = x
            data = database_model
            existing = True
            search = True
            print(data)
        elif len(org) > 0:
            print('CHECK 2')
            if now.month == todays_log.date_save.month:
                if now.day == todays_log.date_save.day:
                    filterByskID = spill_kit_inventory_model.objects.filter(skID=skNumber).order_by('-date')
                    if len(filterByskID) > 0:
                        database_form = filterByskID[0]
                        if todays_log.date_save.month == database_form.date.month:
                            existing = True
                else:
                    batt_prof = '../../../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                    return redirect(batt_prof)
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
        if existing:
            form = spill_kit_inventory_form(copyData, instance=database_form)
        else:
            form = spill_kit_inventory_form(copyData)
        if form.is_valid():
            form.save()
            
            return redirect('spill_kits', facility, "form")
                
    return render(request, "Monthly/spillKits_inventoryForm.html",{
        'full_name': full_name,'skNumber': skNumber, 'skForm': skForm, 'facility': facility, 'supervisor': supervisor, "client": client, 'unlock': unlock, 'formName': formName, "data": data, "search": search, "existing": existing, "data2": data2, "formAttached": formAttached, "selector": selector
    })