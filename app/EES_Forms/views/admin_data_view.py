from django.shortcuts import render
import datetime
from ..models import Forms, user_profile_model
from django.contrib.auth.decorators import login_required

back = Forms.objects.filter(form__exact='Incomplete Forms')
today = datetime.date.today()
lock = login_required(login_url='Login')


@lock
def admin_data_view(request):
    profile = user_profile_model.objects.all()

    return render(request, "ees_forms/admin_data.html", {
        "back": back, "today": today, 'profile': profile,
    })
