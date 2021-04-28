#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: v0.1
@author: xxf
@site:
@software: PyCharm
@file: GRIB数据解码类
@time: 2019-8-2
"""


import lib.array as ay
from module.algorithm.algorithmbase import PyMeteoDataInfo
import clr

import sys
from module.mrc_core.gloalConfig import GloalConfig
net_path=GloalConfig.LibNetPath()
#net_path=r'E:\Work\Hitec\MSZC\MSS2\05source\Code\MMS2_MRC\lib\net'
sys.path.append(net_path)#导入.net动态库路径
clr.AddReference('System.Collections')
clr.AddReference('System.IO')
clr.AddReference('MeteoInfoC')#导入MeteoInfoC.dll
clr.AddReference('Hitec.DataParse')#导入解析dll
#clr.AddReference('nwfd-grib2-win32')
from MeteoInfoC.Data.MeteoData import *
from Hitec.DataParse import *

from module.algorithm.algorithmbase import PyMeteoDataInfo


class GRIB1Info(PyMeteoDataInfo):


    def __init__(self,file_path):
        meteo =MeteoDataInfo()#实例化Hitec.DataParse.MeteoDataInfo类
        meteo.OpenGRIBData(file_path)#打开个点数据

        self.meteo=meteo


    def get_message(self,messagePos):
        '''
        根据获取message，展示数据
        :return:

        '''
        message=self.meteo.GetMessageIdx_GRIB1()

        return message

    def get_messages(self):
        '''
        获取所有messages，用于左侧列表展示
        :return:
        '''
        messages=self.meteo.GetMessageIdx_GRIB1()
        return [messages]

    def print_property_info(self):
        info=self.meteo.PrintPropertyInfo_GRIB1()
        return info

    def print_variable_property(self, name, var=None,**kwargs):
        '''
        Get MessageInfo
        :param name:
        :param var:
        :param kwargs:
        :return:
        '''
        #message=self.meteo.GetMessageIdx(var)

        info=self.meteo.PrintMessageInfo_GRIB1()

        return info


    def get_data_by_name(self,name,**kwargs):
        '''

        :param name:
        :param kwargs:
        :return:
        '''

        data=self.meteo.GetGridDataByMessage_GRIB1()

        return data


    def system_double_2_array(self,grid_data):
        '''
        将C#的二维数组转成python array
        :param grid_data:
        :return:
        '''

        array=ay.zeros(grid_data.YNum,grid_data.XNum)

        for i in range(grid_data.YNum):
            for j in range(grid_data.XNum):
                array[i][j]=grid_data.Data[i,j]


        return array