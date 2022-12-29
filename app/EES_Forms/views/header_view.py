from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import user_profile_model, bat_info_model, User
from ..forms import bat_info_form

lock = login_required(login_url='Login')
profile = user_profile_model.objects.all()

@lock
def about_view(request):
    profile = user_profile_model.objects.all()

    return render(request, 'ees_forms/ees_about.html', {
        'profile': profile,
    })

@lock
def safety_view(request):
    profile = user_profile_model.objects.all()

    return render(request, 'ees_forms/ees_safety.html', {
        'profile': profile,
    })

@lock
def settings_view(request):
    existing = False
    userName = request.user.get_username()
    userProfFaci = user_profile_model.objects.get(user__username=userName).facility_name
    database_model = bat_info_model.objects.filter(facility_name=userProfFaci)
    print(database_model)
    
    if len(bat_info_model.objects.all()) > 0:
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
            return redirect('IncompleteForms')
    
    return render(request, 'ees_forms/ees_settings.html', {
        'data': data,
    })
