# Generated by Django 3.2.4 on 2021-07-15 02:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0096_auto_20210714_2140'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forma2_model',
            old_name='inop_doors',
            new_name='inop_doors_eq',
        ),
        migrations.AlterField(
            model_name='forma3_model',
            name='inop_ovens',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 22, 11, 17, 902750)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 24, 22, 11, 17, 902766)),
        ),
        migrations.AlterField(
            model_name='suba5_readings_model',
            name='o1_average_6',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='suba5_readings_model',
            name='o1_highest_opacity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='suba5_readings_model',
            name='o2_average_6',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='suba5_readings_model',
            name='o2_highest_opacity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='suba5_readings_model',
            name='o3_average_6',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='suba5_readings_model',
            name='o3_highest_opacity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='suba5_readings_model',
            name='o4_average_6',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='suba5_readings_model',
            name='o4_highest_opacity',
            field=models.IntegerField(),
        ),
    ]