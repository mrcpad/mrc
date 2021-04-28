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


from module.algorithm.grib.grib2_info import GRIB2Info
from module.mrc_core.gloalConfig import GloalConfig

file=r'D:\PanoplyWin\gef.gra.grb2'
# file=r'E:\Work\Hitec\MSZC\MSS2\05source\MRC\data\NAFP_ECMF_1_FTM-98-GLB-TEM-125X125-1-0-999998-999998-999998-2017092812-0.GRB'
# ds=xr.open_dataset(file,engine='cfgrib')
# print(ds)



grib_info=GRIB2Info(file,GloalConfig.LibNetPath()+'/grib2Parameters.xml')

s = grib_info.print_property_info()
print(s)

#print(s)
#print(grib_info.print_variable_property(None,38165271))

data=grib_info.get_data_by_name(1071)
array=grib_info.system_double_2_array(data)
print(array)

# meteo = MeteoDataInfo()
# o=meteo.OpenGRIBData(file)
# for var_name in meteo.DataInfo.VariableNames:
#     grid_data=meteo.GetGridData(var_name)

# array=ay.zeros(grid_data.YNum,grid_data.XNum)
#
# for i in range(grid_data.YNum):
#     for j in range(grid_data.XNum):
#         array[i][j]=grid_data.Data[i,j]
#
# print(array)

