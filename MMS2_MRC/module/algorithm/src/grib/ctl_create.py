# -*- coding: utf-8 -*-


import numpy as np
from array import array
from netCDF4 import Dataset

nc = Dataset(r'D:\PanoplyWin\t1\tst\tdata\ER03.nc')
print(nc.variables.keys())
lons = nc.variables['longitude'][:]
lats = nc.variables['latitude'][:]
times = nc.variables['time'][:]
level = nc.variables['level'][:]
var = nc.variables['variable000'][:]
data = []
print(len(lons))
print(var.shape)
count = 0
for t in range(len(times)):
    for v in range(len(level)):
        for i in range(len(lats)):
            for j in range(len(lons)):
                data.append([lons[j], lats[i], level[v], var[t, v, i, j], times[t]])
                #np.float32([lons[j], lats[i], level[v], var[i, j], times[t]]).tofile('output.bin')
                print(count)
                count += 1
np.float32(data).tofile('output20.bin')

