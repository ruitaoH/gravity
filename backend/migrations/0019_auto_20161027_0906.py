# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-27 01:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0018_auto_20161026_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermeet',
            name='meet_time',
            field=models.CharField(default='2016-10-27 09:06:07', max_length=32, verbose_name='相遇时间'),
        ),
        migrations.AlterField(
            model_name='userposition',
            name='create_time',
            field=models.CharField(default='2016-10-27 09:06:07', max_length=32, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='userposition',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UserPosition2User', to='backend.User', verbose_name='主用户'),
        ),
    ]