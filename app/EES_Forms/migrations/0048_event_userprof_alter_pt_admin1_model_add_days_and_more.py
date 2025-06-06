# Generated by Django 4.2.9 on 2025-05-08 09:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0047_remove_issues_model_facilitychoice_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='userProf',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='EES_Forms.user_profile_model'),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2025, 8, 6, 5, 18, 43, 26994)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 18, 5, 18, 43, 27005)),
        ),
    ]
