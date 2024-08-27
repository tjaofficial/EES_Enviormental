from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import *
from datetime import datetime as dtime, date, time
from django.db.models import Q
from django.apps import apps
import ast
import requests
import json
import braintree
import os
from django.shortcuts import redirect
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  

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
        print(selectedForm)
        print(forms)
        if isinstance(selectedForm, str):
            packetsEntry = the_packets_model.objects.get(id=int(selectedForm))
            if packetsEntry.frequency == 'Daily':
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
                        forms_html += "<a href='../../../../printIndex/coke_battery/"+ str(selectedForm) +"/" + str(selectedFormDate.date.year) + "-"+ formatTheDayNumber(selectedFormDate.date.month) +"-"+ formatTheDayNumber(selectedFormDate.date.day) +"'>Submitted Packet</a><br>"
                        break
            elif packetsEntry.frequency == 'Weekly':
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
                            print('check 1')
                            selectedFormDate = h
                            print('check 2')
                            forms_html += "<a href='../../../../printIndex/facility_weekly/"+ str(selectedForm) +"/" + str(selectedFormDate.date.year) + "-"+ formatTheDayNumber(selectedFormDate.date.month) +"-"+ formatTheDayNumber(selectedFormDate.date.day) +"'>Submitted Packet</a><br>"
                            break
                    except:
                        if h.week_start.year == year:
                            selectedFormDate = h
                            forms_html += "<a href='../../../../printIndex/facility_weekly/"+ str(selectedForm) +"/" + str(selectedFormDate.week_start.year) + "-"+ formatTheDayNumber(selectedFormDate.week_start.month) +"-"+ formatTheDayNumber(selectedFormDate.week_start.day) +"'>Submitted Packet</a><br>"
                            break
            elif packetsEntry.frequency == 'Monthly':
                print('Monthly')
        else:
            if selectedForm[1]:
                forms_from_day = forms.filter(date__day=day)
                for form in forms_from_day:
                    if form.date.year == year:
                        forms_html += "<a href='../../../../printIndex/single/" + str(selectedForm[0]) + "/" + str(form.date.year) + "-"+ formatTheDayNumber(form.date.month) +"-"+ formatTheDayNumber(form.date.day) +"'>Submitted Form</a><br>"
            else:
                forms_from_day = forms.filter(week_start__day=day)
                for form in forms_from_day:
                    if form.week_start.year == year:
                        forms_html += "<a href='../../../../printIndex/single/" + str(selectedForm[0]) + "/" + str(form.week_start.year) + "-"+ formatTheDayNumber(form.week_start.month) +"-"+ formatTheDayNumber(form.week_start.day) +"'>Submitted Form</a><br>"        
        
        forms_html += "</ul>"
        
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="hover %s">%d%s</td>' % (self.cssclasses[weekday], day, forms_html)

 
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
        formSettingsQuery = form_settings_model.objects.filter(facilityChoice__facility_name=facility)
        formList = get_facility_forms('facilityName', facility)
        #ogFormID = forms
        
        print("start")
        print(forms)
        if isinstance(forms, str):
            print("This is a Packet Print for packetID "+forms)
            packetsEntry = the_packets_model.objects.get(id=int(forms))
            allFormsSettingsList = []
            for pacForm in packetsEntry.formList:
                pacfsID = packetsEntry.formList[pacForm]['settingsID']
                for settingsEntry in formSettingsQuery:
                    if pacfsID == settingsEntry.id:
                        allFormsSettingsList.append(settingsEntry)
            print(allFormsSettingsList)
            packetExists = []
            for iFormSettings in allFormsSettingsList:
                formID = iFormSettings.formChoice.id
                formInformation = iFormSettings.formChoice
                name_of_model = formInformation.link + "_model"
                if formID == 23:
                    chk_database = formM_model.objects.filter(date__year=year, date__month=themonth, facilityChoice__facility_name=facility)
                else:
                    try:#### ----- Set up a code to switch over to a number based model instead of labels
                        chk_database = apps.get_model('EES_Forms', name_of_model).objects.filter(date__year=year, date__month=themonth, facilityChoice__facility_name=facility)
                    except:
                        chk_database = apps.get_model('EES_Forms', name_of_model).objects.filter(week_start__year=year, week_start__month=themonth, facilityChoice__facility_name=facility)
                
                if chk_database.exists():
                    packetExists.extend(chk_database)
            # if forms == "Coke Battery Daily Packet":
            #     aPacket = ["1","2","3","4","5"]
            #     packetExists = []
            #     for aForm in aPacket:
            #         modelSelect = "formA" + aForm + "_model"
            #         print(modelSelect)
            #         chk_database = apps.get_model('EES_Forms', modelSelect).objects.filter(date__year=year, date__month=themonth, facilityChoice__facility_name=facility)
            #         if chk_database.exists():
            #             packetExists.extend(chk_database)
            #     print(packetExists)
            # elif forms == "Facility Weekly Packet":
            #     wPacket = formList
            #     packetExists = []
            #     for indivForms in wPacket:
            #         formID = indivForms[0]
            #         formInformation = Forms.objects.get(id=formID)
            #         name_of_model = formInformation.link + "_model"
            #         if formID == 23:
            #             chk_database = formM_model.objects.filter(date__year=year, date__month=themonth, facilityChoice__facility_name=facility)
            #         else:
            #             try:#### ----- Set up a code to switch over to a number based model instead of labels
            #                 chk_database = apps.get_model('EES_Forms', name_of_model).objects.filter(date__year=year, date__month=themonth, facilityChoice__facility_name=facility)
            #             except:
            #                 chk_database = apps.get_model('EES_Forms', name_of_model).objects.filter(week_start__year=year, week_start__month=themonth, facilityChoice__facility_name=facility)
                    
            #         if chk_database.exists():
            #             packetExists.extend(chk_database)
            selectedForm = forms
            chk_database = packetExists
        elif isinstance(forms, int):
            for x in formSettingsQuery:
                if x.id == forms:
                    fsEntry = x
            name_of_model = fsEntry.formChoice.link + "_model"
            if fsEntry.formChoice.id == 23:
                chk_database = apps.get_model('EES_Forms', "formM_model").objects.filter(date__year=year, date__month=themonth, facilityChoice__facility_name=facility)
                print(formM_model.objects.all())
                originalStyle = True
            else:
                try:
                    print("CHECK 1.1")
                    chk_database = apps.get_model('EES_Forms', name_of_model).objects.filter(date__year=year, date__month=themonth, facilityChoice__facility_name=facility)
                    originalStyle = True
                except:
                    print("CHECK 1.2")
                    chk_database = apps.get_model('EES_Forms', name_of_model).objects.filter(week_start__year=year, week_start__month=themonth, facilityChoice__facility_name=facility)
                    originalStyle = False
            makeList = [forms]
            makeList.append(originalStyle)
            selectedForm = tuple(makeList)
        else:
            print("not a packet or form")
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

def updateSubmissionForm(fsID, submitted, date):
    formSettingsSub = form_settings_model.objects.get(id=int(fsID)).subChoice
    formSettingsSub.submitted = submitted
    formSettingsSub.dateSubmitted = date
    formSettingsSub.save()
    print("YEAH IT SAVED") 

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
    if count_total == 0:
        percent_completed = False
    else:
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
    else:
        return {'30days': [], '10days': [], '5days': [], 'closest': [], 'all': []}
    
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

def createNotificationDatabase(facility, user, fsID, date, notifSelector):
    todayNumb = datetime.date.today().weekday()
    nFormSettings = form_settings_model.objects.get(id=fsID)
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
        formID = nFormSettings.formChoice.id
        if todayNumb in {5,6}:
            if todayNumb == 5:
                todayName = 'Saturday'
            else:
                todayName = 'Sunday'
        else:
            todayName = False
        newNotifData = json.dumps({'settingsID': fsID, 'date': str(date), 'weekend': todayName})
    else:
        todayName = False
    if notifSelector == 'corrective':
        newNotifData = json.dumps({'settingsID': fsID, 'date': str(date)})
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
    print("Form " + str(nFormSettings.id) + " notification was sent.")
   
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
    facForms = get_facility_forms('facilityName', facility)
    
    unReadList = []
    readList = []
    unReadNotifs = allNotifs.filter(clicked=False, hovered=False)
    readNotifs = allNotifs.filter(hovered=False)
    if unReadNotifs.exists():
        for unRead in unReadNotifs:
            notifFormData = json.loads(unRead.formData)
            for fsID in facForms:
                if int(notifFormData['settingsID']) == int(fsID):
                    settingEntry = form_settings_model.objects.get(id=int(fsID))
                    formPullData = (settingEntry, unRead, notifFormData, settingEntry.formChoice.link)
                    unReadList.append(formPullData)   
    print('__________________________________________________________')
    print(unReadList)
    return {'notifCount': notifCount, 'unRead': unReadList, "read": readNotifs}
        
def createNotification(facility, user, fsID, date, notifSelector):
    createNotificationDatabase(facility, user, fsID, date, notifSelector)
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
    
def braintreeGateway():
    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            braintree.Environment.Sandbox,
            merchant_id=os.environ.get('BRAINTREE_MERCHANT_ID'),
            public_key=os.environ.get('BRAINTREE_PUBLIC_KEY'),
            private_key=os.environ.get('BRAINTREE_PRIVATE_KEY')
        )
    )
    return gateway

def getCompanyFacilities(username):
    thisProfileData = user_profile_model.objects.filter(user__username=username)[0]
    sortedFacilityData = bat_info_model.objects.filter(company__company_name=thisProfileData.company.company_name)
    
    return sortedFacilityData

def checkIfMoreRegistrations(user):
    profileData = user_profile_model.objects.get(user__id=user.id)
    braintreeData = braintree_model.objects.filter(user__id=user.id)
    userCompany = profileData.company
    listOfEmployees = user_profile_model.objects.filter(~Q(position="client"), company=userCompany, )
    if braintreeData.exists():
        braintreeData = braintreeData.get(user__id=user.id)
    else:
        print('There is no braintree entry in database for this Company/User.')
        return False
    if braintreeData.registrations:
        total_registrations = braintreeData.registrations
    else:
        print('There is no data in the database entry for this Company/User.')
        return False
    active_registrations = len(listOfEmployees.filter(is_active=True))
    if active_registrations >= total_registrations:
        addMore = False
    else:
        addMore = True

    return (total_registrations, addMore)

def issueForm_picker(facility, date, fsID):
    if date == 'form' or date == 'edit':
        return False
    parsedDate = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    issueData = issues_model.objects.filter(date__exact=parsedDate, form=str(fsID))
    if issueData.exists():
        issueData = issues_model.objects.get(date__exact=parsedDate, form=str(fsID))
    else:
        issueData = False
    return issueData

def date_change(date):
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
    parsed = month + '-' + day + '-' + str(date.year)
    return parsed

def time_change(time):
    if isinstance(time, str):
        time = str(datetime.datetime.strptime(time, "%H:%M"))[11:]
    if time:
        hourNum = int(str(time)[0:2])
        minNum = str(time)[3:5]
        timeLabel = 'AM'
        if hourNum > 12:
            newHourNum = str(hourNum - 12)
            timeLabel = 'PM'
            newTime = newHourNum + ':' + minNum + ' ' + timeLabel
        elif hourNum == 12:
            newHourNum = str(time)[0:2]
            timeLabel = 'PM'
            newTime = newHourNum + ':' + minNum + ' ' + timeLabel
        elif hourNum == 00:
            newHourNum = '12'
            newTime = newHourNum + ':' + minNum + ' ' + timeLabel
        else:
            newTime = str(hourNum) + ':' + minNum + ' ' + timeLabel
        return newTime
    else:
        print('TIME_CHANGE ERROR: no time entered')
        print('ERROR TIME ENTERED: ' + str(time))
        print('RETURNING: "-" and moving on...')
        return '-'

def date_time_change(dateTime):
    if isinstance(dateTime, str):
        dateTime = datetime.datetime.strptime(dateTime, "%Y-%m-%dT%H:%M")
        
    date = date_change(dateTime.date())
    time = time_change(dateTime.time())
    return date + ', ' + time

def road_choices(input):
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
    if input[1].isnumeric():
        answer = paved_roads[input]
    elif input[0] == 'u':
        answer = unpaved_roads[input]
    else:
        answer = parking_lots[input]
    return answer

def truck_choices(input):
    truck_choices = {
        '#5': 'Truck #5',
        '#6': 'Truck #6',
        '#7': 'Truck #7',
        '#9': 'Truck #9',
        'contractor': 'Contractor',
        'dozer': 'Dozer',
    }
    return truck_choices[input]
        
def area_choices(input):
    area_choices = {
        'panther eagle': 'Panther Eagle',
        'kepler': 'Kepler',
        'rock lick': 'Rock Lick',
        'mcclure': 'McClure',
        'elk valley': 'Elk Valley',
    }
    return area_choices[input]
    
def emptyInputs(input):
    if not input:
        this = 'N/A'
        return this
    else:
        return input
    
def quarterParse(input):
    if input == 1:
        return '1st Quarter'
    elif input == 2:
        return '2nd Quarter'
    elif input == 3:
        return '3rd Quarter'
    elif input == 4:
        return '4th Quarter'
    
def inventoryResponse(tagOn, sk):
    database = spill_kit_inventory_model.objects.filter(skID=sk)
    if tagOn == "No" and len(database) > 0:
        return "Yes"
    elif tagOn == "No" and len(database) == 0:
        return "No"
    else:
        return "N/A"      
    
def get_facility_forms(selector, facilityID):
    if selector == 'facilityName':
        facilityFormsString = facility_forms_model.objects.get(facilityChoice__facility_name=facilityID)
    elif selector == 'facilityID':
        facilityFormsString = facility_forms_model.objects.get(facilityChoice__id=facilityID)
    facilityFormsList = ast.literal_eval(facilityFormsString.formData)
    return facilityFormsList