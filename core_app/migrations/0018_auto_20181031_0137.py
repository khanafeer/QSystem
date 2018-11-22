# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-31 01:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0017_auto_20181031_0134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terminaluser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
