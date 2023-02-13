from django.shortcuts import render

def adminDash(request):
    print('hello')
    return render(request, 'admin/admin_dashboard.html', {
        
    })
    