from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import *
from datetime import datetime as dtime, date, time
from django.db.models import Q
from django.apps import apps
import ast
import requests
import json
from django.shortcuts import redirect
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
    else:
        print("NO IT DIDNT SAVE")    

def setUnlockClientSupervisor(requestUserData):
    unlock = False
    client = False
    supervisor = False
    if requestUserData.groups.filter(name=OBSER_VAR):
        unlock = True
    if requestUserData.groups.filter(name=CLIENT_VAR):
        client = True
    if requestUserData.groups.filter(name=SUPER_VAR) or requestUserData.is_superuser:
        supervisor = True
        
    return (unlock, client, supervisor)

def weatherDict(city):
    # request the API data and convert the JSON to Python data types
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=435ac45f81f3f8d42d164add25764f3c'
    try:
        city_weather = requests.get(url.format(city)).json()
        weather = {
            'city': city,
            'temperature': round(city_weather['main']['temp'], 0),
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
            'wind_speed': round(city_weather['wind']['speed'], 0),
            'wind_direction': city_weather['wind']['deg'],
            'humidity': city_weather['main']['humidity'],
        }
        degree = weather['wind_direction']
        
        def toTextualDescription(degree):
            if degree > 337.5:
                return 'N'
            if degree > 292.5:
                return 'NW'
            if degree > 247.5:
                return 'W'
            if degree > 202.5:
                return 'SW'
            if degree > 157.5:
                return 'S'
            if degree > 122.5:
                return 'SE'
            if degree > 67.5:
                return 'E'
            if degree > 22.5:
                return 'NE'
            return 'N'
        wind_direction = toTextualDescription(degree)
        weather['wind_direction'] = wind_direction
    except:
        weather = {
            'error': "Please inform Supervisor '" + str(city) + "' is not a valid city.",
            'city': False
        }
    return weather

def calculateProgessBar(facility, frequency):
    formSubRecords = formSubmissionRecords_model.objects.filter(facilityChoice__facility_name=facility)
    forms_comp = [] 
    for formSub in formSubRecords.filter(submitted=True):
        if formSub.formID.frequency == frequency:
            forms_comp.append(formSub.formID.id)
    count_comp = len(forms_comp)
    count_total = len(formSubRecords.filter(formID__frequency=frequency))
    percent_completed = (count_comp / count_total) * 100
    print(percent_completed)
    return percent_completed 

def ninetyDayPushTravels(facility):
    all_db_reads = formA5_readings_model.objects.filter(form__facilityChoice__facility_name=facility)
    if all_db_reads.exists():
        def all_ovens(reads):
            A = []
            for p in reads:
                date = p.form.date
                list = [p.o1, p.o2, p.o3, p.o4]
                year = date.year
                month = date.month
                day = date.day

                dateAdded = datetime.datetime(year, month, day)
                EXPdate = dateAdded + datetime.timedelta(days=91)
                daysLeft = EXPdate - datetime.datetime.now()
                
                for q in list:
                    if len(str(q)) == 1:
                        ovenNumber = "0" + str(q)
                    else:
                        ovenNumber = q

                    A.append((ovenNumber, p.form.date, EXPdate.date, daysLeft.days))
            return A
        all_read_ovens = all_ovens(all_db_reads)
        func = lambda x: (x[0], x[1])
        sort_by_oven = sorted(all_read_ovens, key=func, reverse=True)

        def final(organizedOvens):
            B = []
            i = 1
            for oven_a in organizedOvens:
                B.append(oven_a)
            for oven_b in organizedOvens:
                for y in range(i, len(organizedOvens)):
                    check_instance = organizedOvens[y]
                    if check_instance[0] == oven_b[0]:
                        if check_instance in B:
                            B.remove(check_instance)
                i += 1

            for n in range(1, 86):
                for oven in B:
                    if len(str(n)) == 1:
                        zero_n = "0" + str(n)
                    else:
                        zero_n = str(n)
                        
                    if zero_n == oven[0]:
                        exist = True
                        break
                    else:
                        exist = False
                if not exist:
                    B.append((zero_n, 'N/A', 0, 0))              
            return B
        all_ovens_EXP = final(sort_by_oven)
        
        def sort_key(oven):
            return oven[0]
        all_ovens_EXP.sort(key=sort_key, reverse=True) 
        
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

        od_30 = overdue_30(all_ovens_EXP)
        od_10 = overdue_10(all_ovens_EXP)
        od_5 = overdue_5(all_ovens_EXP)
        od_recent = overdue_closest(all_ovens_EXP)
    
        return {'30days': od_30, '10days': od_10, '5days': od_5, 'closest': od_recent, 'all': all_ovens_EXP}
    return 'EMPTY'
    
def userColorMode(user):
    userProfile = user_profile_model.objects.filter(user__username=user.username)
    if userProfile.exists():
        userColorMode = userProfile[0].colorMode
    if userColorMode == 'light':
        return (False, 'lightMode')
    else:
        return (True, 'darkMode')
     
def colorModeSwitch(request):
    userProfile = user_profile_model.objects.filter(user__username=request.user.username)
    if userProfile.exists():
        userProfile = userProfile[0]
    if request.POST['colorMode'] == 'light':
        userProfile.colorMode = 'light'
    else:
        userProfile.colorMode = 'dark'
    print(userProfile.colorMode)
    userProfile.save()
    print(userProfile.colorMode)

    return redirect(request.META['HTTP_REFERER'])

def getOldFormID(facility, formID):
    facilitiesForm = facility_forms_model.objects.filter(facilityChoice__facility_name=facility)
    if facilitiesForm.exists():
        formIDandLabel = ast.literal_eval(facilitiesForm[0].formData)
        for formPair in formIDandLabel:
            if formID == formPair[0]:
                formLabel = formPair[1]
                return formLabel

def createNotificationDatabase(facility, user, formID, date, notifSelector):
    todayNumb = datetime.date.today().weekday()
    nFacility = bat_info_model.objects.filter(facility_name=facility)
    if nFacility.exists():
        nFacility = nFacility[0]
    nUserProfile = user_profile_model.objects.filter(user__username=user.username)
    if nUserProfile.exists():
        nUserProfile = nUserProfile[0]
    companyUsers = user_profile_model.objects.filter(company__company_name=nUserProfile.company.company_name )
    # subForm = formSubmissionRecords_model.objects.filter(facilityChoice__facility_name=facility, formID__id=formID)
    # if subForm.exists():
    #     subForm = subForm[0]
    #     if subForm.formID.id not in {26,27}:
    #         ModelName =  'form' + subForm.formID.form.replace('-','') + '_model'
    #     else:
    #         ModelName = subForm.formID.form.replace(' ', '_').lower() + '_model'
    # modelData = apps.get_model('EES_Forms', ModelName).objects.all()
    newHeader =  notifSelector        
    if notifSelector == 'submitted':
        nForms = getOldFormID(facility, formID)    
        if todayNumb in {5,6}:
            if todayNumb == 5:
                todayName = 'Saturday'
            else:
                todayName = 'Sunday'
        newNotifData = json.dumps({'formID': formID, 'date': str(date), 'weekend': todayName})
    else:
        todayName = False
    if notifSelector == 'corrective':
        newNotifData = json.dumps({'formID': formID, 'date': str(date)})
    elif notifSelector == '90days':
        newNotifData = json.dumps({'ovenNumber': formID, 'date': str(date)})
    elif notifSelector == 'messages':
        print('Inbox Messages: TBA')

    for person in companyUsers:
        n = notifications_model(
            facilityChoice=nFacility,
            user = person,
            clicked = False,
            hovered = False,
            formData = newNotifData,
            header = newHeader,
            body = "Click here to view.",
            notes = "Submitted by " + user.first_name + " " + user.last_name + ". "
        )
        if n not in companyUsers:
            n.save()
    print("Form " + nForms + " notification was sent.")
   
def notificationCalc(user, facility):
    userProfile = user_profile_model.objects.filter(user__username=user.username)
    if userProfile.exists():
        userProfile = userProfile[0]
    notifications = notifications_model.objects.filter(facilityChoice__facility_name=facility)
    newNotifs = notifications.filter(clicked=False, hovered=False, user=userProfile)
    if newNotifs.exists():
        notifCount = len(newNotifs)
    else:
        notifCount = 0
    return notifCount
    
def displayNotifications(user, facility):
    notifCount = notificationCalc(user, facility)
    nUserProfile = user_profile_model.objects.filter(user__username=user.username)
    if nUserProfile.exists():
        nUserProfile = nUserProfile[0]
    allNotifs = notifications_model.objects.filter(facilityChoice__facility_name=facility, user=nUserProfile).order_by('-created_at')
    facForms = facility_forms_model.objects.filter(facilityChoice__facility_name=facility)
    if facForms.exists():
        formIDandLabel = ast.literal_eval(facForms[0].formData)
    unReadList = []
    readList = []
    unReadNotifs = allNotifs.filter(clicked=False, hovered=False)
    readNotifs = allNotifs.filter(hovered=False)
    for unRead in unReadNotifs:
        notifFormData = json.loads(unRead.formData)
        for x in formIDandLabel:
            if int(notifFormData['formID']) == int(x[0]):
                for y in formSubmissionRecords_model.objects.filter(facilityChoice__facility_name=facility, formID__id=x[0]):
                    parseForm = "form" + y.formID.link
                    formPullData = (x, unRead, notifFormData, y.formID.link)
                    unReadList.append(formPullData)
    print('__________________________________________________________')
    return {'notifCount': notifCount, 'unRead': unReadList, "read": readNotifs}
        
def createNotification(facility, user, formID, date, notifSelector):
    createNotificationDatabase(facility, user, formID, date, notifSelector)
    facilityParse = 'notifications_' + facility.replace(" ","_")
    notifCount = str(notificationCalc(user, facility))
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        facilityParse, {
            'type': 'notification',
            'count': notifCount,
            'facility': facility
        }
    )
    
def checkIfFacilitySelected(user, facility):
    if facility != 'supervisor':
        notifs = displayNotifications(user, facility)
    else:
        notifs = ''
    return notifs