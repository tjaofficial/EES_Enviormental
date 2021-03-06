# Generated by Django 3.2.7 on 2022-07-19 02:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0056_auto_20220718_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 16, 22, 6, 11, 675866)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 28, 22, 6, 11, 675884)),
        ),
        migrations.AlterField(
            model_name='sop_model',
            name='pdf_file',
            field=models.FileField(upload_to='SOPs/'),
        ),
    ]
