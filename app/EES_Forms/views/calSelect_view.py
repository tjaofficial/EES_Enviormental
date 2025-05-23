from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils.main_utils import PrintCalendar, checkIfFacilitySelected, setUnlockClientSupervisor
from ..models import the_packets_model, form_settings_model
import ast
import datetime
import calendar

lock = login_required(login_url='Login')

@lock
def calSelect(request, type, forms, year, month):
    facility = getattr(request, 'facility', None)
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
        
    monthConvert = calendar.month_name[month]
    month_number = list(calendar.month_name).index(monthConvert)
    month_number = int(month_number)
    
    if type == 'group':  
        groupForm = True
    else:
        groupForm = False
        
    print(groupForm)

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
        
    date = datetime.datetime.now()
    calend = PrintCalendar()
    calend.setfirstweekday(6)
    
    if groupForm:
        formSelect = str(forms)
        print('not single form')
        print(forms)
    else:
        formSelect = str(forms)
        print(formSelect)
            
    html_cal = calend.formatmonth(year, month, year, type, formSelect, facility, withyear=True)

    return render(request,"shared/calSelect.html",{
        'notifs': notifs,
        'prev_year': prev_year,
        'next_year': next_year,
        "type": type,
        "forms": forms,
        'prev_month': prev_month,
        'next_month': next_month,
        "facility": facility,
        "html_cal": html_cal,
        'supervisor': supervisor,
        "client": client,
        'unlock': unlock
    }) 