# Generated by Django 3.2.4 on 2021-08-02 00:22

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0152_auto_20210801_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='formo_model',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 30, 20, 22, 3, 542006)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 11, 20, 22, 3, 542020)),
        ),
    ]