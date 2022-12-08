from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import issues_model, daily_battery_profile_model, formA1_model, formA1_readings_model, Forms
from ..forms import formA1_form, formA1_readings_form
from django.conf import settings
import os
import json
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from django.apps import apps


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
        

def formPDF(request, formDate, formName):
    if len(formName) > 1:
        reFormName = formName[0] + '-' + formName[1]
    ModelForms = Forms.objects.filter(form=reFormName)[0]
    print(ModelForms)
    mainModel = apps.get_model('EES_Forms', 'form' + formName + '_model')
    org = mainModel.objects.all().order_by('-date')
    for x in org:
        if str(x.date) == str(formDate):
            database_model = x
    data = database_model
    
    if formName in ('A1', 'A5', 'C', 'G1', 'G2', 'H', 'M'):
        readingsModel = apps.get_model('EES_Forms', 'form' + formName + '_readings_model')
        org2 = readingsModel.objects.all().order_by('-form')
        for x in org2:
            if str(x.form.date) == str(formDate):
                database_model2 = x
        readings = database_model2

    styles = getSampleStyleSheet()
    fileName = 'form' + formName + '_' + formDate + ".pdf"
    documentTitle = 'form' + formName + '_' + formDate
    title = ModelForms.header + ' ' + ModelForms.title + ' - Form (' + ModelForms.form + ')'
    subTitle = 'Facility Name: EES Coke Battery LLC'
    #always the same on all A-forms
    inspectorDate = Paragraph('<para align=center><b>Inspectors Name:</b>&#160;&#160;' + data.observer + '&#160;&#160;&#160;&#160;&#160;<b>Date:</b>&#160;&#160;' + str(data.date) + '</para>', styles['Normal'])
    
    if formName in ('A2', 'A3'):
        if data.p_leak_data != '{}':
            p_leaks = json.loads(data.p_leak_data)['data']
        else:
            p_leaks = ''
        if data.c_leak_data != '{}':
            c_leaks = json.loads(data.c_leak_data)['data']
        else:
            c_leaks = ''
        batOvenInop = Paragraph('<para align=center><b>Battery No.:</b> 5&#160;&#160;&#160;&#160;&#160;<b>Total No. Ovens:</b>&#160;&#160;85&#160;&#160;&#160;&#160;&#160;<b>Total No. Inoperable Ovens:</b>&#160;&#160;' + str(data.inop_ovens) + '&#160;(' + str(data.inop_numbs) + ')'  + '</para>', styles['Normal'])
        crewBat = Paragraph('<para align=center><b>Crew:</b>&#160;&#160;' + data.crew + '&#160;&#160;&#160;&#160;&#160;<b>Battery Forman:</b>&#160;&#160;' + data.foreman + '</para>', styles['Normal'])
        if formName == 'A2':
            tableData = [
                [title],
                [subTitle],
                [inspectorDate],
                [batOvenInop],
                [crewBat],
                ['', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', Paragraph('<para align=center><b>Start Time:</b>&#160;&#160;' + time_change(data.p_start) + '</para>', styles['Normal']), '', '','', '', Paragraph('<para align=center><b>Start Time:</b>&#160;&#160;' + time_change(data.c_start) + '</para>', styles['Normal']), '', ''],
                ['', '', Paragraph('<para align=center><b>Stop Time:</b>&#160;&#160;' + time_change(data.p_stop) + '</para>', styles['Normal']), '', '','', '', Paragraph('<para align=center><b>Stop Time:</b>&#160;&#160;' + time_change(data.c_stop) + '</para>', styles['Normal']), '', ''],
                ['', '','Oven', 'Location', 'Zone', '', '', 'Oven', 'Location', 'Zone'],
            ]
            if p_leaks == '' and c_leaks == '':
                tableData.insert(9,['', '', 'No Leaks', '', '', '', '', 'No Leaks', '', '', '', ''],)
                spaced = 1
                spacedP = 1
                spacedC = 1
            elif p_leaks != '' and c_leaks == '':
                for pleak in p_leaks:
                    tableData.insert(9,['', '', pleak['oven'], pleak['location'], pleak['zone'], '', '', '', '', '', '', ''],),
                spaced = len(p_leaks) 
                spacedP = len(p_leaks)
                spacedC = len(p_leaks)
            elif c_leaks != '' and p_leaks == '':
                for cleak in c_leaks:
                    tableData.insert(9,['', '', '', '', '', '', '', cleak['oven'], cleak['location'], cleak['zone'],'', '', '', ''],),
                spaced = len(p_leaks)
                spacedP = len(p_leaks)
                spacedC = len(p_leaks)
            elif p_leaks != '' and c_leaks != '' :
                pLen = len(p_leaks)
                cLen = len(c_leaks)
                for x in range(pLen):
                    tableData.insert(9,['', '', p_leaks[x]['oven'], p_leaks[x]['location'], p_leaks[x]['zone'], '', '', '', '', '', '', ''],)
                if pLen < cLen:
                    for rest in range(cLen - pLen):
                        tableData.insert((9 + pLen),['', '', '', '', '', '', '', '', '', '', '', ''],)
                    spaced = cLen
                    spacedP = pLen
                    spacedC = cLen
                else:
                    spaced = pLen
                    spacedP = pLen
                    spacedC = cLen
                for y in range(cLen):
                    tableData[9 + y][7] = c_leaks[y]['oven']
                    tableData[9 + y][8] = c_leaks[y]['location']
                    tableData[9 + y][9] = c_leaks[y]['zone']
                
            tableInsert = [
                ['', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', Paragraph('<para align=center><b>Temp Blocked:</b></para>', styles['Normal']), '', '','', '', Paragraph('<para align=center><b>Temp Blocked:</b></para>', styles['Normal']), '', ''],
                ['', '', '', str(data.p_temp_block_from) + ' to ' + str(data.p_temp_block_to), '', '', '', '', str(data.c_temp_block_from) + ' to ' + str(data.c_temp_block_to), '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', Paragraph('<para align=center><b>Push Side Travel Time:</b></para>', styles['Normal']), '', '','', '', Paragraph('<para align=center><b>Coke Side Travel Time:</b></para>', styles['Normal']), '', ''],
                ['', '', '', str(data.p_traverse_time_min) + 'min ' + str(data.p_traverse_time_sec) + 'sec', '', '', '', '', str(data.c_traverse_time_min) + 'min ' + str(data.c_traverse_time_sec) + 'sec', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', ''],
                ['', 'D = Door', '', '', Paragraph('<para align=center><b>Total Traverse Time:</b>&#160;&#160;' + data.total_traverse_time + '</para>', styles['Normal']), '', '', '', '', '', '', ''],
                ['', 'C = Chuck Door', '', '', Paragraph('<para align=center><b>Allowed Traverse Time:</b></para>', styles['Normal']), '', '', '', '', Paragraph('<para align=center><b>Valid Run?</b></para>', styles['Normal']), '', ''],
                ['', 'M = Masonry', '', '', 'T = 680 + (10sec x #leaks) =  ' + str(data.allowed_traverse_time), '', '', '', '', data.valid_run, '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '                               ly X 100                     ' + str(data.leaking_doors) + ' X 100', '', '', '', '', '', '', '', ''],
                ['', 'Percent Leaking Doors = ---------------------- = ------------------------ = ' + data.percent_leaking, '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '  Dt - Di - Dno              170 - ' + str(data.inop_doors_eq) + ' - ' + str(data.doors_not_observed), '', '', '', '', '', ''],
                ['', 'Where: Ly = Leaking Doors Obsered, Di = Inoperable Oven x 2, and Dno = Door not observed', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', ''],
                ['', Paragraph('<para align=left><b>Notes:</b>&#160;&#160;' + data.notes + '</para>', styles['Normal'])]
                
            ]
            for lines in tableInsert:
                tableData.append(lines)

            tableColWidths=(50,50,40,55,50,50,50,40,55,50,50,50)
            style = [
                #Top header and info
                ('FONT', (0,0), (-1,0), 'Times-Bold', 22),
                ('FONT', (0,1), (-1,1), 'Times-Bold', 15),
                ('BOTTOMPADDING',(0,1), (-1,1), 25),
                ('SPAN', (0,0), (-1,0)),
                ('SPAN', (0,1), (-1,1)),
                ('SPAN', (0,2), (-1,2)),
                ('SPAN', (0,3), (-1,3)),
                ('SPAN', (0,4), (-1,4)),
                ('ALIGN', (0,0), (-1,4), 'CENTER'),
                
                #leak header
                ('ALIGN', (0,7), (-1,8), 'CENTER'),
                ('SPAN', (2,6), (4,6)),
                ('SPAN', (2,7), (4,7)),
                ('SPAN', (7,6), (9,6)),
                ('SPAN', (7,7), (9,7)),
                ('BOX', (2,8), (4,8), 1, colors.black),
                ('BOX', (7,8), (9,8), 1, colors.black),
                ('BACKGROUND', (2,8), (4,8),'(.6,.7,.8)'),
                ('BACKGROUND', (7,8), (9,8),'(.6,.7,.8)'),
                
                #table data
                ('ALIGN', (0,9), (-1,8 + spaced), 'CENTER'),
                ('BOX', (2,9), (4,8 + spacedP), 1, colors.black),
                ('BOX', (7,9), (9,8 + spacedC), 1, colors.black),
                
                
                #temp blocked
                ('ALIGN', (2,10 + spaced), (-1,11 + spaced), 'CENTER'),
                ('SPAN', (2,10 + spaced), (4,10 + spaced)),
                ('SPAN', (7,10 + spaced), (9,10 + spaced)),
                
                #traverse time
                ('ALIGN', (2,13 + spaced), (-1,13 + spaced), 'CENTER'),
                ('SPAN', (2,13 + spaced), (4,13 + spaced)),
                ('SPAN', (7,13 + spaced), (9,13 + spaced)),
                
                #bottom data
                ('SPAN', (4,16 + spaced), (7,16 + spaced)),
                ('SPAN', (4,17 + spaced), (7,17 + spaced)),
                ('SPAN', (4,18 + spaced), (7,18 + spaced)),
                ('ALIGN', (4,17 + spaced), (7,18 + spaced), 'CENTER'),
                ('SPAN', (1,21 + spaced), (10,21 + spaced)),
                ('ALIGN', (1,21 + spaced), (-1,21 + spaced), 'CENTER'),
                ('SPAN', (3,20 + spaced), (8,20 + spaced)),
                ('ALIGN', (1,20 + spaced), (-1,20 + spaced), 'CENTER'),
                ('SPAN', (1,23 + spaced), (10,23 + spaced)),
                ('ALIGN', (1,23 + spaced), (-1,23 + spaced), 'CENTER'),
                ('SPAN', (1,25 + spaced), (10,25 + spaced)),
                ('BOTTOMPADDING',(0,22 + spaced), (-1,22 + spaced), 25),
                
                #left key
                ('SPAN', (1,16 + spaced), (2,16 + spaced)),
                ('SPAN', (1,17 + spaced), (2,17 + spaced)),
                ('SPAN', (1,18 + spaced), (2,18 + spaced)),
                ('BOX', (1,16 + spaced), (2,18 + spaced), 1, colors.black),
                
                #valid run
                ('SPAN', (9,17 + spaced), (10,17 + spaced)),
                ('SPAN', (9,18 + spaced), (10,18 + spaced)),
                ('ALIGN', (9,18 + spaced), (10,18 + spaced), 'CENTER'),
                ('BOX', (9,17 + spaced), (10,18 + spaced), 1, colors.black),
            ]
            if p_leaks == '':
                style.append(('SPAN', (2,9), (4,8 + spaced)),)
            if c_leaks == '':
                style.append(('SPAN', (7,9), (9,8 + spaced)),)

            if p_leaks != '' and c_leaks != '':
                del style[19]
                del style[20]
                style.append(('BOX', (2,9), (4,8 + spacedP), 1, colors.black),)
                style.append(('BOX', (7,9), (9,8 + spacedC), 1, colors.black),)
    elif formName in ('A1'):
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
        tableColWidths = (25,70,100,100,90,150)
        style = [
            ('FONT', (0,0), (-1,0), 'Times-Bold', 22),
            ('FONT', (0,1), (-1,1), 'Times-Bold', 15),
            ('VALIGN',(0,7),(-1,11),'MIDDLE'),
            ('VALIGN',(0,6),(-1,6),'MIDDLE'),
            ('FONT', (0,6), (-1,6), 'Helvetica-Bold'),
            ('BACKGROUND', (0,6), (-1,6),'(.6,.7,.8)'),
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
            ('SPAN', (0,3), (-1,3)),
            ('SPAN', (0,4), (-1,4)),
            ('SPAN', (0,14), (-1,14)),
            ('SPAN', (0,13), (-1,13)),
            ('GRID',(0,6), (-1,11), 0.5,colors.grey),
            ('BOTTOMPADDING',(0,1), (-1,1), 25),
        ]
    
    pdf = SimpleDocTemplate(settings.MEDIA_ROOT + '/Print/' + fileName, pagesize=letter, topMargin=0.4*inch, title=documentTitle)
    
    table = Table(tableData, colWidths=tableColWidths)
    
    
    #formStyles = {'A1':styleA1, 'A2':styleA2}
    
    style = TableStyle(style)
    
    table.setStyle(style)
    
    #for i in range(7,12):
    #    if i % 2 == 0:
    #        bc = '(.9,.9,.9)'
    #    else:
    #        bc = colors.white
    #    ts = TableStyle([
    #        ('BACKGROUND', (0,i), (-1,i), bc),
    #    ])
    #    table.setStyle(ts)
    
    elems = []
    elems.append(table)
    pdf.build(elems)

    return redirect(settings.MEDIA_URL +'/Print/' + fileName)