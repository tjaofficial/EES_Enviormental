from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..models import facility_model, user_profile_model, Forms, formSubmissionRecords_model, form_settings_model, the_packets_model
from ..forms import the_packets_form, form_settings_form
from django.contrib.auth.decorators import login_required # type: ignore
from .form_settings_builds import formSettingsFunc
from ..utils.main_utils import defaultPacketSettings, setUnlockClientSupervisor, checkIfFacilitySelected, getCompanyFacilities, defaultGlobalFormSettingsDict
from django.db.models import Q # type: ignore
from django.core.paginator import Paginator # type: ignore
from django.contrib import messages # type: ignore
from django.http import JsonResponse # type: ignore
from copy import deepcopy

import datetime
import json
from ..decor import group_required

lock = login_required(login_url='Login')

@lock
@group_required(SUPER_VAR)
def facilityList(request):
    facility = getattr(request, 'facility', None)
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    facList = getCompanyFacilities(request.user.user_profile.company.company_name)
    formSettingsModelOG = form_settings_model.objects.all()
    packetData = the_packets_model.objects.all()

    finalList = []
    for fac in facList:
        formSettingsQuery = formSettingsModelOG.filter(facilityChoice=fac).order_by('id')
        finalList.append((fac, formSettingsQuery))
        
    if request.method == 'POST':
        answer = request.POST
        print(answer)
        if 'newPacket' in answer.keys():
            dataCopy = answer.copy()
            facChoice = facility_model.objects.get(id=int(answer['facilityID']))
            dataCopy['facilityChoice'] = facChoice
            dataCopy['frequency'] = 'Weekly'
            packetFormData = the_packets_form(dataCopy)

            print(packetFormData.errors)
            if packetFormData.is_valid():
                A = packetFormData.save(commit=False)
                print(A)
                A.formList = defaultPacketSettings
                A.save()
                messages.success(request,f"New packet {A.name} has been created for {A.facilityChoice.facility_name}.")
            print('New Packet has been saved')
        elif 'sub_delete' in answer.keys():
            print('delete-packet')
            packToArchive = packetData.get(id=answer['packID'])
            print(packToArchive)
            packToArchive.formList['settings']['active'] = False
            for packForm in packToArchive.formList["formsList"]:
                packToArchive.formList["formsList"][packForm]['active'] = False
            packToArchive.save()
            print("ARCHIVED PACKET")
            return redirect(facilityList)
        elif 'facForm_delete' in answer.keys():
            fsID = answer['facFormID']
            facID = answer['facID']
            #-----Archives selected form from all packets-----
            for pac in packetData.filter(facilityChoice__id=facID):
                for setList in pac.formList["formsList"]:
                    if fsID == pac.formList["formsList"][setList]['settingsID']:
                        print('check 2')
                        pac.formList["formsList"][setList]['active'] = False
                        finalArchive = pac
                        finalArchive.save()

            #-----Archives selected form from Global Forms-----
            formToArchive = formSettingsModelOG.get(id=fsID)
            formToArchive.settings['active'] = False
            formToArchive.save(changed_by=request.user, reason="archive")
            return redirect(facilityList)
        elif 'pacForm_delete' in answer.keys():
            fsIDDelte = answer['pacForm_delete'][14:]
            fsID = answer[f'facFormID{fsIDDelte}']
            pacID = answer[f'pacID{fsIDDelte}']
            print(f"This is the pacID {pacID}")
            #-----Archives selected form from all packets-----
            pac = packetData.get(id=pacID)
            for setList in pac.formList["formsList"]:
                print(fsID)
                print(pac.formList["formsList"][setList]['settingsID'])
                if int(fsID) == pac.formList["formsList"][setList]['settingsID']:
                    print('check 2')
                    pac.formList["formsList"][setList]['active'] = False
                    finalArchive = pac
                    finalArchive.save()
            return redirect(facilityList)
        elif 'packet_update' in answer.keys():
            #receiving fsID and packetID in format of "27-6"
            print(answer['packet_update'])
            print('packetUpdate')
            fsID, packetID = answer['packet_update'].split("-")
            thePacket = packetData.get(id=packetID)
            theSettings = formSettingsModelOG.get(id=fsID)
            #dont forget to come back and delete this no-lbale- BS
            highestLabelNumb = 0
            allLabelsInPacket = thePacket.formList["formsList"]
            if allLabelsInPacket:
                for label in allLabelsInPacket:
                    settingsID = allLabelsInPacket[label]['settingsID']
                    if int(settingsID) == int(fsID):
                        messages.error(request,"The selected form is already been added to the packet.")
                        return redirect(facilityList)
                for label in allLabelsInPacket.keys():
                    noLabelTag = label[:9]
                    noLabelNumber = label[9:]
                    if noLabelTag == "no-label-":
                        if int(noLabelNumber) > int(highestLabelNumb):
                            highestLabelNumb = noLabelNumber
            formNoLabelParse = "no-label-"+str(int(highestLabelNumb)+1)
            if allLabelsInPacket:
                allLabelsInPacket[formNoLabelParse] = {"settingsID":int(fsID), "active": True}
            else:
                allLabelsInPacket = {formNoLabelParse: {"settingsID":int(fsID), "active": True}}

            if theSettings.settings['packets']:
                print('check 1')
                theSettings.settings['packets'][str(thePacket.id)] = formNoLabelParse
            else:
                print('check 2')
                theSettings.settings['packets'] = {str(thePacket.id): formNoLabelParse}
            A = thePacket
            B = theSettings
            A.save()
            B.save(changed_by=request.user, reason='packet_update')
            print('Updating Packet')
            messages.success(request,"The selected form has been added to the packet.")
        elif 'pack_settings' in answer.keys():
            packEntry = packetData.get(id=answer['packID'])
            packEntry.formList['settings']['frequency'] = answer['frequency']
            packEntry.name = answer['name']
            packEntry.save()
            return redirect(facilityList)
    return render(request, 'supervisor/sup_facilityList.html', {
        'notifs': notifs,
        'facility': facility, 
        'unlock': unlock, 
        'client': client, 
        'supervisor': supervisor, 
        'facilities': finalList,
        'packetData': packetData,
        'packetForm': the_packets_form,
        'formSettingsModel': formSettingsModelOG,
    })

@lock
def get_facility_form_data(request):
    facList = []
    
    facilities_qs = getCompanyFacilities(request.user.user_profile.company.company_name)
    
    for facility in facilities_qs:
        fsForms = form_settings_model.objects.filter(facilityChoice=facility, settings__active=True)
        globalActiveForms = [fsSelect.id for fsSelect in fsForms]
        facList.append({
            "facility_name": facility.facility_name,
            "facility_id": facility.id,
            "fsIDList": globalActiveForms,
        })
    print(facList)
    return JsonResponse(facList, safe=False)

@lock
@group_required(SUPER_VAR) 
def facilityForm(request, packet):
    facility = getattr(request, 'facility', None)
    notifs = checkIfFacilitySelected(request.user)
    q = request.GET.get('q')
    packetQuery = the_packets_model.objects.get(id=packet)
    formSettingsQuery = form_settings_model.objects.filter(facilityChoice=facility)
    # If someone searched for a specific for this adjusts
    # the previoous list created. Narrows it down to only
    # what fits the search.
    if q:
        formSettingsQuery = formSettingsQuery.filter(
            Q(title__icontains=q) |
            Q(header__icontains=q)
        ).distinct()
    
    p = Paginator(formSettingsQuery, 15)
    page = request.GET.get('page')
    pageData = p.get_page(page)

    print("-------------------------")

    if request.method == 'POST':
        answer = request.POST
        print(answer)
        #for all selected and filled in, save as a dictionary for the packet
        selectedList = {}
        fsIDsFromInputs = []
        for allKeys in answer.keys():
            if allKeys[:5] == 'forms':
                inputID = allKeys[5:]
                fsIDsFromInputs.append((answer['forms'+inputID], answer['formID'+inputID], answer['settingsID'+inputID]))

        for item in fsIDsFromInputs:
            label = item[1]
            settingsID = int(item[2])
            formOrgLabel = 'formID' + str(item)

            selectedList[label] = {"settingsID": settingsID, "active": True}
            settingsEntry = form_settings_model.objects.get(id=settingsID)
            settingsEntryPacks = settingsEntry.settings["packets"]
            if settingsEntryPacks:
                settingsEntry.settings["packets"][str(packetQuery.id)] = label
            else:
                settingsEntry.settings["packets"] = {str(packetQuery.id): label}
            A = settingsEntry
            A.save(changed_by=request.user, reason='packet_update')
                
        packetQuery.formList["formsList"] = selectedList
        packetQuery.save()
        
        return redirect('facilityList')
    return render (request, 'supervisor/facilityForms.html', {
        'notifs': notifs, 
        'facility': facility, 
        'packet': packetQuery,
        'pageData': pageData,
        'query': q
    })
    
@lock
@group_required(SUPER_VAR) 
def facility_form_settings(request, fsID, packetID, formLabel):
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    selectedSettings = form_settings_model.objects.get(id=fsID)
    formData = selectedSettings.formChoice
    formID = formData.form
    if packetID[:5] != 'facID':
        packetSettings = the_packets_model.objects.get(id=packetID)
        print('check 2')
    else:
        packetSettings = False
        print('check 3')
    
    if formLabel != 'none':
        print('check 1')
        for form in packetSettings.formList['formsList']:
            if form == formLabel:
                settingsID = packetSettings.formList['formsList'][form]['settingsID']
                break
                
    formSettings = selectedSettings.settings
    if request.method == "POST":
        copyPOST = request.POST.copy()
        copyPOST['facilityChoice'] = selectedSettings.facilityChoice
        copyPOST['formChoice'] = selectedSettings.formChoice
        copyPOST['subChoice'] = selectedSettings.subChoice
        keysList = []
        for inputs in request.POST.keys():
            keysList.append(inputs)
        print("--------------------------")
        print(keysList)
        # chek this utils
        newLabel, settingsDict = formSettingsFunc(keysList, request.POST, int(formID))
        print(settingsDict)
        print(f"This is the new label: {newLabel}")
        settingsChange = selectedSettings.settings
        settingsChange['settings'] = settingsDict
        if newLabel:
            settingsChange['packets'][str(packetID)] = newLabel
        copyPOST['settings'] = settingsChange
        formWData = form_settings_form(copyPOST, instance=selectedSettings)
        if formWData.is_valid():
            print('it fucking saved')
            A = formWData.save(commit=False)
            A.save(changed_by=request.user, reason='update')
            formWData.save_m2m()
            if packetSettings:
                print('check 7')
                packetInstance = packetSettings
                packetInstance.formList['formsList'][newLabel] = packetInstance.formList['formsList'].pop(formLabel)
                packetInstance.save()
            #else:
            #     packetInstance = packetSettings
            #     packetInstance.formList['formsList'][newLabel] = {"settingsID": A.id}
            #     packetInstance.save()
            messages.success(request,"The form settings were updated.")
            return redirect('facilityList')
        #     if packetSettings:
        #         newLabel = request.POST['newLabel']
        #         if newLabel not in [formLabel, ""]:
        #             packetSettings.formList['formsList'][newLabel] = packetSettings.formList['formsList'][formLabel]
        #             del packetSettings.formList['formsList'][formLabel]
        #             A = packetSettings
        #             A.save()
                
        else:
            messages.error(request,"Check your inputs and make sure informationw as entered in correctly.")
    return render (request, 'supervisor/facilityForms/facilityFormSettings.html', {
        'notifs': notifs,
        'unlock': unlock, 
        'client': client, 
        'supervisor': supervisor, 
        'formLabel': formLabel,
        'formData': formData,
        'formID': str(formID),
        'formSettings': formSettings,
        'packetSettings': packetSettings,
        'packetID': packetID
    })
    
@lock
@group_required(SUPER_VAR)
def Add_Forms(request):
    facilitySelect = getattr(request, 'facility', None)
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    today = datetime.date.today()
    formList = sorted(
        Forms.objects.all(),
        key=lambda f: int(f.form) if f.form.isdigit() else float('inf')
    )
    q = request.GET.get('q')
    if q:
        formList = formList.filter(
            Q(title__icontains=q) |
            Q(header__icontains=q)
        ).distinct()
    formSettingsQuery = form_settings_model.objects.filter(facilityChoice=facilitySelect)
    print("-------------------------")
    print(formList[0].form)
    p = Paginator(formList, 20)
    page = request.GET.get('page')
    pageData = p.get_page(page)
    first_load = not page and not q
    
    if request.method == 'POST':
        answer = request.POST
        print(answer)
        settingsDictData = json.loads(answer['form_settings'])
        ## Builds the new list of forms selected and created a submission record for each
        selected_form_ids = settingsDictData.keys()
        for formID in selected_form_ids:
            formID = int(formID)
            sameForm = False
            form_qs = formSettingsQuery.filter(formChoice__form=formID)
            settingsDict = deepcopy(defaultGlobalFormSettingsDict)
            for x in settingsDictData[str(formID)].keys():
                print("--------")
                print(x)
                print(settingsDictData[str(formID)][x])
                print("--------")
                # if len(x.split("-")) > 1:
                #     requestFormID = x.split("-")[0]
                #     requestInputName = x.split("-")[1]
                #     if requestFormID == str(formID):
                settingsDict["settings"][x] = settingsDictData[str(formID)][x] if settingsDictData[str(formID)][x] else False

            keysList = list
            for setts in answer.keys():
                if len(setts.split("-")) > 1:
                    requestFormID = setts.split("-")[0]
                    if requestFormID == str(formID):
                        keysList.append(setts)
            if formID == 7:
                newLabel, settingsDict["settings"] = formSettingsFunc(keysList, request.POST, formID)

            print(settingsDict)
            settingsDict = json.loads(json.dumps(settingsDict))

            likeFormsList = []
            for likeForms in form_qs:
                oldSettings = likeForms.settings['settings']
                if oldSettings == settingsDict["settings"]:
                    likeFormsList.append(f"fsID: {likeForms.id}")

            if not likeFormsList:
                newSettings = form_settings_model(
                    facilityChoice = facilitySelect,
                    formChoice = Forms.objects.get(form=formID),
                    settings = settingsDict,
                )
                newSub = formSubmissionRecords_model(
                    dateSubmitted = today - datetime.timedelta(days=9000),
                    dueDate = today - datetime.timedelta(days=5000),
                    submitted = False
                )
                newSub.save()
                newSettings.subChoice = newSub
                newSettings.save(changed_by=request.user, reason='create')

                messages.success(request,f"Form {formID} was added to {facilitySelect.facility_name}.")
                print('Create new form setting')
            else:
                messages.error(request,f"Form {formID} already exist for {facilitySelect.facility_name}. These forms include: {likeFormsList}")
        print("Forms Have Been Saved")
        return redirect('facilityList')
    return render(request, 'supervisor/facilityForms/add_form_to_facility.html', {
        'notifs': notifs, 
        'unlock': unlock, 
        'client': client, 
        'supervisor': supervisor, 
        'formList': formList,
        'pageData': pageData,
        'query': q,
        'first_load': first_load,
    })

@lock
@group_required(SUPER_VAR)
def update_packet_form_label(request):
    data = json.loads(request.body)
    packetID = data.get("packet_ID")
    fsID = data.get("fs_ID")
    new_label = data.get("newLabel")
    packetSelect = the_packets_model.objects.get(id=packetID)
    fsSelect = form_settings_model.objects.get(id=fsID)
    
    for key, item in packetSelect.formList['formsList'].items():
        if item['settingsID'] == int(fsID):
            packetSelect.formList['formsList'][new_label] = packetSelect.formList['formsList'].pop(key)
            break
    fsSelect.settings['packets'][str(packetID)] = new_label
    
    packetSelect.save()
    fsSelect.save()
    
    return JsonResponse({"success": True, "new_label": new_label})




