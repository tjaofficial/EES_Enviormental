# Generated by Django 4.2.9 on 2025-04-15 05:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0037_braintreeplans_priceid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2025, 7, 14, 1, 50, 16, 103370)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2025, 4, 25, 1, 50, 16, 103388)),
        ),
        migrations.CreateModel(
            name='subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_subscription_id', models.CharField(max_length=100)),
                ('plan', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=20)),
                ('customerID', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('settings', models.JSONField(blank=True, default=dict, null=True)),
                ('companyChoice', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to='EES_Forms.company_model')),
            ],
        ),
    ]
