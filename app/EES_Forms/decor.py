import braintree
from django.shortcuts import redirect
from .utils import braintreeGateway
from .models import user_profile_model

# def client_redirect(x):
#     if not x.groups.filter(name='SGI Technician') or x.is_superuser:
#         return redirect('c_dashboard')
     
# client = client_redirect

def isSubActive(func):
    def wrapper(request, facility, *args, **kwargs):
        gateway = braintreeGateway()
        accountData = user_profile_model.objects.get(user__username=request.user.username)
        customerId = accountData.company.customerID
        if not customerId:
            status = False
            print("no customer ID")
        else:
            print(gateway.customer.find(customerId))
        #get rid of the status=True for prod    
        status = True    
        if status:
            return func(request, facility, *args, **kwargs)
        else:
            return redirect('subscriptionSelect', facility, 'subscription')
    return wrapper