#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version:
@author:
@site:
@software: PyCharm
@file:
@time:
"""


from module.algorithm.grib.grib1_info import GRIB1Info


file=r'D:\PanoplyWin\grib.GRB'
# file=r'E:\Work\Hitec\MSZC\MSS2\05source\MRC\data\NAFP_ECMF_1_FTM-98-GLB-TEM-125X125-1-0-999998-999998-999998-2017092812-0.GRB'
# ds=xr.open_dataset(file,engine='cfgrib')
# print(ds)



grib_info=GRIB1Info(file)

s=grib_info.print_property_info()

#print(s)
print(grib_info.print_variable_property(None))

data=grib_info.get_data_by_name(38165271)
array=grib_info.system_double_2_array(data)
print(array)

