# Generated by Django 3.2.7 on 2023-01-10 23:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0053_auto_20230108_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 10, 18, 26, 6, 782293)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 20, 18, 26, 6, 782319)),
        ),
        migrations.AlterField(
            model_name='user_profile_model',
            name='profile_picture',
            field=models.CharField(blank=True, max_length=100000, null=True),
        ),
    ]