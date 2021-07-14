# Generated by Django 3.2.4 on 2021-07-13 14:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0085_auto_20210712_1511'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='formF_model',
            new_name='formF1_model',
        ),
        migrations.AlterField(
            model_name='forms',
            name='date_submitted',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='forms',
            name='due_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 11, 10, 3, 47, 878937)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 23, 10, 3, 47, 878951)),
        ),
    ]