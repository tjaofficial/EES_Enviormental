from django.shortcuts import render, redirect


def signature(request):
    unlock = False
    client = False
    admin = False
    if request.user.groups.filter(name='SGI Technician'):
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        admin = True


    return render(request, "ees_forms/ees_signature.html", {
        'unlock': unlock, 
        'client': client, 
        'admin': admin,
    })