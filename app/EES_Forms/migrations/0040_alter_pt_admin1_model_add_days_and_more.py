# Generated by Django 4.2.9 on 2025-04-16 00:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0039_rename_stripe_subscription_id_subscription_subscriptionid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2025, 7, 14, 20, 48, 11, 720717)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2025, 4, 25, 20, 48, 11, 720729)),
        ),
    ]
