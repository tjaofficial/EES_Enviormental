import braintree # type: ignore
from django.shortcuts import redirect # type: ignore
from .utils import braintreeGateway, get_braintree_query
from .models import user_profile_model, braintree_model

# def client_redirect(x):
#     if not x.groups.filter(name='SGI Technician') or x.is_superuser:
#         return redirect('c_dashboard')
     
# client = client_redirect

def isSubActive(func):
    def wrapper(request, facility, *args, **kwargs):
        status = get_braintree_query(request.user)
        if status:
            status = status.status
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