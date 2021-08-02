

Volumes/FS\ 1/Coding/

python3 manage.py runserver

python3 manage.py migrate

python3 manage.py shell

python3 manage.py makemigration




class subC(models.Model):
    date = models.CharField(max_length=30)
    truck_area = models.CharField(max_length=5)
    title = models.CharField(max_length=30)
    start_time = models.CharField(max_length=30)
    stop_time = models.CharField(max_length=30)
    readings = models.CharField(max_length=30)
    observer = models.CharField(max_length=30)
    cert_date = models.CharField(max_length=30)
    comments = models.CharField(max_length=30)
    issues = models.CharField(max_length=30)
    cor_action = models.CharField(max_length=30)
    notified = models.CharField(max_length=30)
    time_date = models.CharField(max_length=30)
    
     def __str__(self):
        return self.date
    
    
def tobe(request):
    return HttpResponse("Sup, Tobe")

def greet(request, name):
    return render(request, "ees_forms/dashboard.html", {
        "name": name.capitalize()
    })





'County', 'estab_num', 'equip_location', 'city', 'district', 'process_equip1', 'process_equip2', 'op_mode1', 'op_mode2







class subA5_form(ModelForm):
    class Meta:
        model = subA5_model
        fields = ('date', 'estab', 'county', 'estab_no', 'equip_loc', 'district', 'city', 'observer', 'cert_date', 'process_equip1', 'process_equip2', 'op_mode1', 'op_mode2', 'background_color_start', 'background_color_stop', 'sky_conditions', 'wind_speed_start', 'wind_speed_stop', 'wind_direction', 'emission_point_start', 'emission_point_stop', 'ambient_temp_start', 'ambient_temp_stop', 'humidity', 'height_above_ground', 'height_rel_observer', 'distance_from', 'direction_from', 'describe_emissions_start', 'describe_emissions_stop', 'emission_color_start', 'emission_color_stop', 'plume_type', 'water_drolet_present', 'water_droplet_plume', 'plume_opacity_determined_start', 'plume_opacity_determined_stop', 'describe_background_start', 'describe_background_stop', 'o1', 'o1_start', 'o1_stop', 'o1_16_reads', 'o1_highest_opacity', 'o1_instant_over_20', 'o1_average_6', 'o1_average_6_over_35', 'o2', 'o2_start', 'o2_stop', 'o2_16_reads', 'o2_highest_opacity', 'o2_instant_over_20', 'o2_average_6', 'o2_average_6_over_35', 'o3', 'o3_start', 'o3_stop', 'o3_16_reads', 'o3_highest_opacity', 'o3_instant_over_20', 'o3_average_6', 'o3_average_6_over_35', 'o4', 'o4_start', 'o4_stop', 'o4_16_reads', 'o4_highest_opacity', 'o4_instant_over_20', 'o4_average_6', 'o4_average_6_over_35')
        
        
        
        
        
        
        
        from EES_Forms.models import *
        
        
        def add_zero((x[0])):
            for stuff in hello:
                
        
        
        
        
        for x in sort:
            if len(B) == 0:
                B.append(x)
            else:    
                for y in B:
                    if y[0] == x[0]:
                        if y[1] < x[1]:
                            B.append(x)
                    else:
                        B.append(x)   
        return B
    cool = final(sort)
    print (cool)        
        
         #for item in reads:
        #form_date = item.form.date
    #    year = form_date.year
    #    month = form_date.month
    #    day = form_date.day
    #    if len(str(day)) == 1 :
    #        day = "0" + str(day)
    #    if len(str(month)) == 1 :
    #        day = "0" + str(month)
    #    base_date = (str(year) + "/" + str(month) + "/" + str(day))
    #    
    #    added_date = item.form.date + datetime.timedelta(days=91)
    #    year2 = added_date.year
    #    month2 = added_date.month
    #    day2 = added_date.day
    #    if len(str(day2)) == 1 :
    #        day = "0" + str(day2)
    #    if len(str(month2)) == 1 :
    #        day = "0" + str(month2)
    #    base_date2 = (str(year2) + "/" + str(month2) + "/" + str(day2))
    #    return redirect ('pt_admin1')
    
    #pt_data = data.reads_set.all
    #oven1 = first_log.oven1
    #oven2 = first_log.oven2 
    #oven3 = first_log.oven3
    #oven4 = first_log.oven4
    #date = first_log.date
    #MostRec = SpecOven.first
    #MostRecDate = MostRec.date
        
        
       
        
        
        
    cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
    
        
        
        
        
        
        
        lass EmployeeScheduleCalendar(HTMLCalendar):
    def formatday(self, day, weekday):
        """
          Return a day as a table cell.
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>' # day outside month
        else:
            return '<td class="%s"><a href="%s">%d</a></td>' % (self.cssclasses[weekday], weekday, day)
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
Error Codes

EES_00001 - formM_view, "formM_readings_model is Missing One to One data for formM_model, create data object with the corresponding date in admin"
EES_00002 - 
EES_00003 - 
EES_00004 - 
EES_00005 - search_forms_view, "Form-Name and access_page do not equal, not in standard format (form%-%)"
EES_00006 - search_forms_view, "Form-Name and access_page do not equal, not in standard format (form%-%)"
EES_00007 - search_form_view, "none"
EES_00008 - search_form_view, "none"
EES_00009 - search_form_view, "none"
EES_00010 - search_form_view, "none"
EES_00011 - search_form_view, "none"
EES_00012 - search_form_view, "none"
EES_00013 - search_form_view, "none"
EES_00014 - search_form_view, "none"
        
        
        