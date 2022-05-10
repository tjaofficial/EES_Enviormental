# Generated by Django 3.2.7 on 2022-05-03 00:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0036_auto_20220412_0741'),
    ]

    operations = [
        migrations.AddField(
            model_name='forma5_model',
            name='canvasMediaFile',
            field=models.FileField(default='settings.STATIC_ROOT/images/A-5scetchBlack.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 31, 20, 33, 22, 235394)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 12, 20, 33, 22, 235407)),
        ),
    ]