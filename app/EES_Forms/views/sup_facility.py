from django.shortcuts import render, redirect
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..models import bat_info_model, user_profile_model, facility_forms_model, Forms, formSubmissionRecords_model, packets_model, form_settings_model
from ..forms import facility_forms_form, packets_form
import ast
from django.contrib.auth.decorators import login_required
import datetime
from ..utils import setUnlockClientSupervisor, checkIfFacilitySelected, getCompanyFacilities, get_facility_forms
import json
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
    
    packetData = packets_model.objects.all()
    packetForm = packets_form
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
                    found = True
        if found:
            newFacList.append((facil, facilityForms))
        else:
            newFacList.append((facil, []))
        
    finalList = []
    for newFac in newFacList:
        if len(newFac[1]) > 0:
            labelList = []
            for label in newFac[1]:
                for singleForm in formData:
                    if label[0] == singleForm.id:
                        labelList.append((label[0], label[1], singleForm.header + ' - ' + singleForm.title, singleForm))
            def myFunc(e):
                return e[1]
            labelList.sort(key=myFunc)
            
            finalList.append((newFac[0], labelList))
        else:
            finalList.append((newFac[0], newFac[1]))
    print(packetData[0].formList)
    
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
    print(facility)
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
    packetQuery = packets_model.objects.get(name=packet, facilityChoice__facility_name=facility)
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
    if facilityFormsData.exists:
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
def facility_form_settings(request, facility, packetID, formID, formLabel):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    if unlock:
        return redirect('IncompleteForms', facility)
    if client:
        return redirect('c_dashboard', facility)
    formData = Forms.objects.get(id=formID)
    packetSettings = packets_model.objects.get(id=packetID)
    for form in packetSettings.formList:
        if form == formLabel:
            settingsID = packetSettings.formList[form]['settingsID']
            break
    formSettings = form_settings_model.objects.get(id=settingsID).settings
    
    
    return render (request, 'supervisor/facilityForms/facilityFormSettings.html', {
        'notifs': notifs,
        'facility': facility, 
        'unlock': unlock, 
        'client': client, 
        'supervisor': supervisor, 
        'formLabel': formLabel,
        'formData': formData,
        'formID': int(formID),
        'formSettings': formSettings,
        'packetSettings': packetSettings
    })
    