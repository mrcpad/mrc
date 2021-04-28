# -*- coding: utf-8 -*-
import sys
import os
import datetime
import logging
import numpy as np
import netCDF4 as nc
from cdo import *
import pygrib
import time
import ncepgrib2
from functools import reduce
from grib.write.wGRIB.nwfd_g2lib import Data2Grib
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



class NetCDFtoGRIB(BaseFile):

    def __init__(self, ncFilePath,outPath,condtion):
        self.flag = 1
        self.ncFilePath = ncFilePath
        if os.path.exists(self.ncFilePath):
            self.nc = Dataset(ncFilePath, 'r',)
            self.condtion = condtion
            self.outPath = outPath
            self.getlatANDlon()
            self.VerifyData()
            self.griblist = list()
            if self.condtion:
                if self.nc.variables:
                    self.setVaribale()
                    if self.griblist:
                        with open(self.outPath,'wb') as gribFile:
                            for grib in self.griblist:
                                gribFile.write(grib.msg)
                        self.flag = 0
                if self.flag == 0:
                    print('inner: GRIB file generated successfully')

            else:

                if self.nc.variables:
                    self.nc_to_grib()
                    if self.griblist:
                        with open(self.outPath,'wb') as gribFile:
                            for grib in self.griblist:
                                gribFile.write(grib.msg)
                        self.flag = 0
                if self.flag == 0:
                    print('inner: GRIB file generated successfully')

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
                if len(self.nc.variables[cod].dimensions) == 4:  # 解析四维数据
                    if self.vleveldict:
                        pass
                    if self.vtimedict:
                        findex = self.nc.variables[cod].dimensions.index('time')
                        dtime = list(self.vtimedict.keys())
                        if len(dtime) > 1:
                            if len(list(self.vtimedict.keys())[0]) == 13:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                            elif len(list(self.vtimedict.keys())[0]) == 16:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H:%M')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M')
                            else:
                                tdate2 = datetime.datetime.strptime(dtime[1].split('+')[0], '%Y-%m-%d %H:%M:%S')
                                tdate1 = datetime.datetime.strptime(dtime[0].split('+')[0], '%Y-%m-%d %H:%M:%S')

                            self.faging = int((tdate2 - tdate1).total_seconds() / 3600)
                        elif len(dtime) == 1:
                            self.faging = 0

                        for lk, lvinx in self.vleveldict.items():

                            for tk, tvinx in self.vtimedict.items():
                                if len(tk) == 13:
                                    self.ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H')

                                elif len(tk) == 16:

                                    self.ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H:%M')
                                else:
                                    self.ltk = datetime.datetime.strptime(tk.split('+')[0], '%Y-%m-%d %H:%M:%S')

                                if findex == 0:

                                    if isinstance(self.nc.variables[cod][tvinx, lvinx, :, :], np.ma.core.MaskedArray):
                                        grib = self.nc_2_grib_smilped(self.nc.variables[cod][tvinx, lvinx, :, :].data, lk)
                                        self.griblist.append(grib)

                                    else:
                                        grib = self.nc_2_grib_smilped(self.nc.variables[cod][tvinx, lvinx, :, :], lk)
                                        self.griblist.append(grib)

                                else:

                                    if isinstance(self.nc.variables[cod][lvinx, tvinx, :, :], np.ma.core.MaskedArray):
                                        grib = self.nc_2_grib_smilped(self.nc.variables[cod][lvinx, tvinx, :, :].data, lk)
                                        self.griblist.append(grib)
                                    else:

                                        grib = self.nc_2_grib_smilped(self.nc.variables[cod][lvinx, tvinx, :, :], lk)
                                        self.griblist.append(grib)
                    else:
                        print('The file format is incorrect. Please confirm and try again')
            else:
                print('The Varibale ({cod}) does not exist'.format(cod=cod))



    def setNcattrs(self):
        self.outnc.setncatts(self.dictncattrs)

    def VerifyData(self):
        self.check = 0
        for var in self.nc.variables.keys():
            if len(self.nc.variables[var].dimensions) == 4:
                NcCount = reduce(lambda x,y:x*y,self.nc.variables[var].shape)
                print('Verify the integrity of NetCDF data:(file={f})'.format(f=self.ncFilePath))
                print('Check and Verify the Variable:(name={v})'.format(v=str(var)))
                print('Verify the integrity of NetCDF data:')
                print(self.nc.variables[var].dimensions)
                print(self.nc.variables[var].shape)

                print('LatGridNumber = {lat}, LonGridNumber = {lon}'.format(
                    lat=str(self.LatGridNumber), lon=str(self.LonGridNumber)))
                print('Total data :{tot}'.format(tot=str(len(self.nc.variables[var][:].reshape(-1,1)))))

                if NcCount == len(self.nc.variables[var][:].reshape(-1,1)):
                    print('NC file verification succeeded')

                else:
                    print('Failed to verify NetCDF data')
                    self.check = 1


    def getlatANDlon(self):

        lone = self.nc.get_variables_by_attributes(axis='X')
        if lone:
            self.long = lone[0][:]
            self.StartLon = self.long[0]
            self.EndLon = self.long[-1]
            self.LonGridNumber = len(self.long)
            self.LonGridLength = (self.EndLon - self.StartLon) / (self.LonGridNumber - 1)

        else:
            if self.nc.variables.get('longitude'):
                long = self.nc.variables.get('longitude')[:]
                self.StartLon = long[0]
                self.EndLon = long[-1]
                self.LonGridNumber = len(long)
                self.LonGridLength = (self.EndLon - self.StartLon) / (self.LonGridNumber - 1)
                # print(np.round(LonGridLength, decimals=2))
            elif self.nc.variables.get('lon'):
                long = self.nc.variables.get('lon')[:]
                self.StartLon = long[0]
                self.EndLon = long[-1]
                self.LonGridNumber = len(long)
                self.LonGridLength = (self.EndLon - self.StartLon) / (self.LonGridNumber - 1)

        late = self.nc.get_variables_by_attributes(axis='Y')
        if late:
            lat = late[0][:]
            self.StartLat = lat[0]
            self.EndLat = lat[-1]
            self.LatGridNumber = len(lat)
            self.LatGridLength = (self.EndLat - self.StartLat) / (self.LatGridNumber - 1)
        else:
            if self.nc.variables.get('latitude'):
                lat = self.nc.variables.get('latitude')[:]
                self.StartLat = lat[0]
                self.EndLat = lat[-1]
                self.LatGridNumber = len(lat)
                self.LatGridLength = (self.EndLat - self.StartLat) / (self.LatGridNumber - 1)
            elif self.nc.variables.get('lat'):
                lat = self.nc.variables.get('lat')[:]
                self.StartLat = lat[0]
                self.EndLat = lat[-1]
                self.LatGridNumber = len(lat)
                self.LatGridLength = (self.EndLat - self.StartLat) / (self.LatGridNumber - 1)
            else:
                pass

        vtime = self.nc.get_variables_by_attributes(axis='T')

        if vtime:
            if isinstance(vtime[:], np.ma.core.MaskedArray):
                td = nc.num2date(vtime[0][::].data, vtime[0].units)

            else:

                td = nc.num2date(vtime[0][::], vtime[0].units)
            self.vtimedict = dict(zip([str(tds) + '+' + str(idx) for idx, tds in enumerate(td)], range(len(td))))


        else:
            if self.nc.variables.get('time'):
                ftime = self.nc.variables.get('time', '')
                if ftime:
                    if isinstance(ftime[:], np.ma.core.MaskedArray):

                        nd = nc.num2date(ftime[::].data, ftime.units)
                        self.vtimedict = dict(zip([str(tds) for tds in nd.tolist()], range(len(nd.tolist()))))

                    else:
                        if ftime.dtype == np.str:
                            nd = ftime[:]
                        else:
                            nd = nc.num2date(ftime[::], ftime.units)
                        self.vtimedict = dict(zip([str(tds) for tds in nd.tolist()], range(len(nd.tolist()))))
            else:
                self.vtimedict = {}

        vlevel = self.nc.get_variables_by_attributes(axis='Z')

        if vlevel:
            self.vleveldict = dict(zip([str(lv) for lv in vlevel[0][:]], range(len(vlevel[0][:]))))

        else:
            if self.nc.variables.get('level'):
                seclevel = self.nc.variables.get('level')
                if seclevel:
                    ld = seclevel[:]
                    self.vleveldict = dict(zip([str(lv) for lv in ld.tolist()], range(len(ld.tolist()))))
            else:
                self.vleveldict = {}
        if self.vtimedict:

            if len(list(self.vtimedict.keys())[0]) == 13:
                self.ft = datetime.datetime.strptime(list(self.vtimedict.keys())[0], '%Y-%m-%d %H')
            elif len(list(self.vtimedict.keys())[0]) == 16:
                self.ft = datetime.datetime.strptime(list(self.vtimedict.keys())[0], '%Y-%m-%d %H:%M')
            elif len(list(self.vtimedict.keys())[0]) == 19:
                self.ft = datetime.datetime.strptime(list(self.vtimedict.keys())[0], '%Y-%m-%d %H:%M:%S')
            else:
                self.ft = datetime.datetime.now()
        else:
            self.ft = datetime.datetime.now()

    def nc_to_grib(self):
        '''
        nc文件转化grib文件
        :return:
        '''

        for var in self.nc.variables.keys():

            if len(self.nc.variables[var].dimensions) == 4:  # 解析四维数据
                print(self.nc.variables[var].shape)
                if self.vleveldict:
                    pass
                if self.vtimedict:
                    findex = self.nc.variables[var].dimensions.index('time')
                    dtime = list(self.vtimedict.keys())
                    if len(dtime) > 1:
                        if len(list(self.vtimedict.keys())[0]) == 13:
                            tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H')
                            tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                        elif len(list(self.vtimedict.keys())[0]) == 16:
                            tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H:%M')
                            tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M')
                        else:
                            tdate2 = datetime.datetime.strptime(dtime[1].split('+')[0], '%Y-%m-%d %H:%M:%S')
                            tdate1 = datetime.datetime.strptime(dtime[0].split('+')[0], '%Y-%m-%d %H:%M:%S')

                        self.faging = int((tdate2 - tdate1).total_seconds() / 3600)
                    elif len(dtime) == 1:
                        self.faging = 0



                    for lk, lvinx in self.vleveldict.items():

                        for tk, tvinx in self.vtimedict.items():
                            if len(tk) == 13:
                                self.ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H')

                            elif len(tk) == 16:

                                self.ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H:%M')
                            else:
                                self.ltk = datetime.datetime.strptime(tk.split('+')[0], '%Y-%m-%d %H:%M:%S')




                            if findex == 0:


                                if isinstance(self.nc.variables[var][tvinx, lvinx, :, :], np.ma.core.MaskedArray):
                                    grib = self.nc_2_grib_smilped(self.nc.variables[var][tvinx, lvinx, :, :].data, lk)
                                    self.griblist.append(grib)

                                else:
                                    grib = self.nc_2_grib_smilped(self.nc.variables[var][tvinx, lvinx, :, :], lk)
                                    self.griblist.append(grib)

                            else:

                                if isinstance(self.nc.variables[var][lvinx, tvinx, :, :], np.ma.core.MaskedArray):
                                    grib = self.nc_2_grib_smilped(self.nc.variables[var][lvinx, tvinx, :, :].data, lk)
                                    self.griblist.append(grib)
                                else:

                                    grib = self.nc_2_grib_smilped(self.nc.variables[var][lvinx, tvinx, :, :], lk)
                                    self.griblist.append(grib)
                else:
                    pass

    def nc_2_grib_smilped(self, ncdata, level):
        '''
        将一个micaps转码为grib2 message
        :param ncdata:
        :param category:
        :param element:
        :param statistical:
        :param leveltype:
        :param level:
        :param istimepoint:
        :param generating_method:生成方法
        :param status:
        :param discipline:
        :return:
        '''
        # 格点场数据
        field = ncdata.data if isinstance(ncdata, np.ma.core.MaskedArray) else ncdata


        # 读取配置获取产品编码信息
        # discipline = 0  # 学科
        year = self.ltk.year
        month = self.ltk.month
        day = self.ltk.day
        hour = self.ltk.hour
        minute = 0
        second = 0


        # status = 0  # 产品状态
        # category = 0 #产品种类
        # element = 0 #产品编号
        # statistical = 0 #统计方式 （模板4.8）
        # leveltype = 103 #层次类型
        # level = 2   #层次值
        forecasttime = int(self.faging)  # 距离预报基准日期时间的预报起报小时，如，0，3,6,9,12等

        # isforecast = True #是否是预报； True:是预报； False:为实况
        # istimepoint = True  #预报数据是否是某个时间点的数据； Ture:为某个时间点，False:为某个时间段
        timerange = 3  # 预报间隔小时数，如3,6,12,24等   ? 暂时写3,20191119
        curPath = os.path.abspath(os.path.dirname(__file__))
        g2lib = Data2Grib(os.path.join(curPath, 'grib_stb_config.conf'))


        ngrdpts = self.LatGridNumber * self.LonGridNumber


        g2lib.data2grib_info(self.StartLat, self.StartLon, self.EndLat, self.EndLon, self.LatGridLength, self.LonGridLength,
                             self.LatGridNumber, self.LonGridNumber)

        g2lib.data2grib_smiple(year, month, day, hour, minute,second, forecasttime, timerange, field, ngrdpts,level)
        return g2lib.message



if __name__ == '__main__':
    NetCDFtoGRIB(r'/home/trywangdao/mrcpysrc/m4/log/1/RH123.nc',r'./variable000.grb','variable000')