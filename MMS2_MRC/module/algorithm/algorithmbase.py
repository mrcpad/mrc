#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: 
@author: xxf
@site: 
@software: PyCharm
@file: 所有解码算法基类，提供打印属性信息，获取变量信息扥方法
@time: 2019-7-31
"""
from module.algorithm.meteoinfoc.plot_dimension import PlotDimension


class PyMeteoDataInfo(object):


    @property
    def dimensionSet(self):
        return self._dimensionSet

    @dimensionSet.setter
    def dimensionSet(self,value):
        self._dimensionSet=None if isinstance(value,PlotDimension) else value





    def print_property_info(self):
        '''
        打印属性信息
        :return:
        '''
        pass


    def get_variable_by_name(self,name,**kwargs):
        '''
        查询变量信息
        :return:
        '''
        pass

    def get_dimension_by_name(self,name,**kwargs):
        '''
        查询维度信息
        :return:
        '''
        pass


    def print_variable_property(self, name, var=None,**kwargs):
        '''
        打印变量属性信息
        :param name:变量名称
        :param var:
        :return:
        '''
        pass

    def print_dimension_property(self, name, var=None,**kwargs):
        '''
        打印维度属性信息
        :param name:维度名称
        :param var:
        :return:
        '''
        pass

    def get_variables_data(self):
        pass


    def get_data_by_name(self,name,**kwargs):
        '''
        获取数据
        :return:
        '''
        pass

    def get_messages(self):
        '''
        GRIB 数据 获取所有messages，用于左侧列表展示
        :return:

        '''
        pass

    def get_message(self,messagePos):
        '''
        GRIB 数据 获取所有messages，用于左侧列表展示
        :return:

        '''
        pass



class PyMeteoObject(object):

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        self._file = value

    @property
    def fileName(self):
        return self._fileName

    @fileName.setter
    def fileName(self,value):
        self._fileName=value



    @property
    def modelDataType(self):
        '''
        数据类型
        :return:
        '''
        return self._modelDataType

    @modelDataType.setter
    def modelDataType(self, value):
        self._modelDataType = value

    @property
    def meteoDataInfo(self):
        return self._meteoDataInfo

    @meteoDataInfo.setter
    def meteoDataInfo(self, value):
        self._meteoDataInfo =value if isinstance(value,PyMeteoDataInfo) else None


    def __init__(self):
        pass