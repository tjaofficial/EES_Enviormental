from django.shortcuts import render
import datetime
from ..models import Forms, user_profile_model
from django.contrib.auth.decorators import login_required

back = Forms.objects.filter(form__exact='Incomplete Forms')
lock = login_required(login_url='Login')


@lock
def admin_data_view(request, facility):
    profile = user_profile_model.objects.all()
    today = datetime.date.today()

    return render(request, "shared/admin_data.html", {
        'facility': facility, "back": back, "today": today, 'profile': profile,
    })
