# Generated by Django 3.2.7 on 2022-04-02 02:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0024_auto_20220401_0234'),
    ]

    operations = [
        migrations.AddField(
            model_name='forma5_model',
            name='cavas',
            field=models.CharField(default='xyz', max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 30, 22, 1, 25, 103501)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 11, 22, 1, 25, 103519)),
        ),
    ]