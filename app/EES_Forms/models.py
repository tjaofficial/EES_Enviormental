from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError # type: ignore
from django.urls import reverse # type: ignore
import datetime
import uuid
import os
from django.utils.text import slugify # type: ignore

quarter_choices = (
    ('1', '1st'),
    ('2', '2nd'),
    ('3', '3rd'),
    ('4', '4th')
)
position_choices = (
    ('observer', 'Observer'),
    ('supervisor', 'Supervisor'),
    ('client', 'Client')
)
truck_choices = (
    ('#5', 'Truck #5'),
    ('#6', 'Truck #6'),
    ('#7', 'Truck #7'),
    ('#9', 'Truck #9'),
    ('contractor', 'Contractor'),
    ('dozer', 'Dozer'),
)
area_choices = (
    ('panther eagle', 'Panther Eagle'),
    ('kepler', 'Kepler'),
    ('rock lick', 'Rock Lick'),
    ('mcclure', 'McClure'),
    ('elk valley', 'Elk Valley'),
)
heightLabel = (
    ('ft', 'Feet'),
    ('m', 'Meters')
)
batteryMain_choices = (
    ('single','Single'),
    ('double','Double')
)
crew_choices = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D')
)
plume_type_choices = (
    ('N/A', 'N/A'),
    ('Fugitive', 'Fugitive'),
    ('Continuous', 'Continuous'),
    ('Intermittent', 'Intermittent')
)
instant_over_20_choices = (
    ('Yes', 'Yes'),
    ('No', 'No')
)
average_over_35_choices = (
    ('Yes', 'Yes'),
    ('No', 'No')
)
water_present_choices = (
    ('Yes', 'Yes'),
    ('No', 'No')
)
droplet_plume_choices = (
    ('N/A', 'N/A'),
    ('Attached', 'Attached'),
    ('Detached', 'Detached')
)
yes_no_choices = (
    ('Yes', 'Yes'),
    ('No', 'No')
)
yes_no_na_choices = (
    ('N/A', 'N/A'),
    ('Yes', 'Yes'),
    ('No', 'No')
)
good_bad_choices = (
    ('good', 'Good'),
    ('bad', 'Bad')
)
truck_id_choices = (
    ('#5', '#5'),
    ('#6', '#6'),
    ('#7', '#7'),
    ('#9', '#9'),
    ('Dozer', 'Dozer'),
    ('Semi', 'Semi'),
    ('Contractor', 'Contractor'),
    ('Security', 'Security'),
    ('Water Truck', 'Water Truck'),
)
content_choices = (
    ('Coal', 'Coal'),
    ('Coke', 'Coke'),
    ('Breeze', 'Breeze'),
)
wetted_choices = (
    ('N/A', 'N/A'),
    ('Yes', 'Yes'),
    ('No', 'No')
)
source_choices = (
    ('Inspection Cap', 'Inspection Cap'),
    ('GooseNeck', 'GooseNeck'),
    ('Flange', 'Flange'),
    ('Expansion Joint', 'Expansion Joint')
)
paved_roads = (
    ('p1', '#4 Booster Station'),
    ('p2', '#5 Battery Road'),
    ('p3', 'Coal Dump Horseshoe'),
    ('p4', 'Coal Handling Road (Partial)'),
    ('p5', 'Coke Plant Road'),
    ('p6', 'Coke Plant Mech Road'),
    ('p7', 'North Gate Area'),
    ('p8', 'Compound Road'),
    ('p9', 'Gap Gate Road'),
    ('p10', '#3 Ore Dock Road'),
    ('p11', 'River Road'),
    ('p12', 'Weigh Station Road'),
    ('p13', 'Zug Island Road')
)
unpaved_roads = (
    ('unp1', 'North Gate Truck Turn'),
    ('unp2', 'Screening Station Road'),
    ('unp3', 'Coal Handling Road (Partial)'),
    ('unp4', 'Taj Mahal Road'),
    ('unp5', 'PECS Approach'),
    ('unp6', 'No. 2 Boilerhouse Road'),
    ('unp7', 'D-4 Blast Furnace Road'),
    ('unp8', 'Bypass Route')
)
parking_lots = (
    ('par1', 'Gap Gate Parking'),
    ('par2', 'Truck Garage Area'),
    ('par3', 'EES Coke Office Parking'),
)
storage_piles = (
    ('sto1', 'Area B Coke Storage Piles'),
    ('sto2', 'EES Coke Coal Storage Piles'),
)
larry_car_choices = (
    ('1', '1'),
    ('2', '2')
)
door_location = (
    ('Door', 'D'),
    ('Chuck Door', 'C'),
    ('Masonry', 'M')
)
door_zone = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8')
)
om_location = (
    ('Dampered Off', 'D'),
    ('Cap', 'C'),
    ('Flange', 'F'),
    ('Slip Joint', 'S'),
    ('Base', 'B'),
    ('Piping', 'P'),
    ('Other', 'O'),
    ('Mini Standpipe', 'MS')
)
l_location = (
    ('Dampered Off', 'D'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
)
weather_choices = (
    ('clear', 'Clear'),
    ('cloudy', 'Cloudy'),
    ('rain', 'Rain'),
    ('snow', 'Snow'),
    ('excessive wind', 'Excessive Wind'),
)
barrier_choices = (
    ('none', 'None'),
    ('0" - 1/4"', '0" - 1/4"'),
    ('1/4" - 1/2"', '1/4" - 1/2"'),
    ('1/2" - 3/4"', '1/2" - 3/4"'),
    ('3/4" - 1"', '3/4" - 1"'),
    ('1" - 2"', '1" - 2"'),
)
ok_not_ok_choices = (
    ('N/A', 'N/A'),
    ('OK', 'OK'),
    ('Not OK', 'Not OK')
)
waste_code_choices = (
    ('universal', 'UNIV'),
    ('non-hazardous ', 'NON-HAZ'),
    ('hazardous', 'HAZ'),
)
frequent_choices = (
    ('Daily', 'Daily'),
    ('Weekly', 'Weekly'),
    ('Monthly', 'Monthly'),
    ('Quarterly', 'Quarterly '),
    ('Semi-Annual', 'Semi-Annual'),
    ('Annual', 'Annual')
)
days_choices = (
    ('Everyday', 'Everyday'),
    ('0', 'Mondays'),
    ('1', 'Tuesdays'),
    ('2', 'Wednesdays'),
    ('3', 'Thursdays'),
    ('4', 'Fridays'),
    ('5', 'Saturdays'),
    ('6', 'Sundays'),
    ('Weekends', 'Weekends'),
    ('Weekdays', 'Weekdays'),
)
weekend_choices = (
    ('5', 'Saturday'),
    ('6', 'Sunday'),
)
spill_kit_choices = (
    ("oil XL cart","PIG Spill Kit in Extra-Large Response Chest"),
    ("universal drum","PIG Spill Kit in Overpack Salvage Drum")
)
colorMode_choices = (
    ("dark","Dark Mode"),
    ("light", "Light Mode")
)
notification_header_choices = (
    ("compliance","OUT OF COMPLIANCE"),
    ("90days","90 DAY OVENS"),
    ("message","MESSAGE"),
    ("event","EVENT"),
    ("schedule","SCHEDULE UPDATED"),
    ("submitted","FORM SUBMITTED"),
    ("deviations","CORRECTIVE ACTION")
)
weekly_range_choices = (
    ('0','Monday'),
    ('1','Tuesday'),
    ('2','Wednesday'),
    ('3','Thursday'),
    ('4','Friday'),
    ('5','Saturday'),
    ('6','Sunday')
)

# -all_users = User.objects.all()
# -all_user_choices_x = ((x.username, x.get_full_name()) for x in all_users)

# Create your models here.
class braintree_model(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT
    )
    settings = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )
    def __str__(self):
        return str(self.id) + "-" + str(self.user.last_name)
    
class company_model(models.Model):
    company_name = models.CharField(
        max_length=60
    )
    address = models.CharField(
        max_length=60
    )
    city = models.CharField(
        max_length=20
    )
    state = models.CharField(
        max_length=2
    )
    zipcode = models.CharField(
        max_length=5
    )
    phone = models.CharField(
        max_length=14
    )
    braintree = models.OneToOneField(
        braintree_model, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    icon = models.ImageField(
        upload_to='images/icons/',
        blank=True, 
        null=True
    )

    def save(self, *args, **kwargs):
        if self.icon and not self.icon.name.startswith('images/icons/'):
            ext = self.icon.name.split('.')[-1]
            self.icon.name = f"{uuid.uuid4().hex}.{ext}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name

class facility_model(models.Model):
    company = models.ForeignKey(
        company_model, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    bat_num = models.IntegerField(
        null=True,
        blank=True
    )
    total_ovens = models.IntegerField(
        null=True,
        blank=True
    )
    facility_name = models.CharField(max_length=30)
    county = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )
    estab_num = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    equip_location = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )
    address = models.CharField(
        max_length=30
    )
    state = models.CharField(
        max_length=30
    )
    city = models.CharField(
        max_length=30
    )
    zipcode = models.CharField(
        max_length=5,
        null=True,
        blank=True
    )
    district = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )
    bat_height = models.IntegerField(
        null=True,
        blank=True
    )
    bat_height_label = models.CharField(
        max_length=10,
        choices=heightLabel,
        null=True,
        blank=True
    )
    bat_main = models.CharField(
        max_length=10,
        choices=batteryMain_choices,
        null=True,
        blank=True
    )
    bat_lids = models.IntegerField(
        null=True,
        blank=True
    )
    is_battery = models.CharField(
        max_length=10,
        choices=yes_no_choices,
        default='No'
    )
    dashboard = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    settings = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.facility_name

class Forms(models.Model):
    form = models.CharField(max_length=30)
    frequency = models.CharField(max_length=30, choices=frequent_choices)
    day_freq = models.CharField(max_length=30, choices=days_choices, null=True)
    weekdays_only = models.BooleanField(default=False)
    weekend_only = models.BooleanField(default=False)
    link = models.CharField(max_length=30)
    header = models.CharField(max_length=80)
    title = models.CharField(max_length=80)

    def __str__(self):
        return self.form

class formSubmissionRecords_model(models.Model):
    dateSubmitted = models.DateField(auto_now=False, auto_now_add=False)
    dueDate = models.DateField(auto_now=False, auto_now_add=False)
    submitted = models.BooleanField(default=False)
    def __str__(self):
        form_settings = getattr(self, 'form_settings', None)
        fsID = getattr(form_settings, 'id', "N/A")
        formID = getattr(form_settings, 'formChoice', "N/A")
        return f"Id: {self.id} - fsID: {fsID} - FormID: {formID}"

class the_packets_model(models.Model):
    facilityChoice = models.ForeignKey(facility_model, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(
        max_length=70
    )
    formList = models.JSONField(
        null=True,
        blank=True,
        default=dict
    )
    def __str__(self):
        return str(self.id) + ' - ' + str(self.name) + ' - ' + str(self.facilityChoice)
    
class form_settings_model(models.Model):
    facilityChoice = models.ForeignKey(facility_model, on_delete=models.CASCADE)
    formChoice = models.ForeignKey(Forms, on_delete=models.CASCADE)
    subChoice = models.OneToOneField(
        'formSubmissionRecords_model', 
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='form_settings'
    )
    settings = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )
    def __str__(self):
        return str(self.id) + ' - ' + str(self.formChoice) + ' - ' + str(self.facilityChoice)
    
class form7_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    date = models.DateField(auto_now_add=False, auto_now=False)
    observer = models.CharField(
        max_length=30
    )
    cert_date = models.DateField(
        auto_now_add=False,
        auto_now=False
    )
    comments = models.CharField(
        max_length=600
    )
    area_json_1 = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )
    area_json_2 =models.JSONField(
        default=dict,
        null=True,
        blank=True
    )
    area_json_3 =models.JSONField(
        default=dict,
        null=True,
        blank=True
    )
    area_json_4 =models.JSONField(
        default=dict,
        null=True,
        blank=True
    )

    def clean_t(self):
        if self.truck_start_time > self.truck_stop_time:
            raise ValidationError('Start should be before end')
        return super().clean()

    def clean_a(self):
        if self.area_start_time > self.area_stop_time:
            raise ValidationError('Start should be before end')
        return super().clean()

    def __str__(self):
        return f"Facility: {self.formSettings.facilityChoice.facility_name}, fsID: {self.formSettings.id}, Date: {self.date}"

    def save(self, *args, **kwargs):
        for i in range(1, 5):  # Covers area_json_1 to area_json_4
            field_name = f"area_json_{i}"
            if getattr(self, field_name) in [None, "null", False]:
                setattr(self, field_name, {})  # Set it to an empty dictionary

        super().save(*args, **kwargs)

class Profile(models.Model):

    Name = models.CharField(max_length=30)
    cer_date = models.DateField(auto_now_add=False, auto_now=False, blank=True)

    def __str__(self):
        return self.name

class daily_battery_profile_model(models.Model):
    foreman = models.CharField(max_length=30)
    crew = models.CharField(max_length=1, choices=crew_choices)
    inop_ovens = models.CharField(max_length=2, blank=True)
    inop_numbs = models.CharField(max_length=50)
    date_save = models.DateField(auto_now_add=True, auto_now=False)
    time_log = models.TimeField(auto_now_add=True, auto_now=False)
    facilityChoice = models.ForeignKey(facility_model, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.date_save) + " - " +str(self.facilityChoice)

class user_profile_model(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name='user_profile'
    )
    cert_date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    profile_picture = models.ImageField(
        blank=True,
        null=True,
        upload_to='images/profile_pics'
    )
    phone = models.CharField(
        max_length=15,
        null=False,
        blank=False,
    )
    position = models.CharField(
        max_length=75,
        choices=position_choices,
        null=False,
        blank=False,
    )
    certs = models.CharField(
        max_length=300,
        null=True,
        blank=True,
    )
    facilityChoice = models.ForeignKey(
        facility_model, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    company = models.ForeignKey(
        company_model, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    colorMode = models.CharField(
        choices=colorMode_choices,
        max_length=5,
        default='light'
    )
    is_active = models.BooleanField(
        default=False
    )
    settings = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.user.username

class form1_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    observer = models.CharField(
        max_length=30
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    crew = models.CharField(
        max_length=1,
        choices=crew_choices
    )
    foreman = models.CharField(
        max_length=30,
    )
    start = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    stop = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    ovens_data = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.date)

class form2_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    observer = models.CharField(
        max_length=30
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    inop_ovens = models.IntegerField(
    )
    inop_numbs = models.CharField(
        max_length=50
    )
    crew = models.CharField(
        max_length=1,
        choices=crew_choices
    )
    foreman = models.CharField(
        max_length=30,
    )
    p_start = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    p_stop = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    c_start = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    c_stop = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )

    p_leak_data = models.CharField(
        max_length=1000,
        blank=True,
        null=True
    )
    c_leak_data = models.CharField(
        max_length=1000,
        blank=True,
        null=True
    )
    p_temp_block_from = models.CharField(max_length=30)
    p_temp_block_to = models.CharField(max_length=30)
    c_temp_block_from = models.CharField(max_length=30)
    c_temp_block_to = models.CharField(max_length=30)
    p_traverse_time_min = models.CharField(max_length=30)
    p_traverse_time_sec = models.CharField(max_length=30)
    c_traverse_time_min = models.CharField(max_length=30)
    c_traverse_time_sec = models.CharField(max_length=30)
    total_traverse_time = models.CharField(max_length=30)
    allowed_traverse_time = models.CharField(max_length=30)
    valid_run = models.BooleanField(default=None)
    leaking_doors = models.IntegerField(
    )
    doors_not_observed = models.IntegerField(
    )
    inop_doors_eq = models.IntegerField(
    )
    percent_leaking = models.CharField(max_length=30)
    notes = models.CharField(max_length=30)

    def __str__(self):
        return str(self.date)

class form3_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    observer = models.CharField(
        max_length=30
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    inop_ovens = models.IntegerField(
    )
    inop_numbs = models.CharField(
        max_length=50
    )
    crew = models.CharField(
        max_length=1,
        choices=crew_choices
    )
    foreman = models.CharField(
        max_length=30
    )
    om_start = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    om_stop = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    l_start = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    l_stop = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    om_leak_json = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )
    om_leaks2 = models.CharField(
        max_length=30,
    )
    l_leak_json = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )
    l_leaks2 = models.CharField(
        max_length=30,
    )
    om_traverse_time_min = models.CharField(max_length=30)
    om_traverse_time_sec = models.CharField(max_length=30)
    om_total_sec = models.IntegerField(
        default=0
    )
    l_traverse_time_min = models.CharField(max_length=30)
    l_traverse_time_sec = models.CharField(max_length=30)
    l_total_sec = models.IntegerField(
        default=0
    )
    om_allowed_traverse_time = models.CharField(max_length=30)
    l_allowed_traverse_time = models.CharField(max_length=30)
    om_valid_run = models.BooleanField(default=None)
    l_valid_run = models.BooleanField(default=None)
    om_leaks = models.CharField(max_length=30)
    l_leaks = models.CharField(max_length=30)
    om_not_observed = models.CharField(max_length=30)
    l_not_observed = models.CharField(max_length=30)
    om_percent_leaking = models.CharField(max_length=30)
    l_percent_leaking = models.CharField(max_length=30)
    one_pass = models.BooleanField(default=False, null=True)
    notes = models.CharField(max_length=30)

    def __str__(self):
        return str(self.date)

class form4_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    observer = models.CharField(
        max_length=30
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    crew = models.CharField(
        max_length=1,
        choices=crew_choices
    )
    foreman = models.CharField(
        max_length=30
    )
    main_start = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    main_stop = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    main_1 = models.CharField(
        max_length=30
    )
    main_2 = models.CharField(
        max_length=30
    )
    main_3 = models.CharField(
        max_length=30
    )
    main_4 = models.CharField(
        max_length=30
    )
    leak_data = models.CharField(
        max_length=1000,
        blank=True,
        null=True
    )
    suction_main = models.CharField(
        max_length=30
    )
    notes = models.CharField(
        max_length=600
    )

    def __str__(self):
        return str(self.date)

class form5_model(models.Model):
    formSettings = models.ForeignKey('form_settings_model', on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    estab = models.CharField(max_length=30)
    county = models.CharField(max_length=30)
    estab_no = models.CharField(max_length=5)
    equip_loc = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    observer = models.CharField(
        max_length=30
    )
    cert_date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    notes = models.CharField(max_length=600)
    canvas = models.CharField(max_length=100000)
    reading_data = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )
    ovens_data = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )
    
    def __str__(self):
        return str(self.date)

class form6_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    week_start = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    week_end = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    observer_0 = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    time_0 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    weather_0 = models.CharField(
        max_length=30,
        choices=weather_choices,
        blank=True,
        null=True
    )
    wind_speed_0 = models.CharField(
        max_length=3,
        blank=True,
        null=True
    )
    fugitive_dust_observed_0 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    supressant_applied_0 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    supressant_active_0 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    working_face_exceed_0 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    spills_0 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    pushed_back_0 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    coal_vessel_0 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    water_sprays_0 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    loader_lowered_0 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    working_water_sprays_0 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    barrier_thickness_0 = models.CharField(
        max_length=30,
        choices=barrier_choices,
        blank=True,
        null=True
    )
    surface_quality_0 = models.CharField(
        max_length=30,
        choices=good_bad_choices,
        blank=True,
        null=True
    )
    surpressant_crust_0 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    additional_surpressant_0 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    comments_0 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    wharf_0 = models.CharField(
        max_length=30,
        choices=good_bad_choices,
        blank=True,
        null=True
    )
    breeze_0 = models.CharField(
        max_length=30,
        choices=good_bad_choices,
        blank=True,
        null=True
    )
    observer_1 = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    time_1 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    weather_1 = models.CharField(
        max_length=30,
        choices=weather_choices,
        blank=True,
        null=True
    )
    wind_speed_1 = models.CharField(
        max_length=3,
        blank=True,
        null=True
    )
    fugitive_dust_observed_1 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    supressant_applied_1 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    supressant_active_1 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    working_face_exceed_1 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    spills_1 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    pushed_back_1 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    coal_vessel_1 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    water_sprays_1 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    loader_lowered_1 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    working_water_sprays_1 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    barrier_thickness_1 = models.CharField(
        max_length=30,
        choices=barrier_choices,
        blank=True,
        null=True
    )
    surface_quality_1 = models.CharField(
        max_length=30,
        choices=good_bad_choices,
        blank=True,
        null=True
    )
    surpressant_crust_1 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    additional_surpressant_1 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    comments_1 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    wharf_1 = models.CharField(
        max_length=30,
        choices=good_bad_choices,
        blank=True,
        null=True
    )
    breeze_1 = models.CharField(
        max_length=30,
        choices=good_bad_choices,
        blank=True,
        null=True
    )

    observer_2 = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    time_2 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    weather_2 = models.CharField(
        max_length=30,
        choices=weather_choices,
        blank=True,
        null=True
    )
    wind_speed_2 = models.CharField(
        max_length=3,
        blank=True,
        null=True
    )
    fugitive_dust_observed_2 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    supressant_applied_2 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    supressant_active_2 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    working_face_exceed_2 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    spills_2 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    pushed_back_2 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    coal_vessel_2 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    water_sprays_2 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    loader_lowered_2 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    working_water_sprays_2 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    barrier_thickness_2 = models.CharField(
        max_length=30,
        choices=barrier_choices,
        blank=True,
        null=True
    )
    surface_quality_2 = models.CharField(
        max_length=30,
        choices=good_bad_choices,
        blank=True,
        null=True
    )
    surpressant_crust_2 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    additional_surpressant_2 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    comments_2 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    wharf_2 = models.CharField(
        max_length=30,
        choices=good_bad_choices,
        blank=True,
        null=True
    )
    breeze_2 = models.CharField(
        max_length=30,
        choices=good_bad_choices,
        blank=True,
        null=True
    )

    observer_3 = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    time_3 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    weather_3 = models.CharField(
        max_length=30,
        choices=weather_choices,
        blank=True,
        null=True
    )
    wind_speed_3 = models.CharField(
        max_length=3,
        blank=True,
        null=True
    )
    fugitive_dust_observed_3 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    supressant_applied_3 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    supressant_active_3 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    working_face_exceed_3 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    spills_3 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    pushed_back_3 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    coal_vessel_3 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    water_sprays_3 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    loader_lowered_3 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    working_water_sprays_3 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    barrier_thickness_3 = models.CharField(
        max_length=30,
        choices=barrier_choices,
        blank=True,
        null=True
    )
    surface_quality_3 = models.CharField(
        max_length=30,
        choices=good_bad_choices,
        blank=True,
        null=True
    )
    surpressant_crust_3 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    additional_surpressant_3 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    comments_3 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    wharf_3 = models.CharField(
        max_length=30,
        choices=good_bad_choices,
        blank=True,
        null=True
    )
    breeze_3 = models.CharField(
        max_length=30,
        choices=good_bad_choices,
        blank=True,
        null=True
    )

    observer_4 = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    time_4 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    weather_4 = models.CharField(
        max_length=30,
        choices=weather_choices,
        blank=True,
        null=True
    )
    wind_speed_4 = models.CharField(
        max_length=3,
        blank=True,
        null=True
    )
    fugitive_dust_observed_4 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    supressant_applied_4 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    supressant_active_4 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    working_face_exceed_4 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    spills_4 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    pushed_back_4 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    coal_vessel_4 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    water_sprays_4 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    loader_lowered_4 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    working_water_sprays_4 = models.CharField(
        max_length=30,
        choices=yes_no_na_choices,
        blank=True,
        null=True
    )
    barrier_thickness_4 = models.CharField(
        max_length=30,
        choices=barrier_choices,
        blank=True,
        null=True
    )
    surface_quality_4 = models.CharField(
        max_length=30,
        choices=good_bad_choices,
        blank=True,
        null=True
    )
    surpressant_crust_4 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    additional_surpressant_4 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    comments_4 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    wharf_4 = models.CharField(
        max_length=30,
        choices=good_bad_choices,
        blank=True,
        null=True
    )
    breeze_4 = models.CharField(
        max_length=30,
        choices=good_bad_choices,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.week_start)

    def whatever(self):
        return{
            'observer_0': self.observer_0,
            'time_0': self.time_0,
            'weather_0': self.weather_0,
            'wind_speed_0': self.wind_speed_0,
            'fugitive_dust_observed_0': self.fugitive_dust_observed_0,
            'supressant_applied_0': self.supressant_applied_0,
            'supressant_active_0': self.supressant_active_0,
            'working_face_exceed_0': self.working_face_exceed_0,
            'spills_0': self.spills_0,
            'pushed_back_0': self.pushed_back_0,
            'coal_vessel_0': self.coal_vessel_0,
            'water_sprays_0': self.water_sprays_0,
            'loader_lowered_0': self.loader_lowered_0,
            'working_water_sprays_0': self.working_water_sprays_0,
            'barrier_thickness_0': self.barrier_thickness_0,
            'surface_quality_0': self.surface_quality_0,
            'surpressant_crust_0': self.surpressant_crust_0,
            'additional_surpressant_0': self.additional_surpressant_0,
            'comments_0': self.comments_0,
            'wharf_0': self.wharf_0,
            'breeze_0': self.breeze_0,

            'observer_1': self.observer_1,
            'time_1': self.time_1,
            'weather_1': self.weather_1,
            'wind_speed_1': self.wind_speed_1,
            'fugitive_dust_observed_1': self.fugitive_dust_observed_1,
            'supressant_applied_1': self.supressant_applied_1,
            'supressant_active_1': self.supressant_active_1,
            'working_face_exceed_1': self.working_face_exceed_1,
            'spills_1': self.spills_1,
            'pushed_back_1': self.pushed_back_1,
            'coal_vessel_1': self.coal_vessel_1,
            'water_sprays_1': self.water_sprays_1,
            'loader_lowered_1': self.loader_lowered_1,
            'working_water_sprays_1': self.working_water_sprays_1,
            'barrier_thickness_1': self.barrier_thickness_1,
            'surface_quality_1': self.surface_quality_1,
            'surpressant_crust_1': self.surpressant_crust_1,
            'additional_surpressant_1': self.additional_surpressant_1,
            'comments_1': self.comments_1,
            'wharf_1': self.wharf_1,
            'breeze_1': self.breeze_1,

            'observer_2': self.observer_2,
            'time_2': self.time_2,
            'weather_2': self.weather_2,
            'wind_speed_2': self.wind_speed_2,
            'fugitive_dust_observed_2': self.fugitive_dust_observed_2,
            'supressant_applied_2': self.supressant_applied_2,
            'supressant_active_2': self.supressant_active_2,
            'working_face_exceed_2': self.working_face_exceed_2,
            'spills_2': self.spills_2,
            'pushed_back_2': self.pushed_back_2,
            'coal_vessel_2': self.coal_vessel_2,
            'water_sprays_2': self.water_sprays_2,
            'loader_lowered_2': self.loader_lowered_2,
            'working_water_sprays_2': self.working_water_sprays_2,
            'barrier_thickness_2': self.barrier_thickness_2,
            'surface_quality_2': self.surface_quality_2,
            'surpressant_crust_2': self.surpressant_crust_2,
            'additional_surpressant_2': self.additional_surpressant_2,
            'comments_2': self.comments_2,
            'wharf_2': self.wharf_2,
            'breeze_2': self.breeze_2,

            'observer_3': self.observer_3,
            'time_3': self.time_3,
            'weather_3': self.weather_3,
            'wind_speed_3': self.wind_speed_3,
            'fugitive_dust_observed_3': self.fugitive_dust_observed_3,
            'supressant_applied_3': self.supressant_applied_3,
            'supressant_active_3': self.supressant_active_3,
            'working_face_exceed_3': self.working_face_exceed_3,
            'spills_3': self.spills_3,
            'pushed_back_3': self.pushed_back_3,
            'coal_vessel_3': self.coal_vessel_3,
            'water_sprays_3': self.water_sprays_3,
            'loader_lowered_3': self.loader_lowered_3,
            'working_water_sprays_3': self.working_water_sprays_3,
            'barrier_thickness_3': self.barrier_thickness_3,
            'surface_quality_3': self.surface_quality_3,
            'surpressant_crust_3': self.surpressant_crust_3,
            'additional_surpressant_3': self.additional_surpressant_3,
            'comments_3': self.comments_3,
            'wharf_3': self.wharf_3,
            'breeze_3': self.breeze_3,

            'observer_4': self.observer_4,
            'time_4': self.time_4,
            'weather_4': self.weather_4,
            'wind_speed_4': self.wind_speed_4,
            'fugitive_dust_observed_4': self.fugitive_dust_observed_4,
            'supressant_applied_4': self.supressant_applied_4,
            'supressant_active_4': self.supressant_active_4,
            'working_face_exceed_4': self.working_face_exceed_4,
            'spills_4': self.spills_4,
            'pushed_back_4': self.pushed_back_4,
            'coal_vessel_4': self.coal_vessel_4,
            'water_sprays_4': self.water_sprays_4,
            'loader_lowered_4': self.loader_lowered_4,
            'working_water_sprays_4': self.working_water_sprays_4,
            'barrier_thickness_4': self.barrier_thickness_4,
            'surface_quality_4': self.surface_quality_4,
            'surpressant_crust_4': self.surpressant_crust_4,
            'additional_surpressant_4': self.additional_surpressant_4,
            'comments_4': self.comments_4,
            'wharf_4': self.wharf_4,
            'breeze_4': self.breeze_4,
        }

class form8_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    today = datetime.date.today()
    last_friday = today - datetime.timedelta(days=today.weekday() + 2)
    one_week = datetime.timedelta(days=6)
    end_week = last_friday + one_week

    week_start = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    week_end = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    observer1 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    truck_id1 = models.CharField(
        max_length=30,
        choices=truck_id_choices,
        blank=True,
        null=True
    )
    date1 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time1 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    contents1 = models.CharField(
        max_length=30,
        choices=content_choices,
        blank=True,
        null=True
    )
    freeboard1 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    wetted1 = models.CharField(
        max_length=30,
        choices=wetted_choices,
        blank=True,
        null=True
    )
    comments1 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    observer2 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    truck_id2 = models.CharField(
        max_length=30,
        choices=truck_id_choices,
        blank=True,
        null=True
    )
    date2 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time2 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    contents2 = models.CharField(
        max_length=30,
        choices=content_choices,
        blank=True,
        null=True
    )
    freeboard2 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    wetted2 = models.CharField(
        max_length=30,
        choices=wetted_choices,
        blank=True,
        null=True
    )
    comments2 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    observer3 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    truck_id3 = models.CharField(
        max_length=30,
        choices=truck_id_choices,
        blank=True,
        null=True
    )
    date3 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time3 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    contents3 = models.CharField(
        max_length=30,
        choices=content_choices,
        blank=True,
        null=True
    )
    freeboard3 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    wetted3 = models.CharField(
        max_length=30,
        choices=wetted_choices,
        blank=True,
        null=True
    )
    comments3 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    observer4 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    truck_id4 = models.CharField(
        max_length=30,
        choices=truck_id_choices,
        blank=True,
        null=True
    )
    date4 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time4 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    contents4 = models.CharField(
        max_length=30,
        choices=content_choices,
        blank=True,
        null=True
    )
    freeboard4 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    wetted4 = models.CharField(
        max_length=30,
        choices=wetted_choices,
        blank=True,
        null=True
    )
    comments4 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    observer5 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    truck_id5 = models.CharField(
        max_length=30,
        choices=truck_id_choices,
        blank=True,
        null=True
    )
    date5 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time5 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    contents5 = models.CharField(
        max_length=30,
        choices=content_choices,
        blank=True,
        null=True
    )
    freeboard5 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    wetted5 = models.CharField(
        max_length=30,
        choices=wetted_choices,
        blank=True,
        null=True
    )
    comments5 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.week_start)

    def whatever(self):
        return{
            'truck_id1': self.truck_id1,
            'date1': self.date1,
            'time1': self.time1,
            'contents1': self.contents1,
            'freeboard1': self.freeboard1,
            'wetted1': self.wetted1,
            'comments1': self.comments1,
            'truck_id2': self.truck_id2,
            'date2': self.date2,
            'time2': self.time2,
            'contents2': self.contents2,
            'freeboard2': self.freeboard2,
            'wetted2': self.wetted2,
            'comments2': self.comments2,
            'truck_id3': self.truck_id3,
            'date3': self.date3,
            'time3': self.time3,
            'contents3': self.contents3,
            'freeboard3': self.freeboard3,
            'wetted3': self.wetted3,
            'comments3': self.comments3,
            'truck_id4': self.truck_id4,
            'date4': self.date4,
            'time4': self.time4,
            'contents4': self.contents4,
            'freeboard4': self.freeboard4,
            'wetted4': self.wetted4,
            'comments4': self.comments4,
            'truck_id5': self.truck_id5,
            'date5': self.date5,
            'time5': self.time5,
            'contents5': self.contents5,
            'freeboard5': self.freeboard5,
            'wetted5': self.wetted5,
            'comments5': self.comments5,
        }

class form9_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    observer = models.CharField(
        max_length=30
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    crew = models.CharField(
        max_length=1,
        choices=crew_choices
    )
    foreman = models.CharField(
        max_length=30
    )
    start_time = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    end_time = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    leaks = models.CharField(
        max_length=30,
        choices=yes_no_choices
    )
    goose_neck_data = models.CharField(max_length=10000)

    def __str__(self):
        return str(self.date)

class formF1_model(models.Model):
    observer = models.CharField(
        max_length=30
    )
    time = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    retain_date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    status_1 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_2 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_3 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_4 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_5 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_6 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_7 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    comments_1 = models.CharField(
        max_length=30
    )
    comments_2 = models.CharField(
        max_length=30
    )
    comments_3 = models.CharField(
        max_length=30
    )
    comments_4 = models.CharField(
        max_length=30
    )
    comments_5 = models.CharField(
        max_length=30
    )
    comments_6 = models.CharField(
        max_length=30
    )
    comments_7 = models.CharField(
        max_length=30
    )
    action_1 = models.CharField(
        max_length=30
    )
    action_2 = models.CharField(
        max_length=30
    )
    action_3 = models.CharField(
        max_length=30
    )
    action_4 = models.CharField(
        max_length=30
    )
    action_5 = models.CharField(
        max_length=30
    )
    action_6 = models.CharField(
        max_length=30
    )
    action_7 = models.CharField(
        max_length=30
    )
    waste_des_1 = models.CharField(
        max_length=30
    )
    waste_des_2 = models.CharField(
        max_length=30
    )
    waste_des_3 = models.CharField(
        max_length=30
    )
    waste_des_4 = models.CharField(
        max_length=30
    )
    containers_1 = models.IntegerField(
    )
    containers_2 = models.IntegerField(
        blank=True,
        null=True
    )
    containers_3 = models.IntegerField(
        blank=True,
        null=True
    )
    containers_4 = models.IntegerField(
        blank=True,
        null=True
    )
    waste_codes_1 = models.CharField(
        max_length=30,
        choices=waste_code_choices
    )
    waste_codes_2 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    waste_codes_3 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    waste_codes_4 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    dates_1 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    dates_2 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    dates_3 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    dates_4 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.date)

class formF2_model(models.Model):
    observer = models.CharField(
        max_length=30
    )
    time = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    retain_date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    status_1 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_2 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_3 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_4 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_5 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_6 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    comments_1 = models.CharField(
        max_length=30
    )
    comments_2 = models.CharField(
        max_length=30
    )
    comments_3 = models.CharField(
        max_length=30
    )
    comments_4 = models.CharField(
        max_length=30
    )
    comments_5 = models.CharField(
        max_length=30
    )
    comments_6 = models.CharField(
        max_length=30
    )
    action_1 = models.CharField(
        max_length=30
    )
    action_2 = models.CharField(
        max_length=30
    )
    action_3 = models.CharField(
        max_length=30
    )
    action_4 = models.CharField(
        max_length=30
    )
    action_5 = models.CharField(
        max_length=30
    )
    action_6 = models.CharField(
        max_length=30
    )
    waste_des_1 = models.CharField(
        max_length=30
    )
    waste_des_2 = models.CharField(
        max_length=30
    )
    waste_des_3 = models.CharField(
        max_length=30
    )
    waste_des_4 = models.CharField(
        max_length=30
    )
    containers_1 = models.IntegerField(
    )
    containers_2 = models.IntegerField(
        blank=True,
        null=True
    )
    containers_3 = models.IntegerField(
        blank=True,
        null=True
    )
    containers_4 = models.IntegerField(
        blank=True,
        null=True
    )
    waste_codes_1 = models.CharField(
        max_length=30,
        choices=waste_code_choices
    )
    waste_codes_2 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    waste_codes_3 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    waste_codes_4 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    dates_1 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    dates_2 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    dates_3 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    dates_4 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.date)

class formF3_model(models.Model):
    observer = models.CharField(
        max_length=30
    )
    time = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    retain_date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    status_1 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_2 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_3 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_4 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_5 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_6 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    comments_1 = models.CharField(
        max_length=30
    )
    comments_2 = models.CharField(
        max_length=30
    )
    comments_3 = models.CharField(
        max_length=30
    )
    comments_4 = models.CharField(
        max_length=30
    )
    comments_5 = models.CharField(
        max_length=30
    )
    comments_6 = models.CharField(
        max_length=30
    )
    action_1 = models.CharField(
        max_length=30
    )
    action_2 = models.CharField(
        max_length=30
    )
    action_3 = models.CharField(
        max_length=30
    )
    action_4 = models.CharField(
        max_length=30
    )
    action_5 = models.CharField(
        max_length=30
    )
    action_6 = models.CharField(
        max_length=30
    )
    waste_des_1 = models.CharField(
        max_length=30
    )
    waste_des_2 = models.CharField(
        max_length=30
    )
    waste_des_3 = models.CharField(
        max_length=30
    )
    waste_des_4 = models.CharField(
        max_length=30
    )
    containers_1 = models.IntegerField(
    )
    containers_2 = models.IntegerField(
        blank=True,
        null=True
    )
    containers_3 = models.IntegerField(
        blank=True,
        null=True
    )
    containers_4 = models.IntegerField(
        blank=True,
        null=True
    )
    waste_codes_1 = models.CharField(
        max_length=30,
        choices=waste_code_choices
    )
    waste_codes_2 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    waste_codes_3 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    waste_codes_4 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    dates_1 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    dates_2 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    dates_3 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    dates_4 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.date)

class formF4_model(models.Model):
    observer = models.CharField(
        max_length=30
    )
    time = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    retain_date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    status_1 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_2 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_3 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_4 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_5 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_6 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    comments_1 = models.CharField(
        max_length=30
    )
    comments_2 = models.CharField(
        max_length=30
    )
    comments_3 = models.CharField(
        max_length=30
    )
    comments_4 = models.CharField(
        max_length=30
    )
    comments_5 = models.CharField(
        max_length=30
    )
    comments_6 = models.CharField(
        max_length=30
    )
    action_1 = models.CharField(
        max_length=30
    )
    action_2 = models.CharField(
        max_length=30
    )
    action_3 = models.CharField(
        max_length=30
    )
    action_4 = models.CharField(
        max_length=30
    )
    action_5 = models.CharField(
        max_length=30
    )
    action_6 = models.CharField(
        max_length=30
    )
    waste_des_1 = models.CharField(
        max_length=30
    )
    waste_des_2 = models.CharField(
        max_length=30
    )
    waste_des_3 = models.CharField(
        max_length=30
    )
    waste_des_4 = models.CharField(
        max_length=30
    )
    containers_1 = models.IntegerField(
    )
    containers_2 = models.IntegerField(
        blank=True,
        null=True
    )
    containers_3 = models.IntegerField(
        blank=True,
        null=True
    )
    containers_4 = models.IntegerField(
        blank=True,
        null=True
    )
    waste_codes_1 = models.CharField(
        max_length=30,
        choices=waste_code_choices
    )
    waste_codes_2 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    waste_codes_3 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    waste_codes_4 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    dates_1 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    dates_2 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    dates_3 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    dates_4 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.date)

class formF5_model(models.Model):
    observer = models.CharField(
        max_length=30
    )
    time = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    retain_date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    status_1 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_2 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_3 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_4 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_5 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_6 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    comments_1 = models.CharField(
        max_length=30
    )
    comments_2 = models.CharField(
        max_length=30
    )
    comments_3 = models.CharField(
        max_length=30
    )
    comments_4 = models.CharField(
        max_length=30
    )
    comments_5 = models.CharField(
        max_length=30
    )
    comments_6 = models.CharField(
        max_length=30
    )
    action_1 = models.CharField(
        max_length=30
    )
    action_2 = models.CharField(
        max_length=30
    )
    action_3 = models.CharField(
        max_length=30
    )
    action_4 = models.CharField(
        max_length=30
    )
    action_5 = models.CharField(
        max_length=30
    )
    action_6 = models.CharField(
        max_length=30
    )
    waste_des_1 = models.CharField(
        max_length=30
    )
    waste_des_2 = models.CharField(
        max_length=30
    )
    waste_des_3 = models.CharField(
        max_length=30
    )
    waste_des_4 = models.CharField(
        max_length=30
    )
    containers_1 = models.IntegerField(
    )
    containers_2 = models.IntegerField(
        blank=True,
        null=True
    )
    containers_3 = models.IntegerField(
        blank=True,
        null=True
    )
    containers_4 = models.IntegerField(
        blank=True,
        null=True
    )
    waste_codes_1 = models.CharField(
        max_length=30,
        choices=waste_code_choices
    )
    waste_codes_2 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    waste_codes_3 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    waste_codes_4 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    dates_1 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    dates_2 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    dates_3 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    dates_4 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.date)

class formF6_model(models.Model):
    observer = models.CharField(
        max_length=30
    )
    time = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    retain_date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    status_1 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_2 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_3 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_4 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_5 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_6 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    comments_1 = models.CharField(
        max_length=30
    )
    comments_2 = models.CharField(
        max_length=30
    )
    comments_3 = models.CharField(
        max_length=30
    )
    comments_4 = models.CharField(
        max_length=30
    )
    comments_5 = models.CharField(
        max_length=30
    )
    comments_6 = models.CharField(
        max_length=30
    )
    action_1 = models.CharField(
        max_length=30
    )
    action_2 = models.CharField(
        max_length=30
    )
    action_3 = models.CharField(
        max_length=30
    )
    action_4 = models.CharField(
        max_length=30
    )
    action_5 = models.CharField(
        max_length=30
    )
    action_6 = models.CharField(
        max_length=30
    )
    waste_des_1 = models.CharField(
        max_length=30
    )
    waste_des_2 = models.CharField(
        max_length=30
    )
    waste_des_3 = models.CharField(
        max_length=30
    )
    waste_des_4 = models.CharField(
        max_length=30
    )
    containers_1 = models.IntegerField(
    )
    containers_2 = models.IntegerField(
        blank=True,
        null=True
    )
    containers_3 = models.IntegerField(
        blank=True,
        null=True
    )
    containers_4 = models.IntegerField(
        blank=True,
        null=True
    )
    waste_codes_1 = models.CharField(
        max_length=30,
        choices=waste_code_choices
    )
    waste_codes_2 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    waste_codes_3 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    waste_codes_4 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    dates_1 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    dates_2 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    dates_3 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    dates_4 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.date)

class formF7_model(models.Model):
    observer = models.CharField(
        max_length=30
    )
    time = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    retain_date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    status_1 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_2 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_3 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_4 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_5 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    status_6 = models.CharField(
        max_length=30,
        choices=ok_not_ok_choices
    )
    comments_1 = models.CharField(
        max_length=30
    )
    comments_2 = models.CharField(
        max_length=30
    )
    comments_3 = models.CharField(
        max_length=30
    )
    comments_4 = models.CharField(
        max_length=30
    )
    comments_5 = models.CharField(
        max_length=30
    )
    comments_6 = models.CharField(
        max_length=30
    )
    action_1 = models.CharField(
        max_length=30
    )
    action_2 = models.CharField(
        max_length=30
    )
    action_3 = models.CharField(
        max_length=30
    )
    action_4 = models.CharField(
        max_length=30
    )
    action_5 = models.CharField(
        max_length=30
    )
    action_6 = models.CharField(
        max_length=30
    )
    waste_des_1 = models.CharField(
        max_length=30
    )
    waste_des_2 = models.CharField(
        max_length=30
    )
    waste_des_3 = models.CharField(
        max_length=30
    )
    waste_des_4 = models.CharField(
        max_length=30
    )
    containers_1 = models.IntegerField(
    )
    containers_2 = models.IntegerField(
        blank=True,
        null=True
    )
    containers_3 = models.IntegerField(
        blank=True,
        null=True
    )
    containers_4 = models.IntegerField(
        blank=True,
        null=True
    )
    waste_codes_1 = models.CharField(
        max_length=30,
        choices=waste_code_choices
    )
    waste_codes_2 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    waste_codes_3 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    waste_codes_4 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    dates_1 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    dates_2 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    dates_3 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    dates_4 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.date)

class form17_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    estab = models.CharField(max_length=30)
    county = models.CharField(max_length=30)
    estab_no = models.CharField(max_length=30)
    equip_loc = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    observer = models.CharField(max_length=30)
    cert_date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    canvas = models.CharField(max_length=100000)
    reading_data = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )
    ovens_data = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.date)

class form18_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    estab = models.CharField(max_length=30)
    county = models.CharField(max_length=30)
    estab_no = models.CharField(max_length=30)
    equip_loc = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    observer = models.CharField(max_length=30)
    cert_date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    canvas = models.CharField(max_length=100000)
    reading_data = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )
    ovens_data = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )
    
    def __str__(self):
        return str(self.date)

class form19_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    estab = models.CharField(max_length=30)
    county = models.CharField(max_length=30)
    estab_no = models.CharField(max_length=30)
    equip_loc = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    observer = models.CharField(max_length=30)
    cert_date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    canvas = models.CharField(max_length=100000)
    reading_data = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )
    ovens_data = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )
    
    def __str__(self):
        return str(self.date)

class form20_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    week_start = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    week_end = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    data = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )

    def is_fully_filled(self):
        """Check if Monday–Friday have both 'time' and 'observer' filled in the JSON `data` field."""
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        
        if not self.data:
            return False

        for day in weekdays:
            day_data = self.data.get(day)

            if isinstance(day_data, dict):
                time = day_data.get("time", "").strip()
                observer = day_data.get("observer", "").strip()

                if not time or not observer:
                    return False

        return True
    
    def __str__(self):
        return str(self.week_start)
 
class form21_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    today = datetime.date.today()

    week_start = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    week_end = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    time_0 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time_1 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time_2 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time_3 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time_4 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time_5 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time_6 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    obser_0 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    obser_1 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    obser_2 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    obser_3 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    obser_4 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    obser_5 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    obser_6 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    vents_0 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    vents_1 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    vents_2 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    vents_3 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    vents_4 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    vents_5 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    vents_6 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    mixer_0 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    mixer_1 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    mixer_2 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    mixer_3 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    mixer_4 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    mixer_5 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    mixer_6 = models.CharField(
        max_length=30,
        choices=yes_no_choices,
        blank=True,
        null=True
    )
    v_comments_0 = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    v_comments_1 = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    v_comments_2 = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    v_comments_3 = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    v_comments_4 = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    v_comments_5 = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    v_comments_6 = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    m_comments_0 = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    m_comments_1 = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    m_comments_2 = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    m_comments_3 = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    m_comments_4 = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    m_comments_5 = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    m_comments_6 = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )

    def is_fully_filled(self):
        """Checks if all 7 days have both required fields (time, observer, vents, mixer) filled."""
        for i in range(7):  # Monday to Sunday
            if not all([
                getattr(self, f"time_{i}"),
                getattr(self, f"obser_{i}"),
                getattr(self, f"vents_{i}"),
                getattr(self, f"mixer_{i}")
            ]):
                return False  # Missing a required field → Not fully filled
        return True  # Everything is filled
    
    def __str__(self):
        return str(self.week_start)
    



class form22_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
    )
    paved = models.CharField(
        max_length=30,
        choices=paved_roads
    )
    pav_start = models.TimeField(
        auto_now_add=False,
        auto_now=False,
    )
    pav_stop = models.TimeField(
        auto_now_add=False,
        auto_now=False,
    )
    unpaved = models.CharField(
        max_length=30,
        choices=unpaved_roads
    )
    unp_start = models.TimeField(
        auto_now_add=False,
        auto_now=False,
    )
    unp_stop = models.TimeField(
        auto_now_add=False,
        auto_now=False,
    )
    parking = models.CharField(
        max_length=30,
        choices=parking_lots
    )
    par_start = models.TimeField(
        auto_now_add=False,
        auto_now=False,
    )
    par_stop = models.TimeField(
        auto_now_add=False,
        auto_now=False,
    )
    observer = models.CharField(
        max_length=30
    )
    cert_date = models.DateField(
        auto_now_add=False,
        auto_now=False,
    )
    comments = models.CharField(
        max_length=300
    )

    def __str__(self):
        return str(self.date)

class form22_readings_model(models.Model):
    form = models.OneToOneField(
        form22_model,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    pav_1 = models.CharField(
        max_length=30,
    )
    pav_2 = models.CharField(
        max_length=30,
    )
    pav_3 = models.CharField(
        max_length=30,
    )
    pav_4 = models.CharField(
        max_length=30,
    )
    pav_5 = models.CharField(
        max_length=30,
    )
    pav_6 = models.CharField(
        max_length=30,
    )
    pav_7 = models.CharField(
        max_length=30,
    )
    pav_8 = models.CharField(
        max_length=30,
    )
    pav_9 = models.CharField(
        max_length=30,
    )
    pav_10 = models.CharField(
        max_length=30,
    )
    pav_11 = models.CharField(
        max_length=30,
    )
    pav_12 = models.CharField(
        max_length=30,
    )

    unp_1 = models.CharField(
        max_length=30,
    )
    unp_2 = models.CharField(
        max_length=30,
    )
    unp_3 = models.CharField(
        max_length=30,
    )
    unp_4 = models.CharField(
        max_length=30,
    )
    unp_5 = models.CharField(
        max_length=30,
    )
    unp_6 = models.CharField(
        max_length=30,
    )
    unp_7 = models.CharField(
        max_length=30,
    )
    unp_8 = models.CharField(
        max_length=30,
    )
    unp_9 = models.CharField(
        max_length=30,
    )
    unp_10 = models.CharField(
        max_length=30,
    )
    unp_11 = models.CharField(
        max_length=30,
    )
    unp_12 = models.CharField(
        max_length=30,
    )

    par_1 = models.CharField(
        max_length=30,
    )
    par_2 = models.CharField(
        max_length=30,
    )
    par_3 = models.CharField(
        max_length=30,
    )
    par_4 = models.CharField(
        max_length=30,
    )
    par_5 = models.CharField(
        max_length=30,
    )
    par_6 = models.CharField(
        max_length=30,
    )
    par_7 = models.CharField(
        max_length=30,
    )
    par_8 = models.CharField(
        max_length=30,
    )
    par_9 = models.CharField(
        max_length=30,
    )
    par_10 = models.CharField(
        max_length=30,
    )
    par_11 = models.CharField(
        max_length=30,
    )
    par_12 = models.CharField(
        max_length=30,
    )
    
    pav_total = models.CharField(
        max_length=30,
    )
    unp_total = models.CharField(
        max_length=30,
    )
    par_total = models.CharField(
        max_length=30,
    )
    def __str__(self):
        return str(self.form)

class form24_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    observer = models.CharField(
        max_length=30
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False
    )
    data = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.date)
 
class form25_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    observer = models.CharField(
        max_length=30
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False
    )
    data = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.date)

class issues_model(models.Model):
    userChoice = models.ForeignKey(
        'user_profile_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    formChoice = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    issues = models.CharField(max_length=300)
    notified = models.CharField(max_length=30)
    time = models.TimeField(
        auto_now_add=False,
        auto_now=False,
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    cor_action = models.CharField(max_length=150)
    out_of_compliance = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return f"CorrectiveAction: {self.id} - {self.date} - {self.issues}"

class Event(models.Model):
    userProf = models.ForeignKey(
        'user_profile_model',
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    facilityChoice = models.ForeignKey(
        facility_model, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    cal_title_choices = (
        ('P', 'Primary'),
        ('BU', 'Back Up'),
        ('Off', 'Off'),
        ('Office', 'Office '),
        ('BH', 'BagHouses'),
        ('QT', 'Quarterly Trucks'),
        ('BH2-S', 'Boilerhouse Stacks'),
    )
    allDay = models.BooleanField()
    observer = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    title = models.CharField(
        max_length=50,
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    start_time = models.TimeField(u'Starting time', help_text=u'Starting time', null=True, default='00:00:00')
    end_time = models.TimeField(u'Final time', help_text=u'Final time', null=True, blank=True, default='23:59:00')
    notes = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)
    calendarChoice = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        default="Personal"
    )
    repeat = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )
    alerts = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )


    class META:
        verbose_name = u'Scheduling'
        verbose_name_plural = u'Scheduling'

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:  # edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end):  # innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:  # outter limits
            overlap = True

        return overlap

    def get_absolute_url2(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s - %s</a>' % (url, str(self.title), str(self.observer))

    def get_absolute_url(self):
        url = '../../event_detail/' + str(self.id) + '/view'
        return u'<a href="%s">%s - %s</a>' % (url, str(self.title), str(self.observer))

    def clean(self):
        if str(self.end_time) <= str(self.start_time):
            raise ValidationError('Ending times must after starting times')

class form29_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    observer = models.CharField(
        max_length=150
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False
    )
    month = models.CharField(
        max_length=30
    )
    data = models.JSONField(
        default=dict
    )
    
    # def is_fully_filled(self):
    #     """Checks if all 7 days have both required fields (time, observer, vents, mixer) filled."""
    #     for i in range(7):  # Monday to Sunday
    #         if not all([
    #             getattr(self, f"time_{i}"),
    #             getattr(self, f"obser_{i}"),
    #             getattr(self, f"vents_{i}"),
    #             getattr(self, f"mixer_{i}")
    #         ]):
    #             return False  # Missing a required field → Not fully filled
    #     return True  # Everything is filled

    def __str__(self):
        return str(self.month)

class SpillKit_model(models.Model):
    form = models.ForeignKey('form29_model', related_name="spill_kits", on_delete=models.CASCADE)
    label = models.CharField(max_length=50)
    tag_on = models.CharField(
        max_length=3,
        choices=yes_no_choices,
        blank=True,
        null=True,
    )
    serial = models.CharField(
        max_length=7,
        blank=True,
        null=True,
    )
    complete = models.CharField(
        max_length=3,
        choices=yes_no_choices,
        blank=True,
        null=True,
    )
    report = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )
    comment = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"form29 ID: {self.form.id} - Spill Kit: {self.label}"

class quarterly_trucks_model(models.Model):
    facilityChoice = models.ForeignKey(facility_model, on_delete=models.CASCADE, blank=True, null=True)
    quarter = models.CharField(
        choices=quarter_choices,
        max_length=4,
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False
    )
    
    observer_5_1 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    date_5_1 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time_5_1 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    comments_5_1 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    rear_gate_5_1 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    box_interior_5_1 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    box_exterior_5_1 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    exhaust_5_1 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    
    observer_6_2 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    date_6_2 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time_6_2 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    comments_6_2 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    rear_gate_6_2 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    box_interior_6_2 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    box_exterior_6_2 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    exhaust_6_2 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    
    observer_7_3 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    date_7_3 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time_7_3 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    comments_7_3 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    rear_gate_7_3 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    box_interior_7_3 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    box_exterior_7_3 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    exhaust_7_3 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    
    observer_9_4 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    date_9_4 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time_9_4 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    comments_9_4 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    rear_gate_9_4 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    box_interior_9_4 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    box_exterior_9_4 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    exhaust_9_4 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    
    def __str__(self):
        return str(self.date)

    def whatever(self):
        return{
            'observer_5_1': self.observer_5_1,
            'date_5_1': self.date_5_1,
            'time_5_1': self.time_5_1,
            'comments_5_1': self.comments_5_1,
            'rear_gate_5_1': self.rear_gate_5_1,
            'box_interior_5_1': self.box_interior_5_1,
            'box_exterior_5_1': self.box_exterior_5_1,
            'exhaust_5_1': self.exhaust_5_1,
            'observer_6_2': self.observer_6_2,
            'date_6_2': self.date_6_2,
            'time_6_2': self.time_6_2,
            'comments_6_2': self.comments_6_2,
            'rear_gate_6_2': self.rear_gate_6_2,
            'box_interior_6_2': self.box_interior_6_2,
            'box_exterior_6_2': self.box_exterior_6_2,
            'exhaust_6_2': self.exhaust_6_2,
            'observer_7_3': self.observer_7_3,
            'date_7_3': self.date_7_3,
            'time_7_3': self.time_7_3,
            'comments_7_3': self.comments_7_3,
            'rear_gate_7_3': self.rear_gate_7_3,
            'box_interior_7_3': self.box_interior_7_3,
            'box_exterior_7_3': self.box_exterior_7_3,
            'exhaust_7_3': self.exhaust_7_3,
            'observer_9_4': self.observer_9_4,
            'date_9_4': self.date_9_4,
            'time_9_4': self.time_9_4,
            'comments_9_4': self.comments_9_4,
            'rear_gate_9_4': self.rear_gate_9_4,
            'box_interior_9_4': self.box_interior_9_4,
            'box_exterior_9_4': self.box_exterior_9_4,
            'exhaust_9_4': self.exhaust_9_4,
        }

class form27_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    quarter = models.CharField(
        choices=quarter_choices,
        max_length=4,
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False
    )
    
    observer_5_1 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    date_5_1 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time_5_1 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    comments_5_1 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    rear_gate_5_1 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    box_interior_5_1 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    box_exterior_5_1 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    exhaust_5_1 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    
    observer_6_2 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    date_6_2 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time_6_2 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    comments_6_2 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    rear_gate_6_2 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    box_interior_6_2 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    box_exterior_6_2 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    exhaust_6_2 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    
    observer_7_3 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    date_7_3 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time_7_3 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    comments_7_3 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    rear_gate_7_3 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    box_interior_7_3 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    box_exterior_7_3 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    exhaust_7_3 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    
    observer_9_4 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    date_9_4 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    time_9_4 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    comments_9_4 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    rear_gate_9_4 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    box_interior_9_4 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    box_exterior_9_4 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    exhaust_9_4 = models.CharField(
        choices=yes_no_na_choices,
        max_length=4,
        blank=True,
        null=True
    )
    
    def __str__(self):
        return str(self.date)
    
    def is_fully_filled(self):
        """Checks if all fields are filled (not None or empty)."""
        fields = [field.name for field in self._meta.get_fields() if isinstance(field, models.Field) and field.name not in ['id', 'facilityChoice', 'formSettings', 'quarter', 'date']]
        
        return all(bool(getattr(self, field)) for field in fields)

    def whatever(self):
        return{
            'observer_5_1': self.observer_5_1,
            'date_5_1': self.date_5_1,
            'time_5_1': self.time_5_1,
            'comments_5_1': self.comments_5_1,
            'rear_gate_5_1': self.rear_gate_5_1,
            'box_interior_5_1': self.box_interior_5_1,
            'box_exterior_5_1': self.box_exterior_5_1,
            'exhaust_5_1': self.exhaust_5_1,
            'observer_6_2': self.observer_6_2,
            'date_6_2': self.date_6_2,
            'time_6_2': self.time_6_2,
            'comments_6_2': self.comments_6_2,
            'rear_gate_6_2': self.rear_gate_6_2,
            'box_interior_6_2': self.box_interior_6_2,
            'box_exterior_6_2': self.box_exterior_6_2,
            'exhaust_6_2': self.exhaust_6_2,
            'observer_7_3': self.observer_7_3,
            'date_7_3': self.date_7_3,
            'time_7_3': self.time_7_3,
            'comments_7_3': self.comments_7_3,
            'rear_gate_7_3': self.rear_gate_7_3,
            'box_interior_7_3': self.box_interior_7_3,
            'box_exterior_7_3': self.box_exterior_7_3,
            'exhaust_7_3': self.exhaust_7_3,
            'observer_9_4': self.observer_9_4,
            'date_9_4': self.date_9_4,
            'time_9_4': self.time_9_4,
            'comments_9_4': self.comments_9_4,
            'rear_gate_9_4': self.rear_gate_9_4,
            'box_interior_9_4': self.box_interior_9_4,
            'box_exterior_9_4': self.box_exterior_9_4,
            'exhaust_9_4': self.exhaust_9_4,
        }

def sop_file_upload_path(instance, filename):
    # Format the filename: replace spaces with underscores and clean up the name
    base, ext = os.path.splitext(filename)
    formatted_filename = slugify(base).replace('-', '_') + ext  # e.g., SOP__-_Collection_Main_2020-12-11.pdf
    return f'SOPs/{formatted_filename}'

class sop_model(models.Model):
    facilityChoice = models.ForeignKey(facility_model, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=50
    )
    revision_date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    pdf_file = models.FileField(upload_to='SOPs/')
    pdf_url = models.URLField(
        max_length=1024,
        blank=True
    )
    
    def __str__(self):
        return str(self.name)
      
class signature_model(models.Model):
    facilityChoice = models.ForeignKey(facility_model, on_delete=models.CASCADE, blank=True, null=True)
    supervisor = models.CharField(
        max_length=30
    )
    sign_date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    canvas = models.CharField(
        max_length=100000
    )
    
    def __str__(self):
        return str(self.sign_date)
    
class spill_kit_inventory_model(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    inspector = models.CharField(max_length=40)
    skID = models.IntegerField()
    type = models.CharField(max_length=50, choices=spill_kit_choices)
    counted_items = models.CharField(max_length=300)
    missing_items = models.CharField(max_length=300)
    
    def __str__(self):
        return str(self.date) + ' - ' + str(self.skID)
    
class form26_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    form29 = models.ForeignKey(
        'Form29_model',
        on_delete=models.CASCADE,
        related_name="inventories",
        null=True,
        blank=True
    )
    date = models.DateField(auto_now=False, auto_now_add=False)
    inspector = models.CharField(max_length=40)
    skID = models.IntegerField()
    type = models.CharField(max_length=50, choices=spill_kit_choices)
    counted_items = models.CharField(max_length=300)
    missing_items = models.CharField(max_length=300)
    
    def __str__(self):
        return str(self.date) + ' - ' + str(self.skID)
  
class notifications_model(models.Model):
    facilityChoice = models.ForeignKey(
        facility_model,
        on_delete=models.CASCADE, 
        null=True
    )
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    user = models.ForeignKey(
        user_profile_model,
        on_delete=models.CASCADE, 
        null=True
    )
    clicked = models.BooleanField(default=False)
    hovered = models.BooleanField(default=False)
    formData = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )
    header = models.CharField(
        max_length=50,
        choices=notification_header_choices
    )
    body = models.CharField(
        max_length=150
    )
    notes = models.CharField(
        max_length=150
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.id}-{self.created_at}-SELF_FORM_SETTINGS-{self.user}-{self.header}"
    
class braintreePlans(models.Model):
    planID = models.CharField(
        max_length=50
    )
    priceID = models.CharField(
        max_length=50
    )
    name = models.CharField(
        max_length=150
    )
    price = models.FloatField()
    description = models.CharField(
        max_length=150
    )
    def __str__(self):
        return str(self.name) + ' - ' + str(self.planID)
    
class tokens_model(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    token = models.CharField(
        max_length=100
    )
    def __str__(self):
        return str(self.id) + ' - ' + str(self.token)
    
class facility_tags_register_model(models.Model):
    orientation_choices = (
        ('horizontal', 'Horizontal'),
        ('vertical', 'Vertical'),
        ('rectangular', 'Rectangular')
    )
    tankID = models.CharField(max_length=20)
    facilityChoice = models.ForeignKey(facility_model, on_delete=models.CASCADE, blank=True, null=True)
    last_inspection_date = models.DateField(
        auto_now=False, 
        auto_now_add=False,
        null=True,
        blank=True
    )
    manufacturer = models.CharField(
        max_length=70,
        null=True,
        blank=True
    )
    contents = models.CharField(max_length=40)
    construction_date = models.DateField(
        auto_now=False, 
        auto_now_add=False,
        null=True,
        blank=True
    )
    last_repair_reconstruction = models.DateField(
        auto_now=False, 
        auto_now_add=False,
        null=True,
        blank=True
    )
    height = models.CharField(max_length=20)
    diameter = models.CharField(max_length=20)
    capacity = models.CharField(max_length=20)
    last_change_service_date = models.DateField(
        auto_now=False, 
        auto_now_add=False,
        null=True,
        blank=True
    )
    construction = models.CharField(max_length=200)
    design = models.CharField(max_length=40)
    orientation = models.CharField(
        max_length=40,
        choices=orientation_choices
    )
    containment = models.CharField(max_length=40)
    CRDM = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    release_prevention_barrier = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    
    def __str__(self):
        return str(self.facilityChoice.facility_name) + ' - ' + str(self.tankID)
    
class form28_model(models.Model):
    facilityChoice = models.ForeignKey(facility_model, on_delete=models.CASCADE, blank=True, null=True)
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    inspector = models.CharField(max_length=40)
    date = models.DateField(auto_now=False, auto_now_add=False)
    tankChoice = models.ForeignKey(facility_tags_register_model, on_delete=models.CASCADE)
    retain_until_date = models.DateField(auto_now=False, auto_now_add=False)
    prior_inspection_date = models.DateField(auto_now=False, auto_now_add=False)
    containment_structure = models.CharField(max_length=100)
    primary_tank = models.CharField(max_length=100)
    cont_drain_valves = models.CharField(max_length=100)
    pathways_entry = models.CharField(max_length=100)
    tank_leaks = models.CharField(max_length=100)
    secondary_cont_leaks = models.CharField(max_length=100)
    interstice_leaks = models.CharField(max_length=100)
    valves = models.CharField(max_length=200)
    spill_cont_boxes = models.CharField(max_length=200)
    liquid_level_equipment = models.CharField(max_length=200)
    overfill_equipment = models.CharField(max_length=200)
    piping_connections = models.CharField(max_length=100)
    ladder_platform_structure = models.CharField(max_length=100)
    other_conditions = models.CharField(max_length=200)
    additional_comments = models.CharField(max_length=200)
    
    def __str__(self):
        return str(self.facilityChoice.facility_name) + ' - ' + str(self.tankChoice.tankID)
    
class FAQ_model(models.Model):
    section = models.CharField(max_length=75)
    question = models.CharField(max_length=150)
    answer = models.CharField(max_length=700)
    link = models.CharField(
        max_length=30,
        null=True, 
        blank=True
    )
    def __str__(self):
        return str(self.question)
  
class form_requests_model(models.Model):
    days_choices2 = (
        ('','Days Available'),
        ('Everyday', 'Everyday'),
        ('0', 'Mondays'),
        ('1', 'Tuesdays'),
        ('2', 'Wednesdays'),
        ('3', 'Thursdays'),
        ('4', 'Fridays'),
        ('5', 'Saturdays'),
        ('6', 'Sundays'),
        ('Weekends', 'Weekends'),
        ('Weekdays', 'Weekdays'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=150)
    how_data_is_collected = models.CharField(max_length=700)
    inspection_of = models.CharField(max_length=150)
    form_example_file = models.FileField(upload_to='formRequests/')
    form_example_url = models.CharField(
        max_length=1000000,
        blank=True
    )
    optimize = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )
    detailed_description = models.CharField(max_length=1000)
    callBack_days = models.CharField(
        max_length=30,
        choices=days_choices2
    )
    callBack_time = models.TimeField(
        auto_now_add=False,
        auto_now=False
    )
    callBack_time_freq= models.CharField(
        max_length=15,
        choices=(
            ('before', 'Before'),
            ('after', 'After')
        )
    )
    frequency = models.CharField(
        max_length=40,
        choices=frequent_choices
    )

    def __str__(self):
        return str(self.user) + ' - ' + str(self.name)

class account_reactivation_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reactivation_date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return str(self.id) + ' - ' + str(self.user)

class TrafficData(models.Model):
    date = models.DateField()
    views = models.IntegerField()
    unique_visitors = models.IntegerField()

    def __str__(self):
        return f"Traffic on {self.date}"

class form30_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    observer = models.CharField(
        max_length=30
    )
    date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    time = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    area_name = models.CharField(max_length=100)
    inspection_json = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )
    containers_json = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )
    def __str__(self):
        return str(self.date) + " - " + str(self.area_name)

class form31_model(models.Model):
    formSettings = models.ForeignKey(
        'form_settings_model', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    observer = models.CharField(max_length=255, verbose_name="Inspector Name")
    date = models.DateField(verbose_name="Inspection Date")
    time = models.TimeField(verbose_name="Inspection Time")
    tank_json = models.JSONField(default=dict, verbose_name="Tank Data")  # Stores dynamic tank data

    def __str__(self):
        return f"Monthly Tanks: {self.date}"
    
class stripe_model(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name='stripe'
    )
    settings = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.id) + "-" + str(self.user.last_name)

class subscription(models.Model):
    companyChoice = models.OneToOneField(
        "company_model", 
        on_delete=models.PROTECT,
        related_name='subscription'
    )
    subscriptionID = models.CharField(
        max_length=100
    )
    plan = models.ForeignKey(
        'braintreePlans', 
        on_delete=models.PROTECT, 
        blank=True, 
        null=True
    )
    status = models.CharField(max_length=20)
    customerID = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    settings = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.companyChoice.company_name} - {self.plan}"
    
# class tank_library(models.Model):
#     title = models.CharField(max_length=40)
#     description = models.TextField()
#     pic_file = models.FileField(
#         upload_to='tank_library/',
#         blank=True,
#         null=True
#     )
#     pic_url = models.CharField(
#         max_length=1000000,
#         blank=True,
#         null=True
#     )