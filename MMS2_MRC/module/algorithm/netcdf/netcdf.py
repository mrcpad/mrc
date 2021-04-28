#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: 
@author: 
@site: 
@software: PyCharm
@file: 
@time: 2019/05/16
"""

# !/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: 
@author: 
@site: 
@software: PyCharm
@file: 
@time: 

@update:
1.创建Nc类，封装netCDF4数据集合一些扩展方法  2019/05/15
2.增加属性信息输出，支持全部属性和单个变量属性  2019/05/17
3.整理扩展方法 Method  get data array     2019/05/20
4.增加 __get_attr_by_default_fillvals__ ，解决输出信息部分乱码的问题  2019/05/24

"""

import sys
#sys.path.append(r'E:\Work\Hitec\MSZC\MSS2\05source\MMS2_MRC')

import enum
from netCDF4 import Dataset, Variable, Dimension, num2date
import lib.getpath as gp
from module.algorithm.algorithmbase import PyMeteoDataInfo


# reload(sys)
# 设置编码
# sys.setdefaultencoding('utf8')


class Nc(PyMeteoDataInfo):
    default_fillvals = {
        'S1': u'�',
        'f4': 9.969209968386869e+36,
        'f8': 9.969209968386869e+36,
        'i1': -127,
        'i2': -32767,
        'i4': -2147483647,
        'i8': -9223372036854775806,
        'u1': 255,
        'u2': 65535,
        'u4': 4294967295,
        'u8': 18446744073709551614,
    }

    '''
    NetCDF property,contains  dimensions,variables and public property
    one nc file create on Nc class
    '''

    # property
    @property
    def file_name(self):  # 文件名
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @property
    def file_path(self):  # 数据源路径
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        self._file_path = value

    @property
    def file_format(self):  # 数据格式
        return self._file_format

    @file_format.setter
    def file_format(self, value):
        self._file_format = value

    @property
    def dataset(self):
        '''
        数据集，继承netCDF Dataset 类
        由Nc_Dataset对象创建
        :return:
        '''
        return self._dataset

    @dataset.setter
    def dataset(self, value):
        self._dataset = value if isinstance(value, Dataset) else None

    @property
    def dimensions(self):
        '''
        维度，内容为self.dataset.dimensions
        :return:
        '''
        return self._dimensions

    @dimensions.setter
    def dimensions(self, value):
        self._dimensions = value

    @property
    def variables(self):
        '''
        变量，内容为self.dataset.variables
        :return:
        '''
        return self._variables

    @variables.setter
    def variables(self, value):
        self._variables = value

    @property
    def dim_variable(self):
        '''
        维度基本属性
        OrderedDict类型，存储self.dataset的维度名称和维度对应的变量
        key:dimension name;
        value:variable
        '''
        return self._dim_variable

    @dim_variable.setter
    def dim_variable(self, value):
        self._dim_variable = value if isinstance(value, dict) else None

    @property
    def var_variable(self):
        '''
        变量基本属性
        OrderedDict类型，存储self.dataset的要素名称和要素对应的变量
        key:variable name;
        value:variable
        '''
        return self._var_variable

    @var_variable.setter
    def var_variable(self, value):
        self._var_variable = value if isinstance(value, dict) else None

    @property
    def variables_data_orderDict(self):
        '''
        变量基本属性
        OrderedDict类型，存储有顺序的array数据
        key:variable name;
        value:OrderedDict  key:time,value:array
        '''
        return self._variables_data_orderDict

    @variables_data_orderDict.setter
    def variables_data_orderDict(self, value):
        self._variables_data_orderDict = value if isinstance(value, dict) else None

    # init
    def __init__(self, filename):
        # super(Nc, self).__init__(filename, mode, clobber, diskless, persist, keepweakref, format)
        dataset = Dataset(filename)
        if dataset == None:
            print("Set Dataset Error")
            return
        self.dataset = dataset

        # 基础信息
        self.file_path = filename
        self.file_name = gp.get_filename(self.file_path)
        self.file_format = self.dataset.disk_format

        self.variables = self.dataset.variables
        self.dimensions = self.dataset.dimensions
        self.dim_variable, self.var_variable = self.__get_dim_var_variables()
        #self.variables_data_orderDict = self.__get_variables_data()
        self.close()

    # Method

    def close(self):
        self.dataset.close()

    # get variable and dimension
    def get_variable_data_type(self, name):
        '''
        根据变量名，获取变量数据类型，一维数组（1D)，二维数组(Geo2D)
        :param name:
        :return:
        '''
        if self.dim_variable.has_key(name):
            return Var_Type.D
        elif self.var_variable.has_key(name):
            return Var_Type.Geo

    def __get_dim_var_variables(self):
        '''
        :return dimension's variables and feature's variables
        :return:
        '''
        dim_variables = dict()
        var_variables = dict()
        for v_name in self.variables.keys():
            if v_name in self.dimensions.keys():
                dim_variables[v_name] = self.variables[v_name]
            else:
                var_variables[v_name] = self.variables[v_name]
        return dim_variables, var_variables

    # get variable and dimension attribute string info
    def get_nc_variable_title_str(self, variable_name, var="Variable "):
        '''
        创建variable描述标题
        :param variable_name:
        :return:
        '''

        return var + variable_name

    def get_nc_dim_dimension_str(self, name):
        '''
        根据维度名称获取维度信息，输出描述信息
        :param name:
        :return:
        '''
        dim = self.get_dimension_by_name(name)
        if dim == None:
            return ''
        describe = dim.name + " = " + str(dim.size) + ";\n"
        return describe

    def get_nc_dim_variable_str(self, name, var=None):
        '''
        根据维度名称获取维度变量信息，输出描述信息
        :param name:
        :return:
        '''
        if var == None:
            var = self.get_variable_by_name(name)
        if var == None:
            return ''
        datatype_name = "" if var.datatype.name == None else var.datatype.name

        describe = datatype_name + " " + name + "(" + name + "=" + str(var.size) + ");\n"
        # variables 全局变量
        for ncattr in var.ncattrs():
            attr = self.__get_attr_by_default_fillvals__(var.getncattr(ncattr))
            describe += "            " + ncattr + " = " + attr + ";\n"

        return describe

    def get_nc_var_variable_str(self, name, var=None):
        '''
        单个变量的描述信息
        :param name:
        :return:
        '''
        if var == None:
            var = self.get_variable_by_name(name)

        if var == None:
            return ''

        # title=self.__get_nc_variable_title_str(name)
        describe = ""

        datatype_name = "" if var.datatype.name == None else var.datatype.name
        describe += datatype_name + " " + name + "("

        for d in self.dimensions.keys():
            dim = self.dimensions[d]
            describe += dim.name + "=" + str(dim.size) + ","

        describe = describe[:len(describe) - 1]
        describe += ");\n"
        # variables 全局变量
        for ncattr in var.ncattrs():
            attr = self.__get_attr_by_default_fillvals__(var.getncattr(ncattr))
            # attr_type= type(attr)
            describe += "            " + str(ncattr) + " = " + str(attr) + ";\n"

        return describe

    def get_nc_attr_str(self):
        '''
        dataset 全局属性信息
        :return:
        '''
        describe = ""
        for attr in self.dataset.ncattrs():
            a = self.__get_attr_by_default_fillvals__(self.dataset.getncattr(attr))
            describe += "    " + str(attr) + " = " + str(a) + "\n"

        return describe

    def get_nc_attribute_str(self):
        '''
        输出元信息，基本属性，全局变量信息
        :return: 字符串
        '''
        out = ""
        try:
            out += "File " + self.file_name + "\n"
            out += "File Type " + self.file_format + "\n"
            out += "--------------------------------------------------------------------------------------------\n"
            out += "netcdf file: /" + self.file_path + "\n"
            out += "{\n"
            if len(self.dim_variable) > 0:
                out += "    dimensions:\n"
                for d_name in self.dimensions.keys():
                    out += "        " + self.get_nc_dim_dimension_str(d_name)

            if len(self.var_variable) > 0:
                out += "    variables:\n"
                # 先描述维度信息
                for v_name in self.dim_variable.keys():
                    out += "        " + self.get_nc_dim_variable_str(v_name)
                    out += "\n"

                # 在描述属性变量
                for v_name in self.var_variable.keys():
                    out += "        " + self.get_nc_var_variable_str(v_name)
                    out += "\n"

            # dataset全局属性
            if (len(self.dataset.ncattrs()) > 0):
                out += "    //global attributes:\n"
                out += self.get_nc_attr_str()

            out += "}"

            self.attribute_text = out

        except Exception as e:
            # print e
            self.attribute_text = ''
        return out

    # get variables by attributes
    def get_nc_variables_by_attributes(self, axis='T'):
        '''
        """
        Returns a list of variables that match specific conditions.

        :::python
            # Get Axis variables
            vs = nc.get_variables_by_attributes(axis=lambda v: v in ['X', 'Y', 'Z', 'T'])
            # Get variables that don't have an "axis" attribute
            vs = nc.get_variables_by_attributes(axis=lambda v: v is None)

        """
        :param axis:
        :return:
        '''
        return self.dataset.get_variables_by_attributes(axis=axis)

    def get_nc_variables_x_by_attributes(self, axis='X'):
        '''
        """
        Returns a list of variables that axis='X'

        """
        :param axis:
        :return:
        '''
        variables_list = self.dataset.get_variables_by_attributes(axis=axis)
        return variables_list[0] if len(variables_list) > 0 else None

    def get_nc_variables_y_by_attributes(self, axis='Y'):
        '''
        """
        Returns a list of variables that axis='Y'

        """
        :param axis:
        :return:
        '''
        variables_list = self.dataset.get_variables_by_attributes(axis=axis)
        return variables_list[0] if len(variables_list) > 0 else None

    def get_nc_variables_z_by_attributes(self, axis='Z'):
        '''
        """
        Returns a list of variables that axis='Z'

        """
        :param axis:
        :return:
        '''
        variables_list = self.dataset.get_variables_by_attributes(axis=axis)

        return variables_list[0] if len(variables_list) > 0 else None

    def get_nc_variables_t_by_attributes(self, axis='T'):
        '''
        """
        Returns a list of variables that axis='T'

        :param axis:
        :return:
        '''
        variables_list = self.dataset.get_variables_by_attributes(axis=axis)
        return variables_list[0] if len(variables_list) > 0 else None

    def get_nc_variables_no_axis_by_attributes(self, axis=lambda v: v is None):
        '''
        """
        # Get variables that don't have an "axis" attribute

        :param axis:
        :return:
        '''
        variables_list = self.dataset.get_variables_by_attributes(axis=axis)
        return variables_list if len(variables_list) > 0 else None

    # get data array

    def get_times(self):
        '''

        :return:None if time variable==None else variable[::] as array
        '''
        t_variable = self.get_nc_variables_t_by_attributes()
        return None if t_variable == None else num2date(t_variable[::], t_variable.units)

    def __get_variables_data(self):
        variables_data_dict = dict()
        for v_name in self.variables.keys():
            data_array_dict = self.__get_variable_data_by_name(v_name)
            variables_data_dict[v_name] = data_array_dict
        return variables_data_dict

    def __get_variable_data_by_name(self, name):
        '''
        get variable data array by name,return OrderedDict
        :param name:
        :return:
        '''
        variable = self.get_variable_by_name(name)
        t_variable = self.get_nc_variables_t_by_attributes()
        data_array_dict = dict()
        if t_variable == None:
            # not have time  variable
            # print "not have time variable"
            data_array_dict["None"] = variable[::]
        else:
            i = 0

            for time in num2date(t_variable[::], t_variable.units):
                now_time_data = variable[i:i + 1:]
                data_array_dict[time] = now_time_data

                i += 1

        return data_array_dict

    def get_variable_data_by_name_time(self, name, time):
        var_data = self.variables_data_orderDict[name]
        return var_data[time] if var_data.has_key(time) else None

    def __get_attr_by_default_fillvals__(self, attr):
        '''
        add at 2019/05/24
        replace attr if attr has default_fillvals['S1']
        :param attr:
        :return:
        '''
        attr2 = ''

        # if isinstance(attr, unicode):
        #     if self.default_fillvals['S1'] in attr:
        #         attr2 = attr.replace(self.default_fillvals['S1'], ' ')
        # else:
        #     return attr
        return attr

    # 以下是重写AlgorithmClass基类方法
    def print_property_info(self):
        property_info = self.get_nc_attribute_str()
        return property_info

    def get_variables_data(self):
        all_data = self.__get_variables_data()
        return all_data

    def get_data_by_name(self, name, **kwargs):
        data = self.__get_variable_data_by_name(name)
        return data

    def get_variable_by_name(self, variable_name, **kwargs):
        return None if len(self.variables) == 0 else self.variables[variable_name]

    def get_dimension_by_name(self, dimension_name, **kwargs):
        return None if len(self.dim_variable) == 0 else self.dim_variable[dimension_name]

    def print_variable_property(self, name, var=None, **kwargs):
        '''
        打印变量属性信息
        :param name:变量名称
        :param var:
        :return:
        '''
        return self.get_nc_dim_variable_str(name, var)

    def print_dimension_property(self, name, var=None, **kwargs):
        '''
        打印维度属性信息
        :param name:维度名称
        :param var:
        :return:
        '''

        return self.get_nc_var_variable_str(name, var)

    # =================================


def judge_nc_type(file):
    '''
    judge NetCDF data Type ,NetCDF or HDF
    :param file:
    :return:
    '''
    dataset = Dataset(file)
    if dataset == None:
        # print "Set Dataset Error"
        return ncType.Non
    return ncType.HDF if dataset.groups != None and len(dataset.groups) > 0 else ncType.NetCDF


# ================


@enum.unique
class Var_Type(enum.Enum):
    D = "1D"
    Geo = "Geo2D"


@enum.unique
class ncType(enum.Enum):
    Non = "None"
    HDF = "HDF"
    NetCDF = "NetCDF"

