from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.urls import reverse
import datetime


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

foreman_choices = (
    ('Zajas', 'Zajas'),
    ('Folding', 'Folding'),
    ('Cooper', 'Cooper'),
    ('Lopez', 'Lopez')
)

crew_choices = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D')
)

plume_type_choices = (
    ('N/A', 'N/A'),
    ('Fugative', 'Fugative'),
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
    ('Contractor', 'Contractor')
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
    ('#4 Booster Station', '#4 Booster Station'),
    ('#5 Battery Road', '#5 Battery Road'),
    ('Coal Dump Horseshoe', 'Coal Dump Horseshoe'),
    ('Coal Handling Road (Partial)', 'Coal Handling Road (Partial)'),
    ('Coke Plant Road', 'Coke Plant Road'),
    ('Coke Plant Mech Road', 'Coke Plant Mech Road'),
    ('North Gate Area', 'North Gate Area'),
    ('Compund Road', 'Compund Road'),
    ('D-4 Blast Furnace Road', 'D-4 Blast Furnace Road'),
    ('Gap Gate Road', 'Gap Gate Road'),
    ('#3 Ore Dock Road', '#3 Ore Dock Road'),
    ('River Road', 'River Road'),
    ('Weigh Station Road', 'Weigh Station Road'),
    ('Zug Island Road', 'Zug Island Road')
)
unpaved_roads = (
    ('North Gate Truck Turn', 'North Gate Truck Turn'),
    ('Screening Station Road', 'Screening Station Road'),
    ('Coal Handling Road (Partial)', 'Coal Handling Road (Partial)'),
    ('Taj Mahal Road', 'Taj Mahal Road'),
    ('PECS Approach', 'PECS Approach'),
    ('No. 2 Boilerhouse Road', 'No. 2 Boilerhouse Road')
)
parking_lots = (
    ('Gap Gate Parking', 'Gap Gate Parking'),
    ('Truck Garage Area', 'Truck Garage Area'),
    ('EES Coke Office Parking', 'EES Coke Office Parking'),
)
storage_piles = (
    ('Area B Coke Storage Piles', 'Area B Coke Storage Piles'),
    ('EES Coke Coal Storage Piles', 'EES Coke Coal Storage Piles'),
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
    ('Quaterly', 'Quaterly '),
    ('Semi-Annual', 'Semi-Annual'),
    ('Annual', 'Annual')
)
all_users = User.objects.all()
all_user_choices_0 = ((x.username, x.get_full_name()) for x in all_users)
all_user_choices_1 = ((h.username, h.get_full_name()) for h in all_users)
all_user_choices_2 = ((a.username, a.get_full_name()) for a in all_users)
all_user_choices_3 = ((b.username, b.get_full_name()) for b in all_users)
all_user_choices_4 = ((c.username, c.get_full_name()) for c in all_users)

# Create your models here.


class Forms(models.Model):
    form = models.CharField(max_length=30)
    frequency = models.CharField(max_length=30, choices = frequent_choices)
    link = models.CharField(max_length=30)
    header = models.CharField(max_length=80)
    title = models.CharField(max_length=80)
    due_date = models.DateField(auto_now_add=False, auto_now=False, blank = True)
    date_submitted = models.DateField(auto_now_add=False, auto_now=False, blank = True)
    submitted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.form
    
class subC(models.Model):
    date = models.DateField(auto_now_add=False, auto_now=False)
    truck_sel = models.CharField(max_length=30, choices=truck_choices)
    area_sel = models.CharField(max_length=30, choices=area_choices)
    truck_start_time = models.TimeField(max_length=30)
    truck_stop_time = models.TimeField(max_length=30)
    area_start_time = models.TimeField(max_length=30)
    area_stop_time = models.TimeField(max_length=30)
    observer = models.CharField(
        max_length=30,
        choices = all_user_choices_0
    )
    cert_date = models.DateField(
        auto_now_add=False, 
        auto_now=False
    )
    comments = models.CharField(
        max_length=300
    )
    average_t = models.IntegerField(blank=True)
    average_p = models.IntegerField(blank=True)
    
    def __str__(self):
        return str(self.date)
    
    
class FormCReadings(models.Model):
    form = models.OneToOneField(
        subC,
        on_delete=models.CASCADE,
    )
    TRead1 = models.CharField(max_length=3)
    TRead2 = models.CharField(max_length=3)
    TRead3 = models.CharField(max_length=3)
    TRead4 = models.CharField(max_length=3)
    TRead5 = models.CharField(max_length=3)
    TRead6 = models.CharField(max_length=3)
    TRead7 = models.CharField(max_length=3)
    TRead8 = models.CharField(max_length=3)
    TRead9 = models.CharField(max_length=3)
    TRead10 = models.CharField(max_length=3)
    TRead11 = models.CharField(max_length=3)
    TRead12 = models.CharField(max_length=3)
    ARead1 = models.CharField(max_length=3)
    ARead2 = models.CharField(max_length=3)
    ARead3 = models.CharField(max_length=3)
    ARead4 = models.CharField(max_length=3)
    ARead5 = models.CharField(max_length=3)
    ARead6 = models.CharField(max_length=3)
    ARead7 = models.CharField(max_length=3)
    ARead8 = models.CharField(max_length=3)
    ARead9 = models.CharField(max_length=3)
    ARead10 = models.CharField(max_length=3)
    ARead11 = models.CharField(max_length=3)
    ARead12 = models.CharField(max_length=3)
    
    def __str__(self):
        return str(self.form)
    
    
    
class Profile(models.Model):
    
    Name = models.CharField(max_length=30)
    cer_date = models.DateField(auto_now_add=False, auto_now=False, blank=True)
    
    def __str__(self):
        return self.name
    
    
class daily_battery_profile_model(models.Model):
    foreman = models.CharField(max_length=10, choices=foreman_choices)
    crew = models.CharField(max_length=1, choices=crew_choices)
    inop_ovens = models.CharField(max_length=2)
    date_save = models.DateField(auto_now_add=True, auto_now=False)
    time_log = models.TimeField(auto_now_add=True, auto_now=False)
    
    def __str__(self):
        return str(self.date_save)

    
    
class bat_info_model(models.Model):
    bat_num = models.CharField(max_length=30)
    total_ovens = models.CharField(max_length=30)
    facility_name = models.CharField(max_length=30)
    County = models.CharField(max_length=30)
    estab_num = models.CharField(max_length=30)
    equip_location = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    process_equip1 = models.CharField(max_length=30)
    process_equip2 = models.CharField(max_length=30)
    op_mode1 = models.CharField(max_length=30)
    op_mode2 = models.CharField(max_length=30)
    emission_point = models.CharField(max_length=30)
    bat_height = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name
    
class user_profile_model(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    
    cert_date = models.DateField(auto_now_add=False, auto_now=False, blank= True)
    profile_picture = models.ImageField(blank = True, null = True)
    
    def __str__(self):
        return self.user.username
    
    
class subA1_model(models.Model):
    observer = models.CharField(max_length=30)
    date = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
    )
    crew = models.CharField(
        max_length=1, 
        choices = crew_choices
    )
    foreman = models.CharField(
        max_length=30,
        choices = foreman_choices
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
    
    def __str__(self):
        return str(self.date)
    
    
class subA1_readings_model(models.Model):
    form = models.OneToOneField(
        subA1_model, 
        on_delete=models.CASCADE, 
        primary_key=True,
    )
    c1_no = models.CharField(
        max_length=2
    )
    c2_no = models.CharField(
        max_length=2
    )
    c3_no = models.CharField(
        max_length=2
    )
    c4_no = models.CharField(
        max_length=2
    )
    c5_no = models.CharField(
        max_length=2
    )
    c1_start = models.TimeField(
        auto_now_add = False,
        auto_now = False,
        blank = True,
    )
    c2_start = models.TimeField(
        auto_now_add = False,
        auto_now = False,
        blank = True,
    )
    c3_start = models.TimeField(
        auto_now_add = False,
        auto_now = False,
        blank = True,
    )
    c4_start = models.TimeField(
        auto_now_add = False,
        auto_now = False,
        blank = True,
    )
    c5_start = models.TimeField(
        auto_now_add = False,
        auto_now = False,
        blank = True,
    )
    c1_stop = models.TimeField(
        auto_now_add = False,
        auto_now = False,
        blank = True,
    )
    c2_stop = models.TimeField(
        auto_now_add = False,
        auto_now = False,
        blank = True,
    )
    c3_stop = models.TimeField(
        auto_now_add = False,
        auto_now = False,
        blank = True,
    )
    c4_stop = models.TimeField(
        auto_now_add = False,
        auto_now = False,
        blank = True,
    )
    c5_stop = models.TimeField(
        auto_now_add = False,
        auto_now = False,
        blank = True,
    )
    c1_sec = models.FloatField(
        max_length=5
    )
    c2_sec = models.FloatField(
        max_length=5
    )
    c3_sec = models.FloatField(
        max_length=5
    )
    c4_sec = models.FloatField(
        max_length=5
    )
    c5_sec = models.FloatField(
        max_length=5
    )
    c1_comments = models.CharField(
        max_length=30
    )
    c2_comments = models.CharField(
        max_length=30
    )
    c3_comments = models.CharField(
        max_length=30
    )
    c4_comments = models.CharField(
        max_length=30
    )
    c5_comments = models.CharField(
        max_length=30
    )
    larry_car = models.CharField(
        max_length=30,
        choices = larry_car_choices
    )
    comments = models.CharField(
        max_length=300
    )
    total_seconds = models.FloatField(
        max_length=30
    )
    
    def __str__(self):
        return str(self.form)
 #----------------------------------------------------------------------FORM D---------------<   
    
class formA2_model(models.Model):
    observer = models.CharField(max_length=30)
    date = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
    )
    inop_ovens = models.IntegerField(
    )
    crew = models.CharField(
        max_length=1, 
        choices = crew_choices
    )
    foreman = models.CharField(
        max_length=30,
        choices = foreman_choices
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
    
    p_leak_oven1 = models.CharField(
        max_length=2,
        blank=True,
        null = True
    )
    p_leak_loc1 = models.CharField(
        max_length=30,
        choices = door_location,
        blank=True,
        null = True
    )
    p_leak_zone1 = models.CharField(
        max_length=30,
        choices = door_zone,
        blank=True,
        null = True
    )
    c_leak_oven1 = models.CharField(
        max_length=2,
        blank=True,
        null = True
    )
    c_leak_loc1 = models.CharField(
        max_length=30,
        choices = door_location,
        blank=True,
        null = True
    )
    c_leak_zone1 = models.CharField(
        max_length=30,
        choices = door_zone,
        blank=True,
        null = True
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
    
    
class formA3_model(models.Model):
    observer = models.CharField(max_length=30)
    date = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
    )
    inop_ovens = models.IntegerField(
    )
    crew = models.CharField(
        max_length=1, 
        choices = crew_choices
    )
    foreman = models.CharField(
        max_length=30,
        choices = foreman_choices
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
    om_oven1 = models.CharField(
        max_length=2,
        blank=True,
        null = True
    )
    om_loc1 = models.CharField(
        max_length=30,
        choices = om_location,
        blank=True,
        null = True
    )
    l_oven1 = models.CharField(
        max_length=2,
        blank=True,
        null = True
    )
    l_loc1 = models.CharField(
        max_length=30,
        choices = l_location,
        blank=True,
        null = True
    )
    om_traverse_time_min = models.CharField(max_length=30)
    om_traverse_time_sec = models.CharField(max_length=30)
    l_traverse_time_min = models.CharField(max_length=30)
    l_traverse_time_sec = models.CharField(max_length=30)
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
    notes = models.CharField(max_length=30)
    
    def __str__(self):
        return str(self.date)
    
class formA4_model(models.Model):
    observer = models.CharField(max_length=30)
    date = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
    )
    crew = models.CharField(
        max_length=1, 
        choices = crew_choices
    )
    foreman = models.CharField(
        max_length=30,
        choices = foreman_choices
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
    suction_main = models.CharField(
        max_length=30
    )
    oven_leak_1 = models.CharField(
        max_length=2,
        blank = True,
        null = True,
    )
    time_leak_1 = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null = True,
    )
    date_temp_seal_leak_1 = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
        null = True,
    )
    time_temp_seal_leak_1 = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null = True,
    )
    temp_seal_by_leak_1 = models.CharField(
        max_length=30,
        blank = True,
        null = True,
    )
    date_init_repair_leak_1 = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
        null = True,
    )
    time_init_repair_leak_1 = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null = True,
    )
    date_comp_repair_leak_1 = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
        null = True,
    )
    time_comp_repair_leak_1 = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null = True,
    )
    comp_by_leak_1 = models.CharField(
        max_length=30,
        blank = True,
        null = True,
    )
    notes = models.CharField(max_length=30)
    
    def __str__(self):
        return str(self.date)
    
class subA5_model(models.Model):
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
    observer = models.CharField(max_length=30)
    cert_date = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
    )
    process_equip1 = models.CharField(max_length=50)
    process_equip2 = models.CharField(max_length=50)
    op_mode1 = models.CharField(max_length=30)
    op_mode2 = models.CharField(max_length=30)
    background_color_start = models.CharField(max_length=30)
    background_color_stop = models.CharField(max_length=30)
    sky_conditions = models.CharField(max_length=30)
    wind_speed_start = models.CharField(max_length=2)
    wind_speed_stop = models.CharField(max_length=4)
    wind_direction =models.CharField(max_length=3)
    emission_point_start = models.CharField(max_length=50)
    emission_point_stop = models.CharField(max_length=50)
    ambient_temp_start = models.CharField(max_length=3)
    ambient_temp_stop = models.CharField(max_length=4)
    humidity = models.CharField(max_length=3)
    height_above_ground = models.CharField(max_length=30)
    height_rel_observer = models.CharField(max_length=30)
    distance_from = models.CharField(max_length=30)
    direction_from = models.CharField(max_length=3)
    describe_emissions_start = models.CharField(max_length=30)
    describe_emissions_stop = models.CharField(max_length=30)
    emission_color_start = models.CharField(max_length=30)
    emission_color_stop = models.CharField(max_length=30)
    plume_type = models.CharField(max_length=30, choices= plume_type_choices)
    water_drolet_present = models.CharField(max_length=30, choices= water_present_choices)
    water_droplet_plume = models.CharField(max_length=30, choices= droplet_plume_choices)
    plume_opacity_determined_start = models.CharField(max_length=50)
    plume_opacity_determined_stop = models.CharField(max_length=50)
    describe_background_start = models.CharField(max_length=30)
    describe_background_stop = models.CharField(max_length=30)
    notes = models.CharField(max_length=300)
    
    def __str__(self):
        return str(self.date)
    
#----------------------------------------------------------------------FORM A5 - DATA---------------<
class subA5_readings_model(models.Model):
    form = models.OneToOneField(
        subA5_model, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name='foobar',
    )
    o1 = models.CharField(max_length=2)
    o1_start = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True
    )
    o1_stop = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True
    )
    o1_highest_opacity = models.IntegerField(
    )
    o1_instant_over_20 = models.CharField(max_length=30, choices= instant_over_20_choices)
    o1_average_6 = models.FloatField(
    )
    o1_average_6_over_35 =models.CharField(max_length=30, choices= average_over_35_choices)
    o2 = models.CharField(max_length=2)
    o2_start = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True
    )
    o2_stop = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True
    )
    o2_highest_opacity = models.IntegerField(
    )
    o2_instant_over_20 = models.CharField(max_length=30, choices= instant_over_20_choices)
    o2_average_6 = models.FloatField(
    )
    o2_average_6_over_35 =models.CharField(max_length=30, choices= average_over_35_choices)
    o3 = models.CharField(max_length=2)
    o3_start = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True
    )
    o3_stop = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True
    )
    o3_highest_opacity = models.IntegerField(
    )
    o3_instant_over_20 = models.CharField(max_length=30, choices= instant_over_20_choices)
    o3_average_6 = models.FloatField(
    )
    o3_average_6_over_35 =models.CharField(max_length=30, choices= average_over_35_choices)
    o4 = models.CharField(max_length=2)
    o4_start = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True
    )
    o4_stop = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True
    )
    o4_highest_opacity = models.IntegerField(
    )
    o4_instant_over_20 = models.CharField(max_length=30, choices= instant_over_20_choices)
    o4_average_6 = models.FloatField(
    )
    o4_average_6_over_35 = models.CharField(max_length=30, choices= average_over_35_choices)
    o1_1_reads = models.CharField(max_length=3)
    o1_2_reads = models.CharField(max_length=3)
    o1_3_reads = models.CharField(max_length=3)
    o1_4_reads = models.CharField(max_length=3)
    o1_5_reads = models.CharField(max_length=3)
    o1_6_reads = models.CharField(max_length=3)
    o1_7_reads = models.CharField(max_length=3)
    o1_8_reads = models.CharField(max_length=3)
    o1_9_reads = models.CharField(max_length=3)
    o1_10_reads = models.CharField(max_length=3)
    o1_11_reads = models.CharField(max_length=3)
    o1_12_reads = models.CharField(max_length=3)
    o1_13_reads = models.CharField(max_length=3)
    o1_14_reads = models.CharField(max_length=3)
    o1_15_reads = models.CharField(max_length=3)
    o1_16_reads = models.CharField(max_length=3)
    o2_1_reads = models.CharField(max_length=3)
    o2_2_reads = models.CharField(max_length=3)
    o2_3_reads = models.CharField(max_length=3)
    o2_4_reads = models.CharField(max_length=3)
    o2_5_reads = models.CharField(max_length=3)
    o2_6_reads = models.CharField(max_length=3)
    o2_7_reads = models.CharField(max_length=3)
    o2_8_reads = models.CharField(max_length=3)
    o2_9_reads = models.CharField(max_length=3)
    o2_10_reads = models.CharField(max_length=3)
    o2_11_reads = models.CharField(max_length=3)
    o2_12_reads = models.CharField(max_length=3)
    o2_13_reads = models.CharField(max_length=3)
    o2_14_reads = models.CharField(max_length=3)
    o2_15_reads = models.CharField(max_length=3)
    o2_16_reads = models.CharField(max_length=3)
    o3_1_reads = models.CharField(max_length=3)
    o3_2_reads = models.CharField(max_length=3)
    o3_3_reads = models.CharField(max_length=3)
    o3_4_reads = models.CharField(max_length=3)
    o3_5_reads = models.CharField(max_length=3)
    o3_6_reads = models.CharField(max_length=3)
    o3_7_reads = models.CharField(max_length=3)
    o3_8_reads = models.CharField(max_length=3)
    o3_9_reads = models.CharField(max_length=3)
    o3_10_reads = models.CharField(max_length=3)
    o3_11_reads = models.CharField(max_length=3)
    o3_12_reads = models.CharField(max_length=3)
    o3_13_reads = models.CharField(max_length=3)
    o3_14_reads = models.CharField(max_length=3)
    o3_15_reads = models.CharField(max_length=3)
    o3_16_reads = models.CharField(max_length=3)
    o4_1_reads = models.CharField(max_length=3)
    o4_2_reads = models.CharField(max_length=3)
    o4_3_reads = models.CharField(max_length=3)
    o4_4_reads = models.CharField(max_length=3)
    o4_5_reads = models.CharField(max_length=3)
    o4_6_reads = models.CharField(max_length=3)
    o4_7_reads = models.CharField(max_length=3)
    o4_8_reads = models.CharField(max_length=3)
    o4_9_reads = models.CharField(max_length=3)
    o4_10_reads = models.CharField(max_length=3)
    o4_11_reads = models.CharField(max_length=3)
    o4_12_reads = models.CharField(max_length=3)
    o4_13_reads = models.CharField(max_length=3)
    o4_14_reads = models.CharField(max_length=3)
    o4_15_reads = models.CharField(max_length=3)
    o4_16_reads = models.CharField(max_length=3)
    
    def __str__(self):
        return str(self.form)
    
    
class pt_admin1_model(models.Model):
    form = models.OneToOneField(
        subA5_readings_model, 
        on_delete=models.CASCADE, 
        primary_key=True,
    )
    add_days = models.DateTimeField(default=datetime.datetime.now()+timedelta(days=90))
    days_left = models.DateTimeField(default=datetime.datetime.now()+timedelta(days=10))
    #date = models.CharField(max_length=30)
    #oven1 = models.CharField(max_length=30)
    #oven2 = models.CharField(max_length=30)
    #oven3 = models.CharField(max_length=30)
    #oven4 = models.CharField(max_length=30)
    
    
    def __str__(self):
        return self.date

    
class formB_model(models.Model):
    all_users = User.objects.all()
    all_user_choices = ((x.username, x.get_full_name()) for x in all_users)
    
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
        choices=all_user_choices_0,
        null = True
    )
    time_0 = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null = True
    )
    weather_0 = models.CharField(
        max_length=30,
        choices = weather_choices, 
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
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    supressant_applied_0 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    supressant_active_0 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    working_face_exceed_0 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    spills_0 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    pushed_back_0 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    coal_vessel_0 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    water_sprays_0 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    loader_lowered_0 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    working_water_sprays_0 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    barrier_thickness_0 = models.CharField(
        max_length=30,
        choices = barrier_choices, 
        blank=True,
        null=True
    )
    surface_quality_0 = models.CharField(
        max_length=30,
        choices = good_bad_choices, 
        blank=True,
        null=True
    )
    surpressant_crust_0 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
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
        blank = True,
        null=True
    )
    wharf_0 = models.CharField(
        max_length=30,
        choices = good_bad_choices, 
        blank=True,
        null=True
    )
    breeze_0 = models.CharField(
        max_length=30,
        choices = good_bad_choices, 
        blank=True,
        null=True
    )
    
    
    observer_1 = models.CharField(
        max_length=100, 
        blank=True,
        choices=all_user_choices_1,
        null = True
    )
    time_1 = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null=True
    )
    weather_1 = models.CharField(
        max_length=30,
        choices = weather_choices, 
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
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    supressant_applied_1 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    supressant_active_1 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    working_face_exceed_1 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    spills_1 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    pushed_back_1 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    coal_vessel_1 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    water_sprays_1 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    loader_lowered_1 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    working_water_sprays_1 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    barrier_thickness_1 = models.CharField(
        max_length=30,
        choices = barrier_choices, 
        blank=True,
        null=True
    )
    surface_quality_1 = models.CharField(
        max_length=30,
        choices = good_bad_choices, 
        blank=True,
        null=True
    )
    surpressant_crust_1 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
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
        blank = True,
        null=True
    )
    wharf_1 = models.CharField(
        max_length=30,
        choices = good_bad_choices, 
        blank=True,
        null=True
    )
    breeze_1 = models.CharField(
        max_length=30,
        choices = good_bad_choices, 
        blank=True,
        null=True
    )
    
    
    
    observer_2 = models.CharField(
        max_length=100, 
        blank=True,
        choices=all_user_choices_2,
        null = True
    )
    time_2 = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null=True
    )
    weather_2 = models.CharField(
        max_length=30,
        choices = weather_choices, 
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
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    supressant_applied_2 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    supressant_active_2 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    working_face_exceed_2 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    spills_2 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    pushed_back_2 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    coal_vessel_2 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    water_sprays_2 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    loader_lowered_2 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    working_water_sprays_2 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    barrier_thickness_2 = models.CharField(
        max_length=30,
        choices = barrier_choices, 
        blank=True,
        null=True
    )
    surface_quality_2 = models.CharField(
        max_length=30,
        choices = good_bad_choices, 
        blank=True,
        null=True
    )
    surpressant_crust_2 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
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
        blank = True,
        null=True
    )
    wharf_2 = models.CharField(
        max_length=30,
        choices = good_bad_choices, 
        blank=True,
        null=True
    )
    breeze_2 = models.CharField(
        max_length=30,
        choices = good_bad_choices, 
        blank=True,
        null=True
    )
    
    
    
    observer_3 = models.CharField(
        max_length=100, 
        blank=True,
        choices=all_user_choices_3,
        null = True
    )
    time_3 = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null=True
    )
    weather_3 = models.CharField(
        max_length=30,
        choices = weather_choices, 
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
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    supressant_applied_3 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    supressant_active_3 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    working_face_exceed_3 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    spills_3 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    pushed_back_3 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    coal_vessel_3 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    water_sprays_3 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    loader_lowered_3 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    working_water_sprays_3 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    barrier_thickness_3 = models.CharField(
        max_length=30,
        choices = barrier_choices, 
        blank=True,
        null=True
    )
    surface_quality_3 = models.CharField(
        max_length=30,
        choices = good_bad_choices, 
        blank=True,
        null=True
    )
    surpressant_crust_3 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
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
        blank = True,
        null=True
    )
    wharf_3 = models.CharField(
        max_length=30,
        choices = good_bad_choices, 
        blank=True,
        null=True
    )
    breeze_3 = models.CharField(
        max_length=30,
        choices = good_bad_choices, 
        blank=True,
        null=True
    )
    
    
    
    observer_4 = models.CharField(
        max_length=100, 
        blank=True,
        choices=all_user_choices_4,
        null = True
    )
    time_4 = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null=True
    )
    weather_4 = models.CharField(
        max_length=30,
        choices = weather_choices, 
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
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    supressant_applied_4 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    supressant_active_4 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    working_face_exceed_4 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    spills_4 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    pushed_back_4 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    coal_vessel_4 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
        blank=True,
        null=True
    )
    water_sprays_4 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    loader_lowered_4 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    working_water_sprays_4 = models.CharField(
        max_length=30,
        choices = yes_no_na_choices, 
        blank=True,
        null=True
    )
    barrier_thickness_4 = models.CharField(
        max_length=30,
        choices = barrier_choices, 
        blank=True,
        null=True
    )
    surface_quality_4 = models.CharField(
        max_length=30,
        choices = good_bad_choices, 
        blank=True,
        null=True
    )
    surpressant_crust_4 = models.CharField(
        max_length=30,
        choices = yes_no_choices, 
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
        blank = True,
        null=True
    )
    wharf_4 = models.CharField(
        max_length=30,
        choices = good_bad_choices, 
        blank=True,
        null=True
    )
    breeze_4 = models.CharField(
        max_length=30,
        choices = good_bad_choices, 
        blank=True,
        null=True
    )
    
    def __str__(self):
        return str(self.week_start)
    
    def whatever(self):
        return{
            'observer_0' : self.observer_0,
            'time_0' : self.time_0,
            'weather_0' : self.weather_0,
            'wind_speed_0' : self.wind_speed_0,
            'fugitive_dust_observed_0' : self.fugitive_dust_observed_0,
            'supressant_applied_0' : self.supressant_applied_0,
            'supressant_active_0' : self.supressant_active_0,
            'working_face_exceed_0' : self.working_face_exceed_0,
            'spills_0' : self.spills_0,
            'pushed_back_0' : self.pushed_back_0,
            'coal_vessel_0' : self.coal_vessel_0,
            'water_sprays_0' : self.water_sprays_0,
            'loader_lowered_0' : self.loader_lowered_0,
            'working_water_sprays_0' : self.working_water_sprays_0,
            'barrier_thickness_0' : self.barrier_thickness_0,
            'surface_quality_0' : self.surface_quality_0,
            'surpressant_crust_0' : self.surpressant_crust_0,
            'additional_surpressant_0' : self.additional_surpressant_0,
            'comments_0' : self.comments_0,
            'wharf_0' : self.wharf_0,
            'breeze_0' : self.breeze_0,
            
            'observer_1' : self.observer_1,
            'time_1' : self.time_1,
            'weather_1' : self.weather_1,
            'wind_speed_1' : self.wind_speed_1,
            'fugitive_dust_observed_1' : self.fugitive_dust_observed_1,
            'supressant_applied_1' : self.supressant_applied_1,
            'supressant_active_1' : self.supressant_active_1,
            'working_face_exceed_1' : self.working_face_exceed_1,
            'spills_1' : self.spills_1,
            'pushed_back_1' : self.pushed_back_1,
            'coal_vessel_1' : self.coal_vessel_1,
            'water_sprays_1' : self.water_sprays_1,
            'loader_lowered_1' : self.loader_lowered_1,
            'working_water_sprays_1' : self.working_water_sprays_1,
            'barrier_thickness_1' : self.barrier_thickness_1,
            'surface_quality_1' : self.surface_quality_1,
            'surpressant_crust_1' : self.surpressant_crust_1,
            'additional_surpressant_1' : self.additional_surpressant_1,
            'comments_1' : self.comments_1,
            'wharf_1' : self.wharf_1,
            'breeze_1' : self.breeze_1,
            
            'observer_2' : self.observer_2,
            'time_2' : self.time_2,
            'weather_2' : self.weather_2,
            'wind_speed_2' : self.wind_speed_2,
            'fugitive_dust_observed_2' : self.fugitive_dust_observed_2,
            'supressant_applied_2' : self.supressant_applied_2,
            'supressant_active_2' : self.supressant_active_2,
            'working_face_exceed_2' : self.working_face_exceed_2,
            'spills_2' : self.spills_2,
            'pushed_back_2' : self.pushed_back_2,
            'coal_vessel_2' : self.coal_vessel_2,
            'water_sprays_2' : self.water_sprays_2,
            'loader_lowered_2' : self.loader_lowered_2,
            'working_water_sprays_2' : self.working_water_sprays_2,
            'barrier_thickness_2' : self.barrier_thickness_2,
            'surface_quality_2' : self.surface_quality_2,
            'surpressant_crust_2' : self.surpressant_crust_2,
            'additional_surpressant_2' : self.additional_surpressant_2,
            'comments_2' : self.comments_2,
            'wharf_2' : self.wharf_2,
            'breeze_2' : self.breeze_2,
            
            'observer_3' : self.observer_3,
            'time_3' : self.time_3,
            'weather_3' : self.weather_3,
            'wind_speed_3' : self.wind_speed_3,
            'fugitive_dust_observed_3' : self.fugitive_dust_observed_3,
            'supressant_applied_3' : self.supressant_applied_3,
            'supressant_active_3' : self.supressant_active_3,
            'working_face_exceed_3' : self.working_face_exceed_3,
            'spills_3' : self.spills_3,
            'pushed_back_3' : self.pushed_back_3,
            'coal_vessel_3' : self.coal_vessel_3,
            'water_sprays_3' : self.water_sprays_3,
            'loader_lowered_3' : self.loader_lowered_3,
            'working_water_sprays_3' : self.working_water_sprays_3,
            'barrier_thickness_3' : self.barrier_thickness_3,
            'surface_quality_3' : self.surface_quality_3,
            'surpressant_crust_3' : self.surpressant_crust_3,
            'additional_surpressant_3' : self.additional_surpressant_3,
            'comments_3' : self.comments_3,
            'wharf_3' : self.wharf_3,
            'breeze_3' : self.breeze_3,
            
            'observer_4' : self.observer_4,
            'time_4' : self.time_4,
            'weather_4' : self.weather_4,
            'wind_speed_4' : self.wind_speed_4,
            'fugitive_dust_observed_4' : self.fugitive_dust_observed_4,
            'supressant_applied_4' : self.supressant_applied_4,
            'supressant_active_4' : self.supressant_active_4,
            'working_face_exceed_4' : self.working_face_exceed_4,
            'spills_4' : self.spills_4,
            'pushed_back_4' : self.pushed_back_4,
            'coal_vessel_4' : self.coal_vessel_4,
            'water_sprays_4' : self.water_sprays_4,
            'loader_lowered_4' : self.loader_lowered_4,
            'working_water_sprays_4' : self.working_water_sprays_4,
            'barrier_thickness_4' : self.barrier_thickness_4,
            'surface_quality_4' : self.surface_quality_4,
            'surpressant_crust_4' : self.surpressant_crust_4,
            'additional_surpressant_4' : self.additional_surpressant_4,
            'comments_4' : self.comments_4,
            'wharf_4' : self.wharf_4,
            'breeze_4' : self.breeze_4,
        }
    
class formD_model(models.Model):
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
        choices= truck_id_choices, 
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
        null = True,
    )
    contents1 = models.CharField(
        max_length=30, 
        choices= content_choices, 
        blank=True,
        null=True
    )
    freeboard1 = models.CharField(
        max_length=30, 
        choices= yes_no_choices, 
        blank=True,
        null=True
    )
    wetted1 = models.CharField(
        max_length=30, 
        choices= wetted_choices, 
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
        choices= truck_id_choices, 
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
        null = True,
    )
    contents2 = models.CharField(
        max_length=30, 
        choices= content_choices, 
        blank=True,
        null=True
    )
    freeboard2 = models.CharField(
        max_length=30, 
        choices= yes_no_choices, 
        blank=True,
        null=True
    )
    wetted2 = models.CharField(
        max_length=30, 
        choices= wetted_choices, 
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
        choices= truck_id_choices, 
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
        null = True,
    )
    contents3 = models.CharField(
        max_length=30, 
        choices= content_choices, 
        blank=True,
        null=True
    )
    freeboard3 = models.CharField(
        max_length=30, 
        choices= yes_no_choices, 
        blank=True,
        null=True
    )
    wetted3 = models.CharField(
        max_length=30, 
        choices= wetted_choices, 
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
        choices= truck_id_choices, 
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
        null = True,
    )
    contents4 = models.CharField(
        max_length=30, 
        choices= content_choices, 
        blank=True,
        null=True
    )
    freeboard4 = models.CharField(
        max_length=30, 
        choices= yes_no_choices, 
        blank=True,
        null=True
    )
    wetted4 = models.CharField(
        max_length=30, 
        choices= wetted_choices, 
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
        choices= truck_id_choices, 
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
        null = True,
    )
    contents5 = models.CharField(
        max_length=30, 
        choices= content_choices, 
        blank=True,
        null=True
    )
    freeboard5 = models.CharField(
        max_length=30, 
        choices= yes_no_choices, 
        blank=True,
        null=True
    )
    wetted5 = models.CharField(
        max_length=30, 
        choices= wetted_choices, 
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
            'truck_id1' : self.truck_id1, 
            'date1' : self.date1,
            'time1' : self.time1,
            'contents1' : self.contents1,
            'freeboard1' : self.freeboard1,
            'wetted1' : self.wetted1,
            'comments1' : self.comments1,
            'truck_id2' : self.truck_id2,
            'date2' : self.date2,
            'time2' : self.time2,
            'contents2' : self.contents2,
            'freeboard2' : self.freeboard2,
            'wetted2' : self.wetted2,
            'comments2' : self.comments2,
            'truck_id3' : self.truck_id3,
            'date3' : self.date3,
            'time3' : self.time3,
            'contents3' : self.contents3,
            'freeboard3' : self.freeboard3,
            'wetted3' : self.wetted3,
            'comments3' : self.comments3,
            'truck_id4' : self.truck_id4,
            'date4' : self.date4,
            'time4' : self.time4,
            'contents4' : self.contents4,
            'freeboard4' : self.freeboard4,
            'wetted4' : self.wetted4,
            'comments4' : self.comments4,
            'truck_id5' : self.truck_id5,
            'date5' : self.date5,
            'time5' : self.time5,
            'contents5' : self.contents5,
            'freeboard5' : self.freeboard5,
            'wetted5' : self.wetted5,
            'comments5' : self.comments5,
        }
#----------------------------------------------------------------------FORM E---------------<
    
class formE_model(models.Model):
    observer = models.CharField(
        max_length=30,
    )
    date = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True
    )
    crew = models.CharField(
        max_length=1, 
        choices = crew_choices
    )
    foreman = models.CharField(
        max_length=30,
        choices = foreman_choices
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
        choices = yes_no_choices
    )
    oven1 = models.CharField(max_length=2)
    time1 = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True
    )
    source1 = models.CharField(
        max_length=30,
        choices = source_choices
    )
    comments1 = models.CharField(max_length=30)
    
    def __str__(self):
        return str(self.date)
    
#----------------------------------------------------------------------FORM G1---------------<

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
        choices = ok_not_ok_choices
    )
    status_2 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_3 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_4 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_5 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_6 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_7 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
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
        blank = True,
        null = True
    )
    containers_3 = models.IntegerField(
        blank = True,
        null = True
    )
    containers_4 = models.IntegerField(
        blank = True,
        null = True
    )
    waste_codes_1 = models.CharField(
        max_length=30,
        choices = waste_code_choices
    )
    waste_codes_2 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
    )
    waste_codes_3 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
    )
    waste_codes_4 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
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
        null = True
    )
    dates_3 = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
        null = True
    )
    dates_4 = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
        null = True
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
        choices = ok_not_ok_choices
    )
    status_2 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_3 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_4 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_5 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_6 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
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
        blank = True,
        null = True
    )
    containers_3 = models.IntegerField(
        blank = True,
        null = True
    )
    containers_4 = models.IntegerField(
        blank = True,
        null = True
    )
    waste_codes_1 = models.CharField(
        max_length=30,
        choices = waste_code_choices
    )
    waste_codes_2 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
    )
    waste_codes_3 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
    )
    waste_codes_4 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
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
        null = True
    )
    dates_3 = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
        null = True
    )
    dates_4 = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
        null = True
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
        choices = ok_not_ok_choices
    )
    status_2 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_3 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_4 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_5 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_6 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
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
        blank = True,
        null = True
    )
    containers_3 = models.IntegerField(
        blank = True,
        null = True
    )
    containers_4 = models.IntegerField(
        blank = True,
        null = True
    )
    waste_codes_1 = models.CharField(
        max_length=30,
        choices = waste_code_choices
    )
    waste_codes_2 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
    )
    waste_codes_3 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
    )
    waste_codes_4 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
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
        null = True
    )
    dates_3 = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
        null = True
    )
    dates_4 = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
        null = True
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
        choices = ok_not_ok_choices
    )
    status_2 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_3 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_4 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_5 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_6 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
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
        blank = True,
        null = True
    )
    containers_3 = models.IntegerField(
        blank = True,
        null = True
    )
    containers_4 = models.IntegerField(
        blank = True,
        null = True
    )
    waste_codes_1 = models.CharField(
        max_length=30,
        choices = waste_code_choices
    )
    waste_codes_2 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
    )
    waste_codes_3 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
    )
    waste_codes_4 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
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
        null = True
    )
    dates_3 = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
        null = True
    )
    dates_4 = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
        null = True
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
        choices = ok_not_ok_choices
    )
    status_2 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_3 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_4 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_5 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_6 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
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
        blank = True,
        null = True
    )
    containers_3 = models.IntegerField(
        blank = True,
        null = True
    )
    containers_4 = models.IntegerField(
        blank = True,
        null = True
    )
    waste_codes_1 = models.CharField(
        max_length=30,
        choices = waste_code_choices
    )
    waste_codes_2 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
    )
    waste_codes_3 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
    )
    waste_codes_4 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
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
        null = True
    )
    dates_3 = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
        null = True
    )
    dates_4 = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
        null = True
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
        choices = ok_not_ok_choices
    )
    status_2 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_3 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_4 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_5 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_6 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
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
        blank = True,
        null = True
    )
    containers_3 = models.IntegerField(
        blank = True,
        null = True
    )
    containers_4 = models.IntegerField(
        blank = True,
        null = True
    )
    waste_codes_1 = models.CharField(
        max_length=30,
        choices = waste_code_choices
    )
    waste_codes_2 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
    )
    waste_codes_3 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
    )
    waste_codes_4 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
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
        null = True
    )
    dates_3 = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
        null = True
    )
    dates_4 = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
        null = True
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
        choices = ok_not_ok_choices
    )
    status_2 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_3 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_4 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_5 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
    )
    status_6 = models.CharField(
        max_length=30,
        choices = ok_not_ok_choices
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
        blank = True,
        null = True
    )
    containers_3 = models.IntegerField(
        blank = True,
        null = True
    )
    containers_4 = models.IntegerField(
        blank = True,
        null = True
    )
    waste_codes_1 = models.CharField(
        max_length=30,
        choices = waste_code_choices
    )
    waste_codes_2 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
    )
    waste_codes_3 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
    )
    waste_codes_4 = models.CharField(
        max_length=30,
        choices = waste_code_choices,
        blank = True,
        null = True
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
        null = True
    )
    dates_3 = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
        null = True
    )
    dates_4 = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
        null = True
    )
    
    def __str__(self):
        return str(self.date)
class formG1_model(models.Model):
    date = models.CharField(max_length=30)
    estab = models.CharField(max_length=30)
    county = models.CharField(max_length=30)
    estab_no = models.CharField(max_length=30)
    equip_loc = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    observer = models.CharField(max_length=30)
    cert_date = models.CharField(max_length=30)
    process_equip1 = models.CharField(max_length=50)
    process_equip2 = models.CharField(max_length=50)
    op_mode1 = models.CharField(max_length=30)
    op_mode2 = models.CharField(max_length=30)
    background_color_start = models.CharField(max_length=30)
    background_color_stop = models.CharField(max_length=30)
    sky_conditions = models.CharField(max_length=30)
    wind_speed_start = models.CharField(max_length=2)
    wind_speed_stop = models.CharField(max_length=4)
    wind_direction =models.CharField(max_length=3)
    emission_point_start = models.CharField(max_length=50)
    emission_point_stop = models.CharField(max_length=50)
    ambient_temp_start = models.CharField(max_length=3)
    ambient_temp_stop = models.CharField(max_length=4)
    humidity = models.CharField(max_length=3)
    height_above_ground = models.CharField(max_length=30)
    height_rel_observer = models.CharField(max_length=30)
    distance_from = models.CharField(max_length=30)
    direction_from = models.CharField(max_length=30)
    describe_emissions_start = models.CharField(max_length=30)
    describe_emissions_stop = models.CharField(max_length=30)
    emission_color_start = models.CharField(max_length=30)
    emission_color_stop = models.CharField(max_length=30)
    plume_type = models.CharField(max_length=30, choices= plume_type_choices)
    water_drolet_present = models.CharField(max_length=30, choices= water_present_choices)
    water_droplet_plume = models.CharField(max_length=30, choices= droplet_plume_choices)
    plume_opacity_determined_start = models.CharField(max_length=50)
    plume_opacity_determined_stop = models.CharField(max_length=50)
    describe_background_start = models.CharField(max_length=30)
    describe_background_stop = models.CharField(max_length=30)   
    
    def __str__(self):
        return str(self.date)
    
#----------------------------------------------------------------------FORM H---------------<
class formH_model(models.Model):
    date = models.CharField(max_length=30)
    estab = models.CharField(max_length=30)
    county = models.CharField(max_length=30)
    estab_no = models.CharField(max_length=30)
    equip_loc = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    observer = models.CharField(max_length=30)
    cert_date = models.CharField(max_length=30)
    process_equip1 = models.CharField(max_length=50)
    process_equip2 = models.CharField(max_length=50)
    op_mode1 = models.CharField(max_length=30)
    op_mode2 = models.CharField(max_length=30)
    background_color_start = models.CharField(max_length=30)
    background_color_stop = models.CharField(max_length=30)
    sky_conditions = models.CharField(max_length=30)
    wind_speed_start = models.CharField(max_length=2)
    wind_speed_stop = models.CharField(max_length=4)
    wind_direction =models.CharField(max_length=3)
    emission_point_start = models.CharField(max_length=50)
    emission_point_stop = models.CharField(max_length=50)
    ambient_temp_start = models.CharField(max_length=3)
    ambient_temp_stop = models.CharField(max_length=4)
    humidity = models.CharField(max_length=3)
    height_above_ground = models.CharField(max_length=30)
    height_rel_observer = models.CharField(max_length=30)
    distance_from = models.CharField(max_length=30)
    direction_from = models.CharField(max_length=30)
    describe_emissions_start = models.CharField(max_length=30)
    describe_emissions_stop = models.CharField(max_length=30)
    emission_color_start = models.CharField(max_length=30)
    emission_color_stop = models.CharField(max_length=30)
    plume_type = models.CharField(max_length=30, choices= plume_type_choices)
    water_drolet_present = models.CharField(max_length=30, choices= water_present_choices)
    water_droplet_plume = models.CharField(max_length=30, choices= droplet_plume_choices)
    plume_opacity_determined_start = models.CharField(max_length=50)
    plume_opacity_determined_stop = models.CharField(max_length=50)
    describe_background_start = models.CharField(max_length=30)
    describe_background_stop = models.CharField(max_length=30)   
    
    def __str__(self):
        return str(self.date)
    
#----------------------------------------------------------------------FORM I---------------<
class formI_model(models.Model):
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
    time_0 = models.CharField(max_length=30)
    time_1 = models.CharField(max_length=30)
    time_2 = models.CharField(max_length=30)
    time_3 = models.CharField(max_length=30)
    time_4 = models.CharField(max_length=30)
    obser_0 = models.CharField(max_length=30)
    obser_1 = models.CharField(max_length=30)
    obser_2 = models.CharField(max_length=30)
    obser_3 = models.CharField(max_length=30)
    obser_4 = models.CharField(max_length=30)
    
    def __str__(self):
        return str(self.week_start)
    
#----------------------------------------------------------------------FORM L---------------<
class formL_model(models.Model):
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
        choices = yes_no_choices,
        blank=True,
        null=True
    )
    vents_1 = models.CharField(
        max_length=30,
        choices = yes_no_choices,
        blank=True,
        null=True
    )
    vents_2 = models.CharField(
        max_length=30,
        choices = yes_no_choices,
        blank=True,
        null=True
    )
    vents_3 = models.CharField(
        max_length=30,
        choices = yes_no_choices,
        blank=True,
        null=True
    )
    vents_4 = models.CharField(
        max_length=30,
        choices = yes_no_choices,
        blank=True,
        null=True
    )
    vents_5 = models.CharField(
        max_length=30,
        choices = yes_no_choices,
        blank=True,
        null=True
    )
    vents_6 = models.CharField(
        max_length=30,
        choices = yes_no_choices,
        blank=True,
        null=True
    )
    mixer_0 = models.CharField(
        max_length=30,
        choices = yes_no_choices,
        blank=True,
        null=True
    )
    mixer_1 = models.CharField(
        max_length=30,
        choices = yes_no_choices,
        blank=True,
        null=True
    )
    mixer_2 = models.CharField(
        max_length=30,
        choices = yes_no_choices,
        blank=True,
        null=True
    )
    mixer_3 = models.CharField(
        max_length=30,
        choices = yes_no_choices,
        blank=True,
        null=True
    )
    mixer_4 = models.CharField(
        max_length=30,
        choices = yes_no_choices,
        blank=True,
        null=True
    )
    mixer_5 = models.CharField(
        max_length=30,
        choices = yes_no_choices,
        blank=True,
        null=True
    )
    mixer_6 = models.CharField(
        max_length=30,
        choices = yes_no_choices,
        blank=True,
        null=True
    )
    v_comments_0 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    v_comments_1 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    v_comments_2 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    v_comments_3 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    v_comments_4 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    v_comments_5 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    v_comments_6 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    m_comments_0 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    m_comments_1 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    m_comments_2 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    m_comments_3 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    m_comments_4 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    m_comments_5 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    m_comments_6 = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    
    def __str__(self):
        return str(self.week_start)
    
 #-----------------------------------------------------------------FORM M---------------<
class formM_model(models.Model):
    date = models.CharField(max_length=30)
    paved = models.CharField(
        max_length=30,
        choices = paved_roads
    )
    pav_start = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null=True
    )
    pav_stop = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null=True
    )
    unpaved = models.CharField(
        max_length=30,
        choices = unpaved_roads
    )
    unp_start = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null=True
    )
    unp_stop = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null=True
    )
    parking = models.CharField(
        max_length=30,
        choices = parking_lots
    )
    par_start = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null=True
    )
    par_stop = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null=True
    )
    storage = models.CharField(
        max_length=30,
        choices = storage_piles
    )
    sto_start = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null=True
    )
    sto_stop = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null=True
    )
    observer = models.CharField(max_length=30)
    cert_date = models.CharField(max_length=30)
    
    def __str__(self):
        return str(self.date)
    
class issues_model(models.Model):
    form = models.CharField(max_length=30)
    issues = models.CharField(max_length=300)
    notified = models.CharField(max_length=30)
    time = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True
    )
    date = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
    )
    cor_action = models.CharField(max_length=150)
    
    def __str__(self):
        return str(self.date)
    
class Event(models.Model):
    observer = models.CharField(max_length=30)
    day = models.DateField(u'Day of the event', help_text=u'Day of the event')
    start_time = models.TimeField(u'Starting time', help_text=u'Starting time')
    end_time = models.TimeField(u'Final time', help_text=u'Final time')
    notes = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)
    
    class Meta:
        verbose_name = u'Scheduling'
        verbose_name_plural = u'Scheduling'
 
    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:    #edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end): #innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end: #outter limits
            overlap = True
 
        return overlap
 
    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, str(self.start_time))
 
    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('Ending times must after starting times')
 
        events = Event.objects.filter(day=self.day)
        if events.exists():
            for event in events:
                if self.check_overlap(event.start_time, event.end_time, self.start_time, self.end_time):
                    raise ValidationError(
                        'There is an overlap with another event: ' + str(event.day) + ', ' + str(
                            event.start_time) + '-' + str(event.end_time))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    