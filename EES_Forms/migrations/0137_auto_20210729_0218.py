# Generated by Django 3.2.4 on 2021-07-29 06:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0136_auto_20210729_0216'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='subA5_model',
            new_name='formA5_model',
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 2, 17, 58, 563348)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 8, 2, 17, 58, 563362)),
        ),
    ]