# Generated by Django 5.0.6 on 2025-04-30 14:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
        ('social_config', '0004_remove_socialmediaintegration_access_token_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialmediaintegration',
            name='client',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='social_integrations', to='clients.client'),
        ),
    ]
