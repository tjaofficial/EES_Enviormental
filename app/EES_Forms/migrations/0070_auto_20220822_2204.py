# Generated by Django 3.2.7 on 2022-08-23 02:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0069_auto_20220822_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formh_model',
            name='ambient_temp_start',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='formh_model',
            name='direction_from',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='formh_model',
            name='wind_speed_start',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 20, 22, 4, 33, 552998)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 1, 22, 4, 33, 553015)),
        ),
    ]