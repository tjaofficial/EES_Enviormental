from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
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
# Create your models here.


class Forms(models.Model):
    form = models.CharField(max_length=30)
    link = models.CharField(max_length=30)
    date_submitted = models.DateField(auto_now_add=False, auto_now=False)
    submitted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.form
    
class subC(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True, auto_now=False)
    truck_sel = models.CharField(max_length=30, choices=truck_choices)
    area_sel = models.CharField(max_length=30, choices=area_choices)
    truck_start_time = models.TimeField(max_length=30)
    truck_stop_time = models.TimeField(max_length=30)
    area_start_time = models.TimeField(max_length=30)
    area_stop_time = models.TimeField(max_length=30)
    observer = models.CharField(max_length=30)
    cert_date = models.CharField(max_length=30)
    comments = models.CharField(max_length=30)
    issues = models.CharField(max_length=30)
    cor_action = models.CharField(max_length=30)
    notified = models.CharField(max_length=30)
    time_date = models.CharField(max_length=30)
    
    def __str__(self):
        return str(self.date)
    
    
class FormCReadings(models.Model):
    form = models.OneToOneField(
        subC,
        on_delete=models.CASCADE,
        primary_key=True,
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
        return self.foreman

    
    
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
 

class subA5_model(models.Model):
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
        return self.date
    
#----------------------------------------------------------------------FORM A5 - DATA---------------<
class subA5_readings_model(models.Model):
    form = models.OneToOneField(
        subA5_model, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name='foobar',
    )
    o1 = models.CharField(max_length=2)
    o1_start = models.CharField(max_length=30)
    o1_stop = models.CharField(max_length=30)
    o1_highest_opacity = models.CharField(max_length=30)
    o1_instant_over_20 = models.CharField(max_length=30, choices= instant_over_20_choices)
    o1_average_6 = models.CharField(max_length=30)
    o1_average_6_over_35 =models.CharField(max_length=30, choices= average_over_35_choices)
    o2 = models.CharField(max_length=2)
    o2_start = models.CharField(max_length=30)
    o2_stop = models.CharField(max_length=30)
    o2_highest_opacity = models.CharField(max_length=30)
    o2_instant_over_20 = models.CharField(max_length=30, choices= instant_over_20_choices)
    o2_average_6 = models.CharField(max_length=30)
    o2_average_6_over_35 =models.CharField(max_length=30, choices= average_over_35_choices)
    o3 = models.CharField(max_length=2)
    o3_start = models.CharField(max_length=30)
    o3_stop = models.CharField(max_length=30)
    o3_highest_opacity = models.CharField(max_length=30)
    o3_instant_over_20 = models.CharField(max_length=30, choices= instant_over_20_choices)
    o3_average_6 = models.CharField(max_length=30)
    o3_average_6_over_35 =models.CharField(max_length=30, choices= average_over_35_choices)
    o4 = models.CharField(max_length=2)
    o4_start = models.CharField(max_length=30)
    o4_stop = models.CharField(max_length=30)
    o4_highest_opacity = models.CharField(max_length=30)
    o4_instant_over_20 = models.CharField(max_length=30, choices= instant_over_20_choices)
    o4_average_6 = models.CharField(max_length=30)
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

    
class user_profile_model(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    
    cert_date = models.DateField(auto_now_add=False, auto_now=False, blank= True)
    
    def __str__(self):
        return self.user.username
    
    
class subA1_model(models.Model):
    observer = models.CharField(max_length=30)
    date = models.CharField(max_length=30)
    crew = models.CharField(max_length=30)
    foreman = models.CharField(max_length=30)
    start = models.CharField(max_length=30)
    stop = models.CharField(max_length=30)
    
    def __str__(self):
        return str(self.date)
    
    
class subA1_readings_model(models.Model):
    form = models.OneToOneField(
        subA1_model, 
        on_delete=models.CASCADE, 
        primary_key=True,
    )
    c1_no = models.CharField(max_length=30)
    c2_no = models.CharField(max_length=30)
    c3_no = models.CharField(max_length=30)
    c4_no = models.CharField(max_length=30)
    c5_no = models.CharField(max_length=30)
    c1_start = models.CharField(max_length=30)
    c2_start = models.CharField(max_length=30)
    c3_start = models.CharField(max_length=30)
    c4_start = models.CharField(max_length=30)
    c5_start = models.CharField(max_length=30)
    c1_stop = models.CharField(max_length=30)
    c2_stop = models.CharField(max_length=30)
    c3_stop = models.CharField(max_length=30)
    c4_stop = models.CharField(max_length=30)
    c5_stop = models.CharField(max_length=30)
    c1_sec = models.CharField(max_length=30)
    c2_sec = models.CharField(max_length=30)
    c3_sec = models.CharField(max_length=30)
    c4_sec = models.CharField(max_length=30)
    c5_sec = models.CharField(max_length=30)
    c1_comments = models.CharField(max_length=30)
    c2_comments = models.CharField(max_length=30)
    c3_comments = models.CharField(max_length=30)
    c4_comments = models.CharField(max_length=30)
    c5_comments = models.CharField(max_length=30)
    larry_car = models.CharField(max_length=30)
    comments = models.CharField(max_length=30)
    
    def __str__(self):
        return str(self.form)
 #----------------------------------------------------------------------FORM D---------------<   
    
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
    time1 = models.CharField(
        max_length=30, 
        blank=True,
        null=True
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
    time2 = models.CharField(
        max_length=30, 
        blank=True,
        null=True
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
    time3 = models.CharField(
        max_length=30, 
        blank=True,
        null=True
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
    time4 = models.CharField(
        max_length=30, 
        blank=True,
        null=True
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
    time5 = models.CharField(
        max_length=30, 
        blank=True,
        null=True
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
        max_length=30
    )
    date = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True
    )
    crew = models.CharField(
        max_length=30, 
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    