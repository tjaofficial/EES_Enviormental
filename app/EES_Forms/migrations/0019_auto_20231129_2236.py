# Generated by Django 3.2.7 on 2023-11-30 03:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0018_auto_20231113_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='forma3_model',
            name='l_total_sec',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='forma3_model',
            name='om_total_sec',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 27, 22, 36, 29, 579384)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 9, 22, 36, 29, 579400)),
        ),
    ]