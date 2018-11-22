# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-31 01:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0013_auto_20181030_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quelog',
            name='date_join',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='terminal',
            name='service',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='core_app.Service'),
        ),
    ]
