# Generated by Django 4.2.9 on 2025-05-08 09:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0048_event_userprof_alter_pt_admin1_model_add_days_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='enteredBy',
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2025, 8, 6, 5, 19, 8, 427687)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 18, 5, 19, 8, 427698)),
        ),
    ]
