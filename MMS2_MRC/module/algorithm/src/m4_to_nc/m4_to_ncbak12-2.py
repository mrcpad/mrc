# -*- coding: utf-8 -*-
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
from module.algorithm.src.m4.m4property import logginginfo



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



@logginginfo(level="INFO")
def m4_to_nc_batGenNCfile(sourcePath,destinationPath,variablename=None):


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
                ncfile = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.nc'
                destinationPath = os.path.join(destinationPath, ncfile)
            if not os.path.exists(destinationPath):
                newpath = destinationPath.split('\\')
                if len(newpath[-1].split('.')) > 1 and newpath[-1].split('.')[1] == 'nc':
                    npath = '\\'.join(destinationPath.split('\\')[:-1])
                    if not os.path.exists(npath):
                        os.makedirs(npath)
                else:
                    os.makedirs(destinationPath)
                    ncfile = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.nc'
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
                    #t.join()
                    thread_list.append(t)
                for t in thread_list:
                    t.join()
                    t_data.append(t.get_result())



                for data in t_data:
                    dkey = data.level + ' ' + data.year.zfill(2) + data.month.zfill(2) + data.day.zfill(2) + \
                           data.ftime.zfill(2) + '.' + data.aging.zfill(3)
                    #dkey = data[0][1][5] + ' ' + data[0][1][0].zfill(2) + data[0][1][1].zfill(2) + data[0][1][2].zfill(2) + \
                           #data[0][1][3].zfill(2) + '.' + data[0][1][4].zfill(3)
                    sourceDict[dkey] = [data, data.m4data]



                if sourceDict.items():
                    #print sourceDict.keys()
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
                    latdistance = di.LatGridLength
                    startlon = di.StartLon
                    endlon = di.EndLon
                    startlat = di.StartLat
                    endlat = di.EndLat


                    longitudes = np.arange(startlon, endlon + londistance, londistance)

                    longitudes = longitudes[0:LonGridNumber]
                    latitudes = np.arange(startlat, endlat + latdistance, latdistance)
                    latitudes = latitudes[0:LatGridNumber]
                    # print longitudes

                    # 创建nc文件中dimension
                    if os.path.isdir(destinationPath):
                        ncfile = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.nc'
                        destinationPath = os.path.join(destinationPath, ncfile)

                    nc_fid2 = nc.Dataset(destinationPath, 'w', format="NETCDF4")
                    nc_fid2.createDimension('latitude', len(latitudes))
                    nc_fid2.createDimension('longitude', len(longitudes))
                    nc_fid2.createDimension('time', None)
                    nc_fid2.createDimension('level', None)
                    nc_fid2.createDimension('aging', None)

                    # 创建文件变量

                    vlatitudes = nc_fid2.createVariable('latitude', 'f8', ('latitude',))
                    vlongitudes = nc_fid2.createVariable('longitude', 'f8', ('longitude',))
                    #vtemperature = nc_fid2.createVariable("tmp_temperature", "f8", ("latitude", "longitude",))

                    vtime = nc_fid2.createVariable("time", 'f8', ("time",))
                    vlevel = nc_fid2.createVariable("level", 'i4', ("level",))
                    vaging = nc_fid2.createVariable("aging", np.str, ("aging",))

                    #lvtemperature = nc_fid2.createVariable(variablename if variablename else 'four-variable', "f8", ("level", "time", "latitude", "longitude",))#四维变量
                    lvtemperature = nc_fid2.createVariable('variable000' if variablename == '' else variablename,"f8",("time", "level", "latitude", "longitude",))  # 四维变量



                    # 对nc文件增加说明变量
                    nc_fid2.year = year
                    nc_fid2.month = month
                    nc_fid2.day = day
                    nc_fid2.time = ftime
                    nc_fid2.aging = aging
                    nc_fid2.level = level

                    nc_fid2.LonGridLength = di.LonGridLength
                    nc_fid2.LatGridLength = di.LatGridLength
                    nc_fid2.StartLon = di.StartLon
                    nc_fid2.EndLon = di.EndLon
                    nc_fid2.StartLat = di.StartLat
                    nc_fid2.EndLat = di.EndLat



                    nc_fid2.LatGridNumber = LatGridNumber
                    nc_fid2.LonGridNumber = LonGridNumber
                    nc_fid2.ContourInterval = ContourInterval
                    nc_fid2.ContourStartValue = ContourStartValue
                    nc_fid2.ContourEndValue = ContourEndValue
                    nc_fid2.SmoothnessCoefficient = SmoothnessCoefficient
                    nc_fid2.ThickenedLineValue = ThickenedLineValue
                    nc_fid2.description = description
                    nc_fid2.history = 'Created ' + time.ctime(time.time())
                    nc_fid2.source = "m4file operate netcdf file"
                    nc_fid2.flag = "m42nc"
                    vlatitudes.units = 'degrees north'
                    vlatitudes.axis = "Y"
                    vlongitudes.units = 'degrees east'
                    vlongitudes.axis = "X"
                    #vtemperature.units = 'Centigrade'

                    lvtemperature.units = 'Centigrade'

                    vaging.standard_name = 'aging'


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

                    # 按照变量的赋值
                    vlongitudes[:] = longitudes[:]
                    vlatitudes[:] = latitudes[:]

                    times_data = []
                    level_data = []
                    aging_data = []


                    for i, kv in enumerate(sorted(bigDict.items())):#四维赋值
                        #print i, kv[0]
                        #vlevel[i] = kv[0]
                        level_data.append(kv[0])
                        for j, lkv in enumerate(sorted(kv[1].items())):

                            a = str(lkv[0]).split(' ')[1]
                            #print(a.replace('.','-'))
                            aging_data.append(a)
                            tdate = datetime.datetime.strptime(a.split('.')[0], '%y%m%d%H') + datetime.timedelta(hours=int(a.split('.')[1]))
                            times_data.append(tdate)

                            #vtime[j] = tdate.strftime('%Y-%m-%d %H')
                            #print(tdate.strftime('%Y-%m-%d %H'))
                            #vtime[j] = tdate.strftime('%Y-%m-%d %H') + '<-' + a
                            #vtime[j] = a
                            #print(tdate.strftime('%Y-%m-%d %H') + ':' + a)

                            lvtemperature[j, i, :, :] = lkv[1][1]
                    vtime[:] = nc.date2num(times_data, units=vtime.units, calendar=vtime.calendar)
                    vlevel[:] = level_data
                    vaging[:] = np.array(aging_data)





                    #print(bigDict)
                    # for i, kv in enumerate(sorted(bigDict.items())):#四维赋值
                    #     #print i, kv[0]
                    #     vlevel[i] = kv[0]
                    #     for j, lkv in enumerate(sorted(kv[1].items())):
                    #
                    #         a = str(lkv[0]).split(' ')[1]
                    #         tdate = datetime.datetime.strptime(a.split('.')[0], '%y%m%d%H') + datetime.timedelta(hours=int(a.split('.')[1]))
                    #
                    #         vtime[j] = tdate.strftime('%Y-%m-%d %H')
                    #         #print(tdate.strftime('%Y-%m-%d %H'))
                    #         #vtime[j] = tdate.strftime('%Y-%m-%d %H') + ':' + a
                    #         #vtime[j] = a
                    #         #print(tdate.strftime('%Y-%m-%d %H') + ':' + a)
                    #
                    #         lvtemperature[i, j, :, :] = lkv[1][1]

                    nc_fid2.close()
                    print('inner: Successful nc file generation')
                    return 0

            else:
                print('the path [{}] is empty!'.format(sourcePath))
        else:
            print('the path [{}] is not exist!'.format(sourcePath))
    except Exception as arg:
        print('ERROR', arg)
        logging.error('ERROR' + ':' + str(arg))










if __name__ =='__main__':

    sourcePath = r'D:\PanoplyWin\t1\ER03'
    destinationPath = 'D:\\PanoplyWin\\t1\\nc\\1.nc'

    m4_to_nc_batGenNCfile(sourcePath, destinationPath,'')
