# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-30 01:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0007_auto_20181030_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terminal',
            name='details',
            field=models.TextField(default='', null=True),
        ),
    ]