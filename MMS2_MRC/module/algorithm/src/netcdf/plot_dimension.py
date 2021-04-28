#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: v1.0
@author: xxf
@site: 
@software: PyCharm
@file: 支持画图的维度类型
@time: 2019-8-2
"""



import enum


@enum.unique
class PlotDimension(enum.Enum):

    Lat_Lon=0
    Time_Lon=1
    Time_Lat=2
    Level_Lon=3
    Level_Lat=4
    Level_Time=5
    Time=6
    Level=7
    Lon=8
    Lat=9