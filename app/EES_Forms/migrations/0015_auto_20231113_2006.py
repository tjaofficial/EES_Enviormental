# Generated by Django 3.2.7 on 2023-11-14 01:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0014_auto_20231107_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_model',
            name='subID',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='formd_model',
            name='truck_id1',
            field=models.CharField(blank=True, choices=[('#5', '#5'), ('#6', '#6'), ('#7', '#7'), ('#9', '#9'), ('Dozer', 'Dozer'), ('Semi', 'Semi'), ('Contractor', 'Contractor'), ('Security', 'Security'), ('Water Truck', 'Water Truck')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='formd_model',
            name='truck_id2',
            field=models.CharField(blank=True, choices=[('#5', '#5'), ('#6', '#6'), ('#7', '#7'), ('#9', '#9'), ('Dozer', 'Dozer'), ('Semi', 'Semi'), ('Contractor', 'Contractor'), ('Security', 'Security'), ('Water Truck', 'Water Truck')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='formd_model',
            name='truck_id3',
            field=models.CharField(blank=True, choices=[('#5', '#5'), ('#6', '#6'), ('#7', '#7'), ('#9', '#9'), ('Dozer', 'Dozer'), ('Semi', 'Semi'), ('Contractor', 'Contractor'), ('Security', 'Security'), ('Water Truck', 'Water Truck')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='formd_model',
            name='truck_id4',
            field=models.CharField(blank=True, choices=[('#5', '#5'), ('#6', '#6'), ('#7', '#7'), ('#9', '#9'), ('Dozer', 'Dozer'), ('Semi', 'Semi'), ('Contractor', 'Contractor'), ('Security', 'Security'), ('Water Truck', 'Water Truck')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='formd_model',
            name='truck_id5',
            field=models.CharField(blank=True, choices=[('#5', '#5'), ('#6', '#6'), ('#7', '#7'), ('#9', '#9'), ('Dozer', 'Dozer'), ('Semi', 'Semi'), ('Contractor', 'Contractor'), ('Security', 'Security'), ('Water Truck', 'Water Truck')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 11, 20, 6, 53, 45083)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 23, 20, 6, 53, 45097)),
        ),
    ]