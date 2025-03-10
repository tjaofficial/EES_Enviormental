from django import forms # type: ignore
from django.forms import ModelForm, Textarea # type: ignore
from django.contrib.auth.forms import UserCreationForm, UserChangeForm # type: ignore
from django.contrib.auth.models import User # type: ignore
import datetime
from .models import *

now = datetime.datetime.now()

#Create Your Forms here

class SubFormC1(ModelForm):
    class Meta:
        model = form7_model
        fields = (
            'date', 
            'observer', 
            'cert_date', 
            'comments', 
        )
        
        widgets = {
            'date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'observer': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'cert_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'comments': Textarea(attrs={'rows': 7, 'cols': 125}),
        }


class FormCReadForm(ModelForm):
    class Meta:
        model = form7_readings_model
        fields = (
            'TRead1',
            'TRead2',
            'TRead3',
            'TRead4',
            'TRead5',
            'TRead6',
            'TRead7',
            'TRead8',
            'TRead9',
            'TRead10',
            'TRead11',
            'TRead12',
            'ARead1',
            'ARead2',
            'ARead3',
            'ARead4',
            'ARead5',
            'ARead6',
            'ARead7',
            'ARead8',
            'ARead9',
            'ARead10',
            'ARead11',
            'ARead12',
            'storage_1',
            'storage_2',
            'storage_3',
            'storage_4',
            'storage_5',
            'storage_6',
            'storage_7',
            'storage_8',
            'storage_9',
            'storage_10',
            'storage_11',
            'storage_12',
            'salt_1',
            'salt_2',
            'salt_3',
            'salt_4',
            'salt_5',
            'salt_6',
            'salt_7',
            'salt_8',
            'salt_9',
            'salt_10',
            'salt_11',
            'salt_12',
        )
        widgets = {
            'TRead1': forms.TextInput(attrs={'id': 'TRead1', 'oninput': 'truck_average(); autoFillZeros(TRead1.id);', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead2': forms.TextInput(attrs={'id': 'TRead2', 'oninput': 'truck_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead3': forms.TextInput(attrs={'id': 'TRead3', 'oninput': 'truck_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead4': forms.TextInput(attrs={'id': 'TRead4', 'oninput': 'truck_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead5': forms.TextInput(attrs={'id': 'TRead5', 'oninput': 'truck_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead6': forms.TextInput(attrs={'id': 'TRead6', 'oninput': 'truck_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead7': forms.TextInput(attrs={'id': 'TRead7', 'oninput': 'truck_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead8': forms.TextInput(attrs={'id': 'TRead8', 'oninput': 'truck_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead9': forms.TextInput(attrs={'id': 'TRead9', 'oninput': 'truck_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead10': forms.TextInput(attrs={'id': 'TRead10', 'oninput': 'truck_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead11': forms.TextInput(attrs={'id': 'TRead11', 'oninput': 'truck_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'TRead12': forms.TextInput(attrs={'id': 'TRead12', 'oninput': 'truck_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead1': forms.TextInput(attrs={'id': 'ARead1', 'oninput': 'area_average(); autoFillZeros(ARead1.id);', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead2': forms.TextInput(attrs={'id': 'ARead2', 'oninput': 'area_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead3': forms.TextInput(attrs={'id': 'ARead3', 'oninput': 'area_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead4': forms.TextInput(attrs={'id': 'ARead4', 'oninput': 'area_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead5': forms.TextInput(attrs={'id': 'ARead5', 'oninput': 'area_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead6': forms.TextInput(attrs={'id': 'ARead6', 'oninput': 'area_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead7': forms.TextInput(attrs={'id': 'ARead7', 'oninput': 'area_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead8': forms.TextInput(attrs={'id': 'ARead8', 'oninput': 'area_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead9': forms.TextInput(attrs={'id': 'ARead9', 'oninput': 'area_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead10': forms.TextInput(attrs={'id': 'ARead10', 'oninput': 'area_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead11': forms.TextInput(attrs={'id': 'ARead11', 'oninput': 'area_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'ARead12': forms.TextInput(attrs={'id': 'ARead12', 'oninput': 'area_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_1': forms.TextInput(attrs={'required': False, 'id': 'storage_1', 'oninput': 'storage_average(); autoFillZeros(storage_1.id);', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_2': forms.TextInput(attrs={'required': False, 'id': 'storage_2', 'oninput': 'storage_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_3': forms.TextInput(attrs={'required': False, 'id': 'storage_3', 'oninput': 'storage_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_4': forms.TextInput(attrs={'required': False, 'id': 'storage_4', 'oninput': 'storage_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_5': forms.TextInput(attrs={'required': False, 'id': 'storage_5', 'oninput': 'storage_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_6': forms.TextInput(attrs={'required': False, 'id': 'storage_6', 'oninput': 'storage_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_7': forms.TextInput(attrs={'required': False, 'id': 'storage_7', 'oninput': 'storage_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_8': forms.TextInput(attrs={'required': False, 'id': 'storage_8', 'oninput': 'storage_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_9': forms.TextInput(attrs={'required': False, 'id': 'storage_9', 'oninput': 'storage_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_10': forms.TextInput(attrs={'required': False, 'id': 'storage_10', 'oninput': 'storage_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_11': forms.TextInput(attrs={'required': False, 'id': 'storage_11', 'oninput': 'storage_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'storage_12': forms.TextInput(attrs={'required': False, 'id': 'storage_12', 'oninput': 'storage_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'salt_1': forms.TextInput(attrs={'required': False, 'id': 'salt_1', 'oninput': 'salt_average(); autoFillZeros(salt_1.id);', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'salt_2': forms.TextInput(attrs={'required': False, 'id': 'salt_2', 'oninput': 'salt_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'salt_3': forms.TextInput(attrs={'required': False, 'id': 'salt_3', 'oninput': 'salt_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'salt_4': forms.TextInput(attrs={'required': False, 'id': 'salt_4', 'oninput': 'salt_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'salt_5': forms.TextInput(attrs={'required': False, 'id': 'salt_5', 'oninput': 'salt_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'salt_6': forms.TextInput(attrs={'required': False, 'id': 'salt_6', 'oninput': 'salt_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'salt_7': forms.TextInput(attrs={'required': False, 'id': 'salt_7', 'oninput': 'salt_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'salt_8': forms.TextInput(attrs={'required': False, 'id': 'salt_8', 'oninput': 'salt_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'salt_9': forms.TextInput(attrs={'required': False, 'id': 'salt_9', 'oninput': 'salt_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'salt_10': forms.TextInput(attrs={'required': False, 'id': 'salt_10', 'oninput': 'salt_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'salt_11': forms.TextInput(attrs={'required': False, 'id': 'salt_11', 'oninput': 'salt_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'salt_12': forms.TextInput(attrs={'required': False, 'id': 'salt_12', 'oninput': 'salt_average()', 'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
        }

class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'username', 
            'email',
            'first_name', 
            'last_name'
        )
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Username', 'autofocus': False }),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'E-mail', 'style':'width: 15rem;'}),
            'first_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})

class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    class Meta:
        model = User
        fields = (
            'username', 
            'email', 
            'password1', 
            'password2', 
            'first_name', 
            'last_name'
        )
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Username', 'autofocus': False }),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'E-mail', 'style':'width: 15rem;'}),
            'password1': forms.TextInput(attrs={'class': 'input', 'type': 'password', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Confirm Password'}),
            'first_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})


# class daily_battery_profile_form(ModelForm):
#     class Meta:
#         model = daily_battery_profile_model
#         fields = ('foreman', 'crew', 'inop_ovens', 'inop_numbs')
        
#         widgets = {
#             'foreman': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Last Name', 'class': 'input', 'style': 'width:120px; text-align:center;'}),
#             'inop_ovens': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width:50px;'}),
#             'inop_numbs': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Ex. 1,2,3,45', 'style': 'width:150px; text-align:center;'})
#         }

class daily_battery_profile_form(ModelForm):
    class Meta:
        model = daily_battery_profile_model
        fields = ('foreman', 'crew', 'inop_ovens', 'inop_numbs')
        
        widgets = {
            'foreman': forms.TextInput(attrs={
                'id': 'foreman', 
                'type': 'text', 
                'placeholder': " ", 
                'class': 'form-control', 
                'required': True
            }),
            "crew": forms.Select(attrs={
                "class": "form-control",
                "required": True
            }),
            'inop_ovens': forms.NumberInput(attrs={
                'class': 'input', 
                'type': 'number', 
                'style': 'width:50px;'
            }),
            'inop_numbs': forms.HiddenInput(attrs={
                "id": "oven-hidden-input"
            })
        }
    
    def clean_inoperable_ovens(self):
        """Ensure the user enters at least one oven or selects 'No Inoperable Ovens'."""
        data = self.cleaned_data.get("inoperable_ovens")
        if not data or data.strip() == "":
            raise forms.ValidationError("You must enter at least one oven or select 'No Inoperable Ovens'.")
        return data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["crew"].choices = [("", "Select Crew")] + list(self.fields["crew"].choices[1:])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.inop_numbs:
            self.fields["inop_numbs"].initial = self.instance.inop_numbs


class user_profile_form(forms.ModelForm):
    class Meta:
        model = user_profile_model
        fields = (
            'cert_date',
            'profile_picture',
            'phone',
            'position',
            'company',
            'certs',
            'facilityChoice'
        )
        exclude = ['user']

        widgets = {
            'cert_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'profile_picture': forms.FileInput(attrs={'class':'input', 'style': 'width: fit-content;'}),
            'phone': forms.TextInput(attrs={'class':'input', 'oninput':"processPhone(event)", 'type': 'text', 'style': 'width: 150px;', 'placeholder': '(123)456-7890'}),
            'position': forms.Select(attrs={'class':'input', 'oninput': 'cert_date1()', 'style': 'width: 160px;'}),
            'company': forms.TextInput(attrs={'class':'input', 'type': 'text', 'style': 'width: 150px;'}),
            'certs': forms.TextInput(attrs={'class':'input', 'type': 'text', 'style': 'width: 300px;'}),
        }


class pt_admin1_form(ModelForm):
    class Meta:
        model = pt_admin1_model
        fields = ('add_days', 'days_left')


class bat_info_form(ModelForm):
    class Meta:
        model = bat_info_model
        fields = (
            'bat_num', 
            'total_ovens', 
            'facility_name', 
            'county', 
            'estab_num', 
            'equip_location', 
            'address', 
            'state', 
            'district', 
            'bat_height', 
            'bat_height_label', 
            'bat_main', 
            'bat_lids', 
            'city',
            'is_battery',
            'zipcode')

        widgets = {
            'bat_num': forms.NumberInput(attrs={'class':'input', 'type': 'number','style': 'width: 7rem;'}),
            'total_ovens': forms.NumberInput(attrs={'class':'input', 'type': 'number','style': 'width: 6rem;'}),
            'facility_name': forms.TextInput(attrs={'type': 'text', 'class':'input', 'style': 'width: 100%;'}),
            'county': forms.TextInput(attrs={'type': 'text','class':'input', 'style': 'width: 9rem;'}),
            'estab_num': forms.TextInput(attrs={'type': 'text','class':'input', 'style': ''}),
            'equip_location': forms.TextInput(attrs={'type': 'text','class':'input', 'style': ''}),
            'address': forms.TextInput(attrs={'type': 'text','class':'input', 'style': 'width:100%;'}),
            'state': forms.TextInput(attrs={'type': 'text', 'class':'input', 'placeholder':'XX', 'style': 'width: 3rem;'}),
            'district': forms.TextInput(attrs={'type': 'text','class':'input', 'style': 'width: 9rem;'}),
            'city': forms.TextInput(attrs={'type': 'text','class':'input', 'style': ''}),
            'bat_height': forms.NumberInput(attrs={'type': 'number','class':'input', 'style': 'width: 6rem;'}),
            'bat_height_label': forms.Select(attrs={'class':'input', 'style':'height: 24px;width: 81px;'}),
            'bat_main': forms.Select(attrs={'class':'input', 'style':'height: 24px;width: 81px;'}),
            'bat_lids': forms.NumberInput(attrs={'type': 'number','class':'input', 'style': 'width: 6rem;'}),
            'is_battery': forms.Select(attrs={'class':'input', 'style':'height: 24px; width: 81px;'}),
            'zipcode': forms.TextInput(attrs={'class':'input', 'style':'width: 4rem;'}),
        }


class formA1_form(ModelForm):
    class Meta:
        model = form1_model
        fields = ('__all__')
        widgets = {
            'observer': forms.TextInput(attrs={'style': 'width: 180px;'}),
            'date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'crew': forms.Select(attrs={'style': 'width:40px;'}),
            'foreman': forms.TextInput(attrs={'style': 'width: 80px;'}),
            'start': forms.TimeInput(attrs={'id': 'main_start', 'type': 'time', 'style': 'width: 120px;', "required": True}),
            'stop': forms.TimeInput(attrs={'id': 'main_stop', 'type': 'time', 'style': 'width: 120px;', "required": True}),
        }

    DEFAULT_OVENS_FIELDS = {
        'c1_no': "",
        'c2_no': "",
        'c3_no': "",
        'c4_no': "",
        'c5_no': "",
        'c1_start': "",
        'c2_start': "",
        'c3_start': "",
        'c4_start': "",
        'c5_start': "",
        'c1_stop': "",
        'c2_stop': "",
        'c3_stop': "",
        'c4_stop': "",
        'c5_stop': "",
        'c1_sec': "",
        'c2_sec': "",
        'c3_sec': "",
        'c4_sec': "",
        'c5_sec': "",
        'c1_comments': "",
        'c2_comments': "",
        'c3_comments': "",
        'c4_comments': "",
        'c5_comments': "",
        'comments': "",
        'larry_car': "",
        'total_seconds': ""
    }

    JSON_WIDGET_STYLES = {
        'c1_no': forms.NumberInput(attrs={'onchange': 'check_oven_numb()', 'min': '1', 'max': '85', 'id': 'c1_no', 'type': 'number', 'style': 'width: 60px; text-align: center;'}),
        'c1_sec': forms.NumberInput(attrs={'id': 'c1_sec', 'oninput': 'sumTime()','min': "0", 'type': 'number', 'step': '0.5', 'style': 'width: 60px; text-align: center;'}),
        'c1_comments': forms.TextInput(attrs={'type': 'text', 'style': 'width: 275px;'}),
        'c2_no': forms.NumberInput(attrs={'onchange': 'check_oven_numb()', 'min': '1', 'max': '85', 'id': 'c2_no', 'type': 'number', 'style': 'width: 60px; text-align: center;'}),
        'c2_sec': forms.NumberInput(attrs={'id': 'c2_sec', 'oninput': 'sumTime()','min': "0", 'type': 'number', 'step': '0.5', 'style': 'width: 60px; text-align: center;'}),
        'c2_comments': forms.TextInput(attrs={'type': 'text', 'style': 'width: 275px;'}),
        'c3_no': forms.NumberInput(attrs={'onchange': 'check_oven_numb()', 'min': '1', 'max': '85', 'id': 'c3_no', 'type': 'number', 'style': 'width: 60px; text-align: center;'}),
        'c3_sec': forms.NumberInput(attrs={'id': 'c3_sec', 'oninput': 'sumTime()','min': "0", 'type': 'number', 'step': '0.5', 'style': 'width: 60px; text-align: center;'}),
        'c3_comments': forms.TextInput(attrs={'type': 'text', 'style': 'width: 275px;'}),
        'c4_no': forms.NumberInput(attrs={'onchange': 'check_oven_numb()', 'min': '1', 'max': '85', 'id': 'c4_no', 'type': 'number', 'style': 'width: 60px; text-align: center;'}),
        'c4_sec': forms.NumberInput(attrs={'id': 'c4_sec', 'oninput': 'sumTime()','min': "0", 'type': 'number', 'step': '0.5', 'style': 'width: 60px; text-align: center;'}),
        'c4_comments': forms.TextInput(attrs={'type': 'text', 'style': 'width: 275px;'}),
        'c5_no': forms.NumberInput(attrs={'onchange': 'check_oven_numb()', 'min': '1', 'max': '85', 'id': 'c5_no', 'type': 'number', 'style': 'width: 60px; text-align: center;'}),
        'c5_sec': forms.NumberInput(attrs={'id': 'c5_sec', 'oninput': 'sumTime()','min': "0", 'type': 'number', 'step': '0.5', 'style': 'width: 60px; text-align: center;'}),
        'c5_comments': forms.TextInput(attrs={'type': 'text', 'style': 'width: 275px;'}),
        'comments': Textarea(attrs={'id': 'comments', 'rows': 7, 'cols': 125, 'oninput': 'check_oven_numb()'}),
        'c1_start': forms.TimeInput(attrs={'id': 'c1_start', 'oninput': 'timecheck_c1()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'c2_start': forms.TimeInput(attrs={'id': 'c2_start', 'oninput': 'timecheck_c2()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'c3_start': forms.TimeInput(attrs={'id': 'c3_start', 'oninput': 'timecheck_c3()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'c4_start': forms.TimeInput(attrs={'id': 'c4_start', 'oninput': 'timecheck_c4()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'c5_start': forms.TimeInput(attrs={'id': 'c5_start', 'oninput': 'timecheck_c5()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'c1_stop': forms.TimeInput(attrs={'id': 'c1_stop', 'oninput': 'timecheck_c1()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'c2_stop': forms.TimeInput(attrs={'id': 'c2_stop', 'oninput': 'timecheck_c2()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'c3_stop': forms.TimeInput(attrs={'id': 'c3_stop', 'oninput': 'timecheck_c3()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'c4_stop': forms.TimeInput(attrs={'id': 'c4_stop', 'oninput': 'timecheck_c4()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'c5_stop': forms.TimeInput(attrs={
            'id': 'c5_stop',
            'oninput': 'timecheck_c5()',
            'onchange': 'equal_start_stop()',
            'type': 'time',
            'style': 'width: 130px;',
            "required": True}),
        'larry_car': forms.Select(
            attrs={'style': 'width: 60px;'}
        ),
        'total_seconds': forms.NumberInput(attrs={
            'id': 'total_seconds', 
            'oninput': 'sumTime()',
            'min': '0',
            'readonly': True,
            'type': 'number', 
            'step': '0.5', 
            'style': 'width: 60px; text-align: center;'}),
    }

    def __init__(self, *args, **kwargs):
        """ Extract JSON values and create dynamic form fields with the correct styles. """
        super().__init__(*args, **kwargs)

        initial = kwargs.get("initial", {}) or {}  # Prevent NoneType error
        # Extract related facility settings
        related_facility = initial.get("formSettings") if isinstance(initial, dict) and "formSettings" in initial else None

        # Handle case where `instance` is available but `initial` is not
        instance = kwargs.get("instance")
        existing_data = instance.ovens_data if instance and instance.ovens_data else {}
        if not related_facility and instance:
            related_facility = getattr(instance, "formSettings", None)

        # Fetch `larry_car` quantity from the settings
        larry_cars = []
        if related_facility and hasattr(related_facility, "settings"):
            larry_cars = [
                (str(car), str(car))
                for car in range(1, int(related_facility.settings.get("settings", {}).get("larry_car_quantity", 0)) + 1)
            ]

        # **🛠️ Fix: Always re-add choices on POST requests**  
        if not larry_cars:  # If we didn't get settings, default to at least one option
            larry_cars = [("1", "1"), ("2", "2")]

        print("🚀 Larry Car Choices (final):", larry_cars)

        # **Ensure `larry_car` exists in form fields for POST handling**
        self.fields["larry_car"] = forms.ChoiceField(
            choices=[("", "Select a Larry Car")] + larry_cars,
            required=False,
            widget=self.JSON_WIDGET_STYLES.get("larry_car", forms.TextInput(attrs={"class": "input"}))
        )

        print("🚀 Existing fields AFTER adding `larry_car`:", list(self.fields.keys()))

        # **Handling Oven Data**
        for i in range(1, 6):  # Assuming max 5 ovens
            charge_key = f"charge_{i}"
            oven_values = existing_data.get(charge_key, {})

            oven_fields = {
                f"c{i}_no": oven_values.get(f"c{i}_no", ""),
                f"c{i}_start": oven_values.get(f"c{i}_start", ""),
                f"c{i}_stop": oven_values.get(f"c{i}_stop", ""),
                f"c{i}_sec": oven_values.get(f"c{i}_sec", ""),
                f"c{i}_comments": oven_values.get(f"c{i}_comments", ""),
            }

            # Assign fields dynamically to form
            for field_name, value in oven_fields.items():
                widget = self.JSON_WIDGET_STYLES.get(field_name, forms.TextInput(attrs={"class": "input"}))
                self.fields[field_name] = forms.CharField(
                    initial=value,
                    required=False,
                    widget=widget
                )

        # **Handle Extra Fields (`comments`, `larry_car`, `total_seconds`)**
        self.fields["comments"] = forms.CharField(
            initial=existing_data.get("comments", ""),
            required=False,
            widget=self.JSON_WIDGET_STYLES.get("comments", forms.TextInput(attrs={"class": "input"}))
        )

        # self.fields["larry_car"] = forms.ChoiceField(
        #     choices=[("", "Select a Larry Car")] + larry_car_choices,
        #     initial=str(existing_data.get("larry_car", "")),
        #     required=False,
        #     widget=self.JSON_WIDGET_STYLES.get("larry_car", forms.TextInput(attrs={"class": "input"}))
        # )

        self.fields["total_seconds"] = forms.FloatField(
            initial=existing_data.get("total_seconds", ""),
            required=False,
            widget=self.JSON_WIDGET_STYLES.get("total_seconds", forms.TextInput(attrs={"class": "input"}))
        )

class formA1_readings_form(ModelForm):
    class Meta:
        model = form1_readings_model
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
            'c1_no': forms.NumberInput(attrs={'onchange': 'check_oven_numb()', 'min': '1', 'max': '85', 'id': 'c1_no', 'type': 'number', 'style': 'width: 60px; text-align: center;'}),
            'c1_sec': forms.NumberInput(attrs={'id': 'c1_sec', 'oninput': 'sumTime()','min': "0", 'type': 'number', 'step': '0.5', 'style': 'width: 60px; text-align: center;'}),
            'c1_comments': forms.TextInput(attrs={'type': 'text', 'style': 'width: 275px;'}),
            'c2_no': forms.NumberInput(attrs={'onchange': 'check_oven_numb()', 'min': '1', 'max': '85', 'id': 'c2_no', 'type': 'number', 'style': 'width: 60px; text-align: center;'}),
            'c2_sec': forms.NumberInput(attrs={'id': 'c2_sec', 'oninput': 'sumTime()','min': "0", 'type': 'number', 'step': '0.5', 'style': 'width: 60px; text-align: center;'}),
            'c2_comments': forms.TextInput(attrs={'type': 'text', 'style': 'width: 275px;'}),
            'c3_no': forms.NumberInput(attrs={'onchange': 'check_oven_numb()', 'min': '1', 'max': '85', 'id': 'c3_no', 'type': 'number', 'style': 'width: 60px; text-align: center;'}),
            'c3_sec': forms.NumberInput(attrs={'id': 'c3_sec', 'oninput': 'sumTime()','min': "0", 'type': 'number', 'step': '0.5', 'style': 'width: 60px; text-align: center;'}),
            'c3_comments': forms.TextInput(attrs={'type': 'text', 'style': 'width: 275px;'}),
            'c4_no': forms.NumberInput(attrs={'onchange': 'check_oven_numb()', 'min': '1', 'max': '85', 'id': 'c4_no', 'type': 'number', 'style': 'width: 60px; text-align: center;'}),
            'c4_sec': forms.NumberInput(attrs={'id': 'c4_sec', 'oninput': 'sumTime()','min': "0", 'type': 'number', 'step': '0.5', 'style': 'width: 60px; text-align: center;'}),
            'c4_comments': forms.TextInput(attrs={'type': 'text', 'style': 'width: 275px;'}),
            'c5_no': forms.NumberInput(attrs={'onchange': 'check_oven_numb()', 'min': '1', 'max': '85', 'id': 'c5_no', 'type': 'number', 'style': 'width: 60px; text-align: center;'}),
            'c5_sec': forms.NumberInput(attrs={'id': 'c5_sec', 'oninput': 'sumTime()','min': "0", 'type': 'number', 'step': '0.5', 'style': 'width: 60px; text-align: center;'}),
            'c5_comments': forms.TextInput(attrs={'type': 'text', 'style': 'width: 275px;'}),
            'comments': Textarea(attrs={'id': 'comments', 'rows': 7, 'cols': 125, 'oninput': 'check_oven_numb()'}),
            'c1_start': forms.TimeInput(attrs={'id': 'c1_start', 'oninput': 'timecheck_c1()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
            'c2_start': forms.TimeInput(attrs={'id': 'c2_start', 'oninput': 'timecheck_c2()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
            'c3_start': forms.TimeInput(attrs={'id': 'c3_start', 'oninput': 'timecheck_c3()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
            'c4_start': forms.TimeInput(attrs={'id': 'c4_start', 'oninput': 'timecheck_c4()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
            'c5_start': forms.TimeInput(attrs={'id': 'c5_start', 'oninput': 'timecheck_c5()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
            'c1_stop': forms.TimeInput(attrs={'id': 'c1_stop', 'oninput': 'timecheck_c1()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
            'c2_stop': forms.TimeInput(attrs={'id': 'c2_stop', 'oninput': 'timecheck_c2()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
            'c3_stop': forms.TimeInput(attrs={'id': 'c3_stop', 'oninput': 'timecheck_c3()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
            'c4_stop': forms.TimeInput(attrs={'id': 'c4_stop', 'oninput': 'timecheck_c4()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
            'c5_stop': forms.TimeInput(attrs={
                'id': 'c5_stop',
                'oninput': 'timecheck_c5()',
                'onchange': 'equal_start_stop()',
                'type': 'time',
                'style': 'width: 130px;',
                "required": True}),
            'larry_car': forms.Select(attrs={'style': 'width: 60px;'}),
            'total_seconds': forms.NumberInput(attrs={
                'id': 'total_seconds', 
                'oninput': 'sumTime()',
                'min': '0',
                'readonly': True,
                'type': 'number', 
                'step': '0.5', 
                'style': 'width: 60px; text-align: center;'}),
        }
    

class formA2_form(ModelForm):
    class Meta:
        model = form2_model
        fields = ('__all__')
        widgets = {
            'p_traverse_time_min': forms.NumberInput(attrs={
                'oninput': 'total_traverse()',
                'id': 'id_p_traverse_time_min',
                'type': 'number',
                'style': 'width:50px; text-align: center;',
                'min': '0'
            }),
            'p_traverse_time_sec': forms.NumberInput(attrs={
                'oninput': 'total_traverse()',
                'id': 'id_p_traverse_time_sec',
                'type': 'number',
                'style': 'width:50px; text-align: center;',
                'min': '0'
            }),
            'c_traverse_time_min': forms.NumberInput(attrs={
                'oninput': 'total_traverse()',
                'id': 'id_c_traverse_time_min',
                'type': 'number',
                'style': 'width:50px; text-align: center;',
                'min': '0'
            }),
            'c_traverse_time_sec': forms.NumberInput(attrs={
                'oninput': 'total_traverse()',
                'id': 'id_c_traverse_time_sec',
                'type': 'number',
                'style': 'width:50px; text-align: center;',
                'min': '0'
            }),
            'observer': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'inop_ovens': forms.NumberInput(attrs={'oninput': 'inoperable_ovens()', 'id': 'inop_ovens', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'inop_numbs': forms.TextInput(attrs={'onchange': 'pc_doors_not_observed()', 'oninput':'inoperable_ovens()', 'id': 'inop_numbs', 'class': 'input', 'style': 'width:150px; text-align: center;'}),
            'crew': forms.Select(attrs={'style': 'width:40px;'}),
            'foreman': forms.TextInput(attrs={'style': 'width: 80px;'}),
            'p_start': forms.TimeInput(attrs={'oninput': 'timecheck_pushDoors()', 'id': 'p_start', 'type': 'time', 'style': 'width: 120px;', 'required': True}),
            'p_stop': forms.TimeInput(attrs={'oninput': 'timecheck_pushDoors()', 'id': 'p_stop', 'type': 'time', 'style': 'width: 120px;', 'required': True}),
            'c_start': forms.TimeInput(attrs={
                'oninput': 'timecheck_cokeDoors()',
                'id': 'c_start',
                'id': 'c_start', 'type': 'time',
                'style': 'width: 120px;', 
                'required': True
            }),
            'c_stop': forms.TimeInput(attrs={
                'oninput': 'timecheck_cokeDoors()',
                'id': 'c_start',
                'id': 'c_stop',
                'type': 'time',
                'style': 'width: 120px;',
                'required': True
            }),
            'p_temp_block_from': forms.NumberInput(attrs={
                'onchange': 'equation()',
                'id': 'p_temp_block_from',
                'class': 'input',
                'type': 'text',
                'style': 'width:50px; text-align: center;',
                'oninput': 'pc_doors_not_observed()',
                'min': "1",
                'max': "85"
            }),
            'p_temp_block_to': forms.TextInput(attrs={
                'onchange': 'equation()',
                'id': 'p_temp_block_to',
                'class': 'input',
                'type': 'text',
                'style': 'width:50px; text-align: center;',
                'oninput': 'pc_doors_not_observed()',
                'min': "1",
                'max': "85"
            }),
            'c_temp_block_from': forms.TextInput(attrs={
                'onchange': 'equation()',
                'id': 'c_temp_block_from',
                'class': 'input',
                'type': 'text',
                'style': 'width:50px; text-align: center;',
                'oninput': 'pc_doors_not_observed()',
                'min': "1",
                'max': "85"
            }),
            'c_temp_block_to': forms.TextInput(attrs={
                'onchange': 'equation()',
                'id': 'c_temp_block_to',
                'class': 'input',
                'type': 'text',
                'style': 'width:50px; text-align: center;',
                'oninput': 'pc_doors_not_observed()',
                'min': "1",
                'max': "85"
            }),
            'total_traverse_time': forms.NumberInput(attrs={
                'id': 'total_traverse_time', 
                'class': 'input', 
                'type': 'number', 
                'style': 'width:50px; text-align: center;',
                'min': '0'
            }),
            'allowed_traverse_time': forms.NumberInput(attrs={
                'id': 'allowed_traverse_time', 
                'class': 'input', 
                'type': 'number', 
                'style': 'width:50px; text-align: center;', 
                'min': '0'
            }),
            'valid_run': forms.CheckboxInput(attrs={'style': 'width: 50px;'}),
            'leaking_doors': forms.NumberInput(attrs={'onchange': 'equation()', 'id': 'leaking_doors', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;', 'min': '0'}),
            'doors_not_observed': forms.NumberInput(attrs={
                'onchange': 'equation()',
                'id': 'doors_not_observed',
                'class': 'input',
                'type': 'number',
                'style': 'width:50px; text-align: center;',
                'min': '0'
            }),
            'inop_doors_eq': forms.NumberInput(attrs={
                'onchange': 'equation()',
                'id': 'inop_doors_eq',
                'class': 'input',
                'type': 'number',
                'style': 'width:50px; text-align: center;',
                'min': '0'
            }),
            'percent_leaking': forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;', 'min': '0'}),
            'notes': Textarea(attrs={'rows': 7, 'style': 'width: 805px;'}),
            'p_leak_data': forms.TextInput(attrs={'id': "pushSide", 'type': "hidden", 'value': "{}", 'data-resulttable': ""}),
            'c_leak_data': forms.TextInput(attrs={'id': "cokeSide", 'type': "hidden", 'value': "{}", 'data-resulttable': ""}),
        }


class formA3_form(ModelForm):
    class Meta:
        model = form3_model
        fields = ('__all__')
        widgets = {
            'observer': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'inop_ovens': forms.NumberInput(attrs={'oninput':'inoperable_ovens()', 'id': 'inop_ovens', 'class': 'input', 'type': 'number', 'style': 'width:35px; text-align: center;'}),
            'inop_numbs': forms.TextInput(attrs={'oninput':'inoperable_ovens(); check_dampered_inoperable(this, "none", "none")', 'id': 'inop_numbs', 'class': 'input', 'style': 'width:150px; text-align: center;'}),
            'crew': forms.Select(attrs={'style': 'width:40px;'}),
            'foreman': forms.TextInput(attrs={'style': 'width: 80px;'}),
            'om_start': forms.TimeInput(attrs={'oninput': 'offtake_time()', 'type': 'time', 'style': 'width: 120px;', 'required': True}),
            'om_stop': forms.TimeInput(attrs={'oninput': 'offtake_time()', 'type': 'time', 'style': 'width: 120px;', 'required': True}),
            'l_start': forms.TimeInput(attrs={'oninput': 'lid_time()', 'type': 'time', 'style': 'width: 120px;', 'required': True}),
            'l_stop': forms.TimeInput(attrs={'oninput': 'lid_time()', 'type': 'time', 'style': 'width: 120px;', 'required': True}),
            'om_leak_json': forms.TextInput(attrs={'id': 'offtakes', 'type': "hidden", 'value': '{}', 'data-resulttable': ""}),
            'om_leaks2': forms.NumberInput(attrs={'onchange': 'om_equation()', 'id': 'om_leaks2', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'l_leak_json': forms.TextInput(attrs={'id': 'lids', 'type': "hidden", 'value': '{}', 'data-resulttable': ""}),
            'l_leaks2': forms.NumberInput(attrs={'onchange': 'l_equation()', 'id': 'l_leaks2', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;'}),
            'om_traverse_time_min': forms.NumberInput(attrs={'oninput':'total_time("offtakes")', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;', 'required': True, 'min': "0"}),
            'om_traverse_time_sec': forms.NumberInput(attrs={'oninput':'total_time("offtakes")', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;', 'required': True, 'min': "1"}),
            'om_total_sec': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;', 'required': True, 'min': "1"}),
            'l_traverse_time_min': forms.NumberInput(attrs={'oninput':'total_time("lids")', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;', 'required': True, 'min': "0"}),
            'l_traverse_time_sec': forms.NumberInput(attrs={'oninput':'total_time("lids")', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;', 'required': True, 'min': "1"}),
            'l_total_sec': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;', 'required': True, 'min': "1"}),
            'om_allowed_traverse_time': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;', 'required': True, 'min': "0"}),
            'l_allowed_traverse_time': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;', 'required': True, 'min': "0"}),
            'om_valid_run': forms.CheckboxInput(attrs={'style': 'width: 50px;', 'required': True}),
            'l_valid_run': forms.CheckboxInput(attrs={'style': 'width: 50px;', 'required': True}),
            'om_leaks': forms.NumberInput(attrs={'id': 'om_leaks', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;', 'min': "0"}),
            'l_leaks': forms.NumberInput(attrs={'id': 'l_leaks', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;', 'min': "0"}),
            'om_not_observed': forms.NumberInput(attrs={'id': 'om_not_observed', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;', 'min': "0"}),
            'l_not_observed': forms.NumberInput(attrs={'id': 'l_not_observed', 'class': 'input', 'type': 'number', 'style': 'width:50px; text-align: center;', 'min': "0"}),
            'om_percent_leaking': forms.TextInput(attrs={'id': 'om_percent_leaking', 'type': 'number', 'step': '0.001', 'style': 'width: 50px; text-align: center;', 'min': "0"}),
            'l_percent_leaking': forms.TextInput(attrs={'id': 'l_percent_leaking', 'type': 'number', 'step': '0.001', 'style': 'width: 50px; text-align: center;', 'min': "0"}),
            'one_pass': forms.CheckboxInput(attrs={'onchange': 'one_pass_func()', 'style': 'width: 20px;', 'initial': 'false'}),
            'notes': Textarea(attrs={'rows': 7, 'cols': 125}),
        }


class formA4_form(ModelForm):
    class Meta:
        model = form4_model
        fields = ('__all__')
        widgets = {
            'observer': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'crew': forms.Select(attrs={'style': 'width:40px;'}),
            'foreman': forms.TextInput(attrs={'style': 'width: 80px;'}),
            'main_start': forms.TimeInput(attrs={'type': 'time', 'style': 'width: 120px;', 'required': True}),
            'main_stop': forms.TimeInput(attrs={'type': 'time', 'style': 'width: 120px;', 'required': True}),
            'main_1': forms.NumberInput(attrs={'type': 'number', 'step': "0.001",  'style': 'width: 50px; text-align: center;'}),
            'main_2': forms.NumberInput(attrs={'type': 'number', 'step': "0.001",  'style': 'width: 50px; text-align: center;'}),
            'main_3': forms.NumberInput(attrs={'type': 'number', 'step': "0.001",  'style': 'width: 50px; text-align: center;'}),
            'main_4': forms.NumberInput(attrs={'type': 'number', 'step': "0.001",  'style': 'width: 50px; text-align: center;'}),
            'suction_main': forms.NumberInput(attrs={'type': 'number', 'step': "0.001",  'style': 'width: 50px; text-align: center;'}),
            'notes': forms.Textarea(attrs={'rows': 7, 'cols': 125}),
            'leak_data': forms.TextInput(attrs={'id': "collection", 'type': "hidden", 'value': "{}", 'data-resulttable': ""}),
        }


class formA5_form(ModelForm):
    class Meta:
        model = form5_model
        fields = ('__all__')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'cert_date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'estab_no': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 80px; text-align: center;'}),
            'notes': Textarea(attrs={'rows': 7, 'cols': 125, 'style': 'padding: 10px;'}),
            'observer': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'canvas': forms.TextInput(attrs={'id': 'canvas', 'type': 'hidden', 'class': 'input', 'style': 'width:50px; text-align: center;', "required": "true"})
        }
    # Define default expected JSON fields
    DEFAULT_READING_FIELDS = {
        "process_equip1": "",
        "process_equip2": "",
        "op_mode1": "normal",
        "op_mode2": "normal",
        "background_color_start": "",
        "background_color_stop": "",
        "sky_conditions": "",
        "wind_speed_start": "",
        "wind_speed_stop": "",
        "wind_direction": "",
        "emission_point_start": "",
        "emission_point_stop": "",
        "ambient_temp_start": "",
        "ambient_temp_stop": "",
        "humidity": "",
        "height_above_ground": "",
        "height_rel_observer": "",
        "distance_from": "",
        "direction_from": "",
        "describe_emissions_start": "",
        "describe_emissions_stop": "",
        "emission_color_start": "",
        "emission_color_stop": "",
        "plume_type": "",
        "water_drolet_present": "",
        "water_droplet_plume": "",
        "plume_opacity_determined_start": "",
        "plume_opacity_determined_stop": "",
        "describe_background_start": "",
        "describe_background_stop": "",
        "o1_1_reads": "",
        'o1_2_reads': "",
        'o1_3_reads': "",
        'o1_4_reads': "",
        'o1_5_reads': "",
        'o1_6_reads': "",
        'o1_7_reads': "",
        'o1_8_reads': "",
        'o1_9_reads': "",
        'o1_10_reads': "",
        'o1_11_reads': "",
        'o1_12_reads': "",
        'o1_13_reads': "",
        'o1_14_reads': "",
        'o1_15_reads': "",
        'o1_16_reads': "",
        'o2_1_reads': "",
        'o2_2_reads': "",
        'o2_3_reads': "",
        'o2_4_reads': "",
        'o2_5_reads': "",
        'o2_6_reads': "",
        'o2_7_reads': "",
        'o2_8_reads': "",
        'o2_9_reads': "",
        'o2_10_reads': "",
        'o2_11_reads': "",
        'o2_12_reads': "",
        'o2_13_reads': "",
        'o2_14_reads': "",
        'o2_15_reads': "",
        'o2_16_reads': "",
        'o3_1_reads': "",
        'o3_2_reads': "",
        'o3_3_reads': "",
        'o3_4_reads': "",
        'o3_5_reads': "",
        'o3_6_reads': "",
        'o3_7_reads': "",
        'o3_8_reads': "",
        'o3_9_reads': "",
        'o3_10_reads': "",
        'o3_11_reads': "",
        'o3_12_reads': "",
        'o3_13_reads': "",
        'o3_14_reads': "",
        'o3_15_reads': "",
        'o3_16_reads': "",
        'o4_1_reads': "",
        'o4_2_reads': "",
        'o4_3_reads': "",
        'o4_4_reads': "",
        'o4_5_reads': "",
        'o4_6_reads': "",
        'o4_7_reads': "",
        'o4_8_reads': "",
        'o4_9_reads': "",
        'o4_10_reads': "",
        'o4_11_reads': "",
        'o4_12_reads': "",
        'o4_13_reads': "",
        'o4_14_reads': "",
        'o4_15_reads': "",
        'o4_16_reads': "",
        'o1': "",
        'o1_start': "",
        'o1_stop': "",
        'o1_highest_opacity': "",
        'o1_instant_over_20': "",
        'o1_average_6': "",
        'o1_average_6_over_35': "",
        'o2': "",
        'o2_start': "",
        'o2_stop': "",
        'o2_highest_opacity': "",
        'o2_instant_over_20': "",
        'o2_average_6': "",
        'o2_average_6_over_35': "",
        'o3': "",
        'o3_start': "",
        'o3_stop': "",
        'o3_highest_opacity': "",
        'o3_instant_over_20': "",
        'o3_average_6': "",
        'o3_average_6_over_35': "",
        'o4': "",
        'o4_start': "",
        'o4_stop': "",
        'o4_highest_opacity': "",
        'o4_instant_over_20': "",
        'o4_average_6': "",
        'o4_average_6_over_35': ""
    }

    # Widget styles dictionary (applies to JSON fields dynamically)
    JSON_WIDGET_STYLES = {
        "process_equip1": forms.TextInput(attrs={"class": "input", "type": "text", "style": "width: 250px;"}),
        "process_equip2": forms.TextInput(attrs={"class": "input", "type": "text", "style": "width: 250px;"}),
        "background_color_start": forms.TextInput(attrs={"class": "input", "type": "text", "style": "width: 60px; text-align: center;"}),
        "background_color_stop": forms.TextInput(attrs={"class": "input", "type": "text", "style": "width: 60px; text-align: center;"}),
        "sky_conditions": forms.TextInput(attrs={"oninput": "weatherStoplight()", "class": "input", "type": "text", "style": "width: 80px; text-align: center;"}),
        "wind_speed_start": forms.NumberInput(attrs={"oninput": "weatherStoplight()", "class": "input", "type": "number", "style": "width: 40px; text-align: center;"}),
        "wind_speed_stop": forms.TextInput(attrs={"oninput": "weatherStoplight()", "class": "input", "type": "text", "style": "width: 40px; text-align: center;"}),
        "wind_direction": forms.TextInput(attrs={"oninput": "weatherStoplight(); this.value = this.value.toUpperCase()", "class": "input", "type": "text", "style": "width: 60px; text-align: center; text-transform: uppercase;"}),
        "emission_point_stop": forms.TextInput(attrs={"class": "input", "type": "text", "style": "width: 250px;"}),
        "ambient_temp_start": forms.NumberInput(attrs={"oninput": "weatherStoplight()", "class": "input", "type": "number", "style": "width: 40px; text-align: center;"}),
        "ambient_temp_stop": forms.TextInput(attrs={"oninput": "weatherStoplight()", "class": "input", "type": "text", "style": "width: 40px; text-align: center;"}),
        "humidity": forms.NumberInput(attrs={"oninput": "weatherStoplight()", "class": "input", "type": "number", "style": "width: 40px; text-align: center;"}),
        "height_above_ground": forms.NumberInput(attrs={"class": "input", "type": "number", "style": "width: 40px; text-align: center;"}),
        "height_rel_observer": forms.NumberInput(attrs={"class": "input", "type": "number", "style": "width: 40px; text-align: center;"}),
        "distance_from": forms.NumberInput(attrs={"class": "input", "type": "number", "style": "width: 40px; text-align: center;"}),
        "direction_from": forms.TextInput(attrs={"oninput": "this.value = this.value.toUpperCase()", "class": "input", "type": "text", "style": "width: 50px; text-align: center;"}),
        "plume_opacity_determined_stop": forms.TextInput(attrs={"class": "input", "type": "text", "style": "width: 250px;"}),
        "plume_type": forms.Select(
            choices=[("", "---------"),("N/A", "N/A"),("Fugative", "Fugative"),("Continuous", "Continuous"),("Intermittent", "Intermittent")],
            attrs={"class": "input", "required": True}
        ),
        "op_mode1": forms.TextInput(attrs={"name": "op_mode1", "maxlength": "30", "required": True, "class": "input", "type": "text", "style": "width: 150px;"}),
        "op_mode2": forms.TextInput(attrs={"name": "op_mode2", "maxlength": "30", "required": True, "class": "input", "type": "text", "style": "width: 150px;"}),
        "emission_point_start": forms.TextInput(attrs={"name": "emission_point_start", "maxlength": "50", "required": True, "class": "input", "type": "text", "style": "width: 200px;"}),
        "describe_emissions_start": forms.TextInput(attrs={"name": "describe_emissions_start", "maxlength": "30", "required": True, "class": "input", "type": "text", "style": "width: 100px;"}),
        "describe_emissions_stop": forms.TextInput(attrs={"name": "describe_emissions_stop", "maxlength": "30", "required": True, "class": "input", "type": "text", "style": "width: 200px;"}),
        "emission_color_start": forms.TextInput(attrs={"name": "emission_color_start", "maxlength": "30", "required": True, "class": "input", "type": "text", "style": "width: 100px;"}),
        "emission_color_stop": forms.TextInput(attrs={"name": "emission_color_stop", "maxlength": "30", "required": True, "class": "input", "type": "text", "style": "width: 150px;"}),
        "water_drolet_present": forms.Select(
            choices=[("", "---------"), ("Yes", "Yes"), ("No", "No")],
            attrs={"name": "water_drolet_present", "required": True, "class": "input", "style": "width: 120px;"}
        ),
        "water_droplet_plume": forms.Select(
            choices=[("", "---------"), ("N/A", "N/A"), ("Attached", "Attached"), ("Detached", "Detached")],
            attrs={"name": "water_droplet_plume", "required": True, "class": "input", "style": "width: 120px;"}
        ),
        "plume_opacity_determined_start": forms.TextInput(attrs={"name": "plume_opacity_determined_start", "maxlength": "50", "required": True, "class": "input", "type": "text", "style": "width: 200px;"}),
        "describe_background_start": forms.TextInput(attrs={"name": "describe_background_start", "maxlength": "30", "required": True, "class": "input", "type": "text", "style": "width: 200px;"}),
        "describe_background_stop": forms.TextInput(attrs={"name": "describe_background_stop", "maxlength": "30", "required": True, "class": "input", "type": "text", "style": "width: 200px;"}),
        'o1_instant_over_20' : forms.Select(attrs={'id': 'o1_instant_over_20', 'style': 'width: 60px;'}),
        'o2_instant_over_20' : forms.Select(attrs={'id': 'o2_instant_over_20', 'style': 'width: 60px;'}),
        'o3_instant_over_20' : forms.Select(attrs={'id': 'o3_instant_over_20', 'style': 'width: 60px;'}),
        'o4_instant_over_20' : forms.Select(attrs={'id': 'o4_instant_over_20', 'style': 'width: 60px;'}),
        'o1_average_6_over_35' : forms.Select(attrs={'id': 'o1_average_6_over_35', 'style': 'width: 60px;'}),
        'o2_average_6_over_35' : forms.Select(attrs={'id': 'o2_average_6_over_35', 'style': 'width: 60px;'}),
        'o3_average_6_over_35' : forms.Select(attrs={'id': 'o3_average_6_over_35', 'style': 'width: 60px;'}),
        'o4_average_6_over_35' : forms.Select(attrs={'id': 'o4_average_6_over_35', 'style': 'width: 60px;'}),
        'o1_highest_opacity' : forms.NumberInput(attrs={'oninput': 'averages_pt1()', 'id': 'o1_highest_opacity','class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
        'o2_highest_opacity' : forms.NumberInput(attrs={'oninput': 'averages_pt2()', 'id': 'o2_highest_opacity','class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
        'o3_highest_opacity' : forms.NumberInput(attrs={'oninput': 'averages_pt3()', 'id': 'o3_highest_opacity','class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
        'o4_highest_opacity' : forms.NumberInput(attrs={'oninput': 'averages_pt4()', 'id': 'o4_highest_opacity','class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
        'o1_average_6' : forms.NumberInput(attrs={"step": "0.01", 'oninput': 'averages_pt1()', 'id': 'o1_average_6', 'class': 'input', 'type': 'number', 'style':'width: 60px; text-align: center;'}),
        'o2_average_6' : forms.NumberInput(attrs={"step": "0.01", 'oninput': 'averages_pt2()', 'id': 'o2_average_6', 'class': 'input', 'type': 'number', 'style':'width: 60px; text-align: center;'}),
        'o3_average_6' : forms.NumberInput(attrs={"step": "0.01", 'oninput': 'averages_pt3()', 'id': 'o3_average_6', 'class': 'input', 'type': 'number', 'style':'width: 60px; text-align: center;'}),
        'o4_average_6' : forms.NumberInput(attrs={"step": "0.01", 'oninput': 'averages_pt4()', 'id': 'o4_average_6', 'class': 'input', 'type': 'number', 'style':'width: 60px; text-align: center;'}),
        'o1' : forms.NumberInput(attrs={'id' : 'o1', 'class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
        'o2' : forms.NumberInput(attrs={'id' : 'o2', 'class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
        'o3' : forms.NumberInput(attrs={'id' : 'o3', 'class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
        'o4' : forms.NumberInput(attrs={'id' : 'o4', 'class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
        'o1_start' : forms.TimeInput(attrs={'id': 'o1_start', 'oninput': 'timecheck_pt1()', 'type':'time', 'style':'width: 120px;', 'required':True}),
        'o1_stop' : forms.TimeInput(attrs={'id': 'o1_stop', 'oninput': 'timecheck_pt1()', 'type':'time', 'style':'width: 120px;', 'required':True}),
        'o2_start' : forms.TimeInput(attrs={'id': 'o2_start', 'oninput': 'timecheck_pt2()', 'type':'time', 'style':'width: 120px;', 'required':True}),
        'o2_stop' : forms.TimeInput(attrs={'id': 'o2_stop', 'oninput': 'timecheck_pt2()', 'type':'time', 'style':'width: 120px;', 'required':True}),
        'o3_start' : forms.TimeInput(attrs={'id': 'o3_start', 'oninput': 'timecheck_pt3()', 'type':'time', 'style':'width: 120px;', 'required':True}),
        'o3_stop' : forms.TimeInput(attrs={'id': 'o3_stop', 'oninput': 'timecheck_pt3()', 'type':'time', 'style':'width: 120px;', 'required':True}),
        'o4_start' : forms.TimeInput(attrs={'id': 'o4_start', 'oninput': 'timecheck_pt4()', 'type':'time', 'style':'width: 120px;', 'required':True}),
        'o4_stop' : forms.TimeInput(attrs={'id': 'o4_stop', 'oninput': 'timecheck_pt4()', 'type':'time', 'style':'width: 120px;', 'required':True}),
        'o1_1_reads' : forms.TextInput(attrs={'id':'o1_1_reads', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o1_2_reads' : forms.TextInput(attrs={'id':'o1_2_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o1_3_reads' : forms.TextInput(attrs={'id':'o1_3_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o1_4_reads' : forms.TextInput(attrs={'id':'o1_4_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o1_5_reads' : forms.TextInput(attrs={'id':'o1_5_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o1_6_reads' : forms.TextInput(attrs={'id':'o1_6_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o1_7_reads' : forms.TextInput(attrs={'id':'o1_7_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o1_8_reads' : forms.TextInput(attrs={'id':'o1_8_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o1_9_reads' : forms.TextInput(attrs={'id':'o1_9_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o1_10_reads' : forms.TextInput(attrs={'id':'o1_10_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o1_11_reads' : forms.TextInput(attrs={'id':'o1_11_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o1_12_reads' : forms.TextInput(attrs={'id':'o1_12_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o1_13_reads' : forms.TextInput(attrs={'id':'o1_13_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o1_14_reads' : forms.TextInput(attrs={'id':'o1_14_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o1_15_reads' : forms.TextInput(attrs={'id':'o1_15_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o1_16_reads' : forms.TextInput(attrs={'id':'o1_16_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o2_1_reads' : forms.TextInput(attrs={'id':'o2_1_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o2_2_reads' : forms.TextInput(attrs={'id':'o2_2_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o2_3_reads' : forms.TextInput(attrs={'id':'o2_3_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o2_4_reads' : forms.TextInput(attrs={'id':'o2_4_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o2_5_reads' : forms.TextInput(attrs={'id':'o2_5_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o2_6_reads' : forms.TextInput(attrs={'id':'o2_6_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o2_7_reads' : forms.TextInput(attrs={'id':'o2_7_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o2_8_reads' : forms.TextInput(attrs={'id':'o2_8_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o2_9_reads' : forms.TextInput(attrs={'id':'o2_9_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o2_10_reads' : forms.TextInput(attrs={'id':'o2_10_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o2_11_reads' : forms.TextInput(attrs={'id':'o2_11_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o2_12_reads' : forms.TextInput(attrs={'id':'o2_12_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o2_13_reads' : forms.TextInput(attrs={'id':'o2_13_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o2_14_reads' : forms.TextInput(attrs={'id':'o2_14_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o2_15_reads' : forms.TextInput(attrs={'id':'o2_15_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o2_16_reads' : forms.TextInput(attrs={'id':'o2_16_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o3_1_reads' : forms.TextInput(attrs={'id':'o3_1_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o3_2_reads' : forms.TextInput(attrs={'id':'o3_2_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o3_3_reads' : forms.TextInput(attrs={'id':'o3_3_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o3_4_reads' : forms.TextInput(attrs={'id':'o3_4_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o3_5_reads' : forms.TextInput(attrs={'id':'o3_5_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o3_6_reads' : forms.TextInput(attrs={'id':'o3_6_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o3_7_reads' : forms.TextInput(attrs={'id':'o3_7_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o3_8_reads' : forms.TextInput(attrs={'id':'o3_8_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o3_9_reads' : forms.TextInput(attrs={'id':'o3_9_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o3_10_reads' : forms.TextInput(attrs={'id':'o3_10_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o3_11_reads' : forms.TextInput(attrs={'id':'o3_11_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o3_12_reads' : forms.TextInput(attrs={'id':'o3_12_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o3_13_reads' : forms.TextInput(attrs={'id':'o3_13_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o3_14_reads' : forms.TextInput(attrs={'id':'o3_14_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o3_15_reads' : forms.TextInput(attrs={'id':'o3_15_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o3_16_reads' : forms.TextInput(attrs={'id':'o3_16_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o4_1_reads' : forms.TextInput(attrs={'id':'o4_1_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o4_2_reads' : forms.TextInput(attrs={'id':'o4_2_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o4_3_reads' : forms.TextInput(attrs={'id':'o4_3_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o4_4_reads' : forms.TextInput(attrs={'id':'o4_4_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o4_5_reads' : forms.TextInput(attrs={'id':'o4_5_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o4_6_reads' : forms.TextInput(attrs={'id':'o4_6_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o4_7_reads' : forms.TextInput(attrs={'id':'o4_7_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o4_8_reads' : forms.TextInput(attrs={'id':'o4_8_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o4_9_reads' : forms.TextInput(attrs={'id':'o4_9_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o4_10_reads' : forms.TextInput(attrs={'id':'o4_10_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o4_11_reads' : forms.TextInput(attrs={'id':'o4_11_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o4_12_reads' : forms.TextInput(attrs={'id':'o4_12_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o4_13_reads' : forms.TextInput(attrs={'id':'o4_13_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o4_14_reads' : forms.TextInput(attrs={'id':'o4_14_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o4_15_reads' : forms.TextInput(attrs={'id':'o4_15_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        'o4_16_reads' : forms.TextInput(attrs={'id':'o4_16_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
    }

    def __init__(self, *args, **kwargs):
        """ Extract JSON values and create dynamic form fields with the correct styles. """
        super().__init__(*args, **kwargs)

        # Get the instance's existing reading_data (if any)
        instance = kwargs.get("instance")
        existing_data = instance.reading_data if instance and instance.reading_data else {}
        existing_ovens_data = instance.ovens_data if instance and instance.ovens_data else {}

        # Merge default fields with existing data and apply styles
        for key, default_value in self.DEFAULT_READING_FIELDS.items():
            widget = self.JSON_WIDGET_STYLES.get(key, forms.TextInput(attrs={"class": "input"}))  # Default widget if not specified
            self.fields[key] = forms.CharField(
                initial=existing_data.get(key, default_value),
                required=False,
                widget=widget
            )
        # **Merge `ovens_data` into the form fields (preserving structure)**
        for oven_key, oven_values in existing_ovens_data.items():
            oven_number = oven_key.replace("oven", "")  # Extract oven number (1, 2, 3, 4)

            oven_fields = {
                f"o{oven_number}_start": oven_values.get("start", ""),
                f"o{oven_number}_stop": oven_values.get("stop", ""),
                f"o{oven_number}": oven_values.get(f"o{oven_number}_oven_number", ""),
                f"o{oven_number}_highest_opacity": oven_values.get(f"o{oven_number}_highest_opacity", ""),
                f"o{oven_number}_opacity_over_20": oven_values.get(f"o{oven_number}_opacity_over_20", ""),
                f"o{oven_number}_average_6_opacity": oven_values.get(f"o{oven_number}_average_6_opacity", ""),
                f"o{oven_number}_average_6_over_35": oven_values.get(f"o{oven_number}_average_6_over_35", "")
            }

            # **Assign fields dynamically to form**
            for field_name, value in oven_fields.items():
                widget = self.JSON_WIDGET_STYLES.get(field_name, forms.TextInput(attrs={"class": "input"}))  # Default widget
                self.fields[field_name] = forms.CharField(
                    initial=value,
                    required=False,
                    widget=widget
                )

            # **Loop through `readings.push` and `readings.travel`**
            for reading_type, reading_values in oven_values.get("readings", {}).items():
                for index, reading in reading_values.items():
                    field_name = f"o{oven_number}_{reading_type}_{index}_reads"
                    widget = self.JSON_WIDGET_STYLES.get(field_name, forms.TextInput(attrs={"class": "input"}))  # Default widget
                    self.fields[field_name] = forms.CharField(
                        initial=reading,
                        required=False,
                        widget=widget
                    )

class formA5_readings_form(ModelForm):
    class Meta:
        model = form5_readings_model
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
            'o1_highest_opacity' : forms.NumberInput(attrs={'oninput': 'averages_pt1()', 'id': 'o1_highest_opacity','class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
            'o1_average_6' : forms.NumberInput(attrs={'oninput': 'averages_pt1()', 'id': 'o1_average_6', 'class': 'input', 'type': 'number', 'style':'width: 60px; text-align: center;'}),
            'o2_highest_opacity' : forms.NumberInput(attrs={'oninput': 'averages_pt2()', 'id': 'o2_highest_opacity','class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
            'o2_average_6' : forms.NumberInput(attrs={'oninput': 'averages_pt2()', 'id': 'o2_average_6', 'class': 'input', 'type': 'number', 'style':'width: 60px; text-align: center;'}),
            'o3_highest_opacity' : forms.NumberInput(attrs={'oninput': 'averages_pt3()', 'id': 'o3_highest_opacity','class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
            'o3_average_6' : forms.NumberInput(attrs={'oninput': 'averages_pt3()', 'id': 'o3_average_6', 'class': 'input', 'type': 'number', 'style':'width: 60px; text-align: center;'}),
            'o4_highest_opacity' : forms.NumberInput(attrs={'oninput': 'averages_pt4()', 'id': 'o4_highest_opacity','class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
            'o4_average_6' : forms.NumberInput(attrs={'oninput': 'averages_pt4()', 'id': 'o4_average_6', 'class': 'input', 'type': 'number', 'style':'width: 60px; text-align: center;'}),
            'o1' : forms.NumberInput(attrs={'id' : 'o1', 'class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
            'o2' : forms.NumberInput(attrs={'id' : 'o2', 'class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
            'o3' : forms.NumberInput(attrs={'id' : 'o3', 'class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
            'o4' : forms.NumberInput(attrs={'id' : 'o4', 'class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
            'o1_start' : forms.TimeInput(attrs={'id': 'o1_start', 'oninput': 'timecheck_pt1()', 'type':'time', 'style':'width: 120px;', 'required':True}),
            'o1_stop' : forms.TimeInput(attrs={'id': 'o1_stop', 'oninput': 'timecheck_pt1()', 'type':'time', 'style':'width: 120px;', 'required':True}),
            'o2_start' : forms.TimeInput(attrs={'id': 'o2_start', 'oninput': 'timecheck_pt2()', 'type':'time', 'style':'width: 120px;', 'required':True}),
            'o2_stop' : forms.TimeInput(attrs={'id': 'o2_stop', 'oninput': 'timecheck_pt2()', 'type':'time', 'style':'width: 120px;', 'required':True}),
            'o3_start' : forms.TimeInput(attrs={'id': 'o3_start', 'oninput': 'timecheck_pt3()', 'type':'time', 'style':'width: 120px;', 'required':True}),
            'o3_stop' : forms.TimeInput(attrs={'id': 'o3_stop', 'oninput': 'timecheck_pt3()', 'type':'time', 'style':'width: 120px;', 'required':True}),
            'o4_start' : forms.TimeInput(attrs={'id': 'o4_start', 'oninput': 'timecheck_pt4()', 'type':'time', 'style':'width: 120px;', 'required':True}),
            'o4_stop' : forms.TimeInput(attrs={'id': 'o4_stop', 'oninput': 'timecheck_pt4()', 'type':'time', 'style':'width: 120px;', 'required':True}),
            'o1_1_reads' : forms.TextInput(attrs={'id':'o1_1_reads', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_2_reads' : forms.TextInput(attrs={'id':'o1_2_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_3_reads' : forms.TextInput(attrs={'id':'o1_3_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_4_reads' : forms.TextInput(attrs={'id':'o1_4_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_5_reads' : forms.TextInput(attrs={'id':'o1_5_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_6_reads' : forms.TextInput(attrs={'id':'o1_6_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_7_reads' : forms.TextInput(attrs={'id':'o1_7_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_8_reads' : forms.TextInput(attrs={'id':'o1_8_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_9_reads' : forms.TextInput(attrs={'id':'o1_9_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_10_reads' : forms.TextInput(attrs={'id':'o1_10_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_11_reads' : forms.TextInput(attrs={'id':'o1_11_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_12_reads' : forms.TextInput(attrs={'id':'o1_12_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_13_reads' : forms.TextInput(attrs={'id':'o1_13_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_14_reads' : forms.TextInput(attrs={'id':'o1_14_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_15_reads' : forms.TextInput(attrs={'id':'o1_15_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o1_16_reads' : forms.TextInput(attrs={'id':'o1_16_reads', 'class': 'input', 'oninput':'averages_pt1()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            
            'o2_1_reads' : forms.TextInput(attrs={'id':'o2_1_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_2_reads' : forms.TextInput(attrs={'id':'o2_2_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_3_reads' : forms.TextInput(attrs={'id':'o2_3_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_4_reads' : forms.TextInput(attrs={'id':'o2_4_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_5_reads' : forms.TextInput(attrs={'id':'o2_5_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_6_reads' : forms.TextInput(attrs={'id':'o2_6_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_7_reads' : forms.TextInput(attrs={'id':'o2_7_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_8_reads' : forms.TextInput(attrs={'id':'o2_8_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_9_reads' : forms.TextInput(attrs={'id':'o2_9_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_10_reads' : forms.TextInput(attrs={'id':'o2_10_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_11_reads' : forms.TextInput(attrs={'id':'o2_11_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_12_reads' : forms.TextInput(attrs={'id':'o2_12_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_13_reads' : forms.TextInput(attrs={'id':'o2_13_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_14_reads' : forms.TextInput(attrs={'id':'o2_14_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_15_reads' : forms.TextInput(attrs={'id':'o2_15_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o2_16_reads' : forms.TextInput(attrs={'id':'o2_16_reads', 'class': 'input', 'oninput':'averages_pt2()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            
            'o3_1_reads' : forms.TextInput(attrs={'id':'o3_1_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_2_reads' : forms.TextInput(attrs={'id':'o3_2_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_3_reads' : forms.TextInput(attrs={'id':'o3_3_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_4_reads' : forms.TextInput(attrs={'id':'o3_4_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_5_reads' : forms.TextInput(attrs={'id':'o3_5_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_6_reads' : forms.TextInput(attrs={'id':'o3_6_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_7_reads' : forms.TextInput(attrs={'id':'o3_7_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_8_reads' : forms.TextInput(attrs={'id':'o3_8_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_9_reads' : forms.TextInput(attrs={'id':'o3_9_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_10_reads' : forms.TextInput(attrs={'id':'o3_10_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_11_reads' : forms.TextInput(attrs={'id':'o3_11_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_12_reads' : forms.TextInput(attrs={'id':'o3_12_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_13_reads' : forms.TextInput(attrs={'id':'o3_13_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_14_reads' : forms.TextInput(attrs={'id':'o3_14_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_15_reads' : forms.TextInput(attrs={'id':'o3_15_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o3_16_reads' : forms.TextInput(attrs={'id':'o3_16_reads', 'class': 'input', 'oninput':'averages_pt3()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            
            'o4_1_reads' : forms.TextInput(attrs={'id':'o4_1_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_2_reads' : forms.TextInput(attrs={'id':'o4_2_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_3_reads' : forms.TextInput(attrs={'id':'o4_3_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_4_reads' : forms.TextInput(attrs={'id':'o4_4_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_5_reads' : forms.TextInput(attrs={'id':'o4_5_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_6_reads' : forms.TextInput(attrs={'id':'o4_6_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_7_reads' : forms.TextInput(attrs={'id':'o4_7_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_8_reads' : forms.TextInput(attrs={'id':'o4_8_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_9_reads' : forms.TextInput(attrs={'id':'o4_9_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_10_reads' : forms.TextInput(attrs={'id':'o4_10_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_11_reads' : forms.TextInput(attrs={'id':'o4_11_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_12_reads' : forms.TextInput(attrs={'id':'o4_12_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_13_reads' : forms.TextInput(attrs={'id':'o4_13_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_14_reads' : forms.TextInput(attrs={'id':'o4_14_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_15_reads' : forms.TextInput(attrs={'id':'o4_15_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
            'o4_16_reads' : forms.TextInput(attrs={'id':'o4_16_reads', 'class': 'input', 'oninput':'averages_pt4()', 'type': 'text', 'style':'width: 50px; text-align: center;'}),
        }
    
 
class formB_form(ModelForm):
    class Meta:
        model = form6_model
        fields = ('__all__')
        widgets = {
            'week_start': forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'week_end': forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'observer_0' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'time_0' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'weather_0' : forms.Select(attrs={'style':'width: 80px;'}),
            'wind_speed_0' : forms.TextInput(attrs={'oninput': 'wind_placeholder()', 'type':'number', 'style':'width: 50px; text-align: center;'}),
            'fugitive_dust_observed_0' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'supressant_applied_0' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'supressant_active_0' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'working_face_exceed_0' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'spills_0' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'pushed_back_0' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'coal_vessel_0' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'water_sprays_0' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'loader_lowered_0' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'working_water_sprays_0' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'barrier_thickness_0' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 80px;'}),
            'surface_quality_0' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 60px;'}),
            'surpressant_crust_0' : forms.Select(attrs={'oninput': 'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'additional_surpressant_0' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'comments_0' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'wharf_0' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 80px;'}),
            'breeze_0' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 80px;'}),
            
            'observer_1' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'time_1' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'weather_1' : forms.Select(attrs={'style':'width: 80px;'}),
            'wind_speed_1' : forms.TextInput(attrs={'oninput': 'wind_placeholder()', 'type':'number', 'style':'width: 50px; text-align: center;'}),
            'fugitive_dust_observed_1' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'supressant_applied_1' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'supressant_active_1' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'working_face_exceed_1' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'spills_1' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'pushed_back_1' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'coal_vessel_1' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'water_sprays_1' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'loader_lowered_1' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'working_water_sprays_1' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'barrier_thickness_1' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 80px;'}),
            'surface_quality_1' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 60px;'}),
            'surpressant_crust_1' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'additional_surpressant_1' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'comments_1' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'wharf_1' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 80px;'}),
            'breeze_1' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 80px;'}),
            
            'observer_2' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'time_2' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'weather_2' : forms.Select(attrs={'style':'width: 80px;'}),
            'wind_speed_2' : forms.TextInput(attrs={'oninput': 'wind_placeholder()', 'type':'number', 'style':'width: 50px; text-align: center;'}),
            'fugitive_dust_observed_2' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'supressant_applied_2' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'supressant_active_2' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'working_face_exceed_2' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'spills_2' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'pushed_back_2' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'coal_vessel_2' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'water_sprays_2' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'loader_lowered_2' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'working_water_sprays_2' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'barrier_thickness_2' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 80px;'}),
            'surface_quality_2' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 60px;'}),
            'surpressant_crust_2' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'additional_surpressant_2' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'comments_2' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'wharf_2' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 80px;'}),
            'breeze_2' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 80px;'}),
            
            'observer_3' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'time_3' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'weather_3' : forms.Select(attrs={'style':'width: 80px;'}),
            'wind_speed_3' : forms.TextInput(attrs={'oninput': 'wind_placeholder()', 'type':'number', 'style':'width: 50px; text-align: center;'}),
            'fugitive_dust_observed_3' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'supressant_applied_3' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'supressant_active_3' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'working_face_exceed_3' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'spills_3' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'pushed_back_3' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'coal_vessel_3' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'water_sprays_3' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'loader_lowered_3' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'working_water_sprays_3' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'barrier_thickness_3' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 80px;'}),
            'surface_quality_3' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 60px;'}),
            'surpressant_crust_3' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'additional_surpressant_3' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'comments_3' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'wharf_3' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 80px;'}),
            'breeze_3' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 80px;'}),
            
            'observer_4' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'time_4' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'weather_4' : forms.Select(attrs={'style':'width: 80px;'}),
            'wind_speed_4' : forms.TextInput(attrs={'oninput': 'wind_placeholder()', 'type':'number', 'style':'width: 50px; text-align: center;'}),
            'fugitive_dust_observed_4' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'supressant_applied_4' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'supressant_active_4' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'working_face_exceed_4' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'spills_4' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'pushed_back_4' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'coal_vessel_4' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'water_sprays_4' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'loader_lowered_4' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'working_water_sprays_4' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'barrier_thickness_4' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 80px;'}),
            'surface_quality_4' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 60px;'}),
            'surpressant_crust_4' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 50px;'}),
            'additional_surpressant_4' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'comments_4' : forms.TextInput(attrs={'type':'text', 'style':'width: 130px; text-align: center;'}),
            'wharf_4' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 80px;'}),
            'breeze_4' : forms.Select(attrs={'oninput':'clean_up_submitted_form()', 'style':'width: 80px;'}),
        }
    
class formD_form(ModelForm):
    class Meta:
        model = form8_model
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
            'truck_id1' : forms.Select(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'date1' : forms.DateInput(attrs={'onchange': 'if_one_then_all()', 'type':'date', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center;'}),
            'time1' : forms.TimeInput(attrs={'onchange': 'if_one_then_all()', 'type':'time', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center;'}),
            'contents1' : forms.Select(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'freeboard1' : forms.Select(attrs={'oninput': 'freeboard_1()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'wetted1' : forms.Select(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'comments1' : forms.Textarea(attrs={'rows': '3', 'onchange': 'if_one_then_all()', 'type':'text', 'style':'width: 463px; font-size: 1.5rem; border-radius: 15px; height: 8rem;'}),
            'truck_id2' : forms.Select(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'date2' : forms.DateInput(attrs={'onchange': 'if_one_then_all()', 'type':'date', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center;'}),
            'time2' : forms.TimeInput(attrs={'onchange': 'if_one_then_all()', 'type':'time', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center;'}),
            'contents2' : forms.Select(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'freeboard2' : forms.Select(attrs={'oninput': 'freeboard_2()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'wetted2' : forms.Select(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'comments2' : forms.Textarea(attrs={'rows': '3', 'onchange': 'if_one_then_all()', 'type':'text', 'style':'width: 463px; font-size: 1.5rem; border-radius: 15px; height: 8rem;'}),
            'truck_id3' : forms.Select(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'date3' : forms.DateInput(attrs={'onchange': 'if_one_then_all()', 'type':'date', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center;'}),
            'time3' : forms.TimeInput(attrs={'onchange': 'if_one_then_all()', 'type':'time', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center;'}),
            'contents3' : forms.Select(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'freeboard3' : forms.Select(attrs={'oninput': 'freeboard_3()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'wetted3' : forms.Select(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'comments3' : forms.Textarea(attrs={'rows': '3', 'onchange': 'if_one_then_all()', 'type':'text', 'style':'width: 463px; font-size: 1.5rem; border-radius: 15px; height: 8rem;'}),
            'truck_id4' : forms.Select(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'date4' : forms.DateInput(attrs={'onchange': 'if_one_then_all()', 'type':'date', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center;'}),
            'time4' : forms.TimeInput(attrs={'onchange': 'if_one_then_all()', 'type':'time', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center;'}),
            'contents4' : forms.Select(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'freeboard4' : forms.Select(attrs={'oninput': 'freeboard_4()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'wetted4' : forms.Select(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'comments4' : forms.Textarea(attrs={'rows': '3', 'onchange': 'if_one_then_all()', 'type':'text', 'style':'width: 463px; font-size: 1.5rem; border-radius: 15px; height: 8rem;'}),
            'truck_id5' : forms.Select(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'date5' : forms.DateInput(attrs={'onchange': 'if_one_then_all()', 'type':'date', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center;'}),
            'time5' : forms.TimeInput(attrs={'onchange': 'if_one_then_all()', 'type':'time', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center;'}),
            'contents5' : forms.Select(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'freeboard5' : forms.Select(attrs={'oninput': 'freeboard_5()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'wetted5' : forms.Select(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'comments5' : forms.Textarea(attrs={'rows': '3', 'onchange': 'if_one_then_all()', 'type':'text', 'style':'width: 463px; font-size: 1.5rem; border-radius: 15px; height: 8rem;'}),
            'observer1' : forms.TextInput(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center;'}),
            'observer2' : forms.TextInput(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center;'}),
            'observer3' : forms.TextInput(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center;'}),
            'observer4' : forms.TextInput(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center;'}),
            'observer5' : forms.TextInput(attrs={'onchange': 'if_one_then_all()', 'style':'width: 215px; border-radius: 15px; font-size: 1.5rem; text-align: center;'}),
        }
  
class formE_form(ModelForm):
    class Meta:
        model = form9_model
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
            'foreman' : forms.TextInput(attrs={'style':'width: 80px;'}),
            'start_time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'end_time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'leaks' : forms.Select(attrs={'onchange': 'no_leaks(this)', 'style': 'width: 50px;'}),
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
        model = form17_model
        fields = ('__all__')
        
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'cert_date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'process_equip1' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 250px;'}),
            'background_color_start' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 60px;'}),
            'background_color_stop' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 60px;'}),
            'wind_speed_start' : forms.NumberInput(attrs={'oninput': 'weatherStoplight()', 'class': 'input', 'type': 'number', 'style':'width: 40px;text-align: center;'}),
            'wind_speed_stop' : forms.TextInput(attrs={'oninput': 'weatherStoplight()', 'class': 'input', 'type': 'text', 'style':'width: 40px;text-align: center;'}),
            'emission_point_stop' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 250px;'}),
            'ambient_temp_start' : forms.NumberInput(attrs={'oninput': 'weatherStoplight()', 'class': 'input', 'type': 'number', 'style':'width: 40px;text-align: center;'}),
            'ambient_temp_stop' : forms.TextInput(attrs={'oninput': 'weatherStoplight()', 'class': 'input', 'type': 'text', 'style':'width: 40px;text-align: center;'}),
            'plume_opacity_determined_stop' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 250px;'}),
            'humidity': forms.NumberInput(attrs={'oninput': 'weatherStoplight()', 'class': 'input', 'type': 'number', 'style': 'width: 40px; text-align: center;'}),
            'wind_direction': forms.TextInput(attrs={'oninput': 'weatherStoplight(); this.value = this.value.toUpperCase()', 'class': 'input', 'type': 'text', 'style': 'width: 60px; text-align: center; text-transform: uppercase;'}),
            'sky_conditions': forms.TextInput(attrs={'oninput': 'weatherStoplight()', 'class': 'input', 'type': 'text', 'style': 'width: 80px; text-align: center;'}),
            'estab_no': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 80px; text-align: center;'}),
            'height_above_ground': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 40px; text-align: center;'}),
            'height_rel_observer': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 40px; text-align: center;'}),
            'distance_from': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 40px; text-align: center;'}),
            'direction_from': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'observer': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'canvas': forms.TextInput(attrs={'id': 'canvas', 'type': 'hidden', 'class': 'input', 'style': 'width:50px; text-align: center;', "required": "true"})
        }      
class formG1_readings_form(ModelForm):
    class Meta:
        model = form17_readings_model
        fields = ('__all__')
        exclude = ('form',)
        widgets = {
            'PEC_start' : forms.TimeInput(attrs={'type':'time', 'style':'width: 95px;'}),
            'PEC_stop' : forms.TimeInput(attrs={'type':'time', 'style':'width: 95px;'}),
            'PEC_read_1' : forms.TextInput(attrs={'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_2' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_3' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_4' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_5' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_6' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_7' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_8' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_9' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_10' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_11' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_12' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_13' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_14' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_15' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_16' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_17' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_18' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_19' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_20' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_21' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_22' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_23' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_24' : forms.TextInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_oven1' : forms.NumberInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_oven2' : forms.NumberInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_time1' : forms.TimeInput(attrs={'type': 'time', 'style':'width: 95px;'}),
            'PEC_time2' : forms.TimeInput(attrs={'type': 'time', 'style':'width: 95px;'}),
            'PEC_type' : forms.TextInput(attrs={'type': 'hidden'}),
            'PEC_average' : forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_push_oven' : forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_push_time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 95px;'}),
            'PEC_observe_time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 95px;'}),
            'PEC_emissions_present' : forms.CheckboxInput(attrs={'style': 'width: 50px;', 'initial': 'false' }),
        }

class formG2_form(ModelForm):
    class Meta:
        model = form18_model
        fields = ('__all__')
        
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'cert_date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'process_equip1' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 250px;'}),
            'background_color_start' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 60px;'}),
            'background_color_stop' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 60px;'}),
            'wind_speed_start' : forms.NumberInput(attrs={'oninput': 'weatherStoplight()', 'class': 'input', 'type': 'number', 'style':'width: 40px;text-align: center;'}),
            'wind_speed_stop' : forms.TextInput(attrs={'oninput': 'weatherStoplight()', 'class': 'input', 'type': 'text', 'style':'width: 40px;text-align: center;'}),
            'emission_point_stop' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 250px;'}),
            'ambient_temp_start' : forms.NumberInput(attrs={'oninput': 'weatherStoplight()', 'class': 'input', 'type': 'number', 'style':'width: 40px;text-align: center;'}),
            'ambient_temp_stop' : forms.TextInput(attrs={'oninput': 'weatherStoplight()', 'class': 'input', 'type': 'text', 'style':'width: 40px;text-align: center;'}),
            'plume_opacity_determined_stop' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 250px;'}),
            'humidity': forms.NumberInput(attrs={'oninput': 'weatherStoplight()', 'class': 'input', 'type': 'number', 'style': 'width: 40px; text-align: center;'}),
            'wind_direction': forms.TextInput(attrs={'oninput': 'weatherStoplight(); this.value = this.value.toUpperCase()', 'class': 'input', 'type': 'text', 'style': 'width: 60px; text-align: center; text-transform: uppercase;'}),
            'sky_conditions': forms.TextInput(attrs={'oninput': 'weatherStoplight()', 'class': 'input', 'type': 'text', 'style': 'width: 80px; text-align: center;'}),
            'estab_no': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 80px; text-align: center;'}),
            'height_above_ground': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 40px; text-align: center;'}),
            'height_rel_observer': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 40px; text-align: center;'}),
            'distance_from': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 40px; text-align: center;'}),
            'direction_from': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'observer': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'canvas': forms.TextInput(attrs={'id': 'canvas', 'type': 'hidden', 'class': 'input', 'style': 'width:50px; text-align: center;', "required": "true"})
        }
class formG2_readings_form(ModelForm):
    class Meta:
        model = form18_readings_model
        fields = ('__all__')
        exclude = ('form',)
        widgets = {
            'PEC_read_a_1' : forms.TextInput(attrs={'oninput': 'avg_a()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_a_2' : forms.TextInput(attrs={'oninput': 'avg_a()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_a_3' : forms.TextInput(attrs={'oninput': 'avg_a()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_a_4' : forms.TextInput(attrs={'oninput': 'avg_a()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_a_5' : forms.TextInput(attrs={'oninput': 'avg_a()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_a_6' : forms.TextInput(attrs={'oninput': 'avg_a()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_a_7' : forms.TextInput(attrs={'oninput': 'avg_a()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_a_8' : forms.TextInput(attrs={'oninput': 'avg_a()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            
            'PEC_read_b_1' : forms.TextInput(attrs={'oninput': 'avg_b()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_b_2' : forms.TextInput(attrs={'oninput': 'avg_b()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_b_3' : forms.TextInput(attrs={'oninput': 'avg_b()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_b_4' : forms.TextInput(attrs={'oninput': 'avg_b()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_b_5' : forms.TextInput(attrs={'oninput': 'avg_b()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_b_6' : forms.TextInput(attrs={'oninput': 'avg_b()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_b_7' : forms.TextInput(attrs={'oninput': 'avg_b()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_b_8' : forms.TextInput(attrs={'oninput': 'avg_b()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            
            'PEC_read_c_1' : forms.TextInput(attrs={'oninput': 'avg_c()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_c_2' : forms.TextInput(attrs={'oninput': 'avg_c()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_c_3' : forms.TextInput(attrs={'oninput': 'avg_c()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_c_4' : forms.TextInput(attrs={'oninput': 'avg_c()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_c_5' : forms.TextInput(attrs={'oninput': 'avg_c()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_c_6' : forms.TextInput(attrs={'oninput': 'avg_c()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_c_7' : forms.TextInput(attrs={'oninput': 'avg_c()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_read_c_8' : forms.TextInput(attrs={'oninput': 'avg_c()', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),

            'PEC_oven_a' : forms.NumberInput(attrs={'oninput':'firstOvenCheck()', 'class': 'input', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_oven_b' : forms.NumberInput(attrs={'oninput': 'ovenCheck(this)', 'class': 'input', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_oven_c' : forms.NumberInput(attrs={'oninput': 'ovenCheck(this)', 'class': 'input', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
            'PEC_start_a' : forms.TimeInput(attrs={'type':'time', 'style':'width: 100px;', 'required': True}),
            'PEC_start_b' : forms.TimeInput(attrs={'type':'time', 'style':'width: 100px;', 'required': True}),
            'PEC_start_c' : forms.TimeInput(attrs={'type':'time', 'style':'width: 100px;', 'required': True}),
            'PEC_average_a' : forms.NumberInput(attrs={'oninput': 'avg_a()', 'class': 'input', 'type': 'number', 'style': 'width: 50px; text-align: center;', 'required': True}),
            'PEC_average_b' : forms.NumberInput(attrs={'oninput': 'avg_b()', 'class': 'input', 'type': 'number', 'style': 'width: 50px; text-align: center;', 'required': True}),
            'PEC_average_c' : forms.NumberInput(attrs={'oninput': 'avg_c()', 'class': 'input', 'type': 'number', 'style': 'width: 50px; text-align: center;', 'required': True}),
            'PEC_average_main' : forms.NumberInput(attrs={'oninput': 'main_avg()', 'class': 'input', 'type': 'number', 'style': 'width: 50px; text-align: center;', 'required': True}),
        }
        
class formH_form(ModelForm):
    class Meta:
        model = form19_model
        fields = ('__all__')
        
        widgets = {
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'cert_date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'process_equip1' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 250px;'}),
            'background_color_start' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 60px;'}),
            'background_color_stop' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 60px;'}),
            'wind_speed_start' : forms.NumberInput(attrs={'oninput': 'weatherStoplight()', 'class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
            'wind_speed_stop' : forms.TextInput(attrs={'oninput': 'weatherStoplight()', 'class': 'input', 'type': 'text', 'style':'width: 40px; text-align: center;'}),
            'emission_point_stop' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 250px;'}),
            'ambient_temp_start' : forms.NumberInput(attrs={'oninput': 'weatherStoplight()', 'class': 'input', 'type': 'number', 'style':'width: 40px; text-align: center;'}),
            'ambient_temp_stop' : forms.TextInput(attrs={'oninput': 'weatherStoplight()', 'class': 'input', 'type': 'text', 'style':'width: 40px; text-align: center;'}),
            'plume_opacity_determined_stop' : forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style':'width: 250px;'}),
            'humidity': forms.NumberInput(attrs={'oninput': 'weatherStoplight()', 'class': 'input', 'type': 'number', 'style': 'width: 40px; text-align: center;'}),
            'wind_direction': forms.TextInput(attrs={'oninput': 'weatherStoplight(); this.value = this.value.toUpperCase()', 'class': 'input', 'type': 'text', 'style': 'width: 60px; text-align: center; text-transform: uppercase;'}),
            'sky_conditions': forms.TextInput(attrs={'oninput': 'weatherStoplight()', 'class': 'input', 'type': 'text', 'style': 'width: 80px; text-align: center;'}),
            'estab_no': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 80px; text-align: center;'}),
            'height_above_ground': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 40px; text-align: center;'}),
            'height_rel_observer': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 40px; text-align: center;'}),
            'distance_from': forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 40px; text-align: center;'}),
            'direction_from': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'observer': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'canvas': forms.TextInput(attrs={'id': 'canvas', 'type': 'hidden', 'class': 'input', 'style': 'width:50px; text-align: center;', "required": "true"})
        }
class formH_readings_form(ModelForm):
    class Meta:
        model = form19_readings_model
        fields = ('__all__')
        exclude = ('form',)
        widgets = {
            'comb_start' : forms.TimeInput(attrs={'id': 'comb_start', 'oninput': 'timecheck_combustion()', 'type':'time', 'style':'width: 120px;', 'required': True}),
            'comb_stop' : forms.TimeInput(attrs={'id': 'comb_stop', 'oninput': 'timecheck_combustion()', 'type':'time', 'style':'width: 120px;', 'required': True}),
            'comb_read_1' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_2' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_3' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_4' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_5' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_6' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_7' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_8' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_9' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_10' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_11' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_12' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_13' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_14' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_15' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_16' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_17' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_18' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_19' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_20' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_21' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_22' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_23' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_24' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_25' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_26' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_27' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_28' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_29' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_30' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_31' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_32' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_33' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_34' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_35' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_36' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_37' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_38' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_39' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_40' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_41' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_42' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_43' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_44' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_45' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_46' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_47' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_48' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_49' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_50' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_51' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_52' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_53' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_54' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_55' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_56' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_57' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_58' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_59' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_read_60' : forms.TextInput(attrs={'oninput': 'comb_averages()', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'comb_average' : forms.NumberInput(attrs={'oninput': 'comb_averages()', 'class': 'input', 'type': 'number', 'style': 'width: 50px; text-align: center;', 'required': True}),
        }
        
class formI_form(ModelForm):
    class Meta:
        model = form20_model
        fields = ('__all__')
        
        widgets = {
            'week_start': forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'week_end': forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'time_0' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'time_1' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'time_2' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'time_3' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'time_4' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'obser_0' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'obser_1' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'obser_2' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'obser_3' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'obser_4' : forms.TextInput(attrs={'style':'width: 150px;'}),
        }
        
        
class formL_form(ModelForm):
    class Meta:
        #today = datetime.date.today()
        #name_5 = False
        #name_6 = False
        #name_0 = False
        #name_1 = False
        #name_2 = False
        #name_3 = False
        #name_4 = False
        #if today.weekday() == 5:
            #name_5 = True
            #name_6 = False
            #name_0 = False
            #name_1 = False
            #name_2 = False
            #name_3 = False
            #name_4 = False
        #elif today.weekday() == 6:
            #name_5 = True
            #name_6 = True
            #name_0 = False
            #name_1 = False
            #name_2 = False
            #name_3 = False
            #name_4 = False
        #elif today.weekday() == 0:
            #name_5 = True
            #name_6 = True
            #name_0 = True
            #name_1 = False
            #name_2 = False
            #name_3 = False
            #name_4 = False
        #elif today.weekday() == 1:
            #name_5 = True
            #name_6 = True
            #name_0 = True
            #name_1 = True
            #name_2 = False
            #name_3 = False
            #name_4 = False
        #elif today.weekday() == 2:
            #name_5 = True
            #name_6 = True
            #name_0 = True
            #name_1 = True
            #name_2 = True
            #name_3 = False
            #name_4 = False
        #elif today.weekday() == 3:
            #name_5 = True
            #name_6 = True
            #name_0 = True
            #name_1 = True
            #name_2 = True
            #name_3 = True
            #name_4 = False
        #elif today.weekday() == 4:
            #name_5 = True
            #name_6 = True
            #name_0 = True
            #name_1 = True
            #name_2 = True
            #name_3 = True
            #name_4 = True
        
        model = form21_model
        fields = ('__all__')
        
        widgets = {
            'week_start' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'week_end' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'time_0' : forms.TimeInput(attrs={'type':'time', 'style':'width: 130px;'}),
            'time_1' : forms.TimeInput(attrs={'type':'time', 'style':'width: 130px;'}),
            'time_2' : forms.TimeInput(attrs={'type':'time', 'style':'width: 130px;'}),
            'time_3' : forms.TimeInput(attrs={'type':'time', 'style':'width: 130px;'}),
            'time_4' : forms.TimeInput(attrs={'type':'time', 'style':'width: 130px;'}),
            'time_5' : forms.TimeInput(attrs={'type':'time', 'style':'width: 130px;'}),
            'time_6' : forms.TimeInput(attrs={'type':'time', 'style':'width: 130px;'}),
            'obser_0' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'obser_1' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'obser_2' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'obser_3' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'obser_4' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'obser_5' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'obser_6' : forms.TextInput(attrs={'style':'width: 150px;'}),
        }
       
class formM_form(ModelForm):
    class Meta:
        model = form22_model
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
            'observer',
            'cert_date',
            'comments',
        )
        
        widgets = {
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'paved' : forms.Select(attrs={'style':''}),
            'pav_start' : forms.TimeInput(attrs={'oninput': 'timecheck_pav()', 'type':'time', 'style':'width: 120px;'}),
            'pav_stop' : forms.TimeInput(attrs={'oninput': 'timecheck_pav()', 'type':'time', 'style':'width: 120px;'}),
            'unpaved' : forms.Select(attrs={'style':''}),
            'unp_start' : forms.TimeInput(attrs={'oninput': 'timecheck_unpav()', 'type':'time', 'style':'width: 120px;'}),
            'unp_stop' : forms.TimeInput(attrs={'oninput': 'timecheck_unpav()', 'type':'time', 'style':'width: 120px;'}),
            'parking' : forms.Select(attrs={'style':''}),
            'par_start' : forms.TimeInput(attrs={'oninput': 'timecheck_par()', 'type':'time', 'style':'width: 120px;'}),
            'par_stop' : forms.TimeInput(attrs={'oninput': 'timecheck_par()', 'type':'time', 'style':'width: 120px;'}),
            'observer' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'cert_date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'comments' : Textarea(attrs={'rows':7, 'cols':125}),
        }
class formM_readings_form(ModelForm):
    class Meta:
        model = form22_readings_model
        fields = ('__all__')
        exclude = ('form',)
        widgets = {
            'pav_1' : forms.TextInput(attrs={'oninput':'paved_average()', 'oninput':'autoFillZeros(id_pav_1.id)', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'pav_2' : forms.NumberInput(attrs={'oninput':'paved_average()', 'style': 'width: 50px; text-align: center;'}),
            'pav_3' : forms.NumberInput(attrs={'oninput':'paved_average()', 'style': 'width: 50px; text-align: center;'}),
            'pav_4' : forms.NumberInput(attrs={'oninput':'paved_average()', 'style': 'width: 50px; text-align: center;'}),
            'pav_5' : forms.NumberInput(attrs={'oninput':'paved_average()', 'style': 'width: 50px; text-align: center;'}),
            'pav_6' : forms.NumberInput(attrs={'oninput':'paved_average()', 'style': 'width: 50px; text-align: center;'}),
            'pav_7' : forms.NumberInput(attrs={'oninput':'paved_average()', 'style': 'width: 50px; text-align: center;'}),
            'pav_8' : forms.NumberInput(attrs={'oninput':'paved_average()', 'style': 'width: 50px; text-align: center;'}),
            'pav_9' : forms.NumberInput(attrs={'oninput':'paved_average()', 'style': 'width: 50px; text-align: center;'}),
            'pav_10' : forms.NumberInput(attrs={'oninput':'paved_average()', 'style': 'width: 50px; text-align: center;'}),
            'pav_11' : forms.NumberInput(attrs={'oninput':'paved_average()', 'style': 'width: 50px; text-align: center;'}),
            'pav_12' : forms.NumberInput(attrs={'oninput':'paved_average()', 'style': 'width: 50px; text-align: center;'}),
            'unp_1' : forms.TextInput(attrs={'oninput':'unpaved_average()', 'oninput':'autoFillZeros(id_unp_1.id)', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'unp_2' : forms.NumberInput(attrs={'oninput':'unpaved_average()', 'style': 'width: 50px; text-align: center;'}),
            'unp_3' : forms.NumberInput(attrs={'oninput':'unpaved_average()', 'style': 'width: 50px; text-align: center;'}),
            'unp_4' : forms.NumberInput(attrs={'oninput':'unpaved_average()', 'style': 'width: 50px; text-align: center;'}),
            'unp_5' : forms.NumberInput(attrs={'oninput':'unpaved_average()', 'style': 'width: 50px; text-align: center;'}),
            'unp_6' : forms.NumberInput(attrs={'oninput':'unpaved_average()', 'style': 'width: 50px; text-align: center;'}),
            'unp_7' : forms.NumberInput(attrs={'oninput':'unpaved_average()', 'style': 'width: 50px; text-align: center;'}),
            'unp_8' : forms.NumberInput(attrs={'oninput':'unpaved_average()', 'style': 'width: 50px; text-align: center;'}),
            'unp_9' : forms.NumberInput(attrs={'oninput':'unpaved_average()', 'style': 'width: 50px; text-align: center;'}),
            'unp_10' : forms.NumberInput(attrs={'oninput':'unpaved_average()', 'style': 'width: 50px; text-align: center;'}),
            'unp_11' : forms.NumberInput(attrs={'oninput':'unpaved_average()', 'style': 'width: 50px; text-align: center;'}),
            'unp_12' : forms.NumberInput(attrs={'oninput':'unpaved_average()', 'style': 'width: 50px; text-align: center;'}),
            'par_1' : forms.TextInput(attrs={'oninput':'parking_average()', 'oninput':'autoFillZeros(id_par_1.id)', 'type': 'text', 'style': 'width: 50px; text-align: center;'}),
            'par_2' : forms.NumberInput(attrs={'oninput':'parking_average()', 'style': 'width: 50px; text-align: center;'}),
            'par_3' : forms.NumberInput(attrs={'oninput':'parking_average()', 'style': 'width: 50px; text-align: center;'}),
            'par_4' : forms.NumberInput(attrs={'oninput':'parking_average()', 'style': 'width: 50px; text-align: center;'}),
            'par_5' : forms.NumberInput(attrs={'oninput':'parking_average()', 'style': 'width: 50px; text-align: center;'}),
            'par_6' : forms.NumberInput(attrs={'oninput':'parking_average()', 'style': 'width: 50px; text-align: center;'}),
            'par_7' : forms.NumberInput(attrs={'oninput':'parking_average()', 'style': 'width: 50px; text-align: center;'}),
            'par_8' : forms.NumberInput(attrs={'oninput':'parking_average()', 'style': 'width: 50px; text-align: center;'}),
            'par_9' : forms.NumberInput(attrs={'oninput':'parking_average()', 'style': 'width: 50px; text-align: center;'}),
            'par_10' : forms.NumberInput(attrs={'oninput':'parking_average()', 'style': 'width: 50px; text-align: center;'}),
            'par_11' : forms.NumberInput(attrs={'oninput':'parking_average()', 'style': 'width: 50px; text-align: center;'}),
            'par_12' : forms.NumberInput(attrs={'oninput':'parking_average()', 'style': 'width: 50px; text-align: center;'}),
            'pav_total' : forms.NumberInput(attrs={'oninput':'paved_average()', 'style': 'width: 50px; text-align: center;'}),
            'unp_total' : forms.NumberInput(attrs={'oninput':'unpaved_average()', 'style': 'width: 50px; text-align: center;'}),
            'par_total' : forms.NumberInput(attrs={'oninput':'parking_average()', 'style': 'width: 50px; text-align: center;'}),
        }
class formO_form(ModelForm):
    class Meta:
        model = form24_model
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
        model = form25_model
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
            'form' : forms.TextInput(attrs={'type':'text', 'style':'width:50px; text-align: center; border: 1px solid black;'}),
            'issues' : Textarea(attrs={'rows':7, 'style':'width: 100%; border-radius: 18px; padding: .5rem;'}),
            'notified' : forms.TextInput(attrs={'type':'text', 'style':'width:150px; border-radius: 5px; background-color: white; border: 1px solid black; padding-left: .5rem;'}),
            'time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px; border-radius: 5px; background-color: white; border: 1px solid black;'}),
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px; border-radius: 5px; background-color: white; border: 1px solid black;'}),
            'cor_action' : Textarea(attrs={'rows':7, 'style':'width: 100%; border-radius: 18px; padding: .5rem;'}),
        }

class events_form(ModelForm):
    class Meta:
        model = Event
        fields = ('__all__')
        widgets = {
            'observer' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'title' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'description' : forms.TextInput(attrs={'type':'text', 'style':'width:150px;'}),
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'start_time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'end_time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
        }
class spill_kits_form(ModelForm):
    class Meta:
        all_spks = False
        today = datetime.date.today()
        if (today.month in {1, 3, 5, 7, 8, 10, 12} and today.day == 31) or (today.month in {4, 6, 9, 11} and today.day == 30) or (today.month == 2 and today.day == 29):
            all_spks = True
        elif today.month == 2 and today.day == 28:
            all_spks = True
        
        model = form29_model
        fields = ('__all__')
        widgets = {
            'observer' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'month' : forms.TextInput(attrs={'type':'text', 'style':'width: 70px; text-align: center;'}),
            
            'sk1_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk2_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk3_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk4_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk5_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk6_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk7_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk8_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk9_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk10_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk11_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk12_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk13_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk14_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk15_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk16_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk17_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk18_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk19_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk20_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            'sk21_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySK()', 'style':'width: 50px;', 'required': all_spks}),
            
            'skut22_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySKUT()', 'style':'width: 50px;', 'required': all_spks}),
            'skut23_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySKUT()', 'style':'width: 50px;', 'required': all_spks}),
            'skut24_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySKUT()', 'style':'width: 50px;', 'required': all_spks}),
            'skut25_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySKUT()', 'style':'width: 50px;', 'required': all_spks}),
            'skut26_tag_on' : forms.Select(attrs={'oninput': 'rows_true()', 'onchange': 'showInventorySKUT()', 'style':'width: 50px;', 'required': all_spks}),
            
            'sk1_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk2_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk3_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk4_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk5_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk6_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk7_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk8_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk9_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk10_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk11_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk12_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk13_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk14_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk15_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk16_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk17_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk18_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk19_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk20_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'sk21_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            
            'skut22_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'skut23_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'skut24_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'skut25_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            'skut26_serial' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 70px; text-align: center;', 'required': all_spks}),
            
            'sk1_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk2_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk3_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk4_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk5_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk6_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk7_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk8_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk9_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk10_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk11_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk12_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk13_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk14_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk15_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk16_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk17_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk18_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk19_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk20_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'sk21_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            
            'skut22_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'skut23_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'skut24_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'skut25_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            'skut26_complete' : forms.Select(attrs={'oninput': 'rows_true()', 'style':'width: 50px;', 'required': all_spks}),
            
            'sk1_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk2_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk3_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk4_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk5_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk6_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk7_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk8_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk9_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk10_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk11_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk12_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk13_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk14_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk15_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk16_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk17_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk18_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk19_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk20_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk21_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            
            'skut22_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'skut23_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'skut24_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'skut25_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'skut26_report' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            
            'sk1_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk2_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk3_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk4_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk5_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk6_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk7_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk8_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk9_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk10_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk11_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk12_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk13_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk14_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk15_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk16_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk17_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk18_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk19_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk20_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'sk21_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            
            'skut22_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'skut23_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'skut24_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'skut25_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            'skut26_comment' : forms.TextInput(attrs={'oninput': 'rows_true()', 'type':'text', 'style':'width: 130px; text-align: center;', 'required': all_spks}),
            
        }
class quarterly_trucks_form(ModelForm):
    class Meta:
        model = form27_model
        fields = ('__all__')
        widgets = {
            'quarter': forms.Select(attrs={'style':'width: 50px; border-radius: 15px; font-size: 1rem; text-align: center; border-width: 2px; border-style: inset; border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));'}),
            'date': forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'observer_5_1': forms.TextInput(attrs={'style':'width: 150px;'}),
            'date_5_1': forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'time_5_1': forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'comments_5_1': forms.Textarea(attrs={'rows': '3', 'type':'text', 'style':'width: 463px; font-size: 1.5rem; border-radius: 15px; height: 8rem;'}),
            'rear_gate_5_1': forms.Select(attrs={'style':'width: 50px;'}),
            'box_interior_5_1': forms.Select(attrs={'style':'width: 50px;'}),
            'box_exterior_5_1': forms.Select(attrs={'style':'width: 50px;'}),
            'exhaust_5_1': forms.Select(attrs={'style':'width: 50px;'}),
            'observer_6_2': forms.TextInput(attrs={'style':'width: 150px;'}),
            'date_6_2': forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'time_6_2': forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'comments_6_2': forms.Textarea(attrs={'rows': '3', 'type':'text', 'style':'width: 463px; font-size: 1.5rem; border-radius: 15px; height: 8rem;'}),
            'rear_gate_6_2': forms.Select(attrs={'style':'width: 50px;'}),
            'box_interior_6_2': forms.Select(attrs={'style':'width: 50px;'}),
            'box_exterior_6_2': forms.Select(attrs={'style':'width: 50px;'}),
            'exhaust_6_2': forms.Select(attrs={'style':'width: 50px;'}),
            'observer_7_3': forms.TextInput(attrs={'style':'width: 150px;'}) ,
            'date_7_3': forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'time_7_3': forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'comments_7_3': forms.Textarea(attrs={'rows': '3', 'type':'text', 'style':'width: 463px; font-size: 1.5rem; border-radius: 15px; height: 8rem;'}),
            'rear_gate_7_3': forms.Select(attrs={'style':'width: 50px;'}),
            'box_interior_7_3': forms.Select(attrs={'style':'width: 50px;'}),
            'box_exterior_7_3': forms.Select(attrs={'style':'width: 50px;'}),
            'exhaust_7_3': forms.Select(attrs={'style':'width: 50px;'}),
            'observer_9_4': forms.TextInput(attrs={'style':'width: 150px;'}),
            'date_9_4': forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'time_9_4': forms.TimeInput(attrs={'type':'time', 'style':'width: 120px;'}),
            'comments_9_4': forms.Textarea(attrs={'rows': '3', 'type':'text', 'style':'width: 463px; font-size: 1.5rem; border-radius: 15px; height: 8rem;'}),
            'rear_gate_9_4': forms.Select(attrs={'style':'width: 50px;'}),
            'box_interior_9_4': forms.Select(attrs={'style':'width: 50px;'}),
            'box_exterior_9_4': forms.Select(attrs={'style':'width: 50px;'}),
            'exhaust_9_4': forms.Select(attrs={'style':'width: 50px;'}),
        }
        
class sop_form(ModelForm):
    class Meta:
        model = sop_model
        fields = ('__all__')
        widgets = {
            'name' : forms.TextInput(attrs={'style':'width: 150px;'}),
            'revision_date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'pdf_url' : forms.TextInput(attrs={'oninput': 'pdf_link_change()' , 'type':'text', 'style':'width:150px; display: none;', 'required':False}),
        }
        
class signature_form(ModelForm):
    class Meta:
        model = signature_model
        fields = ('__all__')
        widgets = {
            'supervisor': forms.TextInput(attrs={'type': 'text', 'id': 'form_name', 'style': 'font-size: 1.2rem;width: 13rem;border-radius: 1rem; text-align: center;'}),
            'sign_date': forms.DateInput(attrs={'type': 'hidden', 'id': 'form_date', 'style': ''}),
            'canvas': forms.TextInput(attrs={'type': 'hidden', 'id': 'form_canvas', 'style': ''}),
        }
     
class company_form(ModelForm):
    class Meta:
        model = company_model
        fields = ('__all__')
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder':'Company Name', 'style':'width: 250px;'}),
            'address': forms.TextInput(attrs={'placeholder':'Street Address', 'style':'width: 250px;'}),
            'city': forms.TextInput(attrs={'placeholder':'City', 'style':'width: 250px;'}),
            'state': forms.TextInput(attrs={'placeholder':'State', 'style':'width: 250px;'}),
            'zipcode': forms.TextInput(attrs={'placeholder':'Zipcode', 'style':'width: 250px;'}),
            'phone': forms.TextInput(attrs={'placeholder':'Phone', 'oninput':"processPhone(event)", 'style':'width: 250px;'}),
            'customerID': forms.TextInput(attrs={'style':'width: 250px;'}),
        }   

class company_Update_form(ModelForm):
    class Meta:
        model = company_model
        fields = ('__all__')
        widgets = {
            'company_name': forms.TextInput(attrs={'class':'input', 'style':'width:100%;'}),
            'address': forms.TextInput(attrs={'class':'input', 'style':'width:100%;'}),
            'city': forms.TextInput(attrs={'class':'input', 'style':'width:9rem;'}),
            'state': forms.TextInput(attrs={'class':'input', 'placeholder':'State', 'style':'width:3rem;'}),
            'zipcode': forms.TextInput(attrs={'class':'input', 'style':'width: 4rem;'}),
            'phone': forms.TextInput(attrs={'class':'input', 'oninput':"processPhone(event)", 'placeholder':'(123)456-7890', 'style':'width: 100%;'}),
            'customerID': forms.TextInput(attrs={'class':'input', 'style':'width: 250px;'}),
        }   
        
class facility_forms_form(ModelForm):
    class Meta:
        model = facility_forms_model
        fields = ('__all__')
        
class spill_kit_inventory_form(ModelForm):
    class Meta:
        model = form26_model
        fields = ('__all__')
        widgets = {
            "date": forms.DateInput(attrs={'type': 'date'}),
            "inspector": forms.TextInput(attrs={'type': 'text'}),
            "skID": forms.NumberInput(attrs={'type': 'number', 'style': 'width:50px; text-align:center'}),
            "type": forms.Select(attrs={"id": "skType", "onchange": "selectType()"}),
            "counted_items": forms.NumberInput(attrs={'type': 'number'}),
            "missing_items": forms.NumberInput(attrs={'type': 'number'}),
        }
        
class formSubmissionRecords_form(ModelForm):
    class Meta:
        model = formSubmissionRecords_model
        fields = ('__all__')
        widgets = {
            'formID': forms.NumberInput(attrs={'type': 'number'}),
            'dateSubmitted': forms.DateInput(attrs={'type': 'date'}),
            'dueDate': forms.DateInput(attrs={'type': 'date'}),
            'facilityChoice': forms.Select(attrs={}),
            'submitted': forms.CheckboxInput(attrs={})
        }
        
class braintree_form(ModelForm):
    class Meta:
        model = braintree_model
        fields = ('__all__')
        widgets = {}
        
class FAQ_form(ModelForm):
    class Meta:
        model = FAQ_model
        fields = ('__all__')
        widgets = {}
        
class form_requests_form(ModelForm):
    class Meta:
        model = form_requests_model
        fields = ('__all__')
        widgets = {
            'user': forms.Select(),
            'name': forms.TextInput(attrs={'placeholder':'Form Title'}),
            'type': forms.TextInput(attrs={'placeholder':'Type (ie. Environmental, Structural, Mechanical...)'}),
            'how_data_is_collected': forms.Textarea(attrs={'placeholder':'What is the method or process of collecting data for this form?'}),
            'inspection_of': forms.Textarea(attrs={'placeholder':'Describe what is being inspected.'}),
            'form_example_file': forms.FileInput(attrs={}),
            'form_example_url': forms.TextInput(attrs={}),
            'optimize': forms.CheckboxInput(),
            'detailed_description': forms.Textarea(attrs={'placeholder':'Detailed description of form including any other notes or details of functionality.'}),
            'callBack_days': forms.Select(attrs={'style':'width:50%;'}),
            'callBack_time': forms.TimeInput(attrs={'type':'time'}),
            'callBack_time_freq': forms.Select(attrs={}),
            'frequency': forms.Select(attrs={}),
        }
        
class the_packets_form(ModelForm):
    class Meta:
        model = the_packets_model
        fields = ('__all__')
        widgets = {
            'facilityChoice': forms.Select(choices=frequent_choices),
            'name': forms.TextInput(attrs={'type':'text', 'placeholder':'Enter packet name...'}),
            'formList': forms.TextInput(),
        }
        
class form_settings_form(ModelForm):
    class Meta:
        model = form_settings_model
        fields = ('__all__')
        widgets = {
            'facilityChoice': forms.Select(attrs={}),
            'formChoice': forms.Select(attrs={}),
            'packetChoice': forms.Select(attrs={}),
            'settings': forms.TextInput(),
        }

class CustomSelectWidget(forms.Select):
    """Custom Select Widget to add data-submitted attribute to options."""
    
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)

        # 🔥 Add the `data-submitted` attribute with default "false"
        option["attrs"]["data-submitted"] = "false"
        return option   

class form30_form(forms.ModelForm):
    class Meta:
        model = form30_model
        fields = "__all__"
        widgets = {
            "observer": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Observer Name"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)
        super().__init__(*args, **kwargs)

        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form30_form.")

        # Extract facility settings from form_settings
        settings = form_settings.settings.get("settings", {}) if hasattr(form_settings, "settings") else {}

        # Load area_name options from settings JSON
        area_choices = [("", "Select Area")]
        num_of_areas = settings.get("num_of_areas", 0)
        for i in range(1, num_of_areas + 1):
            area_key = f"area{i}"
            if area_key in settings:
                area_choices.append((settings[area_key], settings[area_key]))

        self.fields["area_name"] = forms.ChoiceField(
            choices=area_choices,
            required=True,
            widget=CustomSelectWidget(attrs={"class": "form-control"}),
        )

        # Load inspection_json (Status Checks)
        instance = kwargs.get("instance")
        initial_data = kwargs.get("initial", {})  # ✅ Check if initial values are provided

        if instance and hasattr(instance, "inspection_json"):
            inspection_data = instance.inspection_json or {}  # ✅ Get saved data
        else:
            inspection_data = initial_data.get("inspection_json", {})  # ✅ Use initial if available

        print("Loaded inspection_json:", inspection_data)  # Debugging output


        for i in range(1, 7):  # Assuming 6 status checks
            check_data = inspection_data.get(f"check{i}", {})  # 🔥 Get check data as a dictionary
            print(f"Check {i}: {check_data}")  # Check what is being loaded
            self.fields[f"check{i}"] = forms.ChoiceField(
                choices=[("OK", "OK"), ("N/A", "N/A"), ("Not OK", "Not OK")],
                required=False,
                widget=forms.RadioSelect(attrs={"class": "status-radio"}),
                initial=check_data.get("status", ""),
            )
            self.fields[f"comments{i}"] = forms.CharField(
                required=False,
                widget=forms.Textarea(attrs={"rows": "4", "class": "status-comment", "placeholder": "Add comment..."}),
                initial=check_data.get("comment", ""),
            )

    def clean_inspection_json(self):
        """Ensure the JSON data is valid for status checks"""
        data = self.cleaned_data.get("inspection_json")
        if not isinstance(data, dict):
            raise forms.ValidationError("Invalid data format for inspection status.")
        return data

    def clean_containers_json(self):
        """Ensure the JSON data is valid for waste containers"""
        data = self.cleaned_data.get("containers_json")
        if not isinstance(data, dict):
            raise forms.ValidationError("Invalid data format for containers.")
        return data

