from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from ..decor import group_required
from EES_Enviormental.settings import CLIENT_VAR
from ..utils.main_utils import userColorMode, colorModeSwitch, updateAllFormSubmissions

lock = login_required(login_url='Login')

@lock
@group_required(CLIENT_VAR)
def client_dashboard_view(request):
    facility = getattr(request, 'facility', None)
    updateAllFormSubmissions(facility)
    colorMode = userColorMode(request.user)[0]  
    userMode = userColorMode(request.user)[1]

    if request.method == 'POST':
        answer = request.POST
        if 'colorMode' in answer.keys():
            print("CHECK 1")
            print(answer['colorMode'])
            colorModeSwitch(request)    
            return redirect(request.META['HTTP_REFERER'])
        
    return render(request, "supervisor/sup_dashboard.html", {
        'facility': facility,
        'colorMode': colorMode,
        'userMode': userMode,
    })
