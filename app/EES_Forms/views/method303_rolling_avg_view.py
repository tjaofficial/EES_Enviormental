from django.shortcuts import render
from ..models import Forms, user_profile_model, daily_battery_profile_model, form1_readings_model, form2_model, form3_model, bat_info_model
import datetime
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR

back = Forms.objects.filter(form__exact='Incomplete Forms')
profile = user_profile_model.objects.all()


def method303_rolling_avg(request, facility):
    unlock = False
    client = False
    supervisor = False
    if request.user.groups.filter(name=OBSER_VAR):
        unlock = True
    if request.user.groups.filter(name=CLIENT_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    options = bat_info_model.objects.all()
    now = datetime.datetime.now()
    today = datetime.date.today()
    daily_prof = daily_battery_profile_model.objects.all().order_by('date_save')
    todays_log = daily_prof[0]

    A = []

    def form_compile(daily_prof):
        formA1 = form1_readings_model.objects.all()
        formA2 = form2_model.objects.all()
        formA3 = form3_model.objects.all()
        i = 1
        for date_select in daily_prof:
            for logA1 in formA1:
                if str(date_select.date_save) == str(logA1.form.date):
                    A1 = logA1

                    for logA2 in formA2:
                        if date_select.date_save == logA2.date:
                            A2 = logA2

                            for logA3 in formA3:
                                if date_select.date_save == logA3.date:
                                    A3 = logA3

                                    A.append((
                                        i, date_select.date_save, 
                                        A1.c1_sec, 
                                        A1.c2_sec, 
                                        A1.c3_sec, 
                                        A1.c4_sec, 
                                        A1.c5_sec, 
                                        A2.inop_ovens, 
                                        A2.doors_not_observed, 
                                        A2.leaking_doors, 
                                        A3.inop_ovens, 
                                        A3.l_not_observed, 
                                        A3.l_leaks, 
                                        A3.om_not_observed, 
                                        A3.om_leaks
                                    ))
                                    i += 1
        return A

    list_of_records = form_compile(daily_prof)

    return render(request, "ees_forms/method303_rolling_avg.html", {
        'options': options, 'facility': facility, "now": now, 'todays_log': todays_log, "back": back, "today": today, 'list_of_records': list_of_records, 'profile': profile, 'client': client, "supervisor": supervisor, "unlock": unlock, 
    })
