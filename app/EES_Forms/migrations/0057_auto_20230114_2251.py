# Generated by Django 3.2.7 on 2023-01-15 03:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0056_auto_20230111_2202'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_profile_model',
            old_name='facility_name',
            new_name='company',
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 14, 22, 51, 4, 269071)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 24, 22, 51, 4, 269089)),
        ),
    ]