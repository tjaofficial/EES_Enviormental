# Generated by Django 3.2.7 on 2022-09-09 19:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0002_auto_20220908_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forma3_model',
            name='one_pass',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 8, 15, 22, 9, 92809)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 19, 15, 22, 9, 92826)),
        ),
    ]