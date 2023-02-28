from django.shortcuts import render, redirect
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..models import bat_info_model, user_profile_model, facility_forms_model, Forms
from ..forms import facility_forms_form

def facilityList(request, facility):
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
    userProfData = user_profile_model.objects.all().filter(user__username=request.user.username)[0]
    facList = bat_info_model.objects.all().filter(company__company_name=userProfData.company.company_name).order_by('facility_name')
        
    return render(request, 'supervisor/sup_facilityList.html', {
        'facility': facility, 'unlock': unlock, 'client': client, 'supervisor': supervisor, 'facilities': facList
    })
    
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
    options = bat_info_model.objects.all().filter(facility_name=facility)[0]
    formList = Forms.objects.all()
    facilityForms = facility_forms_model.objects.all().filter(facilityChoice=options)
    
    if len(facilityForms) > 0:
        facilityForms = facilityForms[0].formData[1:-1].replace("'", "").replace(" ", "").split(",")
        existing = True
    
    if existing:
        modelList = facilityForms
    
    if request.method == 'POST':
        selectedList = []
        for item in range((len(request.POST) - 1)):
            selectedList.append(request.POST['forms' + str(item + 1)].replace(" ", "")) 
        dataCopy = request.POST.copy()
        dataCopy['formData'] = selectedList
        dataCopy['facilityChoice'] = options
        
        form = facility_forms_form(dataCopy)
        
        if form.is_valid():
            form.save()
        
        
    return render (request, 'supervisor/facilityForms.html', {
        'facility': facility, 'unlock': unlock, 'client': client, 'supervisor': supervisor, 'formList': formList, 'modelList': modelList,
    })