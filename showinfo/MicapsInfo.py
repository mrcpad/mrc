# -*- coding: utf-8 -*-



import codecs
import lib.array as ay
import numpy as np
import os

default_encoding = 'gbk'

FieldName = ["desc", "year", "month", "day", "time", "aging", "level", "LonGridLength", "LatGridLength", "StartLon","EndLon", "StartLat", "EndLat", "X-DIM", "Y-DIM", "ContourInterval", "ContourStartValue", "ContourEndValue ", "SmoothnessCoefficient", "ThickenedLineValue"]
propertyLen = 20  # 属性信息




class Micaps4(object):

    # property
    @property
    def propertyValue(self):
        return self._propertyValue

    @propertyValue.setter
    def propertyValue(self, value):
        self._propertyValue = value

    @property
    def desc(self):  # 屏幕上需显示的内容
        return self._desc

    @desc.setter
    def desc(self, value):
        self._desc = value

    @property
    def year(self):  # 年
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

    @property
    def month(self):  # 月
        return self._month

    @month.setter
    def month(self, value):
        self._month = value

    @property
    def day(self):  # 日
        return self._day

    @day.setter
    def day(self, value):
        self._day = value

    @property
    def time(self):  # 时次
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def aging(self):  # 时效
        return self._aging

    @aging.setter
    def aging(self, value):
        self._aging = value

    @property
    def level(self):  # 层次
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def LonGridLength(self):  # 经度格距
        return self._LonGridLength

    @LonGridLength.setter
    def LonGridLength(self, value):
        self._LonGridLength = value

    @property
    def LatGridLength(self):  # 纬度格距
        return self._LatGridLength

    @LatGridLength.setter
    def LatGridLength(self, value):
        self._LatGridLength = value

    @property
    def StartLon(self):  # 起始经度
        return self._StartLon

    @StartLon.setter
    def StartLon(self, value):
        self._StartLon = value

    @property
    def EndLon(self):  # 终止经度
        return self._EndLon

    @EndLon.setter
    def EndLon(self, value):
        self._EndLon = value

    @property
    def StartLat(self):  # 起始纬度
        return self._StartLat

    @StartLat.setter
    def StartLat(self, value):
        self._StartLat = value

    @property
    def EndLat(self):  # 终止纬度
        return self._EndLat

    @EndLat.setter
    def EndLat(self, value):
        self._EndLat = value

    @property
    def LatGridNumber(self):  # 纬向格点数
        return self._LatGridNumber

    @LatGridNumber.setter
    def LatGridNumber(self, value):
        self._LatGridNumber = value

    @property
    def LonGridNumber(self):  # 经向格点数
        return self._LonGridNumber

    @LonGridNumber.setter
    def LonGridNumber(self, value):
        self._LonGridNumber = value

    @property
    def ContourInterval(self):  # 等值线间隔
        return self._ContourInterval

    @ContourInterval.setter
    def ContourInterval(self, value):
        self._ContourInterval = value

    @property
    def ContourStartValue(self):  # 等值线起始值
        return self._ContourStartValue

    @ContourStartValue.setter
    def ContourStartValue(self, value):
        self._ContourStartValue = value

    @property
    def ContourEndValue(self):  # 等值线终止值
        return self._ContourEndValue

    @ContourEndValue.setter
    def ContourEndValue(self, value):
        self._ContourEndValue = value

    @property
    def SmoothnessCoefficient(self):  # 平滑系数
        return self._SmoothnessCoefficient

    @SmoothnessCoefficient.setter
    def SmoothnessCoefficient(self, value):
        self._SmoothnessCoefficient = value

    @property
    def ThickenedLineValue(self):  # 加粗线值
        return self._ThickenedLineValue

    @ThickenedLineValue.setter
    def ThickenedLineValue(self, value):
        self._ThickenedLineValue = value

    @property
    def MissValue(self):  # 无效值
        return self._MissValue

    @MissValue.setter
    def MissValue(self, value):
        self._MissValue = value

    @property
    def PixelValue(self):  # 格点值   一维数组
        return self._PixelValue

    @PixelValue.setter
    def PixelValue(self, value):
        self._PixelValue = value

    @property
    def GridValue(self):  # 格点二位数组，取值为从左下角开始先右后上   ...→...↑，即[经度格距,纬度格距]
        return self._GridValue

    @GridValue.setter
    def GridValue(self, value):
        self._GridValue = value

    @property
    def RollGridValue(self):  # 翻转格点二位数组，取值为从左下角开始先右后上   ...→...↑，即[经度格距,纬度格距]
        return self._RollGridValue

    @RollGridValue.setter
    def RollGridValue(self, value):
        self._RollGridValue = value

    def __init__(self, filename):
        self.filepath = filename
        with codecs.open(filename, 'r', encoding=default_encoding) as m4_open:
            m4 = str(m4_open.read())
            s = m4.split()
            if s[0] != "diamond" or s[1] != "4" or len(s) < 22:
                return

            # 属性信息
            self.propertyValue = list()
            for i in range(propertyLen):
                self.propertyValue.append(s[i + 2])

            self.desc = s[2]
            self.year = int(s[3])
            self.month = int(s[4])
            self.day = int(s[5])
            self.time = int(s[6])
            self.aging = int(s[7])
            self.level = int(s[8])
            self.LonGridLength = float(s[9])
            self.LatGridLength = float(s[10])
            self.StartLon = float(s[11])
            self.EndLon = float(s[12])
            self.StartLat = float(s[13])
            self.EndLat = float(s[14])
            self.LonGridNumber = int(s[15])
            self.LatGridNumber = int(s[16])
            self.ContourInterval = float(s[17])
            self.ContourStartValue = float(s[18])
            self.ContourEndValue = float(s[19])
            self.SmoothnessCoefficient = float(s[20])
            self.ThickenedLineValue = float(s[21])

            leng = self.LonGridNumber * self.LatGridNumber
            self.PixelValue = list()  # 数据信息
            # 一维数组
            for i in range(leng):
                if i + 22 < len(s):
                    self.PixelValue.append(float(s[i + 22]))

            self.MissValue = 9999.0

            # 二维格点
            self.GridValue = ay.zeros(self.LonGridNumber, self.LatGridNumber, float)
            for i in range(self.LonGridNumber):
                for j in range(self.LatGridNumber):
                    index = i * self.LatGridNumber + j
                    self.GridValue[i, j] = self.PixelValue[index]

    def ClipRegion(self, xMin, yMin, xMax, yMax):
        '''
        裁剪格点场
        :param xMin:
        :param yMin:
        :param xMax:
        :param yMax:
        :return:
        '''


class M4(Micaps4):
    '''
    Add micaps4 property format  output
    '''

    def micaps_desc(self):
        '''
        Micap 4 data property
        :return:
        '''
        self.disposeM4()
        print('The Micaps file contains  variables information:')
        info = ''
        info += str.format("\t{0}:{1}\n",FieldName[0],self.desc)
        info += str.format("\t{0}:{1}\n",FieldName[1],str(self.year))
        info += str.format("\t{0}:{1}\n", FieldName[2], str(self.month))
        info += str.format("\t{0}:{1}\n", FieldName[3], str(self.day))
        info += str.format("\t{0}:{1}\n", FieldName[4], str(self.time))
        info += str.format("\t{0}:{1}\n", FieldName[5], str(self.aging))
        info += str.format("\t{0}:{1}\n", FieldName[6], str(self.level))
        info += str.format("\t{0}:{1}\n", FieldName[7], str(self.LonGridLength))
        info += str.format("\t{0}:{1}\n", FieldName[8], str(self.LatGridLength))
        info += str.format("\t{0}:{1}\n", FieldName[9], str(self.StartLon))
        info += str.format("\t{0}:{1}\n", FieldName[10], str(self.EndLon))
        info += str.format("\t{0}:{1}\n", FieldName[11], str(self.StartLat))
        info += str.format("\t{0}:{1}\n", FieldName[12], str(self.EndLat))
        info += str.format("\t{0}:{1}\n", FieldName[13], str(self.LonGridNumber))
        info += str.format("\t{0}:{1}\n", FieldName[14], str(self.LatGridNumber))
        info += str.format("\t{0}:{1}\n", FieldName[15], str(self.ContourInterval))
        info += str.format("\t{0}:{1}\n", FieldName[16], str(self.ContourStartValue))
        info += str.format("\t{0}:{1}\n", FieldName[17], str(self.ContourEndValue))
        info += str.format("\t{0}:{1}\n", FieldName[18], str(self.SmoothnessCoefficient))
        info += str.format("\t{0}:{1}\n", FieldName[19], str(self.ThickenedLineValue))

        return info


# 以下是重写AlgorithmClass基类方法

    def print_property_info(self):
        property_info = self.micaps_desc()
        return property_info

    def get_variables_data(self):
        '''
        各店二维数组
        :return:
        '''
        return self.GridValue


    def get_data_by_name(self, name,**kwargs):
        pass

    def get_variable_by_name(self, variable_name,**kwargs):
        pass

    def get_dimension_by_name(self, dimension_name,**kwargs):
        pass


    def print_variable_property(self, name, var=None,**kwargs):
        '''
        打印变量属性信息
        :param name:变量名称
        :param var:
        :return:
        '''
        pass

    def print_dimension_property(self, name, var=None,**kwargs):
        pass

    # =================================

    def disposeM4(self):
        '''
        @名称: 解析m4文件
        @中文注释: 解析m4文件
        @入参:
            @param    path    str    文件路径
        @出参:
            @param  (headinfo,data)    tuple    返回头文件及数据

        @返回状态:
            @return    0    异常
            @return    1    成功
        @作    者: Mr.Wang
        @创建时间: 20190715
        @使用范例: disposeM4('./15121008.000')
        '''
        try:
            #4/0
            if os.path.exists(self.filepath):
                with open(self.filepath, 'r', encoding='gbk') as m4f:
                    mf = m4f.read().split()
                    if mf:
                        if len(mf) > 22:
                            if mf[0] + mf[1] == 'diamond4':
                                if str(mf[15]).isdigit() and str(mf[16]).isdigit():

                                    self.desc = mf[0] + mf[1] + mf[2]
                                    self.year = mf[3]
                                    self.month = mf[4]
                                    self.day = mf[5]
                                    self.ftime = mf[6]
                                    self.aging = mf[7]
                                    self.level = mf[8]
                                    self.LonGridLength = mf[9]
                                    self.LatGridLength = mf[10]
                                    self.StartLon = mf[11]
                                    self.EndLon = mf[12]
                                    self.StartLat = mf[13]
                                    self.EndLat = mf[14]





                                    self.LonGridNumber = mf[15]
                                    self.LatGridNumber = mf[16]
                                    self.ContourInterval = mf[17]
                                    self.ContourStartValue = mf[18]
                                    self.ContourEndValue = mf[19]
                                    self.SmoothnessCoefficient = mf[20]
                                    self.ThickenedLineValue = mf[21]
                                    if str(self.LatGridNumber).isdigit() and str(self.LonGridNumber).isdigit():
                                        print('Verify the integrity of Micaps data:(file={f})'.format(f=self.filepath))
                                        print('\tLatGridNumber = {lat}, LonGridNumber = {lon}'.format(
                                            lat=str(self.LatGridNumber), lon=str(self.LonGridNumber)))
                                        print('\tTotal data:{tot}'.format(tot=str(len(mf[22:]))))
                                        GridCount = int(self.LatGridNumber) * int(self.LonGridNumber)
                                        if GridCount == len(mf[22:]):
                                            print('\tVerify Micaps data success')
                                            self.m4data = np.array(mf[22:], dtype=np.float64).reshape(int(self.LatGridNumber), int(self.LonGridNumber))

                                        else:
                                            print('Failed to verify data,Default to 0 matrix:"np.zeros"')
                                            self.m4data = np.zeros((int(self.LatGridNumber), int(self.LonGridNumber)), dtype=np.int32)


            else:
                print('the path [{}] is empty!'.format(self.filepath))
        except Exception as arg:
            print('ERROR', arg.args)



if __name__ == "__main__":

    file_path = r"/home/trywangdao/mrcpysrc/m4/ER03/18072320.003"

    m4 = M4(file_path)

    print(m4.micaps_desc())

