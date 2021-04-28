# -*- coding: utf-8 -*-
import pygrib
import os
from functools import reduce


'''
 File format : GRIB
    -1 : Institut Source   T Steptype Levels Num    Points Num Dtype : Parameter name
     1 : ECMWF    unknown  v instant       1   1   4150080   1  P16  : var59         
   Grid coordinates :
     1 : lonlat                   : points=4150080 (2880x1441)
                              lon : 0 to 359.875 by 0.125 degrees_east  circular
                              lat : 90 to -90 by -0.125 degrees_north
   Vertical coordinates :
     1 : surface                  : levels=1
   Time coordinate :  1 step
     RefTime =  2017-09-20 00:00:00  Units = hours  Calendar = proleptic_gregorian
  YYYY-MM-DD hh:mm:ss  YYYY-MM-DD hh:mm:ss  YYYY-MM-DD hh:mm:ss  YYYY-MM-DD hh:mm:ss
  2017-09-20 00:00:00
cdo sinfon: Processed 1 variable over 1 timestep [0.00s 17MB] 
'''

def showGribInfo(path):
    if os.path.exists(path):
        grbs = pygrib.open(path)
        grblist = list()
        for grb in grbs:
            NcCount = reduce(lambda x, y: x * y, grb.values.shape)
            if NcCount == grb.getNumberOfValues:
                ls = str(grb).split(":")
                varname = ls[1] + '_' + ls[4]
                grblist.append(varname)
        print('Verify GRIB data successfully')
        print('The GRIB file contains [{count}] variables information:'.format(count=str(len(set(grblist)))))
        for g in set(grblist):
            print('\t' + str(g))
def showOneGribInfo(path,var):
    if os.path.exists(path):
        var = var.split('_')[0]
        grblist = list()
        grbs = pygrib.open(path)
        for grb in grbs:
            grblist.append(grb.name)

        if var in grblist:
            bs = grbs.select(name=var)
            print('The GRIB file contains [{count}] variables information:'.format(count=str(len(set(bs)))))
            for b in bs:
                print('\t' + str(b))
        else:
            print('The Varible ({var}) does not exist! Please change and try again.'.format(var=var))
            print('Please change the variable to (unknown) and try again')
if __name__ == "__main__":
    showGribInfo('/home/trywangdao/mrcpysrc/grib/write/wGRIB/variable000.grb')
    showOneGribInfo('/home/trywangdao/mrcpysrc/grib/write/wGRIB/variable000.grb','unknown')