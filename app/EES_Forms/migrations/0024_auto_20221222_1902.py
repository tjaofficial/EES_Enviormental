# Generated by Django 3.2.7 on 2022-12-23 00:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0023_auto_20221222_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formh_readings_model',
            name='comb_formL',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 22, 19, 2, 34, 612302)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 1, 19, 2, 34, 612320)),
        ),
    ]