from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.hashers import make_password, check_password
import binascii
import os
import math
from datetime import datetime
from . import util

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
    category = models.CharField(max_length=32,choices=(('东校区','东校区'),('主校区','主校区')))

    def __str__(self):
        return self.name + ' ' + self.category


# class Major(models.Model):
#     name = models.CharField(max_length=128)
#     department = models.ForeignKey(Department, default=1)
#
#     def __str__(self):
#         return self.name


class Clazz(models.Model):
    name = models.CharField(max_length=128)
    department = models.ForeignKey(Department,default=1)

    def __str__(self):
        return  self.department.name + ' ' + self.name


class InterestTag(models.Model):
    enname = models.CharField(max_length=128, default='')
    chname = models.CharField(max_length=128, default='')

    def __str__(self):
        return self.enname + ' ' + self.chname


class InterestTagContent(models.Model):
    enname = models.CharField(max_length=128, default='')
    chname = models.CharField(max_length=128, default='')
    category = models.CharField(max_length=32,choices=(('东校区','东校区'),('主校区','主校区')))
    tag = models.ForeignKey(InterestTag)

    def __str__(self):
        return self.enname + ' ' + self.chname


class User(models.Model):
    # 头像url
    avatar_url = models.CharField(max_length=512)
    # 手机
    phone = models.CharField(max_length=32)
    # 昵称
    nickname = models.CharField(max_length=128)
    # 性别(male|female)
    gender = models.CharField(max_length=32)
    # 年龄
    age = models.IntegerField(default=0)
    # 生日
    birthday = models.IntegerField(default=0)
    # 班级 [学院][专业][班级]
    clazz = models.CharField(max_length=128)
    # 是否屏蔽同班同学(true|false)
    block_same_class = models.BooleanField(default=True)
    # 家乡 [省份][城市]
    hometown = models.CharField(max_length=128, default='')
    # 联系方式？？？
    contact = models.CharField(max_length=256)
    # 恋爱状态
    love_status = models.CharField(max_length=128)
    # 想看性别(male|female|both)
    prefer_gender = models.CharField(max_length=128)
    # 个性签名
    introduction = models.CharField(max_length=1024)
    # 能量石
    energy_stone = models.IntegerField(default=10)
    # 密码
    password = models.CharField(max_length=256)
    # 密码盐值
    pw_salt = models.CharField(max_length=128)
    # 校区(west|middle|east)
    region = models.CharField(max_length=32, default='')

    # 注册时间 设备 ip
    # signup_time = models.IntegerField(default=0)
    signup_time = models.CharField(max_length=32)
    signup_ua = models.CharField(max_length=256)
    signup_ip = models.CharField(max_length=32)

    # 登陆时间 设备 ip
    # signin_time = models.IntegerField(default=0)
    signin_time = models.CharField(max_length=32)
    signin_ua = models.CharField(max_length=256)
    signin_ip = models.CharField(max_length=32)

    # 用户自注册以来相遇的总人数
    meet_num = models.IntegerField(default=0)

    # 这两项可以去掉
    # 记录该用户当前所在区域
    area_num = models.IntegerField(default=-1)
    # 所在地点名称
    location_name = models.CharField(max_length=128,default='')

    def __str__(self):
        return str(self.pk) + ' ' + self.nickname + ' ' + self.phone

    @staticmethod
    def generate_pw_salt():
        return binascii.b2a_hex(os.urandom(32))

    @staticmethod
    def encrypt(salt, raw_pw):
        return make_password(raw_pw, salt, 'pbkdf2_sha256')

    def check_password(self, raw_pw):
        encoded = make_password(raw_pw, self.pw_salt, 'pbkdf2_sha256')
        return encoded == self.password


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


# class UserPosition(models.Model):
#     user = models.ForeignKey(User)
#     longitude = models.FloatField(default=0.0)
#     latitude = models.FloatField(default=0.0)
#     altitude = models.FloatField(default=0.0)
#     floor = models.IntegerField(default=0)
#     horizontal_accuracy = models.FloatField(default=0.0)
#     vertical_accuracy = models.FloatField(default=0.0)
#     speed = models.FloatField(default=0.0)
#     heading = models.FloatField(default=0.0)
#     timestamp = models.IntegerField(default=0)
#     create_time = models.IntegerField(default=0)
#     location_name = models.CharField(default='', max_length=512)
#
#     def distance_to(self, other):
#         long_diff = self.longitude - other.longitude
#         lat_diff = self.latitude - other.latitude
#
#         return math.sqrt(long_diff*long_diff + lat_diff*lat_diff)
#
#     def is_meeting(self, other):
#         if abs(self.timestamp - other.timestamp) < 5*60:
#             dis = self.distance_to(other)
#             if dis <= self.horizontal_accuracy + other.horizontal_accuracy:
#                 return True
#         return False
#
#     def readable_timestamp(self):
#         d = datetime.datetime.fromtimestamp(self.timestamp)
#         return d.strftime('%Y-%m-%d %H:%M:%S')
#
#     def upload_time(self):
#         return self.readable_timestamp()
#
#     def __str__(self):
#         return self.user.phone + ' ' + str(self.longitude) + ',' + str(self.latitude) + ' ' + self.readable_timestamp()


# class UserMeet(models.Model):
#     user = models.ForeignKey(User, related_name='user_meet_user')
#     user_pos = models.ForeignKey(UserPosition, related_name='user_meet_user_pos', default=-1)
#     other = models.ForeignKey(User, related_name='user_meet_other')
#     other_pos = models.ForeignKey(UserPosition, related_name='user_meet_other_pos', default=-1)


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

    # 发送时间
    sent_time = models.IntegerField(default=0)
    # 验证时间
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


# 改动的表
'''
    相遇表在每天要进行清理
'''
class UserMeet(models.Model):
    # 主用户
    user = models.ForeignKey(User, related_name='user_meet_user',verbose_name='主用户')
    # 相遇的用户
    other = models.ForeignKey(User, related_name='user_meet_other',verbose_name='相遇用户')
    # 区域编号
    area_num = models.IntegerField(default=-1,verbose_name='区域编号')
    # 相遇地点
    location_name = models.CharField(max_length=32,default='',verbose_name='相遇地点')

    # 方便调试 ---> 增加经纬度 longitude经度 latitude纬度
    longitude = models.FloatField(default=0.0,verbose_name='经度')
    latitude = models.FloatField(default=0.0,verbose_name='纬度')

    # 相遇时间
    # meet_time = models.DateTimeField(default=datetime.datetime.now)
    meet_time = models.CharField(max_length=32,default=util.getStrTime(datetime.now()),verbose_name='相遇时间')

    # 相遇距离
    meet_distance = models.IntegerField(default=0,verbose_name='相遇距离')

class UserMeetHistory(models.Model):
    # 主用户
    user = models.ForeignKey(User, related_name='user_meet_user_history',verbose_name='主用户')
    # 相遇的用户
    other = models.ForeignKey(User, related_name='user_meet_other_history',verbose_name='相遇用户')
    # 相遇次数
    meet_num = models.IntegerField(default=0,verbose_name='相遇次数')
    # 匹配度
    matching = models.IntegerField(default=0,verbose_name='匹配度')
    # 缘分值
    fate = models.IntegerField(default=0,verbose_name='缘分值')

    def __str__(self):
        return str(self.user) + ' ' + str(self.other)

class UserPosition(models.Model):
    # UserPosition通过外键指向一个User
    user = models.ForeignKey(User,verbose_name='主用户',related_name='fkUserPosition2User')

    # 经纬度
    longitude = models.FloatField(default=0.0,verbose_name='经度')
    latitude = models.FloatField(default=0.0,verbose_name='纬度')

    # 区域编号
    area_num = models.IntegerField(default=-1, verbose_name='区域编号')
    # 相遇地点
    location_name = models.CharField(max_length=32, default='', verbose_name='地点名称')

    # 创建时间
    create_time = models.CharField(max_length=32,default=util.getStrTime(datetime.now()),verbose_name='创建时间')
    # 离开时间
    leave_time = models.CharField(max_length=32,null=True,verbose_name='离开时间')

    # def distance_to(self, other):
    #     long_diff = self.longitude - other.longitude
    #     lat_diff = self.latitude - other.latitude
    #
    #     return math.sqrt(long_diff * long_diff + lat_diff * lat_diff)

    # def is_meeting(self, other):
    #     if abs(self.timestamp - other.timestamp) < 5 * 60:
    #         dis = self.distance_to(other)
    #         if dis <= self.horizontal_accuracy + other.horizontal_accuracy:
    #             return True
    #     return False

    # def readable_timestamp(self):
    #     d = datetime.datetime.fromtimestamp(self.timestamp)
    #     return d.strftime('%Y-%m-%d %H:%M:%S')

    # def upload_time(self):
    #     return self.readable_timestamp()

    # def __str__(self):
    #     return self.user
