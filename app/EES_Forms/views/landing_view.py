from django.shortcuts import render
from ..models import braintreePlans, FAQ_model, Forms
from .inital_form_add import add_forms_to_database

def landing_page(request):
    # IMPORTANT - THIS CHECKS IF DATABASE IS EMPTY AND ADD THE INITAL DATA
    # DO NOT DELETE
    add_forms_to_database()
    
    
    btPlans = braintreePlans.objects.all()
    print('hello')
    cPlan = []
    for plan in btPlans:
        oPlan = {
            'pid': plan.planID,
            'description': plan.description.split("\n"),
            'Customizable_Forms': 'Customizable Forms',
            'Real_time_Data_Entry': 'Real-time Data Entry',
            'Multimedia_Integration': 'Multimedia Integration',
            'Advanced_Reporting': 'Advanced Reporting',
            'Collaborative_Workflows': 'Collaborative Workflows',
            'Security_and_Compliance': 'Security and Compliance',
            'Offline_Accessibility': 'Offline Accessibility',
            'name': plan.name,
            'price': plan.price
            }
        cPlan.append(oPlan)
    cPlan.sort(key=lambda d: d['price'])
    return render(request, 'landing/landingPage_main.html', {
        "planList": cPlan
    })
    
def FAQ_view(request):
    FAQData = FAQ_model.objects.all()
    sectionList = []
    for FAQ in FAQData:
        if FAQ.section not in sectionList:
            sectionList.append(FAQ.section)
    
    sectionDict = {}
    for section in sectionList:
        sectionGroup = []
        for question in FAQData:
            if question.section == section:
                sectionGroup.append(question)
        sectionDict[section] = sectionGroup  
    return render(request, 'landing/FAQ.html', {
        'sectionDict': sectionDict
    })

def terms_and_conditions_view(request):

    return render(request, 'landing/terms_and_conditions.html', {})

def privacy_policy_view(request):

    return render(request, 'landing/privacy_policy.html', {})

def included_forms_view(request):
    formData = Forms.objects.exclude(header='Waste Weekly Inspections')
    return render(request, 'landing/included_forms.html', {
        'formData': formData,
    })

def landing_contact_view(request):
    
    return render(request, 'landing/landing_contact.html', {})