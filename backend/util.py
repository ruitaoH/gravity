import random

# 格式化转换datetime
def getStrTime(datetime):
    return datetime.strftime('%Y-%m-%d %H:%M:%S')

def getMeetDistance():
    return random.randint(5,100)
