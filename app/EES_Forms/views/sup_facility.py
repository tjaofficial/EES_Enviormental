from django.shortcuts import render, redirect
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..models import bat_info_model, user_profile_model, facility_forms_model, Forms, formSubmissionRecords_model, form_settings_model, the_packets_model
from ..forms import facility_forms_form, the_packets_form, form_settings_form
import ast
from django.contrib.auth.decorators import login_required
import datetime
from ..utils import setUnlockClientSupervisor, checkIfFacilitySelected, getCompanyFacilities, get_facility_forms
import json
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
lock = login_required(login_url='Login')

@lock
def facilityList(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    if unlock:
        return redirect('IncompleteForms', facility)
    if client:
        return redirect('c_dashboard', facility)
    userProfData = user_profile_model.objects.get(user__username=request.user.username)
    facList = bat_info_model.objects.filter(company__company_name=userProfData.company.company_name).order_by('facility_name')
    facData = facility_forms_model.objects.all()
    formData = Forms.objects.all()
    sortedFacilityData = getCompanyFacilities(request.user.username)
    formSettingsModel = form_settings_model.objects.all()
    packetData = the_packets_model.objects.all()
    packetForm = the_packets_form

    #print(bat_info_model.objects.get(facility_name=facility))
    
    #facilityID = bat_info_model.objects.get(company__company_name=userProfData.company.company_name, facility_name=facility).id
    
    #facilityFormsList = get_facility_forms(facilityID)
    newFacList = []
    for facil in facList:
        found = False
        for line in facData:
            if facil == line.facilityChoice:
                if line.formData:
                    facilityForms = ast.literal_eval(line.formData)
                    print(facilityForms)
                    found = True
        if found:
            newFacList.append((facil, facilityForms))
        else:
            newFacList.append((facil, []))

    finalList = []
    for newFac in newFacList:
        formSettingsModel = formSettingsModel.filter(facilityChoice=newFac[0])
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
    print(finalList)
    if request.method == 'POST':
        answer = request.POST
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
            packToDelete = packetData.get(id=answer['packID'])
            packToDelete.delete()
            return redirect(facilityList, facility)
        elif 'packet_update' in answer.keys():
            #receiving fsID and packetID in format of "27-6"
            print(answer['packet_update'])
            dataReceived = answer['packet_update'].split("-")
            fsID = dataReceived[0]
            packetID = dataReceived[1]
            thePacket = packetData.get(id=packetID)
            theSettings = formSettingsModel.get(id=fsID)
            highestLabelNumb = 0
            for label in thePacket.formList.keys():
                noLabelTag = label[:9]
                noLabelNumber = label[9:]
                if noLabelTag == "no-label-":
                    if int(noLabelNumber) > int(highestLabelNumb):
                        highestLabelNumb = noLabelNumber
            thePacket.formList["no-label-"+str(int(highestLabelNumb)+1)] = {"formID":theSettings.formChoice.id, "settingsID":fsID}
            A = thePacket
            A.save()
            print('Updating Packet')
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
    })

@lock    
def facilityForm(request, facility, packet):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    if unlock:
        return redirect('IncompleteForms', facility)
    existing = False
    modelList = ''
    today = datetime.date.today()
    specificFacility = bat_info_model.objects.filter(facility_name=facility)[0]
    formList = Forms.objects.all().order_by('form')
    formSettingsModel = form_settings_model.objects.all()
    packetQuery = the_packets_model.objects.get(name=packet, facilityChoice__facility_name=facility)
    print("-------------------------")
    print(formList[0].form)
    facilityFormsData = facility_forms_model.objects.filter(facilityChoice=specificFacility)
    sortedFacilityData = getCompanyFacilities(request.user.username)
    
    def doesSubExist(facilityLog, value, selector, delete):
        if selector == "formID":
            for formData in Forms.objects.all():
                if formData.id == value:
                    if not formSubmissionRecords_model.objects.filter(formID=formData, facilityChoice=facilityLog).exists():
                        newSub = formSubmissionRecords_model(
                            formID = formData,
                            dateSubmitted = today - datetime.timedelta(days=9000),
                            dueDate = today - datetime.timedelta(days=5000),
                            facilityChoice = facilityLog,
                            submitted = False
                        )
                        newSub.save()
                    elif delete:
                        toBeDeleted = formSubmissionRecords_model.objects.get(formID=formData, facilityChoice=facilityLog)
                        toBeDeleted.delete()
                    break
                
        elif selector =="list":   
            for x in value:
                for formData in Forms.objects.all():
                    if formData.id == x[0]:
                        if not formSubmissionRecords_model.objects.filter(formID=formData, facilityChoice=facilityLog).exists():
                            newSub = formSubmissionRecords_model(
                                formID = formData,
                                dateSubmitted = today - datetime.timedelta(days=9000),
                                dueDate = today - datetime.timedelta(days=5000),
                                facilityChoice = facilityLog,
                                submitted = False
                            )
                            newSub.save()
                        elif delete:
                            toBeDeleted = formSubmissionRecords_model.objects.get(formID=formData, facilityChoice=facilityLog)
                            toBeDeleted.delete()
                        break
    if facilityFormsData.exists():
        if facilityFormsData[0].formData:
            facilityFormsData = ast.literal_eval(facilityFormsData[0].formData[1:-1])
        else:
            facilityFormsData = []
        existing = True
    
    if existing:
        modelList = facilityFormsData
        replaceModel = facility_forms_model.objects.get(facilityChoice=specificFacility)

    
    if request.method == 'POST':
        answer = request.POST
        print(answer)
        #for all selected and fille in save as a dictionary for the packet
        if 'facilitySelect' in answer.keys():
            return redirect('sup_dashboard', answer['facilitySelect'])
        selectedList = {}
        ## Builds the new list of forms selected and created a submission record
        for item in range(1, len(formList)):
            formIDlabel = 'forms' + str(item)
            formOrgLabel = 'formID' + str(item)
            
            if formIDlabel.replace(" ", "") in answer.keys():
                formID = int(answer[formIDlabel.replace(" ", "")])
                formLabel = answer[formOrgLabel.replace(" ", "")].upper()
                formSettingsQuery = formSettingsModel.filter(facilityChoice=specificFacility, formChoice=formList.get(id=formID), packetChoice=packetQuery)
                settingsDict = {}
                for x in answer.keys():
                    if x[0] == str(formID):
                        settingsDict[x[1:]] = answer[x]
                print(settingsDict)
                if formSettingsQuery.exists():
                    A = formSettingsQuery[0]
                    A.settings = settingsDict
                    A.save()
                    selectSettingID = A.id
                    print('updated')
                else:
                    newSettings = form_settings_model(
                        facilityChoice = specificFacility,
                        formChoice = formList.get(id=formID),
                        settings = settingsDict,
                        packetChoice = packetQuery
                    )
                    newSettings.save()
                    selectSettingID = newSettings.id
                    print('made new')
                
                doesSubExist(specificFacility, formID, "formID", False)
                
                selectedList[formLabel] = {"formID": formID,"settingsID": selectSettingID}
                print('made it')
            else:
                continue
        
        packetQuery.formList = selectedList
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
        'modelList': modelList,
        'packet': packet,
        'packetQuery': packetQuery.formList,
        'formSettingsModel': formSettingsModel
    })
    
@lock
def facility_form_settings(request, facility, fsID, packetID, formLabel):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    if unlock:
        return redirect('IncompleteForms', facility)
    if client:
        return redirect('c_dashboard', facility)
    selectedSettings = form_settings_model.objects.get(id=fsID)
    formData = Forms.objects.get(id=selectedSettings.formChoice.id)
    #fsID = False
    if packetID[:5] != 'facID':
        packetSettings = the_packets_model.objects.get(id=packetID)
    else:
        packetSettings = False
    
    if formLabel != 'none':
        for form in packetSettings.formList:
            if form == formLabel:
                settingsID = packetSettings.formList[form]['settingsID']
                break
                
    formSettings = selectedSettings.settings
    if request.method == "POST":
        if 'facilitySelect' in request.POST.keys():
            return redirect('sup_dashboard', request.POST['facilitySelect'])
        copyPOST = request.POST.copy()
        copyPOST['facilityChoice'] = selectedSettings.facilityChoice
        copyPOST['formChoice'] = selectedSettings.formChoice
        copyPOST['settings'] = formSettings
        for inputs in request.POST.keys():
            if inputs[:9] == "settings_":
                settingsName = inputs[9:]
                copyPOST['settings'][settingsName] = request.POST[inputs]
                
        formWData = form_settings_form(copyPOST, instance=selectedSettings)
        if formWData.is_valid():
            formWData.save()
            messages.success(request,"Form XXX was updated.")
            return redirect('facilityList', 'supervisor')
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
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    if unlock:
        return redirect('IncompleteForms', facility)
    if client:
        return redirect('c_dashboard', facility)
    
    
    existing = False
    modelList = ''
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
    def doesSubExist(facilityLog, value, selector, delete):
        if selector == "formID":
            for formData in Forms.objects.all():
                if formData.id == value:
                    if not formSubmissionRecords_model.objects.filter(formID=formData, facilityChoice=facilityLog).exists():
                        newSub = formSubmissionRecords_model(
                            formID = formData,
                            dateSubmitted = today - datetime.timedelta(days=9000),
                            dueDate = today - datetime.timedelta(days=5000),
                            facilityChoice = facilityLog,
                            submitted = False
                        )
                        newSub.save()
                    elif delete:
                        toBeDeleted = formSubmissionRecords_model.objects.get(formID=formData, facilityChoice=facilityLog)
                        toBeDeleted.delete()
                    break
                
        elif selector =="list":   
            for x in value:
                for formData in Forms.objects.all():
                    if formData.id == x[0]:
                        if not formSubmissionRecords_model.objects.filter(formID=formData, facilityChoice=facilityLog).exists():
                            newSub = formSubmissionRecords_model(
                                formID = formData,
                                dateSubmitted = today - datetime.timedelta(days=9000),
                                dueDate = today - datetime.timedelta(days=5000),
                                facilityChoice = facilityLog,
                                submitted = False
                            )
                            newSub.save()
                        elif delete:
                            toBeDeleted = formSubmissionRecords_model.objects.get(formID=formData, facilityChoice=facilityLog)
                            toBeDeleted.delete()
                        break
    if request.method == 'POST':
        answer = request.POST
        print(answer)
        if 'facilitySelect' in answer.keys():
            return redirect('sup_dashboard', answer['facilitySelect'])
        sameEntryNotif = False
        selectedList = []
        ## Builds the new list of forms selected and created a submission record for each
        for item in range(1, totalAmountofForms):
            formInputName = 'forms' + str(item)
            
            if formInputName.replace(" ", "") in answer.keys():
                formID = int(answer[formInputName.replace(" ", "")])
                formSettingsQuery = formSettingsModel.filter(facilityChoice=specificFacility, formChoice=formList.get(id=formID))
                settingsDict = {}
                for x in answer.keys():
                    print(answer.keys())
                    print(x)
                    print(x[0])
                    if x[0] == str(formID):
                        settingsDict[x[1:]] = answer[x]
                print(settingsDict)
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
                    
                
                doesSubExist(specificFacility, formID, "formID", False)
                
                #selectedList[formLabel] = {"formID": formID,"settingsID": selectSettingID}
                selectedList.append(selectSettingID)
                print('made it')
            else:
                continue
            
            if facilityFormsData.exists():
                if facilityFormsData[0].formData:
                    facilityFormsData2 = ast.literal_eval(facilityFormsData[0].formData[1:-1])
                else:
                    facilityFormsData2 = []
            for oldForms in facilityFormsData2:
                if oldForms not in selectedList:
                    selectedList.append(oldForms)
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