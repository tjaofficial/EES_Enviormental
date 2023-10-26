from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import *
from datetime import datetime as dtime, date, time
from django.db.models import Q
from django.apps import apps
import ast

#from .admin import EventAdmin

parseFormList = [
    (1, "A1"),
    (2, "A2"),
    (3, "A3"),
    (4, "A4"),
    (5, "A5"),
    (6, "B"),
    (7, "C"),
    (8, "D"),
    (9, "E"),
    (10, "F1"),
    (11, "F2"),
    (12, "F3"),
    (13, "F4"),
    (14, "F5"),
    (15, "F6"),
    (16, "F7"),
    (17, "G1"),
    (18, "G1"),
    (19, "H"),
    (20, "I"),
    (21, "L"),
    (22, "M"),
    (23, "N"),
    (24, "O"),
    (25, "P"),
    (26, "R"),
    (27, "Q"),  
]

# takes in the database array and returns wether it is empty True/False
def DBEmpty(DBArray):
    emptyDB = False
    if len(DBArray) == 0:
        emptyDB = True
    return emptyDB

class EventCalendar(HTMLCalendar):
    def __init__(self, events=None):
        super(EventCalendar, self).__init__()
        self.events = events
 
    def formatday(self, day, weekday, events, year):
        """
        Return a day as a table cell.
        """
        events_from_day = events.filter(date__day=day)
        events_html = "<ul>"
        for event in events_from_day:
            if event.date.year == year.year:
                events_html += event.get_absolute_url2() + "<br>"
        events_html += "</ul>"
 
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, events_html)
 
    def formatweek(self, theweek, events, year):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events, year) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s
 
    def formatmonth(self, theyear, themonth, year, withyear=True):
        """
        Return a formatted month as a table.
        """
        
        events = Event.objects.filter(date__month=themonth)
 
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events, year))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)
    
class Calendar(HTMLCalendar):
    def __init__(self, events=None):
        super(Calendar, self).__init__()
        self.events = events
 
    def formatday(self, day, weekday, events, year):
        """
        Return a day as a table cell.
        """        
        events_from_day = events.filter(date__day=day)
        events_html = "<ul>"
        for event in events_from_day:
            if event.date.year == year:
                events_html += event.get_absolute_url() + "<br>"
        events_html += "</ul>"

        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, events_html)

 
    def formatweek(self, theweek, events, year):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events, year) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s
        
        
 
    def formatmonth(self, theyear, themonth, year, facility, withyear=True):
        """
        Return a formatted month as a table.
        """
        if facility == "supervisor":
            events = Event.objects.filter(date__month=themonth, personal=True)
        else:
            events = Event.objects.filter(date__month=themonth, facilityChoice__facility_name=facility)
 
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events, year))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

class Calendar2(HTMLCalendar):
    def __init__(self, events=None):
        super(Calendar2, self).__init__()
        self.events = events
 
    def formatday(self, day, weekday, events, year, forms, selectedForm):
        """
        Return a day as a table cell.
        """        
        def formatTheDayNumber(day):
            day = str(day)
            if len(day) == 1:
                newDay = "0" + day
                return newDay
            else:
                return day
        print("COntinued....")
        forms_html = "<ul>"
         
        if selectedForm == "Coke Battery Daily Packet":
            print("Starting to find Forms that exist on this day for daily...")
            print(forms)
            aPacketFormList = []
            for iForms in forms:
                print(iForms.date)
                print(day)
                if iForms.date.day == day:
                    print(iForms.date)
                    aPacketFormList.append(iForms)
            print(aPacketFormList)
            for h in aPacketFormList:
                if h.date.year == year:
                    selectedFormDate = h
                    forms_html += "<a href='../../../../printIndex/" + selectedForm + "/group-" + str(selectedFormDate.date.year) + "-"+ formatTheDayNumber(selectedFormDate.date.month) +"-"+ formatTheDayNumber(selectedFormDate.date.day) +"'>Submitted Packet</a><br>"
                    break
        elif selectedForm == "Facility Weekly Packet":
            print("Starting to find Forms that exist on this day for weekly...")
            print(forms)
            wPacketFormList = []
            for iForms in forms:
                try:
                    if iForms.date.day == day:
                        wPacketFormList.append(iForms)
                except:
                    if iForms.week_start.day == day:
                        wPacketFormList.append(iForms)
            for h in wPacketFormList:
                try:
                    if h.date.year == year:
                        selectedFormDate = h
                        forms_html += "<a href='../../../../printIndex/" + selectedForm + "/group-" + str(selectedFormDate.date.year) + "-"+ formatTheDayNumber(selectedFormDate.date.month) +"-"+ formatTheDayNumber(selectedFormDate.date.day) +"'>Submitted Packet</a><br>"
                        break
                except:
                    if h.week_start.year == year:
                        selectedFormDate = h
                        forms_html += "<a href='../../../../printIndex/" + selectedForm + "/group-" + str(selectedFormDate.week_start.year) + "-"+ formatTheDayNumber(selectedFormDate.week_start.month) +"-"+ formatTheDayNumber(selectedFormDate.week_start.day) +"'>Submitted Packet</a><br>"
                        break
            
        else:
            # selectedForm = selectedForm.upper()
            if selectedForm[2]:
                print(day)
                forms_from_day = forms.filter(date__day=day)
                for form in forms_from_day:
                    if form.date.year == year:
                        forms_html += "<a href='../../../../printIndex/" + str(selectedForm[0]) + "/single-" + str(form.date.year) + "-"+ formatTheDayNumber(form.date.month) +"-"+ formatTheDayNumber(form.date.day) +"'>Submitted Form</a><br>"
            else:
                forms_from_day = forms.filter(week_start__day=day)
                for form in forms_from_day:
                    if form.week_start.year == year:
                        forms_html += "<a href='../../../../printIndex/" + str(selectedForm[0]) + "/single-" + str(form.week_start.year) + "-"+ formatTheDayNumber(form.week_start.month) +"-"+ formatTheDayNumber(form.week_start.day) +"'>Submitted Form</a><br>"
        forms_html += "</ul>"
        
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, forms_html)

 
    def formatweek(self, theweek, events, year, forms, selectedForm):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events, year, forms, selectedForm) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s
        
        
 
    def formatmonth(self, theyear, themonth, year, forms, facility, withyear=True):
        """
        Return a formatted month as a table.
        """
        facilityForms = facility_forms_model.objects.filter(facilityChoice__facility_name=facility)
        formList = ast.literal_eval(facilityForms[0].formData)
        ogFormID = forms[0]
        
        print("start")
        print(isinstance(forms, tuple))
        if not isinstance(forms, tuple):
            if forms == "Coke Battery Daily Packet":
                aPacket = ["1","2","3","4","5"]
                packetExists = []
                for aForm in aPacket:
                    modelSelect = "formA" + aForm + "_model"
                    print(modelSelect)
                    chk_database = apps.get_model('EES_Forms', modelSelect).objects.filter(date__year=year, date__month=themonth, facilityChoice__facility_name=facility)
                    if chk_database.exists():
                        packetExists.extend(chk_database)
                print(packetExists)
                chk_database = packetExists
                selectedForm = forms
            elif forms == "Facility Weekly Packet":
                wPacket = formList
                packetExists = []
                for indivForms in wPacket:
                    for indivParse in parseFormList:
                        if int(indivForms[0]) == int(indivParse[0]):
                            ogFormLabel = indivForms[1]
                            formID = indivForms[0]
                    if ogFormLabel == "N":
                        continue
                    try:
                        try:
                            modelSelect = "form" + ogFormLabel + "_model"
                            chk_database = apps.get_model('EES_Forms', modelSelect).objects.filter(date__year=year, date__month=themonth, facilityChoice__facility_name=facility)
                        except:
                            modelSelect = "form" + str(formID) + "_model"
                            chk_database = apps.get_model('EES_Forms', modelSelect).objects.filter(date__year=year, date__month=themonth, facilityChoice__facility_name=facility)
                    except:
                        try:
                            modelSelect = "form" + ogFormLabel + "_model"
                            chk_database = apps.get_model('EES_Forms', modelSelect).objects.filter(week_start__year=year, week_start__month=themonth, facilityChoice__facility_name=facility)
                        except:
                            modelSelect = "form" + str(formID) + "_model"
                            chk_database = apps.get_model('EES_Forms', modelSelect).objects.filter(week_start__year=year, week_start__month=themonth, facilityChoice__facility_name=facility)
                    
                    if chk_database.exists():
                        packetExists.extend(chk_database)
                selectedForm = forms
                chk_database = packetExists
                
        else:
            for parsingForm in parseFormList:
                if int(parsingForm[0]) == int(forms[0]):
                    selectedForm = parsingForm

            modelWithNumber = "form" + str(ogFormID) + "_model"
            try:
                print("CHECK 1")
                try:
                    print("CHECK 1.1")
                    chk_database = apps.get_model('EES_Forms', modelWithNumber).objects.filter(date__year=year, date__month=themonth, facilityChoice__facility_name=facility)
                    if len(chk_database) == 0:
                        chk_database.fail
                    makeList = list(selectedForm)
                    makeList.append(True)
                    selectedForm = tuple(makeList)
                except:
                    print("CHECK 1.2")
                    chk_database = apps.get_model('EES_Forms', modelWithNumber).objects.filter(week_start__year=year, week_start__month=themonth, facilityChoice__facility_name=facility)
                    makeList = list(selectedForm)
                    makeList.append(False)
                    selectedForm = tuple(makeList)
            except:
                print("CHECK 2")
                if selectedForm[1] in {"Q", "R"}:
                    if selectedForm[1] == "R":
                        modelWithLetter = "spill_kits_model"
                    else:
                        modelWithLetter = "quarterly_trucks_model"
                else:
                    modelWithLetter = "form" + selectedForm[1].upper() + "_model"
                try:
                    print("CHECK 2.1")
                    chk_database = apps.get_model('EES_Forms', modelWithLetter).objects.filter(date__year=year, date__month=themonth, facilityChoice__facility_name=facility)
                    makeList = list(selectedForm)
                    makeList.append(True)
                    selectedForm = tuple(makeList)
                except:
                    print("CHECK 2.2")
                    chk_database = apps.get_model('EES_Forms', modelWithLetter).objects.filter(week_start__year=year, week_start__month=themonth, facilityChoice__facility_name=facility)
                    makeList = list(selectedForm)
                    makeList.append(False)
                    selectedForm = tuple(makeList)
            
        
        #print(chk_database.filter(date__day=12))
        print("<--------------------------")
        try:
            events = Event.objects.filter(date__month=themonth)
        except:
            events = Event.objects.filter(week_start__month=themonth)
        print(forms)
        # print(len(forms))
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events, year, chk_database, selectedForm))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

def stringToDate(date):
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
    
    if len(str(date.month)) == 2:
        month = str(date.month)
    else:
        month = '0'+str(date.month)
    if len(str(date.day)) == 2:
        day = str(date.day)
    else:
        day = '0'+str(date.day)
    parsed = str(date.year) + '-' + month + '-' + day
    return parsed

def updateSubmissionForm(facility, formID, submitted, date):
    if formSubmissionRecords_model.objects.filter(facilityChoice__facility_name=facility, formID=formID).exists():
        formSubmission = formSubmissionRecords_model.objects.filter(facilityChoice__facility_name=facility, formID=formID)[0]
        formSubmission.submitted = submitted
        formSubmission.dateSubmitted = date
        formSubmission.save()
        print("YEAH IT SAVED")
    print("NO IT DIDNT SAVE")    