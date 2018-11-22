# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-31 01:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core_app', '0015_auto_20181031_0120'),
    ]

    operations = [
        migrations.CreateModel(
            name='TerminalUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('terminal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_app.Terminal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
