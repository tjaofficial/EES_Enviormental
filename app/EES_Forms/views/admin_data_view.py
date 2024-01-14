from django.shortcuts import render
import datetime
from ..models import Forms, user_profile_model
from django.contrib.auth.decorators import login_required
from ..utils import setUnlockClientSupervisor

back = Forms.objects.filter(form__exact='Incomplete Forms')
lock = login_required(login_url='Login')


@lock
def admin_data_view(request, facility):
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    profile = user_profile_model.objects.all()
    today = datetime.date.today()

    return render(request, "shared/admin_data.html", {
        'facility': facility, 
        "back": back, 
        "today": today, 
        'profile': profile,
        'unlock': unlock,
        'client': client,
        'supervisor': supervisor,
    })
