# Generated by Django 3.2.7 on 2023-08-28 22:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0090_auto_20230827_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 26, 18, 55, 11, 837511)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 7, 18, 55, 11, 837526)),
        ),
        migrations.AlterField(
            model_name='spill_kit_inventory_model',
            name='counted_items',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='spill_kit_inventory_model',
            name='missing_items',
            field=models.CharField(max_length=300),
        ),
    ]