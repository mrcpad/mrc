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



class NC_to_M4(Micaps4property):

    def __init__(self, ncFilePath,outPath,condtion):
        self.flag = 1
        self.ncFilePath = ncFilePath
        if os.path.exists(ncFilePath):

            self.nc = nc.Dataset(ncFilePath, 'r',)
            self.condtion = condtion
            self.outPath = outPath
            fncattrs = self.nc.ncattrs()
            self.dictncattrs = dict()
            for attr in fncattrs:
                self.dictncattrs[attr] = self.nc.getncattr(attr)

            #print(self.dictncattrs)

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
            if self.fg == 'm42nc':
                self.agings = self.nc.variables['aging'][:]
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



                self.headinfo = [self.aging, str(self.level), self.LonGridLength, self.LatGridLength, self.StartLon,
                                 self.EndLon, self.StartLat, self.EndLat, self.LonGridNumber, self.LatGridNumber,
                                 self.ContourInterval, self.ContourStartValue, self.ContourEndValue,
                                 self.SmoothnessCoefficient, self.ThickenedLineValue]
                self.headinfo = self.headinfo[0:2] + ['{:.3f}'.format(float(info)) for info in self.headinfo[2:]]
                self.headinfo[8] = str(int(float(self.headinfo[8])))
                self.headinfo[9] = str(int(float(self.headinfo[9])))
                self.VerifyData()
                if self.check == 0:
                    print('Running NetCDF File Conversion......')
                    if self.condtion:
                        self.nc_to_m4_condtion()
                    else:
                        self.nc_to_m4()
                else:
                    print('Failed to verify NetCDF data')


            else:

                lone = self.nc.get_variables_by_attributes(axis='X')
                if lone:
                    long = lone[0][:]
                    StartLon = long[0]
                    EndLon = long[-1]
                    LonGridNumber = len(long)
                    LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)

                else:
                    if self.nc.variables.get('longitude'):
                        long = self.nc.variables.get('longitude')[:]
                        StartLon = long[0]
                        EndLon = long[-1]
                        LonGridNumber = len(long)
                        LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)
                        #print(np.round(LonGridLength, decimals=2))
                    elif self.nc.variables.get('lon'):
                        long = self.nc.variables.get('lon')[:]
                        StartLon = long[0]
                        EndLon = long[-1]
                        LonGridNumber = len(long)
                        LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)


                late = self.nc.get_variables_by_attributes(axis='Y')
                if late:
                    lat = late[0][:]
                    StartLat = lat[0]
                    EndLat = lat[-1]
                    LatGridNumber = len(lat)
                    LatGridLength = (EndLat - StartLat) / (LatGridNumber - 1)
                else:
                    if self.nc.variables.get('latitude'):
                        lat = self.nc.variables.get('latitude')[:]
                        StartLat = lat[0]
                        EndLat = lat[-1]
                        LatGridNumber = len(lat)
                        LatGridLength = (EndLat - StartLat) / (LatGridNumber - 1)
                    elif self.nc.variables.get('lat'):
                        lat = self.nc.variables.get('lat')[:]
                        StartLat = lat[0]
                        EndLat = lat[-1]
                        LatGridNumber = len(lat)
                        LatGridLength = (EndLat - StartLat) / (LatGridNumber - 1)
                    else:
                        pass


                vtime = self.nc.get_variables_by_attributes(axis='T')

                if vtime:
                    if isinstance(vtime[0][:], np.ma.core.MaskedArray):
                        td = nc.num2date(vtime[0][::].data, vtime[0].units)
                    else:

                        td = nc.num2date(vtime[0][::], vtime[0].units)
                    self.vtimedict = dict(zip([str(tds) for tds in td.tolist()], range(len(td.tolist()))))

                else:
                    if self.nc.variables.get('time'):
                        ftime = self.nc.variables.get('time','')
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
                    ld = vlevel[0][:]
                    self.vleveldict = dict(zip([str(lv) for lv in ld.tolist()], range(len(ld.tolist()))))

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
                    print('Running NetCDF File Conversion......')
                    if self.condtion:
                        self.nc_to_m4_v2_condtion()
                    else:
                        self.nc_to_m4_v2()
                else:
                    print('Failed to verify NetCDF data')






            '''if self.nc.variables.get('longitude'):
                #print(self.nc.variables.get('longitude').units)
                long = self.nc.variables.get('longitude')[:]
                StartLon = long[0]
                EndLon = long[-1]
                LonGridNumber = len(long)
                LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)
                print(np.round(LonGridLength,decimals=2))
            elif self.nc.variables.get('lon'):
                long = self.nc.variables.get('lon')[:]
                StartLon = long[0]
                EndLon = long[-1]
                LonGridNumber = len(long)
                LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)
            else:
                pass

            if self.nc.variables.get('latitude'):
                lat = self.nc.variables.get('latitude')[:]
                StartLat = lat[0]
                EndLat = lat[-1]
                LatGridNumber = len(lat)
                LatGridLength = (EndLat - StartLat) / (LatGridNumber - 1)
            elif self.nc.variables.get('lat'):
                lat = self.nc.variables.get('lat')[:]
                StartLat = lat[0]
                EndLat = lat[-1]
                LatGridNumber = len(lat)
                LatGridLength = (EndLat - StartLat) / (LatGridNumber - 1)
            else:
                pass

            if self.nc.variables.get('level'):
                seclevel = self.nc.variables.get('level')[0]


            ft = datetime.datetime.now()
            ftyear = ft.strftime('%y-%m-%d').split('-')[0]
            if self.nc.variables.get('time'):
                ftime = self.nc.variables.get('time')
                if isinstance(ftime[:], np.ma.core.MaskedArray):

                    nd = nc.num2date(ftime[::].data, ftime.units)
                    ft = datetime.datetime.strptime(str(nd[0]), '%Y-%m-%d %H:%M:%S')
                    ftt = ft.strftime('%y-%m-%d %H')
                    ftyear = ftt.split('-')[0]
                else:
                    ft = datetime.datetime.strptime(ftime[0], '%Y-%m-%d %H')
                    ftt = ft.strftime('%y-%m-%d %H')
                    ftyear = ftt.split('-')[0]


            #nc.num2date(t_variable[::], t_variable.units)
            #nc.date2num(t_variable[::], t_variable.units)



            self.fg = self.dictncattrs.get('flag', '')
            if not self.fg:
                print('The NC File not m4file transformations, Abnormalities may occur')
            self.year = self.dictncattrs.get('year', str(ftyear))
            self.month = self.dictncattrs.get('month', str(ft.month))
            self.day = self.dictncattrs.get('day', str(ft.day))
            self.ftime = self.dictncattrs.get('time', str(ft.hour))
            self.aging = self.dictncattrs.get('aging','0')
            self.level = self.dictncattrs.get('level',str(seclevel))
            self.LonGridLength = self.dictncattrs.get('LonGridLength', str(LonGridLength))
            self.LatGridLength = self.dictncattrs.get('LatGridLength',str(LatGridLength))
            self.StartLon = self.dictncattrs.get('StartLon',str(StartLon))
            self.EndLon = self.dictncattrs.get('EndLon',str(EndLon))
            self.StartLat = self.dictncattrs.get('StartLat',str(StartLat))
            self.EndLat = self.dictncattrs.get('EndLat',str(EndLat))
            self.LatGridNumber = self.dictncattrs.get('LatGridNumber',str(LatGridNumber))
            self.LonGridNumber = self.dictncattrs.get('LonGridNumber',str(LonGridNumber))
            self.ContourInterval = self.dictncattrs.get('ContourInterval','0')
            self.ContourStartValue = self.dictncattrs.get('ContourStartValue','0')
            self.ContourEndValue = self.dictncattrs.get('ContourEndValue','0')
            self.SmoothnessCoefficient = self.dictncattrs.get('SmoothnessCoefficient','0')
            tdate = datetime.datetime.strptime(self.year+self.month+self.day+self.ftime, '%y%m%d%H')
            firstline = 'diamond 4 '+ tdate.strftime('%y{}%m{}%d{}%H{}').format('??','??','??','??')
            secondLine = tdate.strftime('%y %m %d %H ')

            self.headinfo = [self.aging,str(self.level),self.LonGridLength,self.LatGridLength,self.StartLon,self.EndLon,self.StartLat,self.EndLat,self.LonGridNumber,self.LatGridNumber,self.ContourInterval,self.ContourStartValue,self.ContourEndValue,self.SmoothnessCoefficient]
            self.headinfo = self.headinfo[0:2] + ['{:.3f}'.format(float(info)) for info in self.headinfo[2:]]
            self.headinfo[8] = str(int(float(self.headinfo[8])))
            self.headinfo[9] = str(int(float(self.headinfo[9])))
            #print(self.headinfo[2:10])
            secondLine = secondLine + '  '.join(self.headinfo[0:10])
            thirdLine = '  '.join(self.headinfo[11:])
            if isinstance(ftime[:], np.ma.core.MaskedArray):
                self.flag = self.nc_to_m4Mask()
            else:
                self.flag = self.nc_to_m4()'''
        self.flag = 0
    def VerifyData(self):
        self.check = 0
        for var in self.nc.variables.keys():
            if len(self.nc.variables[var].dimensions) >= 2:
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
                    print('Verify NetCDF data successfully')

                else:
                    print('Failed to verify NetCDF data')
                    self.check = 1


    def nc_to_m4_condtion(self):

        for cod in self.condtion.split():
            if cod in self.nc.variables.keys():

                if len(self.nc.variables[cod].dimensions) == 4:

                    self.timedict = dict(zip([str(tds) for tds in self.agings.tolist()], range(len(self.agings.tolist()))))

                    self.level = self.nc.variables.get('level')
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

                                for d in self.nc.variables[cod][tvinx, lvinx, :, :]:
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


    def nc_to_m4_v2_condtion(self):

        for cod in self.condtion.split():
            if cod in self.nc.variables.keys():

                if len(self.nc.variables[cod].dimensions) == 2:  # ????????????
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
                        if isinstance(self.nc.variables[cod][:], np.ma.core.MaskedArray):
                            for d in self.nc.variables[cod][:].data:
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
                elif len(self.nc.variables[cod].dimensions) == 3:  # ????????????
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
                                if isinstance(self.nc.variables[cod][tvinx, :, :], np.ma.core.MaskedArray):
                                    for d in self.nc.variables[cod][tvinx, :, :].data:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join(
                                                [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')
                                else:

                                    for d in self.nc.variables[cod][tvinx, :, :]:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')
                    else:
                        layers = self.nc.variables.get(self.nc.variables[cod].dimensions[0])
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

                                if isinstance(self.nc.variables[cod][index, :, :], np.ma.core.MaskedArray):
                                    for d in self.nc.variables[cod][index, :, :].data:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join(
                                                [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')
                                else:

                                    for d in self.nc.variables[cod][index, :, :]:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join(
                                                [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')






                elif len(self.nc.variables[cod].dimensions) == 4:  # ????????????
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
                                        if isinstance(self.nc.variables[cod][tvinx, lvinx, :, :],np.ma.core.MaskedArray):
                                            for d in self.nc.variables[cod][tvinx, lvinx, :, :].data:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in
                                                                  d[h:h + 10]]) + '\n'
                                                    # print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')
                                        else:

                                            for d in self.nc.variables[cod][tvinx, lvinx, :, :]:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    #print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')
                                    else:

                                        if isinstance(self.nc.variables[cod][lvinx, tvinx, :, :],np.ma.core.MaskedArray):

                                            for d in self.nc.variables[cod][lvinx, tvinx, :, :].data:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in
                                                                  d[h:h + 10]]) + '\n'
                                                    # print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')
                                        else:

                                            for d in self.nc.variables[cod][lvinx, tvinx, :, :]:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    #print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')

                    else:
                        print('Dimension of the Variable time error or not exist')

                else:
                    print('Dimension of the Variable ({cod}) is less than 4'.format(cod=cod))
                    '''
                    Dimension of the Variable ({cod}) is less than 4
                    '''

            else:
                print('The Variable ({cod}) does not exist'.format(cod=cod))





    @logginginfo(level="INFO")
    def nc_to_m4(self):
        '''
        nc????????m4????
        :return:
        '''
        #try:

        #m4??????????



        for var in self.nc.variables.keys():
            if len(self.nc.variables[var].dimensions) > 1:
                if len(self.nc.variables[var].dimensions) == 2:#????????????
                    pass
                elif len(self.nc.variables[var].dimensions) == 3:#????????????
                   pass
                elif len(self.nc.variables[var].dimensions) == 4:#????????????
                    #if self.nc.variables[var].dimensions[0] == 'level'


                    self.timedict = dict(zip([str(tds) for tds in self.agings.tolist()], range(len(self.agings.tolist()))))

                    self.level = self.nc.variables.get('level')
                    self.leveldict = dict(zip([str(lv) for lv in self.level[:].tolist()], range(len(self.level[:].tolist()))))

                    for lk, lvinx in self.leveldict.items():
                        if os.path.exists(os.path.join(os.path.join(self.outPath, var), str(lk))):
                            shutil.rmtree(os.path.join(os.path.join(self.outPath, var), str(lk)))
                            os.makedirs(os.path.join(os.path.join(self.outPath, var), str(lk)))
                        else:
                            os.makedirs(os.path.join(os.path.join(self.outPath, var), str(lk)))
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
                            with open(os.path.join(os.path.join(os.path.join(self.outPath, var), str(lk)),titletdate), 'w') as nfc:

                                firstline = 'diamond 4 ' + str(var) + '_' + startdate + '_' + enddate

                                secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                                nfc.write(firstline + '\n')
                                nfc.write(secondLine + '\n')
                                nfc.write('\n')

                                for d in self.nc.variables[var][tvinx, lvinx, :, :]:
                                    for h in range(0, len(d), 10):
                                        # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                        nd = ''.join(
                                            [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                        nfc.write(nd)
                                    nfc.write('\n')

                    # if 'time' in self.nc.variables[var].dimensions:
                    #     self.time = self.nc.variables.get('time')
                    #
                    #     # print(self.v.dimensions.index('time'))
                    #     if self.time.dtype != np.str:
                    #         td = nc.num2date(self.time[::].data, self.time.units)
                    #         # print(td.tolist())
                    #         self.timedict = dict(zip([str(tds) for tds in td.tolist()], range(len(td.tolist()))))
                    #
                    #     else:
                    #         self.timedict = dict(zip([str(td) for td in self.time[:].tolist()], range(len(self.time[:].tolist()))))
                    #         [str(d) for d in self.timedict.keys()]
                    #
                    # if 'level' in self.nc.variables[var].dimensions:
                    #     self.level = self.nc.variables.get('level')
                    #     self.leveldict = dict(zip([str(lv) for lv in self.level[:].tolist()], range(len(self.level[:].tolist()))))


                    # if 'latitude' in self.nc.variables[var].dimensions or 'lat' in self.nc.variables[var].dimensions or 'lats' in self.nc.variables[var].dimensions:
                    #     for lat in ['latitude', 'lat', 'lats']:
                    #         for dim in self.nc.variables[var].dimensions:
                    #             if lat == dim:
                    #                 self.latitude = self.nc.variables.get(lat, np.array([np.nan]))[:].astype(np.str)
                    #     # self.latitude = args[1].get('latitude', '')[:].astype(np.str)
                    #
                    # if 'longitude' in self.nc.variables[var].dimensions or 'lon' in self.nc.variables[var].dimensions or 'lons' in self.nc.variables[var].dimensions:
                    #     for lon in ['longitude', 'lon', 'lons']:
                    #         for dim in self.nc.variables[var].dimensions:
                    #             if lon == dim:
                    #                 self.longitude = self.nc.variables.get(lon, np.array([np.nan]))[:].astype(np.str)





                    # dtime = list(self.timedict.keys())
                    # tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H')
                    # tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                    # aging = int((tdate2 - tdate1).seconds/3600)
                    # #print(tdate1)
                    # #print(tdate2)
                    # #print(aging)
                    # #aging = str((tdate2 - tdate1).days * 24)
                    # yestoday = tdate1 - datetime.timedelta(hours=aging)
                    # #print(yestoday)
                    #
                    # findex = self.nc.variables[var].dimensions.index('time')
                    # #print(findex)
                    # if findex == 1:
                    #     for lk, lvinx in self.leveldict.items():
                    #         if os.path.exists(os.path.join(os.path.join(self.outPath, var), str(lk))):
                    #             shutil.rmtree(os.path.join(os.path.join(self.outPath, var), str(lk)))
                    #             os.makedirs(os.path.join(os.path.join(self.outPath, var), str(lk)))
                    #         else:
                    #             os.makedirs(os.path.join(os.path.join(self.outPath, var), str(lk)))
                    #         for tk,tvinx in self.timedict.items():
                    #             self.headinfo[0] = aging
                    #             self.headinfo[1] = str(lk)
                    #             print(tk)
                    #             tdate2 = datetime.datetime.strptime(tk, '%Y-%m-%d %H')
                    #             yestodaytime = tdate2 - datetime.timedelta(hours=aging)
                    #             titletdate = yestodaytime.strftime('%Y%m%d%H')
                    #             #print(tk)
                    #             #print(tdate2)
                    #             #print(yestoday)
                    #             #print(titletdate)
                    #
                    #             #print(int((tdate2 - tdate1).seconds / 3600))
                    #             #print((tdate2 - yestoday).total_seconds()/3600)
                    #             flinedate = yestodaytime.strftime('%y %m %d %H ')
                    #             with open(os.path.join(os.path.join(os.path.join(self.outPath, var), str(lk)), titletdate + '.' + str(aging).rjust(3, '0')), 'w') as nfc:
                    #                 firstline = 'diamond 4 ' + str(var) + '_' + yestodaytime.strftime('%Y%m%d%H') + '_' + tdate2.strftime('%Y%m%d%H')
                    #                 secondLine = flinedate + '  '.join([str(ls)for ls in self.headinfo])
                    #                 nfc.write(firstline + '\n')
                    #                 nfc.write(secondLine + '\n')
                    #                 nfc.write('\n')
                    #
                    #                 for d in self.nc.variables[var][lvinx, tvinx, :, :]:
                    #                     for h in range(0, len(d), 10):
                    #                         # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                    #                         nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                    #                         #nfc.write(nd)
                    #                     #nfc.write('\n')
                    #
                    #
                    #



                                #print(self.nc.variables[var][lvinx, tvinx, :, :].shape)




        #
        #     return 0
        # except Exception as arg:
        #     print('ERROR', arg)

    def nc_to_m4_v2(self):
        '''
        nc????????m4????
        :return:
        '''
        # try:

        # m4??????????

        for var in self.nc.variables.keys():
            if len(self.nc.variables[var].dimensions) > 1:

                if len(self.nc.variables[var].dimensions) == 2:  # ????????????
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
                        if isinstance(self.nc.variables[var][:], np.ma.core.MaskedArray):
                            for d in self.nc.variables[var][:].data:
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
                elif len(self.nc.variables[var].dimensions) == 3:  # ????????????
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
                                if isinstance(self.nc.variables[var][tvinx, :, :], np.ma.core.MaskedArray):
                                    for d in self.nc.variables[var][tvinx, :, :].data:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join(
                                                [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')
                                else:

                                    for d in self.nc.variables[var][tvinx, :, :]:
                                        for h in range(0, len(d), 10):
                                            # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')
                    else:
                        layers = self.nc.variables.get(self.nc.variables[var].dimensions[0])
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
                                with open(os.path.join(os.path.join(os.path.join(self.outPath, var), str(layer)), titletdate),
                                          'w') as nfc:

                                    firstline = 'diamond 4 ' + str(var) + '_' + startdate + '_' + enddate

                                    secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                                    nfc.write(firstline + '\n')
                                    nfc.write(secondLine + '\n')
                                    nfc.write('\n')

                                    if isinstance(self.nc.variables[var][index, :, :], np.ma.core.MaskedArray):
                                        for d in self.nc.variables[var][index, :, :].data:
                                            for h in range(0, len(d), 10):
                                                # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                nd = ''.join(
                                                    [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                nfc.write(nd)
                                            nfc.write('\n')
                                    else:

                                        for d in self.nc.variables[var][index, :, :]:
                                            for h in range(0, len(d), 10):
                                                # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                nd = ''.join(
                                                    [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                nfc.write(nd)
                                            nfc.write('\n')






                elif len(self.nc.variables[var].dimensions) == 4:  # ????????????
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
                                        if isinstance(self.nc.variables[var][tvinx, lvinx, :, :],np.ma.core.MaskedArray):
                                            for d in self.nc.variables[var][tvinx, lvinx, :, :].data:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in
                                                                  d[h:h + 10]]) + '\n'
                                                    # print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')
                                        else:

                                            for d in self.nc.variables[var][tvinx, lvinx, :, :]:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    #print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')
                                    else:

                                        if isinstance(self.nc.variables[var][lvinx, tvinx, :, :],np.ma.core.MaskedArray):

                                            for d in self.nc.variables[var][lvinx, tvinx, :, :].data:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in
                                                                  d[h:h + 10]]) + '\n'
                                                    # print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')
                                        else:

                                            for d in self.nc.variables[var][lvinx, tvinx, :, :]:
                                                for h in range(0, len(d), 10):
                                                    # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                    #print(nd)
                                                    nfc.write(nd)
                                                nfc.write('\n')

                    else:
                        pass






































                    # self.time = self.nc.variables.get('time')
                    # td = self.time[:]
                    # self.timedict = dict(zip([str(tds) for tds in td.tolist()], range(len(td.tolist()))))
                    #
                    # self.level = self.nc.variables.get('level')
                    # self.leveldict = dict(
                    #     zip([str(lv) for lv in self.level[:].tolist()], range(len(self.level[:].tolist()))))
                    #
                    # for lk, lvinx in self.leveldict.items():
                    #     if os.path.exists(os.path.join(os.path.join(self.outPath, var), str(lk))):
                    #         shutil.rmtree(os.path.join(os.path.join(self.outPath, var), str(lk)))
                    #         os.makedirs(os.path.join(os.path.join(self.outPath, var), str(lk)))
                    #     else:
                    #         os.makedirs(os.path.join(os.path.join(self.outPath, var), str(lk)))
                    #     for tk, tvinx in self.timedict.items():
                    #         aging = tk.split('<-')[1].split('.')[1]
                    #         self.headinfo[0] = aging
                    #         self.headinfo[1] = str(lk)
                    #         # print(tk)
                    #         tdate2 = datetime.datetime.strptime(tk.split('<-')[1].split('.')[0], '%y%m%d%H')
                    #         startdate = tdate2.strftime('%Y%m%d%H')
                    #         enddate1 = datetime.datetime.strptime(tk.split('<-')[0], '%Y-%m-%d %H')
                    #         enddate = enddate1.strftime('%Y%m%d%H')
                    #         titletdate = tk.split('<-')[1]
                    #         flinedate = tdate2.strftime('%y %m %d %H ')
                    #         with open(os.path.join(os.path.join(os.path.join(self.outPath, var), str(lk)), titletdate),
                    #                   'w') as nfc:
                    #
                    #             firstline = 'diamond 4 ' + str(var) + '_' + startdate + '_' + enddate
                    #
                    #             secondLine = flinedate + '  '.join([str(ls) for ls in self.headinfo])
                    #             nfc.write(firstline + '\n')
                    #             nfc.write(secondLine + '\n')
                    #             nfc.write('\n')
                    #
                    #             for d in self.nc.variables[var][tvinx, lvinx, :, :]:
                    #                 for h in range(0, len(d), 10):
                    #                     # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                    #                     nd = ''.join(
                    #                         [str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                    #                     nfc.write(nd)
                    #                 nfc.write('\n')

                    # if 'time' in self.nc.variables[var].dimensions:
                    #     self.time = self.nc.variables.get('time')
                    #
                    #     # print(self.v.dimensions.index('time'))
                    #     if self.time.dtype != np.str:
                    #         td = nc.num2date(self.time[::].data, self.time.units)
                    #         # print(td.tolist())
                    #         self.timedict = dict(zip([str(tds) for tds in td.tolist()], range(len(td.tolist()))))
                    #
                    #     else:
                    #         self.timedict = dict(zip([str(td) for td in self.time[:].tolist()], range(len(self.time[:].tolist()))))
                    #         [str(d) for d in self.timedict.keys()]
                    #
                    # if 'level' in self.nc.variables[var].dimensions:
                    #     self.level = self.nc.variables.get('level')
                    #     self.leveldict = dict(zip([str(lv) for lv in self.level[:].tolist()], range(len(self.level[:].tolist()))))

                    # if 'latitude' in self.nc.variables[var].dimensions or 'lat' in self.nc.variables[var].dimensions or 'lats' in self.nc.variables[var].dimensions:
                    #     for lat in ['latitude', 'lat', 'lats']:
                    #         for dim in self.nc.variables[var].dimensions:
                    #             if lat == dim:
                    #                 self.latitude = self.nc.variables.get(lat, np.array([np.nan]))[:].astype(np.str)
                    #     # self.latitude = args[1].get('latitude', '')[:].astype(np.str)
                    #
                    # if 'longitude' in self.nc.variables[var].dimensions or 'lon' in self.nc.variables[var].dimensions or 'lons' in self.nc.variables[var].dimensions:
                    #     for lon in ['longitude', 'lon', 'lons']:
                    #         for dim in self.nc.variables[var].dimensions:
                    #             if lon == dim:
                    #                 self.longitude = self.nc.variables.get(lon, np.array([np.nan]))[:].astype(np.str)

                    # dtime = list(self.timedict.keys())
                    # tdate2 = datetime.datetime.strptime(dtime[1], '%Y-%m-%d %H')
                    # tdate1 = datetime.datetime.strptime(dtime[0], '%Y-%m-%d %H')
                    # aging = int((tdate2 - tdate1).seconds/3600)
                    # #print(tdate1)
                    # #print(tdate2)
                    # #print(aging)
                    # #aging = str((tdate2 - tdate1).days * 24)
                    # yestoday = tdate1 - datetime.timedelta(hours=aging)
                    # #print(yestoday)
                    #
                    # findex = self.nc.variables[var].dimensions.index('time')
                    # #print(findex)
                    # if findex == 1:
                    #     for lk, lvinx in self.leveldict.items():
                    #         if os.path.exists(os.path.join(os.path.join(self.outPath, var), str(lk))):
                    #             shutil.rmtree(os.path.join(os.path.join(self.outPath, var), str(lk)))
                    #             os.makedirs(os.path.join(os.path.join(self.outPath, var), str(lk)))
                    #         else:
                    #             os.makedirs(os.path.join(os.path.join(self.outPath, var), str(lk)))
                    #         for tk,tvinx in self.timedict.items():
                    #             self.headinfo[0] = aging
                    #             self.headinfo[1] = str(lk)
                    #             print(tk)
                    #             tdate2 = datetime.datetime.strptime(tk, '%Y-%m-%d %H')
                    #             yestodaytime = tdate2 - datetime.timedelta(hours=aging)
                    #             titletdate = yestodaytime.strftime('%Y%m%d%H')
                    #             #print(tk)
                    #             #print(tdate2)
                    #             #print(yestoday)
                    #             #print(titletdate)
                    #
                    #             #print(int((tdate2 - tdate1).seconds / 3600))
                    #             #print((tdate2 - yestoday).total_seconds()/3600)
                    #             flinedate = yestodaytime.strftime('%y %m %d %H ')
                    #             with open(os.path.join(os.path.join(os.path.join(self.outPath, var), str(lk)), titletdate + '.' + str(aging).rjust(3, '0')), 'w') as nfc:
                    #                 firstline = 'diamond 4 ' + str(var) + '_' + yestodaytime.strftime('%Y%m%d%H') + '_' + tdate2.strftime('%Y%m%d%H')
                    #                 secondLine = flinedate + '  '.join([str(ls)for ls in self.headinfo])
                    #                 nfc.write(firstline + '\n')
                    #                 nfc.write(secondLine + '\n')
                    #                 nfc.write('\n')
                    #
                    #                 for d in self.nc.variables[var][lvinx, tvinx, :, :]:
                    #                     for h in range(0, len(d), 10):
                    #                         # nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                    #                         nd = ''.join([str(round(float(s), 3)).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                    #                         #nfc.write(nd)
                    #                     #nfc.write('\n')
                    #
                    #
                    #

                    # print(self.nc.variables[var][lvinx, tvinx, :, :].shape)


        #
        #     return 0
        # except Exception as arg:
        #     print('ERROR', arg)

    @logginginfo(level="INFO")
    def nc_to_m4Mask(self):
        '''
        nc????????m4????
        :return:
        '''
        try:

            # m4??????????
            tdate = datetime.datetime.strptime(self.year + self.month + self.day + self.ftime, '%y%m%d%H')
            # ??????????????
            firstline = 'diamond 4 ' + tdate.strftime('%y{}%m{}%d{}%H{}').format('??', '??', '??', '??')
            print(firstline)
            headsecondLine = tdate.strftime('%y %m %d %H ')

            self.headinfo = [self.aging, str(self.level), self.LonGridLength, self.LatGridLength, self.StartLon,
                             self.EndLon, self.StartLat, self.EndLat, self.LatGridNumber, self.LonGridNumber,
                             self.ContourInterval, self.ContourStartValue, self.ContourEndValue,
                             self.SmoothnessCoefficient]
            self.headinfo = self.headinfo[0:2] + ['{:.3f}'.format(float(info)) for info in self.headinfo[2:]]
            self.headinfo[8] = str(int(float(self.headinfo[8])))
            self.headinfo[9] = str(int(float(self.headinfo[9])))
            # print(self.headinfo)
            secondLine = headsecondLine + '  '.join(self.headinfo[0:10])
            thirdLine = '  '.join(self.headinfo[11:])

            for var in self.nc.variables.keys():
                if len(self.nc.variables[var].dimensions) > 1:
                    if os.path.exists(os.path.join(self.outPath, var)):
                        shutil.rmtree(os.path.join(self.outPath, var))
                        os.makedirs(os.path.join(self.outPath, var))
                    else:
                        os.makedirs(os.path.join(self.outPath, var))
                    if len(self.nc.variables[var].dimensions) == 2:  # ????????????

                        with open(os.path.join(os.path.join(self.outPath, var), var + '.000'), 'w') as nfc:
                            nfc.write(firstline + '\n')
                            nfc.write(secondLine + '\n')
                            nfc.write(thirdLine + '\n')
                            nfc.write('\n')
                            for d in self.nc.variables[var][:]:
                                for i in range(0, len(d), 10):
                                    nd = ''.join([str(round(float(s), 3)).rjust(15, ' ') for s in d[i:i + 10]]) + '\n'
                                    nfc.write(nd)
                                nfc.write('\n')
                    elif len(self.nc.variables[var].dimensions) == 3:  # ????????????

                        headtime = self.nc.variables[self.nc.variables[var].dimensions[1]]
                        nd = nc.num2date(headtime[::].data, headtime.units)
                        ft = datetime.datetime.strptime(str(nd[0]), '%Y-%m-%d %H:%M:%S')
                        baseheadtime = ft.strftime('%Y-%m-%d %H')
                        tdate1 = datetime.datetime.strptime(baseheadtime, '%Y-%m-%d %H')





                        for i, dtime in enumerate(self.nc.variables[self.nc.variables[var].dimensions[0]][:]):

                            htime = self.nc.variables[self.nc.variables[var].dimensions[1]]
                            nd = nc.num2date(dtime.data, htime.units)
                            ft = datetime.datetime.strptime(str(nd), '%Y-%m-%d %H:%M:%S')
                            ft = ft.strftime('%Y-%m-%d %H')
                            tdate2 = datetime.datetime.strptime(ft, '%Y-%m-%d %H')
                            forecasttime = tdate2.strftime('%d{}%H{}').format('??', '??')

                            firstline = 'diamond 4 ' + tdate1.strftime('%y{}%m{}%d{}%H{}').format('??', '??', '??', '??')
                            aging = str((tdate2 - tdate1).days * 24)
                            self.headinfo[0] = aging
                            yestodaytime = tdate2 - datetime.timedelta(days=(tdate2 - tdate1).days)
                            titletdate = yestodaytime.strftime('%Y%m%d%H')

                            with open(os.path.join(os.path.join(self.outPath, var), titletdate + '.' + aging.rjust(3, '0')),
                                      'w') as nfc:

                                secondLine = headsecondLine + '  '.join(self.headinfo[0:10])
                                thirdLine = '  '.join(self.headinfo[11:])
                                if (tdate2 - tdate1).days == 0:
                                    nfc.write(firstline + '\n')
                                else:
                                    firstline = 'diamond 4 ' + tdate1.strftime('%y{}%m{}%d{}%H{}').format('??', '??', '??',
                                                                                                          '??') + '                   ' + forecasttime + '????'
                                    nfc.write(firstline + '\n')
                                nfc.write(secondLine + '\n')
                                nfc.write(thirdLine + '\n')
                                nfc.write('\n')

                                for d in self.nc.variables[var][i, :, :]:
                                    for j in range(0, len(d), 10):
                                        nd = ''.join([str(round(float(s), 3)).rjust(15, ' ') for s in d[i:i + 10]]) + '\n'
                                        nfc.write(nd)
                                    nfc.write('\n')
                    elif len(self.nc.variables[var].dimensions) == 4:  # ????????????
                        headtime = self.nc.variables[self.nc.variables[var].dimensions[1]]
                        nd = nc.num2date(headtime[::].data, headtime.units)
                        ft = datetime.datetime.strptime(str(nd[0]), '%Y-%m-%d %H:%M:%S')
                        baseheadtime = ft.strftime('%Y-%m-%d %H')
                        tdate1 = datetime.datetime.strptime(baseheadtime, '%Y-%m-%d %H')

                        for i, dlevel in enumerate(self.nc.variables[self.nc.variables[var].dimensions[0]][:]):
                            if os.path.exists(os.path.join(os.path.join(self.outPath, var), str(dlevel))):
                                shutil.rmtree(os.path.join(os.path.join(self.outPath, var), str(dlevel)))
                                os.makedirs(os.path.join(os.path.join(self.outPath, var), str(dlevel)))
                            else:
                                os.makedirs(os.path.join(os.path.join(self.outPath, var), str(dlevel)))
                            for j, dtime in enumerate(self.nc.variables[self.nc.variables[var].dimensions[1]][:]):

                                htime = self.nc.variables[self.nc.variables[var].dimensions[1]]
                                nd = nc.num2date(dtime.data, htime.units)
                                ft = datetime.datetime.strptime(str(nd), '%Y-%m-%d %H:%M:%S')
                                ft = ft.strftime('%Y-%m-%d %H')
                                tdate2 = datetime.datetime.strptime(ft, '%Y-%m-%d %H')
                                # tdate = datetime.datetime.strptime('19072912', '%y%m%d%H') - datetime.timedelta(days=1)
                                forecasttime = tdate2.strftime('%d{}%H{}').format('??', '??')
                                # tdate = datetime.datetime.strptime(self.year + self.month + self.day + self.ftime,'%y%m%d%H')
                                firstline = 'diamond 4 ' + tdate1.strftime('%y{}%m{}%d{}%H{}').format('??', '??', '??', '??')
                                # print(str(tdate2.time().hour))
                                aging = str((tdate2 - tdate1).days * 24)
                                self.headinfo[0] = aging
                                self.headinfo[1] = str(dlevel)
                                # print('.' + aging.rjust(3, '0'))
                                yestodaytime = tdate2 - datetime.timedelta(days=(tdate2 - tdate1).days)
                                titletdate = yestodaytime.strftime('%Y%m%d%H')

                                with open(os.path.join(os.path.join(os.path.join(self.outPath, var), str(dlevel)),
                                                       titletdate + '.' + aging.rjust(3, '0')), 'w') as nfc:

                                    secondLine = headsecondLine + '  '.join(self.headinfo[0:10])

                                    thirdLine = '  '.join(self.headinfo[11:])
                                    # print(secondLine)
                                    if (tdate2 - tdate1).days == 0:
                                        nfc.write(firstline + '\n')
                                    else:
                                        firstline = 'diamond 4 ' + tdate1.strftime('%y{}%m{}%d{}%H{}').format('??', '??', '??',
                                                                                                              '??') + '                   ' + forecasttime + '????'
                                        nfc.write(firstline + '\n')
                                    nfc.write(secondLine + '\n')
                                    nfc.write(thirdLine + '\n')
                                    nfc.write('\n')

                                    for d in self.nc.variables[var][i, j, :, :]:
                                        for h in range(0, len(d), 10):
                                            #nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                            nd = ''.join([str(round(float(s), 3)).rjust(15, ' ') for s in d[i:i + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')
            return 0
        except Exception as arg:
            print('ERROR', arg)






if __name__ == '__main__':

    c = NC_to_M4(r'Z_SATE.nc',r'/home/trywangdao/mrcpysrc/data/m4file','')
    #c = NC_to_M4(r'/home/trywangdao/mrcpysrc/data/gen/nc/ncfile.nc', r'/home/trywangdao/mrcpysrc/data/m4file', 'four-variable')
    print(c.flag)
    #print(nc.ncattrs())
    #latitude = nc.variables['latitude'][:]
    #longitude = nc.variables['longitude'][:]
    #level = nc.variables['level'][:]
    #time = nc.variables['time'][:]
    '''for i in range(len(level)):
        for j in range(len(time)):
            b = nc.variables['lvtemperature'][i,j,:,:]
            #print(level[i],time[j])
            pass'''
            #print(pd.DataFrame(b, index=latitude, columns=longitude))
    #print(len(latitude))
    #print(nc.variables['lvtemperature'][0,0,:,:])
    #a = nc.variables['lvtemperature'][0,0,:,:]
    #print(pd.DataFrame(a,index=latitude,columns=longitude))

    tdate1 = datetime.datetime.strptime('2015-12-15 08', '%Y-%m-%d %H')
    tdate2 = datetime.datetime.strptime('2015-12-16 08', '%Y-%m-%d %H')
    #print((tdate2 - tdate1).days*24)

