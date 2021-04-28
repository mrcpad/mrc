# -*- coding: gbk -*-
import sys
import os
ppath = os.path.abspath('..')
sys.path.append(os.path.join(ppath, 'm4'))
import os
import datetime
import netCDF4 as nc
from m4.m4property import Micaps4property
import shutil
from m4.m4property import logginginfo


class HDF_to_M4(Micaps4property):
    '''hdf�ļ�ת��m4�ļ�
        :return:
           '''

    def __init__(self, hdfFilePath, outPath, condtion):
        self.flag = 1
        if os.path.exists(hdfFilePath):
            self.hdf = nc.Dataset(hdfFilePath, 'r',)
            self.condtion = condtion
            self.outPath = outPath
            fncattrs = self.hdf.ncattrs()
            self.dictncattrs = dict()
            for attr in fncattrs:#��ȡͷ��Ϣ
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

            if self.hdf.variables.get('longitude'):
                # print(self.nc.variables.get('longitude').units)
                long = self.hdf.variables.get('longitude')[:]
                StartLon = long[0]
                EndLon = long[-1]
                LonGridNumber = len(long)
                LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)
            elif self.hdf.variables.get('lon'):
                long = self.hdf.variables.get('lon')[:]
                StartLon = long[0]
                EndLon = long[-1]
                LonGridNumber = len(long)
                LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)
            else:
                pass

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

            if self.hdf.variables.get('level'):
                seclevel = self.hdf.variables.get('level')[0]

            ft = datetime.datetime.now()
            ftyear = ft.strftime('%y-%m-%d').split('-')[0]
            if self.hdf.variables.get('time'):
                ftime = self.hdf.variables.get('time')
                ft = datetime.datetime.strptime(ftime[0], '%Y-%m-%d %H')
                ftt = ft.strftime('%y-%m-%d %H')
                ftyear = ftt.split('-')[0]
                if isinstance(ftime[0], int):
                    nd = nc.num2date(ftime[::], ftime.units)
                    ft = datetime.datetime.strptime(nd[0], '%Y-%m-%d %H:%M:%S')
                    ftt = ft.strftime('%y-%m-%d %H')
                    ftyear = ftt.split('-')[0]

            # nc.num2date(t_variable[::], t_variable.units)
            # nc.date2num(t_variable[::], t_variable.units)


            self.fg = self.dictncattrs.get('flag', '')
            if not self.fg:
                print('The hdf File not m4file transformations, Abnormalities may occur')
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


            tdate = datetime.datetime.strptime(self.year+self.month+self.day+self.ftime, '%y%m%d%H')
            firstline = 'diamond 4 '+ tdate.strftime('%y{}%m{}%d{}%H{}').format('��','��','��','��')
            #print(firstline)
            secondLine = tdate.strftime('%y %m %d %H ')

            self.headinfo = [self.aging,str(self.level),self.LonGridLength,self.LatGridLength,self.StartLon,self.EndLon,self.StartLat,self.EndLat,self.LatGridNumber,self.LonGridNumber,self.ContourInterval,self.ContourStartValue,self.ContourEndValue,self.SmoothnessCoefficient]
            self.headinfo = self.headinfo[0:2] + ['{:.3f}'.format(float(info)) for info in self.headinfo[2:]]
            self.headinfo[8] = str(int(float(self.headinfo[8])))
            self.headinfo[9] = str(int(float(self.headinfo[9])))
            #print(self.headinfo[2:10])
            secondLine = secondLine + '  '.join(self.headinfo[0:10])
            thirdLine = '  '.join(self.headinfo[11:])
            self.flag = self.hdf_to_m4()



    @logginginfo(level="INFO")
    def hdf_to_m4(self):
        '''
        hdf�ļ�ת��m4�ļ�
        :return:
        '''
        try:

            #m4�ļ�ͷ��Ϣ
            tdate = datetime.datetime.strptime(self.year + self.month + self.day + self.ftime, '%y%m%d%H')
            #Ĭ�ϵ�һ����Ϣ
            firstline = 'diamond 4 ' + tdate.strftime('%y{}%m{}%d{}%H{}').format('��', '��', '��', '��')
            print(firstline)
            headsecondLine = tdate.strftime('%y %m %d %H ')

            self.headinfo = [self.aging, str(self.level), self.LonGridLength, self.LatGridLength, self.StartLon,
                             self.EndLon, self.StartLat, self.EndLat, self.LatGridNumber, self.LonGridNumber,
                             self.ContourInterval, self.ContourStartValue, self.ContourEndValue,
                             self.SmoothnessCoefficient]
            self.headinfo = self.headinfo[0:2] + ['{:.3f}'.format(float(info)) for info in self.headinfo[2:]]
            self.headinfo[8] = str(int(float(self.headinfo[8])))
            self.headinfo[9] = str(int(float(self.headinfo[9])))
            #print(self.headinfo)
            secondLine = headsecondLine + '  '.join(self.headinfo[0:10])
            thirdLine = '  '.join(self.headinfo[11:])
            for g in self.hdf.groups:
                #print(nc.groups['m4'].variables['lvtemperature'].dimensions)
                self.hdf.groups[g]
                for var in self.hdf.groups[g].variables.keys():
                    if len(self.hdf.groups[g].variables[var].dimensions) > 1:
                        if os.path.exists(os.path.join(self.outPath, var)):
                            shutil.rmtree(os.path.join(self.outPath, var))
                            os.makedirs(os.path.join(self.outPath, var))
                        else:
                            os.makedirs(os.path.join(self.outPath, var))
                        if len(self.hdf.groups[g].variables[var].dimensions) == 2:#������ά����

                            with open(os.path.join(os.path.join(self.outPath, var), var + '.000'), 'w') as nfc:
                                nfc.write(firstline + '\n')
                                nfc.write(secondLine + '\n')
                                nfc.write(thirdLine + '\n')
                                nfc.write('\n')
                                for d in self.hdf.groups[g].variables[var][:]:
                                    for i in range(0, len(d), 10):
                                        nd = ''.join([str(s).rjust(10, ' ') for s in d[i:i + 10]]) + '\n'
                                        nfc.write(nd)
                                    nfc.write('\n')
                        elif len(self.hdf.groups[g].variables[var].dimensions) == 3:#������ά����
                            headtime = sorted(self.hdf.groups[g].variables[self.hdf.groups[g].variables[var].dimensions[0]][:])
                            baseheadtime = headtime[0]
                            tdate1 = datetime.datetime.strptime(str(baseheadtime), '%Y-%m-%d %H')

                            for i, dtime in enumerate(self.hdf.groups[g].variables[self.hdf.groups[g].variables[var].dimensions[0]][:]):

                                tdate2 = datetime.datetime.strptime(dtime, '%Y-%m-%d %H')
                                forecasttime = tdate2.strftime('%d{}%H{}').format('��', '��')

                                firstline = 'diamond 4 ' + tdate1.strftime('%y{}%m{}%d{}%H{}').format('��', '��', '��', '��')
                                aging = str((tdate2 - tdate1).days * 24)
                                self.headinfo[0] = aging
                                yestodaytime = tdate2 - datetime.timedelta(days=(tdate2 - tdate1).days)
                                titletdate = yestodaytime.strftime('%Y%m%d%H')

                                with open(os.path.join(os.path.join(self.outPath, var), titletdate + '.' + aging.rjust(3, '0')),'w') as nfc:

                                    secondLine = headsecondLine + '  '.join(self.headinfo[0:10])
                                    thirdLine = '  '.join(self.headinfo[11:])
                                    if (tdate2 - tdate1).days == 0:
                                        nfc.write(firstline + '\n')
                                    else:
                                        firstline = 'diamond 4 ' + tdate1.strftime('%y{}%m{}%d{}%H{}').format('��', '��', '��','��') + '                   ' + forecasttime + 'Ԥ��'
                                        nfc.write(firstline + '\n')
                                    nfc.write(secondLine + '\n')
                                    nfc.write(thirdLine + '\n')
                                    nfc.write('\n')



                                    for d in self.hdf.groups[g].variables[var][i, :, :]:
                                        for j in range(0, len(d), 10):
                                            nd = ''.join([str(s).rjust(10, ' ') for s in d[j:j + 10]]) + '\n'
                                            nfc.write(nd)
                                        nfc.write('\n')
                        elif len(self.hdf.groups[g].variables[var].dimensions) == 4:#������ά����
                            headtime = sorted(self.hdf.groups[g].variables[self.hdf.groups[g].variables[var].dimensions[1]][:])
                            baseheadtime = headtime[0]
                            tdate1 = datetime.datetime.strptime(baseheadtime, '%Y-%m-%d %H')


                            for i, dlevel in enumerate(self.hdf.groups[g].variables[self.hdf.groups[g].variables[var].dimensions[0]][:]):
                                if os.path.exists(os.path.join(os.path.join(self.outPath, var), str(dlevel))):
                                    shutil.rmtree(os.path.join(os.path.join(self.outPath, var), str(dlevel)))
                                    os.makedirs(os.path.join(os.path.join(self.outPath, var), str(dlevel)))
                                else:
                                    os.makedirs(os.path.join(os.path.join(self.outPath, var), str(dlevel)))
                                for j, dtime in enumerate(self.hdf.groups[g].variables[self.hdf.groups[g].variables[var].dimensions[1]][:]):

                                    tdate2 = datetime.datetime.strptime(dtime, '%Y-%m-%d %H')
                                    #tdate = datetime.datetime.strptime('19072912', '%y%m%d%H') - datetime.timedelta(days=1)
                                    forecasttime = tdate2.strftime('%d{}%H{}').format('��', '��')

                                    #tdate = datetime.datetime.strptime(self.year + self.month + self.day + self.ftime,'%y%m%d%H')
                                    firstline = 'diamond 4 ' + tdate1.strftime('%y{}%m{}%d{}%H{}').format('��', '��', '��', '��')
                                    #print(str(tdate2.time().hour))
                                    aging = str((tdate2 - tdate1).days * 24)
                                    self.headinfo[0] = aging
                                    self.headinfo[1] = str(dlevel)
                                    #print('.' + aging.rjust(3, '0'))
                                    yestodaytime = tdate2 - datetime.timedelta(days=(tdate2 - tdate1).days)
                                    titletdate = yestodaytime.strftime('%Y%m%d%H')

                                    with open(os.path.join(os.path.join(os.path.join(self.outPath, var), str(dlevel)), titletdate + '.' + aging.rjust(3, '0')),'w') as nfc:

                                        secondLine = headsecondLine + '  '.join(self.headinfo[0:10])

                                        thirdLine = '  '.join(self.headinfo[11:])
                                        #print(secondLine)
                                        if (tdate2 - tdate1).days == 0:
                                            nfc.write(firstline + '\n')
                                        else:
                                            firstline = 'diamond 4 ' + tdate1.strftime('%y{}%m{}%d{}%H{}').format('��', '��', '��','��') + '                   ' + forecasttime + 'Ԥ��'
                                            nfc.write(firstline + '\n')
                                        nfc.write(secondLine + '\n')
                                        nfc.write(thirdLine + '\n')
                                        nfc.write('\n')

                                        for d in self.hdf.groups[g].variables[var][i, j, :, :]:
                                            for h in range(0, len(d), 10):
                                                nd = ''.join([str(s).rjust(10, ' ') for s in d[h:h + 10]]) + '\n'
                                                nfc.write(nd)
                                            nfc.write('\n')
            return 0
        except Exception as arg:
            print('ERROR', arg)








if __name__ == '__main__':

    c = HDF_to_M4(r'/home/ynairport/MrWang/pyclick/mrcproject/data/gen/hdf/20190812144728.hdf',
                 r'/home/ynairport/MrWang/pyclick/mrcproject/data/gen/hm', '')
    print(c.flag)

    tdate1 = datetime.datetime.strptime('2015-12-15 08', '%Y-%m-%d %H')
    tdate2 = datetime.datetime.strptime('2015-12-16 08', '%Y-%m-%d %H')
    #print((tdate2 - tdate1).days*24)

