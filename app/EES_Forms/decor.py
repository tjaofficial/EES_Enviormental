def client_redirect(x):
    if not x.groups.filter(name='SGI Technician') or x.is_superuser:
        return redirect('c_dashboard')
     
client = client_redirect