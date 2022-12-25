from django.urls import path
from . import views
from .views.login_logout_view import PasswordsChangeView

urlpatterns = [
    path("", views.IncompleteForms, name="IncompleteForms"),
    path("admin_dashboard", views.admin_dashboard_view, name='admin_dashboard'),

    path("Register", views.register_view, name="Register"),
    path("Login", views.login_view, name="Login"),
    path("no_registration", views.valid_account_logout, name="no_registration"),
    path("Logout", views.logout_view, name="Logout"),
    path('profile_redirect', views.profile_redirect, name='profile_redirect'),
    path("password", PasswordsChangeView.as_view(), name='PasswordChange'),

    path("profile/<str:access_page>", views.profile, name="profile"),
    path('about', views.about_view, name='about'),
    path('safety', views.safety_view, name='safety'),
    

    path("daily_battery_profile/<str:access_page>/<str:date>", views.daily_battery_profile_view, name="daily_battery_profile"),

    path("Corrective-Action", views.corrective_action_view, name="Corrective-Action"),
    path("schedule_view", views.schedule_view, name="Schedule"),
    path("schedule/<int:year>/<str:month>", views.calendar_view, name="Calendar"),
    path("add_event", views.event_add_view, name="Add Event"),
    path("event_detail/<int:event_id>/<str:access_page>", views.event_detail_view, name="Event Details"),
    path('archive', views.archive_view, name='archive'),
    path('search_forms/<str:access_page>', views.search_forms_view, name='search_forms'),
    path("issues_view/<str:form_name>/<str:form_date>/<str:access_page>", views.issues_view, name="issues_view"),
    path("Contacts", views.shared_contacts_view, name="Contacts"),
    path("Sop", views.sop_view, name="Sop"),
    path("DeleteSop/<str:sop_id>", views.delete_sop_view, name="DeleteSop"),
    path("UpdateSop/<str:sop_id>", views.update_sop_view, name="UpdateSop"),


    path("Daily/formA1/<str:selector>", views.formA1, name="formA1"),
    path("Daily/formA2/<str:selector>", views.formA2, name="formA2"),
    path("Daily/formA3/<str:selector>", views.formA3, name="formA3"),
    path("Daily/formA4/<str:selector>", views.formA4, name="formA4"),
    path("Daily/formA5/<str:selector>", views.formA5, name="formA5"),
    path("Daily/formB/<str:selector>", views.formB, name="formB"),
    path("Daily/formC/<str:selector>", views.formC, name="formC"),
    path("Weekly/formD/<str:selector>", views.formD, name="formD"),
    path("Daily/formE/<str:selector>", views.formE, name="formE"),
    path("Weekly/formF1/<str:selector>", views.formF1, name="formF1"),
    path("Weekly/formF2/<str:selector>", views.formF2, name="formF2"),
    path("Weekly/formF3/<str:selector>", views.formF3, name="formF3"),
    path("Weekly/formF4/<str:selector>", views.formF4, name="formF4"),
    path("Weekly/formF5/<str:selector>", views.formF5, name="formF5"),
    path("Weekly/formF6/<str:selector>", views.formF6, name="formF6"),
    path("Weekly/formF7/<str:selector>", views.formF7, name="formF7"),
    path("Weekly/formG1/<str:selector>", views.formG1, name="formG1"),
    path("Monthly/formG2/<str:selector>", views.formG2, name="formG2"),
    path("Weekly/formH/<str:access_page>", views.formH, name="formH"),
    path("Daily/formI/<str:selector>", views.formI, name="formI"),
    path("Daily/formL/<str:access_page>", views.formL, name="formL"),
    path("Daily/formM/<str:selector>", views.formM, name="formM"),
    path("Monthly/formN/<str:selector>", views.formN, name="formN"),
    path("Weekly/formO/<str:selector>/<str:weekend_day>", views.formO, name="formO"),
    path("Weekly/formP/<str:selector>/<str:weekend_day>", views.formP, name="formP"),
    path("Monthly/spill_kits/<str:access_page>", views.spill_kits, name="spill_kits"),
    path("Quarterly/quarterly_trucks/<str:selector>", views.quarterly_trucks, name="quarterly_trucks"),
    

    path("weekly_forms", views.weekly_forms, name="weekly_forms"),
    path("pt_admin1", views.pt_admin1_view, name="pt_admin1"),
    path("pt_mth_input", views.pt_mth_input, name="pt_mth_input"),
    path("method303_rolling_avg", views.method303_rolling_avg, name="rolling_avg"),
    path("admin_data", views.admin_data_view, name="admin_data"),

    path("c_dashboard", views.client_dashboard_view, name="c_dashboard"),

    # path("pdf/<form>/<date>/", views.render_pdf_view, name="formA1_pdf"),

    # path("calendar", views.CalendarView.as_view(), name='calendar'),
    
    
    # path('pdf_view', views.render_pdf_view, name="pdf_view"),
    path('printIndex/<str:formName>/<str:formDate>', views.form_PDF, name='printIndex'),
    path('PrintSelect', views.printSelect, name='PrintSelect'),
    #path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    #path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
]
