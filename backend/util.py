import random
import time

# 格式化转换datetime
def getStrTime(datetime):
    return datetime.strftime('%Y-%m-%d %H:%M:%S')

def timestamp2Str(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(timestamp))

def getMeetDistance():
    return random.randint(5,100)
