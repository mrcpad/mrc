# -*- coding: gbk -*-
import sys
import os
ppath = os.path.abspath('..')
sys.path.append(os.path.join(ppath, 'm4'))
import datetime
import logging
import numpy as np
import time
import re
import netCDF4 as nc
from itertools import groupby
import threading
from module.algorithm.src.m4.m4property import DisposeM4file




class MyThread(threading.Thread):

    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):

        self.result = self.func(*self.args)
        #self.resultlist.append(self.result)

    def get_result(self):
        threading.Thread.join(self)
        try:

            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


def getHingtPath(path):

    flist = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            flist.append(os.path.join(root, file))
    return flist



def m4_to_hdf_batGenNCfile(sourcePath,destinationPath,variablename):

    '''

    @名称: 批量m4文件生成nc文件
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
    @使用范例: disposeM4('./15121008.000')
    '''
    try:
        if os.path.exists(sourcePath):
            if os.path.isdir(destinationPath):
                ncfile = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.hdf'
                destinationPath = os.path.join(destinationPath, ncfile)
            if not os.path.exists(destinationPath):
                newpath = destinationPath.split('/')
                if len(newpath[-1].split('.')) > 1 and newpath[-1].split('.')[1] == 'hdf':
                    # print('/'.join(destinationPath.split('/')[:-1]))
                    npath = '/'.join(destinationPath.split('/')[:-1])
                    if not os.path.exists(npath):
                        os.makedirs(npath)
                else:
                    os.makedirs(destinationPath)
                    ncfile = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.hdf'
                    destinationPath = os.path.join(destinationPath, ncfile)

            levelm4dict = getHingtPath(sourcePath)
            if levelm4dict:
                sourceDict = dict()
                thread_list = []
                t_data = []
                for m4file in levelm4dict:
                    #t = threading.Thread(target=disposeM4, args=(m4file, ))
                    t = MyThread(DisposeM4file(m4file).disposeM4, ())
                    t.start()
                    t.join()
                    thread_list.append(t)
                for t in thread_list:
                    t.join()
                    t_data.append(t.get_result())



                for data in t_data:
                    dkey = data.level + ' ' + data.year.zfill(2) + data.month.zfill(2) + data.day.zfill(2) + \
                           data.ftime.zfill(2) + '.' + data.aging.zfill(3)

                    sourceDict[dkey] = [data, data.m4data]




                if sourceDict.items():
                    #分组

                    bigDict = {k: dict(g) for k, g in groupby(sorted(sourceDict.items(), key=lambda x: x[0]), key=lambda x: x[0].split(' ')[0])}

                    #头信息
                    di = list(bigDict[list(bigDict.keys())[0]].values())[0][0]
                    #dataarray = bigDict.values()[0].values()[0]

                    description = re.findall('\w+_\w+', di.desc)
                    year = di.year
                    month = di.month
                    day = di.day
                    ftime = di.ftime
                    aging = di.aging
                    level = di.level
                    LatGridNumber = di.LatGridNumber
                    LonGridNumber = di.LonGridNumber
                    ContourInterval = di.ContourInterval
                    ContourStartValue = di.ContourStartValue
                    ContourEndValue = di.ContourEndValue
                    SmoothnessCoefficient = di.SmoothnessCoefficient
                    ThickenedLineValue = di.ThickenedLineValue

                    # print headdata
                    londistance = di.LonGridLength
                    latdistance =di.LatGridLength
                    startlon = di.StartLon
                    endlon = di.EndLon
                    startlat = di.StartLat
                    endlat = di.EndLat

                    longitudes = np.arange(startlon, endlon + londistance, londistance)
                    longitudes = longitudes[0:LonGridNumber]
                    latitudes = np.arange(startlat, endlat + latdistance, latdistance)
                    latitudes = latitudes[0:LatGridNumber]
                    setList = []

                    for kv in bigDict.keys():
                        setList.append(len(bigDict[kv]))

                    if len(set(setList)) == 1:
                        try:
                            hdf = nc.Dataset(destinationPath, 'w', format="NETCDF4")
                        except Exception:
                            if os.path.exists(destinationPath):
                                ncfile = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.hdf'
                                destinationPath = os.path.join(destinationPath, ncfile)
                                hdf = nc.Dataset(destinationPath, 'w', format="NETCDF4")
                            else:
                                (filepath, tempfilename) = os.path.split(destinationPath)
                                if not os.path.exists(filepath):
                                    os.makedirs(filepath)
                                if os.path.exists(destinationPath):
                                    ncfile = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.hdf'
                                    destinationPath = os.path.join(destinationPath, ncfile)
                                    hdf = nc.Dataset(destinationPath, 'w', format="NETCDF4")
                                else:
                                    hdf = nc.Dataset(destinationPath, 'w', format="NETCDF4")

                        grp = hdf.createGroup('Micaps')
                        grp.createDimension('latitude', len(latitudes))
                        grp.createDimension('longitude', len(longitudes))
                        grp.createDimension('time', None)
                        grp.createDimension('level', None)
                        grp.createDimension('aging', None)

                        # 创建文件变量

                        vlatitudes = grp.createVariable('latitude', 'f8', ('latitude',))
                        vlongitudes = grp.createVariable('longitude', 'f8', ('longitude',))

                        vtime = grp.createVariable("time", 'f8', ("time",))
                        vlevel = grp.createVariable("level", 'i4', ("level",))
                        vaging = grp.createVariable("aging", np.str, ("aging",))
                        lvtemperature = grp.createVariable(variablename if variablename else 'variable000', "f8",("time", "level", "latitude", "longitude",))



                        # 对nc文件增加说明变量
                        hdf.year = year
                        hdf.month = month
                        hdf.day = day
                        hdf.time = ftime
                        hdf.aging = aging
                        hdf.level = level

                        hdf.LonGridLength = di.LonGridLength
                        hdf.LatGridLength = di.LatGridLength
                        hdf.StartLon = di.StartLon
                        hdf.EndLon = di.EndLon
                        hdf.StartLat = di.StartLat
                        hdf.EndLat = di.EndLat

                        hdf.LatGridNumber = LatGridNumber
                        hdf.LonGridNumber = LonGridNumber
                        hdf.ContourInterval = ContourInterval
                        hdf.ContourStartValue = ContourStartValue
                        hdf.ContourEndValue = ContourEndValue
                        hdf.SmoothnessCoefficient = SmoothnessCoefficient
                        hdf.ThickenedLineValue = ThickenedLineValue
                        hdf.description = description
                        hdf.history = 'Created ' + time.ctime(time.time())
                        hdf.source = "m4file operate hdf file"
                        hdf.flag = "m42hdf"

                        vlatitudes.units = 'degrees north'
                        vlatitudes.axis = "Y"
                        vlongitudes.units = 'degrees east'
                        vlongitudes.axis = "X"
                        #vtemperature.units = 'Centigrade'

                        lvtemperature.units = 'Centigrade'

                        vlevel.units = 'hPa'
                        vlevel.axis = "Z"
                        vlevel.standard_name = "level"
                        tunit = year.zfill(2) + month.zfill(2) + day.zfill(2) + ftime.zfill(2)
                        tun = datetime.datetime.strptime(tunit, '%y%m%d%H')
                        tu = tun.strftime('%Y-%m-%d %H:%M:%S')

                        #vtime.units = "hours since " + tu
                        vtime.start_date = tu
                        vtime.standard_name = "time"
                        vtime.axis = "T"
                        vtime.units = "hours since 0001-01-01 00:00:00.0"
                        vtime.calendar = "gregorian"
                        vaging.standard_name = 'aging'


                        # 按照变量的赋值
                        vlongitudes[:] = longitudes[:]
                        vlatitudes[:] = latitudes[:]


                        times_data = []
                        level_data = []
                        aging_data = []
                        for i, kv in enumerate(sorted(bigDict.items())):  # 四维赋值
                            level_data.append(float(kv[0]) if kv[0] != '' else 0)
                            for j, lkv in enumerate(sorted(kv[1].items())):
                                a = str(lkv[0]).split(' ')[1]
                                aging_data.append(a)
                                tdate = datetime.datetime.strptime(a.split('.')[0], '%y%m%d%H') + datetime.timedelta(hours=int(a.split('.')[1]))
                                times_data.append(tdate)

                                lvtemperature[j, i, :, :] = lkv[1][1]

                        vtime[:] = nc.date2num(times_data, units=vtime.units, calendar=vtime.calendar)
                        vlevel[:] = level_data
                        vaging[:] = np.array(aging_data)
                        hdf.close()
                        print('inner: Successful hdf file generation')
                        return 0
                    else:
                        print("The Micaps file count error!")
                        return "The Micaps file count error!"

            else:
                print('the path [{}] is empty!'.format(sourcePath))
                return 'the path [{}] is empty!'.format(sourcePath)
        else:
            print('the path [{}] is not exist!'.format(sourcePath))
            return 'the path [{}] is not exist!'.format(sourcePath)
    except Exception as arg:
        print('ERROR', arg)
        logging.error('ERROR' + ':' + str(arg))
        return 'ERROR:' + str(arg)

def m4_to_hdfGenNCfile(sourcePath,destinationPath,variablename):

    '''

    @名称: 批量m4文件生成nc文件
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
    @使用范例: disposeM4('./15121008.000')
    '''
    try:
        if isinstance(sourcePath, list) and len(sourcePath) >= 1:



            if sourcePath:
                sourceDict = dict()
                thread_list = []
                t_data = []
                for m4file in sourcePath:
                    #t = threading.Thread(target=disposeM4, args=(m4file, ))
                    t = MyThread(DisposeM4file(m4file).disposeM4, ())
                    t.start()
                    t.join()
                    thread_list.append(t)
                for t in thread_list:
                    t.join()
                    t_data.append(t.get_result())



                for data in t_data:
                    dkey = data.level + ' ' + data.year.zfill(2) + data.month.zfill(2) + data.day.zfill(2) + \
                           data.ftime.zfill(2) + '.' + data.aging.zfill(3)

                    sourceDict[dkey] = [data, data.m4data]




                if sourceDict.items():
                    #分组

                    bigDict = {k: dict(g) for k, g in groupby(sorted(sourceDict.items(), key=lambda x: x[0]), key=lambda x: x[0].split(' ')[0])}

                    #头信息
                    di = list(bigDict[list(bigDict.keys())[0]].values())[0][0]

                    description = re.findall('\w+_\w+', di.desc)
                    year = di.year
                    month = di.month
                    day = di.day
                    ftime = di.ftime
                    aging = di.aging
                    level = di.level
                    LatGridNumber = di.LatGridNumber
                    LonGridNumber = di.LonGridNumber
                    ContourInterval = di.ContourInterval
                    ContourStartValue = di.ContourStartValue
                    ContourEndValue = di.ContourEndValue
                    SmoothnessCoefficient = di.SmoothnessCoefficient
                    ThickenedLineValue = di.ThickenedLineValue

                    # print headdata
                    londistance = di.LonGridLength
                    latdistance =di.LatGridLength
                    startlon = di.StartLon
                    endlon = di.EndLon
                    startlat = di.StartLat
                    endlat = di.EndLat

                    longitudes = np.arange(startlon, endlon + londistance, londistance)
                    longitudes = longitudes[0:LonGridNumber]
                    latitudes = np.arange(startlat, endlat + latdistance, latdistance)
                    latitudes = latitudes[0:LatGridNumber]
                    setList = []

                    for kv in bigDict.keys():
                        setList.append(len(bigDict[kv]))

                    if len(set(setList)) == 1:
                        try:
                            hdf = nc.Dataset(destinationPath, 'w', format="NETCDF4")
                        except Exception:
                            if os.path.exists(destinationPath):
                                ncfile = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.hdf'
                                destinationPath = os.path.join(destinationPath, ncfile)
                                hdf = nc.Dataset(destinationPath, 'w', format="NETCDF4")
                            else:
                                (filepath, tempfilename) = os.path.split(destinationPath)
                                if not os.path.exists(filepath):
                                    os.makedirs(filepath)
                                if os.path.exists(destinationPath):
                                    ncfile = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.hdf'
                                    destinationPath = os.path.join(destinationPath, ncfile)
                                    hdf = nc.Dataset(destinationPath, 'w', format="NETCDF4")
                                else:
                                    hdf = nc.Dataset(destinationPath, 'w', format="NETCDF4")

                        grp = hdf.createGroup('Micaps')
                        grp.createDimension('latitude', len(latitudes))
                        grp.createDimension('longitude', len(longitudes))
                        grp.createDimension('time', None)
                        grp.createDimension('level', None)
                        grp.createDimension('aging', None)

                        # 创建文件变量

                        vlatitudes = grp.createVariable('latitude', 'f8', ('latitude',))
                        vlongitudes = grp.createVariable('longitude', 'f8', ('longitude',))

                        vtime = grp.createVariable("time", 'f8', ("time",))
                        vlevel = grp.createVariable("level", 'i4', ("level",))
                        vaging = grp.createVariable("aging", np.str, ("aging",))
                        lvtemperature = grp.createVariable(variablename if variablename else 'variable000', "f8",("time", "level", "latitude", "longitude",))



                        # 对nc文件增加说明变量
                        hdf.year = year
                        hdf.month = month
                        hdf.day = day
                        hdf.time = ftime
                        hdf.aging = aging
                        hdf.level = level

                        hdf.LonGridLength = di.LonGridLength
                        hdf.LatGridLength = di.LatGridLength
                        hdf.StartLon = di.StartLon
                        hdf.EndLon = di.EndLon
                        hdf.StartLat = di.StartLat
                        hdf.EndLat = di.EndLat

                        hdf.LatGridNumber = LatGridNumber
                        hdf.LonGridNumber = LonGridNumber
                        hdf.ContourInterval = ContourInterval
                        hdf.ContourStartValue = ContourStartValue
                        hdf.ContourEndValue = ContourEndValue
                        hdf.SmoothnessCoefficient = SmoothnessCoefficient
                        hdf.ThickenedLineValue = ThickenedLineValue
                        hdf.description = description
                        hdf.history = 'Created ' + time.ctime(time.time())
                        hdf.source = "m4file operate hdf file"
                        hdf.flag = "m42hdf"

                        vlatitudes.units = 'degrees north'
                        vlatitudes.axis = "Y"
                        vlongitudes.units = 'degrees east'
                        vlongitudes.axis = "X"
                        #vtemperature.units = 'Centigrade'

                        lvtemperature.units = 'Centigrade'

                        vlevel.units = 'hPa'
                        vlevel.axis = "Z"
                        vlevel.standard_name = "level"
                        tunit = year.zfill(2) + month.zfill(2) + day.zfill(2) + ftime.zfill(2)
                        tun = datetime.datetime.strptime(tunit, '%y%m%d%H')
                        tu = tun.strftime('%Y-%m-%d %H:%M:%S')

                        #vtime.units = "hours since " + tu
                        vtime.start_date = tu
                        vtime.standard_name = "time"
                        vtime.axis = "T"
                        vtime.units = "hours since 0001-01-01 00:00:00.0"
                        vtime.calendar = "gregorian"
                        vaging.standard_name = 'aging'


                        # 按照变量的赋值
                        vlongitudes[:] = longitudes[:]
                        vlatitudes[:] = latitudes[:]

                        '''if len(bigDict.keys()) < 2:#三维赋值
    
                            ptemperature = grp.createVariable("temperature", "f8", ("time", "latitude", "longitude",))
    
                            for i, kv in enumerate(sorted(bigDict.items())):  # 三维赋值
                                # print i, kv[0]
                                vlevel[i] = kv[0]
                                for j, lkv in enumerate(sorted(kv[1].items())):
                                    a = str(lkv[0]).split(' ')[1]
                                    tdate = datetime.datetime.strptime(a.split('.')[0], '%y%m%d%H') + datetime.timedelta(days=int(a.split('.')[1]) / 24)
                                    vtime[j] = tdate.strftime('%Y-%m-%d %H')
                                    ptemperature[j, :, :] = lkv[1][1]'''

                        #print(bigDict)
                        times_data = []
                        level_data = []
                        aging_data = []
                        for i, kv in enumerate(sorted(bigDict.items())):  # 四维赋值

                            level_data.append(float(kv[0]) if kv[0] != '' else 0)
                            for j, lkv in enumerate(sorted(kv[1].items())):
                                a = str(lkv[0]).split(' ')[1]
                                # print(a.replace('.','-'))
                                aging_data.append(a)
                                tdate = datetime.datetime.strptime(a.split('.')[0], '%y%m%d%H') + datetime.timedelta(
                                    hours=int(a.split('.')[1]))
                                times_data.append(tdate)


                                lvtemperature[j, i, :, :] = lkv[1][1]

                        vtime[:] = nc.date2num(times_data, units=vtime.units, calendar=vtime.calendar)
                        vlevel[:] = level_data
                        vaging[:] = np.array(aging_data)

                        hdf.close()
                        print('inner: Successful hdf file generation')
                        return 0
                    else:
                        print("The Micaps file count error!")
                        return "The Micaps file count error!"

            else:
                print('the path [{}] is empty!'.format(sourcePath))
                return 'the path [{}] is empty!'.format(sourcePath)
        else:
            print('the path [{}] is not exist or error parameter type!'.format(sourcePath))
            return 'the path [{}] is not exist or error parameter type!'.format(sourcePath)
    except Exception as arg:
        print('ERROR', arg)
        logging.error('ERROR' + ':' + str(arg))
        return 'ERROR:' + str(arg)










if __name__ =='__main__':
    sourcePath = r'D:/PanoplyWin/t1/ER03/'
    destinationPath = r'D:/PanoplyWin/t1/hdf/2244.hdf'

    m4_to_hdf_batGenNCfile(sourcePath, destinationPath,'')
