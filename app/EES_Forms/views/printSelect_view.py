from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.apps import apps
from ..models import Forms
from django.core.exceptions import FieldError

lock = login_required(login_url='Login')

@lock
def printSelect(request, facility):
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
    formList = Forms.objects.all().order_by('form')
    selectList = []
    for line in formList:
        selectList.append([line.form, line.form.replace(' ', '_').replace('-','').lower()])
        print(selectList)
        
    
    
    if request.method == "POST":
        if request.POST['forms'] != '':
            if 1 <= len(request.POST['forms']) <= 2:
                formCheck = 'form' + request.POST['forms'].capitalize() + '_model'
            elif len(request.POST['forms']) > 2:
                formCheck = request.POST['forms'] + '_model'
                print(formCheck)
            else:
                print('something is wrong')
            mainModel = apps.get_model('EES_Forms', formCheck)
                
            try:
                filtered = mainModel.objects.filter(date=request.POST['formDate'])
            except FieldError as e:
                filtered = mainModel.objects.filter(week_start=request.POST['formDate'])
            
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
        'facility': facility, 'selectList': selectList, 'admin': admin, "client": client, 'unlock': unlock, 'alertMessage': alertMessage,
    })