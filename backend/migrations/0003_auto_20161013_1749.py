# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-13 09:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20161013_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='signin_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]