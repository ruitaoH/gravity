# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-13 09:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20161013_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='signin_time',
            field=models.DateTimeField(null=True),
        ),
    ]
