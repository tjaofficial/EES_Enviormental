from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import datetime
from django.core.exceptions import ValidationError
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


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
    ('p1', '#4 Booster Station'),
    ('p2', '#5 Battery Road'),
    ('p3', 'Coal Dump Horseshoe'),
    ('p4', 'Coal Handling Road (Partial)'),
    ('p5', 'Coke Plant Road'),
    ('p6', 'Coke Plant Mech Road'),
    ('p7', 'North Gate Area'),
    ('p8', 'Compund Road'),
    ('p9', 'D-4 Blast Furnace Road'),
    ('p10', 'Gap Gate Road'),
    ('p11', '#3 Ore Dock Road'),
    ('p12', 'River Road'),
    ('p13', 'Weigh Station Road'),
    ('p14', 'Zug Island Road')
)
unpaved_roads = (
    ('unp1', 'North Gate Truck Turn'),
    ('unp2', 'Screening Station Road'),
    ('unp3', 'Coal Handling Road (Partial)'),
    ('unp4', 'Taj Mahal Road'),
    ('unp5', 'PECS Approach'),
    ('unp6', 'No. 2 Boilerhouse Road')
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
    ('Quaterly', 'Quaterly '),
    ('Semi-Annual', 'Semi-Annual'),
    ('Annual', 'Annual')
)
days_choices = (
    ('Any', 'Any'),
    ('0', 'Mondays'),
    ('1', 'Tuesdays'),
    ('2', 'Wednesdays'),
    ('3', 'Thursdays'),
    ('4', 'Fridays'),
    ('5', 'Saturdays'),
    ('6', 'Sundays'),
)
weekend_choices = (
    ('5', 'Saturday'),
    ('6', 'Sunday'),
)
# all_users = User.objects.all()
# all_user_choices_x = ((x.username, x.get_full_name()) for x in all_users)

# Create your models here.


class Forms(models.Model):
    form = models.CharField(max_length=30)
    frequency = models.CharField(max_length=30, choices=frequent_choices)
    day_freq = models.CharField(max_length=30, choices=days_choices, null= True)
    weekdays_only = models.BooleanField(default=False)
    weekend_only = models.BooleanField(default=False)
    link = models.CharField(max_length=30)
    header = models.CharField(max_length=80)
    title = models.CharField(max_length=80)
    due_date = models.DateField(auto_now_add=False, auto_now=False, blank=True)
    date_submitted = models.DateField(auto_now_add=False, auto_now=False, blank=True)
    submitted = models.BooleanField(default=False)

    def __str__(self):
        return self.form


class formC_model(models.Model):
    # all_users = User.objects.all()
    # all_user_choices = ((x.get_full_name(), x.get_full_name()) for x in all_users)

    date = models.DateField(auto_now_add=False, auto_now=False)
    truck_sel = models.CharField(max_length=30, choices=truck_choices)
    area_sel = models.CharField(max_length=30, choices=area_choices)
    truck_start_time = models.TimeField()
    truck_stop_time = models.TimeField()
    area_start_time = models.TimeField()
    area_stop_time = models.TimeField()
    observer = models.CharField(
        max_length=30
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

    def clean_t(self):
        if self.truck_start_time > self.truck_stop_time:
            raise ValidationError('Start should be before end')
        return super().clean()

    def clean_a(self):
        if self.area_start_time > self.area_stop_time:
            raise ValidationError('Start should be before end')
        return super().clean()

    def __str__(self):
        return str(self.date)


class formC_readings_model(models.Model):
    form = models.OneToOneField(
        formC_model,
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
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT
    )

    cert_date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True
    )
    profile_picture = models.ImageField(
        blank=True,
        null=True,
        upload_to='images/profile_pics')
    phone = PhoneNumberField(
        null=False,
        blank=False,
    )
    position = models.CharField(
        max_length=30,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.user.username


class formA1_model(models.Model):

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
        choices=foreman_choices
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


class formA1_readings_model(models.Model):
    form = models.OneToOneField(
        formA1_model,
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
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    c2_start = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    c3_start = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    c4_start = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    c5_start = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    c1_stop = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    c2_stop = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    c3_stop = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    c4_stop = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
    )
    c5_stop = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
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
        choices=larry_car_choices
    )
    comments = models.CharField(
        max_length=300
    )
    total_seconds = models.FloatField(
        max_length=30
    )

    def __str__(self):
        return str(self.form)
# -------------------------------FORM D---------------<


class formA2_model(models.Model):
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
    crew = models.CharField(
        max_length=1,
        choices=crew_choices
    )
    foreman = models.CharField(
        max_length=30,
        choices=foreman_choices
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


class formA3_model(models.Model):

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
    crew = models.CharField(
        max_length=1,
        choices=crew_choices
    )
    foreman = models.CharField(
        max_length=30,
        choices=foreman_choices
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
        null=True
    )
    om_loc1 = models.CharField(
        max_length=30,
        choices=om_location,
        blank=True,
        null=True
    )
    l_oven1 = models.CharField(
        max_length=2,
        blank=True,
        null=True
    )
    l_loc1 = models.CharField(
        max_length=30,
        choices=l_location,
        blank=True,
        null=True
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
        choices=foreman_choices
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
        blank=True,
        null=True,
    )
    time_leak_1 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    date_temp_seal_leak_1 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    time_temp_seal_leak_1 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    temp_seal_by_leak_1 = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )
    date_init_repair_leak_1 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    time_init_repair_leak_1 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    date_comp_repair_leak_1 = models.DateField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    time_comp_repair_leak_1 = models.TimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    comp_by_leak_1 = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )
    notes = models.CharField(max_length=30)

    def __str__(self):
        return str(self.date)


class formA5_model(models.Model):
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
    process_equip1 = models.CharField(max_length=50)
    process_equip2 = models.CharField(max_length=50)
    op_mode1 = models.CharField(max_length=30)
    op_mode2 = models.CharField(max_length=30)
    background_color_start = models.CharField(max_length=30)
    background_color_stop = models.CharField(max_length=30)
    sky_conditions = models.CharField(max_length=30)
    wind_speed_start = models.CharField(max_length=4)
    wind_speed_stop = models.CharField(max_length=4)
    wind_direction = models.CharField(max_length=3)
    emission_point_start = models.CharField(max_length=50)
    emission_point_stop = models.CharField(max_length=50)
    ambient_temp_start = models.CharField(max_length=5)
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
    plume_type = models.CharField(max_length=30, choices=plume_type_choices)
    water_drolet_present = models.CharField(max_length=30, choices=water_present_choices)
    water_droplet_plume = models.CharField(max_length=30, choices=droplet_plume_choices)
    plume_opacity_determined_start = models.CharField(max_length=50)
    plume_opacity_determined_stop = models.CharField(max_length=50)
    describe_background_start = models.CharField(max_length=30)
    describe_background_stop = models.CharField(max_length=30)
    notes = models.CharField(max_length=300)

    def __str__(self):
        return str(self.date)

# -----------------------FORM A5 - DATA---------------<


class formA5_readings_model(models.Model):
    form = models.OneToOneField(
        formA5_model,
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
    o1_instant_over_20 = models.CharField(max_length=30, choices=instant_over_20_choices)
    o1_average_6 = models.FloatField(
    )
    o1_average_6_over_35 = models.CharField(max_length=30, choices=average_over_35_choices)
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
    o2_instant_over_20 = models.CharField(max_length=30, choices=instant_over_20_choices)
    o2_average_6 = models.FloatField(
    )
    o2_average_6_over_35 = models.CharField(max_length=30, choices=average_over_35_choices)
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
    o3_instant_over_20 = models.CharField(max_length=30, choices=instant_over_20_choices)
    o3_average_6 = models.FloatField(
    )
    o3_average_6_over_35 = models.CharField(max_length=30, choices=average_over_35_choices)
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
    o4_instant_over_20 = models.CharField(max_length=30, choices=instant_over_20_choices)
    o4_average_6 = models.FloatField(
    )
    o4_average_6_over_35 = models.CharField(max_length=30, choices=average_over_35_choices)
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
        formA5_readings_model,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    add_days = models.DateTimeField(default=datetime.datetime.now()+timedelta(days=90))
    days_left = models.DateTimeField(default=datetime.datetime.now()+timedelta(days=10))
    # date = models.CharField(max_length=30)
    # oven1 = models.CharField(max_length=30)
    # oven2 = models.CharField(max_length=30)
    # oven3 = models.CharField(max_length=30)
    # oven4 = models.CharField(max_length=30)

    def __str__(self):
        return self.date


class formB_model(models.Model):

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
        max_length=30
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
        choices=waste_code_choices,
        blank=True,
        null=True
    )
    waste_codes_4 = models.CharField(
        max_length=30,
        choices=waste_code_choices,
        blank=True,
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
        null=True
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
        blank =True,
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
class formG2_model(models.Model):
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
    time_0 = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null = True
    )
    time_1 = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null = True
    )
    time_2 = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null = True
    )
    time_3 = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null = True
    )
    time_4 = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
        blank=True,
        null = True
    )
    obser_0 = models.CharField(
        max_length=30,
        blank=True,
        null = True
    )
    obser_1 = models.CharField(
        max_length=30,
        blank=True,
        null = True
    )
    obser_2 = models.CharField(
        max_length=30,
        blank=True,
        null = True
    )
    obser_3 = models.CharField(
        max_length=30,
        blank=True,
        null = True
    )
    obser_4 = models.CharField(
        max_length=30,
        blank=True,
        null = True
    )
    
    def __str__(self):
        return str(self.week_start)
    
#----------------------------------------------------------------------FORM L---------------<
class formL_model(models.Model):
    
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
    
    date = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
    )
    paved = models.CharField(
        max_length=30,
        choices = paved_roads
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
        choices = unpaved_roads
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
        choices = parking_lots
    )
    par_start = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
    )
    par_stop = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
    )
    storage = models.CharField(
        max_length=30,
        choices = storage_piles
    )
    sto_start = models.TimeField(
        auto_now_add=False, 
        auto_now=False,
    )
    sto_stop = models.TimeField(
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
    
class formM_readings_model(models.Model):
    form = models.OneToOneField(
        formM_model, 
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
    
    storage_1 = models.CharField(
        max_length=30,
    )
    storage_2 = models.CharField(
        max_length=30,
    )
    storage_3 = models.CharField(
        max_length=30,
    )
    storage_4 = models.CharField(
        max_length=30,
    )
    storage_5 = models.CharField(
        max_length=30,
    )
    storage_6 = models.CharField(
        max_length=30,
    )
    storage_7 = models.CharField(
        max_length=30,
    )
    storage_8 = models.CharField(
        max_length=30,
    )
    storage_9 = models.CharField(
        max_length=30,
    )
    storage_10 = models.CharField(
        max_length=30,
    )
    storage_11 = models.CharField(
        max_length=30,
    )
    storage_12 = models.CharField(
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
    storage_total = models.CharField(
        max_length=30,
    )
    
    def __str__(self):
        return str(self.form)
    
class formO_model(models.Model):
    
    observer = models.CharField(
        max_length=30
    )
    month = models.CharField(
        max_length=30
    )
    date = models.DateField(
        auto_now_add=False, 
        auto_now=False
    )
    weekend_day = models.CharField(
        max_length=30,
        choices = weekend_choices
    )
    Q_1 = models.CharField(
        max_length=30, 
        choices= yes_no_choices, 
    )
    Q_2 = models.CharField(
        max_length=30, 
        choices= yes_no_choices, 
    )
    Q_3 = models.CharField(
        max_length=30, 
        choices= yes_no_choices,
    )
    Q_4 = models.CharField(
        max_length=30, 
        choices= yes_no_choices,
    )
    Q_5 = models.CharField(
        max_length=30, 
        choices= yes_no_choices,
    )
    Q_6 = models.CharField(
        max_length=30, 
        choices= yes_no_choices,
    )
    Q_7 = models.CharField(
        max_length=30, 
        choices= yes_no_choices,
    )
    Q_8 = models.CharField(
        max_length=30, 
        choices= yes_no_choices,
    )
    Q_9 = models.CharField(
        max_length=30, 
        choices= yes_no_choices,
    )
    comments = models.CharField(
        max_length=300
    )
    actions_taken = models.CharField(
        max_length=150
    )
    
    def __str__(self):
        return str(self.date)
    
class formP_model(models.Model):
    
    observer = models.CharField(
        max_length=30
    )
    month = models.CharField(
        max_length=30
    )
    date = models.DateField(
        auto_now_add=False, 
        auto_now=False
    )
    weekend_day = models.CharField(
        max_length=30,
        choices = weekend_choices
    )
    Q_1 = models.CharField(
        max_length=30, 
        choices= yes_no_choices, 
    )
    Q_2 = models.CharField(
        max_length=30, 
        choices= yes_no_choices, 
    )
    Q_3 = models.CharField(
        max_length=30, 
        choices= yes_no_choices,
    )
    Q_4 = models.CharField(
        max_length=30, 
        choices= yes_no_choices,
    )
    Q_5 = models.CharField(
        max_length=30, 
        choices= yes_no_choices,
    )
    Q_6 = models.CharField(
        max_length=30, 
        choices= yes_no_choices,
    )
    Q_7 = models.CharField(
        max_length=30, 
        choices= yes_no_choices,
    )
    Q_8 = models.CharField(
        max_length=30, 
        choices= yes_no_choices,
    )
    Q_9 = models.CharField(
        max_length=30, 
        choices= yes_no_choices,
    )
    comments = models.CharField(
        max_length=300
    )
    actions_taken = models.CharField(
        max_length=150
    )
    
    def __str__(self):
        return str(self.date)
    
class issues_model(models.Model):
    form = models.CharField(max_length=30)
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
    
    def __str__(self):
        return str(self.date)
    
class Event(models.Model):
    
    cal_title_choices = (
        ('P', 'Primary'),
        ('BU', 'Back Up'),
        ('Off', 'Off'),
        ('Office', 'Office '),
        ('BH', 'BagHouses'),
        ('QT', 'Quarterly Trucks'),
        ('BH2-S', 'Boilerhouse Stacks'),
    )
    
    observer = models.CharField(
        max_length=30
    )
    title = models.CharField(
        max_length=30,
        choices = cal_title_choices
    )
    date = models.DateField(
        auto_now_add=False, 
        auto_now=False, 
        blank=True,
    )
    start_time = models.TimeField(u'Starting time', help_text=u'Starting time', null = True, default = '00:00:00')
    end_time = models.TimeField(u'Final time', help_text=u'Final time', null = True, blank = True, default = '23:59:00')
    notes = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)
    
    class META:
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
 
    def get_absolute_url2(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s - %s</a>' % (url, str(self.title), str(self.observer))
    
    def get_absolute_url(self):
        url = '../../event_detail/' + str(self.id) + '/view'
        return u'<a href="%s">%s - %s</a>' % (url, str(self.title), str(self.observer))
 
    def clean(self):
        if str(self.end_time) <= str(self.start_time):
            raise ValidationError('Ending times must after starting times')

class spill_kits_model(models.Model):
    
    observer = models.CharField(
        max_length=30
    )
    date = models.DateField(
        auto_now_add=False, 
        auto_now=False
    )
    month = models.CharField(
        max_length=30
    )
    sk1_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk1_serial = models.CharField(
        max_length=7
    )
    sk1_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk1_report = models.CharField(
        max_length=30
    )
    sk1_comment = models.CharField(
        max_length=100
    )
    
    sk2_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk2_serial = models.CharField(
        max_length=7
    )
    sk2_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk2_report = models.CharField(
        max_length=30
    )
    sk2_comment = models.CharField(
        max_length=100
    )
    
    sk3_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk3_serial = models.CharField(
        max_length=7
    )
    sk3_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk3_report = models.CharField(
        max_length=30
    )
    sk3_comment = models.CharField(
        max_length=100
    )
    
    sk4_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk4_serial = models.CharField(
        max_length=7
    )
    sk4_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk4_report = models.CharField(
        max_length=30
    )
    sk4_comment = models.CharField(
        max_length=100
    )
    
    sk5_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk5_serial = models.CharField(
        max_length=7
    )
    sk5_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk5_report = models.CharField(
        max_length=30
    )
    sk5_comment = models.CharField(
        max_length=100
    )
    
    sk6_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk6_serial = models.CharField(
        max_length=7
    )
    sk6_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk6_report = models.CharField(
        max_length=30
    )
    sk6_comment = models.CharField(
        max_length=100
    )
    
    sk6_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk6_serial = models.CharField(
        max_length=7
    )
    sk6_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk6_report = models.CharField(
        max_length=30
    )
    sk6_comment = models.CharField(
        max_length=100
    )
    
    sk7_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk7_serial = models.CharField(
        max_length=7
    )
    sk7_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk7_report = models.CharField(
        max_length=30
    )
    sk7_comment = models.CharField(
        max_length=100
    )
    
    sk8_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk8_serial = models.CharField(
        max_length=7
    )
    sk8_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk8_report = models.CharField(
        max_length=30
    )
    sk8_comment = models.CharField(
        max_length=100
    )
    
    sk9_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk9_serial = models.CharField(
        max_length=7
    )
    sk9_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk9_report = models.CharField(
        max_length=30
    )
    sk9_comment = models.CharField(
        max_length=100
    )
    
    sk10_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk10_serial = models.CharField(
        max_length=7
    )
    sk10_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk10_report = models.CharField(
        max_length=30
    )
    sk10_comment = models.CharField(
        max_length=100
    )
    
    sk11_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk11_serial = models.CharField(
        max_length=7
    )
    sk11_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk11_report = models.CharField(
        max_length=30
    )
    sk11_comment = models.CharField(
        max_length=100
    )
    
    sk12_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk12_serial = models.CharField(
        max_length=7
    )
    sk12_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk12_report = models.CharField(
        max_length=30
    )
    sk12_comment = models.CharField(
        max_length=100
    )
    
    sk13_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk13_serial = models.CharField(
        max_length=7
    )
    sk13_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk13_report = models.CharField(
        max_length=30
    )
    sk13_comment = models.CharField(
        max_length=100
    )
    
    sk14_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk14_serial = models.CharField(
        max_length=7
    )
    sk14_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk14_report = models.CharField(
        max_length=30
    )
    sk14_comment = models.CharField(
        max_length=100
    )
    
    sk15_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk15_serial = models.CharField(
        max_length=7
    )
    sk15_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk15_report = models.CharField(
        max_length=30
    )
    sk15_comment = models.CharField(
        max_length=100
    )
    
    sk16_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk16_serial = models.CharField(
        max_length=7
    )
    sk16_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk16_report = models.CharField(
        max_length=30
    )
    sk16_comment = models.CharField(
        max_length=100
    )
    
    sk17_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk17_serial = models.CharField(
        max_length=7
    )
    sk17_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk17_report = models.CharField(
        max_length=30
    )
    sk17_comment = models.CharField(
        max_length=100
    )
    
    sk18_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk18_serial = models.CharField(
        max_length=7
    )
    sk18_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk18_report = models.CharField(
        max_length=30
    )
    sk18_comment = models.CharField(
        max_length=100
    )
    
    sk19_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk19_serial = models.CharField(
        max_length=7
    )
    sk19_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk19_report = models.CharField(
        max_length=30
    )
    sk19_comment = models.CharField(
        max_length=100
    )
    
    sk20_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk20_serial = models.CharField(
        max_length=7
    )
    sk20_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk20_report = models.CharField(
        max_length=30
    )
    sk20_comment = models.CharField(
        max_length=100
    )
    
    sk21_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk21_serial = models.CharField(
        max_length=7
    )
    sk21_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    sk21_report = models.CharField(
        max_length=30
    )
    sk21_comment = models.CharField(
        max_length=100
    )
    
    skut23_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    skut23_serial = models.CharField(
        max_length=7
    )
    skut23_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    skut23_report = models.CharField(
        max_length=30
    )
    skut23_comment = models.CharField(
        max_length=100
    )
    
    skut24_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    skut24_serial = models.CharField(
        max_length=7
    )
    skut24_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    skut24_report = models.CharField(
        max_length=30
    )
    skut24_comment = models.CharField(
        max_length=100
    )
    
    skut25_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    skut25_serial = models.CharField(
        max_length=7
    )
    skut25_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    skut25_report = models.CharField(
        max_length=30
    )
    skut25_comment = models.CharField(
        max_length=100
    )
    
    skut26_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    skut26_serial = models.CharField(
        max_length=7
    )
    skut26_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    skut26_report = models.CharField(
        max_length=30
    )
    skut26_comment = models.CharField(
        max_length=100
    )
    
    skut27_tag_on = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    skut27_serial = models.CharField(
        max_length=7
    )
    skut27_complete = models.CharField(
        max_length=3,
        choices = yes_no_choices
    )
    skut27_report = models.CharField(
        max_length=30
    )
    skut27_comment = models.CharField(
        max_length=100
    )
    
    def __str__(self):
        return str(self.month)
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    