# Generated by Django 3.2.4 on 2021-07-12 05:25

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0082_merge_20210712_0124'),
    ]

    operations = [
        migrations.AddField(
            model_name='forms',
            name='due_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='forms',
            name='title',
            field=models.CharField(default='N/A', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='formf_model',
            name='containers_2',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formf_model',
            name='containers_3',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formf_model',
            name='containers_4',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formf_model',
            name='dates_1',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='formf_model',
            name='dates_2',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formf_model',
            name='dates_3',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formf_model',
            name='dates_4',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formf_model',
            name='waste_codes_2',
            field=models.CharField(blank=True, choices=[('universal', 'UNIV'), ('non-hazardous ', 'NON-HAZ'), ('hazardous', 'HAZ')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='formf_model',
            name='waste_codes_3',
            field=models.CharField(blank=True, choices=[('universal', 'UNIV'), ('non-hazardous ', 'NON-HAZ'), ('hazardous', 'HAZ')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='formf_model',
            name='waste_codes_4',
            field=models.CharField(blank=True, choices=[('universal', 'UNIV'), ('non-hazardous ', 'NON-HAZ'), ('hazardous', 'HAZ')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 10, 1, 24, 54, 943031)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 22, 1, 24, 54, 943046)),
        ),
    ]