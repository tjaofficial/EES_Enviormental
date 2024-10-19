from django.shortcuts import render, redirect # type: ignore
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..models import bat_info_model, user_profile_model, facility_forms_model, Forms, formSubmissionRecords_model, form_settings_model, the_packets_model
from ..forms import the_packets_form, form_settings_form
from django.contrib.auth.decorators import login_required # type: ignore
import datetime
import json
from .form_settings_builds import form1settings, form2settings, form3settings, form4settings, form5settings, form6settings, form7settings, form8settings, form9settings, form17settings, form18settings, form19settings, form20settings, form21settings
from ..utils import setUnlockClientSupervisor, checkIfFacilitySelected, getCompanyFacilities, get_facility_forms, changeStringListIntoList
from django.db.models import Q # type: ignore
from django.core.paginator import Paginator # type: ignore
from django.contrib import messages # type: ignore
lock = login_required(login_url='Login')

@lock
def facilityList(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    if unlock:
        return redirect('IncompleteForms', facility)
    if client:
        return redirect('c_dashboard', facility)
    userProfData = user_profile_model.objects.get(user__username=request.user.username)
    facList = bat_info_model.objects.filter(company__company_name=userProfData.company.company_name).order_by('facility_name')
    facData = facility_forms_model.objects.all()
    formData = Forms.objects.all()
    sortedFacilityData = getCompanyFacilities(request.user.username)
    formSettingsModelOG = form_settings_model.objects.all()
    packetData = the_packets_model.objects.all()
    packetForm = the_packets_form

    newFacList = []
    for facil in facList:
        facilityForms = get_facility_forms('facilityID', facil.id)
        newFacList.append((facil, facilityForms))
    print(newFacList)
    finalList = []
    for newFac in newFacList:
        formSettingsModel = formSettingsModelOG.filter(facilityChoice__id=newFac[0].id)
        if len(newFac[1]) > 0:
            labelList = []
            for label in newFac[1]:
                for formSettings in formSettingsModel:
                    if int(label) == formSettings.id:
                        labelList.append((formSettings))
                # labelList.append((label, label, singleForm.header + ' - ' + singleForm.title, singleForm))
                # for singleForm in formData:
                #     if label == singleForm.id:
            def myFunc(e):
                return e.id
            labelList.sort(key=myFunc)
            
            finalList.append((newFac[0], labelList))
        else:
            finalList.append((newFac[0], newFac[1]))
    if request.method == 'POST':
        answer = request.POST
        print(answer)
        if 'facilitySelect' in answer.keys():
            return redirect('sup_dashboard', answer['facilitySelect'])
        elif 'newPacket' in answer.keys():
            dataCopy = answer.copy()
            facChoice = bat_info_model.objects.get(id=int(answer['facilityID']))
            dataCopy['facilityChoice'] = facChoice
            dataCopy['frequency'] = 'Weekly'
            packetFormData = packetForm(dataCopy)
            print(packetFormData.errors)
            if packetFormData.is_valid():
                packetFormData.save()
            print(request.POST)
            print('hello')
        elif 'sub_delete' in answer.keys():
            print('delete-packet')
            packToDelete = packetData.get(id=answer['packID'])
            print(packToDelete)
            formSettingsQuery = form_settings_model.objects.filter(facilityChoice__id=packToDelete.facilityChoice.id)
            if len(packToDelete.formList["formsList"]) == 0:
                for pacForms in packToDelete.formList["formsList"]:
                    for formSettingsEntry in formSettingsQuery:
                        if packToDelete.formList["formsList"][pacForms]['settingsID'] == formSettingsEntry.id:
                            del formSettingsEntry.settings['packets'][str(packToDelete.id)]
                            formSettingsEntry.save()
                packToDelete.delete()
            return redirect(facilityList, facility)
        elif 'facForm_delete' in answer.keys():
            facFormID = answer['facFormID']
            facID = answer['facID']
            #delete from all packets
            for pac in packetData.filter(facilityChoice__id=facID):
                deleteList = []
                for setList in pac.formList["formsList"]:
                    if facFormID == pac.formList["formsList"][setList]['settingsID']:
                        print('check 1')
                        if setList not in deleteList:
                            print('check 2')
                            deleteList.append(setList)
                print(deleteList)
                for delForm in deleteList:
                    print(pac.formList["formsList"])
                    print(pac.formList["formsList"][delForm])
                    del pac.formList["formsList"][delForm]
                    finalDelete = pac
                    finalDelete.save()
            #delete form facility forms model
            thisFacilityForm = facData.get(facilityChoice__id=facID)
            makeFacFormsList = changeStringListIntoList(thisFacilityForm.formData)
            print(makeFacFormsList)
            for ids in makeFacFormsList:
                print(ids)
                if int(ids) ==  int(facFormID):
                    makeFacFormsList.remove(ids)
            thisFacilityForm.formData = makeFacFormsList
            facilityFormDelete = thisFacilityForm
            facilityFormDelete.save()
            #Change acive from "true" to 'false' to archive form from settings model
            formToDelete = formSettingsModelOG.get(id=facFormID)
            formToDelete.settings['active'] = "false"
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
            thePacket.formList["formsList"][formNoLabelParse] = {"settingsID":int(fsID)}
            settingsEntry = form_settings_model.objects.get(id=int(fsID))
            settingsEntry.settings['packets'][str(thePacket.id)] = formNoLabelParse
            A = thePacket
            B = settingsEntry
            A.save()
            B.save()
            print('Updating Packet')
            messages.success(request,"The selected form has been added to the packet.")
        elif 'pack_settings' in answer.keys():
            packEntry = packetData.get(id=answer['packID'])
            packEntry.frequency = answer['frequency']
            packEntry.name = answer['name']
            packEntry.save()
            return redirect(facilityList, facility)
    return render(request, 'supervisor/sup_facilityList.html', {
        'notifs': notifs, 
        'sortedFacilityData': sortedFacilityData, 
        'facility': facility, 
        'unlock': unlock, 
        'client': client, 
        'supervisor': supervisor, 
        'facilities': finalList,
        'packetData': packetData,
        'packetForm': packetForm,
        'formData': formData,
        'formSettingsModel': formSettingsModelOG,
    })

@lock    
def facilityForm(request, facility, packet):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    if unlock:
        return redirect('IncompleteForms', facility)
    today = datetime.date.today()
    q = request.GET.get('q')
    specificFacility = bat_info_model.objects.filter(facility_name=facility)[0]
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
    
    sortedFacilityData = getCompanyFacilities(request.user.username)
    p = Paginator(newFormList, 15)
    page = request.GET.get('page')
    pageData = p.get_page(page)

    print("-------------------------")
    print(formList[0].form)

    if request.method == 'POST':
        answer = request.POST
        print(answer)
        #for all selected and fille in save as a dictionary for the packet
        if 'facilitySelect' in answer.keys():
            return redirect('sup_dashboard', answer['facilitySelect'])
        selectedList = {}
        ## Builds the new list of forms selected and created a submission record
        fsIDsFromInputs = []
        for allKeys in answer.keys():
            if allKeys[:5] == 'forms':
                inputID = allKeys[5:]
                fsIDsFromInputs.append(answer['settingsID'+inputID])
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
                
                selectedList[formLabel] = {"settingsID": settingsID}
                print('made it')
                settingsEntry = form_settings_model.objects.get(id=settingsID)
                settingsEntryPacks = settingsEntry.settings["packets"]
                print(settingsEntryPacks.keys())
                print(packetQuery.id)
                
                settingsEntryPacks[str(packetQuery.id)] = formLabel
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
        'packetFormList': packetQuery.formList["formsList"],
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
    #fsID = False
    print(formData.id)
    if packetID[:5] != 'facID':
        packetSettings = the_packets_model.objects.get(id=packetID)
    else:
        packetSettings = False
    
    if formLabel != 'none':
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
            if formData.id == 1:
                settingsDict = form1settings(keysList, request.POST)
            elif formData.id == 2:
                settingsDict = form2settings(keysList, request.POST)
            elif formData.id == 3:
                settingsDict = form3settings(keysList, request.POST)
            elif formData.id == 4:
                settingsDict = form4settings(keysList, request.POST)
            elif formData.id == 5:
                settingsDict = form5settings(keysList, request.POST)
            elif formData.id == 6:
                settingsDict = form6settings(keysList, request.POST)
            elif formData.id == 7:
                settingsDict = form7settings(keysList, request.POST)
            elif formData.id == 8:
                settingsDict = form8settings(keysList, request.POST)
            elif formData.id == 9:
                settingsDict = form9settings(keysList, request.POST)
            elif formData.id == 17:
                settingsDict = form17settings(keysList, request.POST)
            elif formData.id == 18:
                settingsDict = form18settings(keysList, request.POST)
            elif formData.id == 19:
                settingsDict = form19settings(keysList, request.POST)
            elif formData.id == 20:
                settingsDict = form20settings(keysList, request.POST)
            elif formData.id == 21:
                settingsDict = form21settings(keysList, request.POST)
            settingsChange = selectedSettings.settings
            settingsChange['settings'] = settingsDict
            copyPOST['settings'] = settingsChange
            formWData = form_settings_form(copyPOST, instance=selectedSettings)
            if formWData.is_valid():
                print('it fucking saved')
                formWData.save()
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
        'formID': int(formData.id),
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
    specificFacility = bat_info_model.objects.filter(facility_name=facility)[0]
    q = request.GET.get('q')
    formList = Forms.objects.all().order_by('form')
    totalAmountofForms = len(formList)
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
    sortedFacilityData = getCompanyFacilities(request.user.username)
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
    
    # def doesSubExist(facilityLog, value, selector, delete):
    #     if selector =="list":   
    #         for x in value:
    #             for formData in Forms.objects.all():
    #                 if formData.id == x[0]:
    #                     if not formSubmissionRecords_model.objects.filter(formID=formData, facilityChoice=facilityLog).exists():
    #                         newSub = formSubmissionRecords_model(
    #                             formID = formData,
    #                             dateSubmitted = today - datetime.timedelta(days=9000),
    #                             dueDate = today - datetime.timedelta(days=5000),
    #                             facilityChoice = facilityLog,
    #                             submitted = False
    #                         )
    #                         newSub.save()
    #                     elif delete:
    #                         toBeDeleted = formSubmissionRecords_model.objects.get(formID=formData, facilityChoice=facilityLog)
    #                         toBeDeleted.delete()
    #                     break
                    
    if request.method == 'POST':
        answer = request.POST
        print(answer)
        if 'facilitySelect' in answer.keys():
            return redirect('sup_dashboard', answer['facilitySelect'])
        sameEntryNotif = False
        selectedList = []
        ## Builds the new list of forms selected and created a submission record for each
        for item in range(1, totalAmountofForms+1):
            formInputName = 'forms' + str(item)
            if formInputName.replace(" ", "") in answer.keys():
                formID = int(answer[formInputName.replace(" ", "")])
                formSettingsQuery = formSettingsModel.filter(facilityChoice=specificFacility, formChoice=formList.get(id=formID))
                settingsDict = {"active": "true", "packets":{}, "settings":{}}
                for x in answer.keys():
                    if len(x.split("-")) > 1:
                        requestFormID = x.split("-")[0]
                        requestInputName = x.split("-")[1]
                        if requestFormID == str(formID):
                            settingsDict["settings"][requestInputName] = answer[x]

                keysList = []
                for setts in answer.keys():
                    if len(setts.split("-")) > 1:
                        requestFormID = setts.split("-")[0]
                        if requestFormID == str(formID):
                            keysList.append(setts)
                if formID == 7:
                    settingsDict["settings"] = form7settings(keysList, request.POST)


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
            else:
                continue
            
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