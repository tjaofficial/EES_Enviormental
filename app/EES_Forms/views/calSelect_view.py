from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import Calendar2
import datetime
import calendar

lock = login_required(login_url='Login')

@lock
def calSelect(request, facility, type, forms, year, month):
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
    calend = Calendar2()
    calend.setfirstweekday(6)
    html_cal = calend.formatmonth(year, month, year, forms, facility, withyear=True)
    
    if request.method == "POST":
        typeFormDate = '/' + request.POST['type'] + '-' + request.POST['formDate']
        
        if request.POST['forms'] == '' and request.POST['formGroups'] != '':
            formGroups = '/' + request.POST['formGroups']
            craftUrl = 'printIndex' + formGroups + typeFormDate
        elif request.POST['formGroups'] == '' and request.POST['forms'] != '':
            forms = '/' + request.POST['forms'].capitalize()
            craftUrl = 'printIndex' + forms + typeFormDate

        return redirect(craftUrl)
    return render(request,"shared/calSelect.html",{
        'prev_year': prev_year, 'next_year': next_year, "type": type, "forms": forms, 'prev_month': prev_month, 'next_month': next_month, "facility": facility, "html_cal": html_cal, 'supervisor': supervisor, "client": client, 'unlock': unlock,
    }) 