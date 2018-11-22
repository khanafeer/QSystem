# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-31 01:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0018_auto_20181031_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terminaluser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
