from django.shortcuts import render, redirect # type: ignore
from django.http import JsonResponse # type: ignore
from django.db.models import Q # type: ignore
from django.apps import apps # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from ..utils.main_utils import setUnlockClientSupervisor, checkIfFacilitySelected, getCompanyFacilities, setUnlockClientSupervisor, createNotification, updateSubmissionForm
from datetime import datetime
from django.contrib import messages # type: ignore
from django.urls import reverse # type: ignore
from ..forms import issues_form
from ..models import issues_model, facility_model, user_profile_model, form_settings_model

lock = login_required(login_url='Login')

@lock
def corrective_action_view(request):
    facility = getattr(request, 'facility', None)
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    issueForm_query = request.GET.get('issueForm')
    issueMonth_query = request.GET.get('issueMonth')
    issueDate_query = request.GET.get('issueDate')
    issue_contains_query = request.GET.get('issue_contains')
    notified_query = request.GET.get('notified')
    ca_forms = issues_model.objects.filter(formChoice__facilityChoice=facility).order_by('-id')
    
    varPull = [
        issueForm_query,
        issueMonth_query,
        issueDate_query,
        issue_contains_query,
        notified_query
    ]

    def issueFormFunc(issueForm_query, ca_forms):
        if issueForm_query != "" and issueForm_query is not None:
            #print("Pre-Form-Search")
            #print(ca_forms)
            ca_forms = ca_forms.filter(formChoice__formChoice__form__icontains=issueForm_query)
            #print("Post-Form-Search")
            #print(ca_forms)
            return ca_forms
        else:
            return "none"
    
    def issueMonthFunc(issueMonth_query, ca_forms):
        if issueMonth_query != "" and issueMonth_query is not None:
            #print("Pre-Month-Search")
            #print(ca_forms)
            issueMonth_query = datetime.strptime(issueMonth_query, "%Y-%m").date()
            ca_forms = ca_forms.filter(date__month=issueMonth_query.month, date__year=issueMonth_query.year)
            #print("Post-Month-Search")
            #print(ca_forms)
            return ca_forms
        else:
            return "none"
    
    def issueDateFunc(issueDate_query, ca_forms):
        if issueDate_query != "" and issueDate_query is not None:
            issueDate_query = datetime.strptime(issueDate_query, "%Y-%m-%d").date()
            ca_forms = ca_forms.filter(date__year=issueDate_query.year, date__month=issueDate_query.month, date__day=issueDate_query.day)
            return ca_forms
        else:
            return "none"
    
    def issue_containsFunc(issue_contains_query, ca_forms):
        if issue_contains_query != "" and issue_contains_query is not None:
            ca_forms = ca_forms.filter(issues__icontains=issue_contains_query)
            return ca_forms
        else:
            return "none"
    
    def notifiedfunc(notified_query, ca_forms):
        if notified_query != "" and notified_query is not None:
            #print("Pre-Notified-Search")
            #print(ca_forms)
            ca_forms = ca_forms.filter(notified__icontains=notified_query)
            #print("Post-Notified-Search")
            #print(ca_forms)
            return ca_forms
        else:
            return "none"
    
    searchList = [
        issueFormFunc(issueForm_query, ca_forms),
        issueMonthFunc(issueMonth_query, ca_forms),
        issueDateFunc(issueDate_query, ca_forms),
        issue_containsFunc(issue_contains_query, ca_forms),
        notifiedfunc(notified_query, ca_forms)
    ]
    
    filterReturn = []
    notEmpty = False
    inputsUsedCount = 0
    for x in searchList:
        if x != 'none':
            inputsUsedCount += 1
            for y in x:
                filterReturn.append(y)
            notEmpty = True
    #print(filterReturn)

    unisonResults = []
    usedItems = []
    for i in range(len(filterReturn)):
        result = filterReturn[i]
        count = 0
        #print("<------USE")
        #print(i)
        if result not in usedItems:
            for z in range(len(filterReturn)):
                result2 = filterReturn[z]
                #print("<------Compared")
                #print(z)
                if result == result2:
                    count += 1
                    #print("<---------------------COUNT")
                    if count == inputsUsedCount:
                        if result2 not in unisonResults:
                            unisonResults.append(result2)
                            #print("Adding " + str(result2) + " to the unison list")
            #print("------END LOOP-------")
            usedItems.append(result)
        else:
            #print("------END LOOP-------")
            continue
    
    #print(unisonResults)
    if notEmpty:
        if unisonResults:
            ca_forms = unisonResults
        else:
            ca_forms = "empty"
    
    profile = user_profile_model.objects.all()
    options = facility_model.objects.all()
    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
    if request.method == 'POST':
        answer = request.POST
        print(answer)
        if answer['facilitySelect'] != '':
            return redirect('Corrective-Action', answer['facilitySelect'])
    return render(request, "shared/corrective_actions.html", {
        'notifs': notifs, 
        "varPull": varPull, 
        'sortedFacilityData': sortedFacilityData, 
        'options': options, 
        'facility': facility, 
        'ca_forms': ca_forms, 
        'profile': profile, 
        'client': client, 
        "supervisor": supervisor, 
        "unlock": unlock, 
    })

@lock
def corrective_action_search_api(request):
    facility = request.GET.get('facility', None)
    facility = facility_model.objects.get(facility_name=facility)
    if not facility or facility in ['None', 'null']:
        return JsonResponse({'error': 'Please select a facility first.'}, status=400)
    form_label = request.GET.get('formLabel', '')
    print(form_label)
    form_issue = request.GET.get('formIssue', '')
    form_month = request.GET.get('formMonth', '')
    form_date = request.GET.get('formDate', '')
    form_personnel = request.GET.get('formPersonnel', '')

    issues_qs = issues_model.objects.filter(formChoice__facilityChoice=facility)
    print(issues_qs)

    if form_label:
        print("query label")
        issues_qs = issues_qs.filter(
            Q(formChoice__settings__packets__icontains=form_label)
        )

    if form_issue:
        print("query issue")
        issues_qs = issues_qs.filter(
            Q(issues__icontains=form_issue)
        )
    
    if form_personnel:
        issues_qs = issues_qs.filter(
            Q(notified__icontains=form_personnel)
        )
    
    if form_month:
        year, month = form_month.split('-')
        issues_qs = issues_qs.filter(date__year=year,date__month=month)
    
    if form_date:
        date_obj = datetime.strptime(form_date, "%Y-%m-%d").date()
        issues_qs = issues_qs.filter(date=date_obj)
    
    if not issues_qs.exists():
        return JsonResponse({'results': []})

    final_results = []
    
    for issue in issues_qs:
        # Build your URL logic exactly like you had before:
        form_url = reverse('issues_view', args=[issue.id,'issue'])

        # Format packets nicely
        packets = issue.formChoice.settings.get('packets', {})
        packet_labels = list(packets.values())

        final_results.append({
            'form_id': issue.id,
            'form_labels': packet_labels,
            'form_title': issue.formChoice.settings['settings'].get('custom_name') or issue.formChoice.formChoice.title,
            'form_header': issue.formChoice.formChoice.header,
            'form_personnel': issue.notified,
            'form_issues': issue.issues,
            'date': str(issue.date),
            'url': form_url,
        })
    print(f"Your looking for this {final_results}")
    return JsonResponse({'results': final_results})

@lock
def issues_view(request, issueID, access_page):
    is_date = True
    try:
        parsed_date = datetime.strptime(access_page, '%Y-%m-%d')
    except ValueError:
        is_date = False

    if is_date:
        issueSelect = issues_model.objects.get(formChoice__id=issueID, date=parsed_date) 
    elif access_page.startswith('form'): 
        issueSelect = form_settings_model.objects.get(id=issueID)
    else:
        issueSelect = issues_model.objects.get(id=issueID) 

    facility = issueSelect.formChoice.facilityChoice.facility_name if access_page[:4] != 'form' else issueSelect.facilityChoice.facility_name
    now = datetime.now().date()
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    notifs = checkIfFacilitySelected(request.user)
    existing = False
    search = False
    notifSelector = ['deviations']

    if access_page.endswith('c'):
        notifSelector.append('compliance')
        access_page = access_page[:-2]

    if access_page == 'form':
        existing = False
    elif access_page == 'issue':
        existing = True
        search = True
        form = issueSelect
        if client:
            issueSelect.viewed = True
            issueSelect.save()
    elif is_date:
        existing = True
    else:
        messages.error(request,"ERROR: ID-11850009. Contact Support Team.")
        return redirect('IncompleteForms')

    if search:
        print("search")
    else:
        if existing:
            initial_data = {
                'issues': issueSelect.issues,
                'notified': issueSelect.notified,
                'time': issueSelect.time,
                'date': issueSelect.date,
                'cor_action': issueSelect.cor_action
            }
        else:
            initial_data = {
                'date': now,
                'formChoice': issueSelect
            }

        form = issues_form(initial=initial_data)

    if request.method == "POST":
        copyRequest = request.POST.copy()
        copyRequest['formChoice'] = issueSelect if not existing else issueSelect.formChoice
        copyRequest['userChoice'] = request.user.user_profile
        if existing:
            data = issues_form(copyRequest, instance=issueSelect)
        else:
            data = issues_form(copyRequest)
        if data.is_valid():
            print('check #1')
            A = data.save()
            if not existing:
                notifSelector.append('submitted')
            
            formModel = apps.get_model('EES_Forms', f"{A.formChoice.formChoice.link}_model")
            formDate = now if not existing else issueSelect.date
            savedForm = formModel.objects.get(date=formDate, formSettings=A.formChoice)
            createNotification(facility, request, A.formChoice.id, now, notifSelector, A.id, savedForm=savedForm)
            if not existing:
                updateSubmissionForm(A.formChoice.id, True, now)
            
            if existing:
                return redirect('issues_view', A.id, 'issue')
            else:
                return redirect('IncompleteForms')

    return render(request, "shared/issues_template.html", {
        'notifs': notifs, 
        'facility': facility, 
        'form': form, 
        'access_page': access_page, 
        "unlock": unlock, 
        "client": client, 
        "supervisor": supervisor,
        'issueSelect': issueSelect
    })


