# Generated by Django 3.1.3 on 2021-07-11 18:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0076_merge_20210711_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='suba1_readings_model',
            name='total_seconds',
            field=models.FloatField(default=0.1, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='forma2_model',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='forma3_model',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='forma4_model',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='forme_model',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='formg1_model',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='formh_model',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='formi_model',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='forml_model',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='formm_model',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 9, 14, 0, 38, 41975)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 21, 14, 0, 38, 41996)),
        ),
        migrations.AlterField(
            model_name='suba1_readings_model',
            name='c1_sec',
            field=models.FloatField(max_length=5),
        ),
        migrations.AlterField(
            model_name='suba1_readings_model',
            name='c2_sec',
            field=models.FloatField(max_length=5),
        ),
        migrations.AlterField(
            model_name='suba1_readings_model',
            name='c3_sec',
            field=models.FloatField(max_length=5),
        ),
        migrations.AlterField(
            model_name='suba1_readings_model',
            name='c4_sec',
            field=models.FloatField(max_length=5),
        ),
        migrations.AlterField(
            model_name='suba1_readings_model',
            name='c5_sec',
            field=models.FloatField(max_length=5),
        ),
    ]