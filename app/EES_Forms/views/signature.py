from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore

def signature(request):
    return render(request, "admin/signature.html", {})