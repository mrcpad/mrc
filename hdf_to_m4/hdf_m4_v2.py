# -*- coding: gbk -*-
import datetime
from functools import reduce
import sys
import os
ppath = os.path.abspath('..')
sys.path.append(os.path.join(ppath, 'm4'))
import netCDF4 as nc
import numpy as np

from m4.m4property import Micaps4property
import shutil
from m4.m4property import logginginfo



class HDF_to_M4(Micaps4property):

    def __init__(self, hdfFilePath,outPath,condtion):
        self.flag = 1
        if os.path.exists(hdfFilePath):

            self.hdf = nc.Dataset(hdfFilePath, 'r', )
            self.condtion = condtion
            self.outPath = outPath
            fncattrs = self.hdf.ncattrs()
            self.dictncattrs = dict()
            for attr in fncattrs:  # 获取头信息
                self.dictncattrs[attr] = self.hdf.getncattr(attr)


            seclevel = '0'
            LonGridLength = '0'
            LatGridLength = '0'
            StartLon = '0'
            EndLon = '0'
            StartLat = '0'
            EndLat = '0'
            LatGridNumber = '0'
            LonGridNumber = '0'

            self.fg = self.dictncattrs.get('flag', '')
            if self.fg == 'm42hdf':
                self.agings = self.hdf.groups['m4'].variables['aging'][:]
                ft = datetime.datetime.strptime(self.agings[0].split('.')[0], '%y%m%d%H')

                ftt = ft.strftime('%y-%m-%d %H')
                ftyear = ftt.split('-')[0]
                self.year = self.dictncattrs.get('year', str(ftyear))
                self.month = self.dictncattrs.get('month', str(ft.month))
                self.day = self.dictncattrs.get('day', str(ft.day))
                self.ftime = self.dictncattrs.get('time', str(ft.hour))
                self.aging = self.dictncattrs.get('aging', '0')
                self.level = self.dictncattrs.get('level', str(seclevel))
                self.LonGridLength = self.dictncattrs.get('LonGridLength', str(LonGridLength))
                self.LatGridLength = self.dictncattrs.get('LatGridLength', str(LatGridLength))
                self.StartLon = self.dictncattrs.get('StartLon', str(StartLon))
                self.EndLon = self.dictncattrs.get('EndLon', str(EndLon))
                self.StartLat = self.dictncattrs.get('StartLat', str(StartLat))
                self.EndLat = self.dictncattrs.get('EndLat', str(EndLat))
                self.LatGridNumber = self.dictncattrs.get('LatGridNumber', str(LatGridNumber))
                self.LonGridNumber = self.dictncattrs.get('LonGridNumber', str(LonGridNumber))
                self.ContourInterval = self.dictncattrs.get('ContourInterval', '0')
                self.ContourStartValue = self.dictncattrs.get('ContourStartValue', '0')
                self.ContourEndValue = self.dictncattrs.get('ContourEndValue', '0')
                self.SmoothnessCoefficient = self.dictncattrs.get('SmoothnessCoefficient', '0')
                self.ThickenedLineValue = self.dictncattrs.get('ThickenedLineValue', '0')

                tdate = datetime.datetime.strptime(self.year + self.month + self.day + self.ftime, '%y%m%d%H')


                self.headinfo = [self.aging, str(self.level), self.LonGridLength, self.LatGridLength, self.StartLon,
                                 self.EndLon, self.StartLat, self.EndLat, self.LonGridNumber, self.LatGridNumber,
                                 self.ContourInterval, self.ContourStartValue, self.ContourEndValue,
                                 self.SmoothnessCoefficient, self.ThickenedLineValue]
                self.headinfo = self.headinfo[0:2] + ['{:.3f}'.format(float(info)) for info in self.headinfo[2:]]
                self.headinfo[8] = str(int(float(self.headinfo[8])))
                self.headinfo[9] = str(int(float(self.headinfo[9])))

                self.VerifyData()
                if self.check == 0:
                    print('Running HDF File Conversion......')
                    if self.condtion:
                        self.hdf_to_m4_condtion()
                    else:
                        self.hdf_to_m4()
                else:
                    print('Failed to verify HDF data')


            else:
                if self.hdf.groups:
                    for g in self.hdf.groups:


                        lone = self.hdf.groups[g].get_variables_by_attributes(axis='X')
                        if lone:
                            long = lone[0][:]
                            StartLon = long[0]
                            EndLon = long[-1]
                            LonGridNumber = len(long)
                            LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)

                        else:
                            if self.hdf.groups[g].variables.get('longitude'):
                                long = self.hdf.groups[g].variables.get('longitude')[:]
                                StartLon = long[0]
                                EndLon = long[-1]
                                LonGridNumber = len(long)
                                LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)
                                #print(np.round(LonGridLength, decimals=2))
                            elif self.hdf.groups[g].variables.get('lon'):
                                long = self.hdf.groups[g].variables.get('lon')[:]
                                StartLon = long[0]
                                EndLon = long[-1]
                                LonGridNumber = len(long)
                                LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)


                        late = self.hdf.groups[g].get_variables_by_attributes(axis='Y')
                        if late:
                            lat = late[0][:]
                            StartLat = lat[0]
                            EndLat = lat[-1]
                            LatGridNumber = len(lat)
                            LatGridLength = (EndLat - StartLat) / (LatGridNumber - 1)
                        else:
                            if self.hdf.groups[g].variables.get('latitude'):
                                lat = self.hdf.groups[g].variables.get('latitude')[:]
                                StartLat = lat[0]
                                EndLat = lat[-1]
                                LatGridNumber = len(lat)
                                LatGridLength = (EndLat - StartLat) / (LatGridNumber - 1)
                            elif self.hdf.groups[g].variables.get('lat'):
                                lat = self.hdf.groups[g].variables.get('lat')[:]
                                StartLat = lat[0]
                                EndLat = lat[-1]
                                LatGridNumber = len(lat)
                                LatGridLength = (EndLat - StartLat) / (LatGridNumber - 1)
                            else:
                                pass


                        vtime = self.hdf.groups[g].get_variables_by_attributes(axis='T')

                        if vtime:
                            if isinstance(vtime[0][:], np.ma.core.MaskedArray):
                                td = nc.num2date(vtime[0][::].data, vtime[0].units)
                            else:

                                td = nc.num2date(vtime[0][::], vtime[0].units)
                            self.vtimedict = dict(zip([str(tds) for tds in td.tolist()], range(len(td.tolist()))))

                        else:
                            if self.hdf.groups[g].variables.get('time'):
                                ftime = self.hdf.groups[g].variables.get('time','')
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




                        vlevel = self.hdf.groups[g].get_variables_by_attributes(axis='Z')

                        if vlevel:
                            ld = vlevel[0][:]
                            self.vleveldict = dict(zip([str(lv) for lv in ld.tolist()], range(len(ld.tolist()))))

                        else:
                            if self.hdf.groups[g].variables.get('level'):
                                seclevel = self.hdf.groups[g].variables.get('level')
                                if seclevel:
                                    ld = seclevel[:]
                                    self.vleveldict = dict(zip([str(lv) for lv in ld.tolist()], range(len(ld.tolist()))))
                            else:
                                self.vleveldict = {}
                        if self.vtimedict:

                            if len(list(self.vtimedict.keys())[0]) == 13:
                                ft = datetime.datetime.strptime(list(self.vtimedict.keys())[0], '%Y-%m-%d %H')
                            elif len(list(self.vtimedict.keys())[0]) == 16:
                                ft = datetime.datetime.strptime(list(self.vtimedict.keys())[0], '%Y-%m-%d %H:%M')
                            elif len(list(self.vtimedict.keys())[0]) == 19:
                                ft = datetime.datetime.strptime(list(self.vtimedict.keys())[0], '%Y-%m-%d %H:%M:%S')
                            else:
                                ft = datetime.datetime.now()
                        else:
                            ft = datetime.datetime.now()

                        self.year = self.dictncattrs.get('year', str(ft.year))
                        self.month = self.dictncattrs.get('month', str(ft.month))
                        self.day = self.dictncattrs.get('day', str(ft.day))
                        self.ftime = self.dictncattrs.get('time', str(ft.hour))
                        self.aging = self.dictncattrs.get('aging', '0')
                        self.level = self.dictncattrs.get('level', str(seclevel))
                        self.LonGridLength = self.dictncattrs.get('LonGridLength', str(LonGridLength))
                        self.LatGridLength = self.dictncattrs.get('LatGridLength', str(LatGridLength))
                        self.StartLon = self.dictncattrs.get('StartLon', str(StartLon))
                        self.EndLon = self.dictncattrs.get('EndLon', str(EndLon))
                        self.StartLat = self.dictncattrs.get('StartLat', str(StartLat))
                        self.EndLat = self.dictncattrs.get('EndLat', str(EndLat))
                        self.LatGridNumber = self.dictncattrs.get('LatGridNumber', str(LatGridNumber))
                        self.LonGridNumber = self.dictncattrs.get('LonGridNumber', str(LonGridNumber))
                        self.ContourInterval = self.dictncattrs.get('ContourInterval', '0')
                        self.ContourStartValue = self.dictncattrs.get('ContourStartValue', '0')
                        self.ContourEndValue = self.dictncattrs.get('ContourEndValue', '0')
                        self.SmoothnessCoefficient = self.dictncattrs.get('SmoothnessCoefficient', '0')
                        self.ThickenedLineValue = self.dictncattrs.get('ThickenedLineValue', '0')
                        #print(self.year + self.month + self.day + self.ftime)

                        #tdate = datetime.datetime.strptime(self.year + self.month + self.day + self.ftime, '%y%m%d%H')

                        self.headinfo = [self.aging, str(self.level), self.LonGridLength, self.LatGridLength, self.StartLon,
                                         self.EndLon, self.StartLat, self.EndLat, self.LonGridNumber, self.LatGridNumber,
                                         self.ContourInterval, self.ContourStartValue, self.ContourEndValue,
                                         self.SmoothnessCoefficient, self.ThickenedLineValue]
                        self.headinfo = self.headinfo[0:2] + ['{:.3f}'.format(float(info)) for info in self.headinfo[2:]]
                        self.headinfo[8] = str(int(float(self.headinfo[8])))
                        self.headinfo[9] = str(int(float(self.headinfo[9])))

                        self.VerifyData()
                        if self.check == 0:
                            print('Running HDF File Conversion......')
                            if self.condtion:
                                self.hdf_to_m4_v2_condtion(g)
                            else:
                                self.hdf_to_m4_v2(g)

                        else:
                            print('Failed to verify HDF data')
                else:
                    #################################

                    lone = self.hdf.get_variables_by_attributes(axis='X')
                    if lone:
                        long = lone[0][:]
                        StartLon = long[0]
                        EndLon = long[-1]
                        LonGridNumber = len(long)
                        LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)

                    else:
                        if self.hdf.variables.get('longitude'):
                            long = self.hdf.variables.get('longitude')[:]
                            StartLon = long[0]
                            EndLon = long[-1]
                            LonGridNumber = len(long)
                            LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)
                            #print(np.round(LonGridLength, decimals=2))
                        elif self.hdf.variables.get('lon'):
                            long = self.hdf.variables.get('lon')[:]
                            StartLon = long[0]
                            EndLon = long[-1]
                            LonGridNumber = len(long)
                            LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)


                    late = self.hdf.get_variables_by_attributes(axis='Y')
                    if late:
                        lat = late[0][:]
                        StartLat = lat[0]
                        EndLat = lat[-1]
                        LatGridNumber = len(lat)
                        LatGridLength = (EndLat - StartLat) / (LatGridNumber - 1)
                    else:
                        if self.hdf.variables.get('latitude'):
                            lat = self.hdf.variables.get('latitude')[:]
                            StartLat = lat[0]
                            EndLat = lat[-1]
                            LatGridNumber = len(lat)
                            LatGridLength = (EndLat - StartLat) / (LatGridNumber - 1)
                        elif self.hdf.variables.get('lat'):
                            lat = self.hdf.variables.get('lat')[:]
                            StartLat = lat[0]
                            EndLat = lat[-1]
                            LatGridNumber = len(lat)
                            LatGridLength = (EndLat - StartLat) / (LatGridNumber - 1)
                        else:
                            pass


                    vtime = self.hdf.get_variables_by_attributes(axis='T')

                    if vtime:
                        if isinstance(vtime[:], np.ma.core.MaskedArray):
                            td = nc.num2date(vtime[0][::].data, vtime[0].units)
                        else:

                            td = nc.num2date(vtime[0][::], vtime[0].units)
                        self.vtimedict = dict(zip([str(tds) for tds in td.tolist()], range(len(td.tolist()))))

                    else:
                        if self.hdf.variables.get('time'):
                            ftime = self.hdf.variables.get('time','')
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




                    vlevel = self.hdf.get_variables_by_attributes(axis='Z')

                    if vlevel:
                        ld = nc.num2date(vlevel[0][::], vlevel[0].units)
                        self.vleveldict = dict(zip([str(lv) for lv in ld.tolist()], range(len(ld.tolist()))))

                    else:
                        if self.hdf.variables.get('level'):
                            seclevel = self.hdf.variables.get('level')
                            if seclevel:
                                ld = seclevel[:]
                                self.vleveldict = dict(zip([str(lv) for lv in ld.tolist()], range(len(ld.tolist()))))
                        else:
                            self.vleveldict = {}
                    if self.vtimedict:

                        if len(list(self.vtimedict.keys())[0]) == 13:
                            ft = datetime.datetime.strptime(list(self.vtimedict.keys())[0], '%Y-%m-%d %H')
                        elif len(list(self.vtimedict.keys())[0]) == 16:
                            ft = datetime.datetime.strptime(list(self.vtimedict.keys())[0], '%Y-%m-%d %H:%M')
                        elif len(list(self.vtimedict.keys())[0]) == 19:
                            ft = datetime.datetime.strptime(list(self.vtimedict.keys())[0], '%Y-%m-%d %H:%M:%S')
                        else:
                            ft = datetime.datetime.now()
                    else:
                        ft = datetime.datetime.now()

                    self.year = self.dictncattrs.get('year', str(ft.year))
                    self.month = self.dictncattrs.get('month', str(ft.month))
                    self.day = self.dictncattrs.get('day', str(ft.day))
                    self.ftime = self.dictncattrs.get('time', str(ft.hour))
                    self.aging = self.dictncattrs.get('aging', '0')
                    self.level = self.dictncattrs.get('level', str(seclevel))
                    self.LonGridLength = self.dictncattrs.get('LonGridLength', str(LonGridLength))
                    self.LatGridLength = self.dictncattrs.get('LatGridLength', str(LatGridLength))
                    self.StartLon = self.dictncattrs.get('StartLon', str(StartLon))
                    self.EndLon = self.dictncattrs.get('EndLon', str(EndLon))
                    self.StartLat = self.dictncattrs.get('StartLat', str(StartLat))
                    self.EndLat = self.dictncattrs.get('EndLat', str(EndLat))
                    self.LatGridNumber = self.dictncattrs.get('LatGridNumber', str(LatGridNumber))
                    self.LonGridNumber = self.dictncattrs.get('LonGridNumber', str(LonGridNumber))
                    self.ContourInterval = self.dictncattrs.get('ContourInterval', '0')
                    self.ContourStartValue = self.dictncattrs.get('ContourStartValue', '0')
                    self.ContourEndValue = self.dictncattrs.get('ContourEndValue', '0')
                    self.SmoothnessCoefficient = self.dictncattrs.get('SmoothnessCoefficient', '0')
                    self.ThickenedLineValue = self.dictncattrs.get('ThickenedLineValue', '0')
                    #print(self.year + self.month + self.day + self.ftime)

                    #tdate = datetime.datetime.strptime(self.year + self.month + self.day + self.ftime, '%y%m%d%H')

                    self.headinfo = [self.aging, str(self.level), self.LonGridLength, self.LatGridLength, self.StartLon,
                                     self.EndLon, self.StartLat, self.EndLat, self.LonGridNumber, self.LatGridNumber,
                                     self.ContourInterval, self.ContourStartValue, self.ContourEndValue,
                                     self.SmoothnessCoefficient, self.ThickenedLineValue]
                    self.headinfo = self.headinfo[0:2] + ['{:.3f}'.format(float(info)) for info in self.headinfo[2:]]
                    self.headinfo[8] = str(int(float(self.headinfo[8])))
                    self.headinfo[9] = str(int(float(self.headinfo[9])))
                    self.hdf_to_m4_v3()
                    self.VerifyData()
                    if self.check == 0:
                        print('Running HDF File Conversion......')
                        if self.condtion:
                            self.hdf_to_m4_v3_condtion()
                        else:
                            self.hdf_to_m4_v3()
                    else:
                        print('Failed to verify HDF data')

        self.flag = 0



    def VerifyData(self):
        self.check = 0
        if self.hdf.groups:
            for g in self.hdf.groups:
                for var in self.hdf.groups[g].variables.keys():
                    if len(self.hdf.groups[g].variables[var].dimensions) >= 2:
                        HdfCount = reduce(lambda x, y: x * y, self.hdf.groups[g].variables[var].shape)
                        print('Check and Verify the Variable:(name={v})'.format(v=str(var)))
                        print('Verify the integrity of HDF data:')
                        print(self.hdf.groups[g].variables[var].dimensions)
                        print(self.hdf.groups[g].variables[var].shape)

                        print('LatGridNumber = {lat}, LonGridNumber = {lon}'.format(
                            lat=str(self.LatGridNumber), lon=str(self.LonGridNumber)))
                        print('Total data :{tot}'.format(tot=str(len(self.hdf.groups[g].variables[var][:].reshape(-1, 1)))))

                        if HdfCount == len(self.hdf.groups[g].variables[var][:].reshape(-1, 1)):
                            print('Verify HDF data successfully')

                        else:
                            print('Failed to verify HDF data')
                            self.check = 1

        else:


            for var in self.hdf.variables.keys():
                if len(self.hdf.variables[var].dimensions) >= 2:
                    NcCount = reduce(lambda x,y:x*y,self.hdf.variables[var].shape)
                    print('Check and Verify the Variable:(name={v})'.format(v=str(var)))
                    print('Verify the integrity of HDF data:')
                    print(self.hdf.variables[var].dimensions)
                    print(self.hdf.variables[var].shape)

                    print('LatGridNumber = {lat}, LonGridNumber = {lon}'.format(
                        lat=str(self.LatGridNumber), lon=str(self.LonGridNumber)))
                    print('Total data :{tot}'.format(tot=str(len(self.hdf.variables[var][:].reshape(-1,1)))))

                    if NcCount == len(self.hdf.variables[var][:].reshape(-1,1)):
                        print('Verify HDF data successfully')

                    else:
                        print('Failed to verify HDF data')
                        self.check = 1




    def hdf_to_m4_condtion(self):

        for cod in self.condtion.split():
            if cod in self.hdf.groups['m4'].variables.keys():

                if len(self.hdf.groups['m4'].variables[cod].dimensions) == 4:

                    self.timedict = dict(zip([str(tds) for tds in self.agings.tolist()], range(len(self.agings.tolist()))))

                    self.level = self.hdf.groups['m4'].variables.get('level')
                    self.leveldict = dict(
                        zip([str(lv) for lv in self.level[:].tolist()], range(len(self.level[:].tolist()))))

                    for lk, lvinx in self.leveldict.items():
                        if os.path.exists(os.path.join(os.path.join(self.outPath, cod), str(lk))):
                            shutil.rmtree(os.path.join(os.path.join(self.outPath, cod), str(lk)))
                            os.makedirs(os.path.join(os.path.join(self.outPath, cod), str(lk)))
                        else:
                            os.makedirs(os.path.join(os.path.join(self.outPath, cod), str(lk)))
                        for tk, tvinx in self.timedict.items():
                            aging = tk.split('.')[1]
                            self.headinfo[0] = aging
                            self.headinfo[1] = str(lk)
                            tdate2 = datetime.datetime.strptime(tk.split('.')[0], '%y%m%d%H')
                            startdate = tdate2.strftime('%Y%m%d%H')
                            enddate1 = tdate2 + datetime.timedelta(hours=int(aging))
                            enddate = enddate1.strftime('%Y%m%d%H')
                            titletdate = tk
                            flinedate = tdate2.strftime('%y %m %d %H ')
                            with open(os.path.join(os.path.join(os.path.join(self.outPath, cod), str(lk)), titletdate),
                                      'w') as nfc:

                                firstline = 'diamond 4 ' + str(cod) + '_' + startdate + '_' + enddate

                                secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                                nfc.write(firstline + '\n')
                                nfc.write(secondLine + '\n')
                                nfc.write('\n')

                                for d in self.hdf.groups['m4'].variables[cod][tvinx, lvinx, :, :]:
                                    for h in range(0, len(d), 10):
                                        # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                        nd = ''.join(
                                            [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                        nfc.write(nd)
                                    nfc.write('\n')
                else:
                    print('Dimension of the Variable ({cod}) is less than 4'.format(cod=cod))
                    '''
                    Dimension of the Variable ({cod}) is less than 4
                    '''

            else:
                print('The Variable ({cod}) does not exist'.format(cod=cod))




    @logginginfo(level="INFO")
    def hdf_to_m4(self):
        '''
        hdf文件转化m4文件
        :return:
        '''
        #try:

        #m4文件头信息

        if self.hdf.groups:
            for g in self.hdf.groups:
                for var in self.hdf.groups[g].variables.keys():
                    if len(self.hdf.groups[g].variables[var].dimensions) > 1:
                        if os.path.exists(os.path.join(self.outPath, g + '/' + var)):
                            shutil.rmtree(os.path.join(self.outPath, g + '/' + var))
                            os.makedirs(os.path.join(self.outPath, g + '/' + var))
                        else:
                            os.makedirs(os.path.join(self.outPath, g + '/' + var))
                        if len(self.hdf.groups[g].variables[var].dimensions) == 2:#解析二维数据
                            pass
                        elif len(self.hdf.groups[g].variables[var].dimensions) == 3:#解析三维数据
                           pass
                        elif len(self.hdf.groups[g].variables[var].dimensions) == 4:#解析四维数据
                            #if self.nc.variables[var].dimensions[0] == 'level'

                            self.timedict = dict(zip([str(tds) for tds in self.agings.tolist()], range(len(self.agings.tolist()))))

                            self.level = self.hdf.groups[g].variables.get('level')
                            self.leveldict = dict(zip([str(lv) for lv in self.level[:].tolist()], range(len(self.level[:].tolist()))))

                            for lk, lvinx in self.leveldict.items():
                                if os.path.exists(os.path.join(os.path.join(self.outPath, g + '/' + var), str(lk))):
                                    shutil.rmtree(os.path.join(os.path.join(self.outPath, g + '/' + var), str(lk)))
                                    os.makedirs(os.path.join(os.path.join(self.outPath, g + '/' + var), str(lk)))
                                else:
                                    os.makedirs(os.path.join(os.path.join(self.outPath, g + '/' + var), str(lk)))
                                for tk, tvinx in self.timedict.items():
                                    aging = tk.split('.')[1]
                                    self.headinfo[0] = aging
                                    self.headinfo[1] = str(lk)
                                    tdate2 = datetime.datetime.strptime(tk.split('.')[0], '%y%m%d%H')
                                    startdate = tdate2.strftime('%Y%m%d%H')
                                    enddate1 = tdate2 + datetime.timedelta(hours=int(aging))
                                    enddate = enddate1.strftime('%Y%m%d%H')
                                    titletdate = tk
                                    flinedate = tdate2.strftime('%y %m %d %H ')
                                    with open(os.path.join(os.path.join(os.path.join(self.outPath, g + '/' + var), str(lk)),titletdate), 'w') as nfc:

                                        firstline = 'diamond 4 ' + str(var) + '_' + startdate + '_' + enddate

                                        secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                                        nfc.write(firstline + '\n')
                                        nfc.write(secondLine + '\n')
                                        nfc.write('\n')

                                        for d in self.hdf.groups[g].variables[var][tvinx, lvinx, :, :]:
                                            for h in range(0, len(d), 10):
                                                # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                nd = ''.join(
                                                    [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                nfc.write(nd)
                                            nfc.write('\n')






        #
        #     return 0
        # except Exception as arg:
        #     print('ERROR', arg)

    def hdf_to_m4_v2(self,g):
        '''
        hdf文件转化m4文件
        :return:
        '''
        # try:

        # m4文件头信息

        for var in self.hdf.groups[g].variables.keys():
            if len(self.hdf.groups[g].variables[var].dimensions) > 1:

                if len(self.hdf.groups[g].variables[var].dimensions) == 2:  # 解析二维数据
                    if os.path.exists(os.path.join(self.outPath, g + '/' + var + '/999')):
                        shutil.rmtree(os.path.join(self.outPath, g + '/' + var + '/999'))
                        os.makedirs(os.path.join(self.outPath, g + '/' + var + '/999'))
                    else:
                        os.makedirs(os.path.join(self.outPath, g + '/' + var + '/999'))

                    ft = datetime.datetime.now()
                    aging = '0'

                    startdate = ft.strftime('%Y%m%d%H')
                    enddate1 = ft + datetime.timedelta(hours=0)
                    enddate = enddate1.strftime('%Y%m%d%H')
                    titletdate = ft.strftime('%y%m%d%H') + '.' + str(aging).zfill(3)
                    flinedate = ft.strftime('%y %m %d %H ')

                    with open(os.path.join(os.path.join(self.outPath, g + '/' + var + '/999'), titletdate), 'w') as nfc:

                        firstline = 'diamond 4 ' + str(var) + '_' + startdate + '_' + enddate

                        secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                        nfc.write(firstline + '\n')
                        nfc.write(secondLine + '\n')

                        nfc.write('\n')
                        if isinstance(self.hdf.groups[g].variables[var][:], np.ma.core.MaskedArray):
                            for d in self.hdf.groups[g].variables[var][:].data:
                                for i in range(0, len(d), 10):
                                    nd = ''.join([str(s).rjust(10, ' ') for s in d[i:i + 10]]) + '\n'
                                    nfc.write(nd)
                                nfc.write('\n')
                        else:

                            for d in self.nc.variables[var][:]:
                                for i in range(0, len(d), 10):
                                    nd = ''.join([str(s).rjust(10, ' ') for s in d[i:i + 10]]) + '\n'
                                    nfc.write(nd)
                                nfc.write('\n')
                elif len(self.hdf.groups[g].variables[var].dimensions) == 3:  # 解析三维数据
                    if self.vleveldict:
                        pass
                    if self.vtimedict:

                        dtime = list(self.vtimedict.keys())
                        if len(dtime) > 1:
                            if len(list(self.vtimedict.keys())[0]) == 13:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                            elif len(list(self.vtimedict.keys())[0]) == 16:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H:%M')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M')
                            else:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H:%M:%S')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M:%S')

                            aging = int((tdate2 - tdate1).total_seconds()/3600)
                            #print(aging)
                        elif len(dtime) == 1:
                            if len(list(self.vtimedict.keys())[0]) == 13:
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                            elif len(list(self.vtimedict.keys())[0]) == 16:

                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M')
                            else:
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M:%S')


                            aging = 0


                        lk = '999'
                        if os.path.exists(os.path.join(os.path.join(self.outPath, g + '/' + var), str(lk))):
                            shutil.rmtree(os.path.join(os.path.join(self.outPath, g + '/' + var), str(lk)))
                            os.makedirs(os.path.join(os.path.join(self.outPath, g + '/' + var), str(lk)))
                        else:
                            os.makedirs(os.path.join(os.path.join(self.outPath, g + '/' + var), str(lk)))
                        for tk, tvinx in self.vtimedict.items():

                            if len(tk) == 13:
                                ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H')

                            elif len(tk) == 16:

                                ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H:%M')
                            else:
                                ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H:%M:%S')

                            aging = int((ltk - tdate1).total_seconds() / 3600)
                            self.headinfo[0] = aging
                            self.headinfo[1] = str(lk)

                            startdate = ltk.strftime('%Y%m%d%H')
                            enddate1 = ltk + datetime.timedelta(hours=aging)
                            enddate = enddate1.strftime('%Y%m%d%H')
                            titletdate = ltk.strftime('%y%m%d%H') + '.' + str(aging).zfill(3)
                            flinedate = ltk.strftime('%y %m %d %H ')
                            with open(os.path.join(os.path.join(os.path.join(self.outPath, g + '/' + var), str(lk)), titletdate),
                                      'w') as nfc:

                                firstline = 'diamond 4 ' + str(var) + '_' + startdate + '_' + enddate

                                secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                                nfc.write(firstline + '\n')
                                nfc.write(secondLine + '\n')
                                nfc.write('\n')
                                if isinstance(self.hdf.groups[g].variables[var][tvinx, :, :], np.ma.core.MaskedArray):
                                    for d in self.hdf.groups[g].variables[var][tvinx, :, :].data:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join(
                                                [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')
                                else:

                                    for d in self.hdf.groups[g].variables[var][tvinx, :, :]:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')
                    else:
                        layers = self.hdf.groups[g].variables.get(self.hdf.groups[g].variables[var].dimensions[0])
                        if layers:
                            ld = layers[:]
                            self.vlayerdict = dict(zip([str(lv) for lv in ld.tolist()], range(len(ld.tolist()))))
                            ltk = datetime.datetime.now()
                            tdate1 = datetime.datetime.now()
                            #num = self.nc.variables[var].shape[0]

                            aging = int((ltk - tdate1).total_seconds() / 3600)
                            self.headinfo[0] = aging

                            startdate = ltk.strftime('%Y%m%d%H')
                            enddate1 = ltk + datetime.timedelta(hours=aging)
                            enddate = enddate1.strftime('%Y%m%d%H')
                            titletdate = ltk.strftime('%y%m%d%H') + '.' + str(aging).zfill(3)
                            flinedate = ltk.strftime('%y %m %d %H ')
                            for layer,index in self.vlayerdict.items():
                                if os.path.exists(os.path.join(self.outPath, var + '/' + layer)):
                                    shutil.rmtree(os.path.join(self.outPath, var + '/' + layer))
                                    os.makedirs(os.path.join(self.outPath, var + '/' + layer))
                                else:
                                    os.makedirs(os.path.join(self.outPath, var + '/' + layer))
                                self.headinfo[1] = str(layer)
                                with open(os.path.join(os.path.join(os.path.join(self.outPath, g + '/' + var), str(layer)), titletdate),
                                          'w') as nfc:

                                    firstline = 'diamond 4 ' + str(var) + '_' + startdate + '_' + enddate

                                    secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                                    nfc.write(firstline + '\n')
                                    nfc.write(secondLine + '\n')
                                    nfc.write('\n')

                                    if isinstance(self.hdf.groups[g].variables[var][index, :, :], np.ma.core.MaskedArray):
                                        for d in self.hdf.groups[g].variables[var][index, :, :].data:
                                            for h in range(0, len(d), 10):
                                                # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                nd = ''.join(
                                                    [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                nfc.write(nd)
                                            nfc.write('\n')
                                    else:

                                        for d in self.hdf.groups[g].variables[var][index, :, :]:
                                            for h in range(0, len(d), 10):
                                                # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                nd = ''.join(
                                                    [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                nfc.write(nd)
                                            nfc.write('\n')






                elif len(self.hdf.groups[g].variables[var].dimensions) == 4:  # 解析四维数据
                    if self.vleveldict:
                        pass
                    if self.vtimedict:
                        findex = self.hdf.groups[g].variables[var].dimensions.index('time')
                        dtime = list(self.vtimedict.keys())
                        if len(dtime) > 1:
                            if len(list(self.vtimedict.keys())[0]) == 13:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                            elif len(list(self.vtimedict.keys())[0]) == 16:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H:%M')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M')
                            else:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H:%M:%S')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M:%S')

                            faging = int((tdate2 - tdate1).total_seconds()/3600)
                        elif len(dtime) == 1:
                            if len(list(self.vtimedict.keys())[0]) == 13:
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                            elif len(list(self.vtimedict.keys())[0]) == 16:

                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M')
                            else:
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M:%S')


                            aging = 0
                            lk = '999'




                        for lk, lvinx in self.vleveldict.items():
                            if os.path.exists(os.path.join(os.path.join(self.outPath, g + '/' + var), str(lk))):
                                shutil.rmtree(os.path.join(os.path.join(self.outPath, g + '/' + var), str(lk)))
                                os.makedirs(os.path.join(os.path.join(self.outPath, g + '/' + var), str(lk)))
                            else:
                                os.makedirs(os.path.join(os.path.join(self.outPath, g + '/' + var), str(lk)))
                            for tk, tvinx in self.vtimedict.items():
                                if len(tk) == 13:
                                    ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H')

                                elif len(tk) == 16:

                                    ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H:%M')
                                else:
                                    ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H:%M:%S')

                                aging = int((ltk - tdate1).total_seconds() / 3600)
                                self.headinfo[0] = aging
                                self.headinfo[1] = str(lk)

                                startdate = ltk.strftime('%Y%m%d%H')
                                enddate1 = ltk + datetime.timedelta(hours=faging)
                                enddate = enddate1.strftime('%Y%m%d%H')
                                titletdate = ltk.strftime('%y%m%d%H') + '.' + str(aging).zfill(3)
                                flinedate = ltk.strftime('%y %m %d %H ')
                                with open(os.path.join(os.path.join(os.path.join(self.outPath, g + '/' + var), str(lk)), titletdate),'w') as nfc:

                                    firstline = 'diamond 4 ' + str(var) + '_' + startdate + '_' + enddate

                                    secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                                    nfc.write(firstline + '\n')
                                    nfc.write(secondLine + '\n')
                                    nfc.write('\n')
                                    if findex == 0:
                                        if isinstance(self.hdf.groups[g].variables[var][tvinx, lvinx, :, :],np.ma.core.MaskedArray):
                                            for d in self.hdf.groups[g].variables[var][tvinx, lvinx, :, :].data:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in
                                                                  d[h:h + 10]]) + '\n'
                                                    # print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')
                                        else:

                                            for d in self.hdf.groups[g].variables[var][tvinx, lvinx, :, :]:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    #print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')
                                    else:

                                        if isinstance(self.hdf.groups[g].variables[var][lvinx, tvinx, :, :],np.ma.core.MaskedArray):

                                            for d in self.hdf.groups[g].variables[var][lvinx, tvinx, :, :].data:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in
                                                                  d[h:h + 10]]) + '\n'
                                                    # print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')
                                        else:

                                            for d in self.hdf.groups[g].variables[var][lvinx, tvinx, :, :]:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    #print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')

                    else:
                        pass









































        #
        #     return 0
        # except Exception as arg:
        #     print('ERROR', arg)




    def hdf_to_m4_v2_condtion(self,g):
        '''
        hdf文件转化m4文件
        :return:
        '''
        # try:

        # m4文件头信息


        for cod in self.condtion.split():
            if cod in self.hdf.groups[g].variables.keys():

                if len(self.hdf.groups[g].variables[cod].dimensions) == 2:  # 解析二维数据
                    if os.path.exists(os.path.join(self.outPath, g + '/' + cod + '/999')):
                        shutil.rmtree(os.path.join(self.outPath, g + '/' + cod + '/999'))
                        os.makedirs(os.path.join(self.outPath, g + '/' + cod + '/999'))
                    else:
                        os.makedirs(os.path.join(self.outPath, g + '/' + cod + '/999'))

                    ft = datetime.datetime.now()
                    aging = '0'

                    startdate = ft.strftime('%Y%m%d%H')
                    enddate1 = ft + datetime.timedelta(hours=0)
                    enddate = enddate1.strftime('%Y%m%d%H')
                    titletdate = ft.strftime('%y%m%d%H') + '.' + str(aging).zfill(3)
                    flinedate = ft.strftime('%y %m %d %H ')

                    with open(os.path.join(os.path.join(self.outPath, g + '/' + cod + '/999'), titletdate), 'w') as nfc:

                        firstline = 'diamond 4 ' + str(cod) + '_' + startdate + '_' + enddate

                        secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                        nfc.write(firstline + '\n')
                        nfc.write(secondLine + '\n')

                        nfc.write('\n')
                        if isinstance(self.hdf.groups[g].variables[cod][:], np.ma.core.MaskedArray):
                            for d in self.hdf.groups[g].variables[cod][:].data:
                                for i in range(0, len(d), 10):
                                    nd = ''.join([str(s).rjust(10, ' ') for s in d[i:i + 10]]) + '\n'
                                    nfc.write(nd)
                                nfc.write('\n')
                        else:

                            for d in self.nc.variables[cod][:]:
                                for i in range(0, len(d), 10):
                                    nd = ''.join([str(s).rjust(10, ' ') for s in d[i:i + 10]]) + '\n'
                                    nfc.write(nd)
                                nfc.write('\n')
                elif len(self.hdf.groups[g].variables[cod].dimensions) == 3:  # 解析三维数据
                    if self.vleveldict:
                        pass
                    if self.vtimedict:

                        dtime = list(self.vtimedict.keys())
                        if len(dtime) > 1:
                            if len(list(self.vtimedict.keys())[0]) == 13:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                            elif len(list(self.vtimedict.keys())[0]) == 16:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H:%M')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M')
                            else:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H:%M:%S')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M:%S')

                            aging = int((tdate2 - tdate1).total_seconds()/3600)
                            #print(aging)
                        elif len(dtime) == 1:
                            if len(list(self.vtimedict.keys())[0]) == 13:
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                            elif len(list(self.vtimedict.keys())[0]) == 16:

                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M')
                            else:
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M:%S')


                            aging = 0


                        lk = '999'
                        if os.path.exists(os.path.join(os.path.join(self.outPath, g + '/' + cod), str(lk))):
                            shutil.rmtree(os.path.join(os.path.join(self.outPath, g + '/' + cod), str(lk)))
                            os.makedirs(os.path.join(os.path.join(self.outPath, g + '/' + cod), str(lk)))
                        else:
                            os.makedirs(os.path.join(os.path.join(self.outPath, g + '/' + cod), str(lk)))
                        for tk, tvinx in self.vtimedict.items():

                            if len(tk) == 13:
                                ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H')

                            elif len(tk) == 16:

                                ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H:%M')
                            else:
                                ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H:%M:%S')

                            aging = int((ltk - tdate1).total_seconds() / 3600)
                            self.headinfo[0] = aging
                            self.headinfo[1] = str(lk)

                            startdate = ltk.strftime('%Y%m%d%H')
                            enddate1 = ltk + datetime.timedelta(hours=aging)
                            enddate = enddate1.strftime('%Y%m%d%H')
                            titletdate = ltk.strftime('%y%m%d%H') + '.' + str(aging).zfill(3)
                            flinedate = ltk.strftime('%y %m %d %H ')
                            with open(os.path.join(os.path.join(os.path.join(self.outPath, g + '/' + cod), str(lk)), titletdate),
                                      'w') as nfc:

                                firstline = 'diamond 4 ' + str(cod) + '_' + startdate + '_' + enddate

                                secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                                nfc.write(firstline + '\n')
                                nfc.write(secondLine + '\n')
                                nfc.write('\n')
                                if isinstance(self.hdf.groups[g].variables[cod][tvinx, :, :], np.ma.core.MaskedArray):
                                    for d in self.hdf.groups[g].variables[cod][tvinx, :, :].data:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join(
                                                [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')
                                else:

                                    for d in self.hdf.groups[g].variables[cod][tvinx, :, :]:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')
                    else:
                        layers = self.hdf.groups[g].variables.get(self.hdf.groups[g].variables[cod].dimensions[0])
                        ld = layers[:]
                        self.vlayerdict = dict(zip([str(lv) for lv in ld.tolist()], range(len(ld.tolist()))))
                        ltk = datetime.datetime.now()
                        tdate1 = datetime.datetime.now()
                        #num = self.nc.variables[var].shape[0]

                        aging = int((ltk - tdate1).total_seconds() / 3600)
                        self.headinfo[0] = aging

                        startdate = ltk.strftime('%Y%m%d%H')
                        enddate1 = ltk + datetime.timedelta(hours=aging)
                        enddate = enddate1.strftime('%Y%m%d%H')
                        titletdate = ltk.strftime('%y%m%d%H') + '.' + str(aging).zfill(3)
                        flinedate = ltk.strftime('%y %m %d %H ')
                        for layer,index in self.vlayerdict.items():
                            if os.path.exists(os.path.join(self.outPath, cod + '/' + layer)):
                                shutil.rmtree(os.path.join(self.outPath, cod + '/' + layer))
                                os.makedirs(os.path.join(self.outPath, cod + '/' + layer))
                            else:
                                os.makedirs(os.path.join(self.outPath, cod + '/' + layer))
                            self.headinfo[1] = str(layer)
                            with open(os.path.join(os.path.join(os.path.join(self.outPath, g + '/' + cod), str(layer)), titletdate),
                                      'w') as nfc:

                                firstline = 'diamond 4 ' + str(cod) + '_' + startdate + '_' + enddate

                                secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                                nfc.write(firstline + '\n')
                                nfc.write(secondLine + '\n')
                                nfc.write('\n')

                                if isinstance(self.hdf.groups[g].variables[cod][index, :, :], np.ma.core.MaskedArray):
                                    for d in self.hdf.groups[g].variables[cod][index, :, :].data:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join(
                                                [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')
                                else:

                                    for d in self.hdf.groups[g].variables[cod][index, :, :]:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join(
                                                [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')






                elif len(self.hdf.groups[g].variables[cod].dimensions) == 4:  # 解析四维数据
                    if self.vleveldict:
                        pass
                    if self.vtimedict:
                        findex = self.hdf.groups[g].variables[cod].dimensions.index('time')
                        dtime = list(self.vtimedict.keys())
                        if len(dtime) > 1:
                            if len(list(self.vtimedict.keys())[0]) == 13:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                            elif len(list(self.vtimedict.keys())[0]) == 16:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H:%M')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M')
                            else:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H:%M:%S')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M:%S')

                            faging = int((tdate2 - tdate1).total_seconds()/3600)
                        elif len(dtime) == 1:
                            if len(list(self.vtimedict.keys())[0]) == 13:
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                            elif len(list(self.vtimedict.keys())[0]) == 16:

                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M')
                            else:
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M:%S')


                            aging = 0
                            lk = '999'




                        for lk, lvinx in self.vleveldict.items():
                            if os.path.exists(os.path.join(os.path.join(self.outPath, g + '/' + cod), str(lk))):
                                shutil.rmtree(os.path.join(os.path.join(self.outPath, g + '/' + cod), str(lk)))
                                os.makedirs(os.path.join(os.path.join(self.outPath, g + '/' + cod), str(lk)))
                            else:
                                os.makedirs(os.path.join(os.path.join(self.outPath, g + '/' + cod), str(lk)))
                            for tk, tvinx in self.vtimedict.items():
                                if len(tk) == 13:
                                    ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H')

                                elif len(tk) == 16:

                                    ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H:%M')
                                else:
                                    ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H:%M:%S')

                                aging = int((ltk - tdate1).total_seconds() / 3600)
                                self.headinfo[0] = aging
                                self.headinfo[1] = str(lk)

                                startdate = ltk.strftime('%Y%m%d%H')
                                enddate1 = ltk + datetime.timedelta(hours=faging)
                                enddate = enddate1.strftime('%Y%m%d%H')
                                titletdate = ltk.strftime('%y%m%d%H') + '.' + str(aging).zfill(3)
                                flinedate = ltk.strftime('%y %m %d %H ')
                                with open(os.path.join(os.path.join(os.path.join(self.outPath, g + '/' + cod), str(lk)), titletdate),'w') as nfc:

                                    firstline = 'diamond 4 ' + str(cod) + '_' + startdate + '_' + enddate

                                    secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                                    nfc.write(firstline + '\n')
                                    nfc.write(secondLine + '\n')
                                    nfc.write('\n')
                                    if findex == 0:
                                        if isinstance(self.hdf.groups[g].variables[cod][tvinx, lvinx, :, :],np.ma.core.MaskedArray):
                                            for d in self.hdf.groups[g].variables[cod][tvinx, lvinx, :, :].data:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in
                                                                  d[h:h + 10]]) + '\n'
                                                    # print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')
                                        else:

                                            for d in self.hdf.groups[g].variables[cod][tvinx, lvinx, :, :]:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    #print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')
                                    else:

                                        if isinstance(self.hdf.groups[g].variables[cod][lvinx, tvinx, :, :],np.ma.core.MaskedArray):

                                            for d in self.hdf.groups[g].variables[cod][lvinx, tvinx, :, :].data:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in
                                                                  d[h:h + 10]]) + '\n'
                                                    # print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')
                                        else:

                                            for d in self.hdf.groups[g].variables[cod][lvinx, tvinx, :, :]:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    #print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')

                    else:
                        pass



    def hdf_to_m4_v3(self):
        '''

        :return:
        '''
        # try:

        # m4文件头信息

        for var in self.hdf.variables.keys():
            if len(self.hdf.variables[var].dimensions) > 1:

                if len(self.hdf.variables[var].dimensions) == 2:  # 解析二维数据
                    if os.path.exists(os.path.join(self.outPath, var + '/999')):
                        shutil.rmtree(os.path.join(self.outPath, var + '/999'))
                        os.makedirs(os.path.join(self.outPath, var + '/999'))
                    else:
                        os.makedirs(os.path.join(self.outPath, var + '/999'))
                    ft = datetime.datetime.now()
                    aging = '0'

                    startdate = ft.strftime('%Y%m%d%H')
                    enddate1 = ft + datetime.timedelta(hours=0)
                    enddate = enddate1.strftime('%Y%m%d%H')
                    titletdate = ft.strftime('%y%m%d%H') + '.' + str(aging).zfill(3)
                    flinedate = ft.strftime('%y %m %d %H ')

                    with open(os.path.join(os.path.join(self.outPath, var + '/999'), titletdate), 'w') as nfc:

                        firstline = 'diamond 4 ' + str(var) + '_' + startdate + '_' + enddate

                        secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                        nfc.write(firstline + '\n')
                        nfc.write(secondLine + '\n')

                        nfc.write('\n')
                        if isinstance(self.hdf.variables[var][:], np.ma.core.MaskedArray):
                            for d in self.hdf.variables[var][:].data:
                                for i in range(0, len(d), 10):
                                    nd = ''.join([str(s).rjust(10, ' ') for s in d[i:i + 10]]) + '\n'
                                    nfc.write(nd)
                                nfc.write('\n')
                        else:

                            for d in self.hdf.variables[var][:]:
                                for i in range(0, len(d), 10):
                                    nd = ''.join([str(s).rjust(10, ' ') for s in d[i:i + 10]]) + '\n'
                                    nfc.write(nd)
                                nfc.write('\n')
                elif len(self.hdf.variables[var].dimensions) == 3:  # 解析三维数据
                    if self.vleveldict:
                        pass
                    if self.vtimedict:

                        dtime = list(self.vtimedict.keys())
                        if len(dtime) > 1:
                            if len(list(self.vtimedict.keys())[0]) == 13:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                            elif len(list(self.vtimedict.keys())[0]) == 16:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H:%M')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M')
                            else:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H:%M:%S')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M:%S')

                            aging = int((tdate2 - tdate1).total_seconds()/3600)
                            #print(aging)
                        elif len(dtime) == 1:
                            if len(list(self.vtimedict.keys())[0]) == 13:
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                            elif len(list(self.vtimedict.keys())[0]) == 16:

                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M')
                            else:
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M:%S')


                            aging = 0


                        lk = '999'
                        if os.path.exists(os.path.join(os.path.join(self.outPath, var), str(lk))):
                            shutil.rmtree(os.path.join(os.path.join(self.outPath, var), str(lk)))
                            os.makedirs(os.path.join(os.path.join(self.outPath, var), str(lk)))
                        else:
                            os.makedirs(os.path.join(os.path.join(self.outPath, var), str(lk)))
                        for tk, tvinx in self.vtimedict.items():

                            if len(tk) == 13:
                                ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H')

                            elif len(tk) == 16:

                                ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H:%M')
                            else:
                                ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H:%M:%S')

                            aging = int((ltk - tdate1).total_seconds() / 3600)
                            self.headinfo[0] = aging
                            self.headinfo[1] = str(lk)

                            startdate = ltk.strftime('%Y%m%d%H')
                            enddate1 = ltk + datetime.timedelta(hours=aging)
                            enddate = enddate1.strftime('%Y%m%d%H')
                            titletdate = ltk.strftime('%y%m%d%H') + '.' + str(aging).zfill(3)
                            flinedate = ltk.strftime('%y %m %d %H ')
                            with open(os.path.join(os.path.join(os.path.join(self.outPath, var), str(lk)), titletdate),
                                      'w') as nfc:

                                firstline = 'diamond 4 ' + str(var) + '_' + startdate + '_' + enddate

                                secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                                nfc.write(firstline + '\n')
                                nfc.write(secondLine + '\n')
                                nfc.write('\n')
                                if isinstance(self.hdf.variables[var][tvinx, :, :], np.ma.core.MaskedArray):
                                    for d in self.hdf.variables[var][tvinx, :, :].data:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join(
                                                [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')
                                else:

                                    for d in self.hdf.variables[var][tvinx, :, :]:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')
                    else:
                        layers = self.hdf.variables.get(self.hdf.variables[var].dimensions[0])
                        ld = layers[:]
                        self.vlayerdict = dict(zip([str(lv) for lv in ld.tolist()], range(len(ld.tolist()))))
                        ltk = datetime.datetime.now()
                        tdate1 = datetime.datetime.now()
                        #num = self.nc.variables[var].shape[0]

                        aging = int((ltk - tdate1).total_seconds() / 3600)
                        self.headinfo[0] = aging

                        startdate = ltk.strftime('%Y%m%d%H')
                        enddate1 = ltk + datetime.timedelta(hours=aging)
                        enddate = enddate1.strftime('%Y%m%d%H')
                        titletdate = ltk.strftime('%y%m%d%H') + '.' + str(aging).zfill(3)
                        flinedate = ltk.strftime('%y %m %d %H ')
                        for layer,index in self.vlayerdict.items():
                            if os.path.exists(os.path.join(self.outPath, var + '/' + layer)):
                                shutil.rmtree(os.path.join(self.outPath, var + '/' + layer))
                                os.makedirs(os.path.join(self.outPath, var + '/' + layer))
                            else:
                                os.makedirs(os.path.join(self.outPath, var + '/' + layer))
                            self.headinfo[1] = str(layer)
                            with open(os.path.join(os.path.join(os.path.join(self.outPath, var), str(layer)), titletdate),
                                      'w') as nfc:

                                firstline = 'diamond 4 ' + str(var) + '_' + startdate + '_' + enddate

                                secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                                nfc.write(firstline + '\n')
                                nfc.write(secondLine + '\n')
                                nfc.write('\n')

                                if isinstance(self.hdf.variables[var][index, :, :], np.ma.core.MaskedArray):
                                    for d in self.hdf.variables[var][index, :, :].data:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join(
                                                [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')
                                else:

                                    for d in self.hdf.variables[var][index, :, :]:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join(
                                                [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')






                elif len(self.hdf.variables[var].dimensions) == 4:  # 解析四维数据
                    if self.vleveldict:
                        pass
                    if self.vtimedict:
                        findex = self.hdf.variables[var].dimensions.index('time')
                        dtime = list(self.vtimedict.keys())
                        if len(dtime) > 1:
                            if len(list(self.vtimedict.keys())[0]) == 13:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                            elif len(list(self.vtimedict.keys())[0]) == 16:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H:%M')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M')
                            else:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H:%M:%S')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M:%S')

                            faging = int((tdate2 - tdate1).total_seconds()/3600)
                            #print(aging)
                        elif len(dtime) == 1:
                            if len(list(self.vtimedict.keys())[0]) == 13:
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                            elif len(list(self.vtimedict.keys())[0]) == 16:

                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M')
                            else:
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M:%S')


                            aging = 0
                            lk = '999'




                        for lk, lvinx in self.vleveldict.items():
                            if os.path.exists(os.path.join(os.path.join(self.outPath, var), str(lk))):
                                shutil.rmtree(os.path.join(os.path.join(self.outPath, var), str(lk)))
                                os.makedirs(os.path.join(os.path.join(self.outPath, var), str(lk)))
                            else:
                                os.makedirs(os.path.join(os.path.join(self.outPath, var), str(lk)))
                            for tk, tvinx in self.vtimedict.items():
                                if len(tk) == 13:
                                    ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H')

                                elif len(tk) == 16:

                                    ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H:%M')
                                else:
                                    ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H:%M:%S')

                                aging = int((ltk - tdate1).total_seconds() / 3600)
                                self.headinfo[0] = aging
                                self.headinfo[1] = str(lk)
                                # print(tk)

                                startdate = ltk.strftime('%Y%m%d%H')
                                enddate1 = ltk + datetime.timedelta(hours=faging)
                                enddate = enddate1.strftime('%Y%m%d%H')
                                titletdate = ltk.strftime('%y%m%d%H') + '.' + str(aging).zfill(3)
                                flinedate = ltk.strftime('%y %m %d %H ')
                                with open(os.path.join(os.path.join(os.path.join(self.outPath, var), str(lk)), titletdate),'w') as nfc:

                                    firstline = 'diamond 4 ' + str(var) + '_' + startdate + '_' + enddate

                                    secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                                    nfc.write(firstline + '\n')
                                    nfc.write(secondLine + '\n')
                                    nfc.write('\n')
                                    if findex == 0:
                                        if isinstance(self.hdf.variables[var][tvinx, lvinx, :, :],np.ma.core.MaskedArray):
                                            for d in self.hdf.variables[var][tvinx, lvinx, :, :].data:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in
                                                                  d[h:h + 10]]) + '\n'
                                                    # print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')
                                        else:

                                            for d in self.hdf.variables[var][tvinx, lvinx, :, :]:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    #print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')
                                    else:

                                        if isinstance(self.hdf.variables[var][lvinx, tvinx, :, :],np.ma.core.MaskedArray):

                                            for d in self.hdf.variables[var][lvinx, tvinx, :, :].data:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in
                                                                  d[h:h + 10]]) + '\n'
                                                    # print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')
                                        else:

                                            for d in self.hdf.variables[var][lvinx, tvinx, :, :]:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    #print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')

                    else:
                        pass


        #
        #     return 0
        # except Exception as arg:
        #     print('ERROR', arg)

    def hdf_to_m4_v3_condtion(self):
        '''

        :return:
        '''
        # try:

        # m4文件头信息

        for cod in self.condtion.split():
            if cod in self.hdf.variables.keys():

                if len(self.hdf.variables[cod].dimensions) == 2:  # 解析二维数据
                    if os.path.exists(os.path.join(self.outPath, cod + '/999')):
                        shutil.rmtree(os.path.join(self.outPath, cod + '/999'))
                        os.makedirs(os.path.join(self.outPath, cod + '/999'))
                    else:
                        os.makedirs(os.path.join(self.outPath, cod + '/999'))
                    ft = datetime.datetime.now()
                    aging = '0'

                    startdate = ft.strftime('%Y%m%d%H')
                    enddate1 = ft + datetime.timedelta(hours=0)
                    enddate = enddate1.strftime('%Y%m%d%H')
                    titletdate = ft.strftime('%y%m%d%H') + '.' + str(aging).zfill(3)
                    flinedate = ft.strftime('%y %m %d %H ')

                    with open(os.path.join(os.path.join(self.outPath, cod + '/999'), titletdate), 'w') as nfc:

                        firstline = 'diamond 4 ' + str(cod) + '_' + startdate + '_' + enddate

                        secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                        nfc.write(firstline + '\n')
                        nfc.write(secondLine + '\n')

                        nfc.write('\n')
                        if isinstance(self.hdf.variables[cod][:], np.ma.core.MaskedArray):
                            for d in self.hdf.variables[cod][:].data:
                                for i in range(0, len(d), 10):
                                    nd = ''.join([str(s).rjust(10, ' ') for s in d[i:i + 10]]) + '\n'
                                    nfc.write(nd)
                                nfc.write('\n')
                        else:

                            for d in self.hdf.variables[cod][:]:
                                for i in range(0, len(d), 10):
                                    nd = ''.join([str(s).rjust(10, ' ') for s in d[i:i + 10]]) + '\n'
                                    nfc.write(nd)
                                nfc.write('\n')
                elif len(self.hdf.variables[cod].dimensions) == 3:  # 解析三维数据
                    if self.vleveldict:
                        pass
                    if self.vtimedict:

                        dtime = list(self.vtimedict.keys())
                        if len(dtime) > 1:
                            if len(list(self.vtimedict.keys())[0]) == 13:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                            elif len(list(self.vtimedict.keys())[0]) == 16:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H:%M')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M')
                            else:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H:%M:%S')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M:%S')

                            aging = int((tdate2 - tdate1).total_seconds()/3600)
                            #print(aging)
                        elif len(dtime) == 1:
                            if len(list(self.vtimedict.keys())[0]) == 13:
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                            elif len(list(self.vtimedict.keys())[0]) == 16:

                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M')
                            else:
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M:%S')


                            aging = 0


                        lk = '999'
                        if os.path.exists(os.path.join(os.path.join(self.outPath, cod), str(lk))):
                            shutil.rmtree(os.path.join(os.path.join(self.outPath, cod), str(lk)))
                            os.makedirs(os.path.join(os.path.join(self.outPath, cod), str(lk)))
                        else:
                            os.makedirs(os.path.join(os.path.join(self.outPath, cod), str(lk)))
                        for tk, tvinx in self.vtimedict.items():

                            if len(tk) == 13:
                                ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H')

                            elif len(tk) == 16:

                                ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H:%M')
                            else:
                                ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H:%M:%S')

                            aging = int((ltk - tdate1).total_seconds() / 3600)
                            self.headinfo[0] = aging
                            self.headinfo[1] = str(lk)

                            startdate = ltk.strftime('%Y%m%d%H')
                            enddate1 = ltk + datetime.timedelta(hours=aging)
                            enddate = enddate1.strftime('%Y%m%d%H')
                            titletdate = ltk.strftime('%y%m%d%H') + '.' + str(aging).zfill(3)
                            flinedate = ltk.strftime('%y %m %d %H ')
                            with open(os.path.join(os.path.join(os.path.join(self.outPath, cod), str(lk)), titletdate),
                                      'w') as nfc:

                                firstline = 'diamond 4 ' + str(cod) + '_' + startdate + '_' + enddate

                                secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                                nfc.write(firstline + '\n')
                                nfc.write(secondLine + '\n')
                                nfc.write('\n')
                                if isinstance(self.hdf.variables[cod][tvinx, :, :], np.ma.core.MaskedArray):
                                    for d in self.hdf.variables[cod][tvinx, :, :].data:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join(
                                                [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')
                                else:

                                    for d in self.hdf.variables[cod][tvinx, :, :]:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')
                    else:
                        layers = self.hdf.variables.get(self.hdf.variables[cod].dimensions[0])
                        ld = layers[:]
                        self.vlayerdict = dict(zip([str(lv) for lv in ld.tolist()], range(len(ld.tolist()))))
                        ltk = datetime.datetime.now()
                        tdate1 = datetime.datetime.now()
                        #num = self.nc.variables[var].shape[0]

                        aging = int((ltk - tdate1).total_seconds() / 3600)
                        self.headinfo[0] = aging

                        startdate = ltk.strftime('%Y%m%d%H')
                        enddate1 = ltk + datetime.timedelta(hours=aging)
                        enddate = enddate1.strftime('%Y%m%d%H')
                        titletdate = ltk.strftime('%y%m%d%H') + '.' + str(aging).zfill(3)
                        flinedate = ltk.strftime('%y %m %d %H ')
                        for layer,index in self.vlayerdict.items():
                            if os.path.exists(os.path.join(self.outPath, cod + '/' + layer)):
                                shutil.rmtree(os.path.join(self.outPath, cod + '/' + layer))
                                os.makedirs(os.path.join(self.outPath, cod + '/' + layer))
                            else:
                                os.makedirs(os.path.join(self.outPath, cod + '/' + layer))
                            self.headinfo[1] = str(layer)
                            with open(os.path.join(os.path.join(os.path.join(self.outPath, cod), str(layer)), titletdate),
                                      'w') as nfc:

                                firstline = 'diamond 4 ' + str(cod) + '_' + startdate + '_' + enddate

                                secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                                nfc.write(firstline + '\n')
                                nfc.write(secondLine + '\n')
                                nfc.write('\n')

                                if isinstance(self.hdf.variables[cod][index, :, :], np.ma.core.MaskedArray):
                                    for d in self.hdf.variables[cod][index, :, :].data:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join(
                                                [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')
                                else:

                                    for d in self.hdf.variables[cod][index, :, :]:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join(
                                                [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')






                elif len(self.hdf.variables[cod].dimensions) == 4:  # 解析四维数据
                    if self.vleveldict:
                        pass
                    if self.vtimedict:
                        findex = self.hdf.variables[cod].dimensions.index('time')
                        dtime = list(self.vtimedict.keys())
                        if len(dtime) > 1:
                            if len(list(self.vtimedict.keys())[0]) == 13:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                            elif len(list(self.vtimedict.keys())[0]) == 16:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H:%M')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M')
                            else:
                                tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H:%M:%S')
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M:%S')

                            faging = int((tdate2 - tdate1).total_seconds()/3600)
                            #print(aging)
                        elif len(dtime) == 1:
                            if len(list(self.vtimedict.keys())[0]) == 13:
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                            elif len(list(self.vtimedict.keys())[0]) == 16:

                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M')
                            else:
                                tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H:%M:%S')


                            aging = 0
                            lk = '999'




                        for lk, lvinx in self.vleveldict.items():
                            if os.path.exists(os.path.join(os.path.join(self.outPath, cod), str(lk))):
                                shutil.rmtree(os.path.join(os.path.join(self.outPath, cod), str(lk)))
                                os.makedirs(os.path.join(os.path.join(self.outPath, cod), str(lk)))
                            else:
                                os.makedirs(os.path.join(os.path.join(self.outPath, cod), str(lk)))
                            for tk, tvinx in self.vtimedict.items():
                                if len(tk) == 13:
                                    ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H')

                                elif len(tk) == 16:

                                    ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H:%M')
                                else:
                                    ltk = datetime.datetime.strptime(tk, '%Y-%m-%d %H:%M:%S')

                                aging = int((ltk - tdate1).total_seconds() / 3600)
                                self.headinfo[0] = aging
                                self.headinfo[1] = str(lk)
                                # print(tk)

                                startdate = ltk.strftime('%Y%m%d%H')
                                enddate1 = ltk + datetime.timedelta(hours=faging)
                                enddate = enddate1.strftime('%Y%m%d%H')
                                titletdate = ltk.strftime('%y%m%d%H') + '.' + str(aging).zfill(3)
                                flinedate = ltk.strftime('%y %m %d %H ')
                                with open(os.path.join(os.path.join(os.path.join(self.outPath, cod), str(lk)), titletdate),'w') as nfc:

                                    firstline = 'diamond 4 ' + str(cod) + '_' + startdate + '_' + enddate

                                    secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                                    nfc.write(firstline + '\n')
                                    nfc.write(secondLine + '\n')
                                    nfc.write('\n')
                                    if findex == 0:
                                        if isinstance(self.hdf.variables[cod][tvinx, lvinx, :, :],np.ma.core.MaskedArray):
                                            for d in self.hdf.variables[cod][tvinx, lvinx, :, :].data:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in
                                                                  d[h:h + 10]]) + '\n'
                                                    # print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')
                                        else:

                                            for d in self.hdf.variables[cod][tvinx, lvinx, :, :]:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    #print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')
                                    else:

                                        if isinstance(self.hdf.variables[cod][lvinx, tvinx, :, :],np.ma.core.MaskedArray):

                                            for d in self.hdf.variables[cod][lvinx, tvinx, :, :].data:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in
                                                                  d[h:h + 10]]) + '\n'
                                                    # print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')
                                        else:

                                            for d in self.hdf.variables[cod][lvinx, tvinx, :, :]:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    #print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')

                    else:
                        pass


        #
        #     return 0
        # except Exception as arg:
        #     print('ERROR', arg)









if __name__ == '__main__':

    c = HDF_to_M4(r'/home/trywangdao/mrcpysrc/m4/log/2/2.hdf',r'/home/trywangdao/mrcpysrc/data/m4file','')
    #c = HDF_to_M4(r'/home/trywangdao/mrcpysrc/data/gen/hdf/20190812144446.hdf', r'/home/trywangdao/mrcpysrc/data/m4file', 'four-variable')
    print(c.flag)


