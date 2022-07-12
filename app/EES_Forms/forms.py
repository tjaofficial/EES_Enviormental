from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime
from .models import *
from phonenumber_field.formfields import PhoneNumberField

now = datetime.datetime.now()

#Create Your Forms here

class SubFormC1(ModelForm):
    class Meta:
        model = formC_model
        fields = ('date', 'truck_sel', 'area_sel', 'truck_start_time', 'truck_stop_time', 'area_start_time', 'area_stop_time', 'observer', 'cert_date', 'comments', 'average_t', 'average_p')
        
        widgets = {
            'date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'truck_start_time': forms.TimeInput(attrs={'id': 'truck_start_time', 'oninput': 'timecheck_1()', 'class': 'input', 'type': 'time'}),
            'truck_stop_time': forms.TimeInput(attrs={'id': 'truck_stop_time', 'oninput': 'timecheck_1()', 'class': 'input', 'type': 'time'}),
            'area_start_time': forms.TimeInput(attrs={'id': 'area_start_time', 'oninput': 'timecheck_2()', 'class': 'input', 'type': 'time'}),
            'area_stop_time': forms.TimeInput(attrs={'id': 'area_stop_time', 'oninput': 'timecheck_2()', 'class': 'input', 'type': 'time'}),
            'truck_sel': forms.Select(attrs={'style': 'width: 100px;'}),
            'area_sel': forms.Select(attrs={'style': 'width: 130px;'}),
            'observer': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'cert_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'comments': Textarea(attrs={'rows': 7, 'cols': 125}),
            'average_t': forms.NumberInput(attrs={'id': 'average_t', 'class': 'input', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'average_p': forms.NumberInput(attrs={'id': 'average_p', 'class': 'input', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
        }

        def clean(self):
            cleaned_data = super().clean()
            start_time = cleaned_data.get("truck_start_time")
            end_time = cleaned_data.get("truck_stop_time")
            print('chciken')
            if end_time < start_time:
                raise forms.ValidationError("End time should be later than start time.")


class FormCReadForm(ModelForm):
    class Meta:
        model = formC_readings_model
        fields = ('TRead1', 'TRead2', 'TRead3', 'TRead4', 'TRead5', 'TRead6', 'TRead7', 'TRead8', 'TRead9', 'TRead10',  'TRead11', 'TRead12', 'ARead1', 'ARead2', 'ARead3', 'ARead4', 'ARead5', 'ARead6', 'ARead7', 'ARead8', 'ARead9', 'ARead10', 'ARead11', 'ARead12')
        widgets = {
            'TRead1': forms.TextInput(attrs={'id': 'TRead1', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead2': forms.TextInput(attrs={'id': 'TRead2', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead3': forms.TextInput(attrs={'id': 'TRead3', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead4': forms.TextInput(attrs={'id': 'TRead4', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead5': forms.TextInput(attrs={'id': 'TRead5', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead6': forms.TextInput(attrs={'id': 'TRead6', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead7': forms.TextInput(attrs={'id': 'TRead7', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead8': forms.TextInput(attrs={'id': 'TRead8', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead9': forms.TextInput(attrs={'id': 'TRead9', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead10': forms.TextInput(attrs={'id': 'TRead10', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead11': forms.TextInput(attrs={'id': 'TRead11', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead12': forms.TextInput(attrs={'id': 'TRead12', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead1': forms.TextInput(attrs={'id': 'ARead1', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead2': forms.TextInput(attrs={'id': 'ARead2', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead3': forms.TextInput(attrs={'id': 'ARead3', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead4': forms.TextInput(attrs={'id': 'ARead4', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead5': forms.TextInput(attrs={'id': 'ARead5', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead6': forms.TextInput(attrs={'id': 'ARead6', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead7': forms.TextInput(attrs={'id': 'ARead7', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead8': forms.TextInput(attrs={'id': 'ARead8', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead9': forms.TextInput(attrs={'id': 'ARead9', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead10': forms.TextInput(attrs={'id': 'ARead10', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead11': forms.TextInput(attrs={'id': 'ARead11', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead12': forms.TextInput(attrs={'id': 'ARead12', 'oninput': 'sumTime()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']


class daily_battery_profile_form(ModelForm):
    class Meta:
        model = daily_battery_profile_model
        fields = ('foreman', 'crew', 'inop_ovens', 'inop_numbs')

        widgets = {
            'inop_ovens': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width:50px;'}),
            'inop_numbs': forms.TextInput(attrs={'class': 'input', 'style': 'width:150px;'})
        }


class user_profile_form(forms.ModelForm):
    class Meta:
        model = user_profile_model
        fields = (
            'cert_date',
            'profile_picture',
            'phone',
            'position'
        )
        exclude = ['user']

        widgets = {
            'cert_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'profile_picture': forms.FileInput(attrs={'style': 'width: fit-content;'}),
            'phone': forms.TextInput(attrs={'type': 'tel', 'style': 'width: 150px;', 'placeholder': '+10005557777'}),
            'position': forms.Select(attrs={'style': 'width: 100px;'}),
        }


class pt_admin1_form(ModelForm):
    class Meta:
        model = pt_admin1_model
        fields = ('add_days', 'days_left')


class bat_info_form(ModelForm):
    class Meta:
        model = bat_info_model
        fields = ('bat_num', 'total_ovens', 'facility_name')

        widgets = {
            'bat_num': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'value':'5'}),
            'total_ovens': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'value':'85'}),
            'facility_name': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'value':'EES Coke Battery LLC'}),
        }


class formA1_form(ModelForm):
    class Meta:
        model = formA1_model
        fields = (
            'observer',
            'date',
            'crew',
            'foreman',
            'start',
            'stop'
        )
        
        widgets = {
            'observer': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'crew': forms.Select(attrs={'style': 'width:40px;'}),
            'foreman': forms.Select(attrs={'style': 'width: 80px;'}),
            'start': forms.TimeInput(attrs={'id': 'main_start', 'oninput': 'equal_start_stop()', 'type': 'time', 'style': 'width: 120px;'}),
            'stop': forms.TimeInput(attrs={'id': 'main_stop', 'type': 'time', 'style': 'width: 120px;'}),
        }


class formA1_readings_form(ModelForm):
    class Meta:
        model = formA1_readings_model
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
            'larry_car',
            'total_seconds'
        )

        widgets = {
            'c1_no': forms.TextInput(attrs={'id': 'c1_no', 'type': 'text', 'style': 'width: 60px; text-align: center;'}),
            'c1_sec': forms.TextInput(attrs={'id': 'c1_sec', 'oninput': 'sumTime()', 'type': 'number', 'step': '0.5', 'style': 'width: 60px; text-align: center;'}),
            'c1_comments': forms.TextInput(attrs={'type': 'text', 'style': 'width: 275px;'}),
            'c2_no': forms.TextInput(attrs={'id': 'c2_no', 'oninput': 'c2_check()', 'type': 'text', 'style': 'width: 60px; text-align: center;'}),
            'c2_sec': forms.TextInput(attrs={'id': 'c2_sec', 'oninput': 'sumTime()', 'type': 'number', 'step': '0.5', 'style': 'width: 60px; text-align: center;'}),
            'c2_comments': forms.TextInput(attrs={'type': 'text', 'style': 'width: 275px;'}),
            'c3_no': forms.TextInput(attrs={'id': 'c3_no', 'oninput': 'c3_check()', 'type': 'text', 'style': 'width: 60px; text-align: center;'}),
            'c3_sec': forms.TextInput(attrs={'id': 'c3_sec', 'oninput': 'sumTime()', 'type': 'number', 'step': '0.5', 'style': 'width: 60px; text-align: center;'}),
            'c3_comments': forms.TextInput(attrs={'type': 'text', 'style': 'width: 275px;'}),
            'c4_no': forms.TextInput(attrs={'id': 'c4_no', 'oninput': 'c4_check()', 'type': 'text', 'style': 'width: 60px; text-align: center;'}),
            'c4_sec': forms.TextInput(attrs={'id': 'c4_sec', 'oninput': 'sumTime()', 'type': 'number', 'step': '0.5', 'style': 'width: 60px; text-align: center;'}),
            'c4_comments': forms.TextInput(attrs={'type': 'text', 'style': 'width: 275px;'}),
            'c5_no': forms.TextInput(attrs={'id': 'c5_no', 'oninput': 'c5_check()', 'type': 'text', 'style': 'width: 60px; text-align: center;'}),
            'c5_sec': forms.TextInput(attrs={'id': 'c5_sec', 'oninput': 'sumTime()', 'type': 'number', 'step': '0.5', 'style': 'width: 60px; text-align: center;'}),
            'c5_comments': forms.TextInput(attrs={'type': 'text', 'style': 'width: 275px;'}),
            'comments': Textarea(attrs={'id': 'comments', 'rows': 7, 'cols': 125}),
            'c1_start': forms.TimeInput(attrs={'id': 'c1_start', 'oninput': 'timecheck_c1()', 'type': 'time', 'style': 'width: 120px;'}),
            'c2_start': forms.TimeInput(attrs={'id': 'c2_start', 'oninput': 'timecheck_c2()', 'type': 'time', 'style': 'width: 120px;'}),
            'c3_start': forms.TimeInput(attrs={'id': 'c3_start', 'oninput': 'timecheck_c3()', 'type': 'time', 'style': 'width: 120px;'}),
            'c4_start': forms.TimeInput(attrs={'id': 'c4_start', 'oninput': 'timecheck_c4()', 'type': 'time', 'style': 'width: 120px;'}),
            'c5_start': forms.TimeInput(attrs={'id': 'c5_start', 'oninput': 'timecheck_c5()', 'type': 'time', 'style': 'width: 120px;'}),
            'c1_stop': forms.TimeInput(attrs={'id': 'c1_stop', 'oninput': 'timecheck_c1()', 'type': 'time', 'style': 'width: 120px;'}),
            'c2_stop': forms.TimeInput(attrs={'id': 'c2_stop', 'oninput': 'timecheck_c2()', 'type': 'time', 'style': 'width: 120px;'}),
            'c4_stop': forms.TimeInput(attrs={'id': 'c4_stop', 'oninput': 'timecheck_c4()', 'type': 'time', 'style': 'width: 120px;'}),
            'c3_stop': forms.TimeInput(attrs={'id': 'c3_stop', 'oninput': 'timecheck_c3()', 'type': 'time', 'style': 'width: 120px;'}),
            'c5_stop': forms.TimeInput(attrs={
                'id': 'c5_stop',
                'oninput': 'timecheck_c5()',
                'onchange': 'equal_start_stop()',
                'type': 'time',
                'style': 'width: 120px;'}),
            'larry_car': forms.Select(attrs={'style': 'width: 60px;'}),
            'total_seconds': forms.TextInput(attrs={
                'id': 'total_seconds', 
                'onchange': 'sumTime()',
                'type': 'number', 
                'step': '0.5', 
                'style': 'width: 60px; text-align: center;'}),
        }


class formA2_form(ModelForm):
    class Meta:
        model = formA2_model
        fields = ('__all__')
        widgets = {
            'p_traverse_time_min': forms.NumberInput(attrs={
                'oninput': 'total_traverse()',
                'id': 'id_p_traverse_time_min',
                'type': 'number',
                'style': 'width:50px; text-align: center;'
            }),
            'p_traverse_time_sec': forms.NumberInput(attrs={
                'oninput': 'total_traverse()',
                'id': 'id_p_traverse_time_sec',
                'type': 'number',
                'style': 'width:50px; text-align: center;'
            }),
            'c_traverse_time_min': forms.NumberInput(attrs={
                'oninput': 'total_traverse()',
                'id': 'id_c_traverse_time_min',
                'type': 'number',
                'style': 'width:50px; text-align: center;'
            }),
            'c_traverse_time_sec': forms.NumberInput(attrs={
                'oninput': 'total_traverse()',
                'id': 'id_c_traverse_time_sec',
                'type': 'number',
                'style': 'width:50px; text-align: center;'
            }),
            'observer': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'inop_ovens': forms.NumberInput(attrs={'id': 'inop_ovens', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'inop_numbs': forms.TextInput(attrs={'onchange': 'pc_doors_not_observed()', 'id': 'inop_numbs', 'class': 'input', 'style': 'width:150px; text-align: center;'}),
            'crew': forms.Select(attrs={'style': 'width:40px;'}),
            'foreman': forms.Select(attrs={'style': 'width: 80px;'}),
            'p_start': forms.TimeInput(attrs={'oninput': 'timecheck_pushDoors()', 'id': 'p_start', 'type': 'time', 'style': 'width: 120px;'}),
            'p_stop': forms.TimeInput(attrs={'oninput': 'timecheck_pushDoors()', 'id': 'p_stop', 'type': 'time', 'style': 'width: 120px;'}),
            'c_start': forms.TimeInput(attrs={
                'oninput': 'timecheck_cokeDoors()',
                'id': 'c_start',
                'id': 'c_start', 'type': 'time',
                'style': 'width: 120px;'
            }),
            'c_stop': forms.TimeInput(attrs={
                'oninput': 'timecheck_cokeDoors()',
                'id': 'c_start',
                'id': 'c_stop',
                'type': 'time',
                'style': 'width: 120px;'
            }),
            'p_temp_block_from': forms.TextInput(attrs={
                'onchange': 'equation()',
                'id': 'p_temp_block_from',
                'class': 'input',
                'type': 'text',
                'style': 'width:50px; text-align: center;',
                'oninput': 'pc_doors_not_observed()'
            }),
            'p_temp_block_to': forms.TextInput(attrs={
                'onchange': 'equation()',
                'id': 'p_temp_block_to',
                'class': 'input',
                'type': 'text',
                'style': 'width:50px; text-align: center;',
                'oninput': 'pc_doors_not_observed()'
            }),
            'c_temp_block_from': forms.TextInput(attrs={
                'onchange': 'equation()',
                'id': 'c_temp_block_from',
                'class': 'input',
                'type': 'text',
                'style': 'width:50px; text-align: center;',
                'oninput': 'pc_doors_not_observed()'
            }),
            'c_temp_block_to': forms.TextInput(attrs={
                'onchange': 'equation()',
                'id': 'c_temp_block_to',
                'class': 'input',
                'type': 'text',
                'style': 'width:50px; text-align: center;',
                'oninput': 'pc_doors_not_observed()'
            }),
            'total_traverse_time': forms.NumberInput(attrs={'id': 'total_traverse_time', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'allowed_traverse_time': forms.NumberInput(attrs={'id': 'allowed_traverse_time', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'valid_run': forms.CheckboxInput(attrs={'style': 'width: 50px;'}),
            'leaking_doors': forms.NumberInput(attrs={'onchange': 'equation()', 'id': 'leaking_doors', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'doors_not_observed': forms.NumberInput(attrs={
                'onchange': 'equation()',
                'id': 'doors_not_observed',
                'class': 'input',
                'type': 'number',
                'style': 'width:50px; text-align: center;'
            }),
            'inop_doors_eq': forms.NumberInput(attrs={
                'onchange': 'equation()',
                'id': 'inop_doors_eq',
                'class': 'input',
                'type': 'number',
                'style': 'width:50px; text-align: center;'
            }),
            'percent_leaking': forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'notes': Textarea(attrs={'rows': 7, 'style': 'width: 805px;'}),
            'p_leak_data': forms.TextInput(attrs={'id': "pushSide", 'type': "hidden", 'value': "{}", 'data-resulttable': ""}),
            'c_leak_data': forms.TextInput(attrs={'id': "cokeSide", 'type': "hidden", 'value': "{}", 'data-resulttable': ""}),
        }


class formA3_form(ModelForm):
    class Meta:
        model = formA3_model
        fields = ('__all__')
        widgets = {
            'observer': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'inop_ovens': forms.NumberInput(attrs={'id': 'inop_ovens', 'class': 'input', 'type': 'number', 'style': 'width:35px; text-align: center;'}),
            'inop_numbs': forms.TextInput(attrs={'id': 'inop_numbs', 'class': 'input', 'style': 'width:150px; text-align: center;'}),
            'crew': forms.Select(attrs={'style': 'width:40px;'}),
            'foreman': forms.Select(attrs={'style': 'width: 80px;'}),
            'om_start': forms.TimeInput(attrs={'type': 'time', 'style': 'width: 120px;'}),
            'om_stop': forms.TimeInput(attrs={'type': 'time', 'style': 'width: 120px;'}),
            'l_start': forms.TimeInput(attrs={'type': 'time', 'style': 'width: 120px;'}),
            'l_stop': forms.TimeInput(attrs={'type': 'time', 'style': 'width: 120px;'}),
            'om_leak_json': forms.TextInput(attrs={'id': 'offtakes', 'type': "hidden", 'value': '{}', 'data-resulttable': ""}),
            'om_leaks2': forms.NumberInput(attrs={'onchange': 'om_equation()', 'id': 'om_leaks2', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'l_leak_json': forms.TextInput(attrs={'id': 'lids', 'type': "hidden", 'value': '{}', 'data-resulttable': ""}),
            'l_leaks2': forms.NumberInput(attrs={'onchange': 'l_equation()', 'id': 'l_leaks2', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'om_traverse_time_min': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'om_traverse_time_sec': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'l_traverse_time_min': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'l_traverse_time_sec': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'om_allowed_traverse_time': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'l_allowed_traverse_time': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'om_valid_run': forms.CheckboxInput(attrs={'style': 'width: 50px;'}),
            'l_valid_run': forms.CheckboxInput(attrs={'style': 'width: 50px;'}),
            'om_leaks': forms.NumberInput(attrs={'id': 'om_leaks', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'l_leaks': forms.NumberInput(attrs={'id': 'l_leaks', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'om_not_observed': forms.NumberInput(attrs={'id': 'om_not_observed', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'l_not_observed': forms.NumberInput(attrs={'id': 'l_not_observed', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'om_percent_leaking': forms.TextInput(attrs={'id': 'om_percent_leaking', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'l_percent_leaking': forms.TextInput(attrs={'id': 'l_percent_leaking', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'notes': Textarea(attrs={'rows': 7, 'cols': 125}),
        }


class formA4_form(ModelForm):
    class Meta:
        model = formA4_model
        fields = ('__all__')
        widgets = {
            'observer': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'crew': forms.Select(attrs={'style': 'width:40px;'}),
            'foreman': forms.Select(attrs={'style': 'width: 80px;'}),
            'main_start': forms.TimeInput(attrs={'type': 'time', 'style': 'width: 120px;'}),
            'main_stop': forms.TimeInput(attrs={'type': 'time', 'style': 'width: 120px;'}),
            'main_1': forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'main_2': forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'main_3': forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'main_4': forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'suction_main': forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'oven_leak_1': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'time_leak_1': forms.TimeInput(attrs={'type': 'time', 'style': 'width: 120px;'}),
            'date_temp_seal_leak_1': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'time_temp_seal_leak_1': forms.TimeInput(attrs={'type': 'time', 'style': 'width: 120px;'}),
            'temp_seal_by_leak_1': forms.TextInput(attrs={'type': 'text', 'style': 'width:150px;'}),
            'date_init_repair_leak_1': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'time_init_repair_leak_1': forms.TimeInput(attrs={'type': 'time', 'style': 'width: 120px;'}),
            'date_comp_repair_leak_1': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'time_comp_repair_leak_1': forms.TimeInput(attrs={'type': 'time', 'style': 'width: 120px;'}),
            'comp_by_leak_1': forms.TextInput(attrs={'type': 'text', 'style': 'width:150px;'}),
            'notes': Textarea(attrs={'rows': 7, 'cols': 125}),
        }


class formA5_form(ModelForm):
    class Meta:
        model = formA5_model
        fields = ('__all__')
        widgets = {
            'process_equip1': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 250px;'}),
            'background_color_start': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 60px; text-align: center;'}),
            'background_color_stop': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 60px; text-align: center;'}),
            'wind_speed_start': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 40px; text-align: center;'}),
            'wind_speed_stop': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 40px; text-align: center;'}),
            'emission_point_stop': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 250px;'}),
            'ambient_temp_start': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 40px; text-align: center;'}),
            'ambient_temp_stop': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 40px; text-align: center;'}),
            'plume_opacity_determined_stop': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 250px;'}),
            'humidity': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 40px; text-align: center;'}),
            'wind_direction': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 60px; text-align: center;'}),
            'sky_conditions': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 80px; text-align: center;'}),
            'date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'cert_date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'estab_no': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 80px; text-align: center;'}),
            'height_above_ground': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 40px; text-align: center;'}),
            'height_rel_observer': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 40px; text-align: center;'}),
            'distance_from': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 40px; text-align: center;'}),
            'direction_from': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'notes': Textarea(attrs={'rows': 7, 'cols': 125}),
            'observer': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'canvas': forms.TextInput(attrs={'id': 'canvas', 'type': 'hidden', 'class': 'input', 'style': 'width:50px; text-align: center;', "required": "true"})
        }


class formA5_readings_form(ModelForm):
    class Meta:
        model = formA5_readings_model
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
            'o1_instant_over_20' : forms.Select(attrs={'id': 'o1_instant_over_20', 'style': 'width: 60px;'}),
            'o2_instant_over_20' : forms.Select(attrs={'id': 'o2_instant_over_20', 'style': 'width: 60px;'}),
            'o3_instant_over_20' : forms.Select(attrs={'id': 'o3_instant_over_20', 'style': 'width: 60px;'}),
            'o4_instant_over_20' : forms.Select(attrs={'id': 'o4_instant_over_20', 'style': 'width: 60px;'}),
            'o1_average_6_over_35' : forms.Select(attrs={'id': 'o1_average_6_over_35', 'style': 'width: 60px;'}),
            'o2_average_6_over_35' : forms.Select(attrs={'id': 'o2_average_6_over_35', 'style': 'width: 60px;'}),
            'o3_average_6_over_35' : forms.Select(attrs={'id': 'o3_average_6_over_35', 'style': 'width: 60px;'}),
            'o4_average_6_over_35' : forms.Select(attrs={'id': 'o4_average_6_over_35', 'style': 'width: 60px;'}),
            'o1_highest_opacity' : forms.NumberInput(attrs={'id': 'o1_highest_opacity','class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
            'o1_average_6' : forms.NumberInput(attrs={'id': 'o1_average_6', 'class': 'input', 'type': 'number', 'style':'width: 60px; text-align: center;'}),
            'o2_highest_opacity' : forms.NumberInput(attrs={'id': 'o2_highest_opacity','class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
            'o2_average_6' : forms.NumberInput(attrs={'id': 'o2_average_6', 'class': 'input', 'type': 'number', 'style':'width: 60px; text-align: center;'}),
            'o3_highest_opacity' : forms.NumberInput(attrs={'id': 'o3_highest_opacity','class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
            'o3_average_6' : forms.NumberInput(attrs={'id': 'o3_average_6', 'class': 'input', 'type': 'number', 'style':'width: 60px; text-align: center;'}),
            'o4_highest_opacity' : forms.NumberInput(attrs={'id': 'o4_highest_opacity','class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
            'o4_average_6' : forms.NumberInput(attrs={'id': 'o4_average_6', 'class': 'input', 'type': 'number', 'style':'width: 60px; text-align: center;'}),
            'o1' : forms.NumberInput(attrs={'id' : 'o1', 'class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
            'o2' : forms.NumberInput(attrs={'id' : 'o2', 'oninput': 'pt2_check()', 'class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
            'o3' : forms.NumberInput(attrs={'id' : 'o3', 'oninput': 'pt3_check()', 'class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
            'o4' : forms.NumberInput(attrs={'id' : 'o4', 'oninput': 'pt4_check()', 'class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
            'o1_start' : forms.TimeInput(attrs={'id': 'o1_start', 'oninput': 'timecheck_1()', 'type':'time', 'style':'width: 120px;'}),
            'o1_stop' : forms.TimeInput(attrs={'id': 'o1_stop', 'oninput': 'timecheck_1()', 'type':'time', 'style':'width: 120px;'}),
            'o2_start' : forms.TimeInput(attrs={'id': 'o2_start', 'oninput': 'timecheck_2()', 'type':'time', 'style':'width: 120px;'}),
            'o2_stop' : forms.TimeInput(attrs={'id': 'o2_stop', 'oninput': 'timecheck_2()', 'type':'time', 'style':'width: 120px;'}),
            'o3_start' : forms.TimeInput(attrs={'id': 'o3_start', 'oninput': 'timecheck_3()', 'type':'time', 'style':'width: 120px;'}),
            'o3_stop' : forms.TimeInput(attrs={'id': 'o3_stop', 'oninput': 'timecheck_3()', 'type':'time', 'style':'width: 120px;'}),
            'o4_start' : forms.TimeInput(attrs={'id': 'o4_start', 'oninput': 'timecheck_4()', 'type':'time', 'style':'width: 120px;'}),
            'o4_stop' : forms.TimeInput(attrs={'id': 'o4_stop', 'oninput': 'timecheck_4()', 'type':'time', 'style':'width: 120px;'}),
            'o1_1_reads' : forms.TextInput(attrs={'id':'o1_1_reads', 'oninput':'pt_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_2_reads' : forms.TextInput(attrs={'id':'o1_2_reads', 'class': 'input', 'oninput':'pt1_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_3_reads' : forms.TextInput(attrs={'id':'o1_3_reads', 'class': 'input', 'oninput':'pt1_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_4_reads' : forms.TextInput(attrs={'id':'o1_4_reads', 'class': 'input', 'oninput':'pt1_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_5_reads' : forms.TextInput(attrs={'id':'o1_5_reads', 'class': 'input', 'oninput':'pt1_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_6_reads' : forms.TextInput(attrs={'id':'o1_6_reads', 'class': 'input', 'oninput':'pt1_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_7_reads' : forms.TextInput(attrs={'id':'o1_7_reads', 'class': 'input', 'oninput':'pt1_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_8_reads' : forms.TextInput(attrs={'id':'o1_8_reads', 'class': 'input', 'oninput':'pt1_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_9_reads' : forms.TextInput(attrs={'id':'o1_9_reads', 'class': 'input', 'oninput':'pt1_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_10_reads' : forms.TextInput(attrs={'id':'o1_10_reads', 'class': 'input', 'oninput':'pt1_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_11_reads' : forms.TextInput(attrs={'id':'o1_11_reads', 'class': 'input', 'oninput':'pt1_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_12_reads' : forms.TextInput(attrs={'id':'o1_12_reads', 'class': 'input', 'oninput':'pt1_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_13_reads' : forms.TextInput(attrs={'id':'o1_13_reads', 'class': 'input', 'oninput':'pt1_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_14_reads' : forms.TextInput(attrs={'id':'o1_14_reads', 'class': 'input', 'oninput':'pt1_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_15_reads' : forms.TextInput(attrs={'id':'o1_15_reads', 'class': 'input', 'oninput':'pt1_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_16_reads' : forms.TextInput(attrs={'id':'o1_16_reads', 'class': 'input', 'oninput':'pt1_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            
            'o2_1_reads' : forms.TextInput(attrs={'id':'o2_1_reads', 'class': 'input', 'oninput':'pt2_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_2_reads' : forms.TextInput(attrs={'id':'o2_2_reads', 'class': 'input', 'oninput':'pt2_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_3_reads' : forms.TextInput(attrs={'id':'o2_3_reads', 'class': 'input', 'oninput':'pt2_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_4_reads' : forms.TextInput(attrs={'id':'o2_4_reads', 'class': 'input', 'oninput':'pt2_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_5_reads' : forms.TextInput(attrs={'id':'o2_5_reads', 'class': 'input', 'oninput':'pt2_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_6_reads' : forms.TextInput(attrs={'id':'o2_6_reads', 'class': 'input', 'oninput':'pt2_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_7_reads' : forms.TextInput(attrs={'id':'o2_7_reads', 'class': 'input', 'oninput':'pt2_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_8_reads' : forms.TextInput(attrs={'id':'o2_8_reads', 'class': 'input', 'oninput':'pt2_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_9_reads' : forms.TextInput(attrs={'id':'o2_9_reads', 'class': 'input', 'oninput':'pt2_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_10_reads' : forms.TextInput(attrs={'id':'o2_10_reads', 'class': 'input', 'oninput':'pt2_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_11_reads' : forms.TextInput(attrs={'id':'o2_11_reads', 'class': 'input', 'oninput':'pt2_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_12_reads' : forms.TextInput(attrs={'id':'o2_12_reads', 'class': 'input', 'oninput':'pt2_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_13_reads' : forms.TextInput(attrs={'id':'o2_13_reads', 'class': 'input', 'oninput':'pt2_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_14_reads' : forms.TextInput(attrs={'id':'o2_14_reads', 'class': 'input', 'oninput':'pt2_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_15_reads' : forms.TextInput(attrs={'id':'o2_15_reads', 'class': 'input', 'oninput':'pt2_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_16_reads' : forms.TextInput(attrs={'id':'o2_16_reads', 'class': 'input', 'oninput':'pt2_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            
            'o3_1_reads' : forms.TextInput(attrs={'id':'o3_1_reads', 'class': 'input', 'oninput':'pt3_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_2_reads' : forms.TextInput(attrs={'id':'o3_2_reads', 'class': 'input', 'oninput':'pt3_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_3_reads' : forms.TextInput(attrs={'id':'o3_3_reads', 'class': 'input', 'oninput':'pt3_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_4_reads' : forms.TextInput(attrs={'id':'o3_4_reads', 'class': 'input', 'oninput':'pt3_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_5_reads' : forms.TextInput(attrs={'id':'o3_5_reads', 'class': 'input', 'oninput':'pt3_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_6_reads' : forms.TextInput(attrs={'id':'o3_6_reads', 'class': 'input', 'oninput':'pt3_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_7_reads' : forms.TextInput(attrs={'id':'o3_7_reads', 'class': 'input', 'oninput':'pt3_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_8_reads' : forms.TextInput(attrs={'id':'o3_8_reads', 'class': 'input', 'oninput':'pt3_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_9_reads' : forms.TextInput(attrs={'id':'o3_9_reads', 'class': 'input', 'oninput':'pt3_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_10_reads' : forms.TextInput(attrs={'id':'o3_10_reads', 'class': 'input', 'oninput':'pt3_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_11_reads' : forms.TextInput(attrs={'id':'o3_11_reads', 'class': 'input', 'oninput':'pt3_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_12_reads' : forms.TextInput(attrs={'id':'o3_12_reads', 'class': 'input', 'oninput':'pt3_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_13_reads' : forms.TextInput(attrs={'id':'o3_13_reads', 'class': 'input', 'oninput':'pt3_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_14_reads' : forms.TextInput(attrs={'id':'o3_14_reads', 'class': 'input', 'oninput':'pt3_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_15_reads' : forms.TextInput(attrs={'id':'o3_15_reads', 'class': 'input', 'oninput':'pt3_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_16_reads' : forms.TextInput(attrs={'id':'o3_16_reads', 'class': 'input', 'oninput':'pt3_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            
            'o4_1_reads' : forms.TextInput(attrs={'id':'o4_1_reads', 'class': 'input', 'oninput':'pt4_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_2_reads' : forms.TextInput(attrs={'id':'o4_2_reads', 'class': 'input', 'oninput':'pt4_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_3_reads' : forms.TextInput(attrs={'id':'o4_3_reads', 'class': 'input', 'oninput':'pt4_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_4_reads' : forms.TextInput(attrs={'id':'o4_4_reads', 'class': 'input', 'oninput':'pt4_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_5_reads' : forms.TextInput(attrs={'id':'o4_5_reads', 'class': 'input', 'oninput':'pt4_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_6_reads' : forms.TextInput(attrs={'id':'o4_6_reads', 'class': 'input', 'oninput':'pt4_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_7_reads' : forms.TextInput(attrs={'id':'o4_7_reads', 'class': 'input', 'oninput':'pt4_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_8_reads' : forms.TextInput(attrs={'id':'o4_8_reads', 'class': 'input', 'oninput':'pt4_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_9_reads' : forms.TextInput(attrs={'id':'o4_9_reads', 'class': 'input', 'oninput':'pt4_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_10_reads' : forms.TextInput(attrs={'id':'o4_10_reads', 'class': 'input', 'oninput':'pt4_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_11_reads' : forms.TextInput(attrs={'id':'o4_11_reads', 'class': 'input', 'oninput':'pt4_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_12_reads' : forms.TextInput(attrs={'id':'o4_12_reads', 'class': 'input', 'oninput':'pt4_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_13_reads' : forms.TextInput(attrs={'id':'o4_13_reads', 'class': 'input', 'oninput':'pt4_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_14_reads' : forms.TextInput(attrs={'id':'o4_14_reads', 'class': 'input', 'oninput':'pt4_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_15_reads' : forms.TextInput(attrs={'id':'o4_15_reads', 'class': 'input', 'oninput':'pt4_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_16_reads' : forms.TextInput(attrs={'id':'o4_16_reads', 'class': 'input', 'oninput':'pt4_averages()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        }
    
 
class formB_form(ModelForm):
    class Meta:
        today = datetime.date.today()
        name_0 = False
        name_1 = False
        name_2 = False
        name_3 = False
        name_4 = False
        sec_1 = False
        sec_2 = False
        if today.weekday() == 0:
            name_0 = True
            name_1 = False
            name_2 = False
            name_3 = False
            name_4 = False
            sec_1 = False
            sec_2 = False
        if today.weekday() == 1:
            name_0 = True
            name_1 = True
            name_2 = False
            name_3 = False
            name_4 = False
            sec_1 = False
            sec_2 = False
        if today.weekday() == 2:
            name_0 = True
            name_1 = True
            name_2 = True
            name_3 = False
            name_4 = False
            sec_1 = False
            sec_2 = False
        if today.weekday() == 3:
            name_0 = True
            name_1 = True
            name_2 = True
            name_3 = True
            name_4 = False
            sec_1 = False
            sec_2 = False
        if today.weekday() == 4:
            name_0 = True
            name_1 = True
            name_2 = True
            name_3 = True
            name_4 = True
            sec_1 = False
            sec_2 = False
            
        model = formB_model
        fields = ('__all__')
        widgets = {
            'week_start': forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'week_end': forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'observer_0' : forms.TextInput(attrs={'style':'width: 150px;', 'required': name_0}),
            'time_0' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;', 'required': name_0}),
            'weather_0' : forms.Select(attrs={'style':'width: 80px;', 'required': name_0}),
            'wind_speed_0' : forms.TextInput(attrs={'type':'text', 'style':'width: 50px; text-align: center;', 'required': name_0}),
            'fugitive_dust_observed_0' : forms.Select(attrs={'style':'width: 50px;', 'required': name_0}),
            'supressant_applied_0' : forms.Select(attrs={'style':'width: 50px;', 'required': name_0}),
            'supressant_active_0' : forms.Select(attrs={'style':'width: 50px;', 'required': name_0}),
            'working_face_exceed_0' : forms.Select(attrs={'style':'width: 50px;', 'required': name_0}),
            'spills_0' : forms.Select(attrs={'oninput':'hidden_spills()', 'style':'width: 50px;', 'required': name_0}),
            'pushed_back_0' : forms.Select(attrs={'style':'width: 50px;', 'required': name_0}),
            'coal_vessel_0' : forms.Select(attrs={'oninput':'hidden_vessel()', 'style':'width: 50px;', 'required': name_0}),
            'water_sprays_0' : forms.Select(attrs={'style':'width: 50px;', 'required': name_0}),
            'loader_lowered_0' : forms.Select(attrs={'style':'width: 50px;', 'required': name_0}),
            'working_water_sprays_0' : forms.Select(attrs={'style':'width: 50px;', 'required': name_0}),
            'barrier_thickness_0' : forms.Select(attrs={'oninput':'info_already_entered_0()', 'style':'width: 80px;', 'required': sec_1}),
            'surface_quality_0' : forms.Select(attrs={'oninput':'info_already_entered_0()', 'style':'width: 60px;', 'required': sec_1}),
            'surpressant_crust_0' : forms.Select(attrs={'oninput': 'info_already_entered_0()', 'style':'width: 50px;', 'required': sec_1}),
            'additional_surpressant_0' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;', 'required': sec_1}),
            'comments_0' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;', 'required': sec_1}),
            'wharf_0' : forms.Select(attrs={'oninput':'house_keeping_0()', 'style':'width: 80px;', 'required': sec_2}),
            'breeze_0' : forms.Select(attrs={'oninput':'house_keeping_0()', 'style':'width: 80px;', 'required': sec_2}),
            
            'observer_1' : forms.TextInput(attrs={'style':'width: 150px;', 'required': name_1}),
            'time_1' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;', 'required': name_1}),
            'weather_1' : forms.Select(attrs={'style':'width: 80px;', 'required': name_1}),
            'wind_speed_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 50px; text-align: center;', 'required': name_1}),
            'fugitive_dust_observed_1' : forms.Select(attrs={'style':'width: 50px;', 'required': name_1}),
            'supressant_applied_1' : forms.Select(attrs={'style':'width: 50px;', 'required': name_1}),
            'supressant_active_1' : forms.Select(attrs={'style':'width: 50px;', 'required': name_1}),
            'working_face_exceed_1' : forms.Select(attrs={'style':'width: 50px;', 'required': name_1}),
            'spills_1' : forms.Select(attrs={'oninput':'hidden_spills()', 'style':'width: 50px;', 'required': name_1}),
            'pushed_back_1' : forms.Select(attrs={'style':'width: 50px;', 'required': name_1}),
            'coal_vessel_1' : forms.Select(attrs={'oninput':'hidden_vessel()', 'style':'width: 50px;', 'required': name_1}),
            'water_sprays_1' : forms.Select(attrs={'style':'width: 50px;', 'required': name_1}),
            'loader_lowered_1' : forms.Select(attrs={'style':'width: 50px;', 'required': name_1}),
            'working_water_sprays_1' : forms.Select(attrs={'style':'width: 50px;', 'required': name_1}),
            'barrier_thickness_1' : forms.Select(attrs={'oninput':'info_already_entered_1()', 'style':'width: 80px;', 'required': sec_1}),
            'surface_quality_1' : forms.Select(attrs={'oninput':'info_already_entered_1()', 'style':'width: 60px;', 'required': sec_1}),
            'surpressant_crust_1' : forms.Select(attrs={'oninput':'info_already_entered_1()', 'style':'width: 50px;', 'required': sec_1}),
            'additional_surpressant_1' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;', 'required': sec_1}),
            'comments_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;', 'required': sec_1}),
            'wharf_1' : forms.Select(attrs={'oninput':'house_keeping_1()', 'style':'width: 80px;', 'required': sec_2}),
            'breeze_1' : forms.Select(attrs={'oninput':'house_keeping_1()', 'style':'width: 80px;', 'required': sec_2}),
            
            'observer_2' : forms.TextInput(attrs={'style':'width: 150px;', 'required': name_2}),
            'time_2' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;', 'required': name_2}),
            'weather_2' : forms.Select(attrs={'style':'width: 80px;', 'required': name_2}),
            'wind_speed_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 50px; text-align: center;', 'required': name_2}),
            'fugitive_dust_observed_2' : forms.Select(attrs={'style':'width: 50px;', 'required': name_2}),
            'supressant_applied_2' : forms.Select(attrs={'style':'width: 50px;', 'required': name_2}),
            'supressant_active_2' : forms.Select(attrs={'style':'width: 50px;', 'required': name_2}),
            'working_face_exceed_2' : forms.Select(attrs={'style':'width: 50px;', 'required': name_2}),
            'spills_2' : forms.Select(attrs={'oninput':'hidden_spills()', 'style':'width: 50px;', 'required': name_2}),
            'pushed_back_2' : forms.Select(attrs={'style':'width: 50px;', 'required': name_2}),
            'coal_vessel_2' : forms.Select(attrs={'oninput':'hidden_vessel()', 'style':'width: 50px;', 'required': name_2}),
            'water_sprays_2' : forms.Select(attrs={'style':'width: 50px;', 'required': name_2}),
            'loader_lowered_2' : forms.Select(attrs={'style':'width: 50px;', 'required': name_2}),
            'working_water_sprays_2' : forms.Select(attrs={'style':'width: 50px;', 'required': name_2}),
            'barrier_thickness_2' : forms.Select(attrs={'oninput':'info_already_entered_2()', 'style':'width: 80px;', 'required': sec_1}),
            'surface_quality_2' : forms.Select(attrs={'oninput':'info_already_entered_2()', 'style':'width: 60px;', 'required': sec_1}),
            'surpressant_crust_2' : forms.Select(attrs={'oninput':'info_already_entered_2()', 'style':'width: 50px;', 'required': sec_1}),
            'additional_surpressant_2' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;', 'required': sec_1}),
            'comments_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;', 'required': sec_1}),
            'wharf_2' : forms.Select(attrs={'oninput':'house_keeping_2()', 'style':'width: 80px;', 'required': sec_2}),
            'breeze_2' : forms.Select(attrs={'oninput':'house_keeping_2()', 'style':'width: 80px;', 'required': sec_2}),
            
            'observer_3' : forms.TextInput(attrs={'style':'width: 150px;', 'required': name_3}),
            'time_3' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;', 'required': name_3}),
            'weather_3' : forms.Select(attrs={'style':'width: 80px;', 'required': name_3}),
            'wind_speed_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 50px; text-align: center;', 'required': name_3}),
            'fugitive_dust_observed_3' : forms.Select(attrs={'style':'width: 50px;', 'required': name_3}),
            'supressant_applied_3' : forms.Select(attrs={'style':'width: 50px;', 'required': name_3}),
            'supressant_active_3' : forms.Select(attrs={'style':'width: 50px;', 'required': name_3}),
            'working_face_exceed_3' : forms.Select(attrs={'style':'width: 50px;', 'required': name_3}),
            'spills_3' : forms.Select(attrs={'oninput':'hidden_spills()', 'style':'width: 50px;', 'required': name_3}),
            'pushed_back_3' : forms.Select(attrs={'style':'width: 50px;', 'required': name_3}),
            'coal_vessel_3' : forms.Select(attrs={'oninput':'hidden_vessel()', 'style':'width: 50px;', 'required': name_3}),
            'water_sprays_3' : forms.Select(attrs={'style':'width: 50px;', 'required': name_3}),
            'loader_lowered_3' : forms.Select(attrs={'style':'width: 50px;', 'required': name_3}),
            'working_water_sprays_3' : forms.Select(attrs={'style':'width: 50px;', 'required': name_3}),
            'barrier_thickness_3' : forms.Select(attrs={'oninput':'info_already_entered_3()', 'style':'width: 80px;', 'required': sec_1}),
            'surface_quality_3' : forms.Select(attrs={'oninput':'info_already_entered_3()', 'style':'width: 60px;', 'required': sec_1}),
            'surpressant_crust_3' : forms.Select(attrs={'oninput':'info_already_entered_3()', 'style':'width: 50px;', 'required': sec_1}),
            'additional_surpressant_3' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;', 'required': sec_1}),
            'comments_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;', 'required': sec_1}),
            'wharf_3' : forms.Select(attrs={'oninput':'house_keeping_3()', 'style':'width: 80px;', 'required': sec_2}),
            'breeze_3' : forms.Select(attrs={'oninput':'house_keeping_3()', 'style':'width: 80px;', 'required': sec_2}),
            
            'observer_4' : forms.TextInput(attrs={'style':'width: 150px;', 'required': name_4}),
            'time_4' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;', 'required': name_4}),
            'weather_4' : forms.Select(attrs={'style':'width: 80px;', 'required': name_4}),
            'wind_speed_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 50px; text-align: center;', 'required': name_4}),
            'fugitive_dust_observed_4' : forms.Select(attrs={'style':'width: 50px;', 'required': name_4}),
            'supressant_applied_4' : forms.Select(attrs={'style':'width: 50px;', 'required': name_4}),
            'supressant_active_4' : forms.Select(attrs={'style':'width: 50px;', 'required': name_4}),
            'working_face_exceed_4' : forms.Select(attrs={'style':'width: 50px;', 'required': name_4}),
            'spills_4' : forms.Select(attrs={'oninput':'hidden_spills()', 'style':'width: 50px;', 'required': name_4}),
            'pushed_back_4' : forms.Select(attrs={'style':'width: 50px;', 'required': name_4}),
            'coal_vessel_4' : forms.Select(attrs={'oninput':'hidden_vessel()', 'style':'width: 50px;', 'required': name_4}),
            'water_sprays_4' : forms.Select(attrs={'style':'width: 50px;', 'required': name_4}),
            'loader_lowered_4' : forms.Select(attrs={'style':'width: 50px;', 'required': name_4}),
            'working_water_sprays_4' : forms.Select(attrs={'style':'width: 50px;', 'required': name_4}),
            'barrier_thickness_4' : forms.Select(attrs={'oninput':'info_already_entered_4()', 'style':'width: 80px;', 'required': sec_1}),
            'surface_quality_4' : forms.Select(attrs={'oninput':'info_already_entered_4()', 'style':'width: 60px;', 'required': sec_1}),
            'surpressant_crust_4' : forms.Select(attrs={'oninput':'info_already_entered_4()', 'style':'width: 50px;', 'required': sec_1}),
            'additional_surpressant_4' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;', 'required': sec_1}),
            'comments_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;', 'required': sec_1}),
            'wharf_4' : forms.Select(attrs={'oninput':'house_keeping_4()', 'style':'width: 80px;', 'required': sec_2}),
            'breeze_4' : forms.Select(attrs={'oninput':'house_keeping_4()', 'style':'width: 80px;', 'required': sec_2}),
        }

         
class formD_form(ModelForm):
    class Meta:
        model = formD_model
        fields = (
            'week_start',
            'week_end',
            'observer1',
            'observer2',
            'observer3',
            'observer4',
            'observer5',
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
            'time1' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'contents1' : forms.Select(attrs={'style':'width: 80px;'}),
            'freeboard1' : forms.Select(attrs={'style':'width: 80px;'}),
            'wetted1' : forms.Select(attrs={'style':'width: 80px;'}),
            'comments1' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'truck_id2' : forms.Select(attrs={'style':'width: 80px;'}),
            'date2' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'time2' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'contents2' : forms.Select(attrs={'style':'width: 80px;'}),
            'freeboard2' : forms.Select(attrs={'style':'width: 80px;'}),
            'wetted2' : forms.Select(attrs={'style':'width: 80px;'}),
            'comments2' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'truck_id3' : forms.Select(attrs={'style':'width: 80px;'}),
            'date3' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'time3' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'contents3' : forms.Select(attrs={'style':'width: 80px;'}),
            'freeboard3' : forms.Select(attrs={'style':'width: 80px;'}),
            'wetted3' : forms.Select(attrs={'style':'width: 80px;'}),
            'comments3' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'truck_id4' : forms.Select(attrs={'style':'width: 80px;'}),
            'date4' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'time4' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'contents4' : forms.Select(attrs={'style':'width: 80px;'}),
            'freeboard4' : forms.Select(attrs={'style':'width: 80px;'}),
            'wetted4' : forms.Select(attrs={'style':'width: 80px;'}),
            'comments4' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'truck_id5' : forms.Select(attrs={'style':'width: 80px;'}),
            'date5' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'time5' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'contents5' : forms.Select(attrs={'style':'width: 80px;'}),
            'freeboard5' : forms.Select(attrs={'style':'width: 80px;'}),
            'wetted5' : forms.Select(attrs={'style':'width: 80px;'}),
            'comments5' : forms.TextInput(attrs={'type':'text', 'style':'width: 60px;'}),
            'observer1' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'observer2' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'observer3' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'observer4' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'observer5' : forms.TextInput(attrs={'style':'width: 150px;'}),
        }

        
class formE_form(ModelForm):
    class Meta:
        model = formE_model
        fields = (
            'observer',
            'date',
            'crew',
            'foreman',
            'start_time',
            'end_time',
            'leaks',
            'goose_neck_data',

        )
        widgets ={
            'observer' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'crew' : forms.Select(attrs={'style':'width: 40px;'}),
            'foreman' : forms.Select(attrs={'style':'width: 80px;'}),
            'start_time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'end_time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'leaks' : forms.Select(attrs={'style':'width: 40px;'}),
            'goose_neck_data' : forms.NumberInput(attrs={'id': "gooseNeckData", 'type': "hidden", 'value': "{}", 'data-resulttable': ""})
            
        }
        
        
class formF1_form(ModelForm):
    class Meta:
        model = formF1_model
        fields = ('__all__')
        
        widgets = {
            'observer' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px;'}),
            'time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'retain_date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'status_1' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_2' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_3' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_4' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_5' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_6' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_7' : forms.Select(attrs={'style':'width: 80px;'}),
            'comments_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_5' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_6' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_7' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_5' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_6' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_7' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'containers_1' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_2' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_3' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_4' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'waste_codes_1' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_2' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_3' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_4' : forms.Select(attrs={'style':'width: 80px;'}),
            'dates_1' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_2' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_3' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_4' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
        }
        
        
class formF2_form(ModelForm):
    class Meta:
        model = formF2_model
        fields = ('__all__')
        
        widgets = {
            'observer' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px;'}),
            'time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'retain_date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'status_1' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_2' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_3' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_4' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_5' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_6' : forms.Select(attrs={'style':'width: 80px;'}),
            'comments_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_5' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_6' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_5' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_6' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'containers_1' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_2' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_3' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_4' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'waste_codes_1' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_2' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_3' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_4' : forms.Select(attrs={'style':'width: 80px;'}),
            'dates_1' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_2' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_3' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_4' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
        }

class formF3_form(ModelForm):
    class Meta:
        model = formF3_model
        fields = ('__all__')
        
        widgets = {
            'observer' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px;'}),
            'time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'retain_date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'status_1' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_2' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_3' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_4' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_5' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_6' : forms.Select(attrs={'style':'width: 80px;'}),
            'comments_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_5' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_6' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_5' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_6' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'containers_1' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_2' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_3' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_4' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'waste_codes_1' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_2' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_3' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_4' : forms.Select(attrs={'style':'width: 80px;'}),
            'dates_1' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_2' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_3' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_4' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
        }

class formF4_form(ModelForm):
    class Meta:
        model = formF4_model
        fields = ('__all__')
        
        widgets = {
            'observer' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px;'}),
            'time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'retain_date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'status_1' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_2' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_3' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_4' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_5' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_6' : forms.Select(attrs={'style':'width: 80px;'}),
            'comments_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_5' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_6' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_5' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_6' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'containers_1' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_2' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_3' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_4' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'waste_codes_1' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_2' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_3' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_4' : forms.Select(attrs={'style':'width: 80px;'}),
            'dates_1' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_2' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_3' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_4' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
        }

class formF5_form(ModelForm):
    class Meta:
        model = formF5_model
        fields = ('__all__')
        
        widgets = {
            'observer' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px;'}),
            'time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'retain_date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'status_1' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_2' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_3' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_4' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_5' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_6' : forms.Select(attrs={'style':'width: 80px;'}),
            'comments_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_5' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_6' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_5' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_6' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'containers_1' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_2' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_3' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_4' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'waste_codes_1' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_2' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_3' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_4' : forms.Select(attrs={'style':'width: 80px;'}),
            'dates_1' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_2' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_3' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_4' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
        }
class formF6_form(ModelForm):
    class Meta:
        model = formF6_model
        fields = ('__all__')
        
        widgets = {
            'observer' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px;'}),
            'time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'retain_date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'status_1' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_2' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_3' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_4' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_5' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_6' : forms.Select(attrs={'style':'width: 80px;'}),
            'comments_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_5' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_6' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_5' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_6' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'containers_1' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_2' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_3' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_4' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'waste_codes_1' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_2' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_3' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_4' : forms.Select(attrs={'style':'width: 80px;'}),
            'dates_1' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_2' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_3' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_4' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
        }
class formF7_form(ModelForm):
    class Meta:
        model = formF7_model
        fields = ('__all__')
        
        widgets = {
            'observer' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px;'}),
            'time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'retain_date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'status_1' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_2' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_3' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_4' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_5' : forms.Select(attrs={'style':'width: 80px;'}),
            'status_6' : forms.Select(attrs={'style':'width: 80px;'}),
            'comments_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_5' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'comments_6' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_5' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'action_6' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'waste_des_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'containers_1' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_2' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_3' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'containers_4' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'waste_codes_1' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_2' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_3' : forms.Select(attrs={'style':'width: 80px;'}),
            'waste_codes_4' : forms.Select(attrs={'style':'width: 80px;'}),
            'dates_1' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_2' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_3' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'dates_4' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
        }

class formG1_form(ModelForm):
    class Meta:
        model = formG1_model
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
class formG2_form(ModelForm):
    class Meta:
        model = formG2_model
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
        
class formH_form(ModelForm):
    class Meta:
        model = formH_model
        fields = ('__all__')
        
        widgets = {
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
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

        
class formI_form(ModelForm):
    class Meta:
        today = datetime.date.today()
        name_0 = False
        name_1 = False
        name_2 = False
        name_3 = False
        name_4 = False
        if today.weekday() == 0:
            name_0 = True
            name_1 = False
            name_2 = False
            name_3 = False
            name_4 = False
        if today.weekday() == 1:
            name_0 = True
            name_1 = True
            name_2 = False
            name_3 = False
            name_4 = False
        if today.weekday() == 2:
            name_0 = True
            name_1 = True
            name_2 = True
            name_3 = False
            name_4 = False
        if today.weekday() == 3:
            name_0 = True
            name_1 = True
            name_2 = True
            name_3 = True
            name_4 = False
        if today.weekday() == 4:
            name_0 = True
            name_1 = True
            name_2 = True
            name_3 = True
            name_4 = True
            
        model = formI_model
        fields = ('__all__')
        
        widgets = {
            'week_start': forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'week_end': forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'time_0' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;', 'required': name_0}),
            'time_1' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;', 'required': name_1}),
            'time_2' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;', 'required': name_2}),
            'time_3' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;', 'required': name_3}),
            'time_4' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;', 'required': name_4}),
            'obser_0' : forms.TextInput(attrs={'style':'width: 150px;', 'required': name_0 }),
            'obser_1' : forms.TextInput(attrs={'style':'width: 150px;', 'required': name_1 }),
            'obser_2' : forms.TextInput(attrs={'style':'width: 150px;', 'required': name_2 }),
            'obser_3' : forms.TextInput(attrs={'style':'width: 150px;', 'required': name_3 }),
            'obser_4' : forms.TextInput(attrs={'style':'width: 150px;', 'required': name_4 }),
        }
        
        
class formL_form(ModelForm):
    class Meta:
        today = datetime.date.today()
        name_5 = False
        name_6 = False
        name_0 = False
        name_1 = False
        name_2 = False
        name_3 = False
        name_4 = False
        if today.weekday() == 5:
            name_5 = True
            name_6 = False
            name_0 = False
            name_1 = False
            name_2 = False
            name_3 = False
            name_4 = False
        if today.weekday() == 6:
            name_5 = True
            name_6 = True
            name_0 = False
            name_1 = False
            name_2 = False
            name_3 = False
            name_4 = False
        if today.weekday() == 0:
            name_5 = True
            name_6 = True
            name_0 = True
            name_1 = False
            name_2 = False
            name_3 = False
            name_4 = False
        if today.weekday() == 1:
            name_5 = True
            name_6 = True
            name_0 = True
            name_1 = True
            name_2 = False
            name_3 = False
            name_4 = False
        if today.weekday() == 2:
            name_5 = True
            name_6 = True
            name_0 = True
            name_1 = True
            name_2 = True
            name_3 = False
            name_4 = False
        if today.weekday() == 3:
            name_5 = True
            name_6 = True
            name_0 = True
            name_1 = True
            name_2 = True
            name_3 = True
            name_4 = False
        if today.weekday() == 4:
            name_5 = True
            name_6 = True
            name_0 = True
            name_1 = True
            name_2 = True
            name_3 = True
            name_4 = True
        
        model = formL_model
        fields = ('__all__')
        
        widgets = {
            'week_start' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'week_end' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'time_0' : forms.TimeInput(attrs={'type':'time', 'style':'width: 130px;', 'required': name_0}),
            'time_1' : forms.TimeInput(attrs={'type':'time', 'style':'width: 130px;', 'required': name_1}),
            'time_2' : forms.TimeInput(attrs={'type':'time', 'style':'width: 130px;', 'required': name_2}),
            'time_3' : forms.TimeInput(attrs={'type':'time', 'style':'width: 130px;', 'required': name_3}),
            'time_4' : forms.TimeInput(attrs={'type':'time', 'style':'width: 130px;', 'required': name_4}),
            'time_5' : forms.TimeInput(attrs={'type':'time', 'style':'width: 130px;', 'required': name_5}),
            'time_6' : forms.TimeInput(attrs={'type':'time', 'style':'width: 130px;', 'required': name_6}),
            'obser_0' : forms.TextInput(attrs={'style':'width: 150px;', 'required': name_0}),
            'obser_1' : forms.TextInput(attrs={'style':'width: 150px;', 'required': name_1}),
            'obser_2' : forms.TextInput(attrs={'style':'width: 150px;', 'required': name_2}),
            'obser_3' : forms.TextInput(attrs={'style':'width: 150px;', 'required': name_3}),
            'obser_4' : forms.TextInput(attrs={'style':'width: 150px;', 'required': name_4}),
            'obser_5' : forms.TextInput(attrs={'style':'width: 150px;', 'required': name_5}),
            'obser_6' : forms.TextInput(attrs={'style':'width: 150px;', 'required': name_6}),
        }
       
class formM_form(ModelForm):
    class Meta:
        model = formM_model
        fields = (
            'date',
            'paved',
            'pav_start',
            'pav_stop',
            'unpaved',
            'unp_start',
            'unp_stop',
            'parking',
            'par_start',
            'par_stop',
            'storage',
            'sto_start',
            'sto_stop',
            'observer',
            'cert_date',
            'comments',
        )
        
        widgets = {
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'paved' : forms.Select(attrs={'style':'width: 150px;'}),
            'pav_start' : forms.TimeInput(attrs={'oninput': 'timecheck_1()', 'type':'time', 'style':'width: 120px;'}),
            'pav_stop' : forms.TimeInput(attrs={'oninput': 'timecheck_1()', 'type':'time', 'style':'width: 120px;'}),
            'unpaved' : forms.Select(attrs={'style':'width: 150px;'}),
            'unp_start' : forms.TimeInput(attrs={'oninput': 'timecheck_2()', 'type':'time', 'style':'width: 120px;'}),
            'unp_stop' : forms.TimeInput(attrs={'oninput': 'timecheck_2()', 'type':'time', 'style':'width: 120px;'}),
            'parking' : forms.Select(attrs={'style':'width: 150px;'}),
            'par_start' : forms.TimeInput(attrs={'oninput': 'timecheck_3()', 'type':'time', 'style':'width: 120px;'}),
            'par_stop' : forms.TimeInput(attrs={'oninput': 'timecheck_3()', 'type':'time', 'style':'width: 120px;'}),
            'storage' : forms.Select(attrs={'style':'width: 150px;'}),
            'sto_start' : forms.TimeInput(attrs={'oninput': 'timecheck_4()', 'type':'time', 'style':'width: 120px;'}),
            'sto_stop' : forms.TimeInput(attrs={'oninput': 'timecheck_4()', 'type':'time', 'style':'width: 120px;'}),
            'observer' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'cert_date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'comments' : Textarea(attrs={'rows':7, 'cols':125}),
        }
class formM_readings_form(ModelForm):
    class Meta:
        model = formM_readings_model
        fields = ('__all__')
        exclude = ('form',)
        widgets = {
            'pav_1' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'pav_2' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'pav_3' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'pav_4' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'pav_5' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'pav_6' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'pav_7' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'pav_8' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'pav_9' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'pav_10' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'pav_11' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'pav_12' : forms.TextInput(attrs={'oninput':'sumTime1()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'unp_1' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'unp_2' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'unp_3' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'unp_4' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'unp_5' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'unp_6' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'unp_7' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'unp_8' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'unp_9' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'unp_10' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'unp_11' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'unp_12' : forms.TextInput(attrs={'oninput':'sumTime2()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'par_1' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'par_2' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'par_3' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'par_4' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'par_5' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'par_6' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'par_7' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'par_8' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'par_9' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'par_10' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'par_11' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'par_12' : forms.TextInput(attrs={'oninput':'sumTime3()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_1' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_2' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_3' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_4' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_5' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_6' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_7' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_8' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_9' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_10' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_11' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_12' : forms.TextInput(attrs={'oninput':'sumTime4()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'pav_total' : forms.TextInput(attrs={'type':'text', 'style': 'width: 50px; text-align: center;'}),
            'unp_total' : forms.TextInput(attrs={'type':'text', 'style': 'width: 50px; text-align: center;'}),
            'par_total' : forms.TextInput(attrs={'type':'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_total' : forms.TextInput(attrs={'type':'text', 'style': 'width: 50px; text-align: center;'}),
        }
class formO_form(ModelForm):
    class Meta:
        model = formO_model
        fields = ('__all__')
        widgets = {
            'observer' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'month' : forms.TextInput(attrs={'type':'text', 'style':'width:100px; text-align: center; font-size: 1.2rem;'}),
            'date' : forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'weekend_day' : forms.Select(attrs={'style':'width: 80px;'}),
            'Q_1' : forms.Select(attrs={'style':'width: 60px;'}),
            'Q_2' : forms.Select(attrs={'style':'width: 60px;'}),
            'Q_3' : forms.Select(attrs={'style':'width: 60px;'}),
            'Q_4' : forms.Select(attrs={'style':'width: 60px;'}),
            'Q_5' : forms.Select(attrs={'style':'width: 60px;'}),
            'Q_6' : forms.Select(attrs={'style':'width: 60px;'}),
            'Q_7' : forms.Select(attrs={'style':'width: 60px;'}),
            'Q_8' : forms.Select(attrs={'style':'width: 60px;'}),
            'Q_9' : forms.Select(attrs={'style':'width: 60px;'}),
            'comments' : Textarea(attrs={'rows':5, 'cols':13,'style':'font-size: 1.2rem;'}),
            'actions_taken' : Textarea(attrs={'rows':5, 'cols':13,'style':'font-size: 1.2rem;'}),
        }
class formP_form(ModelForm):
    class Meta:
        model = formP_model
        fields = ('__all__')
        widgets = {
            'observer' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'month' : forms.TextInput(attrs={'type':'text', 'style':'width:100px; text-align: center; font-size: 1.2rem;'}),
            'date' : forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'weekend_day' : forms.Select(attrs={'style':'width: 80px;'}),
            'Q_1' : forms.Select(attrs={'style':'width: 60px;'}),
            'Q_2' : forms.Select(attrs={'style':'width: 60px;'}),
            'Q_3' : forms.Select(attrs={'style':'width: 60px;'}),
            'Q_4' : forms.Select(attrs={'style':'width: 60px;'}),
            'Q_5' : forms.Select(attrs={'style':'width: 60px;'}),
            'Q_6' : forms.Select(attrs={'style':'width: 60px;'}),
            'Q_7' : forms.Select(attrs={'style':'width: 60px;'}),
            'Q_8' : forms.Select(attrs={'style':'width: 60px;'}),
            'Q_9' : forms.Select(attrs={'style':'width: 60px;'}),
            'comments' : Textarea(attrs={'rows':5, 'cols':13,'style':'font-size: 1.2rem;'}),
            'actions_taken' : Textarea(attrs={'rows':5, 'cols':13,'style':'font-size: 1.2rem;'}),
        }
class issues_form(ModelForm):
    class Meta:
        model = issues_model
        fields = ('__all__')
        widgets = {
            'form' : forms.TextInput(attrs={'type':'text', 'style':'width:50px; text-align: center;'}),
            'issues' : Textarea(attrs={'rows':7, 'style':'width: 100%; border-radius: 18px; padding: .5rem;'}),
            'notified' : forms.TextInput(attrs={'type':'text', 'style':'width:150px; border-radius: 5px; background-color: white; border: 1px solid black; padding-left: .5rem;'}),
            'time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px; border-radius: 5px; background-color: white;'}),
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px; border-radius: 5px; background-color: white;'}),
            'cor_action' : Textarea(attrs={'rows':7, 'style':'width: 100%; border-radius: 18px; padding: .5rem;'}),
        }

class events_form(ModelForm):
    class Meta:
        model = Event
        fields = ('__all__')
        widgets = {
            'observer' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'title' : forms.Select(attrs={'style':'width: 150px;'}),
            'description' : forms.TextInput(attrs={'type':'text', 'style':'width:150px;'}),
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'start_time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'end_time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
        }
class spill_kits_form(ModelForm):
    class Meta:
        model = spill_kits_model
        fields = ('__all__')
        widgets = {
            'observer' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'month' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            
            'sk1_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk2_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk3_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk4_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk5_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk6_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk7_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk8_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk9_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk10_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk11_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk12_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk13_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk14_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk15_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk16_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk17_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk18_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk19_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk20_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk21_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            
            'skut23_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'skut24_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'skut25_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'skut26_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            'skut27_tag_on' : forms.Select(attrs={'style':'width: 50px;'}),
            
            'sk1_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk2_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk3_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk4_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk5_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk6_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk7_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk8_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk9_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk10_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk11_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk12_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk13_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk14_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk15_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk16_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk17_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk18_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk19_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk20_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'sk21_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            
            'skut23_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'skut24_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'skut25_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'skut26_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            'skut27_serial' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            
            'sk1_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk2_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk3_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk4_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk5_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk6_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk7_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk8_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk9_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk10_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk11_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk12_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk13_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk14_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk15_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk16_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk17_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk18_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk19_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk20_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'sk21_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            
            'skut23_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'skut24_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'skut25_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'skut26_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            'skut27_complete' : forms.Select(attrs={'style':'width: 50px;'}),
            
            'sk1_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk2_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk3_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk4_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk5_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk6_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk7_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk8_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk9_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk10_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk11_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk12_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk13_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk14_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk15_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk16_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk17_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk18_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk19_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk20_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk21_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            
            'skut23_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'skut24_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'skut25_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'skut26_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'skut27_report' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            
            'sk1_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk2_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk3_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk4_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk5_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk6_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk7_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk8_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk9_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk10_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk11_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk12_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk13_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk14_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk15_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk16_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk17_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk18_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk19_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk20_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'sk21_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            
            'skut23_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'skut24_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'skut25_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'skut26_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'skut27_comment' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            
        }
        
        
        
        
        
        
        
        