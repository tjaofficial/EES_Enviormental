# Generated by Django 3.2.7 on 2023-10-19 21:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0101_auto_20231019_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 17, 17, 14, 44, 625459)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 29, 17, 14, 44, 625472)),
        ),
        migrations.CreateModel(
            name='form1_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observer', models.CharField(max_length=30)),
                ('date', models.DateField(blank=True)),
                ('crew', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=1)),
                ('foreman', models.CharField(max_length=30)),
                ('start', models.TimeField(blank=True)),
                ('stop', models.TimeField(blank=True)),
                ('facilityChoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='EES_Forms.bat_info_model')),
            ],
        ),
    ]