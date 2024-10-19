from ..models import Forms
from django.shortcuts import HttpResponse # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.apps import apps # type: ignore
from django.http import HttpResponseNotFound # type: ignore
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, PageBreak # type: ignore
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.lib import colors # type: ignore
from reportlab.lib.styles import getSampleStyleSheet # type: ignore
from reportlab.lib.units import inch, mm # type: ignore
from reportlab.pdfgen import canvas # type: ignore
from ..models import issues_model, user_profile_model,form_settings_model, the_packets_model
from ..utils import date_change, time_change
import io
import datetime
import calendar
import time
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
def form_PDF(request, facility, type, formGroup, formIdentity, formDate):
    print(type)
    print(formGroup)
    userProfile = user_profile_model.objects.get(user=request.user)
    formSettingsQuery = form_settings_model.objects.filter(facilityChoice__facility_name=facility)
    packetBeingPrinted = ''
    if type == 'single':
        if formGroup in ['Daily', 'Weekly', 'Monthly']:
            formID_Label = formIdentity.split('-')
            formID = int(formID_Label[0])
            label = formID_Label[1]
            formSettingsEntry = formSettingsQuery.get(id=int(formID))
            formsBeingUsed = [(label,formSettingsEntry)]
    elif formGroup == 'Daily' and type == 'group':
        formsBeingUsed = []
        packetBeingPrinted = the_packets_model.objects.get(id=formIdentity)
        packetFormList = packetBeingPrinted.formList["formsList"]
        for packs in packetFormList:
            for settingsForm in formSettingsQuery:
                if packetFormList[packs]['settingsID'] == settingsForm.id:
                    formsBeingUsed.append((packs ,settingsForm))
    elif formGroup == 'Weekly' and type == 'group':
        formsBeingUsed = []
        packetBeingPrinted = the_packets_model.objects.get(id=formIdentity)
        packetFormList = packetBeingPrinted.formList["formsList"]
        for packs in packetFormList:
            for settingsForm in formSettingsQuery:
                if packetFormList[packs]['settingsID'] == settingsForm.id:
                    formsBeingUsed.append((packs ,settingsForm))
            # if fForms[0] == 23:
            #     continue
    elif formGroup == 'Monthly':
        formsBeingUsed = ['G2', 'Spill Kits']
    elif formGroup == 'tanks':
        formsBeingUsed = []
    elif formGroup == 'waste':
        formsBeingUsed = []
    print("The fsID's being used are listed below:")
    print(formsBeingUsed)
    print("_________________________________")
    elems = []
    for fsIDPackage in formsBeingUsed:
        print("Now running process for form: " + str(fsIDPackage[1].id))
        fsEntry = fsIDPackage[1]
        packetID = fsIDPackage[0]
        formID = fsEntry.formChoice.id
        formInformation = fsEntry.formChoice
        formSettings = fsEntry.settings['settings']
        formModelName = formInformation.link + '_model'
        if type == 'single':
            if packetID == 'none':
                formLabel = ''
            elif packetID == 'fsID':
                formLabel = fsEntry.id
            else:
                formLabel = fsEntry.settings['packets'][packetID]
        else:
            formLabel = packetID
        print(formLabel)
        try:
            formModel = apps.get_model('EES_Forms', formModelName)
            formModel = formModel.objects.filter(facilityChoice__facility_name=facility)
            print("Pulling all submitted data for " + facility + " from "+ formModelName)
            print('')
            print(formModel)
            print('')
        except:
            if formID == 23:
                formModel = apps.get_model('EES_Forms', 'form22_model')
                formModel = formModel.objects.filter(facilityChoice__facility_name=facility)
                print('Using form 22 data to create form 23.')
                print('')  
                print("Pulling all submitted data for " + facility + " from "+ 'form22_model')
            else:
                print("Could not find a model with the name " + formModelName + " for formID " + str(formID))
                continue
        try:
            formDateParsed = datetime.datetime.strptime(formDate, "%Y-%m-%d").date()
        except:
            formDateParsed = datetime.datetime.strptime(formDate, "%Y-%m").date()
        if type == 'single' and formInformation.frequency == 'Monthly':
            monthDays = calendar.monthrange(formDateParsed.year, formDateParsed.month)
            startDateString = str(formDateParsed.year) + "-" + str(formDateParsed.month) + "-01"
            endDateString = str(formDateParsed.year) + "-" + str(formDateParsed.month) + "-" + str(monthDays[1])
            startDate = datetime.datetime.strptime(startDateString, "%Y-%m-%d").date()
            endDate = datetime.datetime.strptime(endDateString, "%Y-%m-%d").date()
        elif formInformation.frequency == 'Daily':
            formDateParsed = datetime.datetime.strptime(formDate, "%Y-%m-%d").date()
            startDate = formDateParsed
            endDate = formDateParsed
        elif formGroup == 'Weekly':
            formDateParsed = datetime.datetime.strptime(formDate, "%Y-%m-%d").date()
            endDate = formDateParsed
            if type not in ['single', 'coke_battery']:
                weekly_start_day = packetBeingPrinted.formList['settings']['weekly_start_day']
                startingDayNumb = time.strptime(weekly_start_day, "%A").tm_wday
                amountOfDaysToStartingDay = (startingDayNumb-formDateParsed.weekday())
                if formDateParsed.weekday() < startingDayNumb:
                    amountOfDaysToStartingDay = amountOfDaysToStartingDay-7
                startDate = formDateParsed + datetime.timedelta(days=amountOfDaysToStartingDay)
                endDate = startDate + datetime.timedelta(days=6)
            else:   
                startDate = formDateParsed
        else:
            formDateParsed = datetime.datetime.strptime(formDate, "%Y-%m-%d").date()
            endDate = formDateParsed
            if type not in ['single', 'coke_battery']:
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
            if int(formID) in (1,5,17,18,19,22):
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
            styles = getSampleStyleSheet()
            if formGroup == 'single':
                fileName = 'form' + str(formLabel) + '_' + formDate + ".pdf"
                documentTitle = 'form' + str(formLabel) + '_' + formDate
            elif formGroup == 'coke_battery':
                fileName = "form_1_packet.pdf"
                documentTitle = "form_1_packet"
            elif type == 'single':
                if formGroup in ['Daily', "Weekly", "Monthly"]:
                    fileName = "form" + str(fsIDPackage[0]) + "_" + str(formDateParsed)+".pdf"
                    documentTitle = "form" + str(fsIDPackage[0]) + "_" + str(formDateParsed)
            elif type == "group":
                if formGroup in ['Daily', "Weekly", "Monthly"]:
                    fileName = str(packetBeingPrinted.name) + "_" + str(formDateParsed)+"_packet.pdf"
                    documentTitle = str(packetBeingPrinted.name)
            title = formInformation.header
            if formSettings['custom_name']:
                title += ' - ' + formSettings['custom_name']
            else:
                title += ' - ' + formInformation.title
            
            if packetID != 'none':
                title += ' - Form (' + str(formLabel) + ')'
            
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
                tableData, tableColWidths, tableRowHeights, style = pdf_template_A5(formData, formSecondaryData, title, subTitle, formInformation)
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
                tableData, tableColWidths, style = pdf_template_25(formData, title, subTitle)
            if formID == 26:
                tableData, tableColWidths, style = pdf_template_26(formData, title, subTitle, formInformation)
            if formID == 27:
                tableData, tableColWidths, style = pdf_template_27(formData, title, subTitle, formInformation)
                
            heightGroup = (5,17,18,19)
            
            try:
                issueForm = issues_model.objects.filter(date=formData.date, form=fsEntry.id)
            except:
                issueForm = issues_model.objects.filter(date=formData.week_start, form=fsEntry.id)
                
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
        print(type)
        print(formGroup)
        return HttpResponseNotFound("No Forms Found")
    
    return response