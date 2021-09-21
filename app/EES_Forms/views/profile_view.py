from django.shortcuts import render, redirect
from ..models import user_profile_model, Forms
from ..forms import user_profile_form
import datetime

back = Forms.objects.filter(form__exact='Incomplete Forms')
today = datetime.date.today()


def profile(request, access_page):
    profile = user_profile_model.objects.all()
    current_user = request.user

    for x in profile:
        if x.user == current_user:
            user_select = x

    pic = user_select.profile_picture
    cert = user_select.cert_date
    # user_sel = user_select.user

    initial_data = {
        'cert_date': user_select.cert_date,
        'profile_picture': user_select.profile_picture,
        'phone': user_select.phone,
        'position': user_select.position,
    }

    pic_form = user_profile_form(initial=initial_data)

    if request.method == "POST":
        form = user_profile_form(request.POST, request.FILES, instance=user_select)

        if form.is_valid():
            A = form.save(commit=False)
            A.cert_date = cert

            form.save()

            return redirect('../profile/main')

    return render(request, "ees_forms/profile.html", {
        "back": back, 'user_select': user_select, "today": today, 'pic': pic, 'pic_form': pic_form, 'access_page': access_page, 'profile': profile,
    })
