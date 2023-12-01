import braintree
from django.shortcuts import redirect
from .utils import braintreeGateway
from .models import user_profile_model, braintree_model

# def client_redirect(x):
#     if not x.groups.filter(name='SGI Technician') or x.is_superuser:
#         return redirect('c_dashboard')
     
# client = client_redirect

def isSubActive(func):
    def wrapper(request, facility, *args, **kwargs):
        braintreeData = braintree_model.objects.filter(user__id=request.user.id)
        profileData = user_profile_model.objects.get(user__id=request.user.id)
        if braintreeData.exists():
            braintreeData = braintreeData.get(user__id=request.user.id)
        else:
            print('handle if there is no braintree entry')
        status = braintreeData.status
        if status == "active":
            status = True
        else:
            status = False
            print("no customer ID")
        #V------get rid of the status=True for prod-----V
        status = True    
        if status:
            return func(request, facility, *args, **kwargs)
        else:
            return redirect('subscriptionSelect', facility, 'subscription')
    return wrapper