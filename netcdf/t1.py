# -*- coding: gbk -*-

from hdf import HDF
from netcdf import Nc
h = HDF('/home/mrc/file/data/gen/hdf/20190812144446.hdf')
print(h.print_property_info())

c = Nc('/home/mrc/file/data/gen/nc/ncfile.nc')
print(c.print_property_info())