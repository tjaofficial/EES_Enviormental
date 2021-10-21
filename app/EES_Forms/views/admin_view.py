from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import CreateUserForm, user_profile_form
import datetime
from django.contrib import messages
from django.contrib.auth.models import Group

lock = login_required(login_url='Login')


def admin_dashboard_view(request):
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        print('hello')
    return render(request, "admin/admin_dashboard.html", {

    })


def register_view(request):
    # change code to redirect if you are not roger/SGI ADMIN
    if not request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        return redirect('IncompleteForms')
    else:
        form = CreateUserForm()
        profile_form = user_profile_form()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            profile_form = user_profile_form(request.POST)
            if form.is_valid() and profile_form.is_valid():
                user = form.save()

                profile = profile_form.save(commit=False)
                profile.user = user

                profile.save()

                group = Group.objects.get(name=profile.position)
                user.groups.add(group)

                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "The Information Entered Was Invalid.")
    return render(request, "ees_forms/ees_register.html", {
                'form': form, 'profile_form': profile_form
            })
