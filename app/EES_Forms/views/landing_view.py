from django.shortcuts import render
from ..models import braintreePlans

def landing_page(request):
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