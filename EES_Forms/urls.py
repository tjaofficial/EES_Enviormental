from django.urls import path
from . import views
from .views import PasswordsChangeView
from django.conf import settings
from django.contrib.auth import views as auth_views



urlpatterns = [
    #path("", views.index, name="index"),
    #path("tobe", views.tobe, name="tobe"),
    path("Register", views.register_view, name="Register"),
    path("Login", views.login_view, name="Login"),
    path("Logout", views.logout_view, name="Logout"),
    path("profile/<str:access_page>", views.profile, name="profile"),
    path("password", PasswordsChangeView.as_view(), name = 'PasswordChange'),
    path('profile_redirect', views.profile_redirect, name='profile_redirect'),
   
    path("daily_battery_profile/<str:access_page>/<str:date>", views.daily_battery_profile_view, name="daily_battery_profile"),
    path("IncompleteForms", views.IncompleteForms, name="IncompleteForms"),
    path("weekly_forms", views.weekly_forms, name="weekly_forms"),
    path("pt_admin1", views.pt_admin1_view, name="pt_admin1"),
    path("pt_mth_input", views.pt_mth_input, name="pt_mth_input"),
    path("method303_rolling_avg", views.method303_rolling_avg, name="rolling_avg"),
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
    path("Weekly/formF4", views.formF4, name="formF4"),
    path("Weekly/formF5", views.formF5, name="formF5"),
    path("Weekly/formF6", views.formF6, name="formF6"),
    path("Weekly/formF7", views.formF7, name="formF7"),
    path("Daily/formG1", views.formG1, name="formG1"),
    path("Daily/formG2", views.formG2, name="formG2"),
    path("Daily/formH/<str:access_page>", views.formH, name="formH"),
    path("Daily/formI", views.formI, name="formI"),
    path("Daily/formL/<str:access_page>", views.formL, name="formL"),
    path("Daily/formM", views.formM, name="formM"),
    
    path("issues_view/<str:form_name>/<str:form_date>/<str:access_page>", views.issues_view, name="issues_view"),
    path("Corrective-Action", views.corrective_action_view, name="Corrective-Action"),
    path("schedule/<int:year>/<str:month>", views.calendar_view, name="Calendar"),
    path("schedule_view", views.schedule_view, name="Schedule"),
    path("add_event", views.event_add_view, name="Add Event"),
    path("event_detail/<int:event_id>/<str:access_page>", views.event_detail_view, name="Event Details"),
   # path("calendar", views.CalendarView.as_view(), name='calendar'),
]