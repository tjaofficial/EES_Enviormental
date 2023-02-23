from django.urls import path
from . import views

urlpatterns = [
    
    
    path("<str:facility>/dashboard", views.IncompleteForms, name="IncompleteForms"),
    path("<str:facility>/sup_dashboard", views.sup_dashboard_view, name='sup_dashboard'),

    path("<str:facility>/Register/<str:access_page>", views.register_view, name="Register"),
    path("login", views.login_view, name="Login"),
    path("register", views.landingRegister, name="register"),
    path("register_company", views.registerCompany, name="companyReg"),
    path("no_registration", views.valid_account_logout, name="no_registration"),
    path("logout", views.logout_view, name="Logout"),
    path('<str:facility>/profile_redirect', views.profile_redirect, name='profile_redirect'),
    path("<str:facility>/password", views.change_password, name='PasswordChange'),
    path("adminDash", views.adminDash, name="adminDash"),
    
    path("billing/<str:step>", views.billing, name="billing"),

    path("<str:facility>/profile/<str:access_page>", views.profile, name="profile"),
    path("<str:facility>/DeleteProf/<str:profile_pic_id>", views.delete_prof_pic_view, name="DeleteProf"),
    path('<str:facility>/about', views.about_view, name='about'),
    path('<str:facility>/safety', views.safety_view, name='safety'),
    path('<str:facility>/settings', views.settings_view, name='settings'),
    
    path("facility/", views.facility_select_view, name="facilitySelect"),
    path("<str:facility>/daily_battery_profile/<str:access_page>/<str:date>", views.daily_battery_profile_view, name="daily_battery_profile"),
    path("<str:facility>/signature",views.signature,name="signature"),

    path("<str:facility>/Corrective-Action", views.corrective_action_view, name="Corrective-Action"),
    path("<str:facility>/schedule_view", views.schedule_view, name="Schedule"),
    path("<str:facility>/schedule/<int:year>/<str:month>", views.calendar_view, name="Calendar"),
    path("<str:facility>/add_event", views.event_add_view, name="Add Event"),
    path("<str:facility>/event_detail/<int:event_id>/<str:access_page>", views.event_detail_view, name="Event Details"),
    path('<str:facility>/archive', views.archive_view, name='archive'),
    path('<str:facility>/search_forms/<str:access_page>', views.search_forms_view, name='search_forms'),
    path("<str:facility>/issues_view/<str:form_name>/<str:form_date>/<str:access_page>", views.issues_view, name="issues_view"),
    path("<str:facility>/Contacts", views.shared_contacts_view, name="Contacts"),
    path("<str:facility>/Sop", views.sop_view, name="Sop"),
    path("<str:facility>/DeleteSop/<str:sop_id>", views.delete_sop_view, name="DeleteSop"),
    path("<str:facility>/UpdateSop/<str:sop_id>", views.update_sop_view, name="UpdateSop"),
    path("<str:facility>/facilitylist", views.facilityList, name="facilityList"),


    path("<str:facility>/Daily/formA1/<str:selector>", views.formA1, name="formA1"),
    path("<str:facility>/Daily/formA2/<str:selector>", views.formA2, name="formA2"),
    path("<str:facility>/Daily/formA3/<str:selector>", views.formA3, name="formA3"),
    path("<str:facility>/Daily/formA4/<str:selector>", views.formA4, name="formA4"),
    path("<str:facility>/Daily/formA5/<str:selector>", views.formA5, name="formA5"),
    path("<str:facility>/Daily/formB/<str:selector>", views.formB, name="formB"),
    path("<str:facility>/Daily/formC/<str:selector>", views.formC, name="formC"),
    path("<str:facility>/Weekly/formD/<str:selector>", views.formD, name="formD"),
    path("<str:facility>/Daily/formE/<str:selector>", views.formE, name="formE"),
    path("<str:facility>/Weekly/formF1/<str:selector>", views.formF1, name="formF1"),
    path("<str:facility>/Weekly/formF2/<str:selector>", views.formF2, name="formF2"),
    path("<str:facility>/Weekly/formF3/<str:selector>", views.formF3, name="formF3"),
    path("<str:facility>/Weekly/formF4/<str:selector>", views.formF4, name="formF4"),
    path("<str:facility>/Weekly/formF5/<str:selector>", views.formF5, name="formF5"),
    path("<str:facility>/Weekly/formF6/<str:selector>", views.formF6, name="formF6"),
    path("<str:facility>/Weekly/formF7/<str:selector>", views.formF7, name="formF7"),
    path("<str:facility>/Weekly/formG1/<str:selector>", views.formG1, name="formG1"),
    path("<str:facility>/Monthly/formG2/<str:selector>", views.formG2, name="formG2"),
    path("<str:facility>/Weekly/formH/<str:selector>", views.formH, name="formH"),
    path("<str:facility>/Daily/formI/<str:selector>", views.formI, name="formI"),
    path("<str:facility>/Daily/formL/<str:selector>", views.formL, name="formL"),
    path("<str:facility>/Daily/formM/<str:selector>", views.formM, name="formM"),
    path("<str:facility>/Monthly/formN/<str:selector>", views.formN, name="formN"),
    path("<str:facility>/Weekly/formO/<str:selector>/<str:weekend_day>", views.formO, name="formO"),
    path("<str:facility>/Weekly/formP/<str:selector>/<str:weekend_day>", views.formP, name="formP"),
    path("<str:facility>/Monthly/spill_kits/<str:selector>", views.spill_kits, name="spill_kits"),
    path("<str:facility>/Quarterly/quarterly_trucks/<str:selector>", views.quarterly_trucks, name="quarterly_trucks"),
    

    path("weekly_forms", views.weekly_forms, name="weekly_forms"),
    path("<str:facility>/pt_admin1", views.pt_admin1_view, name="pt_admin1"),
    path("<str:facility>/pt_mth_input", views.pt_mth_input, name="pt_mth_input"),
    path("<str:facility>/method303_rolling_avg", views.method303_rolling_avg, name="rolling_avg"),
    path("<str:facility>/admin_data", views.admin_data_view, name="admin_data"),

    path("c_dashboard", views.client_dashboard_view, name="c_dashboard"),

    # path("pdf/<form>/<date>/", views.render_pdf_view, name="formA1_pdf"),

    # path("calendar", views.CalendarView.as_view(), name='calendar'),
    
    
    # path('pdf_view', views.render_pdf_view, name="pdf_view"),
    path('<str:facility>/printIndex/<str:formName>/<str:formDate>', views.form_PDF, name='printIndex'),
    path('<str:facility>/PrintSelect', views.printSelect, name='PrintSelect'),
    #path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    #path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
]
