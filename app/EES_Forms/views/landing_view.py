from django.shortcuts import render

def landing_page(request):
    print('hello')
    return render(request, 'landing/landing_page.html', {
        
    })