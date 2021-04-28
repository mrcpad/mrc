# -*- coding: utf-8 -*-
from netCDF4 import Dataset
import os
from abc import ABCMeta,abstractmethod
import numpy as np

class BaseFile(metaclass=ABCMeta):

    @abstractmethod
    def setGroups(self):
        pass

    @abstractmethod
    def setDimensions(self):
        pass

    @abstractmethod
    def setVaribale(self):
        pass

    @abstractmethod
    def setNcattrs(self):
        pass



class NetCDFtoHDF(BaseFile):

    def __init__(self, ncFilePath,outPath,condtion):

        self.flag = 1
        if os.path.exists(ncFilePath):

            self.nc = Dataset(ncFilePath, 'r',)
            self.condtion = condtion
            self.outPath = outPath
            self.outnc = Dataset(outPath, 'w', format="NETCDF4")
            fncattrs = self.nc.ncattrs()
            self.dictncattrs = dict()
            for attr in fncattrs:
                self.dictncattrs[attr] = self.nc.getncattr(attr)
            if self.dictncattrs:
                self.setNcattrs()
            if self.nc.groups:
                self.setGroups()
            if self.nc.variables:
                self.setVaribale()
            print('inner: Successful NetCDF file generation')
            self.flag = 0

        else:
            print('The File does not exist')


    def setGroups(self):
        pass

    def setDimensions(self, var):
        if var:
            dims = var.dimensions
            for dim in dims:
                self.outnc.createDimension(self.nc.dimensions[dim].name,self.nc.dimensions[dim].size)



    def setVaribale(self):
        for cod in self.condtion.split():
            if cod in self.nc.variables.keys():
                self.setDimensions(self.nc.variables[cod])
                self.newVar = self.outnc.createVariable(self.nc.variables[cod].name,self.nc.variables[cod].datatype,self.nc.variables[cod].dimensions,fill_value=np.NAN,zlib=True,least_significant_digit=3)
                for ncattr in self.nc.variables[cod].ncattrs():
                    self.newVar.setncattr(ncattr,self.nc.variables[cod].getncattr(ncattr))
                self.newVar[:] = self.nc.variables[cod][:]


    def setNcattrs(self):
        self.outnc.setncatts(self.dictncattrs)



if __name__ == '__main__':
    NetCDFtoHDF(r'./1.nc',r'./variable000.nc','variable000')