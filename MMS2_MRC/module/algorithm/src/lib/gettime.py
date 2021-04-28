# !-*-coding:utf-8 -*-


'''
版本 ：v1.0.0
创建 ：xxf
更新内容 ：
一、时间辅助类

'''

import datetime
import time
import uuid
import enum


@enum.unique
class TimeZone(enum.Enum):
    BJ = 0
    UTC = 1


# 字符串转时间格式
def strptime(d_datetime, formart="%Y-%m-%d %H:%M:%S"):
    dd_datetime = datetime.datetime.strptime(d_datetime, formart)
    return dd_datetime


def getnowtime(timeformat="%Y-%m-%d %H:%M:%S"):
    # 获取格式化当前时间
    nowtime = datetime.datetime.strftime(datetime.datetime.now(), timeformat)
    return nowtime


def getcurrenttime(timeformat="%Y-%m-%d %H:%M:%S"):
    # 获取格式化当前时间
    localtime = time.localtime(time.time())
    formartime = time.strftime(timeformat, localtime)
    return formartime


def formattime(time, format="%Y-%m-%d %H:%M:%S"):
    # 格式化指定时间 time:datetime.datetime
    timeformat = datetime.datetime.strftime(time, format)
    return timeformat


def getnowutctimestr(format="%Y-%m-%d %H:%M:%S"):
    # 当前时间的国际时
    timedelta = datetime.timedelta(hours=-8)
    utctime = datetime.datetime.now() + timedelta

    return formattime(utctime,format)

def getnowutctime():
    # 当前时间的国际时
    timedelta = datetime.timedelta(hours=-8)
    utctime = datetime.datetime.now() + timedelta
    return utctime

def getutctime(bjtime):
    # 北京时转国际时
    timedelta = datetime.timedelta(hours=-8)
    utctime = bjtime + timedelta
    return utctime


def getbjtime(utctime):
    # 国际时转北京时
    timedelta = datetime.timedelta(hours=8)
    bjtime = utctime + timedelta
    return bjtime


def getutctimestr(bjtime, format="%Y%m%d%H%M%S"):
    # 北京时转国际时
    timedelta = datetime.timedelta(hours=-8)
    utctime = bjtime + timedelta
    utcformattime = datetime.datetime.strftime(utctime, format)
    return utcformattime


def getbjtimestr(utctime, format="%Y%m%d%H%M%S"):
    # 国际时转北京时
    timedelta = datetime.timedelta(hours=8)
    bjtime = utctime + timedelta
    bjformattime = datetime.datetime.strftime(bjtime, format)
    return bjformattime


def addtime(sourcetime, intervalmin, timezone=TimeZone.UTC):
    '''
    sourcetime加上分钟时间间隔
    :param sourcetime:
    :param intervalmin:
    :param timezone:时区
    :return:
    '''
    timedelta = datetime.timedelta(minutes=intervalmin)
    outtime = sourcetime + timedelta
    if timezone == TimeZone.UTC:
        return outtime
    else:
        return getutctime(outtime)


def subtracttime(sourcetime, intervalmin, timezone=TimeZone.UTC):
    '''
    sourcetime减去分钟时间间隔
    :param sourcetime:
    :param intervalmin:
    :param timezone:时区
    :return:
    '''
    timedelta = datetime.timedelta(minutes=intervalmin)
    outtime = sourcetime - timedelta
    if timezone == TimeZone.UTC:
        return outtime
    else:
        return getutctime(outtime)

def addnowtime(intervalmin, timezone=TimeZone.UTC):
    '''
    sourcetime减去分钟时间间隔
    :param intervalmin:分钟间隔
    :param timezone:时区
    :return:
    '''
    timedelta = datetime.timedelta(minutes=intervalmin)
    outtime = datetime.datetime.now() + timedelta
    if timezone == TimeZone.UTC:
        return outtime
    else:
        return getutctime(outtime)

def subtractnowtime(intervalmin, timezone=TimeZone.UTC):
    '''
    sourcetime减去分钟时间间隔
    :param intervalmin:分钟间隔
    :param timezone:时区
    :return:
    '''
    timedelta = datetime.timedelta(minutes=intervalmin)
    outtime = datetime.datetime.now() - timedelta
    if timezone == TimeZone.UTC:
        return outtime
    else:
        return getutctime(outtime)



