# Generated by Django 4.2.9 on 2025-05-08 05:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0046_company_model_icon_alter_notifications_model_header_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issues_model',
            name='facilityChoice',
        ),
        migrations.AlterField(
            model_name='company_model',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='images/icons/'),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2025, 8, 6, 1, 1, 56, 69014)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 18, 1, 1, 56, 69030)),
        ),
    ]
