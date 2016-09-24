# coding: utf-8
from django.http import HttpResponse, HttpResponseBadRequest
from django import forms
from . import models,zhinput
import json
from django.forms import model_to_dict
import requests
import random
import time
import base64
# import config
import os


def full_user_avatar_url(filename):
    return os.path.join(config.AVATAR_HOST, filename)


def age_from_timestamp(timestamp):
    time_struct = time.localtime(float(timestamp))
    now = time.localtime()
    age = now.tm_year - time_struct.tm_year
    return age


def user_model_to_dict(user_model):
    udict = model_to_dict(user_model)
    udict['avatar_url'] = full_user_avatar_url(user_model.avatar_url)
    del udict['password']
    del udict['pw_salt']
    udict['age'] = age_from_timestamp(user_model.birthday)
    return udict


def generate_random_code(length=4):
    s = ''
    for i in range(length):
        s += str(random.randint(0, 9))
    return s


def send_sms_to_phone(phone, message):
    resp = requests.post(
        "http://sms-api.luosimao.com/v1/send.json",
        auth=("api", "api-key"),
        data={
            "mobile": phone,
            "message": message
        },
        timeout=3,
        verify=False
    )
    result = json.loads(resp.content.decode())
    return result


def response(error, msg, data):
    return json.dumps({
        'error': error,
        'msg': msg,
        'data': data
    })


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def get_provinces(request):
    provinces = models.Province.objects.all()
    result = [model_to_dict(p) for p in provinces]
    body = response('ok', 'get provinces success', {
        'provinces': result
    })
    print(result)
    return HttpResponse(body)


def get_cities(request):
    province_id = request.GET.get('province_id', -1)
    cities = models.City.objects.filter(province=province_id)
    result = [model_to_dict(c) for c in cities]
    body = response('ok', 'get cities success', {
        'cities': result
    })
    return HttpResponse(body)


def get_departments(request):
    departments = models.Department.objects.all()
    result = [model_to_dict(d) for d in departments]
    body = response('ok', 'get departments success', {
        'departments': result
    })
    return HttpResponse(body)


def get_majors(request):
    department_id = request.GET.get('department_id', -1)
    majors = models.Major.objects.filter(department=department_id)
    result = [model_to_dict(m) for m in majors]
    body = response('ok', 'get majors success', {
        'majors': result
    })
    return HttpResponse(body)


def get_classes(request):
    major_id = request.GET.get('major_id', -1)
    classes = models.Clazz.objects.filter(major=major_id)
    result = [model_to_dict(c) for c in classes]
    body = response('ok', 'get classes success', {
        'classes': result
    })
    return HttpResponse(body)


def verify_phone(request):
    phone = request.POST.get('phone', '')
    code = request.POST.get('code', '')
    sms_type = request.POST.get('type', '')
    try:
        verify = models.PhoneVerify.objects.get(
            phone=phone,
            code=code,
            sms_type=sms_type,
            verify_time=0
        )
        verify.verify_time = int(time.time())
        verify.save()
    except models.PhoneVerify.DoesNotExist:
        body = response('verify:failed', 'verify failed', {})
        return HttpResponse(body)

    body = response('ok', 'verify success', {})
    return HttpResponse(body)


def post_signup_sms(request):
    phone = request.POST.get('phone', '')
    code = generate_random_code()

    phone_model = models.User.objects.filter(phone=phone)
    if phone_model.count() > 0:
        body = response('phone:exists', 'user exists', {'phone': phone})
        return HttpResponse(body)
    
    # save code and phone to db
    verify = models.PhoneVerify(
        phone=phone,
        code=code,
        sent_time=int(time.time()),
        sms_type=models.PhoneVerify.SIGNUP
    )
    verify.save()

    # send sms
    sms = r'欢迎注册gravity，验证码为{}【引力】'.format(code)
    r = send_sms_to_phone(phone, sms)
    print(r)
    body = response('ok', 'send sms success', {})
    return HttpResponse(body)


def post_password_sms(request):
    phone = request.POST.get('phone', '')
    code = generate_random_code()
    phone_model = models.User.objects.filter(phone=phone)
    if phone_model.count() == 0:
        body = response('phone:not_exists', 'user not exists', {'phone': phone})
        return HttpResponse(body)

    # save code and phone to db
    verify = models.PhoneVerify(
        phone=phone,
        code=code,
        sent_time=int(time.time()),
        sms_type=models.PhoneVerify.PASSWORD
    )
    verify.save()

    # send sms
    sms = r'正在找回gravity密码，验证码为{}【引力】'.format(code)
    send_sms_to_phone(phone, sms)
    body = response('ok', 'send sms success', {})
    return HttpResponse(body)


def phone_signup(request):
    try:
        zhinput.all_exists(request.POST, (
            'nickname', 'phone', 'password', 'verify_location_long', 'verify_location_lat', 'gender', 'birthday', 'clazz', 'block_same_class',
            'hometown', 'love_status', 'prefer_gender', 'contact', 'region'
        ))
    except zhinput.ZHInputKeyNotExist as e:
        body = response(e.key + ':not_exists', e.key + ' missing', {})
        return HttpResponse(body)

    try:
        phone = zhinput.as_string(request.POST, 'phone', min_length=11, max_length=11)
    except (zhinput.ZHInputStringTooShort, zhinput.ZHInputStringNotLongEnough) as e:
        body = response(e.key + ':invalid', e.key + 'is invalid', {})
        return HttpResponse(body)

    # check user by phone
    if models.User.objects.filter(phone=phone).count() > 0:
        body = response('user:exists', 'user exists', {})
        return HttpResponse(body)

    # check verified or not
    try:
        phone_verify_cursor = models.PhoneVerify.objects.filter(
            phone=phone,
            verify_time__gt=0,
            sms_type=models.PhoneVerify.SIGNUP,
            used=False
        ).order_by('-verify_time')
        phone_verify_model = phone_verify_cursor[0]
    except IndexError:
        body = response('phone:not_verified', 'phone not verified', {})
        return HttpResponse(body)

    # data check
    try:
        nickname = zhinput.as_string(request.POST, 'nickname')
        password = zhinput.as_string(request.POST, 'password')
        verify_location_long = zhinput.as_float(request.POST, 'verify_location_long')
        verify_location_lat = zhinput.as_float(request.POST, 'verify_location_lat')
        avatar = zhinput.as_string(request.POST, 'avatar', default='default_avatar.png')
        gender = zhinput.as_enum(request.POST, 'gender', ('', 'male', 'female'))
        birthday = zhinput.as_int(request.POST, 'birthday')
        clazz = zhinput.as_string(request.POST, 'clazz')

        block_same_class = zhinput.as_bool(request.POST, 'block_same_class')
        hometown = zhinput.as_string(request.POST, 'hometown')

        love_status = zhinput.as_enum(request.POST, 'love_status', ('', 'single', 'married', 'loving'))
        prefer_gender = zhinput.as_enum(request.POST, 'prefer_gender', ('', 'male', 'female', 'both'))
        contact = zhinput.as_string(request.POST, 'contact')
        introduction = zhinput.as_string(request.POST, 'introduction')
        # {"tag_id":<id>, "content_id": <id>}
        interest_tags = zhinput.as_json(request.POST, 'interest_tags')
        region = zhinput.as_enum(request.POST, 'region', ('', 'west', 'east', 'middle'))
    except zhinput.ZHInputNotFloat as e:
        body = response(e.key + ':not_float', e.key + ' is not float', {})
        return HttpResponse(body)
    except zhinput.ZHInputNotJSONString as e:
        body = response(e.key + ':not_json', e.key + ' is not json string', {})
        return HttpResponse(body)
    except zhinput.ZHInputEnumNotExists as e:
        body = response(e.key + ':not_valid', e.key + ' is not valid value', {})
        return HttpResponse(body)

    # stone get by interest tags
    tags_count = len(interest_tags)

    pw_salt = models.User.generate_pw_salt()

    print('pw_salt type:',type(pw_salt))
    print('password type:',type(password))
    print(type(models.User.encrypt(pw_salt.decode(), password)))

    user = models.User(
        nickname=nickname,
        phone=phone,
        pw_salt=pw_salt,
        password=models.User.encrypt(pw_salt.decode(), password), # make_password(str,str,'加密算法') ---> 返回str
        verify_location_long=verify_location_long,
        verify_location_lat=verify_location_lat,
        avatar_url=avatar,
        gender=gender,
        birthday=birthday,
        clazz=clazz,
        block_same_class=block_same_class,
        hometown=hometown,
        love_status=love_status,
        prefer_gender=prefer_gender,
        contact=contact,
        introduction=introduction,
        energy_stone=10 + tags_count*5,
        region=region,
        signup_ua=request.META.get('HTTP_USER_AGENT', ''),
        signup_ip=request.META.get('REMOTE_ADDR', ''),
        signup_time=int(time.time())
    )
    user.save()

    # save bills
    for tag in interest_tags:
        bill = models.EnergyStoneBill(
            user=user,
            amount=5,
            create_time=int(time.time()),
            info=models.EnergyStoneBill.COMPLETE_PROFILE_EARN,
            detail=str(tag['id']) + ':' + str(tag['content_id'])
        )
        bill.save()

    # insert interest tags
    for tag in interest_tags:
        # check interest tag id
        try:
            tag_model = models.InterestTag.objects.get(pk=tag['id'])
        except models.InterestTag.DoesNotExist:
            continue

        try:
            tag_content_model = models.InterestTagContent.objects.get(pk=tag['content_id'])
        except models.InterestTagContent.DoesNotExist:
            continue

        user_tag_model = models.UserInterestTag(
            user=user,
            tag=tag_model,
            content=tag_content_model
        )
        user_tag_model.save()

    phone_verify_model.used = True
    phone_verify_model.save()

    body = response('ok', 'signup success', {
        'user': user_model_to_dict(user)
    })
    return HttpResponse(body)


def phone_signin(request):
    phone = request.POST.get('phone', '')
    password = request.POST.get('password', '')
    try:
        phone_model = models.User.objects.get(phone=phone)
        check = phone_model.check_password(password)
        body = ''
        if check:
            body = response('ok', 'signin success', model_to_dict(phone_model))
        else:
            body = response('user:wrong_password', 'wrong password', {})
        return HttpResponse(body)
    except models.User.DoesNotExist:
        body = response('phone:not_exists', 'user not exists', {})
        return HttpResponse(body)


def report_position(request):
    try:
        zhinput.all_exists(request.POST, (
            'user_id', 'longitude', 'latitude', 'altitude', 'floor',
            'horizontal_accuracy', 'vertical_accuracy', 'speed',
            'timestamp', 'heading'
        ))
    except zhinput.ZHInputKeyNotExist as e:
        body = response(e.key + ':not_exists', e.key + ' missing', {})
        return HttpResponse(body)

    try:
        user_id = zhinput.as_int(request.POST, 'user_id')
        longitude = zhinput.as_float(request.POST, 'longitude')
        latitude = zhinput.as_float(request.POST, 'latitude')
        altitude = zhinput.as_float(request.POST, 'altitude')
        floor = zhinput.as_float(request.POST, 'floor')
        horizontal_accuracy = zhinput.as_float(request.POST, 'horizontal_accuracy')
        vertical_accuracy = zhinput.as_float(request.POST, 'vertical_accuracy')
        speed = zhinput.as_float(request.POST, 'speed')
        timestamp = zhinput.as_float(request.POST, 'timestamp')
        heading = zhinput.as_float(request.POST, 'heading')
        location_name = zhinput.as_string(request.POST, 'location_name')
    except zhinput.ZHInputNotInt as e:
        body = response(e.key + ':not_int', e.key + ' is not int', {})
        return HttpResponse(body)
    except zhinput.ZHInputNotFloat as e:
        body = response(e.key + ':not_float', e.key + ' is not float', {})
        return HttpResponse(body)

    try:
        user = models.User.objects.get(pk=user_id)
        pos_model = models.UserPosition(
            user=user,
            longitude=longitude,
            latitude=latitude,
            altitude=altitude,
            floor=floor,
            horizontal_accuracy=horizontal_accuracy,
            vertical_accuracy=vertical_accuracy,
            speed=speed,
            timestamp=timestamp,
            heading=heading,
            create_time=int(time.time()),
            location_name=location_name
        )
        pos_model.save()
    except models.User.DoesNotExist:
        body = response('user:not_exists', 'user doesnt exist', {})
        return HttpResponse(body)

    body = response('ok', 'report position success', {})
    return HttpResponse(body)


def post_device_token(request):
    try:
        zhinput.all_exists(request.POST, (
            'device_token',
        ))
    except zhinput.ZHInputKeyNotExist as e:
        body = response(e.key + ':not_exists', e.key + ' missing', {})
        return HttpResponse(body)

    try:
        user_id = zhinput.as_int(request.POST, 'user_id')
        device_token = zhinput.as_string(request.POST, 'device_token')
    except zhinput.ZHInputNotInt as e:
        body = response(e.key + ':not_int', e.key + ' is not int', {})
        return HttpResponse(body)

    user_in_token = None

    try:
        user = models.User.objects.get(pk=user_id)
        user_in_token = user
    except models.User.DoesNotExist:
        pass
    token_model = models.DeviceToken(
        token=device_token,
        user=user_in_token,
        create_time=int(time.time())
    )
    token_model.save()

    body = response('ok', 'post device token success', {})
    return HttpResponse(body)


def get_other_user_profile(request):
    user_id = request.GET.get('user_id', -1)
    target_id = request.GET.get('target_id', -1)

    try:
        user = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        body = response('user:not_exists', 'user doesnt exist', {})
        return HttpResponse(body)

    try:
        target = models.User.objects.get(pk=target_id)
    except models.User.DoesNotExist:
        body = response('target:not_exists', 'user doesnt exist', {})
        return HttpResponse(body)

    # cost energy stone
    if user.energy_stone < 10:
        body = response('energy_stone:not_enough', 'not enough energy stone', {})
        return HttpResponse(body)

    cost_bill = models.EnergyStoneBill(
        user=user,
        amount=-10,
        create_time=int(time.time()),
        info=models.EnergyStoneBill.CONTACT_COST
    )
    cost_bill.save()

    user.energy_stone -= 10

    earn_bill = models.EnergyStoneBill(
        user=target,
        amount=10,
        create_time=int(time.time()),
        info=models.EnergyStoneBill.CONTACT_EARN
    )
    earn_bill.save()

    target.energy_stone += 10

    body = response('ok', 'get user info success', {
        'target': model_to_dict(target)
    })
    return HttpResponse(body)


def update_password(request):
    phone = request.POST.get('phone', '')
    password = request.POST.get('password', '')

    try:
        phone_verify_cursor = models.PhoneVerify.objects.filter(
            phone=phone,
            verify_time__gt=0,
            used=False,
            sms_type=models.PhoneVerify.PASSWORD
        )
        phone_verify_model = phone_verify_cursor[0]
    except IndexError:
        body = response('phone:not_verified', 'phone is not verified', {})
        return HttpResponse(body)

    try:
        user_model = models.User.objects.get(phone=phone)
        user_model.pw_salt = models.User.generate_pw_salt()
        user_model.password = models.User.encrypt(user_model.pw_salt, password)
        user_model.save()
    except models.User.DoesNotExist:
        body = response('user:not_exists', 'user doesnt exist', {})
        return HttpResponse(body)

    phone_verify_model.used = True
    phone_verify_model.save()

    body = response('ok', 'upadte password success', {})
    return HttpResponse(body)


def update_profile(request):
    keys = (
        'user_id', 'avatar_url', 'nickname', 'gender', 'birthday',
        'clazz', 'block_same_class', 'hometown',
        'contact', 'love_status', 'prefer_gender',
        'introduction'
    )

    try:
        zhinput.all_exists(request.POST, ('user_id', ))
    except zhinput.ZHInputKeyNotExist as e:
        body = response(e.key + ':not_exists', e.key + ' missing', {})
        return HttpResponse(body)

    data = zhinput.filter_by_list(request.POST, keys)
    try:
        user_id = zhinput.as_int(data, 'user_id')
    except zhinput.ZHInputNotInt as e:
        body = response('user_id:not_valid', 'user id not valid', {})
        return HttpResponse(body)

    try:
        data['birthday'] = zhinput.as_int(data, 'birthday')
        data['gender'] = zhinput.as_enum(data, 'gender', ('male', 'female'))
        data['block_same_class'] = zhinput.as_bool(data, 'block_same_class')
        data['love_status'] = zhinput.as_enum(data, 'love_status', ('signle', 'married', 'loving'))
        data['prefer_gender'] = zhinput.as_enum(data, 'prefer_gender', ('male', 'female', 'both'))
    except zhinput.ZHInputException as e:
        body = response(e.key + ':not_valid', e.key + ' not valid', {})
        return HttpResponse(body)

    try:
        user_model = models.User.objects.get(pk=user_id)
        for d in data:
            setattr(user_model, d, data[d])

        user_model.save()
    except models.User.DoesNotExist:
        body = response('user:not_exists', 'user not exists', {})
        return HttpResponse(body)

    body = response('ok', 'update profile success', {
        'user': user_model_to_dict(user_model)
    })
    return HttpResponse(body)


def interest_tags_view(request):
    if request.method == 'POST':
        return update_interest_tags(request)
    elif request.method == 'GET':
        return get_interest_tags(request)
    return HttpResponseBadRequest()


def update_interest_tags(request):
    try:
        zhinput.all_exists(request.POST, (
            'user_id', 'interest_tags'
        ))
    except zhinput.ZHInputKeyNotExist as e:
        body = response(e.key + ':not_exists', e.key + ' not exists', {})
        return HttpResponse(body)

    user_id = zhinput.as_string(request.POST, 'user_id')

    try:
        user_model = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist as e:
        body = response(e.key + ':not_exists', e.key + ' not exists', {})
        return HttpResponse(body)

    try:
        interest_tags = zhinput.as_json(request.POST, 'interest_tags')
    except zhinput.ZHInputNotJSONString as e:
        body = response(e.key + ':not_exists', e.key + ' not exists', {})
        return HttpResponse(body)

    # update interest_tags
    for tag in interest_tags:
        try:
            interest_tag_model = models.InterestTag.objects.get(pk=tag['id'])

            try:
                user_interest_tag_model = models.UserInterestTag.objects.get(tag=interest_tag_model)
                # update one
                try:
                    interest_tag_content_model = models.InterestTagContent.objects.get(pk=tag['content_id'])
                except models.InterestTagContent.DoesNotExist:
                    continue
                user_interest_tag_model['content'] = interest_tag_content_model
                user_interest_tag_model.save()
            except models.UserInterestTag.DoesNotExist:
                # tag not exists, then insert new one
                new_user_interest_tag_model = models.UserInterestTag(
                    user=user_model,
                    tag=interest_tag_model,
                    content=tag['content_id']
                )
                new_user_interest_tag_model.save()

                # insert new bill
                bill = models.EnergyStoneBill(
                    user=user_model,
                    amonut=5,
                    create_time=int(time.time()),
                    info=models.EnergyStoneBill.COMPLETE_PROFILE_EARN,
                    detail=str(tag['id']) + ':' + str(tag['content_id'])
                )
                bill.save()
        except models.InterestTag.DoesNotExist:
            pass


def get_all_user_message(request):
    user_id = request.GET.get('user_id', '')
    try:
        user_model = models.User.objects.get(pk=user_id)
        message = models.Message.objects.filter(
            user=user_model
        )
        result = []
        for msg in message:
            result.append(model_to_dict(msg))
    except models.User.DoesNotExist:
        body = response('user:not_exists', 'user not exists', {})
        return HttpResponse(body)

    body = response('ok', 'get message success', {
        'messages': result
    })
    return HttpResponse(body)


def today_ts_range():
    now_ts = time.time()
    now = time.localtime(now_ts)
    start = time.struct_time((
        now.tm_year,
        now.tm_mon,
        now.tm_mday,
        0, 0, 0, 0, 0,
        now.tm_isdst
    ))
    start_ts = time.mktime(start)
    return (start_ts, start_ts + 86400)


def get_today_user(request):
    try:
        zhinput.all_exists(request.GET, ('user_id', ))
        user_id = zhinput.as_int(request.GET, 'user_id')
    except zhinput.ZHInputNotInt as e:
        body = response(e.key + ':not_int', e.key + 'is not int', {})
        return HttpResponse(body)
    except zhinput.ZHInputKeyNotExist as e:
        body = response(e.key + ':not_exists', 'user_id missing', {})
        return HttpResponse(body)

    try:
        user_model = models.User.objects.get(pk=user_id)
        today_range = today_ts_range()
        today_user_cursor = models.TodayUser.objects.filter(
            user=user_model,
            create_time__gt=today_range[0],
            create_time__lt=today_range[1]
        ).order_by('-create_time')
        neweast = today_user_cursor[0]
        target_user_model = neweast.other
    except models.User.DoesNotExist:
        body = response('user:not_exists', 'user not exists', {})
        return HttpResponse(body)
    except IndexError:
        body = response('user:no_recommended', 'no new user recommended now', {})
        return HttpResponse(body)

    body = response('ok', 'get recommand user success', {
        'user': user_model_to_dict(target_user_model)
    })
    return HttpResponse(body)


class UploadFileForm(forms.Form):
    filename = forms.CharField(max_length=128)
    file = forms.FileField()


def upload_avatar(request):
    try:
        filename = zhinput.as_string(request.POST, 'filename', min_length=1)
        abspath = os.path.abspath(os.path.join(config.AVATAR_FOLDER, filename))

        with open(abspath, 'wb+') as f:
            for chunk in request.FILES['file'].chunks():
                f.write(chunk)
    except zhinput.ZHInputStringTooShort as e:
        body = response(e.key + ':empty', e.key + 'should not be empty', {})
        return HttpResponse(body)
    except Exception as e:
        print(e)
        body = response('avatar:save_failed', 'save avatar failed', {})
        return HttpResponse(body)

    body = response('ok', 'save avatar success', {})
    return HttpResponse(body)


def get_all_interest_tags(request):
    interest_tag_cursor = models.InterestTag.objects.all()

    tags = []
    for interest_tag_model in interest_tag_cursor:
        interest_tag_content_cursor = models.InterestTagContent.objects.filter(
            tag=interest_tag_model
        )
        contents = []
        for content_model in interest_tag_content_cursor:
            contents.append(model_to_dict(content_model))
        tdict = model_to_dict(interest_tag_model)
        tdict['contents'] = contents
        tags.append(tdict)

    body = response('ok', 'get all interest tags', {
        'tags': tags
    })
    return HttpResponse(body)


def get_interest_tags(request):
    try:
        zhinput.all_exists(request.GET, ('user_id', ))
        user_id = zhinput.as_string(request.GET, 'user_id')
    except zhinput.ZHInputKeyNotExist as e:
        body = response(e.key + ':not_exists', e.key + ' missing', {})
        return HttpResponse(body)

    try:
        user_model = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        body = response('user:not_exists', 'user not exists', {})
        return HttpResponse(body)

    user_interest_cursor = models.UserInterestTag.objects.filter(
        user=user_model
    )

    result = []
    for interest_tag in user_interest_cursor:
        tdict = model_to_dict(interest_tag)
        tdict['tag'] = model_to_dict(interest_tag.tag)
        tdict['content'] = model_to_dict(interest_tag.content)
        result.append(tdict)

    body = response('ok', 'get interest tag success', {
        'tags': result
    })
    return HttpResponse(body)

# 新加的方法
from django.shortcuts import render,render_to_response
def UserSignUp(request):
    return render(request,'addUser.html')

def phone(request):
    return render(request,'phone.html')
