# Generated by Django 3.2.7 on 2022-12-20 23:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0014_auto_20221112_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='formg1_readings_model',
            name='PEC_oven1',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='formg1_readings_model',
            name='PEC_oven2',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='formg1_readings_model',
            name='PEC_time1',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='formg1_readings_model',
            name='PEC_time2',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 20, 18, 38, 16, 658703)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 30, 18, 38, 16, 658720)),
        ),
    ]