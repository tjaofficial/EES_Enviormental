from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.apps import apps # type: ignore
from ..models import facility_model, the_packets_model
from ..forms import *
from django.core.exceptions import FieldError # type: ignore
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
import json
from ..utils import checkIfFacilitySelected, getCompanyFacilities, get_facility_forms
import datetime

lock = login_required(login_url='Login')

@lock
def printSelect(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    options = facility_model.objects.all()
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
    formSettingsQuery = form_settings_model.objects.filter(facilityChoice__facility_name=facility)
    packetQuery = the_packets_model.objects.filter(facilityChoice__facility_name=facility)
    sortedFacilityData = getCompanyFacilities(request.user.username)
    facilityForms = get_facility_forms('facilityName', facility)
    selectList = []
    fsList = []
    for fs in formSettingsQuery:
        labelList = []
        for label in fs.settings['packets']:
            labelList.append((fs.settings['packets'][label], int(label)))
        fsList.append((fs.id, labelList))
    formSettingsQueryJson = json.dumps(fsList)
    if len(facilityForms) == 0:
        print('No facility forms have been assigned/No facility has been selected')
    else:
        print('something is in here')
        for fsID in facilityForms:
            for settingsEntry in formSettingsQuery:
                if int(fsID) == settingsEntry.id:
                    selectList.append(settingsEntry)

    if request.method == "POST":
        answer = request.POST
        if 'facilitySelect' in answer.keys():
            if answer['facilitySelect'] != '':
                return redirect('PrintSelect', answer['facilitySelect'])
        inputDate = datetime.datetime.strptime(answer["monthSel"], "%Y-%m").date()
        forms  = request.POST['forms']
        if answer['type'] == 'single':
            print('HFLSKDJFLSKJDFLKSJDF--------')
            print(forms)
            if int(forms) == 23:
                print('yes its 23')
                formDate = answer['monthSel']
                formGroup = 'single'
                formIdentity = forms
                
                return redirect('printIndex', facility, formGroup, formIdentity, formDate)
            if str(answer['formLabels']) == str(forms):
                return redirect("CalSelect", facility, answer['type'], forms, inputDate.year, inputDate.month)
            else:
                forms = str(forms) + '-' + str(answer['formLabels'])
                return redirect("CalSelect", facility, answer['type'], forms, inputDate.year, inputDate.month)
        elif answer['type'] == "group":
            return redirect("CalSelect", facility, answer['type'], answer['formGroups'], inputDate.year, inputDate.month)
            
        try:
            if forms != '':
                if 1 <= len(forms) <= 2:
                    formCheck = 'form' + forms.capitalize() + '_model'
                elif len(forms) > 2:
                    formCheck = forms + '_model'
                else:
                    print('something is wrong')
                mainModel = apps.get_model('EES_Forms', formCheck)
                    
                try:
                    filtered = mainModel.objects.filter(date=answer['formDate'])
                except FieldError as e:
                    filtered = mainModel.objects.filter(week_start=answer['formDate'])
                
                if len(filtered) == 0:
                    alertMessage = '*FORM DOES NOT EXIST PLEASE SELECT ANOTHER DATE*'
                else:
                    alertMessage = ''
            
            typeFormDate = '/' + answer['type'] + '-' + answer['formDate']
                
            if forms == '' and answer['formGroups'] != '':
                formGroups = '/' + answer['formGroups']
                craftUrl = 'printIndex' + formGroups + typeFormDate
            elif answer['formGroups'] == '' and forms != '':
                forms = '/' + forms.capitalize()
                craftUrl = 'printIndex' + forms + typeFormDate

            return redirect(craftUrl)
        except:
            answer = request.POST
            if answer['facilitySelect'] != '':
                return redirect('PrintSelect', answer['facilitySelect'])
            
    
    return render(request, "shared/printSelect.html", {
        'notifs': notifs, 
        'sortedFacilityData': sortedFacilityData, 
        'options': options, 
        'facility': facility, 
        'selectList': selectList, 
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock, 
        'alertMessage': alertMessage,
        'packetQuery': packetQuery,
        'formSettingsQuery': formSettingsQueryJson
    })