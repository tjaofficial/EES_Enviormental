from django.shortcuts import render, redirect # type: ignore
from ..models import signature_model, daily_battery_profile_model, facility_model
from ..forms import signature_form
import datetime
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR

def signature(request, facility):
    existing = False
    unlock = False
    client = False
    supervisor = False
    if request.user.groups.filter(name=OBSER_VAR):
        unlock = True
    if request.user.groups.filter(name=CLIENT_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    options = facility_model.objects.all().filter(facility_name=facility)[0]
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
            'facilityChoice': database_form.facilityChoice,
        }
        data = signature_form(initial=initial_data)
    else:
        data = signature_form()
        
    if request.method == 'POST':
        if existing:
            data = signature_form(request.POST, instance=database_form)
        else:
            dataCopy = request.POST.copy()
            dataCopy['facilityChoice'] = options
            data = signature_form(dataCopy)
        A_valid = data.is_valid()
        
        if A_valid:
            data.save()
            
            return redirect('IncompleteForms', facility)
    return render(request, "observer/personnel_signature.html", {
        'facility': facility, 'unlock': unlock, 'client': client, 'supervisor': supervisor, 'data': data
    })