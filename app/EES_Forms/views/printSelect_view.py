from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.apps import apps # type: ignore
from ..models import facility_model, the_packets_model, form_settings_model
from ..forms import *
from django.http import JsonResponse # type: ignore
from django.core.exceptions import FieldError # type: ignore
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
import json
from ..utils.main_utils import checkIfFacilitySelected, getCompanyFacilities, setUnlockClientSupervisor
import datetime

lock = login_required(login_url='Login')

@lock
def printSelect(request):
    facility = getattr(request, 'facility', None)
    notifs = checkIfFacilitySelected(request.user)
    options = facility_model.objects.all()
    alertMessage = ''
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    formSettingsQuery = form_settings_model.objects.filter(facilityChoice=facility)
    packetQuery = the_packets_model.objects.filter(facilityChoice=facility)
    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
    selectList = []
    fsList = []
    for fs in formSettingsQuery:
        if fs.settings['packets']:
            labelList = []
            for label in fs.settings['packets']:
                labelList.append((fs.settings['packets'][label], int(label)))
            fsList.append((fs.id, labelList))
    formSettingsQueryJson = json.dumps(fsList)
    if len(formSettingsQuery) == 0:
        print('No facility forms have been assigned/No facility has been selected')
    else:
        #this needs to be optimaized, the "select list" can be removes as an empty list and 
        #made to equal the formSettingsQuery
        print('something is in here')
        for settingsEntry in formSettingsQuery:
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
                
                return redirect('printIndex', facility.facility_name, formGroup, formIdentity, formDate)
            if str(answer['formLabels']) == str(forms):
                return redirect("CalSelect", answer['type'], forms, inputDate.year, inputDate.month)
            else:
                forms = str(forms) + '-' + str(answer['formLabels'])
                return redirect("CalSelect", answer['type'], forms, inputDate.year, inputDate.month)
        elif answer['type'] == "group":
            return redirect("CalSelect", answer['type'], answer['formGroups'], inputDate.year, inputDate.month)
            
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

@lock
def print_label_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        freq_id = data.get("freq_id")

        try:
            freq = form_settings_model.objects.get(id=freq_id)
        except form_settings_model.DoesNotExist:
            return JsonResponse({'error': 'Invalid freq_id'}, status=400)

        packets = freq.settings.get('packets', {})
        seen = set()
        unique_labels = []

        for key, label in packets.items():
            if not label.startswith("no") and label not in seen:
                seen.add(label)
                unique_labels.append({"key": key, "label": label})

        return JsonResponse({'labels': unique_labels})