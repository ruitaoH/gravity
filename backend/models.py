from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.hashers import make_password, check_password
import binascii
import os
import math
import datetime


class Province(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=128)
    province = models.ForeignKey(Province, default=1)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=32, default='')

    def __str__(self):
        return self.name + ' ' + self.category


class Major(models.Model):
    name = models.CharField(max_length=128)
    department = models.ForeignKey(Department, default=1)

    def __str__(self):
        return self.name


class Clazz(models.Model):
    name = models.CharField(max_length=128)
    major = models.ForeignKey(Major, default=1)

    def __str__(self):
        return self.name


class InterestTag(models.Model):
    enname = models.CharField(max_length=128, default='')
    chname = models.CharField(max_length=128, default='')

    def __str__(self):
        return self.enname + ' ' + self.chname


class InterestTagContent(models.Model):
    enname = models.CharField(max_length=128, default='')
    chname = models.CharField(max_length=128, default='')
    category = models.CharField(max_length=32, default='')
    tag = models.ForeignKey(InterestTag)

    def __str__(self):
        return self.enname + ' ' + self.chname


class User(models.Model):
    verify_location_long = models.FloatField(default=0.0)
    verify_location_lat = models.FloatField(default=0.0)
    avatar_url = models.CharField(max_length=512)
    phone = models.CharField(max_length=32)
    nickname = models.CharField(max_length=128)
    gender = models.CharField(max_length=32)
    age = models.IntegerField(default=0)
    birthday = models.IntegerField(default=0)
    clazz = models.CharField(max_length=128)
    block_same_class = models.BooleanField(default=True)
    hometown = models.CharField(max_length=128, default='')
    contact = models.CharField(max_length=256)
    love_status = models.CharField(max_length=128)
    prefer_gender = models.CharField(max_length=128)
    introduction = models.CharField(max_length=1024)
    energy_stone = models.IntegerField(default=10)
    password = models.CharField(max_length=256)
    pw_salt = models.CharField(max_length=128)
    signup_time = models.IntegerField(default=0)
    signup_ua = models.CharField(max_length=256)
    signup_ip = models.CharField(max_length=32)
    signin_time = models.IntegerField(default=0)
    signin_ua = models.CharField(max_length=256)
    signin_ip = models.CharField(max_length=32)
    region = models.CharField(max_length=32, default='')

    def __str__(self):
        return str(self.pk) + ' ' + self.phone

    @staticmethod
    def generate_pw_salt():
        return binascii.b2a_hex(os.urandom(32))

    @staticmethod
    def encrypt(salt,raw_pw):
        return make_password(raw_pw,salt,'pbkdf2_sha256')

    def check_password(self,raw_pw):
        encoded = make_password(raw_pw,self.pw_salt,'pbkdf2_sha256')
        return encoded == raw_pw

class UserInterestTag(models.Model):
    user = models.ForeignKey(User)
    content = models.ForeignKey(InterestTagContent, default=-1)
    tag = models.ForeignKey(InterestTag, default=-1)


class EnergyStoneBill(models.Model):
    COMPLETE_PROFILE_EARN = 'complete_profile_earn'
    CONTACT_COST = 'contact_cost'
    CONTACT_EARN = 'contact_earn'

    user = models.ForeignKey(User)
    amount = models.IntegerField(default=0)
    create_time = models.IntegerField(default=0)
    info = models.CharField(max_length=32, default='') # type to identify the bill usage
    detail = models.CharField(max_length=512, default='')


class UserPosition(models.Model):
    user = models.ForeignKey(User)
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    altitude = models.FloatField(default=0.0)
    floor = models.IntegerField(default=0)
    horizontal_accuracy = models.FloatField(default=0.0)
    vertical_accuracy = models.FloatField(default=0.0)
    speed = models.FloatField(default=0.0)
    heading = models.FloatField(default=0.0)
    timestamp = models.IntegerField(default=0)
    create_time = models.IntegerField(default=0)
    location_name = models.CharField(default='', max_length=512)

    def distance_to(self, other):
        long_diff = self.longitude - other.longitude
        lat_diff = self.latitude - other.latitude

        return math.sqrt(long_diff*long_diff + lat_diff*lat_diff)

    def is_meeting(self, other):
        if abs(self.timestamp - other.timestamp) < 5*60:
            dis = self.distance_to(other)
            if dis <= self.horizontal_accuracy + other.horizontal_accuracy:
                return True
        return False
    
    def readable_timestamp(self):
        d = datetime.datetime.fromtimestamp(self.timestamp)
        return d.strftime('%Y-%m-%d %H:%M:%S')
       
    def upload_time(self):
        return self.readable_timestamp()

    def __str__(self):
        return self.user.phone + ' ' + str(self.longitude) + ',' + str(self.latitude) + ' ' + self.readable_timestamp()


class UserMeet(models.Model):
    user = models.ForeignKey(User, related_name='user_meet_user')
    user_pos = models.ForeignKey(UserPosition, related_name='user_meet_user_pos', default=-1)
    other = models.ForeignKey(User, related_name='user_meet_other')
    other_pos = models.ForeignKey(UserPosition, related_name='user_meet_other_pos', default=-1)


class DeviceToken(models.Model):
    token = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, null=True)
    create_time = models.IntegerField(default=0)
    
    def __str__(self):
        if self.user is None:
            return self.token + '  ' + str(self.create_time)
        return self.user.phone + '  ' + self.token + '  ' + str(self.create_time)


class PhoneVerify(models.Model):
    SIGNUP = 'signup'
    PASSWORD = 'password'

    phone = models.CharField(max_length=32)
    code = models.CharField(max_length=8)
    sent_time = models.IntegerField(default=0)
    verify_time = models.IntegerField(default=0)
    sms_type = models.CharField(max_length=16, default='')
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.phone + ' ' + self.code


class PushNotification(models.Model):
    usage = models.CharField(max_length=32, default='', primary_key=True)
    content = models.CharField(max_length=256, default='')

    def __str__(self):
        return self.usage + ' ' + self.content


class MessageSender(models.Model):
    icon_url = models.CharField(max_length=32, default='')
    name = models.CharField(max_length=128, default='')
    mark = models.CharField(max_length=32, default='')


class Message(models.Model):
    user = models.ForeignKey(User)
    sender = models.ForeignKey(MessageSender, default=-1)
    content = models.CharField(max_length=1024, default='')
    create_time = models.IntegerField(default=0)


class TodayUser(models.Model):
    user = models.ForeignKey(User, related_name='today_user_user')
    other = models.ForeignKey(User, related_name='today_user_other')
    create_time = models.IntegerField(default=0)
