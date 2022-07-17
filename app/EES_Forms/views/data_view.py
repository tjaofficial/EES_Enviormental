from django.shortcuts import render
import datetime
from ..models import formA3_model, formA2_model, formA1_readings_model, user_profile_model, daily_battery_profile_model, formA5_readings_model, formA5_model, Forms

back = Forms.objects.filter(form__exact='Incomplete Forms')
profile = user_profile_model.objects.all()


def pt_admin1_view(request):
    client = False
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True

    today = datetime.date.today()
    now = datetime.datetime.now()
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]

    reads = formA5_readings_model.objects.all()
    data = formA5_model.objects.all()
    # add_days = datetime.timedelta(days=91)

    def all_ovens(reads):
        A = []
        for p in reads:
            date = p.form.date
            list = [p.o1, p.o2, p.o3, p.o4]
            year = date.year
            month = date.month
            day = date.day

            form_date = datetime.datetime(year, month, day)
            added_date = form_date + datetime.timedelta(days=91)
            due_date = added_date - datetime.datetime.now()
            
            for q in list:
                if len(str(q)) == 1:
                    oven = "0" + str(q)
                else:
                    oven = q

                A.append((oven, p.form.date, added_date.date, due_date.days))
        return A

    all_read_ovens = all_ovens(reads)
    func = lambda x: (x[0], x[1])
    sort = sorted(all_read_ovens, key=func, reverse=True)
   
    def final(sort):
        B = []
        i = 1
        for new in sort:
            B.append(new)

        for x in sort:
            for y in range(i, len(sort)):
                check_instance = sort[y]
                if check_instance[0] == x[0]:
                    if check_instance in B:
                        B.remove(check_instance)
            i += 1
            
        for oven in B:
            for n in range(1, 86):
                if oven[0] == n:
                    exist = True
                    break
                else:
                    exist = False
            if not exist:
                B.append((oven, 'N/A', 0, 0))
                
                    
        return B
    cool = final(sort)
    print(cool)
    def overdue_30(cool):
        C = []
        for x in cool:
            if x[3] <= 30:
                C.append(x)
        return C

    def overdue_10(cool):
        D = []
        for x in cool:
            if x[3] <= 10:
                D.append(x)
        return D

    def overdue_5(cool):
        E = []
        for x in cool:
            if x[3] <= 5:
                E.append(x)
        return E

    def overdue_closest(cool):
        F = []

        func2 = lambda R: (R[3])
        sort2 = sorted(cool, key=func2)
        most_recent = sort2[0][3]

        for x in sort2:
            if x[3] == most_recent:
                F.append(x)
        return F

    od_30 = overdue_30(cool)
    od_10 = overdue_10(cool)
    od_5 = overdue_5(cool)
    od_recent = overdue_closest(cool)

    return render(request, "ees_forms/PushTravels.html", {
        "now": now, 'todays_log': todays_log, "back": back, 'reads': reads, 'data': data, 'cool': cool, 'od_30': od_30, 'od_10': od_10, 'od_5': od_5, 'od_recent': od_recent, "today": today, 'profile': profile, 'client': client,
    })


def pt_mth_input(request):
    submitted_ordered = formA5_readings_model.objects.all()
    now = datetime.datetime.now()
    today = datetime.date.today()

    def pt_sort(submitted_ordered):
        A = []
        for x in submitted_ordered:
            date = x.form.date
            i = 1
            h = i+1
            j = i+2
            k = i+4
            A.append((
                date,
                x.o1,
                x.o1_start,
                x.o1_1_reads,
                x.o1_2_reads,
                x.o1_3_reads,
                x.o1_4_reads,
                x.o1_5_reads,
                x.o1_6_reads,
                x.o1_7_reads,
                x.o1_8_reads,
                x.o1_9_reads,
                x.o1_10_reads,
                x.o1_11_reads,
                x.o1_12_reads,
                x.o1_13_reads,
                x.o1_14_reads,
                x.o1_15_reads,
                x.o1_16_reads,
                'lightblue',
                i
            ))
            A.append((
                date,
                x.o2,
                x.o2_start,
                x.o2_1_reads,
                x.o2_2_reads,
                x.o2_3_reads,
                x.o2_4_reads,
                x.o2_5_reads,
                x.o2_6_reads,
                x.o2_7_reads,
                x.o2_8_reads,
                x.o2_9_reads,
                x.o2_10_reads,
                x.o2_11_reads,
                x.o2_12_reads,
                x.o2_13_reads,
                x.o2_14_reads,
                x.o2_15_reads,
                x.o2_16_reads,
                'skyblue',
                h
            ))
            A.append((
                date,
                x.o3,
                x.o3_start,
                x.o3_1_reads,
                x.o3_2_reads,
                x.o3_3_reads,
                x.o3_4_reads,
                x.o3_5_reads,
                x.o3_6_reads,
                x.o3_7_reads,
                x.o3_8_reads,
                x.o3_9_reads,
                x.o3_10_reads,
                x.o3_11_reads,
                x.o3_12_reads,
                x.o3_13_reads,
                x.o3_14_reads,
                x.o3_15_reads,
                x.o3_16_reads,
                'lightblue',
                j
            ))
            A.append((
                date,
                x.o4,
                x.o4_start,
                x.o4_1_reads,
                x.o4_2_reads,
                x.o4_3_reads,
                x.o4_4_reads,
                x.o4_5_reads,
                x.o4_6_reads,
                x.o4_7_reads,
                x.o4_8_reads,
                x.o4_9_reads,
                x.o4_10_reads,
                x.o4_11_reads,
                x.o4_12_reads,
                x.o4_13_reads,
                x.o4_14_reads,
                x.o4_15_reads,
                x.o4_16_reads,
                'skyblue',
                k
            ))
            i += 4
        return A

    new_A5_list = pt_sort(submitted_ordered)

    func = lambda x: (x[0])
    sort = sorted(new_A5_list, key=func, reverse=True)

    return render(request, "ees_forms/pt_mth_input.html", {
        "now": now, "back": back, "today": today, 'submitted_ordered': submitted_ordered, 'sort': sort, 'profile': profile,
    })


def method303_rolling_avg(request):
    daily_prof = daily_battery_profile_model.objects.all().order_by('date_save')
    todays_log = daily_prof[0]
    now = datetime.datetime.now()
    today = datetime.date.today()
    A = []

    def form_compile(daily_prof):
        formA1 = formA1_readings_model.objects.all()
        formA2 = formA2_model.objects.all()
        formA3 = formA3_model.objects.all()
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

                                    A.append((i, date_select.date_save, A1.c1_sec, A1.c2_sec, A1.c3_sec, A1.c4_sec, A1.c5_sec, A2.inop_ovens, A2.doors_not_observed, A2.leaking_doors, A3.inop_ovens, A3.l_not_observed, A3.l_leaks, A3.om_not_observed, A3.om_leaks))
                                    print(i)
                                    i += 1
        return A

    list_of_records = form_compile(daily_prof)

    return render(request, "ees_forms/method303_rolling_avg.html", {
        "now": now, 'todays_log': todays_log, "back": back, "today": today, 'list_of_records': list_of_records, 'profile': profile,
    })
