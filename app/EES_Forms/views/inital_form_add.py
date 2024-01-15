import datetime
from ..models import Forms
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

def add_forms_to_database():
    today = datetime.date.today()
    GROUP_LIST = ['supervisor', 'client', 'observer']
    MODEL_LIST = ContentType.objects.all()
    PERMISSION_LIST = ['view','add', 'change', 'delete']
    DONT_CHANGE = ['log entry', 'permission', 'group', 'user', 'content type', 'session', 'fa q_model']

    for group in GROUP_LIST:
        new_group, created = Group.objects.get_or_create(name=group)
        for model in MODEL_LIST:
            if model.name not in DONT_CHANGE:
                print(model.name)
                for perm in PERMISSION_LIST:
                    codename_build = 'can_' + perm + '_' + model.name
                    name_build = 'can '+ perm + ' ' + model.name      
                    permission = Permission.objects.get(
                        codename=codename_build,
                        name=name_build,
                        content_type=model
                    )
                    new_group.permissions.add(permission)
        print("added " + group)
    
    # ADD IN THE FORMS IF DATABASE HAS LESS THAN 5----------
    # ADD IN THE FORMS IF DATABASE HAS LESS THAN 5----------
    if Forms.objects.count() <= 5:
        A1 = Forms(
            form=1,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="formA1",
            header="Method 303",
            title="Charging",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        A2 = Forms(
            form=2,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="formA2",
            header="Method 303",
            title="Doors",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        A3 = Forms(
            form=3,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="formA3",
            header="Method 303",
            title="Lids and Offtakes",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        A4 = Forms(
            form=4,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="formA4",
            header="Method 303",
            title="Collection Main",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        A5 = Forms(
            form=5,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="formA5",
            header="Method 9B",
            title="Push Travels",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        B = Forms(
            form=6,
            frequency="Daily",
            day_freq='Weekdays',
            weekdays_only=True,
            weekend_only=False,
            link="formB",
            header="Method 9",
            title="Fugitive Dust Inspection",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        C = Forms(
            form=7,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="formC",
            header="Method 9",
            title="Method 9D - Coal Field",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        D = Forms(
            form=8,
            frequency="Weekly",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="formD",
            header="Method 9",
            title="Random Truck Inspection",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        E = Forms(
            form=9,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="formE",
            header="Method 9",
            title="Gooseneck Inspection",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F1 = Forms(
            form=10,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="formF1",
            header="Waste Weekly Inspections",
            title="SIF / K087 Process Area (Satellite)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F2 = Forms(
            form=11,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="formF2",
            header="Waste Weekly Inspections",
            title="#1 Shop (Satellite Accumulation)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F3 = Forms(
            form=12,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="formF3",
            header="Waste Weekly Inspections",
            title="#2 Shop (Satellite Accumulation)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F4 = Forms(
            form=13,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="formF4",
            header="Waste Weekly Inspections",
            title="Battery (Satellite Accumulation)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F5 = Forms(
            form=14,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="formF5",
            header="Waste Weekly Inspections",
            title="Bio Plant (Satellite Accumulation)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F6 = Forms(
            form=15,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="formF6",
            header="Waste Weekly Inspections",
            title="No. 8 Tank Area (Satellite Accumulation)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F7 = Forms(
            form=16,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="formF7",
            header="Waste Weekly Inspections",
            title="Booster Pad (90-Day Accumulation)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        G1 = Forms(
            form=17,
            frequency="Weekly",
            day_freq='Weekdays',
            weekdays_only=False,
            weekend_only=False,
            link="formG1",
            header="PECS Baghouse Stack",
            title="Method 9/Non-Certified Observations",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        G2 = Forms(
            form=18,
            frequency="Monthly",
            day_freq='Weekdays',
            weekdays_only=False,
            weekend_only=False,
            link="formG2",
            header="PECS Baghouse Stack",
            title="Method 9B",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        H = Forms(
            form=19,
            frequency="Weekly",
            day_freq='Weekdays',
            weekdays_only=False,
            weekend_only=False,
            link="formH",
            header="Method 9",
            title="Method 9 - Combustion Stack",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        I = Forms(
            form=20,
            frequency="Daily",
            day_freq='Weekdays',
            weekdays_only=True,
            weekend_only=False,
            link="formI",
            header="Sampling",
            title="Quench Water Sampling Form",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        L = Forms(
            form=21,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="formL",
            header="Method 9",
            title="Visual Emissions Observations",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        M = Forms(
            form=22,
            frequency="Daily",
            day_freq='Weekdays',
            weekdays_only=True,
            weekend_only=False,
            link="formM",
            header="Method 9D",
            title="Method 9D Observation",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        N = Forms(
            form=23,
            frequency="Monthly",
            day_freq='Weekdays',
            weekdays_only=False,
            weekend_only=False,
            link="formN",
            header="Fugitive Dust Inspection",
            title="Method 9D Monthly Checklist",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        O = Forms(
            form=24,
            frequency="Weekly",
            day_freq='Weekends',
            weekdays_only=False,
            weekend_only=True,
            link="formO",
            header="Stormwater Observation Form",
            title="MP 108A",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        P = Forms(
            form=25,
            frequency="Weekly",
            day_freq='Weekends',
            weekdays_only=False,
            weekend_only=True,
            link="formP",
            header="Outfall Observation Form",
            title="Outfall 008",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        spill_kits = Forms(
            form=26,
            frequency="Monthly",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="spill_kits",
            header="Spill Kits Form",
            title="Inspection Check List",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        quarterly_trucks = Forms(
            form=27,
            frequency="Quarterly",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="quarterly_trucks",
            header="Quarterly Trucks Form",
            title="Inspection Check List",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        STI_SP001_monthly_inspection = Forms(
            form=28,
            frequency="Monthly",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="form28",
            header="STI SP001",
            title="Monthly Tank Inspection Checklist",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False
        )

        A1.save()
        A2.save()
        A3.save()
        A4.save()
        A5.save()
        B.save()
        C.save()
        D.save()
        E.save()
        F1.save()
        F2.save()
        F3.save()
        F4.save()
        F5.save()
        F6.save()
        F7.save()
        G1.save()
        G2.save()
        H.save()
        I.save()
        L.save()
        M.save()
        N.save()
        O.save()
        P.save()
        spill_kits.save()
        quarterly_trucks.save()
        STI_SP001_monthly_inspection.save()