# Generated by Django 3.2.7 on 2025-07-23 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EES_Forms', '0064_auto_20250722_2304'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('was_helpful', models.BooleanField()),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('user_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='EES_Forms.helparticle')),
            ],
        ),
    ]
