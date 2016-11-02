from django.contrib import admin
from django.utils.text import capfirst
from django.utils.datastructures import OrderedDict

from backend import models

def find_model_index(name):
    count = 0
    for model, model_admin in admin.site._registry.items():
        if capfirst(model._meta.verbose_name_plural) == name:
            return count
        else:
            count += 1
    return count


def index_decorator(func):
    def inner(*args, **kwargs):
        templateresponse = func(*args, **kwargs)
        for app in templateresponse.context_data['app_list']:
            app['models'].sort(key=lambda x: find_model_index(x['name']))
        return templateresponse

    return inner

registry = OrderedDict()
registry.update(admin.site._registry)
admin.site._registry = registry
admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)

# 用户
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'phone',
        'nickname',
        'area_num'
    )

admin.site.register(models.User,UserAdmin)

# 用户相遇
class UserMeetAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'other',
        'area_num',
        'location_name',
        'meet_time',
        'meet_distance',
        'longitude',
        'latitude',
    )
    search_fields = ('user__phone',)

admin.site.register(models.UserMeet,UserMeetAdmin)

# 用户地点
class UserPositionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'area_num',
        'location_name',
        'create_time',
        'leave_time',
        'longitude',
        'latitude'
    )
    search_fields = ('user__phone',)

admin.site.register(models.UserPosition,UserPositionAdmin)

# 每天给每个用户推荐的人
admin.site.register(models.TodayUser)

# 相遇记录
class UserMeetHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'other',
        'meet_num',
        'matching',
        'fate'
    )
    search_fields = ('user__phone',)

admin.site.register(models.UserMeetHistory,UserMeetHistoryAdmin)

# 用户兴趣标签 能量石
admin.site.register(models.UserInterestTag)
admin.site.register(models.EnergyStoneBill)

admin.site.register(models.DeviceToken)
admin.site.register(models.PhoneVerify)
admin.site.register(models.PushNotification)
admin.site.register(models.MessageSender)
admin.site.register(models.Message)

# 需要录入的数据
# 省份 城市
admin.site.register(models.Province)
admin.site.register(models.City)

# 院系 专业 班级
admin.site.register(models.Department)
admin.site.register(models.Clazz)

# 兴趣标签 兴趣标签内容
admin.site.register(models.InterestTag)
admin.site.register(models.InterestTagContent)
