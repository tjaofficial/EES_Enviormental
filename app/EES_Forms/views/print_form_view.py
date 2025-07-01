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
from ..utils.main_utils import date_change, time_change
import io
from django.contrib import messages # type: ignore
import datetime
import calendar
import time
from .form_pdf_templates import *

lock = login_required(login_url='Login')

    
class PageNumCanvas(canvas.Canvas):
    def __init__(self, *args, form_label=None, fs_id=None, **kwargs):
        #Constructor
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        self.form_label = form_label
        self.fs_id = fs_id
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

        # Center bottom: MethodPlus info
        if self.form_label and self.fs_id:
            footer_text = f"MethodPlus+: Form {self.form_label} (fsID: {self.fs_id})"
            self.drawCentredString(105 * mm, 10 * mm, footer_text)
      
@lock
def form_PDF(request, type, formGroup, formIdentity, formDate):
    print(f"This a '{type}' form")
    print(f"Frequency: {formGroup}")
    startingDayNumb = int(request.user.user_profile.company.settings.weekly_start_day)
    if "-" in formIdentity:
        fsID = formIdentity.split('-')[0]
        facility = form_settings_model.objects.get(id=int(fsID)).facilityChoice.facility_name
    else:
        facility = the_packets_model.objects.get(id=int(formIdentity)).facilityChoice.facility_name
    
    formSettingsQuery = form_settings_model.objects.filter(facilityChoice__facility_name=facility)
    packetBeingPrinted = ''
    if type == 'single':
        if formGroup in ['Daily', 'Weekly', 'Monthly', 'Quarterly']:
            fsID, label = map(lambda x: int(x) if x.isdigit() else x, formIdentity.split('-'))
            formSettingsEntry = form_settings_model.objects.get(id=fsID)
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
    print(f"The fsID's being used are listed: {formsBeingUsed}")
    print("_________________________________")
    formsBeingUsed = sorted(formsBeingUsed, key=lambda x: x[0])
    print(f"The same list is sorted by PacketID: {formsBeingUsed}")
    print("_________________________________")
    elems = []
    for fsIDPackage in formsBeingUsed:
        fsEntry = fsIDPackage[1]
        footerFsID = fsEntry.id
        packetID = fsIDPackage[0]
        formID = int(fsEntry.formChoice.form)
        formInformation = fsEntry.formChoice
        formSettings = fsEntry.settings['settings']
        formModelName = formInformation.link + '_model'
        print(f"Now running process for form {formID} with fsID {fsIDPackage[1].id}")
        if type == 'single':
            formLabel = fsEntry.settings['packets'].get(str(packetID), str(fsEntry.id))
            if not formLabel:
                formLabel = fsEntry.id if packetID == "fsID" else False
            
            # if packetID == 'none':
            #     formLabel = ''
            # elif packetID == 'fsID':
            #     formLabel = fsEntry.id
            # else:
        else:
            formLabel = packetID
        footerLabel = formLabel
        print(f"The label for this instance of form {formID} is: {formLabel}")
        try:
            formModel = apps.get_model('EES_Forms', formModelName)
            formModel = formModel.objects.filter(formSettings__id=fsEntry.id)
            print(f"Pulling all submitted data for {formModelName} from {facility}")
            print('')
            print(formModel)
            print('')
        except:
            if formID == 23:
                formModel = apps.get_model('EES_Forms', 'form22_model')
                formModel = formModel.objects.filter(formSettings__facilityChoice__facility_name=facility)
                print('Using form 22 data to create form 23.')
                print('')  
                print("Pulling all submitted data for " + facility + " from "+ 'form22_model')
            else:
                print("Could not find a model with the name " + formModelName + " for formID " + str(formID))
                messages.error(request,"ERROR: ID-11850006. Contact Support Team.")
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
                amountOfDaysToStartingDay = (startingDayNumb-formDateParsed.weekday())
                if formDateParsed.weekday() < startingDayNumb:
                    amountOfDaysToStartingDay = amountOfDaysToStartingDay-7
                startDate = formDateParsed + datetime.timedelta(days=amountOfDaysToStartingDay)
                endDate = startDate + datetime.timedelta(days=6)
            else:   
                startDate = formDateParsed
        print(f"Filtering submissions starting on {startDate} and ending on {endDate}")
        ## ----- ADD NEW FORM DATE SELECTIONS BELOEW ----- ##
        try:
            formsAndData = formModel.filter(date__range=(startDate, endDate))
        except:
            formsAndData = formModel.filter(week_start__range=(startDate, endDate))
        
        print(f"Found {len(formsAndData)} form(s) within the specified time frame.")
        print('')
        if len(formsAndData) == 0:
            print("...Moving to next form")
            print("_________________________________")
            continue
        for formData in formsAndData:
            styles = getSampleStyleSheet()
            if formGroup == 'single':
                fileName = f"form{formLabel}_{formDate}.pdf"
                documentTitle = f"form{formLabel}_{formDate}"
            elif formGroup == 'coke_battery':
                fileName = "form_1_packet.pdf"
                documentTitle = "form_1_packet"
            elif type == 'single':
                if formGroup in ['Daily', "Weekly", "Monthly", "Quarterly"]:
                    fileName = "form" + str(fsIDPackage[0]) + "_" + str(formDateParsed)+".pdf"
                    documentTitle = "form" + str(fsIDPackage[0]) + "_" + str(formDateParsed)
            elif type == "group":
                if formGroup in ['Daily', "Weekly", "Monthly", "Quarterly"]:
                    fileName = str(packetBeingPrinted.name) + "_" + str(formDateParsed)+"_packet.pdf"
                    documentTitle = str(packetBeingPrinted.name)
            title = formInformation.header
            title += f" - {formSettings['custom_name']}" if 'custom_name' in formSettings and formSettings['custom_name'] else f" - {formInformation.title}"
            title += f" - Form ({formLabel if formLabel else 'none'})"
            
            subTitle = 'Facility Name: ' + facility
            #always the same on all A-forms
            marginSet = 0.4
            print('...Creating PDF for formID ' + str(formID) + '...')
            dataList = []
            print('STARTING...')
            #create a stream
            stream = io.BytesIO()
            if formID == 1:
                tableData, tableColWidths, style = pdf_template_A1(formData, title, subTitle)
            if formID == 2:
                tableData, tableColWidths, style = pdf_template_A2(formData, title, subTitle)
            if formID == 3:
                tableData, tableColWidths, style = pdf_template_A3(formData, title, subTitle)
            if formID == 4:
                tableData, tableColWidths, style = pdf_template_A4(formData, title, subTitle)
            if formID == 5:
                tableData, tableColWidths, tableRowHeights, style = pdf_template_A5(formData, title, subTitle, formInformation)
            if formID == 6:
                tableData, tableColWidths, style = pdf_template_6(formData, title, subTitle, formInformation)
            if formID == 7:
                tableData, tableColWidths, style = pdf_template_7(formData, title, subTitle)
            if formID == 8:
                tableData, tableColWidths, style = pdf_template_8(formData, title, subTitle)
            if formID == 9:
                tableData, tableColWidths, style = pdf_template_9(formData, title, subTitle)
            if formID == 17:
                tableData, tableColWidths, tableRowHeights, style = pdf_template_17(formData, title, subTitle)
            if formID == 18:
                tableData, tableColWidths, tableRowHeights, style = pdf_template_18(formData, title, subTitle)
            if formID == 19:
                tableData, tableColWidths, tableRowHeights, style = pdf_template_19(formData, title, subTitle)
            if formID == 20:
                tableData, tableColWidths, style = pdf_template_20(formData, title, subTitle)
            if formID == 21:
                tableData, tableColWidths, style = pdf_template_21(formData, title, subTitle)
            if formID == 22:
                tableData, tableColWidths, style = pdf_template_22(formData, title, subTitle)
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
            if formID == 29:
                tableData, tableColWidths, style = pdf_template_29(formData, title, subTitle, formInformation)

            heightGroup = (5,17,18,19)
            
            try:
                issueForm = issues_model.objects.filter(date=formData.date, formChoice=fsEntry)
            except:
                issueForm = issues_model.objects.filter(date=formData.week_start, formChoice=fsEntry)
                
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
        pdf_canvas = PageNumCanvas

        pdf.build(
            elems, 
            canvasmaker=lambda *args, **kwargs: pdf_canvas(*args, form_label=footerLabel, fs_id=footerFsID, **kwargs)
        )
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