from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from ..models import user_profile_model, facility_model, User
from ..forms import bat_info_form
from..utils import setUnlockClientSupervisor, checkIfFacilitySelected

lock = login_required(login_url='Login')
profile = user_profile_model.objects.all()

@lock
def about_view(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    profile = user_profile_model.objects.all()

    return render(request, 'shared/about_facility.html', {
        'profile': profile, 
        'facility': facility,
        'notifs': notifs,
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock, 
    })

@lock
def safety_view(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    profile = user_profile_model.objects.all()

    return render(request, 'ees_forms/ees_safety.html', {
        'profile': profile, 
        'facility': facility,
        'supervisor': supervisor, 
        'notifs': notifs,
        "client": client, 
        'unlock': unlock, 
    })

@lock
def settings_view(request, facility):
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    if not client:
        return redirect('IncompleteForms', facility)
    existing = False
    userID = request.user.id
    print(user_profile_model.objects.get(user__id=userID).facilityChoice)
    userProfFaci = user_profile_model.objects.get(user__id=userID).facilityChoice.facility_name
    database_model = facility_model.objects.filter(facility_name=userProfFaci)
    print(database_model)
    
    if len(facility_model.objects.all()) > 0:
        if len(database_model) > 0:
            database_form = database_model[0]
            existing = True

    if existing:
        initial_data = {
            'bat_num': database_form.bat_num,
            'total_ovens': database_form.total_ovens,
            'facility_name': database_form.facility_name,
            'county': database_form.county,
            'estab_num': database_form.estab_num,
            'equip_location': database_form.equip_location,
            'address': database_form.address,
            'state': database_form.state,
            'district': database_form.district,
            'bat_height': database_form.bat_height,
            'bat_height_label': database_form.bat_height_label,
            'bat_main': database_form.bat_main,
            'bat_lids': database_form.bat_lids,
        }
        print('its existing')
        data = bat_info_form(initial=initial_data)
    else:
        data = bat_info_form()
    
    if request.method == 'POST':
        if existing:
            data = bat_info_form(request.POST, instance=database_form)
        else:
            data = bat_info_form(request.POST)
            
        A_valid = data.is_valid()
        print(data.errors)
        if A_valid:
            data.save()
            return redirect('IncompleteForms', facility)
    
    return render(request, 'ees_forms/ees_settings.html', {
        'data': data, 'facility': facility
    })
