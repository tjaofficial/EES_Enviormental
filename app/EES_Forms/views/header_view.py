from django.shortcuts import render
from ..models import user_profile_model

profile = user_profile_model.objects.all()


def about_view(request):
    profile = user_profile_model.objects.all()

    return render(request, 'ees_forms/ees_about.html', {
        'profile': profile,
    })


def safety_view(request):
    profile = user_profile_model.objects.all()

    return render(request, 'ees_forms/ees_safety.html', {
        'profile': profile,
    })
