# Generated by Django 3.2.7 on 2022-12-29 20:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0037_auto_20221229_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile_model',
            name='facility_name',
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 29, 15, 7, 47, 940281)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 8, 15, 7, 47, 940300)),
        ),
    ]