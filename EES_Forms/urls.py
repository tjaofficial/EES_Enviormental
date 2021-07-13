from django.urls import path
from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    #path("tobe", views.tobe, name="tobe"),
    path("Register", views.register_view, name="Register"),
    path("Login", views.login_view, name="Login"),
    path("Logout", views.logout_view, name="Logout"),
    path("daily_battery_profile", views.daily_battery_profile_view, name="daily_battery_profile"),
    path("IncompleteForms", views.IncompleteForms, name="IncompleteForms"),
    path("pt_admin1", views.pt_admin1_view, name="pt_admin1"),
    path("admin_data", views.admin_data_view, name="admin_data"),
    path("Daily/Method303/formA1", views.formA1, name="formA1"),
    path("Daily/Method303/formA2", views.formA2, name="formA2"),
    path("Daily/Method303/formA3", views.formA3, name="formA3"),
    path("Daily/Method303/formA4", views.formA4, name="formA4"),
    path("Daily/Method303/formA5", views.formA5, name="formA5"),
    path("Daily/formB", views.formB, name="formB"),
    path("Daily/formC", views.formC, name="formC"),
    path("Daily/formD", views.formD, name="formD"),
    path("Daily/formE", views.formE, name="formE"),
    path("Weekly/formF1", views.formF1, name="formF1"),
    path("Weekly/formF2", views.formF2, name="formF2"),
     path("Weekly/formF3", views.formF3, name="formF3"),
    path("Daily/formG1", views.formG1, name="formG1"),
    path("Daily/formH", views.formH, name="formH"),
    path("Daily/formI", views.formI, name="formI"),
    path("Daily/formL", views.formL, name="formL"),
    path("Daily/formM", views.formM, name="formM")
]