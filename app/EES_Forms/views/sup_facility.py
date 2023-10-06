from django.shortcuts import render, redirect
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..models import bat_info_model, user_profile_model, facility_forms_model, Forms, formSubmissionRecords_model
from ..forms import facility_forms_form
from EES_Forms.views.supervisor_view import getCompanyFacilities
import ast
from django.contrib.auth.decorators import login_required
import datetime
lock = login_required(login_url='Login')

@lock
def facilityList(request, facility):
    unlock = False
    client = False
    supervisor = False
    if request.user.groups.filter(name=OBSER_VAR):
        unlock = True
        return redirect('IncompleteForms', facility)
    if request.user.groups.filter(name=CLIENT_VAR):
        client = True
        return redirect('c_dashboard', facility)
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    userProfData = user_profile_model.objects.all().filter(user__username=request.user.username)[0]
    facList = bat_info_model.objects.all().filter(company__company_name=userProfData.company.company_name).order_by('facility_name')
    facData = facility_forms_model.objects.all()
    formData = Forms.objects.all()
    sortedFacilityData = getCompanyFacilities(request.user.username)
    
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
                        labelList.append((label[0], label[1], singleForm.header + ' - ' + singleForm.title))
            def myFunc(e):
                return e[1]
            labelList.sort(key=myFunc)
            
            finalList.append((newFac[0], labelList))
    return render(request, 'supervisor/sup_facilityList.html', {
        'sortedFacilityData': sortedFacilityData, 'facility': facility, 'unlock': unlock, 'client': client, 'supervisor': supervisor, 'facilities': finalList
    })

@lock    
def facilityForm(request, facility):
    unlock = False
    client = False
    supervisor = False
    if request.user.groups.filter(name=OBSER_VAR):
        unlock = True
        return redirect('IncompleteForms', facility)
    if request.user.groups.filter(name=CLIENT_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    existing = False
    modelList = ''
    today = datetime.date.today()
    specificFacility = bat_info_model.objects.filter(facility_name=facility)[0]
    formList = Forms.objects.all().order_by('form')
    facilityFormsData = facility_forms_model.objects.filter(facilityChoice=specificFacility)
    sortedFacilityData = getCompanyFacilities(request.user.username)
    if len(facilityFormsData) > 0:
        if facilityFormsData[0].formData:
            facilityFormsData = ast.literal_eval(facilityFormsData[0].formData[1:-1])
        existing = True
    
    if existing:
        modelList = facilityFormsData
        replaceModel = facility_forms_model.objects.get(facilityChoice=specificFacility)
    # for x in modelList:
    #     for forms in formList:
    #         print(isinstance(forms.id, int))
            #print(isinstance(x[0], int))
            #if forms.id == x[0]:
                #print("it match tho")
                

    if request.method == 'POST':
        existingSub = formSubmissionRecords_model.objects.filter(facilityChoice=specificFacility)
        existingSub.delete()
        
        selectedList = []
        print(len(formList))
        print(request.POST)
        for item in range(len(formList)):
            formIDlabel = 'forms' + str(item + 1)
            formOrgLabel = 'formID' + str(item + 1)
            try:
                
                formID = int(request.POST[formIDlabel.replace(" ", "")])
                fromOrg = request.POST[formOrgLabel.replace(" ", "")].upper()
                
                selectedList.append((formID,fromOrg))    
                    
                newSub = formSubmissionRecords_model(
                    formID = formID,
                    dateSubmitted = today - datetime.timedelta(days=9000),
                    dueDate = today - datetime.timedelta(days=5000),
                    facilityChoice = specificFacility,
                    submitted = False
                )
                newSub.save()
            except:
                continue
        
        dataCopy = request.POST.copy()
        dataCopy['formData'] = selectedList
        dataCopy['facilityChoice'] = specificFacility
        print(dataCopy)
        if existing:
            form = facility_forms_form(dataCopy, instance=replaceModel)
        else:
            form = facility_forms_form(dataCopy)
            
            
        if form.is_valid():
            form.save()
            return redirect('facilityList', facility)
    return render (request, 'supervisor/facilityForms.html', {
        'sortedFacilityData': sortedFacilityData, 'facility': facility, 'unlock': unlock, 'client': client, 'supervisor': supervisor, 'formList': formList, 'modelList': modelList,
    })