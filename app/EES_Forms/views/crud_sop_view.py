from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import sop_model
import os

lock = login_required(login_url='Login')

@lock
def delete_sop_view(request, facility, sop_id):
    sop = sop_model.objects.get(pk=sop_id)
    
    if os.path.exists("./media/SOPs/" + sop.pdf_link):
        os.remove("./media/SOPs/" + sop.pdf_link)
        print('IT DOES EXIST')
    else:
        print("The file does not exist")
    sop.delete()
    return redirect('Sop', facility)

@lock
def update_sop_view(request, facility, sop_id):
    sop = sop_model.objects.get(pk=sop_id)
    
    if os.path.exists("./media/SOPs/" + sop.pdf_link):
        os.remove("./media/SOPs/" + sop.pdf_link)
        print('IT DOES EXIST')
    else:
        print("The file does not exist")
    sop.delete()
    return redirect('Sop', facility)
    