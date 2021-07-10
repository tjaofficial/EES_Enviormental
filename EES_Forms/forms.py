from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime
from .models import *

now = datetime.datetime.now()

#Create Your Forms here

class SubFormC1(ModelForm):
    class Meta:
        model = subC
        fields = ('truck_sel', 'area_sel', 'truck_start_time', 'truck_stop_time', 'area_start_time', 'area_stop_time', 'observer', 'cert_date', 'comments', 'issues', 'cor_action', 'notified', 'time_date')
        
        widgets = {
            'date' : forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'truck_start_time' : forms.TimeInput(attrs={'class': 'input', 'type': 'time'}),
            'truck_stop_time' : forms.TimeInput(attrs={'class': 'input', 'type': 'time'}),
            'area_start_time' : forms.TimeInput(attrs={'class': 'input', 'type': 'time'}),
            'area_stop_time' : forms.TimeInput(attrs={'class': 'input', 'type': 'time'}),
        }
        
        #date = forms.DateField()
       # date.widget.attrs.update({'class': 'input'})
    
    
class FormCReadForm(ModelForm):
    class Meta:
        model = FormCReadings
        fields = ('TRead1', 'TRead2','TRead3', 'TRead4', 'TRead5', 'TRead6', 'TRead7', 'TRead8', 'TRead9', 'TRead10',  'TRead11', 'TRead12', 'ARead1', 'ARead2', 'ARead3', 'ARead4', 'ARead5', 'ARead6', 'ARead7', 'ARead8', 'ARead9', 'ARead10', 'ARead11', 'ARead12')
              
        
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','first_name', 'last_name']
        
        
class daily_battery_profile_form(ModelForm):
    class Meta:
        model = daily_battery_profile_model
        fields = ('foreman', 'crew', 'inop_ovens')
        
        widgets = {
            'inop_ovens' : forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style':'width:50px;'})
       }
       

    
class bat_info_form(ModelForm):
    class Meta:
        model = bat_info_model
        fields = ('bat_num', 'total_ovens', 'facility_name')
        
        widgets = {
            'bat_num' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'value':'5'}),
            'total_ovens' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'value':'85'}),
            'facility_name' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'value':'EES Coke Battery LLC'}),
        }
        
        
class subA5_form(ModelForm):
    class Meta:
        model = subA5_model
        fields = ('__all__')
        
        widgets = {
            'process_equip1' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 250px;'}),
            'background_color_start' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 60px;'}),
            'background_color_stop' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 60px;'}),
            'wind_speed_start' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 40px;'}),
            'wind_speed_stop' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 40px;'}),
            'emission_point_stop' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 250px;'}),
            'ambient_temp_start' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 40px;'}),
            'ambient_temp_stop' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 40px;'}),
            'plume_opacity_determined_stop' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 250px;'}),
        }
        
class subA5_readings_form(ModelForm):
    class Meta:
        model = subA5_readings_model
        fields = (
            'o1_1_reads',
            'o1_2_reads',
            'o1_3_reads',
            'o1_4_reads',
            'o1_5_reads',
            'o1_6_reads',
            'o1_7_reads',
            'o1_8_reads',
            'o1_9_reads',
            'o1_10_reads',
            'o1_11_reads',
            'o1_12_reads',
            'o1_13_reads',
            'o1_14_reads',
            'o1_15_reads',
            'o1_16_reads',
            
            'o2_1_reads',
            'o2_2_reads',
            'o2_3_reads',
            'o2_4_reads',
            'o2_5_reads',
            'o2_6_reads',
            'o2_7_reads',
            'o2_8_reads',
            'o2_9_reads',
            'o2_10_reads',
            'o2_11_reads',
            'o2_12_reads',
            'o2_13_reads',
            'o2_14_reads',
            'o2_15_reads',
            'o2_16_reads',
            
            'o3_1_reads',
            'o3_2_reads',
            'o3_3_reads',
            'o3_4_reads',
            'o3_5_reads',
            'o3_6_reads',
            'o3_7_reads',
            'o3_8_reads',
            'o3_9_reads',
            'o3_10_reads',
            'o3_11_reads',
            'o3_12_reads',
            'o3_13_reads',
            'o3_14_reads',
            'o3_15_reads',
            'o3_16_reads',
            
            'o4_1_reads',
            'o4_2_reads',
            'o4_3_reads',
            'o4_4_reads',
            'o4_5_reads',
            'o4_6_reads',
            'o4_7_reads',
            'o4_8_reads',
            'o4_9_reads',
            'o4_10_reads',
            'o4_11_reads',
            'o4_12_reads',
            'o4_13_reads',
            'o4_14_reads',
            'o4_15_reads',
            'o4_16_reads',
            'o1',
            'o1_start',
            'o1_stop',
            'o1_highest_opacity',
            'o1_instant_over_20',
            'o1_average_6',
            'o1_average_6_over_35',
            'o2',
            'o2_start',
            'o2_stop',
            'o2_highest_opacity',
            'o2_instant_over_20',
            'o2_average_6',
            'o2_average_6_over_35',
            'o3',
            'o3_start',
            'o3_stop',
            'o3_highest_opacity',
            'o3_instant_over_20',
            'o3_average_6',
            'o3_average_6_over_35',
            'o4',
            'o4_start',
            'o4_stop',
            'o4_highest_opacity',
            'o4_instant_over_20',
            'o4_average_6',
            'o4_average_6_over_35'
        )
        
        
        
        widgets = {
            'o1_1_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o1_2_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o1_3_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o1_4_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o1_5_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o1_6_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o1_7_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o1_8_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o1_9_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o1_10_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o1_11_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o1_12_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o1_13_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o1_14_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o1_15_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o1_16_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            
            'o2_1_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o2_2_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o2_3_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o2_4_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o2_5_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o2_6_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o2_7_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o2_8_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o2_9_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o2_10_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o2_11_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o2_12_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o2_13_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o2_14_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o2_15_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o2_16_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            
            'o3_1_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o3_2_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o3_3_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o3_4_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o3_5_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o3_6_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o3_7_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o3_8_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o3_9_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o3_10_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o3_11_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o3_12_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o3_13_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o3_14_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o3_15_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o3_16_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            
            'o4_1_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o4_2_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o4_3_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o4_4_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o4_5_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o4_6_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o4_7_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o4_8_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o4_9_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o4_10_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o4_11_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o4_12_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o4_13_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o4_14_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o4_15_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
            'o4_16_reads' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 50px;'}),
        }
        
    
class subA1_form(ModelForm):
    class Meta:
        model = subA1_model
        fields = (
            'observer',
            'date',
            'crew',
            'foreman',
            'start',
            'stop'
        )
        
        widgets = {
            'observer' : forms.TextInput(attrs={'type':'text', 'style':'width:150px;'}),
            'date' : forms.TextInput(attrs={'type':'text', 'style':'width:100px;'}),
            'crew' : forms.TextInput(attrs={'type':'text', 'style':'width:30px;'})
        }
        
class subA1_readings_form(ModelForm):
    class Meta:
        model = subA1_readings_model
        fields = (
            'c1_no',
            'c2_no',
            'c3_no',
            'c4_no',
            'c5_no',
            'c1_start',
            'c2_start',
            'c3_start',
            'c4_start',
            'c5_start',
            'c1_stop',
            'c2_stop',
            'c3_stop',
            'c4_stop',
            'c5_stop',
            'c1_sec',
            'c2_sec',
            'c3_sec',
            'c4_sec',
            'c5_sec',
            'c1_comments',
            'c2_comments',
            'c3_comments',
            'c4_comments',
            'c5_comments',
            'comments',
            'larry_car'
        )
        
        widgets = {
            'c1_no' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'c1_sec' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'c1_comments' : forms.TextInput(attrs={'type':'text', 'style':'width: 275px;'}),
            'c2_no' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'c2_sec' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'c2_comments' : forms.TextInput(attrs={'type':'text', 'style':'width: 275px;'}),
            'c3_no' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'c3_sec' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'c3_comments' : forms.TextInput(attrs={'type':'text', 'style':'width: 275px;'}),
            'c4_no' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'c4_sec' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'c4_comments' : forms.TextInput(attrs={'type':'text', 'style':'width: 275px;'}),
            'c5_no' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'c5_sec' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'c5_comments' : forms.TextInput(attrs={'type':'text', 'style':'width: 275px;'}),
            'comments' : Textarea(attrs={'rows':7, 'cols':125}),
            'c1_start' : forms.TextInput(attrs={'type':'text', 'style':'width: 100px;'}),
            'c2_start' : forms.TextInput(attrs={'type':'text', 'style':'width: 100px;'}),
            'c3_start' : forms.TextInput(attrs={'type':'text', 'style':'width: 100px;'}),
            'c4_start' : forms.TextInput(attrs={'type':'text', 'style':'width: 100px;'}),
            'c5_start' : forms.TextInput(attrs={'type':'text', 'style':'width: 100px;'}),
            'c1_stop' : forms.TextInput(attrs={'type':'text', 'style':'width: 100px;'}),
            'c2_stop' : forms.TextInput(attrs={'type':'text', 'style':'width: 100px;'}),
            'c3_stop' : forms.TextInput(attrs={'type':'text', 'style':'width: 100px;'}),
            'c4_stop' : forms.TextInput(attrs={'type':'text', 'style':'width: 100px;'}),
            'c5_stop' : forms.TextInput(attrs={'type':'text', 'style':'width: 100px;'}),
            'larry_car' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
        }
    
    
class user_profile_form(forms.ModelForm):
    class Meta:
        model = user_profile_model
        fields = ('cert_date',)
        
        widgets ={
            'cert_date' : forms.DateInput(attrs={'class': 'input', 'type': 'date'})
        }
        
        
class pt_admin1_form(ModelForm):
    class Meta:
        model = pt_admin1_model
        fields = ('add_days', 'days_left')
        
        
class formD_form(ModelForm):
    class Meta:
        model = formD_model
        fields = (
            'week_start',
            'week_end',
            'truck_id1',
            'date1',
            'time1',
            'contents1',
            'freeboard1',
            'wetted1',
            'comments1',
            'truck_id2',
            'date2',
            'time2',
            'contents2',
            'freeboard2',
            'wetted2',
            'comments2',
            'truck_id3',
            'date3',
            'time3',
            'contents3',
            'freeboard3',
            'wetted3',
            'comments3',
            'truck_id4',
            'date4',
            'time4',
            'contents4',
            'freeboard4',
            'wetted4',
            'comments4',
            'truck_id5',
            'date5',
            'time5',
            'contents5',
            'freeboard5',
            'wetted5',
            'comments5'
        )
        
        widgets = {
            'week_start': forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'week_end': forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'truck_id1' : forms.Select(attrs={'style':'width: 80px;'}),
            'date1' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'time1' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'contents1' : forms.Select(attrs={'style':'width: 80px;'}),
            'freeboard1' : forms.Select(attrs={'style':'width: 80px;'}),
            'wetted1' : forms.Select(attrs={'style':'width: 80px;'}),
            'comments1' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'truck_id2' : forms.Select(attrs={'style':'width: 80px;'}),
            'date2' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'time2' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'contents2' : forms.Select(attrs={'style':'width: 80px;'}),
            'freeboard2' : forms.Select(attrs={'style':'width: 80px;'}),
            'wetted2' : forms.Select(attrs={'style':'width: 80px;'}),
            'comments2' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'truck_id3' : forms.Select(attrs={'style':'width: 80px;'}),
            'date3' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'time3' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'contents3' : forms.Select(attrs={'style':'width: 80px;'}),
            'freeboard3' : forms.Select(attrs={'style':'width: 80px;'}),
            'wetted3' : forms.Select(attrs={'style':'width: 80px;'}),
            'comments3' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'truck_id4' : forms.Select(attrs={'style':'width: 80px;'}),
            'date4' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'time4' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'contents4' : forms.Select(attrs={'style':'width: 80px;'}),
            'freeboard4' : forms.Select(attrs={'style':'width: 80px;'}),
            'wetted4' : forms.Select(attrs={'style':'width: 80px;'}),
            'comments4' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'truck_id5' : forms.Select(attrs={'style':'width: 80px;'}),
            'date5' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'time5' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'contents5' : forms.Select(attrs={'style':'width: 80px;'}),
            'freeboard5' : forms.Select(attrs={'style':'width: 80px;'}),
            'wetted5' : forms.Select(attrs={'style':'width: 80px;'}),
            'comments5' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'})
        }