from functools import wraps
from django.shortcuts import redirect # type: ignore
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.urls import reverse # type: ignore

# def client_redirect(x):
#     if not x.groups.filter(name='SGI Technician') or x.is_superuser:
#         return redirect('c_dashboard')
     
# client = client_redirect

def isSubActive(func):
    def wrapper(request, facility, *args, **kwargs):
        stripeEntry = request.user.user_profile.company.subscription
        if stripeEntry:
            status = stripeEntry.status
        if status == "active":
            return func(request, facility, *args, **kwargs)
        else:
            print("no customer ID")
            return redirect('subscriptionSelect', facility, 'subscription')
    return wrapper

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.groups.filter(name=group_name).exists():
                user_group = request.user.groups.first() 
                redirect_choices = {
                    CLIENT_VAR: ("c_dashboard", [request.user.user_profile.company.company_name]), 
                    OBSER_VAR: ("facilitySelect", ["observer"]), 
                    SUPER_VAR: ("sup_dashboard", ["supervisor"]),
                }
                #delete laterVVVV
                superuser = True
                if user_group and user_group.name in redirect_choices:
                    view_name, view_args = redirect_choices[user_group.name]
                    return redirect(reverse(view_name, args=view_args))
                elif superuser:
                    return view_func(request, *args, **kwargs)
                else:
                    # needs to be a page with a error code and telling user to contact support because
                    # their account doesnt have a group assigned.
                    return redirect('no_registration')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
