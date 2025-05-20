from django import forms # type: ignore
from django.forms import ModelForm, Textarea # type: ignore
from django.contrib.auth.forms import UserCreationForm, UserChangeForm # type: ignore
from django.contrib.auth.models import User # type: ignore
import datetime
import re
from PIL import Image # type: ignore
from io import BytesIO
from .models import *
from types import SimpleNamespace

now = datetime.datetime.now()

#Create Your Forms here

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
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email has already been used. Please enter a different email.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username', '').lower()
        
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username already exists. Please enter a different username.")
        
        return username

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
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        # Strip out common formatting characters
        digits_only = re.sub(r'\D', '', phone or "")
        
        if len(digits_only) < 10:
            raise ValidationError("Please enter a valid phone number. (e.g., 1234567890, (123)456-7890)")

        return phone

class pt_admin1_form(ModelForm):
    class Meta:
        model = pt_admin1_model
        fields = ('add_days', 'days_left')

class bat_info_form(ModelForm):
    class Meta:
        model = facility_model
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
            'address': forms.TextInput(attrs={'type': 'text','class':'input', 'style': 'width:100%;', 'autocomplete': 'on'}),
            'state': forms.TextInput(attrs={'type': 'text', 'class':'input', 'placeholder':'XX', 'style': 'width: 3rem;'}),
            'district': forms.TextInput(attrs={'type': 'text','class':'input', 'style': 'width: 9rem;'}),
            'city': forms.TextInput(attrs={'type': 'text','class':'input', 'style': 'width: 140px;'}),
            'bat_height': forms.NumberInput(attrs={'type': 'number','class':'input', 'style': 'width: 6rem;'}),
            'bat_height_label': forms.Select(attrs={'class':'input', 'style':'height: 37px; width: 81px;'}),
            'bat_main': forms.Select(attrs={'class':'input', 'style':'height: 37px; width: 81px;'}),
            'bat_lids': forms.NumberInput(attrs={'type': 'number','class':'input', 'style': 'width: 6rem;'}),
            'is_battery': forms.Select(attrs={'class':'input', 'style':'height: 37px; width: 81px;'}),
            'zipcode': forms.TextInput(attrs={'class':'input', 'style':'width: 4rem;'}),
        }

class form1_form(ModelForm):
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
        'c1_start': forms.TimeInput(attrs={'oninput': 'timecheck_c1()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'c2_start': forms.TimeInput(attrs={'oninput': 'timecheck_c2()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'c3_start': forms.TimeInput(attrs={'oninput': 'timecheck_c3()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'c4_start': forms.TimeInput(attrs={'oninput': 'timecheck_c4()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'c5_start': forms.TimeInput(attrs={'oninput': 'timecheck_c5()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'c1_stop': forms.TimeInput(attrs={'oninput': 'timecheck_c1()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'c2_stop': forms.TimeInput(attrs={'oninput': 'timecheck_c2()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'c3_stop': forms.TimeInput(attrs={'oninput': 'timecheck_c3()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'c4_stop': forms.TimeInput(attrs={'oninput': 'timecheck_c4()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'c5_stop': forms.TimeInput(attrs={'oninput': 'timecheck_c5()', 'onchange': 'equal_start_stop()', 'type': 'time', 'style': 'width: 130px;', "required": True}),
        'larry_car': forms.Select(attrs={'style': 'width: 60px;'}),
        'total_seconds': forms.NumberInput(attrs={'id': 'total_seconds', 'oninput': 'sumTime()', 'min': '0', 'readonly': True, 'type': 'number', 'step': '0.5', 'style': 'width: 60px; text-align: center;'}),
    }

    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)

        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form1_form.")
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
    
class form2_form(ModelForm):
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
            'p_start': forms.TimeInput(attrs={'oninput': 'timecheck_pushDoors()', 'type': 'time', 'style': 'width: 120px;', 'required': True}),
            'p_stop': forms.TimeInput(attrs={'oninput': 'timecheck_pushDoors()', 'type': 'time', 'style': 'width: 120px;', 'required': True}),
            'c_start': forms.TimeInput(attrs={
                'oninput': 'timecheck_cokeDoors()',
                'type': 'time',
                'style': 'width: 120px;', 
                'required': True
            }),
            'c_stop': forms.TimeInput(attrs={
                'oninput': 'timecheck_cokeDoors()',
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
    
    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)

        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form1_form.")
        """ Extract JSON values and create dynamic form fields with the correct styles. """
        super().__init__(*args, **kwargs)

class form3_form(ModelForm):
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

    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)

        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form1_form.")
        """ Extract JSON values and create dynamic form fields with the correct styles. """
        super().__init__(*args, **kwargs)

class form4_form(ModelForm):
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
    
    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)

        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form1_form.")
        """ Extract JSON values and create dynamic form fields with the correct styles. """
        super().__init__(*args, **kwargs)

class form5_form(ModelForm):
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
            choices=[("", "---------"),("N/A", "N/A"),("Fugitive", "Fugitive"),("Continuous", "Continuous"),("Intermittent", "Intermittent")],
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
        'o1_start' : forms.TimeInput(attrs={'oninput': 'timecheck_pt1()', 'type':'time', 'style':'width: 120px;', 'required':True}),
        'o1_stop' : forms.TimeInput(attrs={'oninput': 'timecheck_pt1()', 'type':'time', 'style':'width: 120px;', 'required':True}),
        'o2_start' : forms.TimeInput(attrs={'oninput': 'timecheck_pt2()', 'type':'time', 'style':'width: 120px;', 'required':True}),
        'o2_stop' : forms.TimeInput(attrs={'oninput': 'timecheck_pt2()', 'type':'time', 'style':'width: 120px;', 'required':True}),
        'o3_start' : forms.TimeInput(attrs={'oninput': 'timecheck_pt3()', 'type':'time', 'style':'width: 120px;', 'required':True}),
        'o3_stop' : forms.TimeInput(attrs={'oninput': 'timecheck_pt3()', 'type':'time', 'style':'width: 120px;', 'required':True}),
        'o4_start' : forms.TimeInput(attrs={'oninput': 'timecheck_pt4()', 'type':'time', 'style':'width: 120px;', 'required':True}),
        'o4_stop' : forms.TimeInput(attrs={'oninput': 'timecheck_pt4()', 'type':'time', 'style':'width: 120px;', 'required':True}),
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
        form_settings = kwargs.pop("form_settings", None)

        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form1_form.")
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
 
class form6_form(ModelForm):
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
    
    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)

        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form1_form.")
        """ Extract JSON values and create dynamic form fields with the correct styles. """
        super().__init__(*args, **kwargs)

class form7_form(ModelForm):
    class Meta:
        model = form7_model
        fields = ('__all__')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'observer': forms.TextInput(attrs={'style': 'width: 150px;', "maxlength": "30", "required": True}),
            'cert_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'comments': Textarea(attrs={'rows': 7, 'cols': 125, "maxlength": "30", "required": True}),
        }

    DEFAULT_READING_FIELDS = {
        **{f"1Read_{i}": "" for i in range(1,13)},
        **{f"2Read_{i}": "" for i in range(1,13)},
        **{f"3Read_{i}": "" for i in range(1,13)},
        **{f"4Read_{i}": "" for i in range(1,13)},
        **{f"{i}_start": "" for i in range(1,5)},
        **{f"{i}_stop": "" for i in range(1,5)},
        **{f"{i}_selection": "" for i in range(1,5)},
        **{f"{i}_average": "" for i in range(1,5)}
    }
    
    JSON_WIDGET_STYLES = {
        **{f"1Read_{i}": forms.NumberInput(attrs={'oninput': f"area1_average();", 'class': 'input', 'type': 'number', 'style': 'text-align: center;', 'maxlength': 3}) for i in range(1,13)},
        **{f"2Read_{i}": forms.NumberInput(attrs={'oninput': f"area2_average(); autoFillZeros(2Read_{i}.id);", 'class': 'input', 'type': 'number', 'style': 'text-align: center;', 'maxlength': 3}) for i in range(1,13)},
        **{f"3Read_{i}": forms.NumberInput(attrs={'oninput': f"area3_average(); autoFillZeros(3Read_{i}.id);", 'class': 'input', 'type': 'number', 'style': 'text-align: center;', 'maxlength': 3}) for i in range(1,13)},
        **{f"4Read_{i}": forms.NumberInput(attrs={'oninput': f"area4_average(); autoFillZeros(4Read_{i}.id);", 'class': 'input', 'type': 'number', 'style': 'text-align: center;', 'maxlength': 3}) for i in range(1,13)},
        **{f"{i}_start": forms.TimeInput(attrs={'type': 'time', "oninput": f"formC_timeCheck_area{i}()", "class": "input", 'style': 'width: 95px;'}) for i in range(1,5)},
        **{f"{i}_stop": forms.TimeInput(attrs={'type': 'time', "oninput": f"formC_timeCheck_area{i}()", "class": "input", 'style': 'width: 95px;'}) for i in range(1,5)},
        **{f"{i}_selection": forms.Select(attrs={"class": "input"}) for i in range(1,5)},
        **{f"{i}_average": forms.NumberInput(attrs={'type': 'number', "oninput": f"area{i}_average()", "class": "input", 'style': 'width: 95px;', "maxlength": "3", "required": True}) for i in range(1,5)},
    }
    
    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)
        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form7_form.")

        initial = kwargs.get("initial", {})
        instance = kwargs.get("instance")

        # Determine the data source: use instance if it exists, otherwise use initial
        data_source = instance if instance else SimpleNamespace(**initial)

        # Extract facility settings from form_settings
        settings = form_settings.settings.get("settings", {}) if hasattr(form_settings, "settings") else {}
        # Load area_name options from settings JSON
        num_of_areas = settings.get("number_of_areas", 0)
        print(f"These are the settings {num_of_areas}")
        area_choices_dict = {}
        for i in range(1, num_of_areas + 1):
            area_key = f"area{i}"
            if area_key in settings:
                areaData = settings[area_key]
                if areaData['number_of_options'] > 0:
                    emptyChoice = [("", "Select Choice")]
                    selectionList = emptyChoice + [(areaName, areaName) for areaKey, areaName in areaData['options'].items()]
                else:
                    selectionList = False
                area_choices_dict[f"area_choices_{i}"] = selectionList
            else:
                print("No Area Data")
        print(f"These are the choices: {area_choices_dict}")
        super().__init__(*args, **kwargs)

        json_data_1 = getattr(data_source, "area_json_1", {}) or {}
        json_data_2 = getattr(data_source, "area_json_2", {}) or {}
        json_data_3 = getattr(data_source, "area_json_3", {}) or {}
        json_data_4 = getattr(data_source, "area_json_4", {}) or {}
        json_dict = {
            "1": json_data_1,
            "2": json_data_2,
            "3": json_data_3,
            "4": json_data_4,
        }

        general_fields = [
            "date", "estab", "county", "estab_no", "equip_loc",
            "district", "city", "observer", "cert_date"
        ]

        for field in general_fields:
            if field in self.fields:  # Ensure the field exists in the form before setting
                self.fields[field].initial = initial.get(field, getattr(data_source, field, None))

        for i in range(1, 13):
            for x in range(1,num_of_areas + 1):
                field_name = f"{x}Read_{i}"
                widget = self.JSON_WIDGET_STYLES.get(field_name, forms.NumberInput(attrs={"type": "number", "style": "width: 50px; text-align: center;"}))
                self.fields[field_name] = forms.IntegerField(
                    initial=json_dict[str(x)].get("readings", {}).get(field_name, None),
                    required=False,
                    widget=widget
                )
        print(json_dict[str(1)].get(f"1_selection", "selection"))
        for i in range(1,num_of_areas + 1):
            areaSelectChoices = area_choices_dict[f"area_choices_{i}"] if area_choices_dict[f"area_choices_{i}"] else []
            self.fields[f"{i}_selection"] = forms.ChoiceField(
                choices=areaSelectChoices,
                initial=json_dict[str(i)].get(f"{i}_selection") or json_dict[str(i)].get("selection"),
                required=False,
                widget=self.JSON_WIDGET_STYLES.get(f"{i}_selection")
            )
            self.fields[f"{i}_start"] = forms.TimeField(
                initial=json_dict[str(i)].get(f"{i}_start") or json_dict[str(i)].get("start"),
                required=False,
                widget=self.JSON_WIDGET_STYLES.get(f"{i}_start")
            )
            self.fields[f"{i}_stop"] = forms.TimeField(
                initial=json_dict[str(i)].get(f"{i}_stop") or json_dict[str(i)].get("stop"),
                required=False,
                widget=self.JSON_WIDGET_STYLES.get(f"{i}_stop")
            )
            self.fields[f"{i}_average"] = forms.FloatField(
                initial=json_dict[str(i)].get(f"{i}_average") or json_dict[str(i)].get("average"),
                required=False,
                widget=self.JSON_WIDGET_STYLES.get(f"{i}_average")
            )

class form8_form(ModelForm):
    class Meta:
        model = form8_model
        fields = ('__all__')
        
        widgets = {
            'week_start': forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'week_end': forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'truck_id1' : forms.Select(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'date1' : forms.DateInput(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()', 'type':'date'}),
            'time1' : forms.TimeInput(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()', 'type':'time'}),
            'contents1' : forms.Select(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'truck_id2' : forms.Select(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'date2' : forms.DateInput(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()', 'type':'date'}),
            'time2' : forms.TimeInput(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()', 'type':'time'}),
            'contents2' : forms.Select(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'truck_id3' : forms.Select(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'date3' : forms.DateInput(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()', 'type':'date'}),
            'time3' : forms.TimeInput(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()', 'type':'time'}),
            'contents3' : forms.Select(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'truck_id4' : forms.Select(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'date4' : forms.DateInput(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()', 'type':'date'}),
            'time4' : forms.TimeInput(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()', 'type':'time'}),
            'contents4' : forms.Select(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'truck_id5' : forms.Select(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'date5' : forms.DateInput(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()', 'type':'date'}),
            'time5' : forms.TimeInput(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()', 'type':'time'}),
            'contents5' : forms.Select(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'freeboard1' : forms.Select(attrs={'class': 'baseInput', 'oninput': 'freeboard(this)'}),
            'freeboard2' : forms.Select(attrs={'class': 'baseInput', 'oninput': 'freeboard(this)'}),
            'freeboard3' : forms.Select(attrs={'class': 'baseInput', 'oninput': 'freeboard(this)'}),
            'freeboard4' : forms.Select(attrs={'class': 'baseInput', 'oninput': 'freeboard(this)'}),
            'freeboard5' : forms.Select(attrs={'class': 'baseInput', 'oninput': 'freeboard(this)'}),
            'wetted1' : forms.Select(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'wetted2' : forms.Select(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'wetted3' : forms.Select(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'wetted4' : forms.Select(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'wetted5' : forms.Select(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'comments1' : forms.Textarea(attrs={'class': 'textBox', 'maxlength': '30', 'rows': '3', 'cols': '40', 'onchange': 'if_one_then_all()', 'type':'text'}),
            'comments2' : forms.Textarea(attrs={'class': 'textBox', 'maxlength': '30', 'rows': '3', 'cols': '40', 'onchange': 'if_one_then_all()', 'type':'text'}),
            'comments3' : forms.Textarea(attrs={'class': 'textBox', 'maxlength': '30', 'rows': '3', 'cols': '40', 'onchange': 'if_one_then_all()', 'type':'text'}),
            'comments4' : forms.Textarea(attrs={'class': 'textBox', 'maxlength': '30', 'rows': '3', 'cols': '40', 'onchange': 'if_one_then_all()', 'type':'text'}),
            'comments5' : forms.Textarea(attrs={'class': 'textBox', 'maxlength': '30', 'rows': '3', 'cols': '40', 'onchange': 'if_one_then_all()', 'type':'text'}),
            'observer1' : forms.TextInput(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'observer2' : forms.TextInput(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'observer3' : forms.TextInput(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'observer4' : forms.TextInput(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
            'observer5' : forms.TextInput(attrs={'class': 'baseInput', 'onchange': 'if_one_then_all()'}),
        }
    
    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)

        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form1_form.")

        # Extract 'initial' and 'instance' data
        initial = kwargs.get("initial", {})
        instance = kwargs.get("instance")

        #print(initial)

        # Ensure we are using an object that can retrieve attributes
        data_source = instance if instance else initial

        """ Extract JSON values and create dynamic form fields with the correct styles. """
        super().__init__(*args, **kwargs)
        # print(f"The meta fields: {self.fields}")
        # print(f"The data source: {data_source}")
        # # Dynamically populate fields from instance or initial data
        # for field_name in self.fields.keys():
        #     print(field_name)
        #     if field_name in data_source:
        #         print(f"For {field_name} it takes the input: {data_source.get(field_name, None)}")
        #         self.fields[field_name].initial = data_source.get(field_name, None)

class form9_form(ModelForm):
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

    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)

        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form1_form.")
        """ Extract JSON values and create dynamic form fields with the correct styles. """
        super().__init__(*args, **kwargs)

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

class form17_form(ModelForm):
    class Meta:
        model = form17_model
        fields = ('__all__')
        
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'cert_date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'estab_no': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 80px; text-align: center;'}),
            'observer': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'canvas': forms.TextInput(attrs={'id': 'canvas', 'type': 'hidden', 'class': 'input', 'style': 'width:50px; text-align: center;', "required": "true"})
        }

    DEFAULT_READING_FIELDS = {
        "process_equip1": "", "process_equip2": "", "op_mode1": "normal", "op_mode2": "normal",
        "background_color_start": "", "background_color_stop": "", "sky_conditions": "",
        "wind_speed_start": "", "wind_speed_stop": "", "wind_direction": "",
        "emission_point_start": "", "emission_point_stop": "",
        "ambient_temp_start": "", "ambient_temp_stop": "", "humidity": "",
        "height_above_ground": "", "height_rel_observer": "",
        "distance_from": "", "direction_from": "",
        "describe_emissions_start": "", "describe_emissions_stop": "",
        "emission_color_start": "", "emission_color_stop": "",
        "plume_type": "", "water_drolet_present": "",
        "water_droplet_plume": "", "plume_opacity_determined_start": "", "plume_opacity_determined_stop": "",
        "describe_background_start": "", "describe_background_stop": "",
        "PEC_start": "", "PEC_stop": "",
        **{f"PEC_read_{i}": "" for i in range(1, 25)},  # Generates PEC_read_1 to PEC_read_24
        "PEC_oven1": "", "PEC_oven2": "", "PEC_time1": "", "PEC_time2": "",
        "PEC_type": "", "PEC_average": "", "PEC_push_oven": "",
        "PEC_push_time": "", "PEC_observe_time": "", "PEC_emissions_present": ""
    }

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
            choices=[("", "---------"),("N/A", "N/A"),("Fugitive", "Fugitive"),("Continuous", "Continuous"),("Intermittent", "Intermittent")],
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
        "PEC_start": forms.TimeInput(attrs={'type': 'time', 'style': 'width: 95px;'}),
        "PEC_stop": forms.TimeInput(attrs={'type': 'time', 'style': 'width: 95px;'}),
        "PEC_oven1": forms.NumberInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
        "PEC_oven2": forms.NumberInput(attrs={'type': 'number', 'style': 'width: 50px; text-align: center;'}),
        "PEC_time1": forms.TimeInput(attrs={'type': 'time', 'style': 'width: 95px;'}),
        "PEC_time2": forms.TimeInput(attrs={'type': 'time', 'style': 'width: 95px;'}),
        **{f"PEC_read_{i}": forms.NumberInput(attrs={"type": "number", "style": "width: 50px; text-align: center;"}) for i in range(1, 25)},  # Restore number input
        'PEC_type' : forms.TextInput(attrs={'type': 'hidden'}),
        "PEC_average": forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
        "PEC_push_oven": forms.NumberInput(attrs={"class": "input", "type": "number", "style": "width: 50px; text-align: center;"}),
        "PEC_push_time": forms.TimeInput(attrs={"type": "time", "style": "width: 95px;"}),
        "PEC_observe_time": forms.TimeInput(attrs={"type": "time", "style": "width: 95px;"}),
        "PEC_emissions_present": forms.RadioSelect(attrs={"class": "status-radio"})
    }

    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)
        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form17_form.")

        initial = kwargs.get("initial", {})
        instance = kwargs.get("instance")

        # Determine the data source: use instance if it exists, otherwise use initial
        data_source = instance if instance else SimpleNamespace(**initial)

        super().__init__(*args, **kwargs)

        # Extract JSON-stored data
        existing_data = getattr(data_source, "reading_data", {}) or {}
        existing_ovens_data = getattr(data_source, "ovens_data", {}) or {}
        type_of_form = existing_ovens_data.get("PEC_type", None)

        general_fields = [
            "date", "estab", "county", "estab_no", "equip_loc",
            "district", "city", "observer", "cert_date"
        ]
    
        for field in general_fields:
            if field in self.fields:  # Ensure the field exists in the form before setting
                self.fields[field].initial = initial.get(field, getattr(data_source, field, None))

        # Handle all fields dynamically, merging data from the source
        for field_name, default_value in self.DEFAULT_READING_FIELDS.items():
            widget = self.JSON_WIDGET_STYLES.get(field_name, forms.TextInput(attrs={"class": "input"}))
            self.fields[field_name] = forms.CharField(
                initial=existing_data.get(field_name, default_value),
                required=False,
                widget=widget
            )

        # Assign PEC type field
        self.fields["PEC_type"] = forms.CharField(
            initial=existing_ovens_data.get("PEC_type", None),
            required=False,
            widget=self.JSON_WIDGET_STYLES.get("PEC_type", forms.TextInput(attrs={"class": "input"}))
        )

        # Assign PEC fields based on type
        if type_of_form == "meth9":
            for i in range(1, 25):
                field_name = f"PEC_read_{i}"
                widget = self.JSON_WIDGET_STYLES.get(field_name, forms.NumberInput(attrs={"type": "number", "style": "width: 50px; text-align: center;"}))
                self.fields[field_name] = forms.IntegerField(
                    initial=existing_ovens_data.get("meth9", {}).get("readings", {}).get(field_name, None),
                    required=False,
                    widget=widget
                )

            self.fields["PEC_oven1"] = forms.IntegerField(
                initial=existing_ovens_data.get("meth9", {}).get("PEC_oven1", {}),
                required=False,
                widget=self.JSON_WIDGET_STYLES.get("PEC_oven1")
            )
            self.fields["PEC_oven2"] = forms.IntegerField(
                initial=existing_ovens_data.get("meth9", {}).get("PEC_oven2", {}),
                required=False,
                widget=self.JSON_WIDGET_STYLES.get("PEC_oven2")
            )
            self.fields["PEC_time1"] = forms.TimeField(
                initial=existing_ovens_data.get("meth9", {}).get("PEC_time1", {}),
                required=False,
                widget=self.JSON_WIDGET_STYLES.get("PEC_time1")
            )
            self.fields["PEC_time2"] = forms.TimeField(
                initial=existing_ovens_data.get("meth9", {}).get("PEC_time2", {}),
                required=False,
                widget=self.JSON_WIDGET_STYLES.get("PEC_time2")
            )
            self.fields["PEC_start"] = forms.TimeField(
                initial=existing_ovens_data.get("meth9", {}).get("PEC_start", {}),
                required=False,
                widget=self.JSON_WIDGET_STYLES.get("PEC_start")
            )
            self.fields["PEC_stop"] = forms.TimeField(
                initial=existing_ovens_data.get("meth9", {}).get("PEC_stop", {}),
                required=False,
                widget=self.JSON_WIDGET_STYLES.get("PEC_stop")
            )
            self.fields["PEC_average"] = forms.IntegerField(
                initial=existing_ovens_data.get("meth9", {}).get("PEC_average", {}),
                required=False,
                widget=self.JSON_WIDGET_STYLES.get("PEC_average")
            )

        else:  # Handling "non" type
            for key in ["PEC_push_oven", "PEC_push_time", "PEC_observe_time"]:
                widget = self.JSON_WIDGET_STYLES.get(key, forms.TextInput(attrs={"class": "input"}))
                field_type = forms.IntegerField if "oven" in key else forms.TimeField if "time" in key else forms.BooleanField
                self.fields[key] = field_type(
                    initial=existing_ovens_data.get("non", {}).get(key, None),
                    required=False,
                    widget=widget
                )
            self.fields["PEC_emissions_present"] = forms.ChoiceField(
                choices=[("Yes", "Yes"), ("No", "No")],
                required=False,
                widget=self.JSON_WIDGET_STYLES.get("PEC_emissions_present"),
                initial=existing_ovens_data.get("non", {}).get("PEC_emissions_present", None)
            )

class form18_form(ModelForm):
    class Meta:
        model = form18_model
        fields = ('__all__')
        
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'cert_date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'estab_no': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 80px; text-align: center;'}),
            'observer': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'canvas': forms.TextInput(attrs={'id': 'canvas', 'type': 'hidden', 'class': 'input', 'style': 'width:50px; text-align: center;', "required": "true"})
        }
    
    DEFAULT_READING_FIELDS = {
        "process_equip1": "", "process_equip2": "", "op_mode1": "normal", "op_mode2": "normal",
        "background_color_start": "", "background_color_stop": "", "sky_conditions": "",
        "wind_speed_start": "", "wind_speed_stop": "", "wind_direction": "",
        "emission_point_start": "", "emission_point_stop": "",
        "ambient_temp_start": "", "ambient_temp_stop": "", "humidity": "",
        "height_above_ground": "", "height_rel_observer": "",
        "distance_from": "", "direction_from": "",
        "describe_emissions_start": "", "describe_emissions_stop": "",
        "emission_color_start": "", "emission_color_stop": "",
        "plume_type": "", "water_drolet_present": "",
        "water_droplet_plume": "", "plume_opacity_determined_start": "", "plume_opacity_determined_stop": "",
        "describe_background_start": "", "describe_background_stop": "",
        **{f"PEC_read_a_{i}": "" for i in range(1, 9)},
        **{f"PEC_read_b_{i}": "" for i in range(1, 9)},
        **{f"PEC_read_c_{i}": "" for i in range(1, 9)},
        "PEC_oven_a": "", "PEC_oven_b": "", "PEC_oven_c": "", "PEC_start_a": "", 
        "PEC_start_b": "", "PEC_start_c": "", "PEC_average_a": "", "PEC_average_b": "", 
        "PEC_average_c": "", "PEC_average_main": ""
    }
    
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
            choices=[("", "---------"),("N/A", "N/A"),("Fugitive", "Fugitive"),("Continuous", "Continuous"),("Intermittent", "Intermittent")],
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
        **{f"PEC_read_a_{i}": forms.NumberInput(attrs={"type": "number", "style": "width: 50px; text-align: center;"}) for i in range(1, 9)},
        **{f"PEC_read_b_{i}": forms.NumberInput(attrs={"type": "number", "style": "width: 50px; text-align: center;"}) for i in range(1, 9)},
        **{f"PEC_read_c_{i}": forms.NumberInput(attrs={"type": "number", "style": "width: 50px; text-align: center;"}) for i in range(1, 9)},
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

    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)
        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form18_form.")

        initial = kwargs.get("initial", {})
        instance = kwargs.get("instance")

        # Determine the data source: use instance if it exists, otherwise use initial
        data_source = instance if instance else SimpleNamespace(**initial)

        super().__init__(*args, **kwargs)

        # Extract JSON-stored data
        existing_data = getattr(data_source, "reading_data", {}) or {}
        existing_ovens_data = getattr(data_source, "ovens_data", {}) or {}

        general_fields = [
            "date", "estab", "county", "estab_no", "equip_loc",
            "district", "city", "observer", "cert_date"
        ]

        for field in general_fields:
            if field in self.fields:
                self.fields[field].initial = initial.get(field, getattr(data_source, field, None))

        # Handle all fields dynamically, merging data from the source
        for field_name, default_value in self.DEFAULT_READING_FIELDS.items():
            widget = self.JSON_WIDGET_STYLES.get(field_name, forms.TextInput(attrs={"class": "input"}))
            self.fields[field_name] = forms.CharField(
                initial=existing_data.get(field_name, default_value),
                required=False,
                widget=widget
            )

        self.fields["PEC_average_main"] = forms.FloatField(
            initial=existing_ovens_data.get("PEC_average_main", {}),
            required=False,
            widget=self.JSON_WIDGET_STYLES.get("PEC_average_main")
        )
        
        for alpha in ["a", "b", "c"]:
            category = f"oven_{alpha}"
            alphaOvenName = f"PEC_oven_{alpha}"
            alphaStartName = f"PEC_start_{alpha}"
            alphaAverageName = f"PEC_average_{alpha}"
            self.fields[alphaOvenName] = forms.IntegerField(
                initial=existing_ovens_data.get(category, {}).get(alphaOvenName, {}),
                required=False,
                widget=self.JSON_WIDGET_STYLES.get(alphaOvenName)
            )
            self.fields[alphaStartName] = forms.TimeField(
                initial=existing_ovens_data.get(category, {}).get(alphaStartName, {}),
                required=False,
                widget=self.JSON_WIDGET_STYLES.get(alphaStartName)
            )
            self.fields[alphaAverageName] = forms.FloatField(
                initial=existing_ovens_data.get(category, {}).get(alphaAverageName, {}),
                required=False,
                widget=self.JSON_WIDGET_STYLES.get(alphaAverageName)
            )
            for ov_numb in range(1,9):
                alphaReadingInput = f"PEC_read_{alpha}_{ov_numb}"
                self.fields[alphaReadingInput] = forms.IntegerField(
                    initial=existing_ovens_data.get(category, {}).get("readings", {}).get(alphaReadingInput, {}),
                    required=False,
                    widget=self.JSON_WIDGET_STYLES.get(alphaReadingInput)
                )
  
class form19_form(ModelForm):
    class Meta:
        model = form19_model
        fields = ('__all__')
        
        widgets = {
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'cert_date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px;'}),
            'estab_no': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'style': 'width: 80px; text-align: center;'}),
            'observer': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'canvas': forms.TextInput(attrs={'id': 'canvas', 'type': 'hidden', 'class': 'input', 'style': 'width:50px; text-align: center;', "required": "true"})
        }
    
    DEFAULT_READING_FIELDS = {
        "process_equip1": "", "process_equip2": "", "op_mode1": "normal", "op_mode2": "normal",
        "background_color_start": "", "background_color_stop": "", "sky_conditions": "",
        "wind_speed_start": "", "wind_speed_stop": "", "wind_direction": "",
        "emission_point_start": "", "emission_point_stop": "",
        "ambient_temp_start": "", "ambient_temp_stop": "", "humidity": "",
        "height_above_ground": "", "height_rel_observer": "",
        "distance_from": "", "direction_from": "",
        "describe_emissions_start": "", "describe_emissions_stop": "",
        "emission_color_start": "", "emission_color_stop": "",
        "plume_type": "", "water_drolet_present": "",
        "water_droplet_plume": "", "plume_opacity_determined_start": "", "plume_opacity_determined_stop": "",
        "describe_background_start": "", "describe_background_stop": "",
        "comb_start": "", "comb_stop": "", "comb_average": "",
        **{f"comb_read_{i}": "" for i in range(1, 61)}
    }

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
            choices=[("", "---------"),("N/A", "N/A"),("Fugitive", "Fugitive"),("Continuous", "Continuous"),("Intermittent", "Intermittent")],
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
        "comb_start": forms.TimeInput(attrs={'type': 'time', 'style': 'width: 95px;'}),
        "comb_stop": forms.TimeInput(attrs={'type': 'time', 'style': 'width: 95px;'}),
        "comb_average": forms.NumberInput(attrs={'class': 'input', 'type': 'number', 'style': 'width: 50px; text-align: center;'}),
        **{f"comb_read_{i}": forms.NumberInput(attrs={"type": "number", "style": "width: 50px; text-align: center;"}) for i in range(1, 25)},
    }

    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)
        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form19_form.")

        initial = kwargs.get("initial", {})
        instance = kwargs.get("instance")

        # Determine the data source: use instance if it exists, otherwise use initial
        data_source = instance if instance else SimpleNamespace(**initial)

        super().__init__(*args, **kwargs)

        # Extract JSON-stored data
        existing_data = getattr(data_source, "reading_data", {}) or {}
        existing_ovens_data = getattr(data_source, "ovens_data", {}) or {}

        general_fields = [
            "date", "estab", "county", "estab_no", "equip_loc",
            "district", "city", "observer", "cert_date"
        ]
    
        for field in general_fields:
            if field in self.fields:  # Ensure the field exists in the form before setting
                self.fields[field].initial = initial.get(field, getattr(data_source, field, None))

        # Handle all fields dynamically, merging data from the source
        for field_name, default_value in self.DEFAULT_READING_FIELDS.items():
            widget = self.JSON_WIDGET_STYLES.get(field_name, forms.TextInput(attrs={"class": "input"}))
            self.fields[field_name] = forms.CharField(
                initial=existing_data.get(field_name, default_value),
                required=False,
                widget=widget
            )
        
        for i in range(1, 61):
            field_name = f"comb_read_{i}"
            widget = self.JSON_WIDGET_STYLES.get(field_name, forms.NumberInput(attrs={"type": "number", "style": "width: 50px; text-align: center;"}))
            self.fields[field_name] = forms.IntegerField(
                initial=existing_ovens_data.get(field_name, None),
                required=False,
                widget=widget
            )

        self.fields["comb_average"] = forms.FloatField(
            initial=existing_ovens_data.get("comb_average", {}),
            required=False,
            widget=self.JSON_WIDGET_STYLES.get("comb_average")
        )

        self.fields["comb_start"] = forms.TimeField(
            initial=existing_ovens_data.get("comb_start", {}),
            required=False,
            widget=self.JSON_WIDGET_STYLES.get("comb_start")
        )

        self.fields["comb_stop"] = forms.TimeField(
            initial=existing_ovens_data.get("comb_stop", {}),
            required=False,
            widget=self.JSON_WIDGET_STYLES.get("comb_stop")
        )

        self.fields["comb_formL"] = forms.CharField(
            initial=existing_ovens_data.get("comb_stop", {}),
            required=False,
            widget=self.JSON_WIDGET_STYLES.get("comb_stop")
        )

class form20_form(ModelForm):
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
        
    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)

        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form1_form.")
        """ Extract JSON values and create dynamic form fields with the correct styles. """
        super().__init__(*args, **kwargs)

class form21_form(ModelForm):
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
    
    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)

        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form1_form.")
        """ Extract JSON values and create dynamic form fields with the correct styles. """
        super().__init__(*args, **kwargs)
     
class form24_form(ModelForm):
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

    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)

        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form1_form.")
        """ Extract JSON values and create dynamic form fields with the correct styles. """
        super().__init__(*args, **kwargs)

class form25_form(ModelForm):
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
    
    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)

        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form1_form.")
        """ Extract JSON values and create dynamic form fields with the correct styles. """
        super().__init__(*args, **kwargs)




class form26_form(ModelForm):
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
    
    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)

        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form1_form.")
        """ Extract JSON values and create dynamic form fields with the correct styles. """
        super().__init__(*args, **kwargs)

class form27_form(ModelForm):
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
        
    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)

        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form1_form.")
        """ Extract JSON values and create dynamic form fields with the correct styles. """
        super().__init__(*args, **kwargs)

class form29_form(ModelForm):
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

    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)

        if not form_settings:
            raise ValueError("Error: `form_settings` must be provided when initializing form1_form.")
        """ Extract JSON values and create dynamic form fields with the correct styles. """
        super().__init__(*args, **kwargs)

class form30_form(forms.ModelForm):
    class Meta:
        model = form30_model
        fields = "__all__"
        widgets = {
            "observer": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Observer Name"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control", 'required': True}),
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

class form31_form(forms.ModelForm):
    class Meta:
        model = form31_model
        fields = ["observer", "date", "time", "tank_json"]
        widgets = {
            "observer": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Observer Name"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control", 'required': True}),
            "time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        form_settings = kwargs.pop("form_settings", None)  # Extract form settings
        super().__init__(*args, **kwargs)

        if not form_settings:
            raise ValueError("Error: `form_settings` is required to initialize form31_form.")

        # ✅ Extract tank settings from `form_settings.settings['settings']`
        settings = form_settings.settings.get("settings", {}) if hasattr(form_settings, "settings") else {}
        tanks = {key: value for key, value in settings.items() if key.startswith("tank")}  # Extract tanks dynamically

        # ✅ Load existing form data
        instance = kwargs.get("instance")
        tank_data = instance.tank_json if instance and instance.tank_json else {}

        # ✅ Generate dynamic fields for each tank
        for tank_key, tank_info in tanks.items():
            tank_id = tank_info.get("id", tank_key)  # Default to key if missing ID

            # Status field (Radio Select: OK / Not OK)
            self.fields[f"{tank_id}_status"] = forms.ChoiceField(
                choices=[("OK", "OK"), ("Not OK", "Not OK")],
                required=False,
                widget=forms.RadioSelect(attrs={"class": "status-radio"}),
                initial=tank_data.get(tank_id, {}).get("status", ""),
            )

            # Comments field (Textarea)
            self.fields[f"{tank_id}_comments"] = forms.CharField(
                required=False,
                widget=forms.Textarea(attrs={"rows": "2", "class": "tank-comment", "placeholder": "Add comment..."}),
                initial=tank_data.get(tank_id, {}).get("comments", ""),
            )

    def clean_tank_json(self):
        """Ensure JSON data is valid for tank inspections."""
        data = self.cleaned_data.get("tank_json")
        if not isinstance(data, dict):
            raise forms.ValidationError("Invalid data format for tank status.")
        return data



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







class issues_form(ModelForm):
    class Meta:
        model = issues_model
        fields = ('__all__')
        widgets = {
            'issues' : Textarea(attrs={'rows':7, 'style':'width: 100%; border-radius: 18px; padding: .5rem;'}),
            'notified' : forms.TextInput(attrs={'type':'text', 'style':'width:150px; border-radius: 5px; background-color: white; border: 1px solid black; padding-left: .5rem;'}),
            'time' : forms.TimeInput(attrs={'type':'time', 'style':'width: 120px; border-radius: 5px; background-color: white; border: 1px solid black;'}),
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px; border-radius: 5px; background-color: white; border: 1px solid black;'}),
            'cor_action' : Textarea(attrs={'rows':7, 'style':'width: 100%; border-radius: 18px; padding: .5rem;'}),
        }

class events_form(ModelForm):
    selected_days = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # grab the user passed from the view
        super().__init__(*args, **kwargs)

        if user:
            facilities = facility_model.objects.filter(company=user.user_profile.company)
            self.fields['calendarChoice'].choices = [(f.facility_name, f.facility_name) for f in facilities]

    class Meta:
        model = Event
        fields = ['title', 'observer', 'notes', 'start_time','end_time','allDay', 'facilityChoice', 'calendarChoice', 'repeat', 'alerts']
        widgets = {
            'facilityChoice': forms.Select(attrs={}),
            'calendarChoice': forms.Select(attrs={}),
            'observer' : forms.TextInput(attrs={}),
            'title' : forms.TextInput(attrs={'placeholder': "e.g., Stack Inspection - Battery A", 'style':'width: 100%;'}),
            'notes' : forms.TextInput(attrs={'type':'text'}),
            #'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'start_time' : forms.TimeInput(attrs={'type':'time'}),
            'end_time' : forms.TimeInput(attrs={'type':'time'}),
            'allDay' : forms.CheckboxInput(attrs={}),
            'repeat' : forms.CheckboxInput(attrs={}),
            'alerts' : forms.CheckboxInput(attrs={}),
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
            'icon': forms.ClearableFileInput(attrs={'class':'input'}),
        }   
    
    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            img = Image.open(image)
            width, height = img.size

            if width < 64 or height < 64:
                raise ValidationError("Image is too small. Minimum size is 64x64 pixels.")
            if width > 512 or height > 512:
                raise ValidationError("Image is too large. Maximum size is 512x512 pixels.")

        return image
           
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
            'name': forms.TextInput(attrs={'class': 'packet-input-input', 'type':'text', 'placeholder':'Enter packet name...'}),
            'formList': forms.TextInput(),
        }
        
class form_settings_form(ModelForm):
    class Meta:
        model = form_settings_model
        fields = ('__all__')
        widgets = {
            'facilityChoice': forms.Select(attrs={}),
            'formChoice': forms.Select(attrs={}),
            'settings': forms.TextInput(),
        }

class CustomSelectWidget(forms.Select):
    """Custom Select Widget to add data-submitted attribute to options."""
    
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)

        # 🔥 Add the `data-submitted` attribute with default "false"
        option["attrs"]["data-submitted"] = "false"
        return option   


