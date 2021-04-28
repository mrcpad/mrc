#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: 1.0
@author: xxf
@site: 
@software: PyCharm
@file: hdf.py
@time: 2019/05/20
"""
import click
import sys
sys.path.append(r'E:\Work\Hitec\MSZC\MSS2\05source\MMS2_MRC')
# reload(sys)
# 设置编码
# sys.setdefaultencoding('utf8')
from module.algorithm.netcdf.netcdf import Nc, num2date
from netCDF4 import OrderedDict


class HDF(Nc):
    """
        Groups define a hierarchical namespace within a netCDF file. They are
        analogous to directories in a unix filesystem. Each `netCDF4.Group` behaves like
        a `netCDF4.Dataset` within a Dataset, and can contain it's own variables,
        dimensions and attributes (and other Groups). See `netCDF4.Group.__init__`
        for more details.

        `netCDF4.Group` inherits from `netCDF4.Dataset`, so all the
        `netCDF4.Dataset` class methods and variables are available
        to a `netCDF4.Group` instance (except the `close` method).

        Additional mrc_app-only class variables:

        **`name`**: String describing the group name.
        """

    # property
    @property
    def groups(self):
        '''
        netCDF4.Group
        :return:
        '''
        return self._groups

    @groups.setter
    def groups(self, value):
        self._groups = value if isinstance(value, OrderedDict) else None

    @property
    def contains_group(self):
        '''
        this's dataset is contains group
        :return:
        '''
        return self._contains_group

    @contains_group.setter
    def contains_group(self, value):
        self._contains_group = value

    # Method

    def __init__(self, filename):
        super(HDF, self).__init__(filename)

        self.groups = self.dataset.groups

        self.contains_group = False if len(self.groups) == 0 else True

        self.variables = self.__get_variables()
        self.dimensions = self.__get_dimensions()

        # get variables data
        self.variables_data_orderDict = self.get_hdf_variables_data()

    def __get_variables(self):
        '''
        get variables,OrderedDict
        :return:
        '''
        group_variables = OrderedDict()
        if len(self.groups) == 0:  # 不包含group信息，只包含variables和groups
            group_variables = self.dataset.variables

        else:
            for group in self.groups.keys():
                variables = OrderedDict()
                for variable in self.groups[group].variables:
                    variables[variable] = self.groups[group].variables[variable]

                group_variables[group] = variables

        return group_variables

    def __get_dimensions(self):
        '''
        get dimensions,OrderedDict
        :return:
        '''
        group_dimensions = OrderedDict()
        if len(self.groups) == 0:  # 不包含group信息，只包含variables和groups
            group_dimensions = self.dataset.dimensions

        else:
            for group in self.groups.keys():
                dimensions = OrderedDict()
                for dimension in self.groups[group].dimensions:
                    dimensions[dimension] = self.groups[group].dimensions[dimension]

                group_dimensions[group] = dimensions

        return group_dimensions

    def __get_dim_var_variables(self):
        '''
        :return dimension's variables and feature's variables
        :return:
        '''
        dim_variables = OrderedDict()
        var_variables = OrderedDict()

        for v_name in self.variables.keys():
            if v_name in self.dimensions.keys():
                dim_variables[v_name] = self.variables[v_name]
            else:
                var_variables[v_name] = self.variables[v_name]
        return dim_variables, var_variables

    def get_variable_by_group_variable(self, group_name, var_name):
        variables = self.variables[group_name]
        return variables[var_name]

    def is_variable_exist(self, group_name, var_name):
        '''
        Determine whether there is variable by group name and variable name
        :param group_name:
        :param var_name:
        :return:
        '''

        return (self.groups.has_key(group_name) and self.variables[group_name].has_key(var_name))

    def get_hdf_describe(self):
        '''
        describe hdf info
        :return:
        '''
        out = ""
        out += "File " + self.file_name + "\n"
        out += "File Type " + self.file_format + "\n"
        out += "--------------------------------------------------------------------------------------------\n"
        out += "HDF File: /" + self.file_path + "\n"
        out += "{\n"
        # dataset 各组（groups）信息
        for g in self.groups.keys():
            out += self.get_hdf_group_str(g)

        # dataset全局属性
        if (len(self.dataset.ncattrs()) > 0):
            out += "    //global attributes:\n"
            out += self.get_nc_attr_str()

        out += "}"

        self.attribute_text = out
        return out

    def get_hdf_group_str(self, group_name):
        '''
        get group describe
        :param group_name:
        :return:
        '''
        variables = self.variables[group_name]
        describe = "group: " + group_name + "{\n"
        describe += "variables:\n"

        for variable in variables:
            var = variables[variable]
            var_describe = self.get_hdf_variable_str(group_name=group_name, var_name=variable, var=var)
            describe += var_describe
            describe += "\n"

        describe += "}\n"

        return describe

    def get_hdf_variable_str(self, group_name, var_name, var=None):
        '''
        get hdf variable describe
        :param group_name:
        :param var_name:
        :param var:
        :return:
        '''

        datatype_name="" if var.datatype.name==None  else var.datatype.name

        describe = ""
        describe += datatype_name + " " + var_name + "("

        for d in self.dimensions[group_name].keys():
            dim = self.dimensions[group_name][d]
            describe += dim.name + "=" + str(dim.size) + ","

        describe = describe[:len(describe) - 1]
        describe += ");\n"
        # variables 全局变量

        for ncattr in var.ncattrs():
            attr = self.__get_attr_by_default_fillvals__(var.getncattr(ncattr))
            describe += "            " + str(ncattr) + " = " + str(attr) + ";\n"

        return describe

    # get variables by attributes
    def get_group_variables_by_attributes(self, group_name, axis='T'):
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
        return self.groups[group_name].get_variables_by_attributes(axis=axis)

    def get_group_variables_x_by_attributes(self, group_name, axis='X'):
        '''
        """
        Returns a list of variables that axis='X'

        """
        :param axis:
        :return:
        '''
        variables_list = self.groups[group_name].get_variables_by_attributes(axis=axis)
        return variables_list[0] if len(variables_list) > 0 else None

    def get_group_variables_y_by_attributes(self, group_name, axis='Y'):
        '''
        """
        Returns a list of variables that axis='Y'

        """
        :param axis:
        :return:
        '''
        variables_list = self.groups[group_name].get_variables_by_attributes(axis=axis)
        return variables_list[0] if len(variables_list) > 0 else None

    def get_group_variables_z_by_attributes(self, group_name, axis='Z'):
        '''
        """
        Returns a list of variables that axis='Z'

        """
        :param axis:
        :return:
        '''
        variables_list = self.groups[group_name].get_variables_by_attributes(axis=axis)
        return variables_list[0] if len(variables_list) > 0 else None

    ## get variables by attributes

    def get_group_variables_t_by_attributes(self, group_name, axis='T'):
        '''
        """
        Returns a list of variables that axis='T'

        :param axis:
        :return:
        '''
        variables_list = self.groups[group_name].get_variables_by_attributes(axis=axis)
        return variables_list[0] if len(variables_list) > 0 else None

    def get_group_variables_no_axis_by_attributes(self, group_name, axis=lambda v: v is None):
        '''
        """
        # Get variables that don't have an "axis" attribute

        :param axis:
        :return:
        '''
        variables_list = self.groups[group_name].get_variables_by_attributes(axis=axis)
        return variables_list if len(variables_list) > 0 else None

        # get data array

    def get_hdf_times(self):
        '''

        :return:None if time variable==None else variable[::] as array
        '''
        t_variable = self.get_nc_variables_t_by_attributes()
        return None if t_variable == None else num2date(t_variable[::], t_variable.units)

    def get_hdf_variables_data(self):
        '''
        return hdf all variables data array,return by OrderedDict
        OrderedDict key:group  name,value:variable data
        :return:
        '''
        variables_data_dict = OrderedDict()
        if not self.contains_group:
            for variable_name in self.variables:
                variables_data_dict[variable_name] = self.__get_hdf_variable_data_by_v_name(variable_name)

        for g_name in self.groups.keys():
            data_array_dict = self.__get_hdf_variable_data_by_name(g_name)
            variables_data_dict[g_name] = data_array_dict
        return variables_data_dict

    def __get_hdf_variable_data_by_v_name(self, variablename):
        '''
        get variable data by name
        :param variablename:
        :return:
        '''

        return self.variables[variablename][::]

    def __get_hdf_variable_data_by_name(self, groupname):
        '''
        get variable data array by name,return OrderedDict
        :param name:
        :return:
        '''
        data_array_dict = OrderedDict()
        for variable_name in self.groups[groupname].variables.keys():
            variable = self.get_variable_by_group_variable(groupname, variable_name)

            data_array_dict[variable_name] = variable[::]

        return data_array_dict

    def get_hdf_variable_data_by_group_var(self, group_name, var_name):
        '''
        return variable data array by group name and variable name,if not contains group_name, var_name,return None
        :param group_name:
        :param var_name:
        :return:
        '''
        return self.variables_data_orderDict[group_name][var_name] if self.is_variable_exist(group_name,
                                                                                             var_name) else None

    # 以下是重写AlgorithmClass基类方法

    def print_property_info(self):
        property_info = self.get_hdf_describe()
        return property_info

    def get_variables_data(self):
        all_data = self.get_hdf_variables_data()
        return all_data

    def get_data_by_name(self, name,**kwargs):
        data = self.__get_hdf_variable_data_by_name(name)
        return data

    def get_variable_by_name(self, variable_name,**kwargs):
        group_name=kwargs.get("group_name")
        return self.get_variable_by_group_variable(group_name,variable_name)

    def get_dimension_by_name(self, dimension_name,**kwargs):
        pass


    def print_variable_property(self, name, var=None,**kwargs):
        '''
        打印变量属性信息
        :param name:变量名称
        :param var:
        :return:
        '''
        group_name=kwargs.get("group_name")
        return self.get_hdf_variable_str(group_name,name,var)

    def print_dimension_property(self, name, var=None,**kwargs):
        '''
        打印维度属性信息
        :param name:维度名称
        :param var:
        :return:
        '''

        return self.get_hdf_group_str(name)

    # =================================


