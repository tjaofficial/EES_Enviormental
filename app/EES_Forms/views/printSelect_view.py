from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.apps import apps
from ..models import Forms, bat_info_model, facility_forms_model
from ..forms import *
from django.core.exceptions import FieldError
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
import ast
from ..utils import Calendar, checkIfFacilitySelected, getCompanyFacilities
import datetime

lock = login_required(login_url='Login')

@lock
def printSelect(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
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
    facilityForms = facility_forms_model.objects.filter(facilityChoice__facility_name=facility)
    if len(facilityForms) == 0:
        selectList = []
        print('No facility forms have been assigned/No facility has been selected')
    else:
        print('something is in here')
        facilityForms = facilityForms[0]
        parseList = ast.literal_eval(facilityForms.formData)


    # parseFromList = [
    #     (1, "A1", form1_form, form1_readings_form),
        # (2, "A2", form2_form),
        # (3, "A3", form3_form),
        # (4, "A4", form4_form),
        # (5, "A5", form5_form),
        # (6, "B", form6_form),
        # (7, "C", form7_form),
        # (8, "D", form8_form),
        # (9, "E", form9_form),
        # (10, "F1", form10_form),
        # (11, "F2", form11_form),
        # (12, "F3", form12_form),
        # (13, "F4", form13_form),
        # (14, "F5", form14_form),
        # (15, "F6", form15_form),
        # (16, "F7", form16_form),
        # (17, "G1", form17_form),
        # (18, "G1", form18_form),
        # (19, "H", form19_form),
        # (20, "I", form20_form),
        # (21, "L", form21_form),
        # (22, "M", form22_form),
        # (23, "N", form23_form),
        # (24, "O", form24_form),
        # (25, "P", form25_form),
        # (26, "R", form26_form),
        # (27, "Q", form27_form),  
    # ]
    # def copy_to_new_model(formID, modelLabel, modelForm, modelForm2):
    #     modelName = "form" + modelLabel + "_model"
    #     modelName2 = "form" + modelLabel + "_readings_model"
    #     existingModelData = apps.get_model('EES_Forms', modelName2).objects.all()
    #     for individualDataEntry in existingModelData:
    #         print("-" + str(individualDataEntry))
    #         existingFormData = individualDataEntry
    #         initial_data = {
    #             'date': existingFormData.form.date,
    #             'observer': existingFormData.form.observer,
    #             'crew': existingFormData.form.crew,
    #             'foreman': existingFormData.form.foreman,
    #             'start': existingFormData.form.start,
    #             'stop': existingFormData.form.stop,
    #             'c1_no': existingFormData.c1_no,
    #             'c2_no': existingFormData.c2_no,
    #             'c3_no': existingFormData.c3_no,
    #             'c4_no': existingFormData.c4_no,
    #             'c5_no': existingFormData.c5_no,
    #             'c1_start': existingFormData.c1_start,
    #             'c2_start': existingFormData.c2_start,
    #             'c3_start': existingFormData.c3_start,
    #             'c4_start': existingFormData.c4_start,
    #             'c5_start': existingFormData.c5_start,
    #             'c1_stop': existingFormData.c1_stop,
    #             'c2_stop': existingFormData.c2_stop,
    #             'c3_stop': existingFormData.c3_stop,
    #             'c4_stop': existingFormData.c4_stop,
    #             'c5_stop': existingFormData.c5_stop,
    #             'c1_sec': existingFormData.c1_sec,
    #             'c2_sec': existingFormData.c2_sec,
    #             'c3_sec': existingFormData.c3_sec,
    #             'c4_sec': existingFormData.c4_sec,
    #             'c5_sec': existingFormData.c5_sec,
    #             'c1_comments': existingFormData.c1_comments,
    #             'c2_comments': existingFormData.c2_comments,
    #             'c3_comments': existingFormData.c3_comments,
    #             'c4_comments': existingFormData.c4_comments,
    #             'c5_comments': existingFormData.c5_comments,
    #             'larry_car': existingFormData.larry_car,
    #             'comments': existingFormData.comments,
    #             'total_seconds': existingFormData.total_seconds,
    #         }
            
    #         if modelForm(instance=individualDataEntry.form).is_valid() and modelForm2(instance=individualDataEntry).is_valid():
    #             print("valid")
    #             modelForm(instance=individualDataEntry.form).save()
    #             modelForm2(instance=individualDataEntry).save()
            
    # copy_to_new_model(1, "A1", form1_form, form1_readings_form)
        
    # for x in parseFromList:
    #     if x[0] in {23,26,27}:
    #         continue
    #     else:
    #         modelName = "form"+x[1]+"_model"
    #         modelBackupName = "form"+x[1]+"_readings_model"
    #         newModelName = "form"+str(x[0])+"_model"
    #         formID = int(x[0])
    #         print("Pulling=> "+ modelBackupName)
    #         existingModelData = apps.get_model('EES_Forms', modelBackupName).objects.all()
    #         for y in existingModelData:
    #             print("-" + str(y))
    #             existingFormData = y
    #             newModel = apps.get_model('EES_Forms', newModelName)
    #             initial_data = {
    #                 'date': existingFormData.form.date,
    #                 'observer': existingFormData.form.observer,
    #                 'crew': existingFormData.form.crew,
    #                 'foreman': existingFormData.form.foreman,
    #                 'start': existingFormData.form.start,
    #                 'stop': existingFormData.form.stop,
    #                 'c1_no': existingFormData.c1_no,
    #                 'c2_no': existingFormData.c2_no,
    #                 'c3_no': existingFormData.c3_no,
    #                 'c4_no': existingFormData.c4_no,
    #                 'c5_no': existingFormData.c5_no,
    #                 'c1_start': existingFormData.c1_start,
    #                 'c2_start': existingFormData.c2_start,
    #                 'c3_start': existingFormData.c3_start,
    #                 'c4_start': existingFormData.c4_start,
    #                 'c5_start': existingFormData.c5_start,
    #                 'c1_stop': existingFormData.c1_stop,
    #                 'c2_stop': existingFormData.c2_stop,
    #                 'c3_stop': existingFormData.c3_stop,
    #                 'c4_stop': existingFormData.c4_stop,
    #                 'c5_stop': existingFormData.c5_stop,
    #                 'c1_sec': existingFormData.c1_sec,
    #                 'c2_sec': existingFormData.c2_sec,
    #                 'c3_sec': existingFormData.c3_sec,
    #                 'c4_sec': existingFormData.c4_sec,
    #                 'c5_sec': existingFormData.c5_sec,
    #                 'c1_comments': existingFormData.c1_comments,
    #                 'c2_comments': existingFormData.c2_comments,
    #                 'c3_comments': existingFormData.c3_comments,
    #                 'c4_comments': existingFormData.c4_comments,
    #                 'c5_comments': existingFormData.c5_comments,
    #                 'larry_car': existingFormData.larry_car,
    #                 'comments': existingFormData.comments,
    #                 'total_seconds': existingFormData.total_seconds,
    #             }
    #             # print(newModel(y))
    #             newModel(initial_data).save()
    #             break
    #         print("___________________________")
    #         break
        
        

    if request.method == "POST":
        answer = request.POST
        forms  = request.POST['forms']
        if 'facilitySelect' in answer.keys():
            if answer['facilitySelect'] != '':
                return redirect('PrintSelect', answer['facilitySelect'])
        inputDate = datetime.datetime.strptime(request.POST["monthSel"], "%Y-%m").date()
        if request.POST['type'] == 'single':
            print('HFLSKDJFLSKJDFLKSJDF--------')
            print(forms)
            if int(forms) == 23:
                print('yes its 23')
                formDate = request.POST['monthSel']
                formGroup = 'single'
                formIdentity = forms
                
                return redirect('printIndex', facility, formGroup, formIdentity, formDate)
            return redirect("CalSelect", facility, request.POST['type'], request.POST['forms'], inputDate.year, inputDate.month)
        elif request.POST['type'] == "group":
            return redirect("CalSelect", facility, request.POST['type'], request.POST['formGroups'], inputDate.year, inputDate.month)
            
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
                    filtered = mainModel.objects.filter(date=request.POST['formDate'])
                except FieldError as e:
                    filtered = mainModel.objects.filter(week_start=request.POST['formDate'])
                
                if len(filtered) == 0:
                    alertMessage = '*FORM DOES NOT EXIST PLEASE SELECT ANOTHER DATE*'
                else:
                    alertMessage = ''
            
            typeFormDate = '/' + request.POST['type'] + '-' + request.POST['formDate']
                
            if forms == '' and request.POST['formGroups'] != '':
                formGroups = '/' + request.POST['formGroups']
                craftUrl = 'printIndex' + formGroups + typeFormDate
            elif request.POST['formGroups'] == '' and forms != '':
                forms = '/' + forms.capitalize()
                craftUrl = 'printIndex' + forms + typeFormDate

            return redirect(craftUrl)
        except:
            answer = request.POST
            if answer['facilitySelect'] != '':
                return redirect('PrintSelect', answer['facilitySelect'])
            
    
    return render(request, "shared/printSelect.html", {
        'notifs': notifs, 'sortedFacilityData': sortedFacilityData, 'options': options, 'facility': facility, 'selectList': parseList, 'supervisor': supervisor, "client": client, 'unlock': unlock, 'alertMessage': alertMessage,
    })