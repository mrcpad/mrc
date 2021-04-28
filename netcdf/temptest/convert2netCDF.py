#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: 
@author: 
@site: 
@software: PyCharm
@file: 
@time: 2019/7/2  HDF和NetCDF互转
"""

import lib.judgetype as jt
from lib.judgetype import ModelDataType
from netCDF4 import Dataset, Dimension, Variable, Group,OrderedDict

#from netcdf.hdf import HDF
#from netcdf.netcdf import Nc
from hdf import HDF
from netcdf import Nc
from numpy.ma import MaskedArray


def hdf2nc(sourcefile, savefile, format="NETCDF4"):
    """
    Dataset(self, filename, mode="r", clobber=True, diskless=False, persist=False, keepweakref=False, format='NETCDF4'):

    Default `'NETCDF4'`, which means the data isstored in an HDF5 file, using netCDF 4 API features.  Setting`format='NETCDF4_CLASSIC'` will create an HDF5 file, using only netCDF 3
    compatible API features


    :param sourcefile:
    :param savefile:
    :return:
    """
    hdf_type = jt.judge_model_data_type(sourcefile)
    print("HDF Convert To NetCDF!")
    # hdf_type=ncf.judge_nc_type(sourcefile)
    if hdf_type == ModelDataType.HDF:
        hdf = HDF(sourcefile)

        f = Dataset(savefile, 'w', format=format)

        if hdf.contains_group == True:  # 解析出来HDF包含组
            f.setncattr("IsContainsGroup", "True")  # 全局变量写入包含组信息，自定义的，用于netcdf转hdf时判断是否包含组  2019/7/9  by xxf
            for g in hdf.groups:  # 遍历组
                f = set_dims(hdf.groups[g].dimensions, f)  # 设置每个组的dimensions和variables
                f = set_vars(hdf.groups[g].variables, f, g)
        else:
            f = set_dims(hdf.dimensions, f)
            f = set_vars(hdf.variables, f)

        # 设置全局变量信息
        for g_attr in hdf.dataset.ncattrs():
            f.setncattr(g_attr, hdf.dataset.getncattr(g_attr))
        f.close()
        print("Convert Success!")
        print("out put : " + savefile)

    else:
        print("please choose hdf type file!")


def nc2hdf(sourcefile, savefile, format="NETCDF4"):
    '''
    NetCDF转HDF
    :param sourcefile:
    :param savefile:
    :param format:
    :return:
    '''
    nc_type = jt.judge_model_data_type(sourcefile)

    print("NetCDF Convert To HDF!")
    if nc_type == ModelDataType.NETCDF:
        nc = Nc(sourcefile)

        f = Dataset(savefile, 'w', format=format)

        # 全局属性包含IsContainsGroup，自定义的，用于netcdf转hdf时判断是否包含组
        l = nc.dataset.ncattrs()
        if "IsContainsGroup" in nc.dataset.ncattrs():
            is_contains_group = nc.dataset.getncattr("IsContainsGroup")
            if is_contains_group == "True":
                f = set_group(nc.variables, f)  # 设置group信息
        else:
            f = set_dims(nc.dimensions, f)
            f = set_vars(nc.variables, f)

        # 设置全局变量信息
        for g_attr in nc.dataset.ncattrs():
            f.setncattr(g_attr, nc.dataset.getncattr(g_attr))
        f.close()
        print("Convert Success!")
        print("out put : " + savefile)

    else:
        print("please choose hdf type file!")


def set_group(variables, dataset):
    '''
    set groups for dataset use dimensions and variables
    :param variables:
    :param dataset:
    :return:
    '''
    if not isinstance(dataset, Dataset):
        return None

    groups = []
    for v in variables:
        var = variables[v]
        if isinstance(var, Variable):
            group_name = var.getncattr("group_name")
            if group_name not in groups:
                groups.append(group_name)
    if len(groups) == 0:
        return None
    for group_name in groups:
        group = dataset.createGroup(group_name)
        if isinstance(group, Group):
            group = set_group_dim_var(group, variables)

        # group.close()

    return dataset


def set_group_dim_var(group, variables):
    '''
    设置 HDF  group ，设置group里的Variable和dimensions
    :param group:
    :param variables:
    :return:
    '''
    if isinstance(variables, OrderedDict):
        def filter_l(data):  # 筛选属性 group_name=group.name
            return {k: v for k, v in data.items() if v.getncattr("group_name") == group.name}

        group_vars = filter_l(variables)  # 筛选的组名是group.name的variables

        # group_vars 中获取维度信息
        for v in group_vars:
            var = group_vars[v]
            if isinstance(var, Variable):
                dims = var.get_dims()  # 获取Variable的Dimension信息
                for i in range(len(dims)):
                    dim = dims[i]
                    if not group.dimensions.has_key(dim.name):  # 去重
                        group.createDimension(dim.name, dim.size)

        group = set_vars(group_vars, group)  # 设置Variable

        return group


def set_dims(dimensions, dataset):
    '''
    set NetCDF Dimensions use HDF Dimension to create NetCDF Dimension by Dataset.createDimension()
    :param dimensions:
    :param dataset:
    :return:
    '''

    for d in dimensions:  # 解析出来HDF不包含组，遍历dimensions  type: orderdict
        dim = dimensions[d]
        if isinstance(dim, Dimension):  # 类型判断
            dataset.createDimension(dim.name, dim.size)  # 内置方法创建维度
    return dataset


def set_vars(variables, dataset, group_name=None):
    '''
    set NetCDF Variables
    use dataset.createVariable(),set Variable's attr and create MaskedArray
    :param hdf:
    :param dataset:
    :return:
    '''
    #print(variables['time'][:])
    for v in variables:  # 遍历variables   type: orderdict
        var = variables[v]
        if isinstance(var, Variable):
            create_var = dataset.createVariable(varname=var.name, datatype=var.datatype, dimensions=var.dimensions,
                                                endian=var.endian(), chunksizes=None)  # 内置方法创建变量
            # 设置属性信息
            for attr in var.ncattrs():  # 遍历属性信息    type:list
                if isinstance(create_var, Variable):
                    create_var.setncattr(attr, var.getncattr(attr))  # 设置属性

            # 设置组信息
            if group_name != None:
                create_var.setncattr("group_name", group_name)  # 设置属性,自定义的信息

            var_data = var[::]  # 数据信息
            if isinstance(var_data, MaskedArray):
                fill_value = var_data.get_fill_value()  # Return the filling value of the masked array
                data = var_data.data  # Return the current data, as a view of the original underlying data
                # MaskedArray对象
                maskedArray = MaskedArray(data, dtype=var_data.dtype, fill_value=fill_value)
                create_var[::] = maskedArray  # 变量数据赋值
                # data2=create_var[::]
            else:
                create_var[::] = var[::]
    return dataset


if __name__ == "__main__":
    sourcefile = r'/home/trywangdao/test_mrc/nc/20190924060623.nc'
    savefile = r'/home/trywangdao/test_mrc/nc2hdf/20190924060623wwwww.hdf'
    sourcefile1 = r'/home/ynairport/MrWang/pyclick/mrcproject/data/gen/hdf/20190820131420.m4_to_hdf'
    savefile1 = r'/home/ynairport/MrWang/pyclick/mrcproject/data/gen/hdf/20190813145426.nc'
    #nc2hdf(sourcefile, savefile)
    import os
    if os.path.exists(sourcefile):
        #nc = Dataset(sourcefile)
        #print nc.variables.keys()
        nc2hdf(sourcefile, savefile)
        #hdf2nc(sourcefile1, savefile1)
