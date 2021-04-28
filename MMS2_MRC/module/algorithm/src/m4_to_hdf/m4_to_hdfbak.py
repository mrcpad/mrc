# -*- coding: gbk -*-
import sys
import os
ppath = os.path.abspath('..')
ppath = os.path.join(ppath,'algorithm\src')
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
                    #t.join()
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

                    # print headdata
                    londistance = di.LonGridLength
                    latdistance =di.LatGridLength
                    startlon = di.StartLon
                    endlon = di.EndLon
                    startlat = di.StartLat
                    endlat = di.EndLat

                    longitudes = np.arange(startlon, endlon + londistance, londistance)
                    latitudes = np.arange(startlat, endlat + latdistance, latdistance)
                    # print longitudes

                    # 创建nc文件中dimension
                    if os.path.isdir(destinationPath):
                        ncfile = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.hdf'
                        destinationPath = os.path.join(destinationPath, ncfile)

                    hdf = nc.Dataset(destinationPath, 'w', format="NETCDF4")
                    grp = hdf.createGroup('m4')
                    grp.createDimension('latitude', len(latitudes))
                    grp.createDimension('longitude', len(longitudes))
                    grp.createDimension('time', None)
                    grp.createDimension('level', None)

                    # 创建文件变量

                    vlatitudes = grp.createVariable('latitude', 'f8', ('latitude',))
                    vlongitudes = grp.createVariable('longitude', 'f8', ('longitude',))

                    vtime = grp.createVariable("time", np.str, ("time",))
                    vlevel = grp.createVariable("level", np.int32, ("level",))
                    lvtemperature = grp.createVariable(variablename if variablename else 'four-variable', "f8",("level", "time", "latitude", "longitude",))



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
                    hdf.description = description
                    hdf.history = 'Created ' + time.ctime(time.time())
                    hdf.source = "m4file operate hdf file"
                    hdf.flag = "m4 to hdf"

                    vlatitudes.units = 'degrees north'
                    vlongitudes.units = 'degrees east'
                    #vtemperature.units = 'Centigrade'

                    lvtemperature.units = 'Centigrade'

                    vlevel.units = 'hPa'
                    vlevel.standard_name = "level"
                    tunit = year.zfill(2) + month.zfill(2) + day.zfill(2) + ftime.zfill(2)
                    tun = datetime.datetime.strptime(tunit, '%y%m%d%H')
                    tu = tun.strftime('%Y-%m-%d %H:%M:%S')

                    #vtime.units = "hours since " + tu
                    vtime.start_date = tu
                    vtime.standard_name = "time"


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
                    for i, kv in enumerate(sorted(bigDict.items())):#四维赋值
                        #print i, kv[0]
                        vlevel[i] = kv[0]
                        for j, lkv in enumerate(sorted(kv[1].items())):

                            a = str(lkv[0]).split(' ')[1]
                            tdate = datetime.datetime.strptime(a.split('.')[0], '%y%m%d%H') + datetime.timedelta(days=int(a.split('.')[1])/24)

                            vtime[j] = tdate.strftime('%Y-%m-%d %H')

                            lvtemperature[i, j, :, :] = lkv[1][1]

                    hdf.close()
                    print('inner: Successful hdf file generation')
                    return 0

            else:
                print('the path [{}] is empty!'.format(sourcePath))
        else:
            print('the path [{}] is not exist!'.format(sourcePath))
    except Exception as arg:
        print('ERROR', arg)
        logging.error('ERROR' + ':' + str(arg))










if __name__ =='__main__':

    sourcePath = r'/home/trywangdao/mrcpysrc/data/m4file/m4'
    destinationPath = r'/home/trywangdao/mrcpysrc/data/m4file/nc/t2'

    m4_to_hdf_batGenNCfile(sourcePath, destinationPath,'')
