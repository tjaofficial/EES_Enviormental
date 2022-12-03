from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import issues_model, daily_battery_profile_model, formA1_model, formA1_readings_model, Forms
from ..forms import formA1_form, formA1_readings_form
from django.conf import settings
import os
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formA1(request, selector):
    formName = "A1"
    existing = False
    unlock = False
    client = False
    search = False
    admin = False
    if request.user.groups.filter(name='SGI Technician'):
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        admin = True
    now = datetime.datetime.now()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')

    org = formA1_model.objects.all().order_by('-date')
    org2 = formA1_readings_model.objects.all().order_by('-form')

    full_name = request.user.get_full_name()

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        print('CHECK 1')
        todays_log = daily_prof[0]
        print('CHECK 2')
        if selector != 'form':
            for x in org:
                if str(x.date) == str(selector):
                    database_model = x
            data = database_model
            for x in org2:
                if str(x.form.date) == str(selector):
                    database_model2 = x
            readings = database_model2
            existing = True
            search = True
        elif len(org) > 0 and len(org2) > 0:
            database_form = org[0]
            database_form2 = org2[0]

            if now.month == todays_log.date_save.month:
                if now.day == todays_log.date_save.day:
                    if todays_log.date_save == database_form.date:
                        existing = True
                else:
                    batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                    return redirect(batt_prof)
            else:
                batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                return redirect(batt_prof)
        if search:
            database_form = ''
        else:
            if existing:
                initial_data = {
                    'date': database_form.date,
                    'observer': database_form.observer,
                    'crew': database_form.crew,
                    'foreman': database_form.foreman,
                    'start': database_form.start,
                    'stop': database_form.stop,
                    'c1_no': database_form2.c1_no,
                    'c2_no': database_form2.c2_no,
                    'c3_no': database_form2.c3_no,
                    'c4_no': database_form2.c4_no,
                    'c5_no': database_form2.c5_no,
                    'c1_start': database_form2.c1_start,
                    'c2_start': database_form2.c2_start,
                    'c3_start': database_form2.c3_start,
                    'c4_start': database_form2.c4_start,
                    'c5_start': database_form2.c5_start,
                    'c1_stop': database_form2.c1_stop,
                    'c2_stop': database_form2.c2_stop,
                    'c3_stop': database_form2.c3_stop,
                    'c4_stop': database_form2.c4_stop,
                    'c5_stop': database_form2.c5_stop,
                    'c1_sec': database_form2.c1_sec,
                    'c2_sec': database_form2.c2_sec,
                    'c3_sec': database_form2.c3_sec,
                    'c4_sec': database_form2.c4_sec,
                    'c5_sec': database_form2.c5_sec,
                    'c1_comments': database_form2.c1_comments,
                    'c2_comments': database_form2.c2_comments,
                    'c3_comments': database_form2.c3_comments,
                    'c4_comments': database_form2.c4_comments,
                    'c5_comments': database_form2.c5_comments,
                    'larry_car': database_form2.larry_car,
                    'comments': database_form2.comments,
                    'total_seconds': database_form2.total_seconds,
                }
                readings = formA1_readings_form(initial=initial_data)
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name,
                    'crew': todays_log.crew,
                    'foreman': todays_log.foreman,
                }
                readings = formA1_readings_form()

            data = formA1_form(initial=initial_data)
        if request.method == "POST":
            if existing:
                form = formA1_form(request.POST, instance=database_form)
                reads = formA1_readings_form(request.POST, instance=database_form2)
            else:
                form = formA1_form(request.POST)
                reads = formA1_readings_form(request.POST)

            A_valid = form.is_valid()
            B_valid = reads.is_valid()

            if A_valid and B_valid:
                A = form.save()
                B = reads.save(commit=False)
                B.form = A
                B.save()

                finder = issues_model.objects.filter(date=A.date, form='A-1')
            #     if B.comments not in {'-', 'n/a', 'N/A'}:
            #         issue_page = '../../issues_view/A-1/' + str(database_form.date) + '/form'

            #         return redirect (issue_page)
                sec = {B.c1_sec, B.c2_sec, B.c3_sec, B.c4_sec, B.c5_sec}
                for x in sec:
                    if 10 <= x:
                        if finder:
                            issue_page = '../../issues_view/A-1/' + str(database_form.date) + '/issue'
                        else:
                            issue_page = '../../issues_view/A-1/' + str(database_form.date) + '/form'

                        return redirect(issue_page)
                    else:
                        if B.total_seconds >= 55:
                            if finder:
                                issue_page = '../../issues_view/A-1/' + str(database_form.date) + '/issue'
                            else:
                                issue_page = '../../issues_view/A-1/' + str(database_form.date) + '/form'

                            return redirect(issue_page)
                done = Forms.objects.filter(form='A-1')[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()

                return redirect('IncompleteForms')
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Daily/formA1.html", {
        'admin': admin, "back": back, 'todays_log': todays_log, 'data': data, 'readings': readings, 'formName': formName, 'selector': selector, "client": client, 'unlock': unlock
    })

def time_change(time):
    hourNum = int(str(time)[0:2])
    minNum = str(time)[3:5]
    timeLabel = 'AM'
    if hourNum > 12:
        newHourNum = str(hourNum - 12)
        timeLabel = 'PM'
        newTime = newHourNum + ':' + minNum + ' ' + timeLabel
    elif hourNum == 00:
        newHourNum = '12'
        newTime = newHourNum + ':' + minNum + ' ' + timeLabel
    else:
        newTime = str(hourNum) + ':' + minNum + ' ' + timeLabel
    return newTime
        

def formA1_pdf(request, formDate):
    org = formA1_model.objects.all().order_by('-date')
    org2 = formA1_readings_model.objects.all().order_by('-form')
    print (time_change('00:59:00'))
    for x in org:
        if str(x.date) == str(formDate):
            database_model = x
    data = database_model
    for x in org2:
        if str(x.form.date) == str(formDate):
            database_model2 = x
    readings = database_model2
    print(str(data.start)[0:5])
    styles = getSampleStyleSheet()
    fileName = "Form_Print.pdf"
    documentTitle = 'NewPrint'
    title = 'Method 303 Charging - Form (A-1)'
    subTitle = 'Facility Name: EES Coke Battery LLC'
    inspectorDate = Paragraph('<para align=center><b>Inspectors Name:</b>&#160;&#160;' + data.observer + '&#160;&#160;&#160;&#160;&#160;<b>Date:</b>&#160;&#160;' + str(data.date) + '</para>', styles['Normal'])
    batNumCrewForeman = Paragraph('<para align=center><b>Battery No.:</b> 5&#160;&#160;&#160;&#160;&#160;<b>Crew:</b>&#160;&#160;' + data.crew + '&#160;&#160;&#160;&#160;&#160;<b>Battery Forman:</b>&#160;&#160;' + data.foreman + '</para>', styles['Normal'])
    startEnd = Paragraph('<para align=center><b>Start Time:</b>&#160;&#160;' + time_change(data.start) + '&#160;&#160;&#160;&#160;&#160;<b>End Time:</b>&#160;&#160;' + time_change(data.stop) + '</para>', styles['Normal'])
    
    text1 = Paragraph(readings.c1_comments,
              styles['Normal'])
    text2 = Paragraph(readings.c2_comments,
              styles['Normal'])
    text3 = Paragraph(readings.c3_comments,
              styles['Normal'])
    text4 = Paragraph(readings.c4_comments,
              styles['Normal'])
    text5 = Paragraph(readings.c5_comments,
              styles['Normal'])
    comments = Paragraph('<b>Comments:</b>    ' + readings.comments,
              styles['Normal'])
    tableData = [
        [title],
        [subTitle],
        [inspectorDate],
        [batNumCrewForeman],
        [startEnd],
        ['', '', '', '', '', ''],
        ['', Paragraph('<para align=center><b>Oven Number</b></para>', styles['Normal']), 'Start Time', 'Stop Time', Paragraph('<para align=center><b>Visible Emissions (sec)</b></para>',styles['Normal']), 'Comments'],
        [1, readings.c1_no, time_change(readings.c1_start), time_change(readings.c1_stop), readings.c1_sec, text1],
        [2, readings.c2_no, time_change(readings.c2_start), time_change(readings.c2_stop), readings.c2_sec, text2],
        [3, readings.c3_no, time_change(readings.c3_start), time_change(readings.c3_stop), readings.c3_sec, text3],
        [4, readings.c4_no, time_change(readings.c4_start), time_change(readings.c4_stop), readings.c4_sec, text4],
        [5, readings.c5_no, time_change(readings.c5_start), time_change(readings.c5_stop), readings.c5_sec, text5],
        ['', '', '', 'Total Seconds:', readings.total_seconds],
        [Paragraph('<b>Larry Car:</b>&#160;&#160;#' + readings.larry_car, styles['Normal'])],
        [comments],
    ]
    
    
    pdf = SimpleDocTemplate(settings.MEDIA_ROOT + '/Print/' + fileName, pagesize=letter, topMargin=0.4*inch)
    #pdf = canvas.Canvas(fileName)
    
    # pdf.setTitle(documentTitle)
    
    # pdf.setFont('Times-Bold', 25)
    # pdf.drawCentredString(300, 774, title)
    # pdf.setFont('Times-Bold', 18)
    # pdf.drawCentredString(300, 750, subTitle)
    
    # pdf.setFont('Times-Roman', 13)
    # pdf.drawCentredString(300, 720, inspector + date)
    # pdf.setFont('Times-Roman', 13)
    # pdf.drawCentredString(300, 702, batNum + crew + forman)
    # pdf.setFont('Times-Roman', 13)
    # pdf.drawCentredString(300, 684, start + end)
    
    table = Table(tableData, colWidths=(25,70,100,100,90,150))
    
    
    style = TableStyle([
        ('FONT', (0,0), (-1,0), 'Times-Bold', 22),
        ('FONT', (0,1), (-1,1), 'Times-Bold', 15),
        
        ('VALIGN',(0,7),(-1,11),'MIDDLE'),
        ('VALIGN',(0,6),(-1,6),'MIDDLE'),
        ('FONT', (0,6), (-1,6), 'Helvetica-Bold'),
        ('BACKGROUND', (0,6), (-1,6),'(.6,.7,.8)'),
        #('BACKGROUND', (1,7), (1,7),'(.6,.7,.8)'),
        ('BOX', (0,6), (-1,11), 1, colors.black),
        ('BOX', (3,12), (4,12), 1, colors.black),
        ('ALIGN', (0,0), (-1,4), 'CENTER'),
        ('ALIGN', (0,6), (-1,6), 'CENTER'),
        ('ALIGN', (0,7), (4,11), 'CENTER'),
        ('ALIGN', (4,12), (4,12), 'CENTER'),
        ('ALIGN', (3,12), (3,12), 'RIGHT'),
        ('SPAN', (0,0), (-1,0)),
        ('SPAN', (0,1), (-1,1)),
        ('SPAN', (0,2), (-1,2)),
        #('SPAN', (2,2), (3,2)),
        #('SPAN', (4,2), (5,2)),
        ('SPAN', (0,3), (-1,3)),
        ('SPAN', (0,4), (-1,4)),
        ('SPAN', (0,14), (-1,14)),
        ('SPAN', (0,13), (-1,13)),
        ('GRID',(0,6), (-1,11), 0.5,colors.grey),
        ('BOTTOMPADDING',(0,1), (-1,1), 25),
    ])
    
    table.setStyle(style)
    
    for i in range(7,12):
        if i % 2 == 0:
            bc = '(.9,.9,.9)'
        else:
            bc = colors.white
        ts = TableStyle([
            ('BACKGROUND', (0,i), (-1,i), bc),
        ])
        table.setStyle(ts)
    
    elems = []
    elems.append(table)
    pdf.build(elems)

    return redirect('../../media/Print/' + fileName)

    # return render(request, "Print/print_index.html", {
    #     formDate: 'formDate'
    # })