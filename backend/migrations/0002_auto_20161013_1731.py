# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-13 09:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMeetHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meet_num', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='userposition',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='verify_location_lat',
        ),
        migrations.RemoveField(
            model_name='user',
            name='verify_location_long',
        ),
        migrations.RemoveField(
            model_name='usermeet',
            name='other_pos',
        ),
        migrations.RemoveField(
            model_name='usermeet',
            name='user_pos',
        ),
        migrations.AddField(
            model_name='user',
            name='meet_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='usermeet',
            name='area_num',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='usermeet',
            name='meet_place',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AddField(
            model_name='usermeet',
            name='meet_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='signin_time',
            field=models.DateTimeField(verbose_name=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='user',
            name='signup_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.DeleteModel(
            name='UserPosition',
        ),
        migrations.AddField(
            model_name='usermeethistory',
            name='other',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_meet_other_history', to='backend.User'),
        ),
        migrations.AddField(
            model_name='usermeethistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_meet_user_history', to='backend.User'),
        ),
    ]
