from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.apps import apps
from ..models import Forms, bat_info_model, facility_forms_model
from django.core.exceptions import FieldError
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from EES_Forms.views.supervisor_view import getCompanyFacilities
import ast
from ..utils import Calendar
import datetime

lock = login_required(login_url='Login')

@lock
def printSelect(request, facility):
    options = bat_info_model.objects.all()
    alertMessage = ''
    unlock = False
    client = False
    supervisor = False
    
    if request.user.groups.filter(name=OBSER_VAR):
        unlock = True
    if request.user.groups.filter(name=CLIENT_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    
    sortedFacilityData = getCompanyFacilities(request.user.username)
    facilityForms = facility_forms_model.objects.all().filter(facilityChoice__facility_name=facility)
    if len(facilityForms) == 0:
        selectList = []
        print('No facility forms have been assigned/No facility has been selected')
    else:
        print('something is in here')
        facilityForms = facilityForms[0]
        parseList = ast.literal_eval(facilityForms.formData)
        newFormList = []
        for theForm in parseList:
            searchName = theForm.split('--')[1]
            newFormList.append(searchName)
        formList = Forms.objects.all().order_by('form')
        selectList = []
        print(newFormList)
        for x in formList:
            if x.title in newFormList:
                selectList.append([x.form, x.form.replace(' ', '_').replace('-','').lower()])

    if request.method == "POST":
        print(request.POST["monthSel"])
        inputDate = datetime.datetime.strptime(request.POST["monthSel"], "%Y-%m").date()
        if request.POST['type'] == 'single':
            return redirect("CalSelect", facility, request.POST['type'], request.POST['forms'], inputDate.year, inputDate.month)
        elif request.POST['type'] == "group":
            return redirect("CalSelect", facility, request.POST['type'], request.POST['formGroups'])
            
        try:
            if request.POST['forms'] != '':
                if 1 <= len(request.POST['forms']) <= 2:
                    formCheck = 'form' + request.POST['forms'].capitalize() + '_model'
                elif len(request.POST['forms']) > 2:
                    formCheck = request.POST['forms'] + '_model'
                else:
                    print('something is wrong')
                mainModel = apps.get_model('EES_Forms', formCheck)
                    
                try:
                    filtered = mainModel.objects.filter(date=request.POST['formDate'])
                except FieldError as e:
                    filtered = mainModel.objects.filter(week_start=request.POST['formDate'])
                
                if len(filtered) == 0:
                    alertMessage = '*FORM DOES NOT EXIST PLEASE SELECT ANOTHER DATE*'
                else:
                    alertMessage = ''
            
            typeFormDate = '/' + request.POST['type'] + '-' + request.POST['formDate']
                
            if request.POST['forms'] == '' and request.POST['formGroups'] != '':
                formGroups = '/' + request.POST['formGroups']
                craftUrl = 'printIndex' + formGroups + typeFormDate
            elif request.POST['formGroups'] == '' and request.POST['forms'] != '':
                forms = '/' + request.POST['forms'].capitalize()
                craftUrl = 'printIndex' + forms + typeFormDate

            return redirect(craftUrl)
        except:
            answer = request.POST
            if answer['facilitySelect'] != '':
                return redirect('PrintSelect', answer['facilitySelect'])
            
    
    return render(request, "shared/printSelect.html", {
        'sortedFacilityData': sortedFacilityData, 'options': options, 'facility': facility, 'selectList': selectList, 'supervisor': supervisor, "client": client, 'unlock': unlock, 'alertMessage': alertMessage,
    })