# -*- coding: gbk -*-
import datetime
import sys
import os
ppath = os.path.abspath('..')
sys.path.append(os.path.join(ppath, 'm4'))
from m4.m4property import Micaps4property
import shutil
from m4.m4property import logginginfo
import pygrib
import numpy as np
import threading





class Grib_to_M4(Micaps4property):

    def __init__(self, GribFilePath,outPath,condtion):

        self.flag = 1
        if os.path.exists(GribFilePath):
            self.condtion = condtion
            self.outPath = outPath
            self.grbs = pygrib.open(GribFilePath)

            year = str(datetime.datetime.now().year)
            month = str(datetime.datetime.now().month)
            day = str(datetime.datetime.now().day)
            hour = str(datetime.datetime.now().hour)
            seclevel = '0'
            LonGridLength = '0'
            LatGridLength = '0'
            StartLon = '0'
            EndLon = '0'
            StartLat = '0'
            EndLat = '0'
            LatGridNumber = '0'
            LonGridNumber = '0'

            keys = [
                'Ni',
                'Nj',
                'latitudeOfFirstGridPointInDegrees',
                'longitudeOfFirstGridPointInDegrees',
                'latitudeOfLastGridPointInDegrees',
                'longitudeOfLastGridPointInDegrees',
                'iDirectionIncrementInDegrees',
                'jDirectionIncrementInDegrees',
                'year',
                'month',
                'day',
                'hour',
                'minute',
                'second',
                'dataDate',
                'level',
                'name',


            ]

            self.kdict = dict()





            vnamedic = self.getGribInfo()

            if self.condtion:
                vd = vnamedic.get(self.condtion, '')
                if vd:
                    vdv = {self.condtion: vd}

                    for k, v in vdv.items():
                        k = k.replace(' ', '')
                        self.kvar = k.replace(' ', '')
                        vtmp = v
                        for ks in keys:
                            if ks:
                                self.kdict[ks] = vtmp[0][0][ks]
                        self.year = str(self.kdict.get('year', str(year)))
                        self.month = str(self.kdict.get('month', str(month)))
                        self.day = str(self.kdict.get('day', str(day)))
                        self.ftime = str(self.kdict.get('time', str(hour)))
                        self.aging = self.kdict.get('aging', '0')
                        self.level = self.kdict.get('level', str(seclevel))
                        self.LonGridLength = self.kdict.get('iDirectionIncrementInDegrees', str(LonGridLength))
                        self.LatGridLength = self.kdict.get('jDirectionIncrementInDegrees', str(LatGridLength))
                        self.StartLon = self.kdict.get('longitudeOfFirstGridPointInDegrees', str(StartLon))
                        self.EndLon = self.kdict.get('longitudeOfLastGridPointInDegrees', str(EndLon))
                        self.StartLat = self.kdict.get('latitudeOfFirstGridPointInDegrees', str(StartLat))
                        self.EndLat = self.kdict.get('latitudeOfLastGridPointInDegrees', str(EndLat))
                        self.LatGridNumber = self.kdict.get('Nj', str(LatGridNumber))
                        self.LonGridNumber = self.kdict.get('Ni', str(LonGridNumber))
                        self.ContourInterval = self.kdict.get('ContourInterval', '0')
                        self.ContourStartValue = self.kdict.get('ContourStartValue', '0')
                        self.ContourEndValue = self.kdict.get('ContourEndValue', '0')
                        self.SmoothnessCoefficient = self.kdict.get('SmoothnessCoefficient', '0')
                        self.headinfo = [self.aging, str(self.level), self.LonGridLength, self.LatGridLength, self.StartLon,
                                         self.EndLon, self.StartLat, self.EndLat, self.LatGridNumber, self.LonGridNumber,
                                         self.ContourInterval, self.ContourStartValue, self.ContourEndValue,
                                         self.SmoothnessCoefficient]
                        self.headinfo = self.headinfo[0:2] + ['{:.3f}'.format(float(info)) for info in self.headinfo[2:]]
                        self.headinfo[8] = str(int(float(self.headinfo[8])))
                        self.headinfo[9] = str(int(float(self.headinfo[9])))
                        self.varibaleName = self.kvar
                        self.vlevel = str(v[0]).split(":")[5].split(' ')[1]
                        # self.value = np.around(self.kdict['values'], decimals=3)
                        #self.value = self.kdict['values']
                        print(k)

                        if len(v) == 1:
                            if len(v[0]) == 1:
                                self.vlevel = str(v[0][0]).split(":")[5].split(' ')[1]

                                self.value = v[0][0]['values']
                                self.grib_to_m4()
                            else:
                                for i, vg in enumerate(v[0]):
                                    self.vlevel = str(v[0][i]).split(":")[5].split(' ')[1]
                                    self.value = vg['values'].data if isinstance(vg['values'], np.ma.core.MaskedArray) else vg['values']
                                    self.grib_to_m4()





                        else:

                            for i, val in enumerate(v):
                                if len(val) == 1:
                                    varname = str(k) + '_' + 'var' + str(i + 1)
                                    self.varibaleName = varname
                                    self.vlevel = str(val[0]).split(":")[5].split(' ')[1]
                                    self.value = val[0]['values'].data if isinstance(val[0]['values'], np.ma.core.MaskedArray) else val[0]['values']
                                    self.grib_to_m4()




                                else:

                                    for j, sval in enumerate(val):
                                        mulvarname = str(k) + '_' + 'var' + str(i + 1) + '_' + str(len(val))
                                        self.varibaleName = mulvarname
                                        self.vlevel = str(sval).split(":")[5].split(' ')[1]
                                        self.value = sval['values'].data if isinstance(sval['values'], np.ma.core.MaskedArray) else sval['values']
                                        self.grib_to_m4()

                    self.flag = 0
                    self.grbs.close()
                else:
                    print('The key is not exist!')
            else:

                if vnamedic:
                    for k, v in vnamedic.items():
                        k = k.replace(' ', '')
                        self.kvar = k.replace(' ', '')
                        vtmp = v
                        for ks in keys:
                            if ks:
                                self.kdict[ks] = vtmp[0][0][ks]
                        self.year = str(self.kdict.get('year', str(year)))
                        self.month = str(self.kdict.get('month', str(month)))
                        self.day = str(self.kdict.get('day', str(day)))
                        self.ftime = str(self.kdict.get('time', str(hour)))
                        self.aging = self.kdict.get('aging', '0')
                        self.level = self.kdict.get('level', str(seclevel))
                        self.LonGridLength = self.kdict.get('iDirectionIncrementInDegrees', str(LonGridLength))
                        self.LatGridLength = self.kdict.get('jDirectionIncrementInDegrees', str(LatGridLength))
                        self.StartLon = self.kdict.get('longitudeOfFirstGridPointInDegrees', str(StartLon))
                        self.EndLon = self.kdict.get('longitudeOfLastGridPointInDegrees', str(EndLon))
                        self.StartLat = self.kdict.get('latitudeOfFirstGridPointInDegrees', str(StartLat))
                        self.EndLat = self.kdict.get('latitudeOfLastGridPointInDegrees', str(EndLat))
                        self.LatGridNumber = self.kdict.get('Nj', str(LatGridNumber))
                        self.LonGridNumber = self.kdict.get('Ni', str(LonGridNumber))
                        self.ContourInterval = self.kdict.get('ContourInterval', '0')
                        self.ContourStartValue = self.kdict.get('ContourStartValue', '0')
                        self.ContourEndValue = self.kdict.get('ContourEndValue', '0')
                        self.SmoothnessCoefficient = self.kdict.get('SmoothnessCoefficient', '0')
                        self.headinfo = [self.aging, str(self.level), self.LonGridLength, self.LatGridLength, self.StartLon,
                                         self.EndLon, self.StartLat, self.EndLat, self.LatGridNumber, self.LonGridNumber,
                                         self.ContourInterval, self.ContourStartValue, self.ContourEndValue,
                                         self.SmoothnessCoefficient]
                        self.headinfo = self.headinfo[0:2] + ['{:.3f}'.format(float(info)) for info in self.headinfo[2:]]
                        self.headinfo[8] = str(int(float(self.headinfo[8])))
                        self.headinfo[9] = str(int(float(self.headinfo[9])))
                        self.varibaleName = self.kvar
                        self.vlevel = str(v[0]).split(":")[5].split(' ')[1]
                        # self.value = np.around(self.kdict['values'], decimals=3)
                        #self.value = self.kdict['values']
                        print(k)

                        if len(v) == 1:
                            if len(v[0]) == 1:
                                self.vlevel = str(v[0][0]).split(":")[5].split(' ')[1]

                                self.value = v[0][0]['values']
                                self.grib_to_m4()
                            else:
                                for i, vg in enumerate(v[0]):
                                    self.vlevel = str(v[0][i]).split(":")[5].split(' ')[1]
                                    self.value = vg['values'].data if isinstance(vg['values'], np.ma.core.MaskedArray) else vg['values']
                                    self.grib_to_m4()





                        else:

                            for i, val in enumerate(v):
                                if len(val) == 1:
                                    varname = str(k) + '_' + 'var' + str(i + 1)
                                    self.varibaleName = varname
                                    self.vlevel = str(val[0]).split(":")[5].split(' ')[1]
                                    self.value = val[0]['values'].data if isinstance(val[0]['values'], np.ma.core.MaskedArray) else val[0]['values']
                                    self.grib_to_m4()




                                else:

                                    for j, sval in enumerate(val):
                                        mulvarname = str(k) + '_' + 'var' + str(i + 1) + '_' + str(len(val))
                                        self.varibaleName = mulvarname
                                        self.vlevel = str(sval).split(":")[5].split(' ')[1]
                                        self.value = sval['values'].data if isinstance(sval['values'], np.ma.core.MaskedArray) else sval['values']
                                        self.grib_to_m4()

                    self.flag = 0
                    self.grbs.close()
                else:
                    print('the GRIB file ERROR!')



    @logginginfo(level="INFO")
    def grib_to_m4(self):
        '''
        grib文件转化m4文件
        :return:
        '''
        try:

            #m4文件头信息
            tdate = datetime.datetime.strptime(self.year + self.month + self.day + self.ftime, '%Y%m%d%H')
            #默认第一行信息
            firstline = 'diamond 4 ' + tdate.strftime('%y{}%m{}%d{}%H{}').format('年', '月', '日', '点')
            print(self.vlevel)
            headsecondLine = tdate.strftime('%y %m %d %H ')
            filename = tdate.strftime('%y%m%d%H')

            self.headinfo = [self.aging, str(self.vlevel), self.LonGridLength, self.LatGridLength, self.StartLon,
                             self.EndLon, self.StartLat, self.EndLat, self.LatGridNumber, self.LonGridNumber,
                             self.ContourInterval, self.ContourStartValue, self.ContourEndValue,
                             self.SmoothnessCoefficient]
            self.headinfo = self.headinfo[0:2] + ['{:.3f}'.format(float(info)) for info in self.headinfo[2:]]
            self.headinfo[8] = str(int(float(self.headinfo[8])))
            self.headinfo[9] = str(int(float(self.headinfo[9])))
            #print(self.headinfo)
            #print(self.headinfo)
            secondLine = headsecondLine + '  '.join(self.headinfo[0:10])
            thirdLine = '  '.join(self.headinfo[11:])
            #print(thirdLine)
            if os.path.exists(os.path.join(os.path.join(self.outPath, self.varibaleName), self.vlevel)):
                shutil.rmtree(os.path.join(os.path.join(self.outPath, self.varibaleName), self.vlevel))
                os.makedirs(os.path.join(os.path.join(self.outPath, self.varibaleName), self.vlevel))
            else:
                os.makedirs(os.path.join(os.path.join(self.outPath, self.varibaleName), self.vlevel))

            with open(os.path.join(os.path.join(os.path.join(self.outPath, self.varibaleName), self.vlevel), filename + '.000'), 'w') as nfc:
                nfc.write(firstline + '\n')
                nfc.write(secondLine + '\n')
                nfc.write(thirdLine + '\n')
                nfc.write('\n')
                #self.value = np.around(self.value, decimals=3)
                if isinstance(self.value, np.ma.core.MaskedArray):
                    maksdata = self.value.data
                    for d in maksdata:
                        for i in range(0, len(d), 10):
                            #nd = ''.join([str(s).rjust(15, ' ') for s in d[i:i + 10]]) + '\n'
                            nd = ''.join([str(round(float(s), 3)).rjust(15, ' ') for s in d[i:i + 10]]) + '\n'
                            nfc.write(nd)
                        nfc.write('\n')
                        nfc.write('\n')
                        nfc.write('\n')
                else:
                    if not np.isnan(self.value).any():

                        for d in self.value:
                            for i in range(0, len(d), 10):
                                #nd = ''.join([str(s).rjust(15, ' ') for s in d[i:i + 10]]) + '\n'
                                nd = ''.join([str(round(float(s), 3)).rjust(15, ' ') for s in d[i:i + 10]]) + '\n'
                                nfc.write(nd)
                            nfc.write('\n')
                            nfc.write('\n')
                            nfc.write('\n')

            return 0
        except Exception as arg:
            print('ERROR', arg)


    def getGribInfo(self):
        vnamedic = dict()
        for g in self.grbs:
            ls = str(g).split(":")
            varname = ls[1] + '_' + ls[4]
            var = ls[5].split(' ')[1]
            if varname in list(vnamedic.keys()):
                if len(vnamedic[varname]) > 0:
                    for i, sv in enumerate(vnamedic[varname]):

                        if var in [str(svs).split(":")[5].split(' ')[1] for svs in sv]:  #
                            if len(vnamedic[varname]) > 1 and (i + 1) != len(vnamedic[varname]):
                                continue
                            else:
                                vnamedic[varname].append([g])  # add first element
                                break



                        else:
                            sv.append(g)
            else:
                vnamedic[varname] = [[g]]
        return vnamedic




if __name__ == '__main__':

    c = Grib_to_M4(r'./gef.gra.grb2',r'./m4','')
    print(c.flag)


