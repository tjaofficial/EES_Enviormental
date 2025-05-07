from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..models import facility_model, user_profile_model, facility_forms_model, Forms, formSubmissionRecords_model, form_settings_model, the_packets_model
from ..forms import the_packets_form, form_settings_form
from django.contrib.auth.decorators import login_required # type: ignore
import datetime
import json
from .form_settings_builds import formSettingsFunc
from ..utils.main_utils import defaultPacketSettings, setUnlockClientSupervisor, checkIfFacilitySelected, getCompanyFacilities, get_facility_forms, changeStringListIntoList
from django.db.models import Q # type: ignore
from django.core.paginator import Paginator # type: ignore
from django.contrib import messages # type: ignore
from django.http import JsonResponse # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore

lock = login_required(login_url='Login')

@lock
def facilityList(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    if unlock:
        return redirect('IncompleteForms', facility)
    if client:
        return redirect('c_dashboard', facility)
    facList = getCompanyFacilities(request.user.user_profile.company.company_name)
    formSettingsModelOG = form_settings_model.objects.all()
    packetData = the_packets_model.objects.all()

    finalList = []
    for newFac in facList:
        formSettingsModel = formSettingsModelOG.filter(facilityChoice=newFac)
        facilityForms = get_facility_forms('facilityID', newFac.id)
        if len(facilityForms) > 0:
            labelList = []
            for label in facilityForms:
                fsIDRecord = formSettingsModel.get(id=int(label))
                labelList.append((fsIDRecord))
            def myFunc(e):
                return e.id
            labelList.sort(key=myFunc)
            
            finalList.append((newFac, labelList))
        else:
            finalList.append((newFac, facilityForms))
    if request.method == 'POST':
        answer = request.POST
        print(answer)
        if 'facilitySelect' in answer.keys():
            return redirect('sup_dashboard', answer['facilitySelect'])
        elif 'newPacket' in answer.keys():
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
            print('hello')
        elif 'sub_delete' in answer.keys():
            print('delete-packet')
            packToDelete = packetData.get(id=answer['packID'])
            print(packToDelete)
            formSettingsQuery = form_settings_model.objects.filter(
                ~Q(settings__packets=False),
                facilityChoice__id=packToDelete.facilityChoice.id,
                settings__packets__has_key=str(packToDelete.id)
            )
            print("______________________")
            print(formSettingsQuery)
            print(str(packToDelete.id))
            if formSettingsQuery.exists():
                for fsEntry in formSettingsQuery:
                    del fsEntry.settings['packets'][str(packToDelete.id)]
                    fsEntry.save()

            # need to delete the log of what packet and what label from the fsModel record;




            # if not packToDelete.formList["formsList"]:
            #     for pacForms in packToDelete.formList["formsList"]:
            #         for formSettingsEntry in formSettingsQuery:
            #             if packToDelete.formList["formsList"][pacForms]['settingsID'] == formSettingsEntry.id:
            #                 del formSettingsEntry.settings['packets'][str(packToDelete.id)]
            #                 formSettingsEntry.save()
            packToDelete.delete()
            print("DELETED PACKET")
            return redirect(facilityList, facility)
        elif 'facForm_delete' in answer.keys():
            fsID = answer['facFormID']
            facID = answer['facID']
            #delete from all packets
            for pac in packetData.filter(facilityChoice__id=facID):
                for setList in pac.formList["formsList"]:
                    if fsID == pac.formList["formsList"][setList]['settingsID']:
                        print('check 2')
                        del pac.formList["formsList"][setList]
                        finalDelete = pac
                        finalDelete.save()

## at this point after clicking delete for a specific form
## it has removed the form from every packet. Where im at now is
## wondering that if it gets deleted from every packet... theres
## no more reference to its old name. So if a client is trying
## to print an old for (could be archived) the system will still
## have the form in the database but that form will have an
## invlaid input for the formSettings input. and can no longer
## pull any data from the main source.

## need to remove it from facility_form_model
## change the model.settings["active"] to false


            #delete form facility forms model
            thisFacilityForm = facList.get(id=facID)
            print(thisFacilityForm)
            makeFacFormsList = get_facility_forms('facilityID', thisFacilityForm.id)
            for ids in makeFacFormsList:
                print(ids)
                if int(ids) ==  int(fsID):
                    makeFacFormsList.remove(ids)
            print(makeFacFormsList)
            thisFacilityForm.formData = makeFacFormsList
            facilityFormDelete = thisFacilityForm
            facilityFormDelete.save()
            #Change acive from "true" to 'false' to archive form from settings model
            formToDelete = formSettingsModelOG.get(id=fsID)
            formToDelete.settings['active'] = False
            formToDelete.save()
            return redirect(facilityList, facility)
        elif 'packet_update' in answer.keys():
            #receiving fsID and packetID in format of "27-6"
            print(answer['packet_update'])
            print('packetUpdate')
            dataReceived = answer['packet_update'].split("-")
            fsID = dataReceived[0]
            packetID = dataReceived[1]
            thePacket = packetData.get(id=packetID)
            theSettings = formSettingsModelOG.get(id=fsID)
            highestLabelNumb = 0

            if thePacket.formList["formsList"]:
                for label in thePacket.formList["formsList"]:
                    settingsID = thePacket.formList["formsList"][label]['settingsID']
                    if int(settingsID) == int(fsID):
                        messages.error(request,"The selected form is already been added to the packet.")
                        return redirect(facilityList, facility)
                for label in thePacket.formList["formsList"].keys():
                    noLabelTag = label[:9]
                    noLabelNumber = label[9:]
                    if noLabelTag == "no-label-":
                        if int(noLabelNumber) > int(highestLabelNumb):
                            highestLabelNumb = noLabelNumber
            formNoLabelParse = "no-label-"+str(int(highestLabelNumb)+1)
            if thePacket.formList["formsList"]:
                thePacket.formList["formsList"][formNoLabelParse] = {"settingsID":int(fsID)}
            else:
                thePacket.formList["formsList"] = {formNoLabelParse: {"settingsID":int(fsID)}}

            settingsEntry = form_settings_model.objects.get(id=int(fsID))
            if settingsEntry.settings['packets']:
                print('check 1')
                settingsEntry.settings['packets'][str(thePacket.id)] = formNoLabelParse
            else:
                print('check 2')
                settingsEntry.settings['packets'] = {str(thePacket.id): formNoLabelParse}
            A = thePacket
            B = settingsEntry
            A.save()
            B.save()
            print('Updating Packet')
            messages.success(request,"The selected form has been added to the packet.")
        elif 'pack_settings' in answer.keys():
            packEntry = packetData.get(id=answer['packID'])
            packEntry.formList['settings']['frequency'] = answer['frequency']
            packEntry.name = answer['name']
            packEntry.save()
            return redirect(facilityList, facility)
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
        facList.append({
            "facility_name": facility.facility_name,
            "facility_id": facility.id,
        })

    return JsonResponse(facList, safe=False)

@lock    
def facilityForm(request, facility, packet):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    if unlock:
        return redirect('IncompleteForms', facility)
    today = datetime.date.today()
    q = request.GET.get('q')
    specificFacility = facility_model.objects.filter(facility_name=facility)[0]
    formList = Forms.objects.all().order_by('form')
    formSettingsModel = form_settings_model.objects.all()
    packetQuery = the_packets_model.objects.get(id=packet)
    facilityFormList = get_facility_forms('facilityID', specificFacility.id)
    # Compares the existing forms added to the facility
    # and all the formSettings entries related to the 
    # facilty. Basically this is pulling all the formSettings
    # entries from all the settingsIDs in the facility forms
    # model. This gives us all the data for all the forms 
    # added to the facility in a nice and neat list to use.
    newFormList = []
    for settingsAll in formSettingsModel.filter(facilityChoice=specificFacility):
        for facFormsAll in facilityFormList:
            if settingsAll.id == int(facFormsAll):
                newFormList.append(settingsAll)
    totalAmountofForms = len(newFormList)
    # If someone searched for a specific for this adjusts
    # the previoous list created. Narrows it down to only
    # what fits the search.
    if q:
        newFormList = newFormList.filter(
            Q(title__icontains=q) |
            Q(header__icontains=q)
        ).distinct()
    
    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
    p = Paginator(newFormList, 15)
    page = request.GET.get('page')
    pageData = p.get_page(page)

    print("-------------------------")
    print(formList[0].form)

    if request.method == 'POST':
        answer = request.POST
        print(answer)
        #for all selected and filled in, save as a dictionary for the packet
        if 'facilitySelect' in answer.keys():
            return redirect('sup_dashboard', answer['facilitySelect'])
        selectedList = {}
        ## Builds the new list of forms selected and created a submission record
        fsIDsFromInputs = []
        for allKeys in answer.keys():
            if allKeys[:5] == 'forms':
                inputID = allKeys[5:]
                fsIDsFromInputs.append(answer['settingsID'+inputID])
        if packetQuery.formList["formsList"]:
            for pacs in packetQuery.formList["formsList"]:
                if str(packetQuery.formList["formsList"][pacs]['settingsID']) not in fsIDsFromInputs:
                    B = form_settings_model.objects.get(id=int(packetQuery.formList["formsList"][pacs]['settingsID']))
                    del B.settings['packets'][str(packetQuery.id)]
                    B.save()

        for item in range(1, totalAmountofForms+1):
            formIDlabel = 'forms' + str(item)
            formOrgLabel = 'formID' + str(item)
            inputSettingsID = 'settingsID' + str(item)
            
            if formIDlabel.replace(" ", "") in answer.keys():
                formID = int(answer[formIDlabel.replace(" ", "")])
                formLabel = answer[formOrgLabel.replace(" ", "")].upper()
                settingsID = int(answer[inputSettingsID])
                # if formLabel:
                #     highestLabelNumb = 0

                #     if packetQuery.formList["formsList"]:
                #         for label in packetQuery.formList["formsList"]:
                #             settingsID2 = packetQuery.formList["formsList"][label]['settingsID']
                #             if int(settingsID2) == int(settingsID):
                #                 messages.error(request,"The selected form is already been added to the packet.")
                #                 return redirect(facilityList, facility)
                #         for label in packetQuery.formList["formsList"].keys():
                #             noLabelTag = label[:9]
                #             noLabelNumber = label[9:]
                #             if noLabelTag == "no-label-":
                #                 if int(noLabelNumber) > int(highestLabelNumb):
                #                     highestLabelNumb = noLabelNumber
                #     formNoLabelParse = "no-label-"+str(int(highestLabelNumb)+1)
                #     if packetQuery.formList["formsList"]:
                #         selectedList[formNoLabelParse] = {"settingsID":int(settingsID)}
                #     else:
                #         packetQuery.formList["formsList"] = {formNoLabelParse: {"settingsID":int(settingsID)}}





                selectedList[formLabel] = {"settingsID": settingsID}
                settingsEntry = form_settings_model.objects.get(id=settingsID)
                settingsEntryPacks = settingsEntry.settings["packets"]
                if settingsEntryPacks:
                    settingsEntry.settings["packets"][str(packetQuery.id)] = formLabel
                else:
                    settingsEntry.settings["packets"] = {str(packetQuery.id): formLabel}
                A = settingsEntry
                A.save()
            else:
                continue
            
        
                
                
        packetQuery.formList["formsList"] = selectedList
        packetQuery.save()
        
        return redirect('facilityList', 'supervisor')
        # ## Removes records for forms that arent selected anymore
        # if existing:
        #     oldForms = []
        #     for transfer in modelList:
        #         oldForms.append(transfer)
        #     different = set(oldForms).difference(selectedList)
            
        #     doesSubExist(specificFacility, different, "list", True)
                
        # dataCopy = request.POST.copy()
        # dataCopy['formData'] = selectedList
        # dataCopy['facilityChoice'] = specificFacility

        # if existing:
        #     form = facility_forms_form(dataCopy, instance=replaceModel)
        # else:
        #     form = facility_forms_form(dataCopy)
            
            
        # if form.is_valid():
        #     form.save()
        #     return redirect('facilityList', facility)
    return render (request, 'supervisor/facilityForms.html', {
        'notifs': notifs, 
        'sortedFacilityData': sortedFacilityData, 
        'facility': facility, 
        'unlock': unlock, 
        'client': client, 
        'supervisor': supervisor, 
        'formList': formList, 
        'packet': packetQuery,
        'formSettingsModel': formSettingsModel,
        'pageData': pageData,
        'query': q
    })
    
@lock
def facility_form_settings(request, facility, fsID, packetID, formLabel):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    if unlock:
        return redirect('IncompleteForms', facility)
    if client:
        userProfile = user_profile_model.objects.get(user=request.user)
        return redirect('c_dashboard', userProfile.facilityChoice.facility_name)
    selectedSettings = form_settings_model.objects.get(id=fsID)
    formData = Forms.objects.get(id=selectedSettings.formChoice.id)
    #NEEDS A FAIL MESSAGE
    #fsID = False
    print(formData.id)
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
        if 'facilitySelect' in request.POST.keys():
            return redirect('sup_dashboard', request.POST['facilitySelect'])
        else:
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
            newLabel, settingsDict = formSettingsFunc(keysList, request.POST, formData.id)
            print(f"This is the new label: {newLabel}")
            settingsChange = selectedSettings.settings
            settingsChange['settings'] = settingsDict
            if newLabel:
                settingsChange['packets'][str(packetID)] = newLabel
            copyPOST['settings'] = settingsChange
            formWData = form_settings_form(copyPOST, instance=selectedSettings)
            if formWData.is_valid():
                print('it fucking saved')
                A = formWData.save()
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
                return redirect('facilityList', 'supervisor')
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
        'facility': facility, 
        'unlock': unlock, 
        'client': client, 
        'supervisor': supervisor, 
        'formLabel': formLabel,
        'formData': formData,
        'formID': str(formData.id),
        'formSettings': formSettings,
        'packetSettings': packetSettings,
        'packetID': packetID
    })
    
@lock
def Add_Forms(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    if unlock:
        return redirect('IncompleteForms', facility)
    if client:
        return redirect('c_dashboard', facility)
    today = datetime.date.today()
    specificFacility = facility_model.objects.filter(facility_name=facility)[0]
    formList = Forms.objects.all().order_by('form')
    q = request.GET.get('q')
    if q:
        formList = formList.filter(
            Q(title__icontains=q) |
            Q(header__icontains=q)
        ).distinct()
    formSettingsModel = form_settings_model.objects.all()
    # packetQuery = the_packets_model.objects.get(name=packet, facilityChoice__facility_name=facility)
    print("-------------------------")
    print(formList[0].form)
    facilityFormsData = facility_forms_model.objects.filter(facilityChoice=specificFacility)
    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
    p = Paginator(formList, 15)
    page = request.GET.get('page')
    pageData = p.get_page(page)
    def doesSubExist(facilityLog, settingsID, selector, delete):
        settingsQuery = form_settings_model.objects.get(id=settingsID)
        if selector == "settingsID":
            formSubQuery = formSubmissionRecords_model.objects.filter(facilityChoice=facilityLog)
            subExists = False
            for formSub in formSubQuery:
                if settingsQuery.subChoice:
                    if formSub.id == settingsQuery.subChoice.id:
                        subExists = True
            if not subExists:
                newSub = formSubmissionRecords_model(
                    formID = settingsQuery.formChoice,
                    dateSubmitted = today - datetime.timedelta(days=9000),
                    dueDate = today - datetime.timedelta(days=5000),
                    facilityChoice = facilityLog,
                    submitted = False
                )
                newSub.save()
                settingsQuery.subChoice = newSub
                A = settingsQuery
                A.save()
            elif delete:
                toBeDeleted = formSubmissionRecords_model.objects.get(id=settingsQuery.subChoice.id)
                toBeDeleted.delete()
    #     elif selector =="list":

    if request.method == 'POST':
        answer = request.POST
        settingsDictData = json.loads(answer['form_settings'])
        if 'facilitySelect' in answer.keys():
            return redirect('sup_dashboard', answer['facilitySelect'])
        sameEntryNotif = False
        selectedList = []
        ## Builds the new list of forms selected and created a submission record for each
        selected_form_ids = settingsDictData.keys()
        for formID in selected_form_ids:
            formID = int(formID)
            formSettingsQuery = formSettingsModel.filter(facilityChoice=specificFacility, formChoice__form=formID)
            settingsDict = {"active": True, "packets": False, "settings":{}}
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

            keysList = []
            for setts in answer.keys():
                if len(setts.split("-")) > 1:
                    requestFormID = setts.split("-")[0]
                    if requestFormID == str(formID):
                        keysList.append(setts)
            if formID == 7:
                newLabel, settingsDict["settings"] = formSettingsFunc(keysList, request.POST, formID)


            print(settingsDict)
            settingsDict = json.loads(json.dumps(settingsDict))
            sameEntry = False
            if formSettingsQuery.exists():
                A = formSettingsQuery[0]
                #check if the settings are the same
                oldSettings = A.settings
                sameEntry = True
                for existInp in oldSettings:
                    for newInp in settingsDict:
                        if existInp == newInp:
                            if oldSettings[existInp] != settingsDict[newInp]:
                                sameEntry = False
            if not sameEntry:
                newSettings = form_settings_model(
                    facilityChoice = specificFacility,
                    formChoice = formList.get(id=formID),
                    settings = settingsDict,
                )
                newSettings.save()
                selectSettingID = newSettings.id
                print('made new form setting')
            else:
                selectSettingID = A.id
                sameEntryNotif = True
                
            doesSubExist(specificFacility, selectSettingID, "settingsID", False)
            selectedList.append(selectSettingID)
            print('made it')
        
        if facilityFormsData.exists():
            print(facilityFormsData[0].formData)
            returnFacList = changeStringListIntoList(facilityFormsData[0].formData)
            for oldForms in returnFacList:
                if int(oldForms) not in selectedList:
                    selectedList.append(int(oldForms))
        
        print(selectedList)
        B = facilityFormsData[0]
        B.formData = selectedList
        B.save()
    
        if sameEntryNotif:
            messages.error(request,"Some of the forms selected already exist for " + str(facility) + ".")
        
        messages.success(request,"All selected forms were added to " + str(facility) + ".")
        print("Forms Have Been Saved")
        return redirect('facilityList', 'supervisor')
    return render(request, 'supervisor/facilityForms/add_form_to_facility.html', {
        'notifs': notifs, 
        'facility': facility, 
        'unlock': unlock, 
        'client': client, 
        'supervisor': supervisor, 
        'formList': formList,
        'pageData': pageData,
        'query': q
    })
