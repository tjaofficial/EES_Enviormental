# Generated by Django 3.2.7 on 2022-08-23 00:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0066_auto_20220822_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='add_days',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 20, 20, 54, 47, 508311)),
        ),
        migrations.AlterField(
            model_name='pt_admin1_model',
            name='days_left',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 1, 20, 54, 47, 508329)),
        ),
        migrations.CreateModel(
            name='formH_readings_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comb_read_1', models.CharField(max_length=3)),
                ('comb_read_2', models.CharField(max_length=3)),
                ('comb_read_3', models.CharField(max_length=3)),
                ('comb_read_4', models.CharField(max_length=3)),
                ('comb_read_5', models.CharField(max_length=3)),
                ('comb_read_6', models.CharField(max_length=3)),
                ('comb_read_7', models.CharField(max_length=3)),
                ('comb_read_8', models.CharField(max_length=3)),
                ('comb_read_9', models.CharField(max_length=3)),
                ('comb_read_10', models.CharField(max_length=3)),
                ('comb_read_11', models.CharField(max_length=3)),
                ('comb_read_12', models.CharField(max_length=3)),
                ('comb_read_13', models.CharField(max_length=3)),
                ('comb_read_14', models.CharField(max_length=3)),
                ('comb_read_15', models.CharField(max_length=3)),
                ('comb_read_16', models.CharField(max_length=3)),
                ('comb_read_17', models.CharField(max_length=3)),
                ('comb_read_18', models.CharField(max_length=3)),
                ('comb_read_19', models.CharField(max_length=3)),
                ('comb_read_20', models.CharField(max_length=3)),
                ('comb_read_21', models.CharField(max_length=3)),
                ('comb_read_22', models.CharField(max_length=3)),
                ('comb_read_23', models.CharField(max_length=3)),
                ('comb_read_24', models.CharField(max_length=3)),
                ('comb_read_25', models.CharField(max_length=3)),
                ('comb_read_26', models.CharField(max_length=3)),
                ('comb_read_27', models.CharField(max_length=3)),
                ('comb_read_28', models.CharField(max_length=3)),
                ('form', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='EES_Forms.formh_model')),
            ],
        ),
    ]