# Generated by Django 3.2.7 on 2023-01-04 00:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0051_auto_20230103_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='bat_info_model',
            name='city',
            field=models.CharField(default='none', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 3, 19, 19, 55, 288171)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 13, 19, 19, 55, 288188)),
        ),
    ]