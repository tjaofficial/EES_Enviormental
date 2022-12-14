from ..models import Forms
from django.conf import settings
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.core.exceptions import FieldError
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import json
import io

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')

def time_change(time):
    if str(time) not in {'None', '', 'No'}:
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
        
@lock
def form_PDF(request, formDate, formName):
    if len(formName) > 1:
        reFormName = formName[0] + '-' + formName[1]
        ModelForms = Forms.objects.filter(form=reFormName)[0]
    else:
        ModelForms = Forms.objects.filter(form=formName)[0]
    print(ModelForms)
    mainModel = apps.get_model('EES_Forms', 'form' + formName + '_model')
    try:
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
    except FieldError as e:
        org = mainModel.objects.all().order_by('-week_start')
        for r in org:
            if str(r.week_start) == str(formDate):
                database_model = r
        data = database_model

    styles = getSampleStyleSheet()
    fileName = 'form' + formName + '_' + formDate + ".pdf"
    documentTitle = 'form' + formName + '_' + formDate
    title = ModelForms.header + ' ' + ModelForms.title + ' - Form (' + ModelForms.form + ')'
    subTitle = 'Facility Name: EES Coke Battery LLC'
    #always the same on all A-forms
    marginSet = 0.4
    
    #create a stream
    stream = io.BytesIO()
    
    if formName == 'A1':
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
    elif formName in ('A2', 'A3'):
        inspectorDate = Paragraph('<para align=center><b>Inspectors Name:</b>&#160;&#160;' + data.observer + '&#160;&#160;&#160;&#160;&#160;<b>Date:</b>&#160;&#160;' + str(data.date) + '</para>', styles['Normal'])
        batOvenInop = Paragraph('<para align=center><b>Battery No.:</b> 5&#160;&#160;&#160;&#160;&#160;<b>Total No. Ovens:</b>&#160;&#160;85&#160;&#160;&#160;&#160;&#160;<b>Total No. Inoperable Ovens:</b>&#160;&#160;' + str(data.inop_ovens) + '&#160;(' + str(data.inop_numbs) + ')'  + '</para>', styles['Normal'])
        crewBat = Paragraph('<para align=center><b>Crew:</b>&#160;&#160;' + data.crew + '&#160;&#160;&#160;&#160;&#160;<b>Battery Forman:</b>&#160;&#160;' + data.foreman + '</para>', styles['Normal'])
        if formName == 'A2':
            if data.p_leak_data != '{}':
                p_leaks = json.loads(data.p_leak_data)['data']
            else:
                p_leaks = ''
            if data.c_leak_data != '{}':
                c_leaks = json.loads(data.c_leak_data)['data']
            else:
                c_leaks = ''
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
                spacedC = 1
            elif c_leaks != '' and p_leaks == '':
                for cleak in c_leaks:
                    tableData.insert(9,['', '', '', '', '', '', '', cleak['oven'], cleak['location'], cleak['zone'],'', '', '', ''],),
                spaced = len(c_leaks)
                spacedP = 1
                spacedC = len(c_leaks)
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
        if formName == 'A3':
            if data.om_leak_json != '{}':
                om_leaks = json.loads(data.om_leak_json)['data']
            else:
                om_leaks = ''
            if data.l_leak_json != '{}':
                l_leaks = json.loads(data.l_leak_json)['data']
            else:
                l_leaks = ''
            tableData = [
                [title],
                [subTitle],
                [inspectorDate],
                [batOvenInop],
                [crewBat],
                ['', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', Paragraph('<para align=center><b>Start Time:</b>&#160;&#160;' + time_change(data.om_start) + '</para>', styles['Normal']), '', '','', '', Paragraph('<para align=center><b>Start Time:</b>&#160;&#160;' + time_change(data.l_start) + '</para>', styles['Normal']), '', ''],
                ['', '', Paragraph('<para align=center><b>Stop Time:</b>&#160;&#160;' + time_change(data.om_stop) + '</para>', styles['Normal']), '', '','', '', Paragraph('<para align=center><b>Stop Time:</b>&#160;&#160;' + time_change(data.l_stop) + '</para>', styles['Normal']), '', ''],
                ['', '','Oven', 'Location', '', '', '', 'Oven', 'Location', ''],
            ]
            
            if om_leaks == '' and l_leaks == '':
                tableData.insert(9,['', '', 'N/A', '', '', '', '', 'N/A', '', '', '', ''],)
                spaced = 1
                spacedOm = 1
                spacedL = 1
            elif om_leaks != '' and l_leaks != '' :
                omLen = len(om_leaks)
                lLen = len(l_leaks)
                for x in range(omLen):
                    text = ''
                    for letters in om_leaks[x]['location']:
                        text += letters + ','
                    tableData.insert(9,['', '', om_leaks[x]['oven'], text, '', '', '', '', '', '', '', ''],)
                if omLen < lLen:
                    for rest in range(lLen - omLen):
                        tableData.insert((9 + omLen),['', '', '', '', '', '', '', '', '', '', '', ''],)
                    spaced = lLen
                    spacedOm = omLen
                    spacedL = lLen
                else:
                    spaced = omLen
                    spacedOm = omLen
                    spacedL = lLen
                for y in range(lLen):
                    textl = ''
                    for letterL in l_leaks[y]['location']:
                        textl += letterL + ','
                    tableData[9 + y][7] = l_leaks[y]['oven']
                    tableData[9 + y][8] = textl
            elif om_leaks != '' and l_leaks == '':
                for omleak in om_leaks:
                    text = ''
                    for letters in omleak['location']:
                        text += letters + ','
                    tableData.insert(9,['', '', omleak['oven'], text, '', '', '', '', '', '', '', ''],),
                spaced = len(om_leaks) 
                spacedOm = len(om_leaks)
                spacedL = 1
            elif l_leaks != '' and om_leaks == '':
                for lleak in l_leaks:
                    textl = ''
                    for letterL in lleak['location']:
                        textl += letterL + ','
                    tableData.insert(9,['', '', '', '', '', '', '', lleak['oven'], textl, '','', '', '', ''],),
                spaced = len(l_leaks)
                spacedOm = 1
                spacedL = len(l_leaks)
        
            tableInsert = [
                ['', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', Paragraph('<para align=center><b>Traverse Time:</b></para>', styles['Normal']), '', '','', '', Paragraph('<para align=center><b>Traverse Time:</b></para>', styles['Normal']), '', ''],
                ['', '', '', str(data.om_traverse_time_min) + 'min ' + str(data.om_traverse_time_sec) + 'sec', '', '', '', '', str(data.l_traverse_time_min) + 'min ' + str(data.l_traverse_time_sec) + 'sec', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', ''],
                ['', Paragraph('<para align=left>D = Dampered Off<br/>C = Cap</para>', styles['Normal']), '', Paragraph('<para align=center><b>Allowed Traverse Time: (Offtakes)</b></para>', styles['Normal']), '', '', '= 340 + (10 sec * # of leaks) =  ' + data.om_allowed_traverse_time, '', '', '', Paragraph('<para align=center><b>Valid Run?</b><br/>' + str(data.om_valid_run) + '</para>', styles['Normal']), ''],
                ['', 'F = Flange', '', '', '', '', '', '', '', '', '', ''],
                ['', Paragraph('<para align=left>S = Slip Joint<br/>B = Base</para>', styles['Normal']), '', Paragraph('<para align=center><b>Allowed Traverse Time:<br/>(lids)</b></para>', styles['Normal']), '', '', '= 340 + (10 sec * # of leaks) =  ' + data.l_allowed_traverse_time, '', '', '', Paragraph('<para align=center><b>Valid Run?</b><br/>' + str(data.l_valid_run) + '</para>', styles['Normal']), ''],
                ['', 'P = Piping', '', '', '', '', '', '', '', '', '', ''],
                ['', 'O = Other', '', '', '', '', '', '', '', '', '', ''],
                ['', 'MS = Mini Standpipe', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '                                    Pve X 100                ' + str(data.l_leaks) + ' X 100', '', '', '', '', '', '', '', ''],
                ['', 'Percent Leaking Lids = ---------------------- = ------------------------ = ' + str(data.l_percent_leaking), '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '          Povn(N - Ni) - Pno        4(85 - ' + str(data.inop_ovens) + ') - ' + str(data.l_not_observed), '', '', '', '', '', '', ''],
                ['', '', '', '                                    Pve X 100                  ' + str(data.l_leaks) + ' X 100', '', '', '', '', '', '', '', ''],
                ['', 'Percent Leaking Offtakes = ---------------------- = ------------------------ = ' + str(data.om_percent_leaking), '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '           Povn(N - Ni) - Pno          4(85 - ' + str(data.inop_ovens) + ') - ' + str(data.om_not_observed), '', '', '', '', '', '', ''],
                ['', 'Where: Ly = Leaking Doors Obsered, Di = Inoperable Oven x 2, and Dno = Door not observed', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', ''],
                ['', Paragraph('<para align=left><b>Notes:</b>&#160;&#160;' + data.notes + '</para>', styles['Normal'])]
            ]
            for lines in tableInsert:
                tableData.append(lines)
                
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
                
                #table header
                ('ALIGN', (0,7), (-1,8), 'CENTER'),
                ('SPAN', (2,6), (4,6)),
                ('SPAN', (2,7), (4,7)),
                ('SPAN', (7,6), (9,6)),
                ('SPAN', (7,7), (9,7)),
                ('SPAN', (3,8), (4,8)),
                ('SPAN', (8,8), (9,8)),
                ('BOX', (2,8), (4,8), 1, colors.black),
                ('BOX', (7,8), (9,8), 1, colors.black),
                ('BACKGROUND', (2,8), (4,8),'(.6,.7,.8)'),
                ('BACKGROUND', (7,8), (9,8),'(.6,.7,.8)'),
                
                #table data
                ('ALIGN', (0,9), (-1,8 + spaced), 'CENTER'),
                ('BOX', (2,9), (4,8 + spacedOm), 1, colors.black),
                ('BOX', (7,9), (9,8 + spacedL), 1, colors.black),
                
                #traverse time
                ('ALIGN', (2,10 + spaced), (-1,11 + spaced), 'CENTER'),
                ('SPAN', (2,10 + spaced), (4,10 + spaced)),
                #('BACKGROUND', (2,10 + spaced), (4,10 + spaced),'(.6,.7,.8)'),
                ('SPAN', (7,10 + spaced), (9,10 + spaced)),
                
                #bottom data
                ('SPAN', (1,13 + spaced), (2, 13 + spaced)),
                ('SPAN', (1,14 + spaced), (2, 14 + spaced)),
                ('SPAN', (1,15 + spaced), (2, 15 + spaced)),
                ('SPAN', (1,16 + spaced), (2, 16 + spaced)),
                ('SPAN', (1,17 + spaced), (2, 17 + spaced)),
                ('BOX', (1,13 + spaced), (2,18 + spaced), 1, colors.black),
                
                ('SPAN', (3,13 + spaced), (5, 13 + spaced)),
                ('SPAN', (3,15 + spaced), (5, 15 + spaced)),
                ('SPAN', (6,13 + spaced), (8, 13 + spaced)),
                ('SPAN', (6,15 + spaced), (8, 15 + spaced)),
                ('VALIGN', (6,13 + spaced), (8, 13 + spaced), 'MIDDLE'),
                ('VALIGN', (6,15 + spaced), (8, 15 + spaced), 'MIDDLE'),
                #('RIGHTPADDING',(6,13 + spaced), (6,13 + spaced), 75),
                ('SPAN', (10,15 + spaced), (11, 15 + spaced)),
                ('BOX', (10,15 + spaced), (11,15 + spaced), 1, colors.black),
                ('SPAN', (10,13 + spaced), (11, 13 + spaced)),
                ('BOX', (10,13 + spaced), (11,13 + spaced), 1, colors.black),
                ('ALIGN', (10,13 + spaced), (11, 15 + spaced), 'CENTER'),
                
                ('SPAN', (1,23 + spaced), (10, 23 + spaced)),
                ('ALIGN', (1,23 + spaced), (10, 23 + spaced), 'CENTER'),
                ('SPAN', (1,20 + spaced), (10, 20 + spaced)),
                ('ALIGN', (1,20 + spaced), (10, 20 + spaced), 'CENTER'),
                ('SPAN', (1,25 + spaced), (10, 25 + spaced)),
                ('ALIGN', (1,25 + spaced), (10, 25 + spaced), 'CENTER'),
                ('SPAN', (1,27 + spaced), (10, 27 + spaced)),
            ]
            if om_leaks == '':
                style.append(('SPAN', (2,9), (4,8 + spaced)),)
            if l_leaks == '':
                style.append(('SPAN', (7,9), (9,8 + spaced)),)
                
            if om_leaks != '' and l_leaks != '':
                del style[21]
                del style[22]
                style.append(('BOX', (2,9), (4,8 + spacedOm), 1, colors.black),)
                style.append(('BOX', (7,9), (9,8 + spacedL), 1, colors.black),)
                for spot in range(spaced):
                    style.append(('SPAN', (3,9 + spot), (4,9 + spot)))
                    style.append(('SPAN', (8,9 + spot), (9,9 + spot)))

            tableColWidths=(40,65,40,55,40,40,50,40,55,40,35,35)
    elif formName == 'A4':
        inspectorDate = Paragraph('<para align=center><b>Inspectors Name:</b>&#160;&#160;' + data.observer + '&#160;&#160;&#160;&#160;&#160;<b>Date:</b>&#160;&#160;' + str(data.date) + '</para>', styles['Normal'])
        batNumCrewForeman = Paragraph('<para align=center><b>Battery No.:</b> 5&#160;&#160;&#160;&#160;&#160;<b>Crew:</b>&#160;&#160;' + data.crew + '&#160;&#160;&#160;&#160;&#160;<b>Battery Forman:</b>&#160;&#160;' + data.foreman + '</para>', styles['Normal'])
        startEnd = Paragraph('<para align=center><b>Start Time:</b>&#160;&#160;' + time_change(data.main_start) + '&#160;&#160;&#160;&#160;&#160;<b>End Time:</b>&#160;&#160;' + time_change(data.main_stop) + '</para>', styles['Normal'])
        tableData = [
            [title],
            [subTitle],
            [inspectorDate],
            [batNumCrewForeman],
            [startEnd],
            ['', '', '', '', '', '', '', ''],
            ['', Paragraph('<para align=right><b>Colletions Main #1:</b></para>', styles['Normal']), '', '', data.main_1, '', '', ''],
            ['', Paragraph('<para align=right><b>Colletions Main #2:</b></para>', styles['Normal']), '', '', data.main_2, '', '', ''],
            ['', Paragraph('<para align=right><b>Colletions Main #3:</b></para>', styles['Normal']), '', '', data.main_3, '', '', ''],
            ['', Paragraph('<para align=right><b>Colletions Main #4:</b></para>', styles['Normal']), '', '', data.main_4, '', '', ''],
            ['', Paragraph('<para align=right><b>Suction Main Pressure:</b></para>', styles['Normal']), '', '', data.suction_main, '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', 'PUSH SIDE COLLECTION MAIN - Leak Observation Detail', '', '', '', '', '', ''],
        ]
        tableColWidths = (120,70,70,70,70,70,70,70)
        
        if data.oven_leak_1:
            tableData.append(['', 'Here is some information', '', '', '', '', '', ''],)
            spaced = 1
        else:
            tableData.append(['', 'N/A', '', '', '', '', '', ''],)
            spaced = 1
            
        tableInsert = [
            ['', '', '', '', '', '', '', ''],
            ['', Paragraph('<para align=left><b>Notes:</b>&#160;&#160;' + data.notes + '</para>', styles['Normal']), '', '', '', '', '', ''],
        ]
        for lines in tableInsert:
            tableData.append(lines)
            
        
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
            
            #pressures
            ('SPAN', (1,6), (3,6)), ('SPAN', (4,6), (5,6)),
            ('SPAN', (1,7), (3,7)), ('SPAN', (4,7), (5,7)),
            ('SPAN', (1,8), (3,8)), ('SPAN', (4,8), (5,8)),
            ('SPAN', (1,9), (3,9)), ('SPAN', (4,9), (5,9)),
            ('SPAN', (1,10), (3,10)), ('SPAN', (4,10), (5,10)),
            
            #leaks
            ('SPAN', (1,12), (5,12)),
            ('SPAN', (1,13), (5,13)),
            ('BOX', (1,12), (5,12), 1, colors.black),
            ('BOX', (1,13), (5,13), 1, colors.black),
            ('ALIGN', (1,12), (5,13), 'CENTER'),
            ('BACKGROUND', (1,12), (5,12),'(.6,.7,.8)'),
            
            #notes
            ('SPAN', (1,15), (5,15)),
        ]
    elif formName == 'A5':
        title = ModelForms.header + ' Visible Emission Observation Form'
        title2 = ModelForms.title + ' - Form (' + ModelForms.form + ')'
        tableData = [
            [title],
            [title2],
            [subTitle],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ]
        tableColWidths = (20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20)
        
        style = [
            #Top header and info
            ('FONT', (0,0), (-1,0), 'Times-Bold', 22),
            ('FONT', (0,1), (-1,1), 'Times-Bold', 15),
            ('FONT', (0,2), (-1,2), 'Times-Bold', 15),
            ('BOTTOMPADDING',(0,2), (-1,2), 25),
            ('SPAN', (0,0), (-1,0)),
            ('SPAN', (0,1), (-1,1)),
            ('SPAN', (0,2), (-1,2)),
            ('ALIGN', (0,0), (-1,2), 'CENTER'),
        ]
    elif formName == 'B':
        marginSet = 0.3
        title2 = ModelForms.title + ' - Form (' + ModelForms.form + ')'
        tableData = [
            [title],
            [title2],
            [subTitle],
            #grid start (0,4)
            [Paragraph('<para><b>Week of:</b>  ' + str(data.week_end) + '</para>', styles['Normal']), 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            ['Inspectors Initials', data.observer_0, data.observer_1, data.observer_2, data.observer_3, data.observer_4],
            ['Time', time_change(data.time_0), time_change(data.time_1), time_change(data.time_2), time_change(data.time_3), time_change(data.time_4)],
            ['Weather Conditions', data.weather_0, data.weather_1, data.weather_2, data.weather_3, data.weather_4],
            ['Wind Speeds', data.wind_speed_0, data.wind_speed_1, data.wind_speed_2, data.wind_speed_3, data.wind_speed_4],
            #grid start (0,9)
            [Paragraph('<para><b>Raw Material Storage and Transportation</b> - 5 days/week March-October, 1 day/week November-February</para>', styles['Normal']), '', '', '', '', ''],
            [Paragraph('Was fugitive dust observed in the raw material storage and transportation area?', styles['Normal']), data.fugitive_dust_observed_0, data.fugitive_dust_observed_1, data.fugitive_dust_observed_2, data.fugitive_dust_observed_3, data.fugitive_dust_observed_4],
            [Paragraph('Has chemical dust supressant been applied to temporary roadways?', styles['Normal']), data.supressant_applied_0, data.supressant_applied_1, data.supressant_applied_2, data.supressant_applied_3, data.supressant_applied_4],
            [Paragraph('Is surpressant being used in the active area of loading and unloading?', styles['Normal']), data.supressant_active_0, data.supressant_active_1, data.supressant_active_2, data.supressant_active_3, data.supressant_active_4],
            [Paragraph('Does the working face of a pile where equipment in removing material exceed 120 linear or horizontal feet across the mouth of the opening?', styles['Normal']), data.working_face_exceed_0, data.working_face_exceed_1, data.working_face_exceed_2, data.working_face_exceed_3, data.working_face_exceed_4],
            [Paragraph('Were any spills near piles or on roadways observed?', styles['Normal']), data.spills_0, data.spills_1, data.spills_2, data.spills_3, data.spills_4],
            [Paragraph('If YES was the material pushed back into pile or removed by vaccum sweeper?', styles['Normal']), data.pushed_back_0, data.pushed_back_1, data.pushed_back_2, data.pushed_back_3, data.pushed_back_4],
            #grid start (0,16)
            [Paragraph('<para><b>Loading and Unloading of Open Storage Piles</b> - 5 days/week March-October, 1 day/week November-February</para>', styles['Normal']), '', '', '', '', ''],
            [Paragraph('Was there a coal vessel unloding at the time of the inspection?', styles['Normal']), data.coal_vessel_0, data.coal_vessel_1, data.coal_vessel_2, data.coal_vessel_3, data.coal_vessel_4],
            [Paragraph('If YES, was the coal vessel equipped with water sprays over the entire width of the boom?', styles['Normal']), data.water_sprays_0, data.water_sprays_1, data.water_sprays_2, data.water_sprays_3, data.water_sprays_4],
            [Paragraph('Is the loader bucket lowered to within 12 inches of the pile before being tilted?', styles['Normal']), data.loader_lowered_0, data.loader_lowered_1, data.loader_lowered_2, data.loader_lowered_3, data.loader_lowered_4],
            [Paragraph('Are water sprays at the end of the stacker boom operating if necessary?', styles['Normal']), data.working_water_sprays_0, data.working_water_sprays_1, data.working_water_sprays_2, data.working_water_sprays_3, data.working_water_sprays_4],
            #grid start (0,21)
            [Paragraph('<para><b>Sprayed Storage Piles</b> - 1 days/week January-December</para>', styles['Normal']), '', '', '', '', ''],
            [Paragraph('Average barrier thickness on storage piles surfaces:', styles['Normal']), data.barrier_thickness_0, data.barrier_thickness_1, data.barrier_thickness_2, data.barrier_thickness_3, data.barrier_thickness_4],
            [Paragraph('Supressant surface quality:', styles['Normal']), data.loader_lowered_0, data.loader_lowered_1, data.loader_lowered_2, data.loader_lowered_3, data.loader_lowered_4],
            [Paragraph('Does supressant on piles have a crust to prevent visible emissions?', styles['Normal']), data.loader_lowered_0, data.loader_lowered_1, data.loader_lowered_2, data.loader_lowered_3, data.loader_lowered_4],
            [Paragraph('If no, when was the additional supressant compound applied?', styles['Normal']), data.loader_lowered_0, data.loader_lowered_1, data.loader_lowered_2, data.loader_lowered_3, data.loader_lowered_4],
            [Paragraph('Comments regarding any of the above inspections:', styles['Normal']), data.loader_lowered_0, data.loader_lowered_1, data.loader_lowered_2, data.loader_lowered_3, data.loader_lowered_4],
            #grid start (0,27)
            [Paragraph('<para><b>Outdoor Conveying Transfer Points</b> - 1 days/week January-December</para>', styles['Normal']), '', '', '', '', ''],
            [Paragraph('Wharf - General Housekeeping of Area (Good or Needs Housekeeping)? Any Spills?', styles['Normal']), data.loader_lowered_0, data.loader_lowered_1, data.loader_lowered_2, data.loader_lowered_3, data.loader_lowered_4],
            [Paragraph('Breeze - General Housekeeping of Area (Good or Needs Housekeeping)? Any Spills?', styles['Normal']), data.loader_lowered_0, data.loader_lowered_1, data.loader_lowered_2, data.loader_lowered_3, data.loader_lowered_4],
            
        ]
        tableColWidths = (270,53,53,53,53,53)
        
        style = [
            #Top header and info
            ('FONT', (0,0), (-1,0), 'Times-Bold', 18),
            ('FONT', (0,1), (-1,1), 'Times-Bold', 10),
            ('FONT', (0,2), (-1,2), 'Times-Bold', 10),
            #('BOTTOMPADDING',(0,2), (-1,2), 5),
            ('SPAN', (0,0), (-1,0)),
            ('SPAN', (0,1), (-1,1)),
            ('SPAN', (0,2), (-1,2)),
            ('ALIGN', (0,0), (-1,2), 'CENTER'),
            
            #table grid
            ('GRID',(0,4), (-1,28), 0.5,colors.black),
            ('BOX', (1,3), (-1,3), 1.5, colors.black),
            
            #Table
            ('ALIGN', (1,4), (-1,28), 'CENTER'),
            ('VALIGN', (1,4), (-1,28), 'MIDDLE'),
            ('BOX', (0,8), (-1,8), 1.5, colors.black),
            ('SPAN', (0,8), (-1,8)),
            ('BOX', (0,15), (-1,15), 1.5, colors.black),
            ('SPAN', (0,15), (-1,15)),
            ('BOX', (0,20), (-1,20), 1.5, colors.black),
            ('SPAN', (0,20), (-1,20)),
            ('BOX', (0,26), (-1,26), 1.5, colors.black),
            ('SPAN', (0,26), (-1,26)),
        ]
    elif formName == 'C':
        if data.sto_start_time and not data.salt_start_time or not data.sto_start_time and data.salt_start_time:
            count = 7
        elif data.sto_start_time and data.salt_start_time:
            count = 14
        else:
            count = 0
        date = Paragraph('<para align=center font=Times-Roman><b>Date:</b> ' + str(data.date) + '</para>', styles['Normal'])
        startStopTruck = Paragraph('<para align=center><b>Start:</b>&#160;' + time_change(data.truck_start_time) + '&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;<b>End:</b>&#160;' + time_change(data.truck_stop_time)+ '</para>', styles['Normal'])
        startStopArea = Paragraph('<para align=center><b>Start:</b>&#160;' + time_change(data.area_start_time) + '&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;<b>End:</b>&#160;' + time_change(data.area_stop_time)+ '</para>', styles['Normal'])
        if data.sto_start_time:
            startStopSto = Paragraph('<para align=center><b>Start:</b>&#160;' + time_change(data.sto_start_time) + '&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;<b>End:</b>&#160;' + time_change(data.sto_stop_time)+ '</para>', styles['Normal'])
        if data.salt_start_time:
            startStopSalt = Paragraph('<para align=center><b>Start:</b>&#160;' + time_change(data.salt_start_time) + '&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;<b>End:</b>&#160;' + time_change(data.salt_stop_time)+ '</para>', styles['Normal'])
        observerCert = Paragraph('<para align=center><b>Observer:</b>&#160;' + data.observer + '&#160;&#160;&#160;&#160;<b>Certified Date:</b>&#160;' + str(data.cert_date) + '</para>', styles['Normal'])
        comments = Paragraph('<para align=left><b>Comments:</b>    ' + data.comments + '</para>', styles['Normal'])
        
        tableData = [
            [title],
            [subTitle],
            [date],
            ['','','','','','','',''],
            ['',Paragraph('<para align=left><b>Truck:</b> ' + data.truck_sel + '</para>', styles['Normal']),'',startStopTruck,'','','',''],
            ['','MIN/SEC','0','15','30','45','',''],
            ['','0',readings.TRead1,readings.TRead2,readings.TRead3,readings.TRead4,'',''],
            ['','1',readings.TRead5,readings.TRead6,readings.TRead7,readings.TRead8,'',''],
            ['','2',readings.TRead9,readings.TRead10,readings.TRead11,readings.TRead12,'',''],
            ['','3-minute Average Opacity (sum of the 12 readings above/12)','','','','',data.average_t,''],
            ['','','','','','','',''],
            ['',Paragraph('<para align=left><b>Area:</b> ' + data.area_sel + '</para>', styles['Normal']),'',startStopArea,'','','',''],
            ['','MIN/SEC','0','15','30','45','',''],
            ['','0',readings.ARead1,readings.ARead2,readings.ARead3,readings.ARead4,'',''],
            ['','1',readings.ARead5,readings.ARead6,readings.ARead7,readings.ARead8,'',''],
            ['','2',readings.ARead9,readings.ARead10,readings.ARead11,readings.ARead12,'',''],
            ['','3-minute Average Opacity (sum of the 12 readings above/12)','','','','',data.average_p,''],
            ['','','','','','','',''],
        ]
        tableColWidths = (60,75,75,75,75,75,40,60)
        
        if data.sto_start_time:
            tableInsertSto = [
                ['',Paragraph('<para align=left><b>Area B Coke Storage Area:</b></para>', styles['Normal']),'',startStopSto,'','','',''],
                ['','MIN/SEC','0','15','30','45','',''],
                ['','0',readings.storage_1,readings.storage_2,readings.storage_3,readings.storage_4,'',''],
                ['','1',readings.storage_5,readings.storage_6,readings.storage_7,readings.storage_8,'',''],
                ['','2',readings.storage_9,readings.storage_10,readings.storage_11,readings.storage_12,'',''],
                ['','3-minute Average Opacity (sum of the 12 readings above/12)','','','','',data.average_storage,''],
                ['','','','','','','',''],
            ]
            for lineSto in tableInsertSto:
                tableData.append(lineSto)
        if data.salt_start_time:
            tableInsertSalt = [
                ['',Paragraph('<para align=left><b>Monthly Salt Pile Inspections:</b></para>', styles['Normal']),'',startStopSalt,'','','',''],
                ['','MIN/SEC','0','15','30','45','',''],
                ['','0',readings.salt_1,readings.salt_2,readings.salt_3,readings.salt_4,'',''],
                ['','1',readings.salt_5,readings.salt_6,readings.salt_7,readings.salt_8,'',''],
                ['','2',readings.salt_9,readings.salt_10,readings.salt_11,readings.salt_12,'',''],
                ['','3-minute Average Opacity (sum of the 12 readings above/12)','','','','',data.average_salt,''],
                ['','','','','','','',''],
            ]
            for lineSalt in tableInsertSalt:
                tableData.append(lineSalt)
        
        tableInsert =[
            ['',observerCert,'','','','','',''],
            ['','','','','','','',''],
            ['',comments,'','','','','',''],
        ]
        
        for finalLines in tableInsert:
            tableData.append(finalLines)
            
        style = [
            #Top header and info
            ('FONT', (0,0), (-1,0), 'Times-Bold', 18),
            ('FONT', (0,1), (-1,1), 'Times-Bold', 10),
            #('BOTTOMPADDING',(0,2), (-1,2), 5),
            ('SPAN', (0,0), (-1,0)),
            ('SPAN', (0,1), (-1,1)),
            ('SPAN', (0,2), (-1,2)),
            ('ALIGN', (0,0), (-1,2), 'CENTER'),
            
            #truck table (1,4)
            ('GRID',(1,5), (-3,9), 0.5,colors.black),
            ('BOX',(1,4), (-3,9), 0.5,colors.black),
            ('GRID',(6,9), (-2,9), 0.5,colors.black),
            ('SPAN', (1,4), (2,4)),
            ('SPAN', (1,9), (5,9)),
            ('ALIGN', (1,5), (5,8), 'CENTER'),
            ('ALIGN', (6,9), (6,9), 'CENTER'),
            ('SPAN', (3,4), (5,4)),
            ('ALIGN', (3,4), (5,4), 'RIGHT'),
            ('BACKGROUND', (1,5), (5,5),'(.6,.7,.8)'),
            
            #truck table (1,11)
            ('GRID',(1,12), (-3,16), 0.5,colors.black),
            ('BOX',(1,11), (-3,16), 0.5,colors.black),
            ('GRID',(6,16), (-2,16), 0.5,colors.black),
            ('SPAN', (1,11), (2,11)),
            ('SPAN', (1,16), (5,16)),
            ('ALIGN', (1,12), (5,15), 'CENTER'),
            ('ALIGN', (6,16), (6,16), 'CENTER'),
            ('SPAN', (3,11), (5,11)),
            ('ALIGN', (3,11), (5,11), 'RIGHT'),
            ('BACKGROUND', (1,12), (5,12),'(.6,.7,.8)'),
            
            #ending data (1,18)
            ('SPAN', (1,18 + count), (6,18 + count)),
            ('SPAN', (1,20 + count), (6,20 + count)),
        ]
        if data.sto_start_time and not data.salt_start_time or not data.sto_start_time and data.salt_start_time:
            styleInsertOne = [
                ('GRID',(1,19), (-3,23), 0.5,colors.black),
                ('BOX',(1,18), (-3,23), 0.5,colors.black),
                ('GRID',(6,23), (-2,23), 0.5,colors.black),
                ('SPAN', (1,18), (2,18)),
                ('SPAN', (1,23), (5,23)),
                ('ALIGN', (1,19), (5,22), 'CENTER'),
                ('ALIGN', (6,23), (6,23), 'CENTER'),
                ('SPAN', (3,18), (5,18)),
                ('ALIGN', (3,18), (5,18), 'RIGHT'),
                ('BACKGROUND', (1,19), (5,19),'(.6,.7,.8)'),
            ]
            for styleOne in styleInsertOne:
                style.append(styleOne)
        elif data.sto_start_time and data.salt_start_time:
            styleInsertTwo = [
                ('GRID',(1,19), (-3,23), 0.5,colors.black),
                ('BOX',(1,18), (-3,23), 0.5,colors.black),
                ('GRID',(6,23), (-2,23), 0.5,colors.black),
                ('SPAN', (1,18), (2,18)),
                ('SPAN', (1,23), (5,23)),
                ('ALIGN', (1,19), (5,22), 'CENTER'),
                ('ALIGN', (6,23), (6,23), 'CENTER'),
                ('SPAN', (3,18), (5,18)),
                ('ALIGN', (3,18), (5,18), 'RIGHT'),
                ('BACKGROUND', (1,19), (5,19),'(.6,.7,.8)'),
                
                ('GRID',(1,26), (-3,30), 0.5,colors.black),
                ('BOX',(1,25), (-3,30), 0.5,colors.black),
                ('GRID',(6,30), (-2,30), 0.5,colors.black),
                ('SPAN', (1,25), (2,25)),
                ('SPAN', (1,30), (5,30)),
                ('ALIGN', (1,26), (5,29), 'CENTER'),
                ('ALIGN', (6,30), (6,30), 'CENTER'),
                ('SPAN', (3,25), (5,25)),
                ('ALIGN', (3,25), (5,25), 'RIGHT'),
                ('BACKGROUND', (1,26), (5,26),'(.6,.7,.8)'),
            ]
            for styleTwo in styleInsertTwo:
                style.append(styleTwo)

            
    pdf = SimpleDocTemplate(stream, pagesize=letter, topMargin=marginSet*inch, bottomMargin=0.3*inch, title=documentTitle)
    #settings.MEDIA_ROOT + '/Print/' + fileName
    table = Table(tableData, colWidths=tableColWidths)
    
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
    
    # get buffer
    stream.seek(0)
    pdf_buffer = stream.getbuffer()
    # bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    # object_name = 'media/Print/'
    
    # s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #      aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY)

    # s3.Bucket(bucket_name).put_object(Key=object_name + fileName, Body=bytes(pdf_buffer))

    # stream2 = io.BytesIO()
    # s3.Object(bucket_name, object_name + fileName).download_fileobj(stream2)
    # stream2.seek(0)
    # pdf_buffer2 = stream2.getbuffer()
    
    #with open(settings.MEDIA_ROOT + '/penis/'+ fileName, 'ab') as file:
    #    file.write(bytes(pdf_buffer2))
    #    file.close()
    response = HttpResponse(bytes(pdf_buffer), content_type='application/pdf')
    return response