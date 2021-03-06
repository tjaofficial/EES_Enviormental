# Generated by Django 3.2.7 on 2022-07-30 00:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0059_auto_20220718_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formc_model',
            name='salt_start_time',
            field=models.TimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='formc_model',
            name='sto_start_time',
            field=models.TimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='formc_model',
            name='sto_stop_time',
            field=models.TimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='salt_1',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='salt_10',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='salt_11',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='salt_12',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='salt_2',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='salt_3',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='salt_4',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='salt_5',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='salt_6',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='salt_7',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='salt_8',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='salt_9',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='storage_1',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='storage_10',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='storage_11',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='storage_12',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='storage_2',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='storage_3',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='storage_4',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='storage_5',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='storage_6',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='storage_7',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='storage_8',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='formc_readings_model',
            name='storage_9',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 27, 20, 44, 17, 771629)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 8, 20, 44, 17, 771650)),
        ),
    ]
