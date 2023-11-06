from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import Calendar2, checkIfFacilitySelected
from ..models import facility_forms_model
import ast
import datetime
import calendar

lock = login_required(login_url='Login')

@lock
def calSelect(request, facility, type, forms, year, month):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = False
    client = False
    supervisor = False
    if request.user.groups.filter(name=OBSER_VAR):
        unlock = True
    if request.user.groups.filter(name=CLIENT_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
        
    monthConvert = calendar.month_name[month]
    month_number = list(calendar.month_name).index(monthConvert)
    month_number = int(month_number)
    facilityForms = facility_forms_model.objects.all().filter(facilityChoice__facility_name=facility)
    formList = ast.literal_eval(facilityForms[0].formData)
    
    if forms.upper().isupper():
        groupForm = True
    else:
        groupForm = False
        
    print(groupForm)
    print(formList)

    if month_number == 1:
        prev_month = 12
        prev_year = str(year - 1)
    else:
        prev_month = month_number - 1
        prev_year = year

    if month_number == 12:
        next_month = 1
        next_year = str(year + 1)
    else:
        next_month = month_number + 1
        next_year = year
    print(formList)
        
    date = datetime.datetime.now()
    calend = Calendar2()
    calend.setfirstweekday(6)
    
    if groupForm:
        formSelect = forms
        # if forms == "Coke Battery Daily Packet":
        #     formSelect = ((1,"A1"),(2,"A2"),(3,"A3"),(4,"A4"),(5,"A5"))
        print('not single form')
        print(forms)
    else:
        for x in formList:
            if x[0] == int(forms):
                formSelect = x
                print(formSelect)
                break
            
    html_cal = calend.formatmonth(year, month, year, formSelect, facility, withyear=True)
    
    # if request.method == "POST":
    #     typeFormDate = '/' + request.POST['type'] + '-' + request.POST['formDate']
        
    #     if request.POST['forms'] == '' and request.POST['formGroups'] != '':
    #         formGroups = '/' + request.POST['formGroups']
    #         craftUrl = 'printIndex' + formGroups + typeFormDate
    #     elif request.POST['formGroups'] == '' and request.POST['forms'] != '':
    #         forms = '/' + request.POST['forms'].capitalize()
    #         craftUrl = 'printIndex' + forms + typeFormDate

        # return redirect(craftUrl)
    return render(request,"shared/calSelect.html",{
        'notifs': notifs, 'prev_year': prev_year, 'next_year': next_year, "type": type, "forms": forms, 'prev_month': prev_month, 'next_month': next_month, "facility": facility, "html_cal": html_cal, 'supervisor': supervisor, "client": client, 'unlock': unlock,
    }) 