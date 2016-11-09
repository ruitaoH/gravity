import random
import time

# 格式化转换datetime ---> 精确到毫秒
def getStrTime(datetime):
    return datetime.strftime('%Y-%m-%d %H:%M:%S %f')

def timestamp2Str(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(timestamp)) + ' ' + str(int((timestamp * 1000000) % 1000000))

def getMeetDistance():
    return random.randint(5,100)
