# Generated by Django 4.2.9 on 2024-03-02 01:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0045_alter_packets_model_frequency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packets_model',
            name='formList',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 30, 20, 11, 40, 115194)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 11, 20, 11, 40, 115216)),
        ),
    ]