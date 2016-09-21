from django.contrib import admin

# Register your models here.
from backend import models

# 省份 城市
admin.site.register(models.Province)
admin.site.register(models.City)

# 院系 专业 班级
admin.site.register(models.Department)
admin.site.register(models.Major)
admin.site.register(models.Clazz)

# 兴趣标签 兴趣内容 用户 用户兴趣标签 能量石
admin.site.register(models.InterestTag)
admin.site.register(models.InterestTagContent)
admin.site.register(models.User)
admin.site.register(models.UserInterestTag)
admin.site.register(models.EnergyStoneBill)

admin.site.register(models.UserMeet)
admin.site.register(models.DeviceToken)
admin.site.register(models.PhoneVerify)
admin.site.register(models.PushNotification)
admin.site.register(models.MessageSender)
admin.site.register(models.Message)
admin.site.register(models.TodayUser)

class UserPositionAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp','upload_time')

admin.site.register(models.UserPosition,UserPositionAdmin)
