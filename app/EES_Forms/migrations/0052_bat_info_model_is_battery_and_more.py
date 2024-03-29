# Generated by Django 4.2.9 on 2024-03-09 00:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0051_alter_form_settings_model_settings_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bat_info_model',
            name='is_battery',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='no', max_length=10),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 6, 19, 14, 28, 723403)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 18, 19, 14, 28, 723418)),
        ),
    ]
