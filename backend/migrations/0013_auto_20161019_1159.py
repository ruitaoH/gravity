# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-19 03:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_auto_20161019_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermeet',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='usermeet',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='usermeet',
            name='meet_time',
            field=models.CharField(default='2016-10-19 11:59:42', max_length=32),
        ),
        migrations.AlterField(
            model_name='usermeet',
            name='other',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_meet_other', to='backend.User', verbose_name='相遇的用户'),
        ),
        migrations.AlterField(
            model_name='usermeet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_meet_user', to='backend.User', verbose_name='主用户'),
        ),
    ]
