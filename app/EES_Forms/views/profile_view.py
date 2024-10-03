from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from ..models import user_profile_model, Forms
from ..forms import user_profile_form
from ..utils import setUnlockClientSupervisor, checkIfFacilitySelected
import datetime
import os

back = Forms.objects.filter(form__exact='Incomplete Forms')
lock = login_required(login_url='Login')

@lock
def profile(request, facility, access_page):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    profile = user_profile_model.objects.all()
    existing = False
    today = datetime.date.today()
    user_select = ''
    pic = ''
    if len(profile) > 0:
        same_user = user_profile_model.objects.filter(user__exact=request.user.id)[0]
        if same_user:
            existing = True
            user_select = same_user
            pic = same_user.profile_picture
            cert = same_user.cert_date
    if existing:
        initial_data = {
            'cert_date': user_select.cert_date,
            'profile_picture': user_select.profile_picture,
            'phone': user_select.phone,
            'position': user_select.position,
        }
        pic_form = user_profile_form(initial=initial_data)
    else:
        pic_form = user_profile_form()

    if request.method == "POST":
        if existing:
            form = user_profile_form(request.POST, request.FILES, instance=user_select)
        else:
            form = user_profile_form(request.POST)

        if form.is_valid():
            A = form.save(commit=False)
            A.cert_date = cert

            form.save()

            return redirect('../profile/main')

    return render(request, "shared/profile.html", {
        'notifs': notifs,
        'unlock': unlock, 
        'client': client, 
        'supervisor': supervisor, 
        'facility': facility, 
        "back": back, 
        'user_select': user_select, 
        "today": today, 
        'pic': pic, 
        'pic_form': pic_form, 
        'access_page': access_page, 
        'profile': profile,
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