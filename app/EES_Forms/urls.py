from django.urls import path
from . import views

urlpatterns = [
    
    ##---MAIN DASHBOARDS----
    path("<str:facility>/dashboard", views.IncompleteForms, name="IncompleteForms"),
    path("<str:facility>/sup_dashboard", views.sup_dashboard_view, name='sup_dashboard'),
    path("adminDash", views.adminDash, name="adminDash"),
    path("<str:facility>/c_dashboard", views.client_dashboard_view, name="c_dashboard"),
    
    ##---REGISTRATION-----
    path("<str:facility>/Register/<str:access_page>", views.register_view, name="Register"),
    path("login", views.login_view, name="Login"),
    path("register", views.landingRegister, name="register"),
    path("activate/<str:uidb64>/<str:token>/", views.activate_view, name="activate"),
    path("register_company", views.registerCompany, name="companyReg"),
    path("no_registration", views.valid_account_logout, name="no_registration"),
    path("logout", views.logout_view, name="Logout"),
    path("request-password", views.request_password_view, name='requestPassword'),
    path("change-password", views.main_change_password, name='mainPasswordChange'),
    path("<str:facility>/password", views.change_password, name='PasswordChange'),
    path("<str:facility>/profile/<str:access_page>", views.profile, name="profile"),
    
    ##--ACCOUNT SETTINGS-----
    path("<str:facility>/account", views.sup_account_view, name="Account"),
    path("<str:facility>/account/payment-method/<str:action>/<str:planId>/<str:seats>", views.sup_card_update, name="cardUpdate"),
    path("<str:facility>/account/subscription/<str:selector>", views.sup_select_subscription, name="subscriptionSelect"),
    path("<str:facility>/account/update/<str:selector>", views.sup_update_account, name="accountUpdate"),
    path("<str:facility>/subscription/change", views.sup_change_subscription, name="subscriptionChange"),
    path("<str:facility>/subscription/billing", views.sup_billing_history, name="billingHistory"),
    
    ##---BILLING
    path("billing/<str:step>", views.billing, name="billing"),

    path("<str:facility>/DeleteProf/<str:profile_pic_id>", views.delete_prof_pic_view, name="DeleteProf"),
    path('<str:facility>/about', views.about_view, name='about'),
    path('<str:facility>/safety', views.safety_view, name='safety'),
    path('<str:facility>/settings', views.settings_view, name='settings'),
    path('<str:facility>/form_select', views.facilityForm, name='facilityForms'),
    
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
    path("<str:facility>/progress/<str:section>", views.formsProgress, name="Progress"),

    ##---FORMS
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
    path("<str:facility>/Monthly/spill_kits/<str:month>/<int:skNumber>/<str:selector>", views.spill_kits_inventory_form, name="skInventory"),
    path("<str:facility>/Quarterly/quarterly_trucks/<str:selector>", views.quarterly_trucks, name="quarterly_trucks"),
    
    ##---COKE_BATTERY_DATA
    path("weekly_forms", views.weekly_forms, name="weekly_forms"),
    path("<str:facility>/pt_admin1", views.pt_admin1_view, name="pt_admin1"),
    path("<str:facility>/pt_mth_input", views.pt_mth_input, name="pt_mth_input"),
    path("<str:facility>/method303_rolling_avg", views.method303_rolling_avg, name="rolling_avg"),
    path("<str:facility>/admin_data", views.admin_data_view, name="admin_data"),

    ##---PRINTING
    path('<str:facility>/printIndex/<str:formGroup>/<str:formIdentity>/<str:formDate>', views.form_PDF, name='printIndex'),
    path('<str:facility>/PrintSelect', views.printSelect, name='PrintSelect'),
    path('<str:facility>/calSelect/<str:type>/<str:forms>/<int:year>/<int:month>', views.calSelect, name='CalSelect'),

    # path("pdf/<form>/<date>/", views.render_pdf_view, name="formA1_pdf"),

    # path("calendar", views.CalendarView.as_view(), name='calendar'),
    
    
    # path('pdf_view', views.render_pdf_view, name="pdf_view"),
    #path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    #path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
]
