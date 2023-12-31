from ..models import Forms, formM_model
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.core.exceptions import FieldError
from django.http import HttpResponseNotFound
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from ..models import spill_kit_inventory_model, facility_forms_model, issues_model
from ..utils import parseFormList, getCompanyFacilities, getNewFormLabel_w_formID, getFormID_w_oldFormLabel, date_change, time_change, date_time_change, road_choices, truck_choices, area_choices, emptyInputs, quarterParse, inventoryResponse
import json
import io
import datetime
import calendar
import ast

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')
    
class PageNumCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        #Constructor
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
    #----------------------------------------------------------------------
    def showPage(self):
        #On a page break, add information to the list
        self.pages.append(dict(self.__dict__))
        self._startPage()
    #----------------------------------------------------------------------
    def save(self):
        #Add the page number to each page (page x of y)
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
    #----------------------------------------------------------------------
    def draw_page_number(self, page_count):
        #Add the page number
        page = "Page %s of %s" % (self._pageNumber, page_count)
        self.setFont("Helvetica", 9)
        self.drawRightString(200*mm, 10*mm, page)
      
@lock
def form_PDF(request, facility, formGroup, formIdentity, formDate):
    facilityForms = facility_forms_model.objects.filter(facilityChoice__facility_name=facility)
    forms_and_labels = ast.literal_eval(facilityForms[0].formData)
    allForms = Forms.objects.all()
    ## Group Choices = (sinlge, coke_battery, facility_weekly)
    ## If formGroup ISNT single the formIdentity will be 'multi'

    if formGroup == 'single':
        formsBeingUsed = [formIdentity]
    elif formGroup == 'coke_battery':
        formsBeingUsed = ['1', '2', '3', '4', '5']
    elif formGroup == 'facility_weekly':
        formsBeingUsed = []
        for fForms in forms_and_labels:
            if fForms[0] == 23:
                continue
            formsBeingUsed.append(fForms[0])
            # if fList[0] == 26:
            #     formList.append('Spill Kits')
            # elif fList[0] == 27:
            #     formList.append('Quarterly Trucks')
    elif formGroup == 'monthly':
        formList = ['G2', 'Spill Kits']
    elif formGroup == 'tanks':
        formList = []
    elif formGroup == 'waste':
        formList = []
    print("The formID's being used are listed below:")
    print(formsBeingUsed)
    print("_________________________________") 
    elems = []
    for formID in formsBeingUsed:
        print("Now running process for form: " + str(formID))
        formID = int(formID)
        formInformation = allForms.get(id=formID)
        formModelName = formInformation.link + '_model'
        try:
            formModel = apps.get_model('EES_Forms', formModelName)
            formModel = formModel.objects.filter(facilityChoice__facility_name=facility)
            print("Pulling all submitted data for " + facility + " from "+ formModelName)
            print('')
            print(formModel)
            print('')
        except:
            print("Could not find a model with the name " + formModelName + " for formID " + formID)
            continue
        formDateParsed = datetime.datetime.strptime(formDate, "%Y-%m-%d").date()
        endDate = formDateParsed
        if formGroup not in ['single', 'coke_battery']:
            startDate = formDateParsed - datetime.timedelta(days=6)
        else:   
            startDate = formDateParsed
        print("Filtering submissions starting on " + str(startDate) + " and ending on " + str(endDate))
        formsAndData = {}
        ## ----- ADD NEW FORM DATE SELECTIONS BELOEW ----- ##
        for submittedForm in formModel:
            listOfPulledForms = [submittedForm]
            try:
                submittedFormDate = submittedForm.date
            except:
                submittedFormDate = submittedForm.week_start
            if int(formID) in (1,5,7,17,18,19,22):
                formSecondaryModelName = formInformation.link + '_readings_model'
                try:
                    formSecondaryModel = apps.get_model('EES_Forms', formSecondaryModelName)
                    try:
                        formSecondaryModel = formSecondaryModel.objects.get(form__facilityChoice__facility_name=facility, form__date=str(submittedFormDate))
                    except:
                        formSecondaryModel = formSecondaryModel.objects.get(form__facilityChoice__facility_name=facility, form__week_start=submittedFormDate)
                    listOfPulledForms.append(formSecondaryModel)
                except:
                    print("Could not find a secondary model with the name " + formSecondaryModelName + " for formID " + str(formID))
                    continue
            if startDate <= submittedFormDate <= endDate:
                formsAndData[str(submittedFormDate)] = [listOfPulledForms]
            if formGroup == 'single':
                break
        print("Found " + str(len(formsAndData)) + " form(s) within the specified time frame.")
            
            
            
            
          

        
        
        
        
        
        
        
        # .order_by('-date')
        # .order_by('-week_start')
        # allSubmittedDataForForm = 
        
        
        
        
        
        
        
        
        
    elems = []
    for item in formList:
        print(item)
        try:
            int(item)
            print("This is a number: " + str(item))
            itemID = int(item)
            ModelForms = Forms.objects.filter(form=item, facilityChoice__facility_name=facility)
            if ModelForms.exists():
                ModelForms = ModelForms[0]
                reFormName = item
                modelName = 'form' + item + '_model'
            else:
                for newParse in parseFormList:
                    if int(newParse[0]) == int(item):
                        item = newParse[1]
                        ModelForms = Forms.objects.filter(form=newParse[1], facilityChoice__facility_name=facility)
                        print("Now it has been changed to: "+ item)
                        break
        except:
            print("The '" + str(item) + "' form has been caught by the EXCEPTION")

            print("This is a Letter/String: " + str(item))
            itemID = item
            ModelForms = Forms.objects.filter(form=item, facilityChoice__facility_name=facility)
            if len(ModelForms) > 0:
                ModelForms = ModelForms[0]
                reFormName = item
                modelName = 'form' + item + '_model'

        goNext = False
        if item in ['N', "Q", "R"]:#23,27,26
            if item == "N":
                reFormName = 'N'
                modelName = 'formM_model'
            elif item == "Q":
                reFormName = 'Quarterly Trucks'
                modelName = 'quarterly_trucks_model'
            elif item == "R":
                reFormName = 'Spill Kits'
                modelName = 'spill_kits_model'
        elif len(item) > 1 and len(item) <= 3:
            reFormName = item[0] + '-' + item[1]
            modelName = 'form' + item + '_model'
        elif len(item) > 3:
            modelName = item.replace(' ', '_').lower() + '_model'
            reFormName = item.replace('_', ' ').title()
        else:
            print(item)
            reFormName = item
            modelName = 'form' + item + '_model'
            ModelForms = Forms.objects.filter(form=reFormName, facilityChoice__facility_name=facility)
            if len(ModelForms) > 0:
                ModelForms = ModelForms[0]
            else:
                print("no modelForm")
        
        ModelForms = Forms.objects.filter(form=reFormName, facilityChoice__facility_name=facility)[0]
        mainModel = apps.get_model('EES_Forms', modelName)
        #Pick the specific form date
        formsAndData = {}
        if reFormName[-1] == 'N':
            parseDateN = datetime.datetime.strptime(formDate[:-2], "%m-%Y")
            daysInMonth = calendar.monthrange(parseDateN.year, parseDateN.month)
            newDateN = str(parseDateN.year) + '-' + str(parseDateN.month) + '-' + '01'
            print(daysInMonth[1] + 1)
            print(newDateN)
            parseDateStart = datetime.datetime.strptime(newDateN, "%Y-%m-%d").date()
            parseDateStop = parseDateStart + datetime.timedelta(days=(daysInMonth[1] - 1))
            print(parseDateStop)
            print(parseDateStart)
            print('--------')
            print(parseDateN)
        else:
            parseDateN = ''
            parseDateStop = datetime.datetime.strptime(formDate, "%Y-%m-%d").date()
            parseDateStart = parseDateStop - datetime.timedelta(days=6)
        database_model = ''
        try:
            org = mainModel.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
            print(org)
            for x in org:
                if formName == 'Facility Weekly Packet':
                    if parseDateStart <= x.date <= parseDateStop:
                        formsAndData[str(x.date)] = [x]
                        continue
                    else:
                        database_model = ''
                        continue
                elif formName == 'Coke Battery Daily Packet':
                    if str(x.date) == str(formDate):
                        formsAndData[str(x.date)] = [x]
                        continue
                    else:
                        database_model = ''
                        continue
                elif str(formName) == str(23): #this is form 'N'
                    if parseDateStart <= x.date <= parseDateStop:
                        formsAndData[str(x.date)] = [x]
                        print(x)
                        print('what the fuck')
                        break
                    else:
                        database_model = ''
                        continue
                else:
                    if str(x.date) == str(formDate):
                        database_model = x
                        formsAndData[str(x.date)] = [database_model]
                        
                        break
                    elif org[len(org)-1] == x:
                        database_model = ''
                        goNext = True
                        print('goNext1')
            print("-------This is MARKER 1")
            print(formsAndData)
            if item in ('A1', 'A5', 'C', 'G1', 'G2', 'H', 'M'):
                print('made it here')
                readingsModel = apps.get_model('EES_Forms', 'form' + item + '_readings_model')
                org2 = readingsModel.objects.filter(form__facilityChoice__facility_name=facility).order_by('-form')
                print(org2)
                for x in org2:
                    if formName == 'Facility Weekly Packet':
                        print("Getting paired Readings Model...")
                        if parseDateStart <= x.form.date <= parseDateStop:
                            for pairs in list(formsAndData):
                                xDate = str(x.form.date)
                                if xDate == pairs:
                                    formsAndData[pairs].append(x)
                                    continue
                    elif formName[-1] == 'N':
                        if parseDateStart <= x.date <= parseDateStop:
                            formsAndData[str(x.date)] = [x]
                            break
                        else:
                            database_model2 = ''
                            continue
                    else:
                        if str(x.form.date) == str(formDate):
                            for pairs in list(formsAndData):
                                xDate = str(x.form.date)
                                if xDate == pairs:
                                    formsAndData[pairs].append(x)
                            break
                        else:
                            database_model2 = ''
        except FieldError as e:
            print('Check A - Form ' + item)
            org = mainModel.objects.filter(facilityChoice__facility_name=facility).order_by('-week_start')
            for r in org:
                if formName == 'Facility Weekly Packet':
                    if parseDateStart <= r.week_start <= parseDateStop:
                        print(r)
                        print('<-------HERE')
                        formsAndData[str(r.week_start)] = [r]
                elif formName[-1] == 'N':
                    if parseDateStart <= x.date <= parseDateStop:
                        formsAndData[str(x.date)] = [x]
                        break
                    else:
                        database_model = ''
                        continue
                else:
                    if str(r.week_start) == str(formDate):
                        database_model = r
                        formsAndData[str(r.week_start)] = [database_model]
                        print('Check B - Form Exist')
                        break
                    elif r == org[len(org)-1]:
                        database_model = ''
                        print('FORM DOES NOT EXIST')
                        goNext = True
                        print('goNext2')  
        
        data = database_model
        print('Form ' + item + ' includes these:' + str(list(formsAndData)))    
        if goNext:
            continue
        print('Processing Forms that were found for ' + item + '...')
        alphaStore = ''
        print(list(formsAndData))
        for alpha in list(formsAndData):
            print("CHECK 1")
            if len(formsAndData[alpha]) == 2:
                doubleDB = True
                print(item + ' is a double database...')
                data = formsAndData[alpha][0]
                readings = formsAndData[alpha][1]
            else:
                data = formsAndData[alpha][0]
                print(item + ' is a single database...')
            print(ModelForms)
            styles = getSampleStyleSheet()
            fileName = 'form' + formName + '_' + formDate + ".pdf"
            documentTitle = 'form' + formName + '_' + formDate
            title = ModelForms.header + ' ' + ModelForms.title + ' - Form (' + ModelForms.form + ')'
            subTitle = 'Facility Name: ' + facility
            #always the same on all A-forms
            marginSet = 0.4
            print('...Creating PDF for ' + item + '...')
            dataList = []
            print('STARTING...')
            #create a stream
            stream = io.BytesIO()
            if item == 'I':
                tableData = [
                    [title],
                    [subTitle],
                    ['', Paragraph('<para align=center><b>Week of:&#160;</b>' + date_change(data.week_start) + '&#160;&#160;to&#160;&#160;' + date_change(data.week_end) + '</para>', styles['Normal']), '', '', '', ''],
                    ['', '', '', '', '', ''],
                    ['', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                    [Paragraph('<para align=center><b>Sampling Time</b></para>', styles['Normal']), time_change(data.time_0), time_change(data.time_1), time_change(data.time_2), time_change(data.time_3), time_change(data.time_4)],
                    [Paragraph("<para align=center><b>Inspector's Signature</b></para>", styles['Normal']), data.obser_0, data.obser_1, data.obser_2, data.obser_3, data.obser_4],
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
            elif item == 'L':
                tableData = [
                    [title],
                    [subTitle],
                    [Paragraph('<para align=center><b>Week of:&#160;</b>' + date_change(data.week_start) + '&#160;&#160;to&#160;&#160;' + date_change(data.week_end) + '</para>', styles['Normal'])],
                    ['', '', '', '', ''],
                    [Paragraph('<para align=center><b>Observer</b></para>', styles['Normal']), Paragraph('<para align=center><b>Day/Time</b></para>', styles['Normal']), Paragraph('<para align=center><b>Location</b></para>', styles['Normal']), Paragraph('<para align=center><b>Visible Emissions</b></para>', styles['Normal']), Paragraph('<para align=center><b>Comments</b></para>', styles['Normal'])],
                    [data.obser_5, 'Saturday/' + time_change(data.time_5), 'Coal Bin Vents', data.vents_5, Paragraph('<para>' + emptyInputs(data.v_comments_5) + '</para>', styles['Normal'])],
                    ['', '', 'Mixer Building Bag House', data.mixer_5, Paragraph('<para>' + emptyInputs(data.m_comments_5) + '</para>', styles['Normal'])],
                    [data.obser_6, 'Sunday/' + time_change(data.time_6), 'Coal Bin Vents', data.vents_6, Paragraph('<para>' + emptyInputs(data.v_comments_6) + '</para>', styles['Normal'])],
                    ['', '', 'Mixer Building Bag House', data.mixer_6, Paragraph('<para>' + emptyInputs(data.m_comments_6) + '</para>', styles['Normal'])],
                    [data.obser_0, 'Monday/' + time_change(data.time_0), 'Coal Bin Vents', data.vents_0, Paragraph('<para>' + emptyInputs(data.v_comments_0) + '</para>', styles['Normal'])],
                    ['', '', 'Mixer Building Bag House', data.mixer_0, Paragraph('<para>' + emptyInputs(data.m_comments_0) + '</para>', styles['Normal'])],
                    [data.obser_1, 'Tuesday/' + time_change(data.time_1), 'Coal Bin Vents', data.vents_1, Paragraph('<para>' + emptyInputs(data.v_comments_1) + '</para>', styles['Normal'])],
                    ['', '', 'Mixer Building Bag House', data.mixer_1, Paragraph('<para>' + emptyInputs(data.m_comments_1) + '</para>', styles['Normal'])],
                    [data.obser_2, 'Wednesday/' + time_change(data.time_2), 'Coal Bin Vents', data.vents_2, Paragraph('<para>' + emptyInputs(data.v_comments_2) + '</para>', styles['Normal'])],
                    ['', '', 'Mixer Building Bag House', data.mixer_2, Paragraph('<para>' + emptyInputs(data.m_comments_2) + '</para>', styles['Normal'])],
                    [data.obser_3, 'Thursday/' + time_change(data.time_3), 'Coal Bin Vents', data.vents_3, Paragraph('<para>' + emptyInputs(data.v_comments_3) + '</para>', styles['Normal'])],
                    ['', '', 'Mixer Building Bag House', data.mixer_3, Paragraph('<para>' + emptyInputs(data.m_comments_3) + '</para>', styles['Normal'])],
                    [data.obser_4, 'Friday/' + time_change(data.time_4), 'Coal Bin Vents', data.vents_4, Paragraph('<para>' + emptyInputs(data.v_comments_4) + '</para>', styles['Normal'])],
                    ['', '', 'Mixer Building Bag House', data.mixer_4, Paragraph('<para>' + emptyInputs(data.m_comments_4) + '</para>', styles['Normal'])],
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
            elif item == 'M':
                date = Paragraph('<para align=center font=Times-Roman><b>Date:</b> ' + date_change(data.date) + '</para>', styles['Normal'])
                startStopPaved = Paragraph('<para align=center><b>Start:</b>&#160;' + time_change(data.pav_start) + '&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;<b>End:</b>&#160;' + time_change(data.pav_stop)+ '</para>', styles['Normal'])
                startStopUnPaved = Paragraph('<para align=center><b>Start:</b>&#160;' + time_change(data.unp_start) + '&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;<b>End:</b>&#160;' + time_change(data.unp_stop)+ '</para>', styles['Normal'])
                startStopPark = '&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;<b>Start:</b>&#160;' + time_change(data.par_start) + '&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;<b>End:</b>&#160;' + time_change(data.par_stop)
                observerCert = Paragraph('<para align=center><b>Observer:</b>&#160;' + data.observer + '&#160;&#160;&#160;&#160;<b>Certified Date:</b>&#160;' + date_change(data.cert_date) + '</para>', styles['Normal'])
                comments = Paragraph('<para align=left><b>Comments:</b>    ' + data.comments + '</para>', styles['Normal'])
                print(data.unpaved)
                tableData = [
                    [title],
                    [subTitle],
                    [date],
                    ['','','','','','','',''],
                    ['',Paragraph('<para align=left><b>Paved:</b> ' + road_choices(data.paved) + '</para>', styles['Normal']),'',startStopPaved,'','','',''],
                    ['','MIN/SEC','0','15','30','45','',''],
                    ['','0',readings.pav_1,readings.pav_2,readings.pav_3,readings.pav_4,'',''],
                    ['','1',readings.pav_5,readings.pav_6,readings.pav_7,readings.pav_8,'',''],
                    ['','2',readings.pav_9,readings.pav_10,readings.pav_11,readings.pav_12,'',''],
                    ['','3-minute Average Opacity (sum of the 12 readings above/12)','','','','',readings.pav_total,''],
                    ['','','','','','','',''],
                    ['',Paragraph('<para align=left><b>Area:</b> ' + road_choices(data.unpaved) + '</para>', styles['Normal']),'',startStopUnPaved,'','','',''],
                    ['','MIN/SEC','0','15','30','45','',''],
                    ['','0',readings.unp_1,readings.unp_2,readings.unp_3,readings.unp_4,'',''],
                    ['','1',readings.unp_5,readings.unp_6,readings.unp_7,readings.unp_8,'',''],
                    ['','2',readings.unp_9,readings.unp_10,readings.unp_11,readings.unp_12,'',''],
                    ['','3-minute Average Opacity (sum of the 12 readings above/12)','','','','',readings.unp_total,''],
                    ['','','','','','','',''],
                    ['',Paragraph('<para align=left><b>Parking Lot:</b> ' + road_choices(data.parking) + startStopPark + '</para>', styles['Normal']),'','','','','',''],
                    ['','MIN/SEC','0','15','30','45','',''],
                    ['','0',readings.par_1,readings.par_2,readings.par_3,readings.par_4,'',''],
                    ['','1',readings.par_5,readings.par_6,readings.par_7,readings.par_8,'',''],
                    ['','2',readings.par_9,readings.par_10,readings.par_11,readings.par_12,'',''],
                    ['','3-minute Average Opacity (sum of the 12 readings above/12)','','','','',readings.par_total,''],
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
            elif item == 'N': 
                print(formM_model.objects.all()[0].date.year)
                dataN = formM_model.objects.filter(facilityChoice__facility_name=facility, date__year=parseDateN.year, date__month=parseDateN.month)
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
            elif item == 'O':
                tableData = [
                    [title],
                    [subTitle],
                    ['', Paragraph('<para align=center><b>Date:&#160;</b>' + date_change(data.date) + '</para>', styles['Normal']), '', '', '', ''],
                    ['', '', '', '', '', ''],
                    ['', '', '', '', '', ''],
                    ['', '', Paragraph('<para><b>Flow observed at monitoring location?</b></para>', styles['Normal']), data.Q_1, '', ''],
                    ['', '', Paragraph('<para><b>Does the observed flow have an unnatural turbidity?</b></para>', styles['Normal']), data.Q_2, '', ''],
                    ['', '', Paragraph('<para><b>Does the observed flow have an unnatural color?</b></para>', styles['Normal']), data.Q_3, '', ''],
                    ['', '', Paragraph('<para><b>Does the observed flow have an oil film?</b></para>', styles['Normal']), data.Q_4, '', ''],
                    ['', '', Paragraph('<para><b>Does the observed flow have floating solids?</b></para>', styles['Normal']), data.Q_5, '', ''],
                    ['', '', Paragraph('<para><b>Does the observed flow have foams?</b></para>', styles['Normal']), data.Q_6, '', ''],
                    ['', '', Paragraph('<para><b>Does the observed flow have settleable solids?</b></para>', styles['Normal']), data.Q_7, '', ''],
                    ['', '', Paragraph('<para><b>Does the observed flow have suspended solids?</b></para>', styles['Normal']), data.Q_8, '', ''],
                    ['', '', Paragraph('<para><b>Does the observed flow have deposits?</b></para>', styles['Normal']), data.Q_9, '', ''],
                    ['', '', '', '', '', ''],
                    ['', Paragraph('<para><b>Comments (Describe any problemsor conditions found during inspections)</b></para>', styles['Normal']), '', data.comments, '', ''],
                    ['', Paragraph('<para><b>Actions Taken (Include date mitigated)</b></para>', styles['Normal']), '', data.actions_taken, '', ''],
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
            elif item == 'P':
                title = 'Outfall 008 Observation Form' + ' - Form (' + ModelForms.form + ')'
                tableData = [
                    [title],
                    [subTitle],
                    ['', Paragraph('<para align=center><b>Date:&#160;</b>' + date_change(data.date) + '</para>', styles['Normal']), '', '', '', ''],
                    ['', '', '', '', '', ''],
                    ['', '', '', '', '', ''],
                    ['', '', Paragraph('<para><b>Flow observed at monitoring location?</b></para>', styles['Normal']), data.Q_1, '', ''],
                    ['', '', Paragraph('<para><b>Does the observed flow have an unnatural turbidity?</b></para>', styles['Normal']), data.Q_2, '', ''],
                    ['', '', Paragraph('<para><b>Does the observed flow have an unnatural color?</b></para>', styles['Normal']), data.Q_3, '', ''],
                    ['', '', Paragraph('<para><b>Does the observed flow have an oil film?</b></para>', styles['Normal']), data.Q_4, '', ''],
                    ['', '', Paragraph('<para><b>Does the observed flow have floating solids?</b></para>', styles['Normal']), data.Q_5, '', ''],
                    ['', '', Paragraph('<para><b>Does the observed flow have foams?</b></para>', styles['Normal']), data.Q_6, '', ''],
                    ['', '', Paragraph('<para><b>Does the observed flow have settleable solids?</b></para>', styles['Normal']), data.Q_7, '', ''],
                    ['', '', Paragraph('<para><b>Does the observed flow have suspended solids?</b></para>', styles['Normal']), data.Q_8, '', ''],
                    ['', '', Paragraph('<para><b>Does the observed flow have deposits?</b></para>', styles['Normal']), data.Q_9, '', ''],
                    ['', '', '', '', '', ''],
                    ['', Paragraph('<para><b>Comments (Describe any problemsor conditions found during inspections)</b></para>', styles['Normal']), '', data.comments, '', ''],
                    ['', Paragraph('<para><b>Actions Taken (Include date mitigated)</b></para>', styles['Normal']), '', data.actions_taken, '', ''],
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
            elif item.replace(' ','_').lower() == 'spill_kits' or item == "R":
                print('made it here')
                title = ModelForms.header + ' - ' + ModelForms.title
                tableData = [
                    [title],
                    [subTitle],
                    [Paragraph('<para align=center><b>Month:&#160;</b>' + data.month + '</para>', styles['Normal']), '', '', '', ''],
                    ['', '', '', '', '', ''],
                    [Paragraph('<para align=center><b>Inspector Names:&#160;</b>' + data.observer + '&#160;&#160;&#160;&#160;&#160;<b>Date:&#160;</b>' + date_change(data.date) +'</para>', styles['Normal']), '', '', '', ''],
                    ['', '', '', '', '', ''],
                    [Paragraph('<para align=center><b>Spill Kit #</b></para>', styles['Normal']), Paragraph('<para align=center><b>Tag On?</b></para>', styles['Normal']), Paragraph('<para align=center><b>Inventory</b></para>', styles['Normal']), Paragraph('<para align=center><b>Tag Serial #</b></para>', styles['Normal']), Paragraph('<para align=center><b>Complete Kit?</b></para>', styles['Normal']), Paragraph('<para align=center><b>Incident Report</b></para>', styles['Normal']), Paragraph('<para align=center><b>Comments</b></para>', styles['Normal'])],
                    ['1', str(data.sk1_tag_on), inventoryResponse(str(data.sk1_tag_on), 1), str(data.sk1_serial), str(data.sk1_complete), str(data.sk1_report), data.sk1_comment],
                    ['2', str(data.sk2_tag_on), inventoryResponse(str(data.sk2_tag_on), 2), str(data.sk2_serial), str(data.sk2_complete), str(data.sk2_report), data.sk2_comment],
                    ['3', str(data.sk3_tag_on), inventoryResponse(str(data.sk3_tag_on), 3), str(data.sk3_serial), str(data.sk3_complete), str(data.sk3_report), data.sk3_comment],
                    ['4', str(data.sk4_tag_on), inventoryResponse(str(data.sk4_tag_on), 4), str(data.sk4_serial), str(data.sk4_complete), str(data.sk4_report), data.sk4_comment],
                    ['5', str(data.sk5_tag_on), inventoryResponse(str(data.sk5_tag_on), 5), str(data.sk5_serial), str(data.sk5_complete), str(data.sk5_report), data.sk5_comment],
                    ['6', str(data.sk6_tag_on), inventoryResponse(str(data.sk6_tag_on), 6), str(data.sk6_serial), str(data.sk6_complete), str(data.sk6_report), data.sk6_comment],
                    ['7', str(data.sk7_tag_on), inventoryResponse(str(data.sk7_tag_on), 7), str(data.sk7_serial), str(data.sk7_complete), str(data.sk7_report), data.sk7_comment],
                    ['8', str(data.sk8_tag_on), inventoryResponse(str(data.sk8_tag_on), 8), str(data.sk8_serial), str(data.sk8_complete), str(data.sk8_report), data.sk8_comment],
                    ['9', str(data.sk9_tag_on), inventoryResponse(str(data.sk9_tag_on), 9), str(data.sk9_serial), str(data.sk9_complete), str(data.sk9_report), data.sk9_comment],
                    ['10', str(data.sk10_tag_on), inventoryResponse(str(data.sk10_tag_on), 10), str(data.sk10_serial), str(data.sk10_complete), str(data.sk10_report), data.sk10_comment],
                    ['11', str(data.sk11_tag_on), inventoryResponse(str(data.sk11_tag_on), 11), str(data.sk11_serial), str(data.sk11_complete), str(data.sk11_report), data.sk11_comment],
                    ['12', str(data.sk12_tag_on), inventoryResponse(str(data.sk12_tag_on), 12), str(data.sk12_serial), str(data.sk12_complete), str(data.sk12_report), data.sk12_comment],
                    ['13', str(data.sk13_tag_on), inventoryResponse(str(data.sk13_tag_on), 13), str(data.sk13_serial), str(data.sk13_complete), str(data.sk13_report), data.sk13_comment],
                    ['14', str(data.sk14_tag_on), inventoryResponse(str(data.sk14_tag_on), 14), str(data.sk14_serial), str(data.sk14_complete), str(data.sk14_report), data.sk14_comment],
                    ['15', str(data.sk15_tag_on), inventoryResponse(str(data.sk15_tag_on), 15), str(data.sk15_serial), str(data.sk15_complete), str(data.sk15_report), data.sk15_comment],
                    ['16', str(data.sk16_tag_on), inventoryResponse(str(data.sk16_tag_on), 16), str(data.sk16_serial), str(data.sk16_complete), str(data.sk16_report), data.sk16_comment],
                    ['17', str(data.sk17_tag_on), inventoryResponse(str(data.sk17_tag_on), 17), str(data.sk17_serial), str(data.sk17_complete), str(data.sk17_report), data.sk17_comment],
                    ['18', str(data.sk18_tag_on), inventoryResponse(str(data.sk18_tag_on), 18), str(data.sk18_serial), str(data.sk18_complete), str(data.sk18_report), data.sk18_comment],
                    ['19', str(data.sk19_tag_on), inventoryResponse(str(data.sk19_tag_on), 19), str(data.sk19_serial), str(data.sk19_complete), str(data.sk19_report), data.sk19_comment],
                    ['20', str(data.sk20_tag_on), inventoryResponse(str(data.sk20_tag_on), 20), str(data.sk20_serial), str(data.sk20_complete), str(data.sk20_report), data.sk20_comment],
                    ['21', str(data.sk21_tag_on), inventoryResponse(str(data.sk21_tag_on), 21), str(data.sk21_serial), str(data.sk21_complete), str(data.sk21_report), data.sk21_comment],
                    ['', '', '', '', '', ''],
                    ['#2 Boilerhouse', '', '', '', '', ''],
                    ['UT-23', str(data.skut22_tag_on), inventoryResponse(str(data.skut22_tag_on), 22), str(data.skut22_serial), str(data.skut22_complete), str(data.skut22_report), data.skut22_comment],
                    ['UT-24', str(data.skut23_tag_on), inventoryResponse(str(data.skut23_tag_on), 23), str(data.skut23_serial), str(data.skut23_complete), str(data.skut23_report), data.skut23_comment],
                    ['UT-25', str(data.skut24_tag_on), inventoryResponse(str(data.skut24_tag_on), 24), str(data.skut24_serial), str(data.skut24_complete), str(data.skut24_report), data.skut24_comment],
                    ['UT-26', str(data.skut25_tag_on), inventoryResponse(str(data.skut25_tag_on), 25), str(data.skut25_serial), str(data.skut25_complete), str(data.skut25_report), data.skut25_comment],
                    ['UT-27', str(data.skut26_tag_on), inventoryResponse(str(data.skut26_tag_on), 26), str(data.skut26_serial), str(data.skut26_complete), str(data.skut26_report), data.skut26_comment],
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
                print(style)
            elif item.replace(' ','_').lower() == 'quarterly_trucks' or item == "Q":
                title = Paragraph('<para fontSize=20 align=center font=Times-Bold leading=25><b>' + ModelForms.header + '<br/>' + ModelForms.title + ' - Form (' + ModelForms.form + ')</b></para>', styles['Normal'])
                tableData = [
                    [title],
                    [subTitle],
                    ['', '', Paragraph('<para>' + str(data.date.year) + '&#160;&#160;-&#160;&#160;' + quarterParse(int(data.quarter)) + '</para>', styles['Normal']), '', '', ''],
                    ['Truck 5', '', '', '', '', ''],
                    #truck 5 start (0,4)
                    [Paragraph('<para><b>Observer:&#160;</b>' + data.observer_5_1 + '</para>', styles['Normal']), Paragraph('<para><b>Date:&#160;</b>' + str(data.date_5_1) + '</para>', styles['Normal']), Paragraph('<para><b>Time:&#160;</b>' + time_change(data.time_5_1) + '</para>', styles['Normal']), ''],
                    [Paragraph('<para><b>1) Condition of Rear Gate Satisfactory:&#160;</b>' + data.rear_gate_5_1 + '</para>', styles['Normal']), ''],
                    [Paragraph('<para><b>2) Condition of Box Interior Satisfactory:&#160;</b>' + data.box_interior_5_1 + '</para>', styles['Normal']), ''],
                    [Paragraph('<para><b>3) Condition of Box Exterior Satisfactory:&#160;</b>' + data.box_exterior_5_1 + '</para>', styles['Normal']), ''],
                    [Paragraph('<para><b>4) Exhaust Position Satisfactory:&#160;</b>' + data.exhaust_5_1 + '</para>', styles['Normal']), ''],
                    [Paragraph('<para><b>Comments:&#160;</b>' + data.comments_5_1 + '</para>', styles['Normal']), '', '', '', '', ''],
                    ['', '', '', '', '', ''],
                    ['Truck 6', '', '', '', '', ''],
                    #truck 6 start (0,12)
                    [Paragraph('<para><b>Observer:&#160;</b>' + data.observer_6_2 + '</para>', styles['Normal']), Paragraph('<para><b>Date:&#160;</b>' + str(data.date_6_2) + '</para>', styles['Normal']), Paragraph('<para><b>Time:&#160;</b>' + time_change(data.time_6_2) + '</para>', styles['Normal']), '', '', ''],
                    [Paragraph('<para><b>1) Condition of Rear Gate Satisfactory:&#160;</b>' + data.rear_gate_6_2 + '</para>', styles['Normal']), ''],
                    [Paragraph('<para><b>2) Condition of Box Interior Satisfactory:&#160;</b>' + data.box_interior_6_2 + '</para>', styles['Normal']), ''],
                    [Paragraph('<para><b>3) Condition of Box Exterior Satisfactory:&#160;</b>' + data.box_exterior_6_2 + '</para>', styles['Normal']), ''],
                    [Paragraph('<para><b>4) Exhaust Position Satisfactory:&#160;</b>' + data.exhaust_6_2 + '</para>', styles['Normal']), ''],
                    [Paragraph('<para><b>Comments:&#160;</b>' + data.comments_6_2 + '</para>', styles['Normal']), ''],
                    ['', '', '', '', '', ''],
                    ['Truck 7', '', '', '', '', ''],
                    #truck 7 start (0,20)
                    [Paragraph('<para><b>Observer:&#160;</b>' + data.observer_7_3 + '</para>', styles['Normal']), Paragraph('<para><b>Date:&#160;</b>' + str(data.date_7_3) + '</para>', styles['Normal']), Paragraph('<para><b>Time:&#160;</b>' + time_change(data.time_7_3) + '</para>', styles['Normal']), '', '', ''],
                    [Paragraph('<para><b>1) Condition of Rear Gate Satisfactory:&#160;</b>' + data.rear_gate_7_3 + '</para>', styles['Normal']), ''],
                    [Paragraph('<para><b>2) Condition of Box Interior Satisfactory:&#160;</b>' + data.box_interior_7_3 + '</para>', styles['Normal']), ''],
                    [Paragraph('<para><b>3) Condition of Box Exterior Satisfactory:&#160;</b>' + data.box_exterior_7_3 + '</para>', styles['Normal']), ''],
                    [Paragraph('<para><b>4) Exhaust Position Satisfactory:&#160;</b>' + data.exhaust_7_3 + '</para>', styles['Normal']), ''],
                    [Paragraph('<para><b>Comments:&#160;</b>' + data.comments_7_3 + '</para>', styles['Normal']), ''],
                    ['', '', '', '', '', ''],
                    ['Truck 9', '', '', '', '', ''],
                    #truck 9 start (0,28)
                    [Paragraph('<para><b>Observer:&#160;</b>' + data.observer_9_4 + '</para>', styles['Normal']), Paragraph('<para><b>Date:&#160;</b>' + str(data.date_9_4) + '</para>', styles['Normal']), Paragraph('<para><b>Time:&#160;</b>' + time_change(data.time_9_4) + '</para>', styles['Normal']), '', '', ''],
                    [Paragraph('<para><b>1) Condition of Rear Gate Satisfactory:&#160;</b>' + data.rear_gate_9_4 + '</para>', styles['Normal']), '', '', '', '', ''],
                    [Paragraph('<para><b>2) Condition of Box Interior Satisfactory:&#160;</b>' + data.box_interior_9_4 + '</para>', styles['Normal']), '', '', '', '', ''],
                    [Paragraph('<para><b>3) Condition of Box Exterior Satisfactory:&#160;</b>' + data.box_exterior_9_4 + '</para>', styles['Normal']), '', '', '', '', ''],
                    [Paragraph('<para><b>4) Exhaust Position Satisfactory:&#160;</b>' + data.exhaust_9_4 + '</para>', styles['Normal']), '', '', '', '', ''],
                    [Paragraph('<para><b>Comments:&#160;</b>' + data.comments_9_4 + '</para>', styles['Normal']), '', '', '', '', ''],
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
            heightGroup = ('A5', 'G1', 'G2', 'H')
            print("________________")
            print(itemID)
            # try:
            #     int(item)
            issueFormID = getNewFormLabel_w_formID(facility, itemID) #getFormID_w_oldFormLabel(itemID)
            try:
                issueForm = issues_model.objects.filter(date=data.date, form=issueFormID)
            except:
                issueForm = issues_model.objects.filter(date=data.week_start, form=issueFormID)
                
            if issueForm.exists():
                issueSpace = len(tableData)
                issueForm = issueForm[0]
                issueTable = [
                    [''],
                    [Paragraph('<para align=center><b>Corrective-Action</b></para>', styles['Normal'])],
                    [Paragraph('<para><b>Issues:</b>&#160;&#160;' + issueForm.issues + '</para>', styles['Normal'])],
                    [Paragraph('<para><b>EES Personnel Notified:</b>&#160;&#160;' + issueForm.notified + '&#160;&#160;&#160;&#160;&#160;<b>Date/Time:</b>&#160;&#160;' + date_change(issueForm.date) + '&#160;/&#160;' + time_change(issueForm.time) + '</para>', styles['Normal'])],
                    [Paragraph('<para><b>Corrective Action Taken:</b>&#160;&#160;' + issueForm.cor_action + '</para>', styles['Normal'])],
                ]
                for issue_line in issueTable:
                    tableData.append(issue_line)
                issueStyle = [
                    ('SPAN', (0,1 + issueSpace), (-1,1 + issueSpace)),
                    ('SPAN', (0,2 + issueSpace), (-1,2 + issueSpace)),
                    ('SPAN', (0,3 + issueSpace), (-1,3 + issueSpace)),
                    ('SPAN', (0,4 + issueSpace), (-1,4 + issueSpace)),
                    ('BOX', (0,1 + issueSpace), (-1,4 + issueSpace), 1, colors.black),
                    ('BOX', (0,1 + issueSpace), (-1,1 + issueSpace), 1, colors.black),
                ]
                for issue_style in issueStyle:
                    style.append(issue_style)
                if item in heightGroup:
                    addedRowHeights = (20,15,15,15,15)    
                    tableRowHeights = tableRowHeights + addedRowHeights
            print("________________")
            
            if item in heightGroup:
                dataList.append([tableData, tableColWidths, style, tableRowHeights],)
            else:
                dataList.append([tableData, tableColWidths, style, None],)
                
            pdf = SimpleDocTemplate(stream, pagesize=letter, topMargin=marginSet*inch, bottomMargin=0.3*inch, title=documentTitle)

            if item in heightGroup:
                table = Table(dataList[0][0], colWidths=dataList[0][1], rowHeights=dataList[0][3])
            else:
                table = Table(dataList[0][0], colWidths=dataList[0][1])
            style = TableStyle(dataList[0][2])
            
            table.setStyle(style)
            
            elems.append(table)
            elems.append(PageBreak())
            print('FINISHED...')
            print('PDFs for ' + item + ' has been created. Moving to next form')
    
    print('Finished creating PDFs...')        
    try:
        
        pdf.build(elems, canvasmaker=PageNumCanvas)
            # get buffer
        stream.seek(0)
        pdf_buffer = stream.getbuffer()
        print(pdf_buffer)
        response = HttpResponse(bytes(pdf_buffer), content_type='application/pdf')
        print('Starting to Compile...')
    except UnboundLocalError as e:
        return HttpResponseNotFound("No Forms Found")
   
    return response