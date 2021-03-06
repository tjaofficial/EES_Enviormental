# Generated by Django 3.2.7 on 2022-07-08 20:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0043_auto_20220705_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formm_model',
            name='parking',
            field=models.CharField(choices=[('par1', 'Gap Gate Parking'), ('par2', 'Truck Garage Area'), ('par3', 'EES Coke Office Parking')], max_length=30),
        ),
        migrations.AlterField(
            model_name='formm_model',
            name='storage',
            field=models.CharField(choices=[('sto1', 'Area B Coke Storage Piles'), ('sto2', 'EES Coke Coal Storage Piles')], max_length=30),
        ),
        migrations.AlterField(
            model_name='formm_model',
            name='unpaved',
            field=models.CharField(choices=[('unp1', 'North Gate Truck Turn'), ('unp2', 'Screening Station Road'), ('unp3', 'Coal Handling Road (Partial)'), ('unp4', 'Taj Mahal Road'), ('unp5', 'PECS Approach'), ('unp6', 'No. 2 Boilerhouse Road')], max_length=30),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 6, 16, 23, 27, 465617)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 18, 16, 23, 27, 465640)),
        ),
    ]
