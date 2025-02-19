from reportlab.platypus import Paragraph # type: ignore
from reportlab.lib.styles import getSampleStyleSheet # type: ignore
from ..utils import time_change, date_change, date_time_change, truck_choices, area_choices, emptyInputs, road_choices, inventoryResponse, quarterParse, formBNone
from reportlab.lib import colors # type: ignore
import json
from ..models import form22_model, braintreePlans
import datetime
import calendar

styles = getSampleStyleSheet()

def pdf_template_invoice(primaryData, userProf, title):
    btPlan = braintreePlans.objects.get(planID=primaryData.plan_id)
    print(primaryData)
    tableData = [
        [title],
        ['Invoice Date','','','Invoice ID'],
        [primaryData.created_at.date(), '', '', primaryData.id],
        [''],
        ['To'],
        [userProf.company.company_name],
        [primaryData.credit_card_details.cardholder_name],
        [userProf.user.email],
        [''],
        ['Subscription'],
        [btPlan.name, '', '', '$' + str(btPlan.price) + '.00'],
        [primaryData.plan_id],
        [primaryData.created_at.date()],
        [''],
        ['Paid with '+ primaryData.payment_instrument_type.replace('_',' ').capitalize(), '', '', 'Total', '$' + str(btPlan.price) + '.00'],
        ['','','','Includes tax','$0.00'],
        ['','','','Total charge','$' + str(btPlan.price) + '.00'],
        ['Pleaser retain for your records.'],
        ['MethodPlus US Voxol Universe LLC'],
        ['Copyright (c) 2024 Voxol Universe LLC. All rights reserved.']
    ]
    tableColWidths = (100,100,100,100,100)
    style = [
        ('FONT', (0,0), (-1,0), 'Times-Bold', 22),
    ]
    
    return tableData, tableColWidths, style 

def pdf_template_A1(primaryData, secondaryData, title, subTitle):
    print(primaryData)
    inspectorDate = Paragraph('<para align=center><b>Inspectors Name:</b>&#160;&#160;' + primaryData.observer + '&#160;&#160;&#160;&#160;&#160;<b>Date:</b>&#160;&#160;' + date_change(primaryData.date) + '</para>', styles['Normal'])
    batNumCrewForeman = Paragraph('<para align=center><b>Battery No.:</b> 5&#160;&#160;&#160;&#160;&#160;<b>Crew:</b>&#160;&#160;' + primaryData.crew + '&#160;&#160;&#160;&#160;&#160;<b>Battery Forman:</b>&#160;&#160;' + primaryData.foreman + '</para>', styles['Normal'])
    startEnd = Paragraph('<para align=center><b>Start Time:</b>&#160;&#160;' + time_change(primaryData.start) + '&#160;&#160;&#160;&#160;&#160;<b>End Time:</b>&#160;&#160;' + time_change(primaryData.stop) + '</para>', styles['Normal'])
    text1 = Paragraph(secondaryData.c1_comments,
            styles['Normal'])
    text2 = Paragraph(secondaryData.c2_comments,
            styles['Normal'])
    text3 = Paragraph(secondaryData.c3_comments,
            styles['Normal'])
    text4 = Paragraph(secondaryData.c4_comments,
            styles['Normal'])
    text5 = Paragraph(secondaryData.c5_comments,
            styles['Normal'])
    comments = Paragraph('<b>Comments:</b>    ' + secondaryData.comments,
            styles['Normal'])
    print(primaryData.start)
    tableData = [
            [title],
            [subTitle],
            [inspectorDate],
            [batNumCrewForeman],
            [startEnd],
            ['', '', '', '', '', ''],
            ['', Paragraph('<para align=center><b>Oven Number</b></para>', styles['Normal']), 'Start Time', 'Stop Time', Paragraph('<para align=center><b>Visible Emissions (sec)</b></para>',styles['Normal']), 'Comments'],
            [1, secondaryData.c1_no, time_change(secondaryData.c1_start), time_change(secondaryData.c1_stop), secondaryData.c1_sec, text1],
            [2, secondaryData.c2_no, time_change(secondaryData.c2_start), time_change(secondaryData.c2_stop), secondaryData.c2_sec, text2],
            [3, secondaryData.c3_no, time_change(secondaryData.c3_start), time_change(secondaryData.c3_stop), secondaryData.c3_sec, text3],
            [4, secondaryData.c4_no, time_change(secondaryData.c4_start), time_change(secondaryData.c4_stop), secondaryData.c4_sec, text4],
            [5, secondaryData.c5_no, time_change(secondaryData.c5_start), time_change(secondaryData.c5_stop), secondaryData.c5_sec, text5],
            ['', '', '', 'Total Seconds:', secondaryData.total_seconds],
            [Paragraph('<b>Larry Car:</b>&#160;&#160;#' + secondaryData.larry_car, styles['Normal'])],
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
    return tableData, tableColWidths, style 

def pdf_template_A2(primaryData, title, subTitle):
    inspectorDate = Paragraph('<para align=center><b>Inspectors Name:</b>&#160;&#160;' + primaryData.observer + '&#160;&#160;&#160;&#160;&#160;<b>Date:</b>&#160;&#160;' + date_change(primaryData.date) + '</para>', styles['Normal'])
    batOvenInop = Paragraph('<para align=center><b>Battery No.:</b> 5&#160;&#160;&#160;&#160;&#160;<b>Total No. Ovens:</b>&#160;&#160;85&#160;&#160;&#160;&#160;&#160;<b>Total No. Inoperable Ovens:</b>&#160;&#160;' + str(primaryData.inop_ovens) + '&#160;(' + str(primaryData.inop_numbs) + ')'  + '</para>', styles['Normal'])
    crewBat = Paragraph('<para align=center><b>Crew:</b>&#160;&#160;' + primaryData.crew + '&#160;&#160;&#160;&#160;&#160;<b>Battery Forman:</b>&#160;&#160;' + primaryData.foreman + '</para>', styles['Normal'])

    if primaryData.p_leak_data != '{}':
        p_leaks = json.loads(primaryData.p_leak_data)['data']
        print(p_leaks)
    else:
        p_leaks = ''
    if primaryData.c_leak_data != '{}':
        c_leaks = json.loads(primaryData.c_leak_data)['data']
    else:
        c_leaks = ''
    tableData = [
        [title],
        [subTitle],
        [inspectorDate],
        [batOvenInop],
        [crewBat],
        ['', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', Paragraph('<para align=center><b>Start Time:</b>&#160;&#160;' + time_change(primaryData.p_start) + '</para>', styles['Normal']), '', '','', '', Paragraph('<para align=center><b>Start Time:</b>&#160;&#160;' + time_change(primaryData.c_start) + '</para>', styles['Normal']), '', ''],
        ['', '', Paragraph('<para align=center><b>Stop Time:</b>&#160;&#160;' + time_change(primaryData.p_stop) + '</para>', styles['Normal']), '', '','', '', Paragraph('<para align=center><b>Stop Time:</b>&#160;&#160;' + time_change(primaryData.c_stop) + '</para>', styles['Normal']), '', ''],
        ['', '','Oven', 'Location', 'Zone', '', '', 'Oven', 'Location', 'Zone'],
    ]
    if p_leaks == '' and c_leaks == '':
        tableData.insert(9,['', '', 'No Leaks', '', '', '', '', 'No Leaks', '', '', '', ''],)
        spaced = 1
        spacedP = 1
        spacedC = 1
    elif p_leaks != '' and c_leaks == '':
        count = 1
        for pleak in p_leaks:
            if count == len(p_leaks):
                tableData.insert(9,['', '', pleak['oven'], pleak['location'], pleak['zone'], '', '', 'No Leaks', '', '', '', ''],)
            else:
                tableData.insert(9,['', '', pleak['oven'], pleak['location'], pleak['zone'], '', '', '', '', '', '', ''],)
            count += 1
        spaced = len(p_leaks) 
        spacedP = len(p_leaks)
        spacedC = 1
    elif c_leaks != '' and p_leaks == '':
        count = 1
        for cleak in c_leaks:
            if count == len(c_leaks):
                tableData.insert(9,['', '', 'No Leaks', '', '', '', '', cleak['oven'], cleak['location'], cleak['zone'],'', ''],)
            else:
                tableData.insert(9,['', '', '', '', '', '', '', cleak['oven'], cleak['location'], cleak['zone'],'', ''],)
            count += 1
        spaced = len(c_leaks)
        spacedP = 1
        spacedC = len(c_leaks)
    elif p_leaks != '' and c_leaks != '' :
        pLen = len(p_leaks)
        cLen = len(c_leaks)
        for x in range(pLen):
            try:
                tableData.insert(9,['', '', p_leaks[x]['oven'], p_leaks[x]['location'], p_leaks[x]['zone'], '', '', '', '', '', '', ''],)
            except:
                tableData.insert(9,['', '', p_leaks[x]['oven'], p_leaks[x]['location'], "N/A", '', '', '', '', '', '', ''],)
                print("The leaks were submitted without a zone being selected. Please revisit form and add 'Zone' to the specific leak")
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
            try:
                tableData[9 + y][9] = c_leaks[y]['zone']
            except:
                tableData[9 + y][9] = 'N/A'
        
    tableInsert = [
        ['', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', Paragraph('<para align=center><b>Temp Blocked:</b></para>', styles['Normal']), '', '','', '', Paragraph('<para align=center><b>Temp Blocked:</b></para>', styles['Normal']), '', ''],
        ['', '', '', str(primaryData.p_temp_block_from) + ' to ' + str(primaryData.p_temp_block_to), '', '', '', '', str(primaryData.c_temp_block_from) + ' to ' + str(primaryData.c_temp_block_to), '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', Paragraph('<para align=center><b>Push Side Travel Time:</b></para>', styles['Normal']), '', '','', '', Paragraph('<para align=center><b>Coke Side Travel Time:</b></para>', styles['Normal']), '', ''],
        ['', '', '', str(primaryData.p_traverse_time_min) + 'min ' + str(primaryData.p_traverse_time_sec) + 'sec', '', '', '', '', str(primaryData.c_traverse_time_min) + 'min ' + str(primaryData.c_traverse_time_sec) + 'sec', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', ''],
        ['', 'D = Door', '', '', Paragraph('<para align=center><b>Total Traverse Time:</b>&#160;&#160;' + primaryData.total_traverse_time + '</para>', styles['Normal']), '', '', '', '', '', '', ''],
        ['', 'C = Chuck Door', '', '', Paragraph('<para align=center><b>Allowed Traverse Time:</b></para>', styles['Normal']), '', '', '', '', Paragraph('<para align=center><b>Valid Run?</b></para>', styles['Normal']), '', ''],
        ['', 'M = Masonry', '', '', 'T = 680 + (10sec x #leaks) =  ' + str(primaryData.allowed_traverse_time), '', '', '', '', primaryData.valid_run, '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '                               ly X 100                     ' + str(primaryData.leaking_doors) + ' X 100', '', '', '', '', '', '', '', ''],
        ['', 'Percent Leaking Doors = ---------------------- = ------------------------ = ' + primaryData.percent_leaking, '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '  Dt - Di - Dno              170 - ' + str(primaryData.inop_doors_eq) + ' - ' + str(primaryData.doors_not_observed), '', '', '', '', '', ''],
        ['', 'Where: Ly = Leaking Doors Observed, Di = Inoperable Oven x 2, and Dno = Door not observed', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', ''],
        ['', Paragraph('<para align=left><b>Notes:</b>&#160;&#160;' + primaryData.notes + '</para>', styles['Normal'])]
        
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
        style.append(('SPAN', (2,9), (4,8 + spacedP)),)
    if c_leaks == '':
        style.append(('SPAN', (7,9), (9,8 + spacedC)),)

    if p_leaks != '' and c_leaks != '':
        del style[19]
        del style[20]
        style.append(('BOX', (2,9), (4,8 + spacedP), 1, colors.black),)
        style.append(('BOX', (7,9), (9,8 + spacedC), 1, colors.black),)
    return tableData, tableColWidths, style

def pdf_template_A3(primaryData, title, subTitle):
    inspectorDate = Paragraph('<para align=center><b>Inspectors Name:</b>&#160;&#160;' + primaryData.observer + '&#160;&#160;&#160;&#160;&#160;<b>Date:</b>&#160;&#160;' + date_change(primaryData.date) + '</para>', styles['Normal'])
    batOvenInop = Paragraph('<para align=center><b>Battery No.:</b> 5&#160;&#160;&#160;&#160;&#160;<b>Total No. Ovens:</b>&#160;&#160;85&#160;&#160;&#160;&#160;&#160;<b>Total No. Inoperable Ovens:</b>&#160;&#160;' + str(primaryData.inop_ovens) + '&#160;(' + str(primaryData.inop_numbs) + ')'  + '</para>', styles['Normal'])
    crewBat = Paragraph('<para align=center><b>Crew:</b>&#160;&#160;' + primaryData.crew + '&#160;&#160;&#160;&#160;&#160;<b>Battery Forman:</b>&#160;&#160;' + primaryData.foreman + '</para>', styles['Normal'])
    
    if primaryData.om_leak_json != '{}':
        om_leaks = json.loads(primaryData.om_leak_json)['data']
    else:
        om_leaks = ''
    if primaryData.l_leak_json != '{}':
        l_leaks = json.loads(primaryData.l_leak_json)['data']
    else:
        l_leaks = ''
    tableData = [
        [title],
        [subTitle],
        [inspectorDate],
        [batOvenInop],
        [crewBat],
        ['', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', Paragraph('<para align=center><b>Start Time:</b>&#160;&#160;' + time_change(primaryData.om_start) + '</para>', styles['Normal']), '', '','', '', Paragraph('<para align=center><b>Start Time:</b>&#160;&#160;' + time_change(primaryData.l_start) + '</para>', styles['Normal']), '', ''],
        ['', '', Paragraph('<para align=center><b>Stop Time:</b>&#160;&#160;' + time_change(primaryData.om_stop) + '</para>', styles['Normal']), '', '','', '', Paragraph('<para align=center><b>Stop Time:</b>&#160;&#160;' + time_change(primaryData.l_stop) + '</para>', styles['Normal']), '', ''],
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
            om_leak_len = len(om_leaks[x]['location'])
            omCount = 0
            for letters in om_leaks[x]['location']:
                omCount += 1
                if letters == 'dampered_off':
                    omNewLetter = 'D'
                text += omNewLetter + ','
                if omCount == om_leak_len:
                    text = text[:-1]
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
            l_leak_len = len(om_leaks[x]['location'])
            lCount = 0
            for letterL in l_leaks[y]['location']:
                lCount += 1
                if letters == 'dampered_off':
                    lNewLetter = 'D'
                textl += lNewLetter + ','
                if lCount == l_leak_len:
                    textl = textl[:-1]
            tableData[9 + y][7] = l_leaks[y]['oven']
            tableData[9 + y][8] = textl
    elif om_leaks != '' and l_leaks == '':
        for omleak in om_leaks:
            text = ''
            for letters in omleak['location']:
                if letters == 'dampered_off':
                    letters = 'dampered'
                text += letters + ','
            if text != '':
                text = text[:-1]
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
        ['', '', str(primaryData.om_traverse_time_min) + 'min  ' + str(primaryData.om_traverse_time_sec) + 'sec = ' + str(primaryData.om_total_sec) + ' sec', '', '', '', '', str(primaryData.l_traverse_time_min) + 'min  ' + str(primaryData.l_traverse_time_sec) + 'sec = ' + str(primaryData.l_total_sec) + ' sec', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', ''],
        ['', Paragraph('<para align=left>D = Dampered Off<br/>C = Cap</para>', styles['Normal']), '', Paragraph('<para align=center><b>Allowed Traverse Time: (Offtakes)</b></para>', styles['Normal']), '', '', '= 340 + (10 sec * # of leaks) =  ' + primaryData.om_allowed_traverse_time, '', '', '', Paragraph('<para align=center><b>Valid Run?</b><br/>' + str(primaryData.om_valid_run) + '</para>', styles['Normal']), ''],
        ['', 'F = Flange', '', '', '', '', '', '', '', '', '', ''],
        ['', Paragraph('<para align=left>S = Slip Joint<br/>B = Base</para>', styles['Normal']), '', Paragraph('<para align=center><b>Allowed Traverse Time:<br/>(lids)</b></para>', styles['Normal']), '', '', '= 340 + (10 sec * # of leaks) =  ' + primaryData.l_allowed_traverse_time, '', '', '', Paragraph('<para align=center><b>Valid Run?</b><br/>' + str(primaryData.l_valid_run) + '</para>', styles['Normal']), ''],
        ['', 'P = Piping', '', '', '', '', '', '', '', '', '', ''],
        ['', 'O = Other', '', '', '', '', '', '', '', '', '', ''],
        ['', 'MS = Mini Standpipe', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '                                    Pve X 100                ' + str(primaryData.l_leaks) + ' X 100', '', '', '', '', '', '', '', ''],
        ['', 'Percent Leaking Lids = ---------------------- = ------------------------ = ' + str(primaryData.l_percent_leaking), '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '          Povn(N - Ni) - Pno        4(85 - ' + str(primaryData.inop_ovens) + ') - ' + str(primaryData.l_not_observed), '', '', '', '', '', '', ''],
        ['', '', '', '                                    Pve X 100                  ' + str(primaryData.l_leaks) + ' X 100', '', '', '', '', '', '', '', ''],
        ['', 'Percent Leaking Offtakes = ---------------------- = ------------------------ = ' + str(primaryData.om_percent_leaking), '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '           Povn(N - Ni) - Pno          2(85 - ' + str(primaryData.inop_ovens) + ') + 0 - ' + str(primaryData.om_not_observed), '', '', '', '', '', '', ''],
        ['', 'Where: Ly = Leaking Doors Observed, Di = Inoperable Oven x 2, and Dno = Door not observed', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', ''],
        ['', Paragraph('<para align=left><b>Notes:</b>&#160;&#160;' + primaryData.notes + '</para>', styles['Normal'])]
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
        ('SPAN', (2,11 + spaced), (4,11 + spaced)),
        ('ALIGN', (2,11 + spaced), (4,11 + spaced), 'CENTER'),
        #('BACKGROUND', (2,10 + spaced), (4,10 + spaced),'(.6,.7,.8)'),
        ('SPAN', (7,10 + spaced), (9,10 + spaced)),
        ('SPAN', (7,11 + spaced), (9,11 + spaced)),
        ('ALIGN', (7,11 + spaced), (9,11 + spaced), 'CENTER'),
        
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
    return tableData, tableColWidths, style

def pdf_template_A4(primaryData, title, subTitle):
    inspectorDate = Paragraph('<para align=center><b>Inspectors Name:</b>&#160;&#160;' + primaryData.observer + '&#160;&#160;&#160;&#160;&#160;<b>Date:</b>&#160;&#160;' + date_change(primaryData.date) + '</para>', styles['Normal'])
    batNumCrewForeman = Paragraph('<para align=center><b>Battery No.:</b> 5&#160;&#160;&#160;&#160;&#160;<b>Crew:</b>&#160;&#160;' + primaryData.crew + '&#160;&#160;&#160;&#160;&#160;<b>Battery Forman:</b>&#160;&#160;' + primaryData.foreman + '</para>', styles['Normal'])
    startEnd = Paragraph('<para align=center><b>Start Time:</b>&#160;&#160;' + time_change(primaryData.main_start) + '&#160;&#160;&#160;&#160;&#160;<b>End Time:</b>&#160;&#160;' + time_change(primaryData.main_stop) + '</para>', styles['Normal'])
    tableData = [
        [title],
        [subTitle],
        [inspectorDate],
        [batNumCrewForeman],
        [startEnd],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', Paragraph('<para align=right><b>Colletions Main #1:</b></para>', styles['Normal']), '', str(primaryData.main_1) + ' INWC', '', ''],
        ['', '', '', Paragraph('<para align=right><b>Colletions Main #2:</b></para>', styles['Normal']), '', str(primaryData.main_2) + ' INWC', '', ''],
        ['', '', '', Paragraph('<para align=right><b>Colletions Main #3:</b></para>', styles['Normal']), '', str(primaryData.main_3) + ' INWC', '', ''],
        ['', '', '', Paragraph('<para align=right><b>Colletions Main #4:</b></para>', styles['Normal']), '', str(primaryData.main_4) + ' INWC', '', ''],
        ['', '', '', Paragraph('<para align=right><b>Suction Main Pressure:</b></para>', styles['Normal']), '', str(primaryData.suction_main) + ' INWC', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', 'PUSH SIDE COLLECTION MAIN - Leak Observation Detail', '', '', '', '', '', '', ''],
    ]
    tableColWidths = (70,38,50,105,80,105,105,70,70)
    
    if primaryData.leak_data != "{}":
        mainsLeaks = json.loads(primaryData.leak_data)['data']
        tableData.append(['', Paragraph('<para align=center><b>Oven</b></para>', styles['Normal']), Paragraph('<para align=center><b>Time</b></para>', styles['Normal']), Paragraph('<para align=center><b>Temporarily Sealed</b></para>', styles['Normal']), Paragraph('<para align=center><b>By</b></para>', styles['Normal']), Paragraph('<para align=center><b>Final Repair Initiated</b></para>', styles['Normal']), Paragraph('<para align=center><b>Final Repair Completed</b></para>', styles['Normal']), Paragraph('<para align=center><b>By</b></para>', styles['Normal'])],)
        spaced = 0
        for leak in mainsLeaks:
            tableData.append(['', leak['oven'], time_change(leak['time']), date_time_change(leak['tempSealed']), leak['tempSealedBy'], date_time_change(leak['repairInit']), date_time_change(leak['repairComplete']), leak['repairBy'], ''],)
            spaced += 1
    else:
        tableData.append(['', 'N/A', '', '', '', '', '', ''],)
        spaced = 1
        
    tableInsert = [
        ['', '', '', '', '', '', '', ''],
        ['', Paragraph('<para align=left><b>Notes:</b>&#160;&#160;' + primaryData.notes + '</para>', styles['Normal']), '', '', '', '', '', ''],
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
        ('SPAN', (3,6), (4,6)), ('SPAN', (5,6), (5,6)),
        ('SPAN', (3,7), (4,7)), ('SPAN', (5,7), (5,7)),
        ('SPAN', (3,8), (4,8)), ('SPAN', (5,8), (5,8)),
        ('SPAN', (3,9), (4,9)), ('SPAN', (5,9), (5,9)),
        ('SPAN', (3,10), (4,10)), ('SPAN', (5,10), (5,10)),
        ('ALIGN', (5,6), (7,10), 'CENTER'),
        
        #leaks
        ('SPAN', (1,12), (7,12)),
        ('VALIGN', (1,13), (7,13), 'MIDDLE'),
        ('BOX', (1,12), (7,12), 1, colors.black),
        ('BOX', (1,13), (7,13), 1, colors.black),
        ('ALIGN', (1,12), (7,13), 'CENTER'),
        ('BACKGROUND', (1,12), (7,12),'(.6,.7,.8)'),
        
        #notes
        ('SPAN', (1,15), (5,15)),
    ]
    if primaryData.leak_data != "{}":
        styleInsert = [
            ('ALIGN', (1,13), (7,13 + spaced), 'CENTER'),
            ('GRID', (1,13), (7,13 + spaced), 1, colors.black),
        ] 
    else:
        styleInsert = [
            ('SPAN', (1,13), (7,13)),
        ]
    
    for lines in styleInsert:
        style.append(lines)         
    return tableData, tableColWidths, style

def pdf_template_A5(primaryData, title, subTitle, formInformation):
    marginSet = 0.3
    o1NumberTime = Paragraph('<para fontSize=8 align=center><b>Oven No:</b>&#160;' + primaryData.ovens_data['oven1']['oven_number'] + '&#160;&#160;&#160; <b>Start:</b>&#160;' + time_change(primaryData.ovens_data['oven1']['start']) + '&#160;&#160;&#160;<b>Stop:</b>' + time_change(primaryData.ovens_data['oven1']['stop']) + '</para>', styles['Normal'])
    o2NumberTime = Paragraph('<para fontSize=8 align=center><b>Oven No:</b>&#160;' + primaryData.ovens_data['oven2']['oven_number'] + '&#160;&#160;&#160; <b>Start:</b>&#160;' + time_change(primaryData.ovens_data['oven2']['start']) + '&#160;&#160;&#160;<b>Stop:</b>' + time_change(primaryData.ovens_data['oven2']['stop']) + '</para>', styles['Normal'])
    o3NumberTime = Paragraph('<para fontSize=8 align=center><b>Oven No:</b>&#160;' + primaryData.ovens_data['oven3']['oven_number'] + '&#160;&#160;&#160; <b>Start:</b>&#160;' + time_change(primaryData.ovens_data['oven3']['start']) + '&#160;&#160;&#160;<b>Stop:</b>' + time_change(primaryData.ovens_data['oven3']['stop']) + '</para>', styles['Normal'])
    o4NumberTime = Paragraph('<para fontSize=8 align=center><b>Oven No:</b>&#160;' + primaryData.ovens_data['oven4']['oven_number'] + '&#160;&#160;&#160; <b>Start:</b>&#160;' + time_change(primaryData.ovens_data['oven4']['start']) + '&#160;&#160;&#160;<b>Stop:</b>' + time_change(primaryData.ovens_data['oven4']['stop']) + '</para>', styles['Normal'])
    suffix = '' if primaryData.reading_data['wind_speed_stop'] == 'same' else ' mph'
    suffix2 = '' if primaryData.reading_data['ambient_temp_stop'] == 'same' else '<sup>o</sup>'

    tableData = [
        [title],
        [subTitle],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b><sup>ESTABLISHMENT</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.estab + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b><sup>COUNTY</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.county + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b><sup>ESTABLISHMENT NO.</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.estab_no + '</para>', styles['Normal']), '', ''],
        [Paragraph('<para fontSize=7><b><sup>EQUIPMENT LOCATION</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.equip_loc + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b><sup>DISTRICT</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.district + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b><sup>DATE</sup></b>&#160;&#160;</para><para fontSize=7>' + date_change(primaryData.date) + '</para>', styles['Normal']), '', ''],
        [Paragraph('<para fontSize=7><b><sup>CITY</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.city + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b><sup>OBSERVER</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.observer + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b><sup>CERTIFIED DATE</sup></b>&#160;&#160;</para><para fontSize=7>' + date_change(primaryData.cert_date) + '</para>', styles['Normal']), '', ''],
        [Paragraph('<para fontSize=7><b>PROCESS EQUIPMENT</b><br/></para><para fontSize=7>' + primaryData.reading_data['process_equip1'] + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b>OPERATING MODE</b><br/></para><para fontSize=7>' + primaryData.reading_data['op_mode1'] + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>BACKGROUND COLOR</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.reading_data['background_color_start'] + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.reading_data['background_color_stop'] + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>SKY CONDITION</b><br/></para><para fontSize=7>' + primaryData.reading_data['sky_conditions'] + '</para>', styles['Normal']), ''],
        [Paragraph('<para fontSize=7><b>PROCESS EQUIPMENT</b><br/></para><para fontSize=7>' + primaryData.reading_data['process_equip2'] + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b>OPERATING MODE</b><br/></para><para fontSize=7>' + primaryData.reading_data['op_mode2'] + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>WIND SPEED</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + str(primaryData.reading_data['wind_speed_start']) + ' mph&#160;&#160;&#160;<b>Stop:</b>&#160;' + str(primaryData.reading_data['wind_speed_stop']) + suffix + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>WIND DIRECTION</b><br/></para><para fontSize=7>' + primaryData.reading_data['wind_direction'] + '</para>', styles['Normal']), ''],
        [Paragraph('<para fontSize=7><b>DESCRIBE EMISSION POINT</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.reading_data['emission_point_start'] + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.reading_data['emission_point_stop'] + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b>AMBIENT TEMP</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + str(primaryData.reading_data['ambient_temp_start']) + '<sup>o</sup>&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + str(primaryData.reading_data['ambient_temp_stop']) + suffix2 + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>HUMIDITY</b><br/></para><para fontSize=7>' + str(primaryData.reading_data['humidity']) + '%</para>', styles['Normal']), ''],
        [Paragraph('<para fontSize=7><b>HEIGHT ABOVE GROUND LEVEL</b><br/></para><para fontSize=7>' + primaryData.reading_data['height_above_ground'] + '&#160;' + primaryData.reading_data['units'] + '</para>', styles['Normal']), '', '', '', '', '', Paragraph('<para fontSize=7><b>HEIGHT RELATIVE TO OBSERVER</b><br/></para><para fontSize=7>'+ primaryData.reading_data['height_rel_observer'] + '&#160;' + primaryData.reading_data['units'] + '</para>', styles['Normal']), '', '', '', Paragraph('<para align=center><img src=' + primaryData.canvas + ' height=175 width=248 valign=middle></img></para>'), '', '', '', ''],
        [Paragraph('<para fontSize=7><b>DISTANCE FROM OBSERVER</b><br/></para><para fontSize=7>' + primaryData.reading_data['distance_from'] + '&#160;' + primaryData.reading_data['units'] + '</para>', styles['Normal']), '', '', '', '', '', Paragraph('<para fontSize=7><b>DIRECTION FROM OBSERVER</b><br/></para><para fontSize=7>' + primaryData.reading_data['direction_from'] + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>DESCRIBE EMISSIONS</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.reading_data['describe_emissions_start'] + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.reading_data['describe_emissions_stop'] + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>EMISSIONS COLOR</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.reading_data['emission_color_start'] + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;</para><para fontSize=7>' + primaryData.reading_data['emission_color_stop'] + '</para>', styles['Normal']), '', '', '', '', '', '', Paragraph('<para fontSize=7><b>PLUME TYPE:</b><br/></para><para fontSize=7>' + primaryData.reading_data['plume_type'] + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>WATER DROPLET PRESENT:</b><br/></para><para fontSize=7>' + primaryData.reading_data['water_drolet_present'] + '</para>', styles['Normal']), '', '', '', '', '', '', Paragraph('<para fontSize=7><b>IF WATER DROPLET PLUME:</b><br/></para><para fontSize=7>' + primaryData.reading_data['water_droplet_plume'] + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>POINT IN PLUME WERE OPACITY WAS DETERMINED</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.reading_data['plume_opacity_determined_start'] + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.reading_data['plume_opacity_determined_stop'] + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>DESCRIBE BACKGROUND</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.reading_data['describe_background_start'] + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.reading_data['describe_background_stop'] + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        # bottom data starts at (0,17)
        ['', '', o1NumberTime, '', '', '', '', '', '', '', o2NumberTime, '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', Paragraph('<para fontSize=10 leading=9><b>P</b></para>',styles['Normal']), '', '0', '15', '30', '45', '', '', Paragraph('<para fontSize=10 leading=9><b>P</b></para>',styles['Normal']), '', '0', '15', '30', '45', ''],
        ['', '', '', '0', primaryData.ovens_data['oven1']['readings']['push']['1'], primaryData.ovens_data['oven1']['readings']['push']['2'], primaryData.ovens_data['oven1']['readings']['push']['3'], primaryData.ovens_data['oven1']['readings']['push']['4'], '', '', '', '0', primaryData.ovens_data['oven2']['readings']['push']['1'], primaryData.ovens_data['oven2']['readings']['push']['2'], primaryData.ovens_data['oven2']['readings']['push']['3'], primaryData.ovens_data['oven2']['readings']['push']['4'], ''],
        ['', '', '', '1', primaryData.ovens_data['oven1']['readings']['push']['5'], primaryData.ovens_data['oven1']['readings']['push']['6'], primaryData.ovens_data['oven1']['readings']['push']['7'], primaryData.ovens_data['oven1']['readings']['push']['8'], '', '', '', '1', primaryData.ovens_data['oven2']['readings']['push']['5'], primaryData.ovens_data['oven2']['readings']['push']['6'], primaryData.ovens_data['oven2']['readings']['push']['7'], primaryData.ovens_data['oven2']['readings']['push']['8'], ''],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', Paragraph('<para fontSize=10 leading=9><b>T</b></para>',styles['Normal']), '', '0', '15', '30', '45', '', '', Paragraph('<para fontSize=10 leading=9><b>T</b></para>',styles['Normal']), '', '0', '15', '30', '45', ''],
        ['', '', '', '0', primaryData.ovens_data['oven1']['readings']['travel']['1'], primaryData.ovens_data['oven1']['readings']['travel']['2'], primaryData.ovens_data['oven1']['readings']['travel']['3'], primaryData.ovens_data['oven1']['readings']['travel']['4'], '', '', '', '0', primaryData.ovens_data['oven2']['readings']['travel']['1'], primaryData.ovens_data['oven2']['readings']['travel']['2'], primaryData.ovens_data['oven2']['readings']['travel']['3'], primaryData.ovens_data['oven2']['readings']['travel']['4'], ''],
        ['', '', '', '1', primaryData.ovens_data['oven1']['readings']['travel']['5'], primaryData.ovens_data['oven1']['readings']['travel']['6'], primaryData.ovens_data['oven1']['readings']['travel']['7'], primaryData.ovens_data['oven1']['readings']['travel']['8'], '', '', '', '1', primaryData.ovens_data['oven2']['readings']['travel']['5'], primaryData.ovens_data['oven2']['readings']['travel']['6'], primaryData.ovens_data['oven2']['readings']['travel']['7'], primaryData.ovens_data['oven2']['readings']['travel']['8'], ''],
        ['', '', Paragraph('<para fontSize=9>Highest Instantaneous Opacity:&#160;' + str(primaryData.ovens_data['oven1']['highest_opacity']) + '%</para>', styles['Normal']), '', '', '', '', '', '', '', Paragraph('<para fontSize=9>Highest Instantaneous Opacity:&#160;' + str(primaryData.ovens_data['oven2']['highest_opacity']) + '%</para>', styles['Normal']), '', '', '', '', '', ''],
        ['', '', Paragraph('<para fontSize=9>Instantaneous Over 20%?&#160;' + str(primaryData.ovens_data['oven1']['opacity_over_20']) + '</para>', styles['Normal']), '', '', '', '', '', '', '', Paragraph('<para fontSize=9>Instantaneous Over 20%?&#160;' + str(primaryData.ovens_data['oven2']['opacity_over_20']) + '</para>', styles['Normal']), '', '', '', '', '', ''],
        ['', '', Paragraph('<para fontSize=9>Average Opacity of 6 Highest Readings:&#160;' + str(primaryData.ovens_data['oven1']['average_6_opacity']) + '%</para>', styles['Normal']), '', '', '', '', '', '', '', Paragraph('<para fontSize=9>Average Opacity of 6 Highest Readings:&#160;' + str(primaryData.ovens_data['oven2']['average_6_opacity']) + '%</para>', styles['Normal']), '', '', '', '', '', ''],
        ['', '', Paragraph('<para fontSize=9>Average Opacity of 6 Highest Readings Over 35%?&#160;' + str(primaryData.ovens_data['oven1']['average_6_over_35']) + '</para>', styles['Normal']), '', '', '', '', '', '', '', Paragraph('<para fontSize=9>Average Opacity of 6 Highest Readings Over 35%?&#160;' + str(primaryData.ovens_data['oven2']['average_6_over_35']) + '</para>', styles['Normal']), '', '', '', '', '', ''],
        # bottom data starts at (0,30)
        ['', '', o3NumberTime, '', '', '', '', '', '', '', o4NumberTime, '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', Paragraph('<para fontSize=10 leading=9><b>P</b></para>',styles['Normal']), '', '0', '15', '30', '45', '', '', Paragraph('<para fontSize=10 leading=9><b>P</b></para>',styles['Normal']), '', '0', '15', '30', '45', ''],
        ['', '', '', '0', primaryData.ovens_data['oven3']['readings']['push']['1'], primaryData.ovens_data['oven3']['readings']['push']['2'], primaryData.ovens_data['oven3']['readings']['push']['3'], primaryData.ovens_data['oven3']['readings']['push']['4'], '', '', '', '0', primaryData.ovens_data['oven4']['readings']['push']['1'], primaryData.ovens_data['oven4']['readings']['push']['2'], primaryData.ovens_data['oven4']['readings']['push']['3'], primaryData.ovens_data['oven4']['readings']['push']['4'], ''],
        ['', '', '', '1', primaryData.ovens_data['oven3']['readings']['push']['5'], primaryData.ovens_data['oven3']['readings']['push']['6'], primaryData.ovens_data['oven3']['readings']['push']['7'], primaryData.ovens_data['oven3']['readings']['push']['8'], '', '', '', '1', primaryData.ovens_data['oven4']['readings']['push']['5'], primaryData.ovens_data['oven4']['readings']['push']['6'], primaryData.ovens_data['oven4']['readings']['push']['7'], primaryData.ovens_data['oven4']['readings']['push']['8'], ''],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', Paragraph('<para fontSize=10 leading=9><b>T</b></para>',styles['Normal']), '', '0', '15', '30', '45', '', '', Paragraph('<para fontSize=10 leading=9><b>T</b></para>',styles['Normal']), '', '0', '15', '30', '45', ''],
        ['', '', '', '0', primaryData.ovens_data['oven3']['readings']['travel']['1'], primaryData.ovens_data['oven3']['readings']['travel']['2'], primaryData.ovens_data['oven3']['readings']['travel']['3'], primaryData.ovens_data['oven3']['readings']['travel']['4'], '', '', '', '0', primaryData.ovens_data['oven4']['readings']['travel']['1'], primaryData.ovens_data['oven4']['readings']['travel']['2'], primaryData.ovens_data['oven4']['readings']['travel']['3'], primaryData.ovens_data['oven4']['readings']['travel']['4'], ''],
        ['', '', '', '1', primaryData.ovens_data['oven3']['readings']['travel']['5'], primaryData.ovens_data['oven3']['readings']['travel']['6'], primaryData.ovens_data['oven3']['readings']['travel']['7'], primaryData.ovens_data['oven3']['readings']['travel']['8'], '', '', '', '1', primaryData.ovens_data['oven4']['readings']['travel']['5'], primaryData.ovens_data['oven4']['readings']['travel']['6'], primaryData.ovens_data['oven4']['readings']['travel']['7'], primaryData.ovens_data['oven4']['readings']['travel']['8'], ''],
        ['', '', Paragraph('<para fontSize=9>Highest Instantaneous Opacity:&#160;' + str(primaryData.ovens_data['oven1']['highest_opacity']) + '%</para>', styles['Normal']), '', '', '', '', '', '', '', Paragraph('<para fontSize=9>Highest Instantaneous Opacity:&#160;' + str(primaryData.ovens_data['oven1']['highest_opacity']) + '%</para>', styles['Normal']), '', '', '', '', '', ''],
        ['', '', Paragraph('<para fontSize=9>Instantaneous Over 20%?&#160;' + str(primaryData.ovens_data['oven1']['opacity_over_20']) + '</para>', styles['Normal']), '', '', '', '', '', '', '', Paragraph('<para fontSize=9>Instantaneous Over 20%?&#160;' + str(primaryData.ovens_data['oven1']['opacity_over_20']) + '</para>', styles['Normal']), '', '', '', '', '', ''],
        ['', '', Paragraph('<para fontSize=9>Average Opacity of 6 Highest Readings:&#160;' + str(primaryData.ovens_data['oven1']['average_6_opacity']) + '%</para>', styles['Normal']), '', '', '', '', '', '', '', Paragraph('<para fontSize=9>Average Opacity of 6 Highest Readings:&#160;' + str(primaryData.ovens_data['oven1']['average_6_opacity']) + '%</para>', styles['Normal']), '', '', '', '', '', ''],
        ['', '', Paragraph('<para fontSize=9>Average Opacity of 6 Highest Readings Over 35%?&#160;' + str(primaryData.ovens_data['oven1']['average_6_over_35']) + '</para>', styles['Normal']), '', '', '', '', '', '', '', Paragraph('<para fontSize=9>Average Opacity of 6 Highest Readings Over 35%?&#160;' + str(primaryData.ovens_data['oven1']['average_6_over_35']) + '</para>', styles['Normal']), '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', Paragraph('<para fontSize=8><b>Notes:&#160;</b>' + primaryData.notes + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ]
    tableColWidths = (45,10,20,20,40,40,40,40,30,40,20,20,42,42,42,42,40)
    tableRowHeights = (15, 15, 0, 16, 16, 16, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 7, 14, 0, 14, 14, 14, 5, 14, 14, 14, 14, 14, 14, 14, 21, 0, 14, 14, 14, 5, 14, 14, 14, 14, 14, 14, 14, 10, 35)
    
    style = [
        #Fonts
        ('FONT', (0,0), (-1,0), 'Times-Bold', 16),
        ('FONT', (0,1), (-1,1), 'Times-Bold', 10),
        
        #Top header and info
        #('BOTTOMPADDING',(0,1), (-1,1), 5),
        ('SPAN', (0,0), (-1,0)),
        ('SPAN', (0,1), (-1,1)),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('ALIGN', (0,1), (-1,1), 'CENTER'),
        
        #readings first 2 (0,17)
        ('VALIGN', (0,17), (-1,29), 'MIDDLE'),
        ('ALIGN', (0,17), (-1,25), 'CENTER'),
        ('GRID', (2,19), (7,21), 0.5, colors.black),
        ('GRID', (10,19), (15,21), 0.5, colors.black),
        ('BACKGROUND', (3,19), (7,19),'(.6,.7,.8)'),
        ('BACKGROUND', (11,19), (15,19),'(.6,.7,.8)'),
        ('SPAN', (2,17), (8,17)),
        ('SPAN', (10,17), (16,17)),
        ('SPAN', (2,19), (2,21)),
        ('SPAN', (10,19), (10,21)),
        ('SPAN', (2,26), (9,26)),
        ('SPAN', (10,26), (16,26)),
        ('SPAN', (2,27), (9,27)),
        ('SPAN', (10,27), (16,27)),
        ('SPAN', (2,28), (9,28)),
        ('SPAN', (10,28), (16,28)),
        ('SPAN', (2,29), (9,29)),
        ('SPAN', (10,29), (16,29)),
        
        
        ('GRID', (2,23), (7,25), 0.5, colors.black),
        ('GRID', (10,23), (15,25), 0.5, colors.black),
        ('BACKGROUND', (3,23), (7,23),'(.6,.7,.8)'),
        ('BACKGROUND', (11,23), (15,23),'(.6,.7,.8)'),
        ('SPAN', (2,23), (2,25)),
        ('SPAN', (10,23), (10,25)),
        
        #readings Second 2 (0,30)
        ('VALIGN', (0,3), (-1,5), 'MIDDLE'),
        ('VALIGN', (0,30), (-1,42), 'MIDDLE'),
        ('VALIGN', (0,30), (-1,30), 'BOTTOM'),
        ('ALIGN', (0,30), (-1,38), 'CENTER'),
        ('GRID', (2,32), (7,34), 0.5, colors.black),
        ('GRID', (10,32), (15,34), 0.5, colors.black),
        ('BACKGROUND', (3,32), (7,32),'(.6,.7,.8)'),
        ('BACKGROUND', (11,32), (15,32),'(.6,.7,.8)'),
        ('SPAN', (2,30), (8,30)),
        ('SPAN', (10,30), (16,30)),
        ('SPAN', (2,32), (2,34)),
        ('SPAN', (10,32), (10,34)),
        ('SPAN', (2,39), (9,39)),
        ('SPAN', (10,39), (16,39)),
        ('SPAN', (2,40), (9,40)),
        ('SPAN', (10,40), (16,40)),
        ('SPAN', (2,41), (9,41)),
        ('SPAN', (10,41), (16,41)),
        ('SPAN', (2,42), (9,42)),
        ('SPAN', (10,42), (16,42)),
        
        ('SPAN', (2,44), (-2,44)),
        ('GRID', (2,44), (-2,44), 0.5, colors.black),
        ('VALIGN', (2,44), (-2,44), 'TOP'),
        
        
        ('GRID', (2,36), (7,38), 0.5, colors.black),
        ('GRID', (10,36), (15,38), 0.5, colors.black),
        ('BACKGROUND', (3,36), (7,36),'(.6,.7,.8)'),
        ('BACKGROUND', (11,36), (15,36),'(.6,.7,.8)'),
        ('SPAN', (2,36), (2,38)),
        ('SPAN', (10,36), (10,38)),
        
        # top table information
        ('VALIGN', (0,6), (-1,15), 'MIDDLE'),
        ('GRID', (0,3), (-1,8), 0.5, colors.black),
        ('GRID', (0,3), (9,15), 0.5, colors.black),
        ('SPAN', (0,3), (10,3)),
        ('SPAN', (11,3), (13,3)),
        ('SPAN', (14,3), (-1,3)),
        
        ('SPAN', (0,4), (10,4)),
        ('SPAN', (11,4), (13,4)),
        ('SPAN', (14,4), (-1,4)),
        
        ('SPAN', (0,5), (2,5)),
        ('SPAN', (3,5), (13,5)),
        ('SPAN', (14,5), (-1,5)),
        
        ('SPAN', (0,6), (8,6)),
        ('SPAN', (9,6), (11,6)),
        ('SPAN', (12,6), (14,6)),
        ('SPAN', (15,6), (-1,6)),
        
        ('SPAN', (0,7), (8,7)),
        ('SPAN', (9,7), (11,7)),
        ('SPAN', (12,7), (14,7)),
        ('SPAN', (15,7), (-1,7)),
        
        ('SPAN', (0,8), (11,8)),
        ('SPAN', (12,8), (14,8)),
        ('SPAN', (15,8), (-1,8)),
        
        ('SPAN', (0,9), (5,9)),
        ('SPAN', (6,9), (9,9)),
        
        ('SPAN', (0,10), (5,10)),
        ('SPAN', (6,10), (9,10)),
        
        ('SPAN', (0,11), (9,11)),
        
        ('SPAN', (0,12), (6,12)),
        ('SPAN', (7,12), (9,12)),
        
        ('SPAN', (0,13), (6,13)),
        ('SPAN', (7,13), (9,13)),
        
        ('SPAN', (0,14), (9,14)),
        
        ('SPAN', (0,15), (9,15)),
        #canvas
        ('SPAN', (10,9), (16,15)),
        ('BOX', (10,9), (16,15), 0.5, colors.black),
        ('VALIGN', (10,9), (16,15), 'MIDDLE'),
    ]
    return tableData, tableColWidths, tableRowHeights, style

def pdf_template_6(primaryData, title, subTitle, formInformation):
    marginSet = 0.3
    title2 = formInformation.title + ' - Form (' + formInformation.form + ')'
    tableData = [
        [title],
        [title2],
        [subTitle],
        #grid start (0,4)
        [Paragraph('<para><b>Week of:</b>  ' + date_change(primaryData.week_end) + '</para>', styles['Normal']), 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        ['Inspectors Initials', primaryData.observer_0, primaryData.observer_1, primaryData.observer_2, primaryData.observer_3, primaryData.observer_4],
        ['Time', time_change(primaryData.time_0), time_change(primaryData.time_1), time_change(primaryData.time_2), time_change(primaryData.time_3), time_change(primaryData.time_4)],
        ['Weather Conditions', primaryData.weather_0, primaryData.weather_1, primaryData.weather_2, primaryData.weather_3, primaryData.weather_4],
        ['Wind Speeds', formBNone(primaryData.wind_speed_0), formBNone(primaryData.wind_speed_1), formBNone(primaryData.wind_speed_2), formBNone(primaryData.wind_speed_3), formBNone(primaryData.wind_speed_4)],
        #grid start (0,9)
        [Paragraph('<para><b>Raw Material Storage and Transportation</b> - 5 days/week March-October, 1 day/week November-February</para>', styles['Normal']), '', '', '', '', ''],
        [Paragraph('Was fugitive dust observed in the raw material storage and transportation area?', styles['Normal']), primaryData.fugitive_dust_observed_0, primaryData.fugitive_dust_observed_1, primaryData.fugitive_dust_observed_2, primaryData.fugitive_dust_observed_3, primaryData.fugitive_dust_observed_4],
        [Paragraph('Has chemical dust supressant been applied to temporary roadways?', styles['Normal']), primaryData.supressant_applied_0, primaryData.supressant_applied_1, primaryData.supressant_applied_2, primaryData.supressant_applied_3, primaryData.supressant_applied_4],
        [Paragraph('Is surpressant being used in the active area of loading and unloading?', styles['Normal']), primaryData.supressant_active_0, primaryData.supressant_active_1, primaryData.supressant_active_2, primaryData.supressant_active_3, primaryData.supressant_active_4],
        [Paragraph('Does the working face of a pile where equipment in removing material exceed 120 linear or horizontal feet across the mouth of the opening?', styles['Normal']), primaryData.working_face_exceed_0, primaryData.working_face_exceed_1, primaryData.working_face_exceed_2, primaryData.working_face_exceed_3, primaryData.working_face_exceed_4],
        [Paragraph('Were any spills near piles or on roadways observed?', styles['Normal']), primaryData.spills_0, primaryData.spills_1, primaryData.spills_2, primaryData.spills_3, primaryData.spills_4],
        [Paragraph('If YES was the material pushed back into pile or removed by vaccum sweeper?', styles['Normal']), primaryData.pushed_back_0, primaryData.pushed_back_1, primaryData.pushed_back_2, primaryData.pushed_back_3, primaryData.pushed_back_4],
        #grid start (0,16)
        [Paragraph('<para><b>Loading and Unloading of Open Storage Piles</b> - 5 days/week March-October, 1 day/week November-February</para>', styles['Normal']), '', '', '', '', ''],
        [Paragraph('Was there a coal vessel unloding at the time of the inspection?', styles['Normal']), primaryData.coal_vessel_0, primaryData.coal_vessel_1, primaryData.coal_vessel_2, primaryData.coal_vessel_3, primaryData.coal_vessel_4],
        [Paragraph('If YES, was the coal vessel equipped with water sprays over the entire width of the boom?', styles['Normal']), primaryData.water_sprays_0, primaryData.water_sprays_1, primaryData.water_sprays_2, primaryData.water_sprays_3, primaryData.water_sprays_4],
        [Paragraph('Is the loader bucket lowered to within 12 inches of the pile before being tilted?', styles['Normal']), primaryData.loader_lowered_0, primaryData.loader_lowered_1, primaryData.loader_lowered_2, primaryData.loader_lowered_3, primaryData.loader_lowered_4],
        [Paragraph('Are water sprays at the end of the stacker boom operating if necessary?', styles['Normal']), primaryData.working_water_sprays_0, primaryData.working_water_sprays_1, primaryData.working_water_sprays_2, primaryData.working_water_sprays_3, primaryData.working_water_sprays_4],
        #grid start (0,21)
        [Paragraph('<para><b>Sprayed Storage Piles</b> - 1 days/week January-December</para>', styles['Normal']), '', '', '', '', ''],
        [Paragraph('Average barrier thickness on storage piles surfaces:', styles['Normal']), primaryData.barrier_thickness_0, primaryData.barrier_thickness_1, primaryData.barrier_thickness_2, primaryData.barrier_thickness_3, primaryData.barrier_thickness_4],
        [Paragraph('Supressant surface quality:', styles['Normal']), primaryData.surface_quality_0, primaryData.surface_quality_1, primaryData.surface_quality_2, primaryData.surface_quality_3, primaryData.surface_quality_4],
        [Paragraph('Does supressant on piles have a crust to prevent visible emissions?', styles['Normal']), primaryData.surpressant_crust_0, primaryData.surpressant_crust_1, primaryData.surpressant_crust_2, primaryData.surpressant_crust_3, primaryData.surpressant_crust_4],
        [Paragraph('If no, when was the additional supressant compound applied?', styles['Normal']), primaryData.additional_surpressant_0, primaryData.additional_surpressant_1, primaryData.additional_surpressant_2, primaryData.additional_surpressant_3, primaryData.additional_surpressant_4],
        [Paragraph('Comments regarding any of the above inspections:', styles['Normal']), primaryData.comments_0, primaryData.comments_1, primaryData.comments_2, primaryData.comments_3, primaryData.comments_4],
        #grid start (0,27)
        [Paragraph('<para><b>Outdoor Conveying Transfer Points</b> - 1 days/week January-December</para>', styles['Normal']), '', '', '', '', ''],
        [Paragraph('Wharf - General Housekeeping of Area (Good or Needs Housekeeping)? Any Spills?', styles['Normal']), primaryData.wharf_0, primaryData.wharf_1, primaryData.wharf_2, primaryData.wharf_3, primaryData.wharf_4],
        [Paragraph('Breeze - General Housekeeping of Area (Good or Needs Housekeeping)? Any Spills?', styles['Normal']), primaryData.breeze_0, primaryData.breeze_1, primaryData.breeze_2, primaryData.breeze_3, primaryData.breeze_4],
        
    ]
    tableColWidths = (270,60,60,60,60,60)
    
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
        ('ALIGN', (1,3), (-1,3), 'CENTER'),
        
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
    return tableData, tableColWidths, style

def pdf_template_7(primaryData, secondaryData, title, subTitle):
    # formSettings = primaryData.settings['settings']
    date = Paragraph('<para align=center font=Times-Roman><b>Date:</b> ' + date_change(primaryData.date) + '</para>', styles['Normal'])
    tableData = [
        [title],
        [subTitle],
        [date],
        ['','','','','','','',''],
    ]
    style = [
        #Top header and info
        ('FONT', (0,0), (-1,0), 'Times-Bold', 18),
        ('FONT', (0,1), (-1,1), 'Times-Bold', 10),
        #('BOTTOMPADDING',(0,2), (-1,2), 5),
        ('SPAN', (0,0), (-1,0)),
        ('SPAN', (0,1), (-1,1)),
        ('SPAN', (0,2), (-1,2)),
        ('ALIGN', (0,0), (-1,2), 'CENTER')
    ]
    tableCount = -1
    areaData = [primaryData.area_json_1, primaryData.area_json_2, primaryData.area_json_3, primaryData.area_json_4]
    for areaDict in areaData:
        if areaDict:
            tableCount += 1
            startStop = Paragraph('<para align=center><b>Start:</b>&#160;' + time_change(areaDict['start_time']) + '&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;<b>End:</b>&#160;' + time_change(areaDict['stop_time'])+ '</para>', styles['Normal'])
            readings = areaDict['readings']
            areaBuild = [
                ['',Paragraph('<para align=left><b>Truck:</b> ' + areaDict['selection'] + '</para>', styles['Normal']),'',startStop,'','','',''],
                ['','MIN/SEC','0','15','30','45','',''],
                ['','0',readings['1'],readings['2'],readings['3'],readings['4'],'',''],
                ['','1',readings['5'],readings['6'],readings['7'],readings['8'],'',''],
                ['','2',readings['9'],readings['10'],readings['11'],readings['12'],'',''],
                ['','3-minute Average Opacity (sum of the 12 readings above/12)','','','','',areaDict['average'],''],
                ['','','','','','','',''],
            ]
            for lines in areaBuild:
                tableData.append(lines)
            count = tableCount * 7
            styleBuild = [
                ('GRID',(1,5 + count), (-3,9 + count), 0.5,colors.black),
                ('BOX',(1,4 + count), (-3,9 + count), 0.5,colors.black),
                ('GRID',(6,9 + count), (-2,9 + count), 0.5,colors.black),
                ('SPAN', (1,4 + count), (2,4 + count)),
                ('SPAN', (1,9 + count), (5,9 + count)),
                ('ALIGN', (1,5 + count), (5,8 + count), 'CENTER'),
                ('ALIGN', (6,9 + count), (6,9 + count), 'CENTER'),
                ('SPAN', (3,4 + count), (5,4 + count)),
                ('ALIGN', (3,4 + count), (5,4 + count), 'RIGHT'),
                ('BACKGROUND', (1,5 + count), (5,5 + count),'(.6,.7,.8)')
            ]
            for styleLine in styleBuild:
                style.append(styleLine)
    observerCert = Paragraph('<para align=center><b>Observer:</b>&#160;' + primaryData.observer + '&#160;&#160;&#160;&#160;<b>Certified Date:</b>&#160;' + date_change(primaryData.cert_date) + '</para>', styles['Normal'])
    comments = Paragraph('<para align=left><b>Comments:</b>    ' + primaryData.comments + '</para>', styles['Normal'])
    tableColWidths = (60,75,75,75,75,75,40,60)
    tableInsert =[
        ['',observerCert,'','','','','',''],
        ['','','','','','','',''],
        ['',comments,'','','','','',''],
    ]
    endingCount = count + 11
    endingStyleInsert = [
        #ending data (1,18)
        ('SPAN', (1,endingCount), (6,endingCount)),
        ('SPAN', (1,endingCount), (6,endingCount))
    ]
    for finalLines in tableInsert:
        tableData.append(finalLines)
    for finalStyleLines in endingStyleInsert:
        style.append(finalStyleLines)
    
    return tableData, tableColWidths, style

def pdf_template_8(primaryData, title, subTitle):
    tableData = [
        [title],
        [subTitle],
        ['', '', Paragraph('<para><b>Week of:&#160;</b>' + date_change(primaryData.week_start) + '&#160;&#160;to&#160;&#160;' + date_change(primaryData.week_end) + '</para>', styles['Normal']), '', '', ''],
        ['Truck 1', '', '', '', '', ''],
        [Paragraph('<para><b>Observer:&#160;</b>' + emptyInputs(primaryData.observer1) + '</para>', styles['Normal']), '', '', '', '', ''],
        [Paragraph('<para><b>Truck ID:&#160;</b>' + emptyInputs(primaryData.truck_id1) + '</para>', styles['Normal']), Paragraph('<para><b>Contents:&#160;</b>' + emptyInputs(primaryData.contents1) + '</para>', styles['Normal']), Paragraph('<para><b>Date:&#160;</b>' + emptyInputs(str(primaryData.date1)) + '</para>', styles['Normal']), Paragraph('<para><b>Time:&#160;</b>' + emptyInputs(time_change(primaryData.time1)) + '</para>', styles['Normal']), '', ''],
        [Paragraph('<para><b>Freeboard:&#160;</b>' + emptyInputs(primaryData.freeboard1) + '</para>', styles['Normal']), Paragraph('<para><b>If NO, is material adequately wetted and stable?&#160;</b>' + emptyInputs(primaryData.wetted1) + '</para>', styles['Normal']), '', '',  '', ''],
        [Paragraph('<para><b>Comments:&#160;</b>' + emptyInputs(primaryData.comments1) + '</para>', styles['Normal']), '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['Truck 2', '', '', '', '', ''],
        [Paragraph('<para><b>Observer:&#160;</b>' + emptyInputs(primaryData.observer2) + '</para>', styles['Normal']), '', '', '', '', ''],
        [Paragraph('<para><b>Truck ID:&#160;</b>' + emptyInputs(primaryData.truck_id2) + '</para>', styles['Normal']), Paragraph('<para><b>Contents:&#160;</b>' + emptyInputs(primaryData.contents2) + '</para>', styles['Normal']), Paragraph('<para><b>Date:&#160;</b>' + emptyInputs(str(primaryData.date2)) + '</para>', styles['Normal']), Paragraph('<para><b>Time:&#160;</b>' + emptyInputs(time_change(primaryData.time2)) + '</para>', styles['Normal']), '', ''],
        [Paragraph('<para><b>Freeboard:&#160;</b>' + emptyInputs(primaryData.freeboard2) + '</para>', styles['Normal']), Paragraph('<para><b>If NO, is material adequately wetted and stable?&#160;</b>' + emptyInputs(primaryData.wetted2) + '</para>', styles['Normal']), '', '', '', ''],
        [Paragraph('<para><b>Comments:&#160;</b>' + emptyInputs(primaryData.comments2) + '</para>', styles['Normal']), '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['Truck 3', '', '', '', '', ''],
        [Paragraph('<para><b>Observer:&#160;</b>' + emptyInputs(primaryData.observer3) + '</para>', styles['Normal']), '', '', '', '', ''],
        [Paragraph('<para><b>Truck ID:&#160;</b>' + emptyInputs(primaryData.truck_id3) + '</para>', styles['Normal']), Paragraph('<para><b>Contents:&#160;</b>' + emptyInputs(primaryData.contents3) + '</para>', styles['Normal']), Paragraph('<para><b>Date:&#160;</b>' + emptyInputs(str(primaryData.date3)) + '</para>', styles['Normal']), Paragraph('<para><b>Time:&#160;</b>' + emptyInputs(time_change(primaryData.time3)) + '</para>', styles['Normal']), '', ''],
        [Paragraph('<para><b>Freeboard:&#160;</b>' + emptyInputs(primaryData.freeboard3) + '</para>', styles['Normal']), Paragraph('<para><b>If NO, is material adequately wetted and stable?&#160;</b>' + emptyInputs(primaryData.wetted3) + '</para>', styles['Normal']), '', '', '', ''],
        [Paragraph('<para><b>Comments:&#160;</b>' + emptyInputs(primaryData.comments3) + '</para>', styles['Normal']), '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['Truck 4', '', '', '', '', ''],
        [Paragraph('<para><b>Observer:&#160;</b>' + emptyInputs(primaryData.observer4) + '</para>', styles['Normal']), '', '', '', '', ''],
        [Paragraph('<para><b>Truck ID:&#160;</b>' + emptyInputs(primaryData.truck_id4) + '</para>', styles['Normal']), Paragraph('<para><b>Contents:&#160;</b>' + emptyInputs(primaryData.contents4) + '</para>', styles['Normal']), Paragraph('<para><b>Date:&#160;</b>' + emptyInputs(str(primaryData.date4)) + '</para>', styles['Normal']), Paragraph('<para><b>Time:&#160;</b>' + emptyInputs(time_change(primaryData.time4)) + '</para>', styles['Normal']), '', ''],
        [Paragraph('<para><b>Freeboard:&#160;</b>' + emptyInputs(primaryData.freeboard4) + '</para>', styles['Normal']), Paragraph('<para><b>If NO, is material adequately wetted and stable?&#160;</b>' + emptyInputs(primaryData.wetted4) + '</para>', styles['Normal']), '', '', '', ''],
        [Paragraph('<para><b>Comments:&#160;</b>' + emptyInputs(primaryData.comments4) + '</para>', styles['Normal']), '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['Truck 5', '', '', '', '', ''],
        [Paragraph('<para><b>Observer:&#160;</b>' + emptyInputs(primaryData.observer5) + '</para>', styles['Normal']), '', '', '', '', ''],
        [Paragraph('<para><b>Truck ID:&#160;</b>' + emptyInputs(primaryData.truck_id5) + '</para>', styles['Normal']), Paragraph('<para><b>Contents:&#160;</b>' + emptyInputs(primaryData.contents5) + '</para>', styles['Normal']), Paragraph('<para><b>Date:&#160;</b>' + emptyInputs(str(primaryData.date5)) + '</para>', styles['Normal']), Paragraph('<para><b>Time:&#160;</b>' + emptyInputs(time_change(primaryData.time5)) + '</para>', styles['Normal']), '', ''],
        [Paragraph('<para><b>Freeboard:&#160;</b>' + emptyInputs(primaryData.freeboard5) + '</para>', styles['Normal']), Paragraph('<para><b>If NO, is material adequately wetted and stable?&#160;</b>' + emptyInputs(primaryData.wetted5) + '</para>', styles['Normal']), '', '', '', ''],
        [Paragraph('<para><b>Comments:&#160;</b>' + emptyInputs(primaryData.comments5) + '</para>', styles['Normal']), '', '', '', '', ''],
        ['', '', '', '', '', ''],
    ]
    tableColWidths = (90,90,100,90,80,80)

    style = [
        #Top header and info
        ('FONT', (0,0), (-1,0), 'Times-Bold', 22),
        ('FONT', (0,1), (-1,1), 'Times-Bold', 15),
        ('BOTTOMPADDING',(0,2), (-1,2), 25),
        ('SPAN', (0,0), (-1,0)),
        ('SPAN', (0,1), (-1,1)),
        ('SPAN', (2,2), (3,2)),
        ('ALIGN', (0,0), (-1,2), 'CENTER'),
        
        #truck 1
        ('BOX',(0,3), (-3,7), 0.5,colors.black),
        ('FONT', (0,3), (0,3), 'Times-Bold', 15),
        ('SPAN', (0,3), (-3,3)),
        ('ALIGN', (0,3), (-3,3), 'LEFT'),
        ('SPAN', (0,4), (1,4)),
        ('SPAN', (2,4), (3,4)),
        ('SPAN', (4,4), (5,4)),
        ('SPAN', (4,5), (5,5)),
        ('SPAN', (1,6), (3,6)),
        ('SPAN', (0,7), (3,7)),
        
        #truck 2
        ('BOX',(0,9), (-3,13), 0.5,colors.black),
        ('FONT', (0,9), (0,9), 'Times-Bold', 15),
        ('SPAN', (0,9), (-3,9)),
        ('ALIGN', (0,9), (-3,9), 'LEFT'),
        ('SPAN', (0,10), (1,10)),
        ('SPAN', (2,10), (3,10)),
        ('SPAN', (4,10), (5,10)),
        ('SPAN', (4,11), (5,11)),
        ('SPAN', (1,12), (3,12)),
        ('SPAN', (0,13), (3,13)),
        
        #truck 3
        ('BOX',(0,15), (-3,19), 0.5,colors.black),
        ('FONT', (0,15), (0,15), 'Times-Bold', 15),
        ('SPAN', (0,15), (-3,15)),
        ('ALIGN', (0,15), (-3,15), 'LEFT'),
        ('SPAN', (0,16), (1,16)),
        ('SPAN', (2,16), (3,16)),
        ('SPAN', (4,16), (5,16)),
        ('SPAN', (4,17), (5,17)),
        ('SPAN', (1,18), (3,18)),
        ('SPAN', (0,19), (3,19)),
        
        #truck 4
        ('BOX',(0,21), (-3,25), 0.5,colors.black),
        ('FONT', (0,21), (0,21), 'Times-Bold', 15),
        ('SPAN', (0,21), (-3,21)),
        ('ALIGN', (0,21), (-3,21), 'LEFT'),
        ('SPAN', (0,22), (1,22)),
        ('SPAN', (2,22), (3,22)),
        ('SPAN', (4,22), (5,22)),
        ('SPAN', (4,23), (5,23)),
        ('SPAN', (1,24), (3,24)),
        ('SPAN', (0,25), (3,25)),
        
        #truck 5
        ('BOX',(0,27), (-3,31), 0.5,colors.black),
        ('FONT', (0,27), (0,27), 'Times-Bold', 15),
        ('SPAN', (0,27), (-3,27)),
        ('ALIGN', (0,27), (-3,27), 'LEFT'),
        ('SPAN', (0,28), (1,28)),
        ('SPAN', (2,28), (3,28)),
        ('SPAN', (4,28), (5,28)),
        ('SPAN', (4,29), (5,29)),
        ('SPAN', (1,30), (3,30)),
        ('SPAN', (0,31), (3,31)),
    ]
    return tableData, tableColWidths, style

def pdf_template_9(primaryData, title, subTitle):
    count = 0
    inspectorDate = Paragraph('<para align=center><b>Inspectors Name:</b>&#160;&#160;' + primaryData.observer + '&#160;&#160;&#160;&#160;&#160;<b>Date:</b>&#160;&#160;' + date_change(primaryData.date) + '</para>', styles['Normal'])
    batNumCrewForeman = Paragraph('<para align=center><b>Battery No.:</b> 5&#160;&#160;&#160;&#160;&#160;<b>Crew:</b>&#160;&#160;' + primaryData.crew + '&#160;&#160;&#160;&#160;&#160;<b>Battery Forman:</b>&#160;&#160;' + primaryData.foreman + '</para>', styles['Normal'])
    startEnd = Paragraph('<para align=center><b>Start Time:</b>&#160;&#160;' + time_change(primaryData.start_time) + '&#160;&#160;&#160;&#160;&#160;<b>End Time:</b>&#160;&#160;' + time_change(primaryData.end_time) + '</para>', styles['Normal'])
    tableData = [
        [title],
        [subTitle],
        [inspectorDate],
        [batNumCrewForeman],
        [startEnd],
        [Paragraph('<para align=center><b>Leaks:</b>&#160;&#160;' + primaryData.leaks + '</para>', styles['Normal'])],
        ['', 'Gooseneck Inspection', '', '', '', ''],
        ['', 'Oven', 'Time', 'Source', 'Comments', ''],
        ['', '', 'I', 'Inspection Cap', '', ''],
        ['', '', 'G', 'GooseNeck', '', ''],
        ['', '', 'F', 'Flange', '', ''],
        ['', '', 'J', 'Expansion Joint', '', ''],
        ['', '', 'B', 'Bitman Joint', '', ''],
    ]
    tableColWidths = (80,60,80,80,120,80)

    if primaryData.goose_neck_data != '{}':
        allLeaks = json.loads(primaryData.goose_neck_data)['data']
        count = len(allLeaks)
        rowCount = 0
        for leak in allLeaks:
            tableData.insert(8 + rowCount, ['', leak['oven'], time_change(leak['time']), leak['source'], Paragraph('<para align=center>' + leak['comment'] + '</para>', styles['Normal']), ''],)
            rowCount += 1
    else:
        tableData.insert(8, ['', 'No Leaks Found During Observation', '', '', '',''],)
            
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
        ('ALIGN', (0,0), (-1,2), 'CENTER'),
        ('BOTTOMPADDING',(0,4), (-1,4), 20),
        ('SPAN', (0,5), (-1,5)),
        ('BOTTOMPADDING',(0,5), (-1,5), 15),
        
        #table
        ('SPAN', (1,6), (4,6)),
        ('GRID', (1,6), (4,7), 0.5, colors.black),
        
        ('ALIGN', (1,6), (4,7), 'CENTER'),
        ('FONT', (1,6), (4,7), 'Helvetica-Bold', 10),
        ('ALIGN', (2,8 + count), (2,12 + count), 'CENTER'),
        
    ]
    
    if primaryData.goose_neck_data != '{}':
        for x in range(count):
            style.append(('ALIGN', (1,8 + x), (4,8 + x), 'CENTER'),)
            style.append(('GRID', (1,8 + x), (4,8 + x), 0.5, colors.black),)
            style.append(('TOPPADDING',(0,8 + count), (-1,8 + count), 35),)
            style.append(('BOX', (1,6), (4,7 + count), 1.5, colors.black),)
            style.append(('ALIGN', (2,8 + count), (2,12 + count), 'CENTER'),)
    else:
        style.append(('ALIGN', (1,8), (4,8), 'CENTER'),)
        style.append(('SPAN', (1,8), (4,8)),)
        style.append(('BOX', (1,6), (4,8), 1.5, colors.black),)
        style.append(('TOPPADDING',(1,8), (4,8), 10),)
        style.append(('BOTTOMPADDING',(1,8), (4,8), 10),)
        style.append(('TOPPADDING',(1,9), (4,9), 35),)
        style.append(('ALIGN', (2,9), (2,12), 'CENTER'),)
    return tableData, tableColWidths, style

def pdf_template_17(primaryData, secondaryData, title, subTitle, formInformation):
    if secondaryData.PEC_emissions_present:
        emissions = 'Yes'
    else:
        emissions = 'No'
    if secondaryData.PEC_type == 'non':
        pecType = 'Non-Certifed'
        nonOvenTime = Paragraph('<para fontSize=10 align=center>#' + str(secondaryData.PEC_push_oven) + '&#160;-&#160;' + time_change(secondaryData.PEC_push_time) + '</para>', styles['Normal'])
    else:
        pecType = 'Method 9'
        methOvenTime1 = Paragraph('<para fontSize=10 align=center>#' + str(secondaryData.PEC_oven1) + '&#160;-&#160;' + time_change(secondaryData.PEC_time1) + '</para>', styles['Normal'])
        methOvenTime2 = Paragraph('<para fontSize=10 align=center>#' + str(secondaryData.PEC_oven2) + '&#160;-&#160;' + time_change(secondaryData.PEC_time2) + '</para>', styles['Normal']) if secondaryData.PEC_oven2 else ""
        methStartStop = Paragraph('<para fontSize=10 align=center><b>Start:</b>&#160;' + time_change(secondaryData.PEC_start) + '&#160;&#160;&#160;<b>Stop:&#160;</b>' + time_change(secondaryData.PEC_stop) + '</para>', styles['Normal'])
    marginSet = 0.3
    bothDataHeader = Paragraph('<para fontSize=10 align=center>Type of Visible Emissions Observation (select once and complete form below):&#160;' + pecType + '</para>', styles['Normal'])
    
    #title = Paragraph('<para align=center><b>' + formInformation.header + '<br/> Visible Emission Observation Form</b><br/><b>' + formInformation.title + ' - Form (' + formInformation.form + ')</b></para>', styles['Normal'])
    if primaryData.wind_speed_stop == 'same':
        suffix = ''
    else:
        suffix = 'mph'
    if primaryData.ambient_temp_stop == 'same':
        suffix2 = ''
    else:
        suffix2 = '<sup>o</sup>'
    tableData = [
        [title],
        [subTitle],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        # Top Data - (0, 3)
        [Paragraph('<para fontSize=7><b><sup>ESTABLISHMENT</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.estab + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b><sup>COUNTY</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.county + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b><sup>ESTABLISHMENT NO.</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.estab_no + '</para>', styles['Normal']), '', ''],
        [Paragraph('<para fontSize=7><b><sup>EQUIPMENT LOCATION</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.equip_loc + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b><sup>DISTRICT</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.district + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b><sup>DATE</sup></b>&#160;&#160;</para><para fontSize=7>' + date_change(primaryData.date) + '</para>', styles['Normal']), '', ''],
        [Paragraph('<para fontSize=7><b><sup>CITY</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.city + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b><sup>OBSERVER</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.observer + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b><sup>CERTIFIED DATE</sup></b>&#160;&#160;</para><para fontSize=7>' + date_change(primaryData.cert_date) + '</para>', styles['Normal']), '', ''],
        [Paragraph('<para fontSize=7><b>PROCESS EQUIPMENT</b><br/></para><para fontSize=7>' + primaryData.process_equip1 + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b>OPERATING MODE</b><br/></para><para fontSize=7>' + primaryData.op_mode1 + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>BACKGROUND COLOR</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.background_color_start + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.background_color_stop + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>SKY CONDITION</b><br/></para><para fontSize=7>' + primaryData.sky_conditions + '</para>', styles['Normal']), ''],
        [Paragraph('<para fontSize=7><b>PROCESS EQUIPMENT</b><br/></para><para fontSize=7>' + primaryData.process_equip2 + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b>OPERATING MODE</b><br/></para><para fontSize=7>' + primaryData.op_mode2 + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>WIND SPEED</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.wind_speed_start + 'mph&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.wind_speed_stop + suffix + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>WIND DIRECTION</b><br/></para><para fontSize=7>' + primaryData.wind_direction + '</para>', styles['Normal']), ''],
        [Paragraph('<para fontSize=7><b>DESCRIBE EMISSION POINT</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.emission_point_start + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.emission_point_stop + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b>AMBIENT TEMP</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.ambient_temp_start + '<sup>o</sup>&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.ambient_temp_stop + suffix2 + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>HUMIDITY</b><br/></para><para fontSize=7>' + primaryData.humidity + '%</para>', styles['Normal']), ''],
        [Paragraph('<para fontSize=7><b>HEIGHT ABOVE GROUND LEVEL</b><br/></para><para fontSize=7>' + primaryData.height_above_ground + '&#160;ft.</para>', styles['Normal']), '', '', '', '', '', Paragraph('<para fontSize=7><b>HEIGHT RELATIVE TO OBSERVER</b><br/></para><para fontSize=7>'+ primaryData.height_rel_observer + '&#160;ft.</para>', styles['Normal']), '', '', '',  Paragraph('<para align=center><img src=' + primaryData.canvas + ' height=175 width=248 valign=middle></img></para>'), '', '', '', ''],
        [Paragraph('<para fontSize=7><b>DISTANCE FROM OBSERVER</b><br/></para><para fontSize=7>' + primaryData.distance_from + '&#160;ft.</para>', styles['Normal']), '', '', '', '', '', Paragraph('<para fontSize=7><b>DIRECTION FROM OBSERVER</b><br/></para><para fontSize=7>' + primaryData.direction_from + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>DESCRIBE EMISSIONS</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.describe_emissions_start + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.describe_emissions_stop + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>EMISSIONS COLOR</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.emission_color_start + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;</para><para fontSize=7>' + primaryData.emission_color_stop + '</para>', styles['Normal']), '', '', '', '', '', '', Paragraph('<para fontSize=7><b>PLUME TYPE:</b><br/></para><para fontSize=7>' + primaryData.plume_type + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>WATER DROPLET PRESENT:</b><br/></para><para fontSize=7>' + primaryData.water_drolet_present + '</para>', styles['Normal']), '', '', '', '', '', '', Paragraph('<para fontSize=7><b>IF WATER DROPLET PLUME:</b><br/></para><para fontSize=7>' + primaryData.water_droplet_plume + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>POINT IN PLUME WERE OPACITY WAS DETERMINED</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.plume_opacity_determined_start + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.plume_opacity_determined_stop + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>DESCRIBE BACKGROUND</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.describe_background_start + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.describe_background_stop + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ]
    if secondaryData.PEC_type == 'non':
        dataInsert = [
            #Bottom Data, Non-Certified - (0,17)
            ['', bothDataHeader, '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', Paragraph('<para fontSize=10 align=center><b>Non-Certified Observation</b></para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', 'One (1) instantaneous observation during pushing.'],
            ['', '', '', '', '', Paragraph('<para fontSize=10><b>Pushing - Oven # and Time:</b></para>', styles['Normal']), '', '', 'o', nonOvenTime, '', '', '', '', '', '', ''],
            ['', '', '', '', '', Paragraph('<para fontSize=10><b>Time of observation:</b></para>', styles['Normal']), '', '', 'o', Paragraph('<para fontSize=10 align=center>' + time_change(secondaryData.PEC_observe_time) + '</para>', styles['Normal']), '', '', '', '', '', '', ''],
            ['', '', '', '', '', Paragraph('<para fontSize=10><b>Visible Emissions Present?</b></para>', styles['Normal']), '', '', 'o', Paragraph('<para fontSize=10 align=center>' + emissions + '</para>', styles['Normal']), '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', Paragraph('<para fontSize=10><b>If visible emissions are present during during the non-certified observation perform method 9B readings for three consecutive pushes and document the observation using form G-2.</b></para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ]
        tableColWidths = (45,10,20,20,40,40,40,40,30,40,20,20,42,42,42,42,40)
        tableRowHeights = (20, 20, 5, 20, 20, 20, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 30, 15, 15, 15, 20, 25, 15, 15, 20, 35, 15)
    else:
        dataInsert = [
            # Bottom Data, Method 9 - (0,17)
            ['', bothDataHeader, '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', Paragraph('<para fontSize=10 align=center><b>Method 9 Observation</b></para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', Paragraph('<para fontSize=10 align=center>Read for 6 minutes at 15 second intervals <br/>DURING PUSHING</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', Paragraph("<para fontSize=10 align=center><b>Pushing Oven #'s/ Times</b></para>", styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', methOvenTime1, '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', methOvenTime2, '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            # Table starts at (0,25)
            ['', methStartStop, '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', '0', '15', '30', '45', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '0', secondaryData.PEC_read_1, secondaryData.PEC_read_2, secondaryData.PEC_read_3, secondaryData.PEC_read_4, '', '', '', '', ''],
            ['', '', '', '', '', '', '', '1', secondaryData.PEC_read_5, secondaryData.PEC_read_6, secondaryData.PEC_read_7, secondaryData.PEC_read_8, '', '', '', '', ''],
            ['', '', '', '', '', '', '', '2', secondaryData.PEC_read_9, secondaryData.PEC_read_10, secondaryData.PEC_read_11, secondaryData.PEC_read_12, '', '', '', '', ''],
            ['', '', '', '', '', '', '', '3', secondaryData.PEC_read_13, secondaryData.PEC_read_14, secondaryData.PEC_read_15, secondaryData.PEC_read_16, '', '', '', '', ''],
            ['', '', '', '', '', '', '', '4', secondaryData.PEC_read_17, secondaryData.PEC_read_18, secondaryData.PEC_read_19, secondaryData.PEC_read_20, '', '', '', '', ''],
            ['', '', '', '', '', '', '', '5', secondaryData.PEC_read_21, secondaryData.PEC_read_22, secondaryData.PEC_read_23, secondaryData.PEC_read_24, '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', '', '', 'Average: ' + str(secondaryData.PEC_average), '', '', '', '', '', ''],
        ]
        tableColWidths = (45,10,20,20,20,40,35,38,38,38,38,34,34,34,34,34,40)
        tableRowHeights = (20, 20, 5, 20, 20, 20, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 30, 15, 5, 15, 30, 25, 15, 15, 5, 15, 20, 20, 20, 20, 20, 20, 20, 20)
    for line in dataInsert:
        tableData.append(line)

    style = [
        #Fonts
        ('FONT', (0,0), (-1,0), 'Times-Bold', 16),
        ('FONT', (0,1), (-1,1), 'Times-Bold', 10),
        
        #Top header and info
        #('BOTTOMPADDING',(0,1), (-1,1), 5),
        ('SPAN', (0,0), (-1,0)),
        ('SPAN', (0,1), (-1,1)),
        ('ALIGN', (0,0), (-1,1), 'CENTER'),
        
        # top table information
        ('VALIGN', (0,6), (-1,15), 'MIDDLE'),
        ('GRID', (0,3), (-1,8), 0.5, colors.black),
        ('GRID', (0,3), (11,15), 0.5, colors.black),
        ('SPAN', (0,3), (10,3)),
        ('SPAN', (11,3), (13,3)),
        ('SPAN', (14,3), (-1,3)),
        
        ('SPAN', (0,4), (10,4)),
        ('SPAN', (11,4), (13,4)),
        ('SPAN', (14,4), (-1,4)),
        
        ('SPAN', (0,5), (2,5)),
        ('SPAN', (3,5), (13,5)),
        ('SPAN', (14,5), (-1,5)),
        
        ('SPAN', (0,6), (8,6)),
        ('SPAN', (9,6), (11,6)),
        ('SPAN', (12,6), (14,6)),
        ('SPAN', (15,6), (-1,6)),
        
        ('SPAN', (0,7), (8,7)),
        ('SPAN', (9,7), (11,7)),
        ('SPAN', (12,7), (14,7)),
        ('SPAN', (15,7), (-1,7)),
        
        ('SPAN', (0,8), (11,8)),
        ('SPAN', (12,8), (14,8)),
        ('SPAN', (15,8), (-1,8)),
        
        ('SPAN', (0,9), (5,9)),
        ('SPAN', (6,9), (9,9)),
        
        ('SPAN', (0,10), (5,10)),
        ('SPAN', (6,10), (9,10)),
        
        ('SPAN', (0,11), (9,11)),
        
        ('SPAN', (0,12), (6,12)),
        ('SPAN', (7,12), (9,12)),
        
        ('SPAN', (0,13), (6,13)),
        ('SPAN', (7,13), (9,13)),
        
        ('SPAN', (0,14), (9,14)),
        
        ('SPAN', (0,15), (9,15)),
        
        ('SPAN', (10,9), (-1,15)),
        ('BOX', (10,9), (-1,15), 0.5, colors.black),
    ]
    if secondaryData.PEC_type == 'non':
        styleInsert = [
            #non data
            ('SPAN', (1,17), (-2,17)),
            ('ALIGN', (1,17), (-2,17), 'CENTER'),
            ('SPAN', (1,19), (-2,19)),
            ('SPAN', (1,20), (-2,20)),
            ('ALIGN', (1,20), (-2,20), 'CENTER'),
            ('SPAN', (5,21), (8,21)),
            ('SPAN', (9,21), (12,21)),
            ('SPAN', (5,22), (8,22)),
            ('SPAN', (9,22), (12,22)),
            ('SPAN', (5,23), (8,23)),
            ('SPAN', (9,23), (12,23)),
            ('SPAN', (5,25), (-4,25)),
            ('ALIGN', (5,25), (-4,25), 'CENTER'),
        ]
    else:
        styleInsert = [
            # meth 9 data
            ('SPAN', (1,17), (-2,17)),
            ('ALIGN', (1,17), (-2,17), 'CENTER'),
            ('SPAN', (1,19), (-2,19)),
            ('SPAN', (1,20), (-2,20)),
            ('ALIGN', (1,20), (-2,20), 'CENTER'),
            ('SPAN', (1,21), (-2,21)),
            ('ALIGN', (1,21), (-2,21), 'CENTER'),
            ('SPAN', (1,22), (-2,22)),
            ('ALIGN', (1,22), (-2,22), 'CENTER'),
            ('SPAN', (1,23), (-2,23)),
            ('ALIGN', (1,23), (-2,23), 'CENTER'),
            ('SPAN', (1,25), (-2,25)),
            ('GRID', (7,26), (-6,32), 0.5, colors.black),
            ('ALIGN', (0,26), (-1,32), 'CENTER'),
            ('VALIGN', (0,26), (-1,32), 'MIDDLE'),
            ('BACKGROUND', (7,26), (-6,26),'(.6,.7,.8)'),
        ]
    for line2 in styleInsert:
        style.append(line2)
    return tableData, tableColWidths, tableRowHeights, style

def pdf_template_18(primaryData, secondaryData, title, subTitle, formInformation):
    marginSet = 0.3
    o1NumberTime = Paragraph('<para fontSize=8 align=center><b>Oven No:</b>&#160;' + str(secondaryData.PEC_oven_a) + '&#160;&#160;&#160; <b>Start:</b>&#160;' + time_change(secondaryData.PEC_start_a) + '</para>', styles['Normal'])
    o2NumberTime = Paragraph('<para fontSize=8 align=center><b>Oven No:</b>&#160;' + str(secondaryData.PEC_oven_b) + '&#160;&#160;&#160; <b>Start:</b>&#160;' + time_change(secondaryData.PEC_start_b) + '</para>', styles['Normal'])
    o3NumberTime = Paragraph('<para fontSize=8 align=center><b>Oven No:</b>&#160;' + str(secondaryData.PEC_oven_c) + '&#160;&#160;&#160; <b>Start:</b>&#160;' + time_change(secondaryData.PEC_start_c) + '</para>', styles['Normal'])
    #title = Paragraph('<para align=center><b>' + formInformation.header + ' Visible Emission Observation Form</b><br/><b>' + formInformation.title + ' - Form (' + formInformation.form + ')</b></para>', styles['Normal'])
    if primaryData.wind_speed_stop == 'same':
        suffix = ''
    else:
        suffix = 'mph'
    if primaryData.ambient_temp_stop == 'same':
        suffix2 = ''
    else:
        suffix2 = '<sup>o</sup>'
    tableData = [
        [title],
        [subTitle],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        # Top Data - (0, 3)
        [Paragraph('<para fontSize=7><b><sup>ESTABLISHMENT</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.estab + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b><sup>COUNTY</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.county + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b><sup>ESTABLISHMENT NO.</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.estab_no + '</para>', styles['Normal']), '', ''],
        [Paragraph('<para fontSize=7><b><sup>EQUIPMENT LOCATION</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.equip_loc + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b><sup>DISTRICT</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.district + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b><sup>DATE</sup></b>&#160;&#160;</para><para fontSize=7>' + date_change(primaryData.date) + '</para>', styles['Normal']), '', ''],
        [Paragraph('<para fontSize=7><b><sup>CITY</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.city + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b><sup>OBSERVER</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.observer + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b><sup>CERTIFIED DATE</sup></b>&#160;&#160;</para><para fontSize=7>' + date_change(primaryData.cert_date) + '</para>', styles['Normal']), '', ''],
        [Paragraph('<para fontSize=7><b>PROCESS EQUIPMENT</b><br/></para><para fontSize=7>' + primaryData.process_equip1 + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b>OPERATING MODE</b><br/></para><para fontSize=7>' + primaryData.op_mode1 + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>BACKGROUND COLOR</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.background_color_start + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.background_color_stop + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>SKY CONDITION</b><br/></para><para fontSize=7>' + primaryData.sky_conditions + '</para>', styles['Normal']), ''],
        [Paragraph('<para fontSize=7><b>PROCESS EQUIPMENT</b><br/></para><para fontSize=7>' + primaryData.process_equip2 + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b>OPERATING MODE</b><br/></para><para fontSize=7>' + primaryData.op_mode2 + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>WIND SPEED</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.wind_speed_start + 'mph&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.wind_speed_stop + suffix + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>WIND DIRECTION</b><br/></para><para fontSize=7>' + primaryData.wind_direction + '</para>', styles['Normal']), ''],
        [Paragraph('<para fontSize=7><b>DESCRIBE EMISSION POINT</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.emission_point_start + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.emission_point_stop + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b>AMBIENT TEMP</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.ambient_temp_start + '<sup>o</sup>&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.ambient_temp_stop + suffix2 + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>HUMIDITY</b><br/></para><para fontSize=7>' + primaryData.humidity + '%</para>', styles['Normal']), ''],
        [Paragraph('<para fontSize=7><b>HEIGHT ABOVE GROUND LEVEL</b><br/></para><para fontSize=7>' + primaryData.height_above_ground + '&#160;ft.</para>', styles['Normal']), '', '', '', '', '', Paragraph('<para fontSize=7><b>HEIGHT RELATIVE TO OBSERVER</b><br/></para><para fontSize=7>'+ primaryData.height_rel_observer + '&#160;ft.</para>', styles['Normal']), '', '', '', Paragraph('<para align=center><img src=' + primaryData.canvas + ' height=175 width=248 valign=middle></img></para>'), '', '', '', ''],
        [Paragraph('<para fontSize=7><b>DISTANCE FROM OBSERVER</b><br/></para><para fontSize=7>' + primaryData.distance_from + '&#160;ft.</para>', styles['Normal']), '', '', '', '', '', Paragraph('<para fontSize=7><b>DIRECTION FROM OBSERVER</b><br/></para><para fontSize=7>' + primaryData.direction_from + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>DESCRIBE EMISSIONS</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.describe_emissions_start + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.describe_emissions_stop + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>EMISSIONS COLOR</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.emission_color_start + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;</para><para fontSize=7>' + primaryData.emission_color_stop + '</para>', styles['Normal']), '', '', '', '', '', '', Paragraph('<para fontSize=7><b>PLUME TYPE:</b><br/></para><para fontSize=7>' + primaryData.plume_type + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>WATER DROPLET PRESENT:</b><br/></para><para fontSize=7>' + primaryData.water_drolet_present + '</para>', styles['Normal']), '', '', '', '', '', '', Paragraph('<para fontSize=7><b>IF WATER DROPLET PLUME:</b><br/></para><para fontSize=7>' + primaryData.water_droplet_plume + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>POINT IN PLUME WERE OPACITY WAS DETERMINED</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.plume_opacity_determined_start + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.plume_opacity_determined_stop + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>DESCRIBE BACKGROUND</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.describe_background_start + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.describe_background_stop + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        # bottom tables (0,17)
        ['', '', o1NumberTime, '', '', '', '', '', '', '', o2NumberTime, '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '0', '15', '30', '45', '', '', '', '', '0', '15', '30', '45', ''],
        ['', '', '', '0', secondaryData.PEC_read_a_1, secondaryData.PEC_read_a_2, secondaryData.PEC_read_a_3, secondaryData.PEC_read_a_4, '', '', '', '0', secondaryData.PEC_read_b_1, secondaryData.PEC_read_b_2, secondaryData.PEC_read_b_3, secondaryData.PEC_read_b_4, ''],
        ['', '', '', '1', secondaryData.PEC_read_a_5, secondaryData.PEC_read_a_6, secondaryData.PEC_read_a_7, secondaryData.PEC_read_a_8, '', '', '', '1', secondaryData.PEC_read_b_5, secondaryData.PEC_read_b_6, secondaryData.PEC_read_b_7, secondaryData.PEC_read_b_8, ''],
        ['', '', Paragraph('<para fontSize=9><b>Highest 6-reading Average Opacity for Push:&#160;</b>' + str(secondaryData.PEC_average_a) + '%</para>', styles['Normal']), '', '', '', '', '', '', '', Paragraph('<para fontSize=9><b>Highest 6-reading Average Opacity for Push:&#160;</b>' + str(secondaryData.PEC_average_b) + '%</para>', styles['Normal']), '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', o3NumberTime, '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '0', '15', '30', '45', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '0', secondaryData.PEC_read_c_1, secondaryData.PEC_read_c_2, secondaryData.PEC_read_c_3, secondaryData.PEC_read_c_4, '', Paragraph('<para fontSize=9 align=center><b>Highest average opacity for Method 9B reading:&#160;</b>' + str(secondaryData.PEC_average_main) + '%</para>', styles['Normal']), '', '', '', '', '', ''],
        ['', '', '', '1', secondaryData.PEC_read_c_5, secondaryData.PEC_read_c_6, secondaryData.PEC_read_c_7, secondaryData.PEC_read_c_8, '', '', '', '', '', '', '', '', ''],
        ['', '', Paragraph('<para fontSize=9><b>Highest 6-reading Average Opacity for Push:&#160;</b>' + str(secondaryData.PEC_average_c) + '%</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ]
    
    tableColWidths = (45,10,20,20,40,40,40,40,30,40,20,20,42,42,42,42,40)
    tableRowHeights = (20, 20, 5, 20, 20, 20, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 30, 15, 2, 20, 20, 20, 30, 20, 15, 2, 20, 20, 20, 30)
    
    style = [
        #Fonts
        ('FONT', (0,0), (-1,0), 'Times-Bold', 16),
        ('FONT', (0,1), (-1,1), 'Times-Bold', 10),
        
        #Top header and info
        #('BOTTOMPADDING',(0,1), (-1,1), 5),
        ('SPAN', (0,0), (-1,0)),
        ('SPAN', (0,1), (-1,1)),
        ('ALIGN', (0,0), (-1,1), 'CENTER'),
        
        # top table information
        ('VALIGN', (0,6), (-1,15), 'MIDDLE'),
        ('GRID', (0,3), (-1,8), 0.5, colors.black),
        ('GRID', (0,3), (11,15), 0.5, colors.black),
        ('SPAN', (0,3), (10,3)),
        ('SPAN', (11,3), (13,3)),
        ('SPAN', (14,3), (-1,3)),
        
        ('SPAN', (0,4), (10,4)),
        ('SPAN', (11,4), (13,4)),
        ('SPAN', (14,4), (-1,4)),
        
        ('SPAN', (0,5), (2,5)),
        ('SPAN', (3,5), (13,5)),
        ('SPAN', (14,5), (-1,5)),
        
        ('SPAN', (0,6), (8,6)),
        ('SPAN', (9,6), (11,6)),
        ('SPAN', (12,6), (14,6)),
        ('SPAN', (15,6), (-1,6)),
        
        ('SPAN', (0,7), (8,7)),
        ('SPAN', (9,7), (11,7)),
        ('SPAN', (12,7), (14,7)),
        ('SPAN', (15,7), (-1,7)),
        
        ('SPAN', (0,8), (11,8)),
        ('SPAN', (12,8), (14,8)),
        ('SPAN', (15,8), (-1,8)),
        
        ('SPAN', (0,9), (5,9)),
        ('SPAN', (6,9), (9,9)),
        
        ('SPAN', (0,10), (5,10)),
        ('SPAN', (6,10), (9,10)),
        
        ('SPAN', (0,11), (9,11)),
        
        ('SPAN', (0,12), (6,12)),
        ('SPAN', (7,12), (9,12)),
        
        ('SPAN', (0,13), (6,13)),
        ('SPAN', (7,13), (9,13)),
        
        ('SPAN', (0,14), (9,14)),
        
        ('SPAN', (0,15), (9,15)),
        
        ('SPAN', (10,9), (-1,15)),
        ('BOX', (10,9), (-1,15), 0.5, colors.black),
        
        #bottom table
        ('SPAN', (2,17), (8,17)),
        ('SPAN', (10,17), (16,17)),
        ('SPAN', (2,19), (2,21)),
        ('SPAN', (10,19), (10,21)),
        ('VALIGN', (0,17), (-1,29), 'MIDDLE'),
        ('ALIGN', (0,17), (-1,25), 'CENTER'),
        ('GRID', (2,19), (7,21), 0.5, colors.black),
        ('GRID', (10,19), (15,21), 0.5, colors.black),
        ('BACKGROUND', (3,19), (7,19),'(.6,.7,.8)'),
        ('BACKGROUND', (11,19), (15,19),'(.6,.7,.8)'),
        ('SPAN', (2,22), (8,22)),
        ('SPAN', (10,22), (16,22)),
        
        ('SPAN', (2,24), (8,24)),
        ('SPAN', (2,26), (2,28)),
        ('VALIGN', (0,24), (-1,36), 'MIDDLE'),
        ('ALIGN', (0,24), (-1,32), 'CENTER'),
        ('GRID', (2,26), (7,28), 0.5, colors.black),
        ('BACKGROUND', (3,26), (7,26),'(.6,.7,.8)'),
        ('SPAN', (2,29), (8,29)),
        
        ('SPAN', (9,27), (16,27)),
        ('ALIGN', (9,27), (16,27), 'CENTER'),
    ]
    return tableData, tableColWidths, tableRowHeights, style

def pdf_template_19(primaryData, secondaryData, title, subTitle, formInformation):
    marginSet = 0.3
    startStop = Paragraph('<para fontSize=10 align=center><b>Start:</b>&#160;' + time_change(secondaryData.comb_start) + '&#160;&#160;&#160; <b>Stop:</b>&#160;' + time_change(secondaryData.comb_stop) + '</para>', styles['Normal'])
    bottomHeader = Paragraph('<para fontSize=10 align=center><b>Method 9 Observation</b></para>', styles['Normal'])
    #title = Paragraph('<para align=center><b>' + formInformation.header + ' Visible Emission Observation Form</b><br/><b>' + formInformation.title + ' - Form (' + formInformation.form + ')</b></para>', styles['Normal'])
    if secondaryData.comb_formL:
        interval = 'Read for 15 minutes MINIMUM at 15 second intervals'
    else:
        interval = 'Read for 6 minutes at 15 second intervals'
    
    if primaryData.wind_speed_stop == 'same':
        suffix = ''
    else:
        suffix = 'mph'
    if primaryData.ambient_temp_stop == 'same':
        suffix2 = ''
    else:
        suffix2 = '<sup>o</sup>'
    tableData = [
        [title],
        [subTitle],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        # Top Data - (0, 3)
        [Paragraph('<para fontSize=7><b><sup>ESTABLISHMENT</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.estab + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b><sup>COUNTY</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.county + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b><sup>ESTABLISHMENT NO.</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.estab_no + '</para>', styles['Normal']), '', ''],
        [Paragraph('<para fontSize=7><b><sup>EQUIPMENT LOCATION</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.equip_loc + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b><sup>DISTRICT</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.district + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b><sup>DATE</sup></b>&#160;&#160;</para><para fontSize=7>' + date_change(primaryData.date) + '</para>', styles['Normal']), '', ''],
        [Paragraph('<para fontSize=7><b><sup>CITY</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.city + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b><sup>OBSERVER</sup></b>&#160;&#160;</para><para fontSize=7>' + primaryData.observer + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b><sup>CERTIFIED DATE</sup></b>&#160;&#160;</para><para fontSize=7>' + date_change(primaryData.cert_date) + '</para>', styles['Normal']), '', ''],
        [Paragraph('<para fontSize=7><b>PROCESS EQUIPMENT</b><br/></para><para fontSize=7>' + primaryData.process_equip1 + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b>OPERATING MODE</b><br/></para><para fontSize=7>' + primaryData.op_mode1 + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>BACKGROUND COLOR</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.background_color_start + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.background_color_stop + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>SKY CONDITION</b><br/></para><para fontSize=7>' + primaryData.sky_conditions + '</para>', styles['Normal']), ''],
        [Paragraph('<para fontSize=7><b>PROCESS EQUIPMENT</b><br/></para><para fontSize=7>' + primaryData.process_equip2 + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b>OPERATING MODE</b><br/></para><para fontSize=7>' + primaryData.op_mode2 + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>WIND SPEED</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.wind_speed_start + 'mph&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.wind_speed_stop + suffix + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>WIND DIRECTION</b><br/></para><para fontSize=7>' + primaryData.wind_direction + '</para>', styles['Normal']), ''],
        [Paragraph('<para fontSize=7><b>DESCRIBE EMISSION POINT</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.emission_point_start + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.emission_point_stop + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', Paragraph('<para fontSize=7><b>AMBIENT TEMP</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.ambient_temp_start + '<sup>o</sup>&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.ambient_temp_stop + suffix2 + '</para>', styles['Normal']), '', '', Paragraph('<para fontSize=7><b>HUMIDITY</b><br/></para><para fontSize=7>' + primaryData.humidity + '%</para>', styles['Normal']), ''],
        [Paragraph('<para fontSize=7><b>HEIGHT ABOVE GROUND LEVEL</b><br/></para><para fontSize=7>' + primaryData.height_above_ground + '&#160;ft.</para>', styles['Normal']), '', '', '', '', '', Paragraph('<para fontSize=7><b>HEIGHT RELATIVE TO OBSERVER</b><br/></para><para fontSize=7>'+ primaryData.height_rel_observer + '&#160;ft.</para>', styles['Normal']), '', '', '', '', Paragraph('<para align=center><img src=' + primaryData.canvas + ' height=175 width=228 valign=middle></img></para>'), '', '', '', ''],
        [Paragraph('<para fontSize=7><b>DISTANCE FROM OBSERVER</b><br/></para><para fontSize=7>' + primaryData.distance_from + '&#160;ft.</para>', styles['Normal']), '', '', '', '', '', Paragraph('<para fontSize=7><b>DIRECTION FROM OBSERVER</b><br/></para><para fontSize=7>' + primaryData.direction_from + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>DESCRIBE EMISSIONS</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.describe_emissions_start + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.describe_emissions_stop + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>EMISSIONS COLOR</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.emission_color_start + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;</para><para fontSize=7>' + primaryData.emission_color_stop + '</para>', styles['Normal']), '', '', '', '', '', '', Paragraph('<para fontSize=7><b>PLUME TYPE:</b><br/></para><para fontSize=7>' + primaryData.plume_type + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>WATER DROPLET PRESENT:</b><br/></para><para fontSize=7>' + primaryData.water_drolet_present + '</para>', styles['Normal']), '', '', '', '', '', '', Paragraph('<para fontSize=7><b>IF WATER DROPLET PLUME:</b><br/></para><para fontSize=7>' + primaryData.water_droplet_plume + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>POINT IN PLUME WERE OPACITY WAS DETERMINED</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.plume_opacity_determined_start + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.plume_opacity_determined_stop + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        [Paragraph('<para fontSize=7><b>DESCRIBE BACKGROUND</b><br/></para><para fontSize=7><b>Start:</b>&#160;' + primaryData.describe_background_start + '&#160;&#160;&#160;&#160;<b>Stop:</b>&#160;' + primaryData.describe_background_stop + '</para>', styles['Normal']), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        # bottom tables (0,17)
        ['', bottomHeader, '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', interval, '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', startStop, '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '0', '15', '30', '45'],
        ['', '', '', '', '', '', '', '0', secondaryData.comb_read_1, secondaryData.comb_read_2, secondaryData.comb_read_3, secondaryData.comb_read_4],
        ['', '', '', '', '', '', '', '1', secondaryData.comb_read_5, secondaryData.comb_read_6, secondaryData.comb_read_7, secondaryData.comb_read_8],
        ['', '', '', '', '', '', '', '2', secondaryData.comb_read_9, secondaryData.comb_read_10, secondaryData.comb_read_11, secondaryData.comb_read_12],
        ['', '', '', '', '', '', '', '3', secondaryData.comb_read_13, secondaryData.comb_read_14, secondaryData.comb_read_15, secondaryData.comb_read_16],
        ['', '', '', '', '', '', '', '4', secondaryData.comb_read_17, secondaryData.comb_read_18, secondaryData.comb_read_19, secondaryData.comb_read_20],
        ['', '', '', '', '', '', '', '5', secondaryData.comb_read_21, secondaryData.comb_read_22, secondaryData.comb_read_23, secondaryData.comb_read_24],
    ]
    
    if secondaryData.comb_formL:
        tableInsert = [   
            ['', '', '', '', '', '', '', '6', secondaryData.comb_read_25, secondaryData.comb_read_26, secondaryData.comb_read_27, secondaryData.comb_read_28],
            ['', '', '', '', '', '', '', '7', secondaryData.comb_read_29, secondaryData.comb_read_30, secondaryData.comb_read_31, secondaryData.comb_read_32],
            ['', '', '', '', '', '', '', '8', secondaryData.comb_read_33, secondaryData.comb_read_34, secondaryData.comb_read_35, secondaryData.comb_read_36],
            ['', '', '', '', '', '', '', '9', secondaryData.comb_read_37, secondaryData.comb_read_38, secondaryData.comb_read_39, secondaryData.comb_read_40],
            ['', '', '', '', '', '', '', '10', secondaryData.comb_read_41, secondaryData.comb_read_42, secondaryData.comb_read_43, secondaryData.comb_read_44],
            ['', '', '', '', '', '', '', '11', secondaryData.comb_read_45, secondaryData.comb_read_46, secondaryData.comb_read_47, secondaryData.comb_read_48],
            ['', '', '', '', '', '', '', '12', secondaryData.comb_read_49, secondaryData.comb_read_50, secondaryData.comb_read_51, secondaryData.comb_read_52],
            ['', '', '', '', '', '', '', '13', secondaryData.comb_read_53, secondaryData.comb_read_54, secondaryData.comb_read_55, secondaryData.comb_read_56],
            ['', '', '', '', '', '', '', '14', secondaryData.comb_read_57, secondaryData.comb_read_58, secondaryData.comb_read_59, secondaryData.comb_read_60],
            ['', '', Paragraph('<para fontSize=10 align=center><b>Highest 6-reading Average Opacity for Push:&#160;</b>' + str(secondaryData.comb_average) + '%</para>', styles['Normal'])],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ]
        tableRowHeights = (20, 20, 5, 20, 20, 20, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 15, 15, 15, 5, 20, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 25, 20)
    else:
        tableInsert = [
            ['', '', Paragraph('<para fontSize=10 align=center><b>Highest 6-reading Average Opacity for Push:&#160;</b>' + str(secondaryData.comb_average) + '%</para>', styles['Normal'])],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ]
        tableRowHeights = (20, 20, 5, 20, 20, 20, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 15, 15, 15, 5, 20, 15, 15, 15, 15, 15, 15, 15, 25, 20)
        
    for lines in tableInsert:
        tableData.append(lines)
    
    tableColWidths = (45,10,20,20,25,30,40, 30,40,40,40,40,20,42,42,42,42)
    
    style = [
        #Fonts
        ('FONT', (0,0), (-1,0), 'Times-Bold', 16),
        ('FONT', (0,1), (-1,1), 'Times-Bold', 10),
        
        #Top header and info
        #('BOTTOMPADDING',(0,1), (-1,1), 5),
        ('SPAN', (0,0), (-1,0)),
        ('SPAN', (0,1), (-1,1)),
        ('ALIGN', (0,0), (-1,1), 'CENTER'),
        
        # top table information
        ('VALIGN', (0,6), (-1,15), 'MIDDLE'),
        ('GRID', (0,3), (-1,8), 0.5, colors.black),
        ('GRID', (0,3), (11,15), 0.5, colors.black),
        ('SPAN', (0,3), (10,3)),
        ('SPAN', (11,3), (13,3)),
        ('SPAN', (14,3), (-1,3)),
        
        ('SPAN', (0,4), (10,4)),
        ('SPAN', (11,4), (13,4)),
        ('SPAN', (14,4), (-1,4)),
        
        ('SPAN', (0,5), (2,5)),
        ('SPAN', (3,5), (13,5)),
        ('SPAN', (14,5), (-1,5)),
        
        ('SPAN', (0,6), (8,6)),
        ('SPAN', (9,6), (11,6)),
        ('SPAN', (12,6), (14,6)),
        ('SPAN', (15,6), (-1,6)),
        
        ('SPAN', (0,7), (8,7)),
        ('SPAN', (9,7), (11,7)),
        ('SPAN', (12,7), (14,7)),
        ('SPAN', (15,7), (-1,7)),
        
        ('SPAN', (0,8), (11,8)),
        ('SPAN', (12,8), (14,8)),
        ('SPAN', (15,8), (-1,8)),
        
        ('SPAN', (0,9), (5,9)),
        ('SPAN', (6,9), (10,9)),
        
        ('SPAN', (0,10), (5,10)),
        ('SPAN', (6,10), (10,10)),
        
        ('SPAN', (0,11), (10,11)),
        
        ('SPAN', (0,12), (6,12)),
        ('SPAN', (7,12), (10,12)),
        
        ('SPAN', (0,13), (6,13)),
        ('SPAN', (7,13), (10,13)),
        
        ('SPAN', (0,14), (10,14)),
        
        ('SPAN', (0,15), (10,15)),
        
        ('SPAN', (11,9), (-1,15)),
        ('BOX', (11,9), (-1,15), 0.5, colors.black),
    ]
    
    if secondaryData.comb_formL:
        styleInsert = [
            #bottom table
            ('BACKGROUND', (7,21), (11,21),'(.6,.7,.8)'),
            ('SPAN', (1,17), (-2,17)),
            ('SPAN', (1,18), (-2,18)),
            ('ALIGN', (1,18), (-2,18), 'CENTER'),
            ('SPAN', (1,20), (-2,20)),
            ('GRID', (7,21), (11,36), 0.5, colors.black),
            ('ALIGN', (7,21), (11,36), 'CENTER'),
            ('VALIGN', (7,21), (11,36), 'MIDDLE'),
            ('SPAN', (2,37), (-2,37)),
        ]
    else:
        styleInsert = [
            ('BACKGROUND', (7,21), (11,21),'(.6,.7,.8)'),
            ('SPAN', (1,17), (-2,17)),
            ('SPAN', (1,18), (-2,18)),
            ('ALIGN', (1,18), (-2,18), 'CENTER'),
            ('SPAN', (1,20), (-2,20)),
            ('GRID', (7,21), (11,27), 0.5, colors.black),
            ('ALIGN', (7,21), (11,27), 'CENTER'),
            ('VALIGN', (7,21), (11,27), 'MIDDLE'),
            ('SPAN', (2,28), (-2,28)),
        ]
        
    for lineStyle in styleInsert:
        style.append(lineStyle)
    return tableData, tableColWidths, tableRowHeights, style

def pdf_template_20(primaryData, title, subTitle):
    tableData = [
        [title],
        [subTitle],
        ['', Paragraph('<para align=center><b>Week of:&#160;</b>' + date_change(primaryData.week_start) + '&#160;&#160;to&#160;&#160;' + date_change(primaryData.week_end) + '</para>', styles['Normal']), '', '', '', ''],
        ['', '', '', '', '', ''],
        ['', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        [Paragraph('<para align=center><b>Sampling Time</b></para>', styles['Normal']), time_change(primaryData.time_0), time_change(primaryData.time_1), time_change(primaryData.time_2), time_change(primaryData.time_3), time_change(primaryData.time_4)],
        [Paragraph("<para align=center><b>Inspector's Signature</b></para>", styles['Normal']), primaryData.obser_0, primaryData.obser_1, primaryData.obser_2, primaryData.obser_3, primaryData.obser_4],
        ['', '*Collect 100 mL each day (Monday - Friday)', '', '', '', ''],
    ]
    tableColWidths = (70,80,80,80,80,80)

    style = [
        #Top header and info
        ('FONT', (0,0), (-1,0), 'Times-Bold', 22),
        ('FONT', (0,1), (-1,1), 'Times-Bold', 15),
        ('BOTTOMPADDING',(0,2), (-1,2), 55),
        ('SPAN', (0,0), (-1,0)),
        ('SPAN', (0,1), (-1,1)),
        ('SPAN', (1,2), (4,2)),
        ('ALIGN', (0,0), (-1,2), 'CENTER'),
        
        #table
        ('GRID', (0,4),(-1,6), 0.5,  colors.black),
        ('BOX', (0,4),(-1,6), 1.5,  colors.black),
        ('ALIGN', (0,4), (-1,6), 'CENTER'),
        ('VALIGN', (0,4), (-1,6), 'MIDDLE'),
        
        #under table
        ('TOPPADDING',(0,7), (-1,7), 35),
        ('SPAN', (1,7), (4,7)),
        ('ALIGN', (0,7), (-1,7), 'CENTER'),
    ]
    return tableData, tableColWidths, style

def pdf_template_21(primaryData, title, subTitle):
    tableData = [
        [title],
        [subTitle],
        [Paragraph('<para align=center><b>Week of:&#160;</b>' + date_change(primaryData.week_start) + '&#160;&#160;to&#160;&#160;' + date_change(primaryData.week_end) + '</para>', styles['Normal'])],
        ['', '', '', '', ''],
        [Paragraph('<para align=center><b>Observer</b></para>', styles['Normal']), Paragraph('<para align=center><b>Day/Time</b></para>', styles['Normal']), Paragraph('<para align=center><b>Location</b></para>', styles['Normal']), Paragraph('<para align=center><b>Visible Emissions</b></para>', styles['Normal']), Paragraph('<para align=center><b>Comments</b></para>', styles['Normal'])],
        [primaryData.obser_5, 'Saturday/' + time_change(primaryData.time_5), 'Coal Bin Vents', primaryData.vents_5, Paragraph('<para>' + emptyInputs(primaryData.v_comments_5) + '</para>', styles['Normal'])],
        ['', '', 'Mixer Building Bag House', primaryData.mixer_5, Paragraph('<para>' + emptyInputs(primaryData.m_comments_5) + '</para>', styles['Normal'])],
        [primaryData.obser_6, 'Sunday/' + time_change(primaryData.time_6), 'Coal Bin Vents', primaryData.vents_6, Paragraph('<para>' + emptyInputs(primaryData.v_comments_6) + '</para>', styles['Normal'])],
        ['', '', 'Mixer Building Bag House', primaryData.mixer_6, Paragraph('<para>' + emptyInputs(primaryData.m_comments_6) + '</para>', styles['Normal'])],
        [primaryData.obser_0, 'Monday/' + time_change(primaryData.time_0), 'Coal Bin Vents', primaryData.vents_0, Paragraph('<para>' + emptyInputs(primaryData.v_comments_0) + '</para>', styles['Normal'])],
        ['', '', 'Mixer Building Bag House', primaryData.mixer_0, Paragraph('<para>' + emptyInputs(primaryData.m_comments_0) + '</para>', styles['Normal'])],
        [primaryData.obser_1, 'Tuesday/' + time_change(primaryData.time_1), 'Coal Bin Vents', primaryData.vents_1, Paragraph('<para>' + emptyInputs(primaryData.v_comments_1) + '</para>', styles['Normal'])],
        ['', '', 'Mixer Building Bag House', primaryData.mixer_1, Paragraph('<para>' + emptyInputs(primaryData.m_comments_1) + '</para>', styles['Normal'])],
        [primaryData.obser_2, 'Wednesday/' + time_change(primaryData.time_2), 'Coal Bin Vents', primaryData.vents_2, Paragraph('<para>' + emptyInputs(primaryData.v_comments_2) + '</para>', styles['Normal'])],
        ['', '', 'Mixer Building Bag House', primaryData.mixer_2, Paragraph('<para>' + emptyInputs(primaryData.m_comments_2) + '</para>', styles['Normal'])],
        [primaryData.obser_3, 'Thursday/' + time_change(primaryData.time_3), 'Coal Bin Vents', primaryData.vents_3, Paragraph('<para>' + emptyInputs(primaryData.v_comments_3) + '</para>', styles['Normal'])],
        ['', '', 'Mixer Building Bag House', primaryData.mixer_3, Paragraph('<para>' + emptyInputs(primaryData.m_comments_3) + '</para>', styles['Normal'])],
        [primaryData.obser_4, 'Friday/' + time_change(primaryData.time_4), 'Coal Bin Vents', primaryData.vents_4, Paragraph('<para>' + emptyInputs(primaryData.v_comments_4) + '</para>', styles['Normal'])],
        ['', '', 'Mixer Building Bag House', primaryData.mixer_4, Paragraph('<para>' + emptyInputs(primaryData.m_comments_4) + '</para>', styles['Normal'])],
        ['Observe visual emissions areas once per day', '', '', '', ''],
        ['If visual emission are observed perform a Method 9 Observation for 15 minutes MINIMUM', '', '', '', ''],
        ['If average opacity > 10%, Contact and Notify Enviornmental Engineer', '', '', '', ''],
    ]
    tableColWidths = (70,110,130,65,130)

    style = [
        #Top header and info
        ('FONT', (0,0), (-1,0), 'Times-Bold', 22),
        ('FONT', (0,1), (-1,1), 'Times-Bold', 15),
        ('BOTTOMPADDING',(0,1), (-1,1), 25),
        ('BOTTOMPADDING',(0,2), (-1,2), 25),
        ('SPAN', (0,0), (-1,0)),
        ('SPAN', (0,1), (-1,1)),
        ('SPAN', (0,2), (-1,2)),
        ('ALIGN', (0,0), (-1,2), 'CENTER'),
        
        #table
        ('GRID', (0,4),(-1,4), 1.5,  colors.black),
        ('GRID', (0,5),(-1,18), 0.5,  colors.black),
        ('SPAN', (0,5), (0,6)),
        ('SPAN', (1,5), (1,6)),
        ('SPAN', (0,7), (0,8)),
        ('SPAN', (1,7), (1,8)),
        ('SPAN', (0,9), (0,10)),
        ('SPAN', (1,9), (1,10)),
        ('SPAN', (0,11), (0,12)),
        ('SPAN', (1,11), (1,12)),
        ('SPAN', (0,13), (0,14)),
        ('SPAN', (1,13), (1,14)),
        ('SPAN', (0,15), (0,16)),
        ('SPAN', (1,15), (1,16)),
        ('SPAN', (0,17), (0,18)),
        ('SPAN', (1,17), (1,18)),
        ('VALIGN', (0,5),(-1,18), 'MIDDLE'),
        ('VALIGN', (0,4),(-1,4), 'MIDDLE'),
        ('ALIGN', (0,4),(-1,4), 'CENTER'),
        ('ALIGN', (0,5),(1,18), 'CENTER'),
        ('ALIGN', (3,5),(3,18), 'CENTER'),
        ('TOPPADDING',(0,19), (-1,19), 25),
        ('SPAN', (0,19), (-1,19)),
        ('SPAN', (0,20), (-1,20)),
        ('SPAN', (0,21), (-1,21)),
    ]
    return tableData, tableColWidths, style

def pdf_template_22(primaryData, secondaryData, title, subTitle):
    date = Paragraph('<para align=center font=Times-Roman><b>Date:</b> ' + date_change(primaryData.date) + '</para>', styles['Normal'])
    startStopPaved = Paragraph('<para align=center><b>Start:</b>&#160;' + time_change(primaryData.pav_start) + '&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;<b>End:</b>&#160;' + time_change(primaryData.pav_stop)+ '</para>', styles['Normal'])
    startStopUnPaved = Paragraph('<para align=center><b>Start:</b>&#160;' + time_change(primaryData.unp_start) + '&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;<b>End:</b>&#160;' + time_change(primaryData.unp_stop)+ '</para>', styles['Normal'])
    startStopPark = '&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;<b>Start:</b>&#160;' + time_change(primaryData.par_start) + '&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;<b>End:</b>&#160;' + time_change(primaryData.par_stop)
    observerCert = Paragraph('<para align=center><b>Observer:</b>&#160;' + primaryData.observer + '&#160;&#160;&#160;&#160;<b>Certified Date:</b>&#160;' + date_change(primaryData.cert_date) + '</para>', styles['Normal'])
    comments = Paragraph('<para align=left><b>Comments:</b>    ' + primaryData.comments + '</para>', styles['Normal'])
    print(primaryData.unpaved)
    tableData = [
        [title],
        [subTitle],
        [date],
        ['','','','','','','',''],
        ['',Paragraph('<para align=left><b>Paved:</b> ' + road_choices(primaryData.paved) + '</para>', styles['Normal']),'',startStopPaved,'','','',''],
        ['','MIN/SEC','0','15','30','45','',''],
        ['','0',secondaryData.pav_1,secondaryData.pav_2,secondaryData.pav_3,secondaryData.pav_4,'',''],
        ['','1',secondaryData.pav_5,secondaryData.pav_6,secondaryData.pav_7,secondaryData.pav_8,'',''],
        ['','2',secondaryData.pav_9,secondaryData.pav_10,secondaryData.pav_11,secondaryData.pav_12,'',''],
        ['','3-minute Average Opacity (sum of the 12 readings above/12)','','','','',secondaryData.pav_total,''],
        ['','','','','','','',''],
        ['',Paragraph('<para align=left><b>Area:</b> ' + road_choices(primaryData.unpaved) + '</para>', styles['Normal']),'',startStopUnPaved,'','','',''],
        ['','MIN/SEC','0','15','30','45','',''],
        ['','0',secondaryData.unp_1,secondaryData.unp_2,secondaryData.unp_3,secondaryData.unp_4,'',''],
        ['','1',secondaryData.unp_5,secondaryData.unp_6,secondaryData.unp_7,secondaryData.unp_8,'',''],
        ['','2',secondaryData.unp_9,secondaryData.unp_10,secondaryData.unp_11,secondaryData.unp_12,'',''],
        ['','3-minute Average Opacity (sum of the 12 readings above/12)','','','','',secondaryData.unp_total,''],
        ['','','','','','','',''],
        ['',Paragraph('<para align=left><b>Parking Lot:</b> ' + road_choices(primaryData.parking) + startStopPark + '</para>', styles['Normal']),'','','','','',''],
        ['','MIN/SEC','0','15','30','45','',''],
        ['','0',secondaryData.par_1,secondaryData.par_2,secondaryData.par_3,secondaryData.par_4,'',''],
        ['','1',secondaryData.par_5,secondaryData.par_6,secondaryData.par_7,secondaryData.par_8,'',''],
        ['','2',secondaryData.par_9,secondaryData.par_10,secondaryData.par_11,secondaryData.par_12,'',''],
        ['','3-minute Average Opacity (sum of the 12 readings above/12)','','','','',secondaryData.par_total,''],
        ['','','','','','','',''],
        ['',observerCert,'','','','','',''],
        ['','','','','','','',''],
        ['',comments,'','','','','',''],
    ]
    
    tableColWidths = (60,75,75,75,75,75,40,60)
    
    style = [
        #Top header and info
        ('FONT', (0,0), (-1,0), 'Times-Bold', 18),
        ('FONT', (0,1), (-1,1), 'Times-Bold', 10),
        #('BOTTOMPADDING',(0,2), (-1,2), 5),
        ('SPAN', (0,0), (-1,0)),
        ('SPAN', (0,1), (-1,1)),
        ('SPAN', (0,2), (-1,2)),
        ('ALIGN', (0,0), (-1,2), 'CENTER'),
        
        #pav table (1,4)
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
        
        #unpaved table (1,11)
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
        
        #park table
        ('GRID',(1,19), (-3,23), 0.5,colors.black),
        ('BOX',(1,18), (-3,23), 0.5,colors.black),
        ('GRID',(6,23), (-2,23), 0.5,colors.black),
        ('SPAN', (1,18), (5,18)),
        ('SPAN', (1,23), (5,23)),
        ('ALIGN', (1,19), (5,22), 'CENTER'),
        ('ALIGN', (6,23), (6,23), 'CENTER'),
        ('SPAN', (3,18), (5,18)),
        ('ALIGN', (3,18), (5,18), 'RIGHT'),
        ('BACKGROUND', (1,19), (5,19),'(.6,.7,.8)'),
        
        #ending data (1,18)
        ('SPAN', (1,25), (6,25)),
        ('SPAN', (1,27), (6,27)),
    ]
    return tableData, tableColWidths, style

def pdf_template_23(formDate, facility):
    try:
        parseDateN = datetime.datetime.strptime(formDate, "%Y-%m")
    except:
        parseDateN = datetime.datetime.strptime(formDate, "%Y-%m-%d")
    daysInMonth = calendar.monthrange(parseDateN.year, parseDateN.month)
    newDateN = str(parseDateN.year) + '-' + str(parseDateN.month) + '-' + '01'
    parseDateStart = datetime.datetime.strptime(newDateN, "%Y-%m-%d").date()
    parseDateStop = parseDateStart + datetime.timedelta(days=(daysInMonth[1] - 1))
    dataN = form22_model.objects.filter(facilityChoice__facility_name=facility, date__year=parseDateN.year, date__month=parseDateN.month)
    new = 'Fugitive Dust Inspection'
    titleN = 'Method 9D Monthly Checklist - (N)'
    subTitleN = 'Facility Name: ' + facility
    dateN = str(parseDateN.month) + '-' + str(parseDateN.year)
    tableData = [   
        [titleN],
        [subTitleN],
        [dateN],
        ['','','','','','','',''],
        ['','Paved Roads','','','Dates','','',''],
    ]
    
    def roadFunc(allForms, typeRoad):
        paved_roads = {
            'p1': '#4 Booster Station',
            'p2': '#5 Battery Road',
            'p3': 'Coal Dump Horseshoe',
            'p4': 'Coal Handling Road (Partial)',
            'p5': 'Coke Plant Road',
            'p6': 'Coke Plant Mech Road',
            'p7': 'North Gate Area',
            'p8': 'Compund Road',
            'p9': 'D-4 Blast Furnace Road',
            'p10': 'Gap Gate Road',
            'p11': '#3 Ore Dock Road',
            'p12': 'River Road',
            'p13': 'Weigh Station Road',
            'p14': 'Zug Island Road'
        }
        unpaved_roads = {
            'unp1': 'North Gate Truck Turn',
            'unp2': 'Screening Station Road',
            'unp3': 'Coal Handling Road (Partial)',
            'unp4': 'Taj Mahal Road',
            'unp5': 'PECS Approach',
            'unp6': 'No. 2 Boilerhouse Road',
            'unp7': 'Bypass Route',
        }
        parking_lots = {
            'par1': 'Gap Gate Parking',
            'par2': 'Truck Garage Area',
            'par3': 'EES Coke Office Parking',
        }
        if typeRoad == 'paved':
            rangeSet = 14
            varSelect = 'p'
            sorter = paved_roads
        elif typeRoad == 'unpaved':
            rangeSet = 7
            varSelect = 'unp'
            sorter = unpaved_roads
        elif typeRoad == 'parking':
            rangeSet = 3
            varSelect = 'par'
            sorter = parking_lots
            
        dateList = []
        for paved in range(rangeSet):
            roadSelector = varSelect + str(paved + 1)
            road_string = sorter[roadSelector]
            rowList = ''
            for entry in allForms:
                if typeRoad == 'paved':
                    entrySel = entry.paved
                elif typeRoad == 'unpaved':
                    entrySel = entry.unpaved
                elif typeRoad == 'parking':
                    entrySel = entry.parking
                    
                if entrySel == roadSelector:
                    roadDate = '(' + str(entry.date.month) + '/' + str(entry.date.day) + ')'
                    if rowList == '':
                        rowList += roadDate
                    else:
                        rowList += ', ' + roadDate
            dateList.append((road_string, rowList))
            
        roadInsert = []
        for insert in dateList:
            roadInsert.append(['',insert[0],'','',insert[1],'','',''],)
        return roadInsert
    
    for line in roadFunc(dataN, 'paved'):
        tableData.append(line)
    
    tableData.append(['','Unpaved Roads','','','Dates','','',''])
    
    for line in roadFunc(dataN, 'unpaved'):
        tableData.append(line)
        
    tableData.append(['','Parking Lots','','','Dates','','',''])
    
    for line in roadFunc(dataN, 'parking'):
        tableData.append(line)
        
    tableColWidths = (60,50,40,60,70,70,70,60)
    
    style = [
        #Top header and info
        ('FONT', (0,0), (-1,0), 'Times-Bold', 18),
        ('FONT', (0,1), (-1,1), 'Times-Bold', 10),
        #('BOTTOMPADDING',(0,2), (-1,2), 5),
        ('SPAN', (0,0), (-1,0)),
        ('SPAN', (0,1), (-1,1)),
        ('SPAN', (0,2), (-1,2)),
        ('ALIGN', (0,0), (-1,2), 'CENTER'),
        #general
        ('GRID',(1,4), (6,30), 0.5,colors.black),
        #Table paved (1,4)
            #header
        ('SPAN', (1,4), (3,4)),
        ('SPAN', (4,4), (6,4)),
        ('BACKGROUND', (1,4), (6,4),'(.6,.7,.8)'),
        ('ALIGN', (1,4), (6,4), 'CENTER'),
        
        #Table unpaved (1,19)
            #header
        ('SPAN', (1,19), (3,19)),
        ('SPAN', (4,19), (6,19)),
        ('BACKGROUND', (1,19), (6,19),'(.6,.7,.8)'),
        ('ALIGN', (1,19), (6,19), 'CENTER'),
        
        #Table unpaved (1,27)
            #header
        ('SPAN', (1,27), (3,27)),
        ('SPAN', (4,27), (6,27)),
        ('BACKGROUND', (1,27), (6,27),'(.6,.7,.8)'),
        ('ALIGN', (1,27), (6,27), 'CENTER'),
        
    ]
    styleInsert = []
    for i in range(30):
        mark = 4 + (i-1)
        styleInsert.append(('SPAN', (1,mark), (3,mark)))
        styleInsert.append(('SPAN', (4,mark), (6,mark)))
    
    for line in styleInsert:
        style.append(line)       
    return tableData, tableColWidths, style

def pdf_template_24(primaryData, title, subTitle):
    tableData = [
        [title],
        [subTitle],
        ['', Paragraph('<para align=center><b>Date:&#160;</b>' + date_change(primaryData.date) + '</para>', styles['Normal']), '', '', '', ''],
        ['', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['', '', Paragraph('<para><b>Flow observed at monitoring location?</b></para>', styles['Normal']), primaryData.Q_1, '', ''],
        ['', '', Paragraph('<para><b>Does the observed flow have an unnatural turbidity?</b></para>', styles['Normal']), primaryData.Q_2, '', ''],
        ['', '', Paragraph('<para><b>Does the observed flow have an unnatural color?</b></para>', styles['Normal']), primaryData.Q_3, '', ''],
        ['', '', Paragraph('<para><b>Does the observed flow have an oil film?</b></para>', styles['Normal']), primaryData.Q_4, '', ''],
        ['', '', Paragraph('<para><b>Does the observed flow have floating solids?</b></para>', styles['Normal']), primaryData.Q_5, '', ''],
        ['', '', Paragraph('<para><b>Does the observed flow have foams?</b></para>', styles['Normal']), primaryData.Q_6, '', ''],
        ['', '', Paragraph('<para><b>Does the observed flow have settleable solids?</b></para>', styles['Normal']), primaryData.Q_7, '', ''],
        ['', '', Paragraph('<para><b>Does the observed flow have suspended solids?</b></para>', styles['Normal']), primaryData.Q_8, '', ''],
        ['', '', Paragraph('<para><b>Does the observed flow have deposits?</b></para>', styles['Normal']), primaryData.Q_9, '', ''],
        ['', '', '', '', '', ''],
        ['', Paragraph('<para><b>Comments (Describe any problemsor conditions found during inspections)</b></para>', styles['Normal']), '', primaryData.comments, '', ''],
        ['', Paragraph('<para><b>Actions Taken (Include date mitigated)</b></para>', styles['Normal']), '', primaryData.actions_taken, '', ''],
    ]
    tableColWidths = (40,50,270,80,50,40)

    style = [
        #Top header and info
        ('FONT', (0,0), (-1,0), 'Times-Bold', 22),
        ('FONT', (0,1), (-1,1), 'Times-Bold', 15),
        ('BOTTOMPADDING',(0,2), (-1,2), 0),
        ('SPAN', (0,0), (-1,0)),
        ('SPAN', (0,1), (-1,1)),
        ('BOTTOMPADDING',(0,1), (-1,1), 15),
        ('SPAN', (1,2), (4,2)),
        ('ALIGN', (0,0), (-1,2), 'CENTER'),
        
        #table
        ('GRID',(2,5), (3,13), 0.5,colors.black),
        ('SPAN', (2,4), (3,4)),
        ('ALIGN', (2,4), (3,4), 'CENTER'),
        ('ALIGN', (3,5), (3,13), 'CENTER'),
        ('SPAN', (1,15), (2,15)),
        ('SPAN', (3,15), (4,15)),
        ('SPAN', (1,16), (2,16)),
        ('SPAN', (3,16), (4,16)),
        ('GRID',(1,15), (4,16), 0.5,colors.black),
        ('ALIGN', (3,15), (4,16), 'CENTER'),
        ('VALIGN', (3,15), (4,16), 'MIDDLE'),
    ]
    return tableData, tableColWidths, style

def pdf_template_25(primaryData, title, subTitle):
    #title = 'Outfall 008 Observation Form' + ' - Form (' + formInformation.form + ')'
    tableData = [
        [title],
        [subTitle],
        ['', Paragraph('<para align=center><b>Date:&#160;</b>' + date_change(primaryData.date) + '</para>', styles['Normal']), '', '', '', ''],
        ['', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['', '', Paragraph('<para><b>Flow observed at monitoring location?</b></para>', styles['Normal']), primaryData.Q_1, '', ''],
        ['', '', Paragraph('<para><b>Does the observed flow have an unnatural turbidity?</b></para>', styles['Normal']), primaryData.Q_2, '', ''],
        ['', '', Paragraph('<para><b>Does the observed flow have an unnatural color?</b></para>', styles['Normal']), primaryData.Q_3, '', ''],
        ['', '', Paragraph('<para><b>Does the observed flow have an oil film?</b></para>', styles['Normal']), primaryData.Q_4, '', ''],
        ['', '', Paragraph('<para><b>Does the observed flow have floating solids?</b></para>', styles['Normal']), primaryData.Q_5, '', ''],
        ['', '', Paragraph('<para><b>Does the observed flow have foams?</b></para>', styles['Normal']), primaryData.Q_6, '', ''],
        ['', '', Paragraph('<para><b>Does the observed flow have settleable solids?</b></para>', styles['Normal']), primaryData.Q_7, '', ''],
        ['', '', Paragraph('<para><b>Does the observed flow have suspended solids?</b></para>', styles['Normal']), primaryData.Q_8, '', ''],
        ['', '', Paragraph('<para><b>Does the observed flow have deposits?</b></para>', styles['Normal']), primaryData.Q_9, '', ''],
        ['', '', '', '', '', ''],
        ['', Paragraph('<para><b>Comments (Describe any problemsor conditions found during inspections)</b></para>', styles['Normal']), '', primaryData.comments, '', ''],
        ['', Paragraph('<para><b>Actions Taken (Include date mitigated)</b></para>', styles['Normal']), '', primaryData.actions_taken, '', ''],
    ]
    tableColWidths = (40,50,270,80,50,40)

    style = [
        #Top header and info
        ('FONT', (0,0), (-1,0), 'Times-Bold', 22),
        ('FONT', (0,1), (-1,1), 'Times-Bold', 15),
        ('BOTTOMPADDING',(0,2), (-1,2), 0),
        ('SPAN', (0,0), (-1,0)),
        ('SPAN', (0,1), (-1,1)),
        ('BOTTOMPADDING',(0,1), (-1,1), 15),
        ('SPAN', (1,2), (4,2)),
        ('ALIGN', (0,0), (-1,2), 'CENTER'),
        
        #table
        ('GRID',(2,5), (3,13), 0.5,colors.black),
        ('SPAN', (2,4), (3,4)),
        ('ALIGN', (2,4), (3,4), 'CENTER'),
        ('ALIGN', (3,5), (3,13), 'CENTER'),
        ('SPAN', (1,15), (2,15)),
        ('SPAN', (3,15), (4,15)),
        ('SPAN', (1,16), (2,16)),
        ('SPAN', (3,16), (4,16)),
        ('GRID',(1,15), (4,16), 0.5,colors.black),
        ('ALIGN', (3,15), (4,16), 'CENTER'),
        ('VALIGN', (3,15), (4,16), 'MIDDLE'),
    ]
    return tableData, tableColWidths, style

def pdf_template_26(primaryData, title, subTitle, formInformation):
    title = formInformation.header + ' - ' + formInformation.title
    tableData = [
        [title],
        [subTitle],
        [Paragraph('<para align=center><b>Month:&#160;</b>' + primaryData.inspector + '</para>', styles['Normal']), '', '', '', ''],
        ['', '', '', '', '', ''],
        [Paragraph('<para align=center><b>Inspector Names:&#160;</b>' + primaryData.inspector + '&#160;&#160;&#160;&#160;&#160;<b>Date:&#160;</b>' + date_change(primaryData.date) +'</para>', styles['Normal']), '', '', '', ''],
        ['', '', '', '', '', ''],
        [Paragraph('<para align=center><b>Spill Kit #</b></para>', styles['Normal']), Paragraph('<para align=center><b>Tag On?</b></para>', styles['Normal']), Paragraph('<para align=center><b>Inventory</b></para>', styles['Normal']), Paragraph('<para align=center><b>Tag Serial #</b></para>', styles['Normal']), Paragraph('<para align=center><b>Complete Kit?</b></para>', styles['Normal']), Paragraph('<para align=center><b>Incident Report</b></para>', styles['Normal']), Paragraph('<para align=center><b>Comments</b></para>', styles['Normal'])]
    ]
    tableColWidths = (50,80,80,80,80,80,80)

    style = [
        #Top header and info
        ('FONT', (0,0), (-1,0), 'Times-Bold', 22),
        ('FONT', (0,1), (-1,1), 'Times-Bold', 15),
        ('BOTTOMPADDING',(0,2), (-1,2), 5),
        ('SPAN', (0,0), (-1,0)),
        ('SPAN', (0,1), (-1,1)),
        ('SPAN', (0,2), (-1,2)),
        ('SPAN', (0,4), (-1,4)),
        ('ALIGN', (0,0), (-1,2), 'CENTER'),
        
        #table
        ('GRID', (0,6),(-1,27), 0.5,  colors.black),
        ('BOX', (0,6),(-1,6), 1.5,  colors.black),
        ('ALIGN', (0,4), (-1,6), 'CENTER'),
        ('VALIGN', (0,4), (-1,6), 'MIDDLE'),
        ('ALIGN', (0,6), (-1,27), 'CENTER'),
        
        ('GRID', (0,30),(-1,35), 0.5,  colors.black),
        ('ALIGN', (0,30),(-1,35), 'CENTER'),
    ]
    return tableData, tableColWidths, style

def pdf_template_27(primaryData, title, subTitle, formInformation):
    title = Paragraph('<para fontSize=20 align=center font=Times-Bold leading=25><b>' + formInformation.header + '<br/>' + formInformation.title + ' - Form (' + formInformation.form + ')</b></para>', styles['Normal'])
    tableData = [
        [title],
        [subTitle],
        ['', '', Paragraph('<para>' + str(primaryData.date.year) + '&#160;&#160;-&#160;&#160;' + quarterParse(int(primaryData.quarter)) + '</para>', styles['Normal']), '', '', ''],
        ['Truck 5', '', '', '', '', ''],
        #truck 5 start (0,4)
        [Paragraph('<para><b>Observer:&#160;</b>' + primaryData.observer_5_1 + '</para>', styles['Normal']), Paragraph('<para><b>Date:&#160;</b>' + str(primaryData.date_5_1) + '</para>', styles['Normal']), Paragraph('<para><b>Time:&#160;</b>' + time_change(primaryData.time_5_1) + '</para>', styles['Normal']), ''],
        [Paragraph('<para><b>1) Condition of Rear Gate Satisfactory:&#160;</b>' + primaryData.rear_gate_5_1 + '</para>', styles['Normal']), ''],
        [Paragraph('<para><b>2) Condition of Box Interior Satisfactory:&#160;</b>' + primaryData.box_interior_5_1 + '</para>', styles['Normal']), ''],
        [Paragraph('<para><b>3) Condition of Box Exterior Satisfactory:&#160;</b>' + primaryData.box_exterior_5_1 + '</para>', styles['Normal']), ''],
        [Paragraph('<para><b>4) Exhaust Position Satisfactory:&#160;</b>' + primaryData.exhaust_5_1 + '</para>', styles['Normal']), ''],
        [Paragraph('<para><b>Comments:&#160;</b>' + primaryData.comments_5_1 + '</para>', styles['Normal']), '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['Truck 6', '', '', '', '', ''],
        #truck 6 start (0,12)
        [Paragraph('<para><b>Observer:&#160;</b>' + primaryData.observer_6_2 + '</para>', styles['Normal']), Paragraph('<para><b>Date:&#160;</b>' + str(primaryData.date_6_2) + '</para>', styles['Normal']), Paragraph('<para><b>Time:&#160;</b>' + time_change(primaryData.time_6_2) + '</para>', styles['Normal']), '', '', ''],
        [Paragraph('<para><b>1) Condition of Rear Gate Satisfactory:&#160;</b>' + primaryData.rear_gate_6_2 + '</para>', styles['Normal']), ''],
        [Paragraph('<para><b>2) Condition of Box Interior Satisfactory:&#160;</b>' + primaryData.box_interior_6_2 + '</para>', styles['Normal']), ''],
        [Paragraph('<para><b>3) Condition of Box Exterior Satisfactory:&#160;</b>' + primaryData.box_exterior_6_2 + '</para>', styles['Normal']), ''],
        [Paragraph('<para><b>4) Exhaust Position Satisfactory:&#160;</b>' + primaryData.exhaust_6_2 + '</para>', styles['Normal']), ''],
        [Paragraph('<para><b>Comments:&#160;</b>' + primaryData.comments_6_2 + '</para>', styles['Normal']), ''],
        ['', '', '', '', '', ''],
        ['Truck 7', '', '', '', '', ''],
        #truck 7 start (0,20)
        [Paragraph('<para><b>Observer:&#160;</b>' + primaryData.observer_7_3 + '</para>', styles['Normal']), Paragraph('<para><b>Date:&#160;</b>' + str(primaryData.date_7_3) + '</para>', styles['Normal']), Paragraph('<para><b>Time:&#160;</b>' + time_change(primaryData.time_7_3) + '</para>', styles['Normal']), '', '', ''],
        [Paragraph('<para><b>1) Condition of Rear Gate Satisfactory:&#160;</b>' + primaryData.rear_gate_7_3 + '</para>', styles['Normal']), ''],
        [Paragraph('<para><b>2) Condition of Box Interior Satisfactory:&#160;</b>' + primaryData.box_interior_7_3 + '</para>', styles['Normal']), ''],
        [Paragraph('<para><b>3) Condition of Box Exterior Satisfactory:&#160;</b>' + primaryData.box_exterior_7_3 + '</para>', styles['Normal']), ''],
        [Paragraph('<para><b>4) Exhaust Position Satisfactory:&#160;</b>' + primaryData.exhaust_7_3 + '</para>', styles['Normal']), ''],
        [Paragraph('<para><b>Comments:&#160;</b>' + primaryData.comments_7_3 + '</para>', styles['Normal']), ''],
        ['', '', '', '', '', ''],
        ['Truck 9', '', '', '', '', ''],
        #truck 9 start (0,28)
        [Paragraph('<para><b>Observer:&#160;</b>' + primaryData.observer_9_4 + '</para>', styles['Normal']), Paragraph('<para><b>Date:&#160;</b>' + str(primaryData.date_9_4) + '</para>', styles['Normal']), Paragraph('<para><b>Time:&#160;</b>' + time_change(primaryData.time_9_4) + '</para>', styles['Normal']), '', '', ''],
        [Paragraph('<para><b>1) Condition of Rear Gate Satisfactory:&#160;</b>' + primaryData.rear_gate_9_4 + '</para>', styles['Normal']), '', '', '', '', ''],
        [Paragraph('<para><b>2) Condition of Box Interior Satisfactory:&#160;</b>' + primaryData.box_interior_9_4 + '</para>', styles['Normal']), '', '', '', '', ''],
        [Paragraph('<para><b>3) Condition of Box Exterior Satisfactory:&#160;</b>' + primaryData.box_exterior_9_4 + '</para>', styles['Normal']), '', '', '', '', ''],
        [Paragraph('<para><b>4) Exhaust Position Satisfactory:&#160;</b>' + primaryData.exhaust_9_4 + '</para>', styles['Normal']), '', '', '', '', ''],
        [Paragraph('<para><b>Comments:&#160;</b>' + primaryData.comments_9_4 + '</para>', styles['Normal']), '', '', '', '', ''],
        ['', '', '', '', '', ''],
    ]
    
    tableColWidths = (120,120,100,90,50,20)

    style = [
        #Top header and info
        ('FONT', (0,0), (-1,0), 'Times-Bold', 22),
        ('FONT', (0,1), (-1,1), 'Times-Bold', 15),
        ('BOTTOMPADDING',(0,2), (-1,2), 15),
        ('SPAN', (0,0), (-1,0)),
        ('SPAN', (0,1), (-1,1)),
        ('SPAN', (2,2), (3,2)),
        ('ALIGN', (0,0), (-1,2), 'CENTER'),
        
        #truck 5
        ('BOX',(0,3), (-3,9), 0.5,colors.black),
        ('FONT', (0,3), (0,3), 'Times-Bold', 15),
        ('SPAN', (0,3), (-3,3)),
        ('ALIGN', (0,3), (-3,3), 'LEFT'),
        ('SPAN', (0,5), (1,5)),
        ('SPAN', (2,4), (3,4)),
        ('SPAN', (4,4), (5,4)),
        ('SPAN', (4,5), (5,5)),
        ('SPAN', (0,6), (2,6)),
        ('SPAN', (0,7), (3,7)),
        ('SPAN', (0,8), (3,8)),
        ('SPAN', (0,9), (3,9)),
        
        #truck 6
        ('BOX',(0,11), (-3,17), 0.5,colors.black),
        ('FONT', (0,11), (0,11), 'Times-Bold', 15),
        ('SPAN', (0,11), (-3,11)),
        ('ALIGN', (0,11), (-3,11), 'LEFT'),
        ('SPAN', (0,13), (1,13)),
        ('SPAN', (2,12), (3,12)),
        ('SPAN', (4,12), (5,12)),
        ('SPAN', (0,14), (3,14)),
        ('SPAN', (0,15), (2,15)),
        ('SPAN', (0,16), (3,16)),
        ('SPAN', (0,17), (3,17)),
        ('SPAN', (0,18), (3,18)),
        
        #truck 7
        ('BOX',(0,19), (-3,25), 0.5,colors.black),
        ('FONT', (0,19), (0,19), 'Times-Bold', 15),
        ('SPAN', (0,19), (-3,19)),
        ('ALIGN', (0,19), (-3,19), 'LEFT'),
        ('SPAN', (0,21), (1,21)),
        ('SPAN', (2,20), (3,20)),
        ('SPAN', (4,20), (5,20)),
        ('SPAN', (0,22), (3,22)),
        ('SPAN', (0,23), (2,23)),
        ('SPAN', (0,24), (3,24)),
        ('SPAN', (0,25), (3,25)),
        ('SPAN', (0,26), (3,26)),
        
        #truck 9
        ('BOX',(0,27), (-3,33), 0.5,colors.black),
        ('FONT', (0,27), (0,27), 'Times-Bold', 15),
        ('SPAN', (0,27), (-3,27)),
        ('ALIGN', (0,27), (-3,27), 'LEFT'),
        ('SPAN', (0,29), (1,29)),
        ('SPAN', (2,28), (3,28)),
        ('SPAN', (4,31), (5,31)),
        ('SPAN', (4,32), (5,32)),
        ('SPAN', (0,30), (2,30)),
        ('SPAN', (0,31), (3,31)),
        ('SPAN', (0,32), (3,32)),
        ('SPAN', (0,33), (3,33)),
    ]
    return tableData, tableColWidths, style

def pdf_template_29(primaryData, title, subTitle, formInformation):
    title = formInformation.header + ' - ' + formInformation.title
    tableData = [
        [title],
        [subTitle],
        [Paragraph('<para align=center><b>Month:&#160;</b>' + primaryData.month + '</para>', styles['Normal']), '', '', '', ''],
        ['', '', '', '', '', ''],
        [Paragraph('<para align=center><b>Inspector Names:&#160;</b>' + primaryData.observer + '&#160;&#160;&#160;&#160;&#160;<b>Date:&#160;</b>' + date_change(primaryData.date) +'</para>', styles['Normal']), '', '', '', ''],
        ['', '', '', '', '', ''],
        [Paragraph('<para align=center><b>Spill Kit #</b></para>', styles['Normal']), Paragraph('<para align=center><b>Tag On?</b></para>', styles['Normal']), Paragraph('<para align=center><b>Inventory</b></para>', styles['Normal']), Paragraph('<para align=center><b>Tag Serial #</b></para>', styles['Normal']), Paragraph('<para align=center><b>Complete Kit?</b></para>', styles['Normal']), Paragraph('<para align=center><b>Incident Report</b></para>', styles['Normal']), Paragraph('<para align=center><b>Comments</b></para>', styles['Normal'])],
        ['1', str(primaryData.sk1_tag_on), inventoryResponse(str(primaryData.sk1_tag_on), 1), str(primaryData.sk1_serial), str(primaryData.sk1_complete), str(primaryData.sk1_report), Paragraph('<para align=center>'+primaryData.sk1_comment+'</para>', styles['Normal'])],
        ['2', str(primaryData.sk2_tag_on), inventoryResponse(str(primaryData.sk2_tag_on), 2), str(primaryData.sk2_serial), str(primaryData.sk2_complete), str(primaryData.sk2_report), Paragraph('<para align=center>'+primaryData.sk2_comment+'</para>', styles['Normal'])],
        ['3', str(primaryData.sk3_tag_on), inventoryResponse(str(primaryData.sk3_tag_on), 3), str(primaryData.sk3_serial), str(primaryData.sk3_complete), str(primaryData.sk3_report), Paragraph('<para align=center>'+primaryData.sk3_comment+'</para>', styles['Normal'])],
        ['4', str(primaryData.sk4_tag_on), inventoryResponse(str(primaryData.sk4_tag_on), 4), str(primaryData.sk4_serial), str(primaryData.sk4_complete), str(primaryData.sk4_report), Paragraph('<para align=center>'+primaryData.sk4_comment+'</para>', styles['Normal'])],
        ['5', str(primaryData.sk5_tag_on), inventoryResponse(str(primaryData.sk5_tag_on), 5), str(primaryData.sk5_serial), str(primaryData.sk5_complete), str(primaryData.sk5_report), Paragraph('<para align=center>'+primaryData.sk5_comment+'</para>', styles['Normal'])],
        ['6', str(primaryData.sk6_tag_on), inventoryResponse(str(primaryData.sk6_tag_on), 6), str(primaryData.sk6_serial), str(primaryData.sk6_complete), str(primaryData.sk6_report), Paragraph('<para align=center>'+primaryData.sk6_comment+'</para>', styles['Normal'])],
        ['7', str(primaryData.sk7_tag_on), inventoryResponse(str(primaryData.sk7_tag_on), 7), str(primaryData.sk7_serial), str(primaryData.sk7_complete), str(primaryData.sk7_report), Paragraph('<para align=center>'+primaryData.sk7_comment+'</para>', styles['Normal'])],
        ['8', str(primaryData.sk8_tag_on), inventoryResponse(str(primaryData.sk8_tag_on), 8), str(primaryData.sk8_serial), str(primaryData.sk8_complete), str(primaryData.sk8_report), Paragraph('<para align=center>'+primaryData.sk8_comment+'</para>', styles['Normal'])],
        ['9', str(primaryData.sk9_tag_on), inventoryResponse(str(primaryData.sk9_tag_on), 9), str(primaryData.sk9_serial), str(primaryData.sk9_complete), str(primaryData.sk9_report), Paragraph('<para align=center>'+primaryData.sk9_comment+'</para>', styles['Normal'])],
        ['10', str(primaryData.sk10_tag_on), inventoryResponse(str(primaryData.sk10_tag_on), 10), str(primaryData.sk10_serial), str(primaryData.sk10_complete), str(primaryData.sk10_report), Paragraph('<para align=center>'+primaryData.sk10_comment+'</para>', styles['Normal'])],
        ['11', str(primaryData.sk11_tag_on), inventoryResponse(str(primaryData.sk11_tag_on), 11), str(primaryData.sk11_serial), str(primaryData.sk11_complete), str(primaryData.sk11_report), Paragraph('<para align=center>'+primaryData.sk11_comment+'</para>', styles['Normal'])],
        ['12', str(primaryData.sk12_tag_on), inventoryResponse(str(primaryData.sk12_tag_on), 12), str(primaryData.sk12_serial), str(primaryData.sk12_complete), str(primaryData.sk12_report), Paragraph('<para align=center>'+primaryData.sk12_comment+'</para>', styles['Normal'])],
        ['13', str(primaryData.sk13_tag_on), inventoryResponse(str(primaryData.sk13_tag_on), 13), str(primaryData.sk13_serial), str(primaryData.sk13_complete), str(primaryData.sk13_report), Paragraph('<para align=center>'+primaryData.sk13_comment+'</para>', styles['Normal'])],
        ['14', str(primaryData.sk14_tag_on), inventoryResponse(str(primaryData.sk14_tag_on), 14), str(primaryData.sk14_serial), str(primaryData.sk14_complete), str(primaryData.sk14_report), Paragraph('<para align=center>'+primaryData.sk14_comment+'</para>', styles['Normal'])],
        ['15', str(primaryData.sk15_tag_on), inventoryResponse(str(primaryData.sk15_tag_on), 15), str(primaryData.sk15_serial), str(primaryData.sk15_complete), str(primaryData.sk15_report), Paragraph('<para align=center>'+primaryData.sk15_comment+'</para>', styles['Normal'])],
        ['16', str(primaryData.sk16_tag_on), inventoryResponse(str(primaryData.sk16_tag_on), 16), str(primaryData.sk16_serial), str(primaryData.sk16_complete), str(primaryData.sk16_report), Paragraph('<para align=center>'+primaryData.sk16_comment+'</para>', styles['Normal'])],
        ['17', str(primaryData.sk17_tag_on), inventoryResponse(str(primaryData.sk17_tag_on), 17), str(primaryData.sk17_serial), str(primaryData.sk17_complete), str(primaryData.sk17_report), Paragraph('<para align=center>'+primaryData.sk17_comment+'</para>', styles['Normal'])],
        ['18', str(primaryData.sk18_tag_on), inventoryResponse(str(primaryData.sk18_tag_on), 18), str(primaryData.sk18_serial), str(primaryData.sk18_complete), str(primaryData.sk18_report), Paragraph('<para align=center>'+primaryData.sk18_comment+'</para>', styles['Normal'])],
        ['19', str(primaryData.sk19_tag_on), inventoryResponse(str(primaryData.sk19_tag_on), 19), str(primaryData.sk19_serial), str(primaryData.sk19_complete), str(primaryData.sk19_report), Paragraph('<para align=center>'+primaryData.sk19_comment+'</para>', styles['Normal'])],
        ['20', str(primaryData.sk20_tag_on), inventoryResponse(str(primaryData.sk20_tag_on), 20), str(primaryData.sk20_serial), str(primaryData.sk20_complete), str(primaryData.sk20_report), Paragraph('<para align=center>'+primaryData.sk20_comment+'</para>', styles['Normal'])],
        ['21', str(primaryData.sk21_tag_on), inventoryResponse(str(primaryData.sk21_tag_on), 21), str(primaryData.sk21_serial), str(primaryData.sk21_complete), str(primaryData.sk21_report), Paragraph('<para align=center>'+primaryData.sk21_comment+'</para>', styles['Normal'])],
        ['', '', '', '', '', ''],
        ['#2 Boilerhouse', '', '', '', '', ''],
        ['UT-23', str(primaryData.skut22_tag_on), inventoryResponse(str(primaryData.skut22_tag_on), 22), str(primaryData.skut22_serial), str(primaryData.skut22_complete), str(primaryData.skut22_report), Paragraph('<para align=center>'+primaryData.skut22_comment+'</para>', styles['Normal'])],
        ['UT-24', str(primaryData.skut23_tag_on), inventoryResponse(str(primaryData.skut23_tag_on), 23), str(primaryData.skut23_serial), str(primaryData.skut23_complete), str(primaryData.skut23_report), Paragraph('<para align=center>'+primaryData.skut23_comment+'</para>', styles['Normal'])],
        ['UT-25', str(primaryData.skut24_tag_on), inventoryResponse(str(primaryData.skut24_tag_on), 24), str(primaryData.skut24_serial), str(primaryData.skut24_complete), str(primaryData.skut24_report), Paragraph('<para align=center>'+primaryData.skut24_comment+'</para>', styles['Normal'])],
        ['UT-26', str(primaryData.skut25_tag_on), inventoryResponse(str(primaryData.skut25_tag_on), 25), str(primaryData.skut25_serial), str(primaryData.skut25_complete), str(primaryData.skut25_report), Paragraph('<para align=center>'+primaryData.skut25_comment+'</para>', styles['Normal'])],
        ['UT-27', str(primaryData.skut26_tag_on), inventoryResponse(str(primaryData.skut26_tag_on), 26), str(primaryData.skut26_serial), str(primaryData.skut26_complete), str(primaryData.skut26_report), Paragraph('<para align=center>'+primaryData.skut26_comment+'</para>', styles['Normal'])],
    ]
    tableColWidths = (50,80,80,80,80,80,80)

    style = [
        #Top header and info
        ('FONT', (0,0), (-1,0), 'Times-Bold', 22),
        ('FONT', (0,1), (-1,1), 'Times-Bold', 15),
        ('BOTTOMPADDING',(0,2), (-1,2), 5),
        ('SPAN', (0,0), (-1,0)),
        ('SPAN', (0,1), (-1,1)),
        ('SPAN', (0,2), (-1,2)),
        ('SPAN', (0,4), (-1,4)),
        ('ALIGN', (0,0), (-1,2), 'CENTER'),
        
        #table
        ('GRID', (0,6),(-1,27), 0.5,  colors.black),
        ('BOX', (0,6),(-1,6), 1.5,  colors.black),
        ('ALIGN', (0,4), (-1,6), 'CENTER'),
        ('VALIGN', (0,4), (-1,6), 'MIDDLE'),
        ('ALIGN', (0,6), (-1,27), 'CENTER'),
        
        ('GRID', (0,30),(-1,35), 0.5,  colors.black),
        ('ALIGN', (0,30),(-1,35), 'CENTER'),
    ]
    return tableData, tableColWidths, style

