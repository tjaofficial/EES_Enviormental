# Generated by Django 3.2.7 on 2023-11-30 07:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0020_auto_20231130_0221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='braintree_model',
            name='next_billing_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='braintree_model',
            name='planID',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='braintree_model',
            name='planName',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='braintree_model',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='braintree_model',
            name='registrations',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='braintree_model',
            name='status',
            field=models.CharField(default='inactive', max_length=12),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 28, 2, 27, 31, 908619)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 10, 2, 27, 31, 908633)),
        ),
    ]