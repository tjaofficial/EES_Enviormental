# Generated by Django 3.2.7 on 2023-09-01 19:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0091_auto_20230828_1855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spill_kit_inventory_model',
            name='spill_kit_submitted',
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 30, 15, 22, 59, 285610)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 11, 15, 22, 59, 285625)),
        ),
    ]