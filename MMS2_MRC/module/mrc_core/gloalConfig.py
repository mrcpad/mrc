#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: v0.1
@author: xxf
@site: 
@software: PyCharm
@file: 输出全局变量配置
@time: 2019-7-26

2019-8-2更新，增加获取路径的静态方法

"""

import lib.getpath as gp
#import MRC as sp


class GloalConfig(object):


    @property
    def config(self):#config目录
        return self._config

    @config.setter
    def config(self,value):
        self._config=value

    @property
    def image(self):#config/image目录
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def data(self):#data目录
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def logs(self):#logs目录
        return self._logs

    @logs.setter
    def logs(self, value):
        self._logs = value

    @property
    def log(self):#logs/logs目录
        return self._log

    @log.setter
    def log(self, value):
        self._log = value

    @property
    def lib(self):  # lib目录
        return self._lib

    @lib.setter
    def lib(self, value):
        self._lib = value

    def __init__(self):
        p_path = gp.get_sys_path()  # 系统路径
        self.config=p_path + '/config'
        self.image=p_path + '/config/image'
        self.data = p_path + '/data'
        self.logs=p_path + '/logs'
        self.log=p_path + '/logs/logs'
        self.lib = p_path + '/lib'


#   2019-8-2更新，增加获取路径的静态方法

    @staticmethod
    def ConfigPath():
        '''
        配置文件路径   config/
        :return:
        '''
        p_path = gp.get_sys_path()  # 系统路径
        return p_path + '/config'

    @staticmethod
    def ImagePath():
        '''
        图标目录，config/image/
        :return:
        '''
        p_path = gp.get_sys_path()  # 系统路径
        return p_path + '/config/image'

    @staticmethod
    def DataPath():
        '''
        data/测试数据路径，本地测试数据，和业务无关
        :return:
        '''
        p_path = gp.get_sys_path()  # 系统路径
        return p_path + '/data'

    @staticmethod
    def LogsPath():
        '''
        logs/
        :return:
        '''
        p_path = gp.get_sys_path()  # 系统路径
        return p_path + '/logs'

    @staticmethod
    def LogPath():
        '''
        logs/logs
        :return:
        '''
        p_path = gp.get_sys_path()  # 系统路径
        return p_path + '/logs/logs'

    @staticmethod
    def LibPath():
        '''
        lib路径
        :return:
        '''
        p_path = gp.get_sys_path()  # 系统路径
        return p_path + '/lib'

    @staticmethod
    def LibNetPath():
        '''
        net动态库路径
        :return:
        '''
        p_path = gp.get_sys_path()  # 系统路径
        return p_path + '/lib/net'



#=======================================================================


