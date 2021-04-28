#!/usr/bin/env python
# !-*-coding:utf-8 -*-

# describe download data by api-url

'''
版本 ：v1.0.0
创建 ：xxf
更新内容 ：
一、api接口下载辅助类

版本 ：v1.0.1
更新 ：xxf at 2019/02/22 14:28
更新内容 ：
1、增加 下载文件方法api_file_download


版本 ：v1.0.2
更新 ：xxf at 2019/03/01 09:28
更新内容 ：去掉api_file_download方法中的日志
1、

'''


import urllib.request
import json
import json.decoder
import lib.getpath as gp
import ssl
import bz2
import shutil


# download data by api-url
def api_data_download(url):
    try:
        # 使用ssl创建未经验证的上下文，在urlopen中传入上下文参数
        context = ssl._create_unverified_context()
        request = urllib.request.urlopen(url=url, context=context)
        data = request.read().decode('utf-8')
        if data == "当前查询条件没有数据":
            return None
        datas = json.loads(data)
        if datas["success"] == True:
            return datas["datas"]
        else:
            return None
    except json.decoder.JSONDecodeError as jsonerr:  # 返回数据异常
        return None
    except urllib.request.HTTPError as httperr:  # 接口访问异常
        return None


def url_download(url):
    try:
        # 使用ssl创建未经验证的上下文，在urlopen中传入上下文参数
        context = ssl._create_unverified_context()
        request = urllib.request.urlopen(url=url, context=context)
        data = request.read().decode('utf-8')
        datas = json.loads(data)
        return datas
    except json.decoder.JSONDecodeError as jsonerr:  # 返回数据异常
        return None
    except urllib.request.HTTPError as httperr:  # 接口访问异常
        return None

def api_download(url):
    try:
        # 使用ssl创建未经验证的上下文，在urlopen中传入上下文参数
        context = ssl._create_unverified_context()
        request = urllib.request.urlopen(url=url, context=context)
        data = request.read().decode('utf-8')
        if data == "当前查询条件没有数据":
            return None
        datas = json.loads(data)
        return datas
    except json.decoder.JSONDecodeError as jsonerr:  # 返回数据异常

        return None
    except urllib.request.HTTPError as httperr:  # 接口访问异常
        return None


def api_file_download(url, filename):
    try:
        # 使用ssl创建未经验证的上下文，在urlopen中传入上下文参数
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(url=url, context=context) as request:
            data = request.read()
            with open(filename, 'wb') as f: #二进制写入
                f.write(data)
                #logger.info("Save File : " + filename)
                return True
    except json.decoder.JSONDecodeError as jsonerr:  # 返回数据异常
        return False
    except urllib.request.HTTPError as httperr:  # 接口访问异常
        return False

def api_file_download_unpack(url, filename):
    '''
    从指定url下载资源，并解压到指定路径
    :param url:
    :param filename:
    :return:
    '''
    try:
        # 使用ssl创建未经验证的上下文，在urlopen中传入上下文参数
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(url=url, context=context) as request:
            data = request.read()
            with open(filename, 'wb') as f: #二进制写入
                f.write(data)

            write_path=gp.combine_path_name(gp.get_path(filename),gp.filename_add_extension(filename,'bin'))

            with bz2.open(filename,'rb') as read,open(write_path,'wb') as write:
                shutil.copyfileobj(read,write)
                return True,write_path
    except json.decoder.JSONDecodeError as jsonerr:  # 返回数据异常
        return False,None
    except urllib.request.HTTPError as httperr:  # 接口访问异常
        return False,None