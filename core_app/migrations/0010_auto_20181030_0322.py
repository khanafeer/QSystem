# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-30 03:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0009_auto_20181030_0127'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='serviceterminal',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='serviceterminal',
            name='service',
        ),
        migrations.RemoveField(
            model_name='serviceterminal',
            name='terminal',
        ),
        migrations.AddField(
            model_name='terminal',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core_app.Service'),
        ),
        migrations.DeleteModel(
            name='ServiceTerminal',
        ),
    ]
