# Generated by Django 3.2.7 on 2022-04-02 02:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0025_auto_20220401_2204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forma5_model',
            old_name='cavas',
            new_name='canvas',
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 30, 22, 6, 29, 897243)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 11, 22, 6, 29, 897265)),
        ),
    ]
