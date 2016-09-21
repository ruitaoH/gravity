# gravity
## repsonse body
```
{
    "error": "error hint",
    "msg": "xxx",
    "data": {
        "provinces": []
    }
}
```

## 域名
开发环境 `devgravity.zhihaojun.com` -> 121.42.201.80
http访问端口 56341
https访问端口 56342 还未开放
`还未开放`生产环境 `gravity.zhihaojun.com` -> 121.42.201.80
http访问端口 56341
https访问端口 56342 还未开放

```
推荐使用dnspod的d+服务手动把域名转成ip地址，这样连接的成功率会高一些
```
D+ [https://www.dnspod.cn/httpdns](https://www.dnspod.cn/httpdns)

## 流程
### 注册
signup_sms -> verify_phone -> signup

### 重置密码
password_sms -> verify_phone -> password

## 接口返回
接口的统一返回格式为json

```
{
    "error": "<error>",
    "msg": "<msg>",
    "data": {

    }
}
```

* error 这个字段代表错误，如果没有错误则为`ok`
 ```
 error错误表示法
 <key>:<error_type>表示key数据发生了错误
 例如
 user:not_exists表示用户不存在
 phone:not_int表示手机号不是数字
 phone:exists表示手机已经存在

 ```
* msg 中为友好的提示，作为调试的可视化信息，不应该作为判断是否成功的标准
* data 在有数据的返回中保存了数据，是一个字典，如果没有数据返回则为空字典

## apis
```
### POST /backend/api/user/signup_sms 发送注册短信 √
* phone 手机号 11位数字

```
成功结果
{
    "msg": "send sms success",
    "data": {},
    "error": "ok"
}

用户已经存在时
{
    "msg": "user exists",
    "data": {"phone": "<phone>"},
    "error": "phone:exists"
}
```

### POST /backend/api/user/password_sms 重置密码短信 √
* phone 手机号 11位数字

```
成功时
{
    "msg": "send sms success",
    "data": {},
    "error": "ok"
}

用户不存在时
{
    "msg": "user not exists",
    "data": {"phone": "18327645626"},
    "error": "phone:not_exists"
}
```

### POST /backend/api/user/verify_phone 验证手机 √
* phone 手机号 11位数字
* code 验证码 4位数字
* type 类型 字符串 只能是`password - 重置密码 signup - 注册`

```
验证注册发的请求
phone=<phone>&code=<code>&type=signup

验证成功时
{
    "msg": "verify success",
    "data": {},
    "error": "ok"
}

验证失败时
{
    "msg": "verify failed",
    "data": {},
    "error": "verify:failed"
}
```

### POST /backend/api/user/signup 注册
* nickname 昵称
* phone 手机号 11位手机号
* password 密码 字符串
* verify_location_long 认证地点经度 浮点数
* verify_location_lat 认证地点经度 浮点数
* avatar 头像 头像名字 非必须
* gender 性别 固定字符串 `male - 男 female - 女`
* birthday 生日 整数 表示生日的时间戳
* clazz 班级 字符串 如 `计算机科学与技术 计算机科学与技术 ACM1301`
* block_same_class 固定字符串 `true或者false`
* hometown 家乡 `湖北 武汉`
* love_status 情感状态 固定字符串 `signle - 单身`
* prefer_gender 性取向 固定字符串 `male - 男 female - 女 both - 双性恋`
* contact 联系方式 字符串
* interest_tags 可选 json的字符串 `[{"id":"xxx", "content_id":"xxx"}, {"id":"xxx", "content_id":"xxx"}]`
* introduction 可选 自我介绍
* region 校区 目前三种取值 west - 西校区 middle - 中间 east - 东校区

```
注册成功时

{
    "msg": "signup success",
    "data": {
        "user": {
            "prefer_gender": "female",
            "hometown": "\u6e56\u5317 \u6b66\u6c49",
            "verify_location_long": 30.0,
            "id": 3,
            "signin_ip": "",
            "introduction": "",
            "clazz": "\u8ba1\u7b97\u673a\u79d1\u5b66\u4e0e\u6280\u672fIS1501",
            "signup_ip": "127.0.0.1",
            "avatar_url": "a",
            "contact": "wechat",
            "love_status": "single",
            "block_same_class": true,
            "pw_salt": "2e9d538bbe76b06e364a919b82ac7cebf840b6eef5749a7ffb59d6b07008bf1f",
            "phone": "18702796776",
            "birthday": 1461322544,
            "password": "pbkdf2_sha256$24000$2e9d538bbe76b06e364a919b82ac7cebf840b6eef5749a7ffb59d6b07008bf1f$AcQL6QxvfJjnmqkN91wSjEmXVE0VGao9pHooLdxyFfo=",
            "nickname": "",
            "signup_ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36",
            "energy_stone": 10,
            "signin_time": 0,
            "gender": "",
            "verify_location_lat": 100.0,
            "signin_ua": "",
            "signup_time": 1461412771,
            "age": 0
        }
    },
    "error": "ok"
}
```

### POST /backend/api/user/signin 登陆
* phone 11位数字
* password 密码

### POST /backend/api/user/profile 更新资料
* user_id

### POST /backend/api/user/interests 更新兴趣标签
* user_id 用户id
* interest_tags 兴趣点json字符串

### GET /backend/api/user/interests 获取兴趣标签
* user_id 用户id

```
获取成功
tags是一个数组
chname为中文名
enname为英文名
最好以英文名作为if判断的条件
{
    msg: "get interest tag success",
    data: {
        tags: [
            {
                content: {
                    chname: "西一食堂",
                    tag: 2,
                    id: 1,
                    enname: "xiyi_canteen"
                },
                tag: {
                    chname: "饭堂",
                    id: 2,
                    enname: "canteen"
                },
                id: 1,
                user: 9
            }
        ]
    },
    error: "ok"
}
```

### GET /backend/api/misc/interests 获取所有的兴趣标签

```
获取成功时
{
    msg: "get all interest tags",
    data: {
        tags: [
            {
                chname: "饭堂",
                id: 2,
                enname: "canteen",
                contents: [
                    {
                        chname: "西一食堂",
                        tag: 2,
                        id: 1,
                        enname: "xiyi_canteen"
                    }
                ]
            }
        ]
    },
    error: "ok"
}
```

### POST /backend/api/user/password 更新密码
* phone
* code
* password

### POST /backend/api/user/position 报告地理位置
* user_id 用户id 整数
* longitude 经度 浮点数
* latitude 维度 浮点数
* altitude 高度 浮点数
* floor 楼层 整数
* horizontal_accuracy 水平误差 浮点数
* vertical_accuracy 垂直误差 浮点数
* speed 移动速度 浮点数
* heading 朝向 浮点数
* timestamp 时间戳 整数
* location_name 地点名称 字符串

```
请求成功时
{
    "msg": "report position success",
    "data": {},
    "error": "ok"
}
```

### GET /backend/api/user/messages 获取用户消息
* user_id 用户ID 整数


### GET /backend/api/misc/provinces 获取省份 √
```
请求成功时
{
    "msg": "get provinces success",
    "data": {
        "provinces": [
            {
                "id": 1,
                "name": "湖北"
            }
        ]
    },
    "error": "ok"
}
```

### GET /backend/api/misc/citys 获取城市 √
* province_id 省份id

```
请求成功时
{
    "msg": "get cities success",
    "data": {
        "cities": [
            {
                "province": 1,
                "id": 1,
                "name": "武汉"
            }
        ]
    },
    "error": "ok"
}
```

### GET /backend/api/misc/departments 获取学院 √
```
请求成功时
{
    "msg": "get departments success",
    "data": {
        "departments": [
            {
                "id": 1,
                "name": "计算机科学与技术"
            }
        ]
    },
    "error": "ok"
}
```

### GET /backend/api/misc/majors 获取专业 √
* department_id 学院id

```
获取成功时
{
  "msg": "get majors success",
  "data": {
    "majors": [
      {
        "department": 1,
        "id": 1,
        "name": "计算机科学与技术"
      }
    ]
  },
  "error": "ok"
}
```

### GET /backend/api/misc/classes 班级 √
* major_id 专业id

```
获取成功时
{
  "msg": "get classes success",
  "data": {
    "classes": [
      {
        "major": 1,
        "id": 1,
        "name": "ACM1301"
      }
    ]
  },
  "error": "ok"
}
```


### POST /backend/api/misc/avatar 上传头像
* filename 要保存的文件名 avatar-<user_id>-<timestamp>.<ext>
* file 上传的文件（二进制格式）

**注意form的类型需要是`multipart/form-data`**

发送的文件名作为文件的key，对应的是文件的内容

```
成功时返回
{
    "msg": "save avatar success",
    "data": {},
    "error": "ok"
}
```

### POST /backend/api/misc/device_token
* user_id 用户id
* device_token

```
成功时返回
{
    "msg": "post device token success",
    "data": {},
    "error": "ok"
}
```

保存的头像可以通过
http://img.devgravity.zhihaojun.com:56343/<filename>查看

### GET /backend/api/user/today 获取今天匹配的人
* user_id

返回的是用户表中的信息

## models
```
user
用户表
verify_location_long 认证地点经度 float
verify_location_lat 认证地点维度 float
avatar_url 头像url
phone 手机号
nickname 昵称
gender 性别 male - 男 female - 女
age 年龄
cls 班级 [学院] [专业] [班级]
class_id 班级id
block_same_class 屏蔽同班人 true/false
hometown 家乡 [省份] [城市]
city_id 所属城市
contact 联系方式
love_status 恋爱状态 single - 单身
prefer_gender 我想看 male - 男 female - 女 both - 男女
introduction 个性签名
energy_stone 能量石 default 0

password 密码
pw_salt 密码盐值

signup_time 注册时间
signup_ua 登陆设备
signup_ip 注册ip
signin_time 登陆时间
signin_ua 登陆设备
signin_ip 登陆ip

----
interest_tag
兴趣标签
name 标签名

----
user_interest_tag
用户兴趣标签关系表
user 用户id
interest_tag 兴趣标签id
content 内容

----
department
学院
name 学院名

----
major
专业
name 专业名

----
Clazz
班级
name 班级名

----
department_major
学院 专业 关系表
department
major

----
major_class
专业 班级 关系表
major
class

----
province
省份
name 省份名

----
city
城市
name 城市名

----
province_city
省份 城市 关系表
province
city
```
