#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: 
@author: xxf
@site: 
@software: PyCharm
@file: 
@time: 2019-7-4

Judge Data Type

"""

import enum
import lib.getpath as gp
#judgetype.py

def judge_model_data_type(filename):
    extension=gp.get_extension(filename).lower()#小写
    if 'hdf' in extension:
        return ModelDataType.HDF
    elif 'nc' in extension:
        return ModelDataType.NETCDF
    elif 'grib' in extension or 'grb' in extension:
        return ModelDataType.GRIB
    elif '000' in extension or 'txt' in extension:
        return ModelDataType.MICAPS4


@enum.unique
class ModelDataType(enum.Enum):
    GRIB=0
    NETCDF=1
    HDF=2
    MICAPS4=3








