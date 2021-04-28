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



class HDFtoNetCDF(BaseFile):

    def __init__(self, hdfFilePath,outPath,condtion):

        self.flag = 1
        if os.path.exists(hdfFilePath):

            self.hdf = Dataset(hdfFilePath, 'r',)
            self.condtion = condtion
            self.outPath = outPath
            self.outhdf = Dataset(outPath, 'w', format="NETCDF4")
            fncattrs = self.hdf.ncattrs()
            self.dictncattrs = dict()
            for attr in fncattrs:
                self.dictncattrs[attr] = self.hdf.getncattr(attr)
            if self.dictncattrs:
                self.setNcattrs()
            if self.hdf.groups:
                self.setGroups()
            else:
                if self.hdf.variables:
                    self.setVaribale()
            print('inner: Successful HDF file generation')
            self.flag = 0

        else:
            print('The File does not exist')


    def setGroups(self):

        for g in self.hdf.groups:

            for cod in self.condtion.split():
                if cod in self.hdf.groups[g].variables.keys():

                    if self.hdf.groups[g].variables[cod]:
                        dims = self.hdf.groups[g].variables[cod].dimensions
                        for dim in dims:
                            if dim not in list(self.outhdf.dimensions.keys()):
                                self.outhdf.createDimension(self.hdf.groups[g].dimensions[dim].name, self.hdf.groups[g].dimensions[dim].size)


                    self.newVar = self.outhdf.createVariable(self.hdf.groups[g].variables[cod].name,self.hdf.groups[g].variables[cod].datatype,self.hdf.groups[g].variables[cod].dimensions, fill_value=np.NAN,zlib=True, least_significant_digit=3)
                    for ncattr in self.hdf.groups[g].variables[cod].ncattrs():
                        self.newVar.setncattr(ncattr, self.hdf.groups[g].variables[cod].getncattr(ncattr))
                    self.newVar[:] = self.hdf.groups[g].variables[cod][:]

    def setDimensions(self, var):
        if var:
            dims = var.dimensions
            for dim in dims:
                self.outhdf.createDimension(self.hdf.dimensions[dim].name,self.hdf.dimensions[dim].size)



    def setVaribale(self):
        for cod in self.condtion.split():
            if cod in self.hdf.variables.keys():
                self.setDimensions(self.hdf.variables[cod])
                self.newVar = self.outhdf.createVariable(self.hdf.variables[cod].name,self.hdf.variables[cod].datatype,self.hdf.variables[cod].dimensions,fill_value=np.NAN,zlib=True,least_significant_digit=3)
                for ncattr in self.hdf.variables[cod].ncattrs():
                    self.newVar.setncattr(ncattr,self.hdf.variables[cod].getncattr(ncattr))
                self.newVar[:] = self.hdf.variables[cod][:]


    def setNcattrs(self):
        self.outhdf.setncatts(self.dictncattrs)



if __name__ == '__main__':
    HDFtoNetCDF(r'./1.hdf',r'./variable000.hdf','variable000')