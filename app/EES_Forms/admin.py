from django.contrib import admin # type: ignore
from .models import *
import calendar
from django.urls import reverse # type: ignore
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe # type: ignore
from .utils import EventCalendar

# Register your models here.

admin.site.register(Forms)
admin.site.register(subscription)
admin.site.register(daily_battery_profile_model)
admin.site.register(user_profile_model)
admin.site.register(form1_model)
admin.site.register(form2_model)
admin.site.register(form3_model)
admin.site.register(form4_model)
admin.site.register(form5_model)
admin.site.register(form6_model)
admin.site.register(form7_model)
admin.site.register(form8_model)
admin.site.register(form9_model)
admin.site.register(form17_model)
admin.site.register(form18_model)
admin.site.register(form19_model)
admin.site.register(form20_model)
admin.site.register(form21_model)
admin.site.register(form22_model)
admin.site.register(form22_readings_model)
admin.site.register(form24_model)
admin.site.register(form25_model)
admin.site.register(form26_model)
admin.site.register(form27_model)
admin.site.register(form28_model)
admin.site.register(formF1_model)
admin.site.register(formF2_model)
admin.site.register(formF3_model)
admin.site.register(formF4_model)
admin.site.register(formF5_model)
admin.site.register(formF6_model)
admin.site.register(formF7_model)
admin.site.register(form29_model)
admin.site.register(quarterly_trucks_model)
admin.site.register(sop_model)
admin.site.register(issues_model)
admin.site.register(facility_model)
admin.site.register(signature_model)
admin.site.register(company_model)
admin.site.register(spill_kit_inventory_model)
admin.site.register(formSubmissionRecords_model)
admin.site.register(notifications_model)
admin.site.register(braintree_model)
admin.site.register(braintreePlans)
admin.site.register(tokens_model)
admin.site.register(FAQ_model)
admin.site.register(form_requests_model)
admin.site.register(the_packets_model)
admin.site.register(form_settings_model)
admin.site.register(account_reactivation_model)
admin.site.register(form30_model)
admin.site.register(form31_model)
admin.site.register(SpillKit_model)

class EventAdmin(admin.ModelAdmin):
    list_display = ['observer', 'date', 'start_time', 'end_time', 'notes']
    change_list_template = 'supervisor/events/change_list.html'
 
    def changelist_view(self, request, extra_context=None):
        after_day = request.GET.get('date__gte', None)
        extra_context = extra_context or {}
 
        if not after_day:
            d = datetime.date.today()
            year = d
        else:
            try:
                split_after_day = after_day.split('-')
                d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
                year = d
            except:
                d = datetime.date.today()
                year = d
 
        previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
        previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
        previous_month = datetime.date(year=previous_month.year, month=previous_month.month, day=1)  # find first day of previous month
 
        last_day = calendar.monthrange(d.year, d.month)
        next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
        next_month = next_month + datetime.timedelta(days=1)  # forward a single day
        next_month = datetime.date(year=next_month.year, month=next_month.month, day=1)  # find first day of next month
        AppLabel = 'EES_Forms'
        
        extra_context['previous_month'] = reverse('admin:EES_Forms_event_changelist') + '?date__gte=' + str(previous_month)
        extra_context['next_month'] = reverse('admin:EES_Forms_event_changelist') + '?date__gte=' + str(next_month)
 
        cal = EventCalendar()
        cal.setfirstweekday(6)
        html_calendar = cal.formatmonth(d.year, d.month, year, withyear=True)
        html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
        extra_context['calendar'] = mark_safe(html_calendar)
        
        return super(EventAdmin, self).changelist_view(request, extra_context)

admin.site.register(Event, EventAdmin)
