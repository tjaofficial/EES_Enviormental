from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def signature(request):
    return render(request, "admin/signature.html", {})