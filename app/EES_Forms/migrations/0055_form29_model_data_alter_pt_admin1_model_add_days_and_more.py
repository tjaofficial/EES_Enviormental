# Generated by Django 4.2.9 on 2025-05-21 06:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0054_alter_pt_admin1_model_add_days_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='form29_model',
            name='data',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2025, 8, 19, 2, 13, 42, 851833)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 31, 2, 13, 42, 851848)),
        ),
    ]
