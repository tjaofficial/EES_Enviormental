# Generated by Django 3.2.7 on 2023-11-07 22:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0013_auto_20231104_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_model',
            name='payment_method_token',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 5, 17, 21, 20, 1212)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 17, 17, 21, 20, 1226)),
        ),
    ]