# -*- coding: utf-8 -*-
import sys
import os

ppath = os.path.abspath('..')
sys.path.append(os.path.join(ppath, 'm4'))
import datetime
import logging
import numpy as np
import netCDF4 as nc
import pygrib
import time

from m4.m4property import logginginfo




def getHingtPath(path):
    flist = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            flist.append(os.path.join(root, file))
    return flist






def getGribInfo(grbs):
    vnamedic = dict()
    for g in grbs:
        ls = str(g).split(":")
        varname = ls[1] + '_' + ls[4]
        var = ls[5].split(' ')[1]
        if varname in list(vnamedic.keys()):##############
            if len(vnamedic[varname]) > 0:
                for i,sv in enumerate(vnamedic[varname]):

                    if var in [str(svs).split(":")[5].split(' ')[1] for svs in sv]:  #
                        if len(vnamedic[varname]) > 1 and (i+1) != len(vnamedic[varname]):
                            continue
                        else:
                            vnamedic[varname].append([g])  # add first
                            break



                    else:
                        sv.append(g)
        else:
            vnamedic[varname] = [[g]]
    return vnamedic



@logginginfo(level="INFO")
def grib_to_nc_batGenNCfile(sourcePath, destinationPath, variablename=None):
    '''

    @名称: 批量grib文件生成nc文件
    @中文注释: 批量m4文件生成nc文件
    @入参:
        @param    path    str    文件路径
    @出参:
        @param  (headinfo,data)    tuple    返回头文件及数据

    @返回状态:
        @return    0    异常
        @return    1    成功
    @作    者: Mr.Wang
    @创建时间: 20190718
    @使用范例: disposeM4('./grib.grib')
    '''
    #try:

    if os.path.exists(sourcePath):
        if os.path.isdir(destinationPath):
            ncfile = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.nc'
            destinationPath = os.path.join(destinationPath, ncfile)
        if not os.path.exists(destinationPath):
            newpath = destinationPath.split('/')
            if len(newpath[-1].split('.')) > 1 and newpath[-1].split('.')[1] == 'nc':
                # print('/'.join(destinationPath.split('/')[:-1]))
                npath = '/'.join(destinationPath.split('/')[:-1])
                if not os.path.exists(npath):
                    os.makedirs(npath)
            else:
                os.makedirs(destinationPath)
                ncfile = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.nc'
                destinationPath = os.path.join(destinationPath, ncfile)

        grbs = pygrib.open(sourcePath)
        nc_fid = nc.Dataset(destinationPath, 'w', format="NETCDF4")
        vnamedic = getGribInfo(grbs)
        if variablename:
            vd = vnamedic.get(variablename,'')
            if vd:
                vdv = {variablename: vd}
                for k, v in vdv.items():
                    k = k.replace(' ', '')
                    dimv = k.split('_')[1]

                    if len(v) == 1:
                        if k not in list(nc_fid.variables.keys()):
                            if len(v[0]) == 1:
                                if 'latitude' not in list(nc_fid.dimensions.keys()):
                                    lat = np.array(v[0][0]['distinctLatitudes'])
                                    nc_fid.createDimension('latitude', len(lat))
                                if 'longitude' not in list(nc_fid.dimensions.keys()):
                                    lon = v[0][0]['distinctLongitudes']
                                    nc_fid.createDimension('longitude', len(lon))
                                if 'time' not in list(nc_fid.dimensions.keys()):
                                    nc_fid.createDimension('time', None)
                                if 'level' not in list(nc_fid.dimensions.keys()):
                                    nc_fid.createDimension('level', None)
                                if dimv not in list(nc_fid.dimensions.keys()):
                                    nc_fid.createDimension(dimv, None)
                                if 'latitude' not in list(nc_fid.variables.keys()):
                                    lat = v[0][0]['distinctLatitudes']
                                    vlatitudes = nc_fid.createVariable('latitude', 'f8', ('latitude',), )
                                    vlatitudes[:] = lat[:]
                                if 'longitude' not in list(nc_fid.variables.keys()):
                                    lon = v[0][0]['distinctLongitudes']
                                    vlongitudes = nc_fid.createVariable('longitude', 'f8', ('longitude',), )
                                    vlongitudes[:] = lon[:]
                                if 'time' not in list(nc_fid.variables.keys()):
                                    vtime = nc_fid.createVariable("time", 'f8', ("time",), fill_value=0)
                                    tunit = str(v[0][0]).split(":")[6].split(' ')[3]
                                    if tunit == 'hrs':
                                        vtime.units = "hours since 0001-01-01 00:00:00.0"
                                    elif tunit == 'mins':
                                        vtime.units = "minutes since 0001-01-01 00:00:00.0"
                                    else:
                                        vtime.units = "hours since 0001-01-01 00:00:00.0"

                                    stime = str(v[0][0]).split(":")[7].split(' ')[1]
                                    stime = datetime.datetime.strptime(stime, '%Y%m%d%H%M%S')
                                    vtime.standard_name = "time"
                                    vtime.long_name = "GRIB forecast or observation time"
                                    vtime.calendar = "proleptic_gregorian"
                                    vtime[:] = nc.date2num(stime, units=vtime.units, calendar=vtime.calendar)
                                if 'level' not in list(nc_fid.variables.keys()):
                                    vens = nc_fid.createVariable("level", 'i4', ("level",))

                                multivat = nc_fid.createVariable(k, "f8", ("time", "level", "latitude", "longitude",),
                                                                 fill_value=np.NAN, zlib=True,
                                                                 least_significant_digit=3)

                                if len(str(v[0][0]).split(":")[5].split(' ')) == 3:
                                    vens[:] = np.array([int(str(v[0][0]).split(":")[5].split(' ')[1])])
                                    vens.units = str(v[0][0]).split(":")[5].split(' ')[2]

                                else:
                                    vens[:] = np.array([0])
                                    vens.units = 'Pa'

                                multivat[0, 0, :, :] = v[0][0]['values'].data if isinstance(v[0][0]['values'],
                                                                                            np.ma.core.MaskedArray) else \
                                v[0][0]['values']
                                multivat.units = v[0][0]['units']
                                multivat.longname = v[0][0]['name']
                                multivat.dataDate = v[0][0]['dataDate']
                                multivat.pressureUnits = v[0][0]['pressureUnits']
                                multivat.level = v[0][0]['level']
                                multivat.shortName = v[0][0]['shortName']
                                multivat.maximum = v[0][0]['maximum']
                                multivat.minimum = v[0][0]['minimum']
                                multivat.average = v[0][0]['average']
                                # multivat.nameOfFirstFixedSurface = v[0][0]['nameOfFirstFixedSurface']
                                # multivat.missingValue = v[0][0]['missingValue']
                            else:

                                if 'latitude' not in list(nc_fid.dimensions.keys()):
                                    lat = np.array(v[0][0]['distinctLatitudes'])
                                    nc_fid.createDimension('latitude', len(lat))
                                if 'longitude' not in list(nc_fid.dimensions.keys()):
                                    lon = v[0][0]['distinctLongitudes']
                                    nc_fid.createDimension('longitude', len(lon))
                                if 'time' not in list(nc_fid.dimensions.keys()):
                                    nc_fid.createDimension('time', None)

                                if dimv not in list(nc_fid.dimensions.keys()):
                                    nc_fid.createDimension(dimv, None)
                                if 'latitude' not in list(nc_fid.variables.keys()):
                                    lat = v[0][0]['distinctLatitudes']
                                    vlatitudes = nc_fid.createVariable('latitude', 'f8', ('latitude',), )
                                    vlatitudes[:] = lat[:]
                                if 'longitude' not in list(nc_fid.variables.keys()):
                                    lon = v[0][0]['distinctLongitudes']
                                    vlongitudes = nc_fid.createVariable('longitude', 'f8', ('longitude',), )
                                    vlongitudes[:] = lon[:]
                                if 'time' not in list(nc_fid.variables.keys()):
                                    vtime = nc_fid.createVariable("time", 'f8', ("time",), fill_value=0)
                                    tunit = str(v[0][0]).split(":")[6].split(' ')[3]
                                    if tunit == 'hrs':
                                        vtime.units = "hours since 0001-01-01 00:00:00.0"
                                    elif tunit == 'mins':
                                        vtime.units = "minutes since 0001-01-01 00:00:00.0"
                                    else:
                                        vtime.units = "hours since 0001-01-01 00:00:00.0"

                                    stime = str(v[0][0]).split(":")[7].split(' ')[1]
                                    stime = datetime.datetime.strptime(stime, '%Y%m%d%H%M%S')
                                    vtime.standard_name = "time"
                                    vtime.long_name = "GRIB forecast or observation time"
                                    vtime.calendar = "proleptic_gregorian"
                                    vtime[:] = nc.date2num(stime, units=vtime.units, calendar=vtime.calendar)

                                for i, vg in enumerate(v[0]):

                                    print(str(v[0][i]).split(":")[5].split(' '))
                                    if dimv not in list(nc_fid.dimensions.keys()):
                                        nc_fid.createDimension(dimv, None)
                                    if dimv not in list(nc_fid.variables.keys()):
                                        if str(v[0][i]).split(":")[5].split(' ')[1].isdigit():
                                            vlevel = nc_fid.createVariable(dimv, np.int32, (dimv,), fill_value=0)
                                        else:
                                            vlevel = nc_fid.createVariable(dimv, np.str, (dimv,), fill_value=0)
                                    if k not in list(nc_fid.variables.keys()):
                                        multivat = nc_fid.createVariable(k, "f8",
                                                                         ('time', dimv, "latitude", "longitude",),
                                                                         fill_value=np.NAN, zlib=True,
                                                                         least_significant_digit=3)

                                    nc_fid.variables[dimv][i] = str(v[0][i]).split(":")[5].split(' ')[1]
                                    if len(str(v[0][i]).split(":")[5].split(' ')) > 2:
                                        nc_fid.variables[dimv].units = str(v[0][i]).split(":")[5].split(' ')[2]
                                    # multivat[i, 0, :, :] = np.array(vg['values'])
                                    multivat[0, i, :, :] = vg['values'].data if isinstance(vg['values'],
                                                                                           np.ma.core.MaskedArray) else \
                                    vg['values']
                                    multivat.units = vg['units']
                                    multivat.longname = vg['name']
                                    multivat.dataDate = vg['dataDate']
                                    multivat.pressureUnits = vg['pressureUnits']
                                    multivat.level = vg['level']
                                    multivat.shortName = vg['shortName']
                                    multivat.maximum = vg['maximum']
                                    multivat.minimum = vg['minimum']
                                    multivat.average = vg['average']
                                    multivat.nameOfFirstFixedSurface = vg['nameOfFirstFixedSurface']
                                    multivat.missingValue = vg['missingValue']



                    else:

                        for i, val in enumerate(v):

                            if len(val) == 1:
                                varname = str(k) + '_' + 'var' + str(i + 1)
                                if 'latitude' not in list(nc_fid.dimensions.keys()):
                                    lat = np.array(val[0]['distinctLatitudes'])
                                    nc_fid.createDimension('latitude', len(lat))
                                if 'longitude' not in list(nc_fid.dimensions.keys()):
                                    lon = val[0]['distinctLongitudes']
                                    nc_fid.createDimension('longitude', len(lon))
                                if 'time' not in list(nc_fid.dimensions.keys()):
                                    nc_fid.createDimension('time', None)
                                if 'level' not in list(nc_fid.dimensions.keys()):
                                    nc_fid.createDimension('level', None)
                                if 'latitude' not in list(nc_fid.variables.keys()):
                                    lat = val[0]['distinctLatitudes']
                                    vlatitudes = nc_fid.createVariable('latitude', 'f8', ('latitude',), )
                                    vlatitudes[:] = lat[:]
                                if 'longitude' not in list(nc_fid.variables.keys()):
                                    lon = val[0]['distinctLongitudes']
                                    vlongitudes = nc_fid.createVariable('longitude', 'f8', ('longitude',), )
                                    vlongitudes[:] = lon[:]
                                if 'time' not in list(nc_fid.variables.keys()):
                                    vtime = nc_fid.createVariable("time", 'f8', ("time",), fill_value=0)
                                    tunit = str(v[0][0]).split(":")[6].split(' ')[3]
                                    if tunit == 'hrs':
                                        vtime.units = "hours since 0001-01-01 00:00:00.0"
                                    elif tunit == 'mins':
                                        vtime.units = "minutes since 0001-01-01 00:00:00.0"
                                    else:
                                        vtime.units = "hours since 0001-01-01 00:00:00.0"

                                    stime = str(v[0][0]).split(":")[7].split(' ')[1]
                                    stime = datetime.datetime.strptime(stime, '%Y%m%d%H%M%S')
                                    vtime.standard_name = "time"
                                    vtime.long_name = "GRIB forecast or observation time"
                                    vtime.calendar = "proleptic_gregorian"
                                    vtime[:] = nc.date2num(stime, units=vtime.units, calendar=vtime.calendar)

                                if 'level' not in list(nc_fid.variables.keys()):
                                    vens = nc_fid.createVariable("level", np.int32, ("level",))
                                    vens[:] = np.array([0])
                                if varname not in list(nc_fid.variables.keys()):
                                    multivat = nc_fid.createVariable(varname, "f8",
                                                                     ("time", "level", "latitude", "longitude",),
                                                                     fill_value=np.NAN, zlib=True,
                                                                     least_significant_digit=3)
                                    vens[:] = np.array([int(str(val[0]).split(":")[5].split(' ')[1])])
                                    multivat[0, 0, :, :] = val[0]['values'].data if isinstance(val[0]['values'],
                                                                                               np.ma.core.MaskedArray) else \
                                    val[0]['values']
                                    multivat.units = val[0]['units']
                                    multivat.longname = val[0]['name']
                                    multivat.dataDate = val[0]['dataDate']
                                    multivat.pressureUnits = val[0]['pressureUnits']
                                    multivat.level = val[0]['level']
                                    multivat.shortName = val[0]['shortName']
                                    multivat.maximum = val[0]['maximum']
                                    multivat.minimum = val[0]['minimum']
                                    multivat.average = val[0]['average']
                                    multivat.nameOfFirstFixedSurface = val[0]['nameOfFirstFixedSurface']
                                    multivat.missingValue = val[0]['missingValue']




                            else:

                                for j, sval in enumerate(val):

                                    mulvarname = str(k) + '_' + 'var' + str(i + 1) + '_' + str(len(val))
                                    mdimv = str(dimv) + '_' + 'var' + str(i + 1) + '_' + str(len(val))
                                    # print(str(k) + '_' + 'var' + str(i + 1) + '_' + str(len(val)))
                                    # print(mulvarname)
                                    if 'latitude' not in list(nc_fid.dimensions.keys()):
                                        lat = np.array(sval['distinctLatitudes'])
                                        nc_fid.createDimension('latitude', len(lat))
                                    if 'longitude' not in list(nc_fid.dimensions.keys()):
                                        lon = sval['distinctLongitudes']
                                        nc_fid.createDimension('longitude', len(lon))
                                    if 'time' not in list(nc_fid.dimensions.keys()):
                                        nc_fid.createDimension('time', None)

                                    if dimv not in list(nc_fid.dimensions.keys()):
                                        nc_fid.createDimension(dimv, None)
                                    if 'latitude' not in list(nc_fid.variables.keys()):
                                        lat = sval['distinctLatitudes']
                                        vlatitudes = nc_fid.createVariable('latitude', 'f8', ('latitude',), )
                                        vlatitudes[:] = lat[:]
                                    if 'longitude' not in list(nc_fid.variables.keys()):
                                        lon = sval['distinctLongitudes']
                                        vlongitudes = nc_fid.createVariable('longitude', 'f8', ('longitude',), )
                                        vlongitudes[:] = lon[:]
                                    if 'time' not in list(nc_fid.variables.keys()):
                                        vtime = nc_fid.createVariable("time", 'f8', ("time",), fill_value=0)
                                        tunit = str(v[0][0]).split(":")[6].split(' ')[3]
                                        if tunit == 'hrs':
                                            vtime.units = "hours since 0001-01-01 00:00:00.0"
                                        elif tunit == 'mins':
                                            vtime.units = "minutes since 0001-01-01 00:00:00.0"
                                        else:
                                            vtime.units = "hours since 0001-01-01 00:00:00.0"

                                        stime = str(v[0][0]).split(":")[7].split(' ')[1]
                                        stime = datetime.datetime.strptime(stime, '%Y%m%d%H%M%S')
                                        vtime.standard_name = "time"
                                        vtime.long_name = "GRIB forecast or observation time"
                                        vtime.calendar = "proleptic_gregorian"
                                        vtime[:] = nc.date2num(stime, units=vtime.units, calendar=vtime.calendar)

                                    if mdimv not in list(nc_fid.dimensions.keys()):
                                        nc_fid.createDimension(mdimv, None)
                                    if mdimv not in list(nc_fid.variables.keys()):
                                        if str(sval).split(":")[5].split(' ')[1].isdigit():
                                            vlevel = nc_fid.createVariable(mdimv, np.int32, (mdimv,), fill_value=0)
                                        else:
                                            vlevel = nc_fid.createVariable(mdimv, np.str, (mdimv,), fill_value=0)
                                        # vlevel = nc_fid.createVariable(dimv, np.int32, (dimv,), fill_value=0)
                                        # vlevel = nc_fid.createVariable(mdimv, np.str,(mdimv,), fill_value=0)
                                    if mulvarname not in list(nc_fid.variables.keys()):
                                        multivat = nc_fid.createVariable(mulvarname, "f8",
                                                                         ("time", mdimv, "latitude", "longitude",),
                                                                         fill_value=np.NAN, zlib=True,
                                                                         least_significant_digit=3)
                                    print(str(sval).split(":")[5].split(' '))
                                    nc_fid.variables[mdimv][j] = str(sval).split(":")[5].split(' ')[1]
                                    if len(str(sval).split(":")[5].split(' ')) > 2:
                                        nc_fid.variables[mdimv].units = str(sval).split(":")[5].split(' ')[2]
                                    multivat[0, j, :, :] = sval['values'].data if isinstance(sval['values'],
                                                                                             np.ma.core.MaskedArray) else \
                                    sval['values']
                                    multivat.units = sval['units']
                                    multivat.longname = sval['name']
                                    multivat.dataDate = sval['dataDate']
                                    multivat.pressureUnits = sval['pressureUnits']
                                    multivat.level = sval['level']
                                    multivat.shortName = sval['shortName']
                                    multivat.maximum = sval['maximum']
                                    multivat.minimum = sval['minimum']
                                    multivat.average = sval['average']
                                    multivat.nameOfFirstFixedSurface = sval['nameOfFirstFixedSurface']
                                    multivat.missingValue = sval['missingValue']
                nc_fid.history = 'Created ' + time.ctime(time.time())
                nc_fid.source = "grib operate netcdf file"
                nc_fid.flag = "grib to nc"
                nc_fid.close()
                grbs.close()
                print('inner: Successful nc file generation')
                return 0
            else:
                print('The Key is not exist!')

        else:
            if vnamedic:
                for k, v in vnamedic.items():
                    k = k.replace(' ', '')
                    dimv = k.split('_')[1]
                    print(k)

                    if len(v) == 1:
                        if k not in list(nc_fid.variables.keys()):
                            if len(v[0]) == 1:
                                if 'latitude' not in list(nc_fid.dimensions.keys()):
                                    lat = np.array(v[0][0]['distinctLatitudes'])
                                    nc_fid.createDimension('latitude', len(lat))
                                if 'longitude' not in list(nc_fid.dimensions.keys()):
                                    lon = v[0][0]['distinctLongitudes']
                                    nc_fid.createDimension('longitude', len(lon))
                                if 'time' not in list(nc_fid.dimensions.keys()):
                                    nc_fid.createDimension('time', None)
                                if 'level' not in list(nc_fid.dimensions.keys()):
                                    nc_fid.createDimension('level', None)
                                if dimv not in list(nc_fid.dimensions.keys()):
                                    nc_fid.createDimension(dimv, None)
                                if 'latitude' not in list(nc_fid.variables.keys()):
                                    lat = v[0][0]['distinctLatitudes']
                                    vlatitudes = nc_fid.createVariable('latitude', 'f8', ('latitude',), )
                                    vlatitudes[:] = lat[:]
                                if 'longitude' not in list(nc_fid.variables.keys()):
                                    lon = v[0][0]['distinctLongitudes']
                                    vlongitudes = nc_fid.createVariable('longitude', 'f8', ('longitude',), )
                                    vlongitudes[:] = lon[:]
                                if 'time' not in list(nc_fid.variables.keys()):
                                    vtime = nc_fid.createVariable("time", 'f8', ("time",), fill_value=0)
                                    tunit = str(v[0][0]).split(":")[6].split(' ')[3]
                                    if tunit == 'hrs':
                                        vtime.units = "hours since 0001-01-01 00:00:00.0"
                                    elif tunit == 'mins':
                                        vtime.units = "minutes since 0001-01-01 00:00:00.0"
                                    else:
                                        vtime.units = "hours since 0001-01-01 00:00:00.0"


                                    stime = str(v[0][0]).split(":")[7].split(' ')[1]
                                    stime = datetime.datetime.strptime(stime, '%Y%m%d%H%M%S')
                                    vtime.standard_name = "time"
                                    vtime.long_name = "GRIB forecast or observation time"
                                    vtime.calendar = "proleptic_gregorian"
                                    vtime[:] = nc.date2num(stime, units=vtime.units, calendar=vtime.calendar)
                                if 'level' not in list(nc_fid.variables.keys()):
                                    vens = nc_fid.createVariable("level", 'i4', ("level",))

                                multivat = nc_fid.createVariable(k, "f8", ("time", "level", "latitude", "longitude",), fill_value=np.NAN,zlib=True,least_significant_digit=3)


                                if len(str(v[0][0]).split(":")[5].split(' ')) == 3:
                                    vens[:] = np.array([int(str(v[0][0]).split(":")[5].split(' ')[1])])
                                    vens.units = str(v[0][0]).split(":")[5].split(' ')[2]

                                else:
                                    vens[:] = np.array([0])
                                    vens.units = 'Pa'

                                multivat[0, 0, :, :] = v[0][0]['values'].data if isinstance(v[0][0]['values'], np.ma.core.MaskedArray) else v[0][0]['values']
                                multivat.units = v[0][0]['units']
                                multivat.longname = v[0][0]['name']
                                multivat.dataDate = v[0][0]['dataDate']
                                multivat.pressureUnits = v[0][0]['pressureUnits']
                                multivat.level = v[0][0]['level']
                                multivat.shortName = v[0][0]['shortName']
                                multivat.maximum = v[0][0]['maximum']
                                multivat.minimum = v[0][0]['minimum']
                                multivat.average = v[0][0]['average']
                                #multivat.nameOfFirstFixedSurface = v[0][0]['nameOfFirstFixedSurface']
                                #multivat.missingValue = v[0][0]['missingValue']
                            else:

                                if 'latitude' not in list(nc_fid.dimensions.keys()):
                                    lat = np.array(v[0][0]['distinctLatitudes'])
                                    nc_fid.createDimension('latitude', len(lat))
                                if 'longitude' not in list(nc_fid.dimensions.keys()):
                                    lon = v[0][0]['distinctLongitudes']
                                    nc_fid.createDimension('longitude', len(lon))
                                if 'time' not in list(nc_fid.dimensions.keys()):
                                    nc_fid.createDimension('time', None)

                                if dimv not in list(nc_fid.dimensions.keys()):
                                    nc_fid.createDimension(dimv, None)
                                if 'latitude' not in list(nc_fid.variables.keys()):
                                    lat = v[0][0]['distinctLatitudes']
                                    vlatitudes = nc_fid.createVariable('latitude', 'f8', ('latitude',), )
                                    vlatitudes[:] = lat[:]
                                if 'longitude' not in list(nc_fid.variables.keys()):
                                    lon = v[0][0]['distinctLongitudes']
                                    vlongitudes = nc_fid.createVariable('longitude', 'f8', ('longitude',), )
                                    vlongitudes[:] = lon[:]
                                if 'time' not in list(nc_fid.variables.keys()):
                                    vtime = nc_fid.createVariable("time", 'f8', ("time",), fill_value=0)
                                    tunit = str(v[0][0]).split(":")[6].split(' ')[3]
                                    if tunit == 'hrs':
                                        vtime.units = "hours since 0001-01-01 00:00:00.0"
                                    elif tunit == 'mins':
                                        vtime.units = "minutes since 0001-01-01 00:00:00.0"
                                    else:
                                        vtime.units = "hours since 0001-01-01 00:00:00.0"

                                    stime = str(v[0][0]).split(":")[7].split(' ')[1]
                                    stime = datetime.datetime.strptime(stime, '%Y%m%d%H%M%S')
                                    vtime.standard_name = "time"
                                    vtime.long_name = "GRIB forecast or observation time"
                                    vtime.calendar = "proleptic_gregorian"
                                    vtime[:] = nc.date2num(stime, units=vtime.units, calendar=vtime.calendar)


                                for i, vg in enumerate(v[0]):

                                    print(str(v[0][i]).split(":")[5].split(' '))
                                    if dimv not in list(nc_fid.dimensions.keys()):
                                        nc_fid.createDimension(dimv, None)
                                    if dimv not in list(nc_fid.variables.keys()):
                                        if str(v[0][i]).split(":")[5].split(' ')[1].isdigit():
                                            vlevel = nc_fid.createVariable(dimv, np.int32, (dimv,), fill_value=0)
                                        else:
                                            vlevel = nc_fid.createVariable(dimv, np.str, (dimv,), fill_value=0)
                                    if k not in list(nc_fid.variables.keys()):
                                        multivat = nc_fid.createVariable(k, "f8", ('time', dimv, "latitude", "longitude",), fill_value=np.NAN,zlib=True,least_significant_digit=3)

                                    nc_fid.variables[dimv][i] = str(v[0][i]).split(":")[5].split(' ')[1]
                                    if len(str(v[0][i]).split(":")[5].split(' ')) > 2:
                                        nc_fid.variables[dimv].units = str(v[0][i]).split(":")[5].split(' ')[2]
                                    # multivat[i, 0, :, :] = np.array(vg['values'])
                                    multivat[0, i, :, :] = vg['values'].data if isinstance(vg['values'], np.ma.core.MaskedArray) else vg['values']
                                    multivat.units = vg['units']
                                    multivat.longname = vg['name']
                                    multivat.dataDate = vg['dataDate']
                                    multivat.pressureUnits = vg['pressureUnits']
                                    multivat.level = vg['level']
                                    multivat.shortName = vg['shortName']
                                    multivat.maximum = vg['maximum']
                                    multivat.minimum = vg['minimum']
                                    multivat.average = vg['average']
                                    multivat.nameOfFirstFixedSurface = vg['nameOfFirstFixedSurface']
                                    multivat.missingValue = vg['missingValue']



                    else:

                        for i,val in enumerate(v):

                            if len(val) == 1:
                                varname = str(k) + '_' + 'var' + str(i + 1)
                                if 'latitude' not in list(nc_fid.dimensions.keys()):
                                    lat = np.array(val[0]['distinctLatitudes'])
                                    nc_fid.createDimension('latitude', len(lat))
                                if 'longitude' not in list(nc_fid.dimensions.keys()):
                                    lon = val[0]['distinctLongitudes']
                                    nc_fid.createDimension('longitude', len(lon))
                                if 'time' not in list(nc_fid.dimensions.keys()):
                                    nc_fid.createDimension('time', None)
                                if 'level' not in list(nc_fid.dimensions.keys()):
                                    nc_fid.createDimension('level', None)
                                if 'latitude' not in list(nc_fid.variables.keys()):
                                    lat = val[0]['distinctLatitudes']
                                    vlatitudes = nc_fid.createVariable('latitude', 'f8', ('latitude',), )
                                    vlatitudes[:] = lat[:]
                                if 'longitude' not in list(nc_fid.variables.keys()):
                                    lon = val[0]['distinctLongitudes']
                                    vlongitudes = nc_fid.createVariable('longitude', 'f8', ('longitude',), )
                                    vlongitudes[:] = lon[:]
                                if 'time' not in list(nc_fid.variables.keys()):
                                    vtime = nc_fid.createVariable("time", 'f8', ("time",), fill_value=0)
                                    tunit = str(v[0][0]).split(":")[6].split(' ')[3]
                                    if tunit == 'hrs':
                                        vtime.units = "hours since 0001-01-01 00:00:00.0"
                                    elif tunit == 'mins':
                                        vtime.units = "minutes since 0001-01-01 00:00:00.0"
                                    else:
                                        vtime.units = "hours since 0001-01-01 00:00:00.0"

                                    stime = str(v[0][0]).split(":")[7].split(' ')[1]
                                    stime = datetime.datetime.strptime(stime, '%Y%m%d%H%M%S')
                                    vtime.standard_name = "time"
                                    vtime.long_name = "GRIB forecast or observation time"
                                    vtime.calendar = "proleptic_gregorian"
                                    vtime[:] = nc.date2num(stime, units=vtime.units, calendar=vtime.calendar)

                                if 'level' not in list(nc_fid.variables.keys()):
                                    vens = nc_fid.createVariable("level", np.int32, ("level",))
                                    vens[:] = np.array([0])
                                if varname not in list(nc_fid.variables.keys()):
                                    multivat = nc_fid.createVariable(varname, "f8", ("time", "level", "latitude", "longitude",), fill_value=np.NAN,zlib=True,least_significant_digit=3)
                                    vens[:] = np.array([int(str(val[0]).split(":")[5].split(' ')[1])])
                                    multivat[0, 0, :, :] = val[0]['values'].data if isinstance(val[0]['values'], np.ma.core.MaskedArray) else val[0]['values']
                                    multivat.units = val[0]['units']
                                    multivat.longname = val[0]['name']
                                    multivat.dataDate = val[0]['dataDate']
                                    multivat.pressureUnits = val[0]['pressureUnits']
                                    multivat.level = val[0]['level']
                                    multivat.shortName = val[0]['shortName']
                                    multivat.maximum = val[0]['maximum']
                                    multivat.minimum = val[0]['minimum']
                                    multivat.average = val[0]['average']
                                    multivat.nameOfFirstFixedSurface = val[0]['nameOfFirstFixedSurface']
                                    multivat.missingValue = val[0]['missingValue']




                            else:

                                for j, sval in enumerate(val):

                                    mulvarname = str(k) + '_' + 'var' + str(i + 1) + '_' + str(len(val))
                                    mdimv = str(dimv) + '_' + 'var' + str(i + 1) + '_' + str(len(val))
                                    #print(str(k) + '_' + 'var' + str(i + 1) + '_' + str(len(val)))
                                    #print(mulvarname)
                                    if 'latitude' not in list(nc_fid.dimensions.keys()):
                                        lat = np.array(sval['distinctLatitudes'])
                                        nc_fid.createDimension('latitude', len(lat))
                                    if 'longitude' not in list(nc_fid.dimensions.keys()):
                                        lon = sval['distinctLongitudes']
                                        nc_fid.createDimension('longitude', len(lon))
                                    if 'time' not in list(nc_fid.dimensions.keys()):
                                        nc_fid.createDimension('time', None)

                                    if dimv not in list(nc_fid.dimensions.keys()):
                                        nc_fid.createDimension(dimv, None)
                                    if 'latitude' not in list(nc_fid.variables.keys()):
                                        lat = sval['distinctLatitudes']
                                        vlatitudes = nc_fid.createVariable('latitude', 'f8', ('latitude',), )
                                        vlatitudes[:] = lat[:]
                                    if 'longitude' not in list(nc_fid.variables.keys()):
                                        lon = sval['distinctLongitudes']
                                        vlongitudes = nc_fid.createVariable('longitude', 'f8', ('longitude',), )
                                        vlongitudes[:] = lon[:]
                                    if 'time' not in list(nc_fid.variables.keys()):
                                        vtime = nc_fid.createVariable("time", 'f8', ("time",), fill_value=0)
                                        tunit = str(v[0][0]).split(":")[6].split(' ')[3]
                                        if tunit == 'hrs':
                                            vtime.units = "hours since 0001-01-01 00:00:00.0"
                                        elif tunit == 'mins':
                                            vtime.units = "minutes since 0001-01-01 00:00:00.0"
                                        else:
                                            vtime.units = "hours since 0001-01-01 00:00:00.0"

                                        stime = str(v[0][0]).split(":")[7].split(' ')[1]
                                        stime = datetime.datetime.strptime(stime, '%Y%m%d%H%M%S')
                                        vtime.standard_name = "time"
                                        vtime.long_name = "GRIB forecast or observation time"
                                        vtime.calendar = "proleptic_gregorian"
                                        vtime[:] = nc.date2num(stime, units=vtime.units, calendar=vtime.calendar)

                                    if mdimv not in list(nc_fid.dimensions.keys()):
                                        nc_fid.createDimension(mdimv, None)
                                    if mdimv not in list(nc_fid.variables.keys()):
                                        if str(sval).split(":")[5].split(' ')[1].isdigit():
                                            vlevel = nc_fid.createVariable(mdimv, np.int32, (mdimv,), fill_value=0)
                                        else:
                                            vlevel = nc_fid.createVariable(mdimv, np.str, (mdimv,), fill_value=0)
                                        # vlevel = nc_fid.createVariable(dimv, np.int32, (dimv,), fill_value=0)
                                        #vlevel = nc_fid.createVariable(mdimv, np.str,(mdimv,), fill_value=0)
                                    if mulvarname not in list(nc_fid.variables.keys()):
                                        multivat = nc_fid.createVariable(mulvarname, "f8", ("time", mdimv, "latitude", "longitude",), fill_value=np.NAN, zlib=True, least_significant_digit=3)
                                    print(str(sval).split(":")[5].split(' '))
                                    nc_fid.variables[mdimv][j] = str(sval).split(":")[5].split(' ')[1]
                                    if len(str(sval).split(":")[5].split(' ')) > 2:
                                        nc_fid.variables[mdimv].units = str(sval).split(":")[5].split(' ')[2]
                                    multivat[0, j, :, :] = sval['values'].data if isinstance(sval['values'], np.ma.core.MaskedArray) else sval['values']
                                    multivat.units = sval['units']
                                    multivat.longname = sval['name']
                                    multivat.dataDate = sval['dataDate']
                                    multivat.pressureUnits = sval['pressureUnits']
                                    multivat.level = sval['level']
                                    multivat.shortName = sval['shortName']
                                    multivat.maximum = sval['maximum']
                                    multivat.minimum = sval['minimum']
                                    multivat.average = sval['average']
                                    multivat.nameOfFirstFixedSurface = sval['nameOfFirstFixedSurface']
                                    multivat.missingValue = sval['missingValue']




                nc_fid.history = 'Created ' + time.ctime(time.time())
                nc_fid.source = "grib operate netcdf file"
                nc_fid.flag = "grib to nc"
                nc_fid.close()
                grbs.close()
                print('inner: Successful nc file generation')
                return 0
            else:
                print('the GRIB file ERROR!')


    else:
        print('the path [{}] is not exist!'.format(sourcePath))
    # except Exception as arg:
    #     nc_fid.close()
    #     grbs.close()
    #     print('ERROR', arg)
    #     logging.error('ERROR' + ':' + str(arg))


if __name__ == '__main__':
    #sourcePath = r'./gmf.gra.2018091100009.grb2'
    sourcePath = r'./gef.gra.grb2'
    destinationPath = r'./gen/gnc/gribtoncFile02.nc'
    grib_to_nc_batGenNCfile(sourcePath, destinationPath, 'Convective precipitation (water)_surface')
