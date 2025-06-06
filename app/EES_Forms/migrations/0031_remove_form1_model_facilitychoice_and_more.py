# Generated by Django 4.2.9 on 2025-04-03 21:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0030_alter_pt_admin1_model_add_days_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form1_model',
            name='facilityChoice',
        ),
        migrations.RemoveField(
            model_name='form2_model',
            name='facilityChoice',
        ),
        migrations.RemoveField(
            model_name='form3_model',
            name='facilityChoice',
        ),
        migrations.RemoveField(
            model_name='form4_model',
            name='facilityChoice',
        ),
        migrations.RemoveField(
            model_name='form5_model',
            name='facilityChoice',
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2025, 7, 2, 17, 4, 14, 3257)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2025, 4, 13, 17, 4, 14, 3269)),
        ),
    ]
