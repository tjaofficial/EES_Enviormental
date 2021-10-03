# Generated by Django 3.2.7 on 2021-09-20 21:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0005_merge_0002_auto_20210831_1020_0004_auto_20210823_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='observer',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='forma1_model',
            name='observer',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='forma2_model',
            name='observer',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='forma3_model',
            name='observer',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='forma4_model',
            name='observer',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='forma5_model',
            name='observer',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='formb_model',
            name='observer_0',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='formb_model',
            name='observer_1',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='formb_model',
            name='observer_2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='formb_model',
            name='observer_3',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='formb_model',
            name='observer_4',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='formc_model',
            name='observer',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='formd_model',
            name='observer1',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='formd_model',
            name='observer2',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='formd_model',
            name='observer3',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='formd_model',
            name='observer4',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='formd_model',
            name='observer5',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='forme_model',
            name='observer',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='formi_model',
            name='obser_0',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='formi_model',
            name='obser_1',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='formi_model',
            name='obser_2',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='formi_model',
            name='obser_3',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='formi_model',
            name='obser_4',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='forml_model',
            name='obser_0',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='forml_model',
            name='obser_1',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='forml_model',
            name='obser_2',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='forml_model',
            name='obser_3',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='forml_model',
            name='obser_4',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='forml_model',
            name='obser_5',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='forml_model',
            name='obser_6',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='formm_model',
            name='observer',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='formo_model',
            name='observer',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='formp_model',
            name='observer',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 19, 17, 20, 16, 80809)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 30, 17, 20, 16, 80830)),
        ),
        migrations.AlterField(
            model_name='spill_kits_model',
            name='observer',
            field=models.CharField(max_length=30),
        ),
    ]