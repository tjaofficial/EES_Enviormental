from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from ..models import user_profile_model, Forms
from ..forms import user_profile_form
from ..utils.main_utils import setUnlockClientSupervisor, checkIfFacilitySelected
import datetime
import os


lock = login_required(login_url='Login')

@lock
def profile(request, facility, access_page):
    facility = getattr(request, 'facility', None)
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    profile = request.user.user_profile
    today = datetime.date.today()
    user_select = ''
    pic = ''

    initial_data = {
        'cert_date': profile.cert_date,
        'profile_picture': profile.profile_picture,
        'phone': profile.phone,
        'position': profile.position,
    }
    pic_form = user_profile_form(initial=initial_data)

    if request.method == "POST":
        form = user_profile_form(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            A = form.save(commit=False)
            A.cert_date = profile.cert_date

            form.save()

            return redirect('../profile/main')

    return render(request, "shared/profile.html", {
        'notifs': notifs,
        'unlock': unlock, 
        'client': client, 
        'supervisor': supervisor, 
        'facility': facility, 
         
        'user_select': user_select, 
        "today": today, 
        'pic': pic, 
        'pic_form': pic_form, 
        'access_page': access_page, 
    })

@lock
def delete_prof_pic_view(request, facility, profile_pic_id):
    prof = user_profile_model.objects.get(pk=profile_pic_id)
    
    if os.path.exists("./media/" + str(prof.profile_picture)):
        os.remove("./media/" + str(prof.profile_picture))
        print('IT DOES EXIST')
    else:
        print("The file does not exist")
    prof.profile_picture.delete()
    return redirect('Contacts', facility)