"""gravity_backend_transfer_master URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/misc/provinces$', views.get_provinces, name='get_provinces'),
    url(r'^api/misc/cities$', views.get_cities, name='get_cities'),
    url(r'^api/misc/departments$', views.get_departments, name='get_departments'),
    url(r'^api/misc/majors$', views.get_majors, name='get_majors'),
    url(r'^api/misc/classes$', views.get_classes, name='get_classes'),
    url(r'^api/misc/avatar$', views.upload_avatar, name='upload_avatar'),
    url(r'^api/misc/interests$', views.get_all_interest_tags, name='get_all_interest_tags'),
    url(r'^api/misc/device_token$', views.post_device_token, name='post_device_token'),
    url(r'^api/user/signup_sms$', views.post_signup_sms, name='post_signup_sms'),
    url(r'^api/user/password_sms$', views.post_password_sms, name='post_password_sms'),
    url(r'^api/user/verify_phone$', views.verify_phone, name='verify_phone'),
    url(r'^api/user/signin$', views.phone_signin, name='phone_signin'),
    url(r'^api/user/signup$', views.phone_signup, name='phone_signup'),
    url(r'^api/user/password$', views.update_password, name='update_password'),
    url(r'^api/user/profile$', views.update_profile, name='update_profile'),
    url(r'^api/user/interests$', views.interest_tags_view, name='interest_tags_view'),
    url(r'^api/user/position$', views.report_position, name='report_position'),
    url(r'^api/user/messages$', views.get_all_user_message, name='get_all_user_message'),
    url(r'^api/user/today$', views.get_today_user, name='get_today_user'),



    url(r'^api/user/$',views.UserSignUp),
    url(r'^api/user/phone/$',views.phone),
    url(r'^api/user/login/$',views.login),
    url(r'^api/position/$',views.post_position)
]
