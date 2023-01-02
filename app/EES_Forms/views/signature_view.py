from django.shortcuts import render, redirect
from ..models import signature_model, daily_battery_profile_model
from ..forms import signature_form
import datetime

def signature(request, facility):
    existing = False
    unlock = False
    client = False
    admin = False
    if request.user.groups.filter(name='SGI Technician'):
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        admin = True
    
    count_bp = daily_battery_profile_model.objects.count()

    today = datetime.date.today()
    org = signature_model.objects.all().order_by('-sign_date')   
    
    if count_bp != 0:
        if len(org) > 0:
            if today == org[0].sign_date:
                database_form = org[0]
                existing = True
                
    if existing:
        initial_data = {
            'supervisor': database_form.supervisor,
            'sign_date': database_form.sign_date,
            'canvas': database_form.canvas,
        }
        data = signature_form(initial=initial_data)
    else:
        data = signature_form()
        
    if request.method == 'POST':
        if existing:
            data = signature_form(request.POST, instance=database_form)
        else:
            data = signature_form(request.POST)
        
        A_valid = data.is_valid()
        
        if A_valid:
            data.save()
            
            return redirect('IncompleteForms', facility)
    return render(request, "ees_forms/ees_signature.html", {
        'facility': facility, 'unlock': unlock, 'client': client, 'admin': admin, 'data': data
    })