from ..models import Forms
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.http import HttpResponseNotFound
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from ..models import facility_forms_model, issues_model, user_profile_model
from ..utils import parseFormList, getCompanyFacilities, getNewFormLabel_w_formID, getFormID_w_oldFormLabel, date_change, time_change, date_time_change, road_choices, truck_choices, area_choices, emptyInputs, quarterParse, inventoryResponse
import json
import io
import datetime
import calendar
import ast
from .form_pdf_templates import *

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
    userProfile = user_profile_model.objects.get(user=request.user)
    facilityForms = facility_forms_model.objects.filter(facilityChoice__facility_name=facility)
    forms_and_labels = ast.literal_eval(facilityForms[0].formData)
    print(forms_and_labels)
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
            # if fForms[0] == 23:
            #     continue
            formsBeingUsed.append(fForms[0])
    elif formGroup == 'monthly':
        formsBeingUsed = ['G2', 'Spill Kits']
    elif formGroup == 'tanks':
        formsBeingUsed = []
    elif formGroup == 'waste':
        formsBeingUsed = []
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
            if formID == 23:
                formModel = apps.get_model('EES_Forms', 'formM_model')
                formModel = formModel.objects.filter(facilityChoice__facility_name=facility)
                print('Using form 22 data to create form 23.')
                print('')  
                print("Pulling all submitted data for " + facility + " from "+ 'formM_model')
            else:
                print("Could not find a model with the name " + formModelName + " for formID " + str(formID))
                continue
        try:
            formDateParsed = datetime.datetime.strptime(formDate, "%Y-%m-%d").date()
        except:
            formDateParsed = datetime.datetime.strptime(formDate, "%Y-%m").date()
        if formGroup == 'single' and formInformation.frequency == 'Monthly':
            monthDays = calendar.monthrange(formDateParsed.year, formDateParsed.month)
            startDateString = str(formDateParsed.year) + "-" + str(formDateParsed.month) + "-01"
            endDateString = str(formDateParsed.year) + "-" + str(formDateParsed.month) + "-" + str(monthDays[1])
            startDate = datetime.datetime.strptime(startDateString, "%Y-%m-%d").date()
            endDate = datetime.datetime.strptime(endDateString, "%Y-%m-%d").date()
        else:
            formDateParsed = datetime.datetime.strptime(formDate, "%Y-%m-%d").date()
            endDate = formDateParsed
            if formGroup not in ['single', 'coke_battery']:
                startingDayNumb = int(userProfile.company.settings.weekly_start_day)
                amountOfDaysToStartingDay = (startingDayNumb-formDateParsed.weekday())
                if formDateParsed.weekday() < startingDayNumb:
                    amountOfDaysToStartingDay = amountOfDaysToStartingDay-7
                startDate = formDateParsed + datetime.timedelta(days=amountOfDaysToStartingDay)
                endDate = startDate + datetime.timedelta(days=6)
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
                formsAndData[str(submittedFormDate)] = listOfPulledForms
                if formGroup == 'single':
                    break
        print("Found " + str(len(formsAndData)) + " form(s) within the specified time frame.")
        print('')
        if len(formsAndData) == 0:
            print("...Moving to next form")
            print("_________________________________")
            continue
        for listForm in formsAndData:
            formData = formsAndData[listForm][0]
            formSecondaryData = False
            if len(formsAndData[listForm]) == 2:
                doubleDB = True
                print(str(formID) + ' is a double database...')
                formSecondaryData = formsAndData[listForm][1]
            for label in forms_and_labels:
                if formID == label[0]:
                    formLabel = label[1]
            
            styles = getSampleStyleSheet()
            if formGroup == 'single':
                fileName = 'form' + formLabel + '_' + formDate + ".pdf"
                documentTitle = 'form' + formLabel + '_' + formDate
            elif formGroup == 'coke_battery':
                fileName = "form_1_packet.pdf"
                documentTitle = "form_1_packet"
            elif formGroup == 'facility_weekly':
                fileName = "facility_weekly_packet.pdf"
                documentTitle = "facility_weekly_packet"
            title = formInformation.header + ' ' + formInformation.title + ' - Form (' + formInformation.form + ')'
            subTitle = 'Facility Name: ' + facility
            #always the same on all A-forms
            marginSet = 0.4
            print('...Creating PDF for formID ' + str(formID) + '...')
            dataList = []
            print('STARTING...')
            #create a stream
            stream = io.BytesIO()
            if formID == 1:
                tableData, tableColWidths, style = pdf_template_A1(formData, formSecondaryData, title, subTitle)
            if formID == 2:
                tableData, tableColWidths, style = pdf_template_A2(formData, title, subTitle)
            if formID == 3:
                tableData, tableColWidths, style = pdf_template_A3(formData, title, subTitle)
            if formID == 4:
                tableData, tableColWidths, style = pdf_template_A4(formData, title, subTitle)
            if formID == 5:
                tableData, tableColWidths, tableRowHeights, style = pdf_template_A5(formData, formSecondaryData, formInformation)
            if formID == 6:
                tableData, tableColWidths, style = pdf_template_6(formData, title, subTitle, formInformation)
            if formID == 7:
                tableData, tableColWidths, style = pdf_template_7(formData, formSecondaryData, title, subTitle)
            if formID == 8:
                tableData, tableColWidths, style = pdf_template_8(formData, title, subTitle)
            if formID == 9:
                tableData, tableColWidths, style = pdf_template_9(formData, title, subTitle)
            if formID == 17:
                tableData, tableColWidths, tableRowHeights, style = pdf_template_17(formData, formSecondaryData, title, subTitle, formInformation)
            if formID == 18:
                tableData, tableColWidths, tableRowHeights, style = pdf_template_18(formData, formSecondaryData, title, subTitle, formInformation)
            if formID == 19:
                tableData, tableColWidths, tableRowHeights, style = pdf_template_19(formData, formSecondaryData, title, subTitle, formInformation)
            if formID == 20:
                tableData, tableColWidths, style = pdf_template_20(formData, title, subTitle)
            if formID == 21:
                tableData, tableColWidths, style = pdf_template_21(formData, title, subTitle)
            if formID == 22:
                tableData, tableColWidths, style = pdf_template_22(formData, formSecondaryData, title, subTitle)
            if formID == 23:
                tableData, tableColWidths, style = pdf_template_23(formDate, facility)
            if formID == 24:
                tableData, tableColWidths, style = pdf_template_24(formData, title, subTitle)
            if formID == 25:
                tableData, tableColWidths, style = pdf_template_25(formData, title, subTitle, formInformation)
            if formID == 26:
                tableData, tableColWidths, style = pdf_template_26(formData, title, subTitle, formInformation)
            if formID == 27:
                tableData, tableColWidths, style = pdf_template_27(formData, title, subTitle, formInformation)
                
            heightGroup = (5,17,18,19)
            
            #issueFormID = getNewFormLabel_w_formID(facility, itemID) #getFormID_w_oldFormLabel(itemID)
            try:
                issueForm = issues_model.objects.filter(date=formData.date, form=formID)
            except:
                issueForm = issues_model.objects.filter(date=formData.week_start, form=formID)
                
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
                if formID in heightGroup:
                    addedRowHeights = (20,15,15,15,15)    
                    tableRowHeights = tableRowHeights + addedRowHeights
            
            if formID in heightGroup:
                dataList.append([tableData, tableColWidths, style, tableRowHeights],)
            else:
                dataList.append([tableData, tableColWidths, style, None],)
                
            pdf = SimpleDocTemplate(stream, pagesize=letter, topMargin=marginSet*inch, bottomMargin=0.3*inch, title=documentTitle)

            if formID in heightGroup:
                table = Table(dataList[0][0], colWidths=dataList[0][1], rowHeights=dataList[0][3])
            else:
                table = Table(dataList[0][0], colWidths=dataList[0][1])
            style = TableStyle(dataList[0][2])
            
            table.setStyle(style)
            
            elems.append(table)
            elems.append(PageBreak())
            print('FINISHED...')
            print('PDFs for ' + str(formID) + ' has been created. Moving to next form')
            print("_________________________________")
    print('')
    print("End of process")
    print("_________________________________")
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

    # if formDate[0:6] == 'single':
    #     formTag = formDate[0:6]
    #     formDate = formDate[7:]
    # elif formDate[0:5] == 'group':
    #     formTag = formDate[0:5]
    #     formDate = formDate[6:]
    # else:
    #     formTag = ''
    
    # if formTag == 'single' or formTag == '':
    #     formList = [formName]
    #     print(formName)
    #     for fList in formList1:
    #         for sList in formList:
    #             print("hello")
    # elif formName == 'Coke Battery Daily Packet':
    #     formList = ['1', '2', '3', '4', '5']
    # elif formName == 'Facility Weekly Packet':
    #     formList = []
    #     for fList in formList1:
    #         if fList[0] == 23:
    #             continue
    #         else:
    #             for pFormList in parseFormList:
    #                 if fList[0] == pFormList[0]:
    #                     if fList[0] == 26:
    #                         formList.append('Spill Kits')
    #                     elif fList[0] == 27:
    #                         formList.append('Quarterly Trucks')
    #                     else:
    #                         formList.append(fList[1])
    # elif formName == 'monthly':
    #     formList = ['G2', 'Spill Kits']
    # elif formName == 'tanks':
    #     formList = []
    # elif formName == 'waste':
    #     formList = []
    # print(formList)
    # elems = []
    # for item in formList:
    #     print(item)
    #     try:
    #         int(item)
    #         print("This is a number: " + str(item))
    #         itemID = int(item)
    #         ModelForms = Forms.objects.filter(form=item, facilityChoice__facility_name=facility)
    #         if len(ModelForms) > 0:
    #             ModelForms = ModelForms[0]
    #             reFormName = item
    #             modelName = 'form' + item + '_model'
    #         else:
    #             for newParse in parseFormList:
    #                 if int(newParse[0]) == int(item):
    #                     item = newParse[1]
    #                     ModelForms = Forms.objects.filter(form=newParse[1], facilityChoice__facility_name=facility)
    #                     print("Now it has been changed to: "+ item)
    #                     break
    #     except:
    #         print("The '" + str(item) + "' form has been caught by the EXCEPTION")

    #         print("This is a Letter/String: " + str(item))
    #         itemID = item
    #         ModelForms = Forms.objects.filter(form=item, facilityChoice__facility_name=facility)
    #         if len(ModelForms) > 0:
    #             ModelForms = ModelForms[0]
    #             reFormName = item
    #             modelName = 'form' + item + '_model'
    #     if item[0] == 'F':
    #         print('Skipped Form and Continued')
    #         continue
    #     goNext = False
    #     if item in ['N', "Q", "R"]:
    #         if item == "N":
    #             reFormName = 'N'
    #             modelName = 'formM_model'
    #         elif item == "Q":
    #             reFormName = 'Quarterly Trucks'
    #             modelName = 'quarterly_trucks_model'
    #         elif item == "R":
    #             reFormName = 'Spill Kits'
    #             modelName = 'spill_kits_model'
    #     elif len(item) > 1 and len(item) <= 3:
    #         reFormName = item[0] + '-' + item[1]
    #         modelName = 'form' + item + '_model'
    #     elif len(item) > 3:
    #         modelName = item.replace(' ', '_').lower() + '_model'
    #         reFormName = item.replace('_', ' ').title()
    #     else:
    #         print(item)
    #         reFormName = item
    #         modelName = 'form' + item + '_model'
    #         ModelForms = Forms.objects.filter(form=reFormName, facilityChoice__facility_name=facility)
    #         if len(ModelForms) > 0:
    #             ModelForms = ModelForms[0]
    #         else:
    #             print("no modelForm")
        
    #     ModelForms = Forms.objects.filter(form=reFormName, facilityChoice__facility_name=facility)[0]
    #     mainModel = apps.get_model('EES_Forms', modelName)
    #     #Pick the specific form date
    #     formsAndData = {}
    #     if reFormName[-1] == 'N':
    #         parseDateN = datetime.datetime.strptime(formDate[:-2], "%m-%Y")
    #         daysInMonth = calendar.monthrange(parseDateN.year, parseDateN.month)
    #         newDateN = str(parseDateN.year) + '-' + str(parseDateN.month) + '-' + '01'
    #         print(daysInMonth[1] + 1)
    #         print(newDateN)
    #         parseDateStart = datetime.datetime.strptime(newDateN, "%Y-%m-%d").date()
    #         parseDateStop = parseDateStart + datetime.timedelta(days=(daysInMonth[1] - 1))
    #         print(parseDateStop)
    #         print(parseDateStart)
    #         print('--------')
    #         print(parseDateN)
    #     else:
    #         parseDateN = ''
    #         parseDateStop = datetime.datetime.strptime(formDate, "%Y-%m-%d").date()
    #         parseDateStart = parseDateStop - datetime.timedelta(days=6)
    #     database_model = ''
    #     try:
    #         org = mainModel.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
    #         print(org)
    #         for x in org:
    #             if formName == 'Facility Weekly Packet':
    #                 if parseDateStart <= x.date <= parseDateStop:
    #                     formsAndData[str(x.date)] = [x]
    #                     continue
    #                 else:
    #                     database_model = ''
    #                     continue
    #             elif formName == 'Coke Battery Daily Packet':
    #                 if str(x.date) == str(formDate):
    #                     formsAndData[str(x.date)] = [x]
    #                     continue
    #                 else:
    #                     database_model = ''
    #                     continue
    #             elif str(formName) == str(23): #this is form 'N'
    #                 if parseDateStart <= x.date <= parseDateStop:
    #                     formsAndData[str(x.date)] = [x]
    #                     print(x)
    #                     print('what the fuck')
    #                     break
    #                 else:
    #                     database_model = ''
    #                     continue
    #             else:
    #                 if str(x.date) == str(formDate):
    #                     database_model = x
    #                     formsAndData[str(x.date)] = [database_model]
                        
    #                     break
    #                 elif org[len(org)-1] == x:
    #                     database_model = ''
    #                     goNext = True
    #                     print('goNext1')
    #         print("-------This is MARKER 1")
    #         print(formsAndData)
    #         if item in ('A1', 'A5', 'C', 'G1', 'G2', 'H', 'M'):
    #             print('made it here')
    #             readingsModel = apps.get_model('EES_Forms', 'form' + item + '_readings_model')
    #             org2 = readingsModel.objects.filter(form__facilityChoice__facility_name=facility).order_by('-form')
    #             print(org2)
    #             for x in org2:
    #                 if formName == 'Facility Weekly Packet':
    #                     print("Getting paired Readings Model...")
    #                     if parseDateStart <= x.form.date <= parseDateStop:
    #                         for pairs in list(formsAndData):
    #                             xDate = str(x.form.date)
    #                             if xDate == pairs:
    #                                 formsAndData[pairs].append(x)
    #                                 continue
    #                 elif formName[-1] == 'N':
    #                     if parseDateStart <= x.date <= parseDateStop:
    #                         formsAndData[str(x.date)] = [x]
    #                         break
    #                     else:
    #                         database_model2 = ''
    #                         continue
    #                 else:
    #                     if str(x.form.date) == str(formDate):
    #                         for pairs in list(formsAndData):
    #                             xDate = str(x.form.date)
    #                             if xDate == pairs:
    #                                 formsAndData[pairs].append(x)
    #                         break
    #                     else:
    #                         database_model2 = ''
    #     except FieldError as e:
    #         print('Check A - Form ' + item)
    #         org = mainModel.objects.filter(facilityChoice__facility_name=facility).order_by('-week_start')
    #         for r in org:
    #             if formName == 'Facility Weekly Packet':
    #                 if parseDateStart <= r.week_start <= parseDateStop:
    #                     print(r)
    #                     print('<-------HERE')
    #                     formsAndData[str(r.week_start)] = [r]
    #             elif formName[-1] == 'N':
    #                 if parseDateStart <= x.date <= parseDateStop:
    #                     formsAndData[str(x.date)] = [x]
    #                     break
    #                 else:
    #                     database_model = ''
    #                     continue
    #             else:
    #                 if str(r.week_start) == str(formDate):
    #                     database_model = r
    #                     formsAndData[str(r.week_start)] = [database_model]
    #                     print('Check B - Form Exist')
    #                     break
    #                 elif r == org[len(org)-1]:
    #                     database_model = ''
    #                     print('FORM DOES NOT EXIST')
    #                     goNext = True
    #                     print('goNext2')  
        
    #     data = database_model
    #     print('Form ' + item + ' includes these:' + str(list(formsAndData)))    
    #     if goNext:
    #         continue
    #     print('Processing Forms that were found for ' + item + '...')
    #     alphaStore = ''
    #     print(list(formsAndData))
    #     for alpha in list(formsAndData):
    #         print("CHECK 1")
    #         if len(formsAndData[alpha]) == 2:
    #             doubleDB = True
    #             print(item + ' is a double database...')
    #             data = formsAndData[alpha][0]
    #             readings = formsAndData[alpha][1]
    #         else:
    #             data = formsAndData[alpha][0]
    #             print(item + ' is a single database...')
    #         print(ModelForms)
    #         styles = getSampleStyleSheet()
    #         fileName = 'form' + formName + '_' + formDate + ".pdf"
    #         documentTitle = 'form' + formName + '_' + formDate
    #         title = ModelForms.header + ' ' + ModelForms.title + ' - Form (' + ModelForms.form + ')'
    #         subTitle = 'Facility Name: ' + facility
    #         #always the same on all A-forms
    #         marginSet = 0.4
    #         print('...Creating PDF for ' + item + '...')
    #         dataList = []
    #         print('STARTING...')
    #         #create a stream
    #         stream = io.BytesIO()
    #         heightGroup = ('A5', 'G1', 'G2', 'H')
    #         print("________________")
    #         print(itemID)
    #         # try:
    #         #     int(item)
    #         issueFormID = getNewFormLabel_w_formID(facility, itemID) #getFormID_w_oldFormLabel(itemID)
    #         try:
    #             issueForm = issues_model.objects.filter(date=data.date, form=issueFormID)
    #         except:
    #             issueForm = issues_model.objects.filter(date=data.week_start, form=issueFormID)
                
    #         if issueForm.exists():
    #             issueSpace = len(tableData)
    #             issueForm = issueForm[0]
    #             issueTable = [
    #                 [''],
    #                 [Paragraph('<para align=center><b>Corrective-Action</b></para>', styles['Normal'])],
    #                 [Paragraph('<para><b>Issues:</b>&#160;&#160;' + issueForm.issues + '</para>', styles['Normal'])],
    #                 [Paragraph('<para><b>EES Personnel Notified:</b>&#160;&#160;' + issueForm.notified + '&#160;&#160;&#160;&#160;&#160;<b>Date/Time:</b>&#160;&#160;' + date_change(issueForm.date) + '&#160;/&#160;' + time_change(issueForm.time) + '</para>', styles['Normal'])],
    #                 [Paragraph('<para><b>Corrective Action Taken:</b>&#160;&#160;' + issueForm.cor_action + '</para>', styles['Normal'])],
    #             ]
    #             for issue_line in issueTable:
    #                 tableData.append(issue_line)
    #             issueStyle = [
    #                 ('SPAN', (0,1 + issueSpace), (-1,1 + issueSpace)),
    #                 ('SPAN', (0,2 + issueSpace), (-1,2 + issueSpace)),
    #                 ('SPAN', (0,3 + issueSpace), (-1,3 + issueSpace)),
    #                 ('SPAN', (0,4 + issueSpace), (-1,4 + issueSpace)),
    #                 ('BOX', (0,1 + issueSpace), (-1,4 + issueSpace), 1, colors.black),
    #                 ('BOX', (0,1 + issueSpace), (-1,1 + issueSpace), 1, colors.black),
    #             ]
    #             for issue_style in issueStyle:
    #                 style.append(issue_style)
    #             if item in heightGroup:
    #                 addedRowHeights = (20,15,15,15,15)    
    #                 tableRowHeights = tableRowHeights + addedRowHeights
    #         print("________________")
            
    #         if item in heightGroup:
    #             dataList.append([tableData, tableColWidths, style, tableRowHeights],)
    #         else:
    #             dataList.append([tableData, tableColWidths, style, None],)
                
    #         pdf = SimpleDocTemplate(stream, pagesize=letter, topMargin=marginSet*inch, bottomMargin=0.3*inch, title=documentTitle)

    #         if item in heightGroup:
    #             table = Table(dataList[0][0], colWidths=dataList[0][1], rowHeights=dataList[0][3])
    #         else:
    #             table = Table(dataList[0][0], colWidths=dataList[0][1])
    #         style = TableStyle(dataList[0][2])
            
    #         table.setStyle(style)
            
    #         elems.append(table)
    #         elems.append(PageBreak())
    #         print('FINISHED...')
    #         print('PDFs for ' + item + ' has been created. Moving to next form')
    
    # print('Finished creating PDFs...')        
    # try:
        
    #     pdf.build(elems, canvasmaker=PageNumCanvas)
    #         # get buffer
    #     stream.seek(0)
    #     pdf_buffer = stream.getbuffer()
    #     print(pdf_buffer)
    #     response = HttpResponse(bytes(pdf_buffer), content_type='application/pdf')
    #     print('Starting to Compile...')
    # except UnboundLocalError as e:
    #     return HttpResponseNotFound("No Forms Found")