# Generated by Django 4.2.9 on 2024-10-19 21:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0005_bat_info_model_zipcode_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sop_model',
            name='facilityChoice',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, to='EES_Forms.bat_info_model'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 17, 17, 48, 13, 248934)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 29, 17, 48, 13, 248948)),
        ),
    ]
