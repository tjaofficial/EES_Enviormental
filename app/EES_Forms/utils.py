from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import *
from datetime import datetime as dtime, date, time
#from .admin import EventAdmin


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

