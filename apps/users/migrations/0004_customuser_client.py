# Generated by Django 5.0.6 on 2025-04-30 14:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
        ('users', '0003_alter_customuser_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clients.client'),
        ),
    ]
