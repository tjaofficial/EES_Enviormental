# Generated by Django 3.2.4 on 2021-07-29 06:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0135_auto_20210728_1934'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='subA1_model',
            new_name='formA1_model',
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 2, 16, 2, 512849)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 8, 2, 16, 2, 512863)),
        ),
    ]