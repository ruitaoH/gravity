import random
import time
from datetime import datetime

# 格式化转换datetime ---> 精确到毫秒
def getStrTime(datetime):
    return datetime.strftime('%Y-%m-%d %H:%M:%S %f')

def timestamp2Str(timestamp):
    return getStrTime(datetime.fromtimestamp(timestamp))

def getMeetDistance():
    return random.randint(5,100)
