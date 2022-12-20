from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.apps import apps

lock = login_required(login_url='Login')

@lock
def printSelect(request):
    unlock = False
    client = False
    admin = False
    alertMessage = ''
    if request.user.groups.filter(name='SGI Technician'):
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        admin = True
        
    if request.method == "POST":
        if request.POST['forms'] != '':
            formCheck = request.POST['forms'].capitalize()
            print(formCheck)
            mainModel = apps.get_model('EES_Forms', 'form' + formCheck + '_model')
            filtered = mainModel.objects.filter(date=request.POST['formDate'])
            if len(filtered) == 0:
                alertMessage = '*FORM DOES NOT EXIST PLEASE SELECT ANOTHER DATE*'
            else:
                alertMessage = ''
        
        typeFormDate = '/' + request.POST['type'] + '-' + request.POST['formDate']
            
        if request.POST['forms'] == '' and request.POST['formGroups'] != '':
            formGroups = '/' + request.POST['formGroups']
            craftUrl = 'printIndex' + formGroups + typeFormDate
        elif request.POST['formGroups'] == '' and request.POST['forms'] != '':
            forms = '/' + request.POST['forms'].capitalize()
            craftUrl = 'printIndex' + forms + typeFormDate

        return redirect(craftUrl)
    
    return render(request, "shared/printSelect.html", {
        'admin': admin, "client": client, 'unlock': unlock, 'alertMessage': alertMessage,
    })