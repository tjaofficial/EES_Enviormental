from django.shortcuts import render # type: ignore
import datetime
from ..models import Forms, user_profile_model
from django.contrib.auth.decorators import login_required # type: ignore
from ..utils.main_utils import setUnlockClientSupervisor


lock = login_required(login_url='Login')


@lock
def admin_data_view(request, facility):
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    profile = user_profile_model.objects.all()
    today = datetime.date.today()

    return render(request, "shared/admin_data.html", {
        'facility': facility, 
         
        "today": today, 
        'profile': profile,
        'unlock': unlock,
        'client': client,
        'supervisor': supervisor,
    })
