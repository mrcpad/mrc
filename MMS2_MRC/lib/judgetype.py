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

# 数据后缀
netCDF_extension = ["nc", "cdf", "netcdf", "nc3", "nc4"]
hdf_extension = ["hdf", "hd"]
micaps_extension = ["000", "003", "006", "009", "012", "015", "018", "021", "024", "027", "030", "033", "036", "039",
                    "042", "045", "048", "051", "054", "057", "060", "063", "066", "069", "072", "078", "084", "090",
                    "096", "102", "108", "114", "120", "126", "132", "138", "144", "150", "162", "168", "174", "180",
                    "186", "192", "198", "204", "210", "216", "222", "234", "240"]
grib_extension = ["gr", "gr1", "grb", "grib", "grb1", "grib1", "gr2", "grib2", "grb2"]
txt_extension = ['txt', 'ini', 'conf', 'md']

def judge_model_data_type(filename):
    extension = gp.get_extension(filename).lower()  # 小写
    if extension in hdf_extension:
        return ModelDataType.HDF
    elif extension in netCDF_extension:
        return ModelDataType.NETCDF
    elif extension in grib_extension:
        return ModelDataType.GRIB
    #elif extension in micaps_extension:
    elif extension.isdigit() and len(extension) in [3, 4]:
        return ModelDataType.MICAPS4
    elif extension in txt_extension:
        return ModelDataType.TXT

    else:
        return ModelDataType.NoTYPE


@enum.unique
class ModelDataType(enum.Enum):
    GRIB = 0
    NETCDF = 1
    HDF = 2
    MICAPS4 = 3
    TXT = 4
    NoTYPE = 9
