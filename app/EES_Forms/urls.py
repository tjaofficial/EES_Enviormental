from django.urls import path # type: ignore
from . import views

urlpatterns = [
    ##---MAIN DASHBOARDS----
    path("<str:facility>/dashboard", views.IncompleteForms, name="IncompleteForms"),
    path("<str:facility>/default-dashboard", views.default_dashboard, name="defaultDash"),
    path("<str:facility>/sup_dashboard", views.sup_dashboard_view, name='sup_dashboard'),
    path("adminDash/<str:selector>", views.adminDash, name="adminDash"),
    path("<str:facility>/c_dashboard", views.client_dashboard_view, name="c_dashboard"),
    
    ##---ADMIN PAGES -------
    path("admin-pages/addFAQ", views.admin_add_FAQ_view, name="adminFAQ"),
    path('api/get_revenue', views.get_monthly_revenue, name='get_revenue'),
    path('api/get_subscriptions/', views.get_subscriptions, name='get_subscriptions'),
    
    ##---LANDNG PAGES-----
    path("FAQ", views.FAQ_view, name="FAQ"),
    path("TAC", views.terms_and_conditions_view, name="TAC"),
    path("privacy-policy", views.privacy_policy_view, name="privacyPolicy"),
    path("included-forms", views.included_forms_view, name="includedForms"),
    path("contact-mp", views.landing_contact_view, name="landingContact"),
    path("register", views.landingRegister, name="register"),
    path("login", views.login_view, name="Login"),
    path("register_company", views.registerCompany, name="companyReg"),
    path("logout", views.logout_view, name="Logout"),
    path("activate/<str:uidb64>/<str:token>/", views.activate_view, name="activate"),
    path("reset/<str:uidb64>/<str:token>/", views.reset_password_activate_view, name="reset"),
    path("request-password", views.request_password_view, name='requestPassword'),
    path("change-password", views.main_change_password, name='mainPasswordChange'),
    
    ##---SUPERVISOR PAGES-----
    path("<str:facility>/Register/<str:access_page>", views.register_view, name="Register"),
    path("<str:facility>/password", views.change_password, name='PasswordChange'),
    path("<str:facility>/request-form", views.form_request_view, name='requestForm'),
    path("<str:facility>/facilitylist", views.facilityList, name="facilityList"),
    path("<str:facility>/facilityFormSettings/<str:fsID>/<str:packetID>/<str:formLabel>", views.facility_form_settings, name="facilityFormSettings"),
    path("<str:facility>/profileEdits/<str:userID>", views.profile_edit_view, name="profileEdits"),
    path('<str:facility>/form-select/add-forms', views.Add_Forms, name='addingForms'),
    
    ##--ACCOUNT SETTINGS-----
    path("<str:facility>/account", views.sup_account_view, name="Account"),
    path("<str:facility>/account/payment-method/<str:action>/<str:planId>/<str:seats>", views.sup_card_update, name="cardUpdate"),
    path("billing/payment-method/<str:planId>/<str:seats>", views.landing_addCard_view, name="cardAdd"),
    path("<str:facility>/account/subscription/<str:selector>", views.sup_select_subscription, name="subscriptionSelect"),
    path("<str:facility>/account/update/<str:selector>", views.sup_update_account, name="accountUpdate"),
    path("<str:facility>/subscription/change", views.sup_change_subscription, name="subscriptionChange"),
    path("<str:facility>/subscription/billing", views.sup_billing_history, name="billingHistory"),
    path("<str:facility>/account/facility-settings/<int:facilityID>/<str:selector>", views.sup_facility_settings, name="selectedFacilitySettings"),
    
    ##---BILLING
    path("billing/<str:step>", views.billing_view, name="billing"),
    
    path("<str:facility>/DeleteProf/<str:profile_pic_id>", views.delete_prof_pic_view, name="DeleteProf"),
    path('<str:facility>/about', views.about_view, name='about'),
    path('<str:facility>/safety', views.safety_view, name='safety'),
    path('<str:facility>/settings', views.settings_view, name='settings'),
    path('<str:facility>/<str:packet>/form_select', views.facilityForm, name='facilityForms'),
    
    ##---OBSERVER PAGES-------
    path("<str:facility>/facility/", views.facility_select_view, name="facilitySelect"),
    path("<str:facility>/daily_battery_profile/<str:access_page>/<str:date>", views.daily_battery_profile_view, name="daily_battery_profile"),
    path("<str:facility>/signature",views.signature,name="signature"),

    ##---SHARED PAGES-----
    path("<str:facility>/profile/<str:access_page>", views.profile, name="profile"),
    path("<str:facility>/Corrective-Action", views.corrective_action_view, name="Corrective-Action"),
    path("<str:facility>/schedule_view", views.schedule_view, name="Schedule"),
    path("<str:facility>/schedule/<int:year>/<str:month>", views.calendar_view, name="Calendar"),
    path("<str:facility>/add_event", views.event_add_view, name="Add Event"),
    path("<str:facility>/event_detail/<int:event_id>/<str:access_page>", views.event_detail_view, name="Event Details"),
    path('<str:facility>/archive', views.archive_view, name='archive'),
    path('<str:facility>/search_forms/<str:access_page>', views.search_forms_view, name='search_forms'),
    path("<str:facility>/issues_view/<int:fsID>/<str:form_date>/<str:access_page>", views.issues_view, name="issues_view"),
    path("<str:facility>/Contacts", views.shared_contacts_view, name="Contacts"),
    path("<str:facility>/Sop", views.sop_view, name="Sop"),
    path('delete_selected_sops/<str:facility>/', views.delete_selected_sops, name='delete_selected_sops'),
    path("<str:facility>/DeleteSop/<str:sop_id>", views.delete_sop_view, name="DeleteSop"),
    path("<str:facility>/UpdateSop/<str:sop_id>", views.update_sop_view, name="UpdateSop"),
    path("<str:facility>/progress/<str:section>", views.formsProgress, name="Progress"),

    ##---FORMS
    path("<str:facility>/Daily/1/<int:fsID>/<str:selector>", views.form1, name="form1"),
    path("<str:facility>/Daily/2/<int:fsID>/<str:selector>", views.form2, name="form2"),
    path("<str:facility>/Daily/3/<int:fsID>/<str:selector>", views.form3, name="form3"),
    path("<str:facility>/Daily/4/<int:fsID>/<str:selector>", views.form4, name="form4"),
    path("<str:facility>/Daily/5/<int:fsID>/<str:selector>", views.form5, name="form5"),
    path("<str:facility>/Daily/6/<int:fsID>/<str:selector>", views.form6, name="form6"),
    path("<str:facility>/Daily/7/<int:fsID>/<str:selector>", views.form7, name="form7"),
    path("<str:facility>/Weekly/8/<int:fsID>/<str:selector>", views.form8, name="form8"),
    path("<str:facility>/Daily/9/<int:fsID>/<str:selector>", views.form9, name="form9"),
    path("<str:facility>/Weekly/F1/<int:fsID>/<str:selector>", views.formF1, name="formF1"),
    path("<str:facility>/Weekly/F2/<int:fsID>/<str:selector>", views.formF2, name="formF2"),
    path("<str:facility>/Weekly/F3/<int:fsID>/<str:selector>", views.formF3, name="formF3"),
    path("<str:facility>/Weekly/F4/<int:fsID>/<str:selector>", views.formF4, name="formF4"),
    path("<str:facility>/Weekly/F5/<int:fsID>/<str:selector>", views.formF5, name="formF5"),
    path("<str:facility>/Weekly/F6/<int:fsID>/<str:selector>", views.formF6, name="formF6"),
    path("<str:facility>/Weekly/F7/<int:fsID>/<str:selector>", views.formF7, name="formF7"),
    path("<str:facility>/Weekly/17/<int:fsID>/<str:selector>", views.form17, name="form17"),
    path("<str:facility>/Monthly/18/<int:fsID>/<str:selector>", views.form18, name="form18"),
    path("<str:facility>/Weekly/19/<int:fsID>/<str:selector>", views.form19, name="form19"),
    path("<str:facility>/Daily/20/<int:fsID>/<str:selector>", views.form20, name="form20"),
    path("<str:facility>/Daily/21/<int:fsID>/<str:selector>", views.form21, name="form21"),
    path("<str:facility>/Daily/22/<int:fsID>/<str:selector>", views.form22, name="form22"),
    path("<str:facility>/Monthly/23/<int:fsID>/<str:selector>", views.form23, name="form23"),
    path("<str:facility>/Daily/24/<int:fsID>/<str:selector>/<str:weekend_day>", views.form24, name="form24"),
    path("<str:facility>/Daily/25/<int:fsID>/<str:selector>/<str:weekend_day>", views.form25, name="form25"),
    path("<str:facility>/Monthly/26/inventory/<int:fsID>/<str:month>/<int:skNumber>/<str:selector>", views.form26, name="skInventory"),
    path("<str:facility>/Quarterly/27/<int:fsID>/<str:selector>", views.form27, name="form27"),
    path("<str:facility>/Monthly/29/<int:fsID>/<str:selector>", views.form29, name="form29"),
    path("<str:facility>/Weekly/30/<int:fsID>/<str:selector>", views.form30, name="form30"),
    path("<str:facility>/Monthly/31/<int:fsID>/<str:selector>", views.form31, name="form31"),
    path("api/get-inop/", views.inop_check_form_1, name="get-inop"),
    path("get-existing-form/", views.get_existing_form, name="get_existing_form"),
    path("get-submitted-areas/", views.get_submitted_areas, name="get_submitted_areas"),

    
    ##---COKE_BATTERY_DATA
    path("weekly_forms", views.weekly_forms, name="weekly_forms"),
    path("<str:facility>/pt_admin1", views.pt_admin1_view, name="pt_admin1"),
    path("<str:facility>/pt_mth_input", views.pt_mth_input, name="pt_mth_input"),
    path("<str:facility>/method303_rolling_avg", views.method303_rolling_avg, name="rolling_avg"),
    path("<str:facility>/admin_data", views.admin_data_view, name="admin_data"),

    ##---PRINTING
    path('<str:facility>/printIndex/<str:type>/<str:formGroup>/<str:formIdentity>/<str:formDate>', views.form_PDF, name='printIndex'),
    path('<str:facility>/PrintSelect', views.printSelect, name='PrintSelect'),
    path('<str:facility>/calSelect/<str:type>/<str:forms>/<int:year>/<int:month>', views.calSelect, name='CalSelect'),
    path('billing-history/invoice/<str:invoiceID>', views.invoices, name='invoicePDF'),

    # path("pdf/<form>/<date>/", views.render_pdf_view, name="formA1_pdf"),

    # path("calendar", views.CalendarView.as_view(), name='calendar'),
    
    
    # path('pdf_view', views.render_pdf_view, name="pdf_view"),
    #path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    #path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
]
