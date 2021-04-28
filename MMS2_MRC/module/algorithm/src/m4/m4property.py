# -*- coding: gbk -*-


class Micaps4property(object):

    @property
    def desc(self):  # ����
        return self._desc

    @desc.setter
    def desc(self, value):
        self._desc = value
    @property
    def year(self):  # ��
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

    @property
    def month(self):  # ��
        return self._month

    @month.setter
    def month(self, value):
        self._month = value

    @property
    def day(self):  # ��
        return self._day

    @day.setter
    def day(self, value):
        self._day = value

    @property
    def ftime(self):  # ʱ��
        return self._ftime

    @ftime.setter
    def ftime(self, value):
        self._ftime = value

    @property
    def aging(self):  # ʱЧ
        return self._aging

    @aging.setter
    def aging(self, value):
        self._aging = value

    @property
    def level(self):  # ���
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def LonGridLength(self):  # ���ȸ��
        return self._LonGridLength

    @LonGridLength.setter
    def LonGridLength(self, value):
            self._LonGridLength = float(value) if value != '' else value

    @property
    def LatGridLength(self):  # γ�ȸ��
        return self._LatGridLength

    @LatGridLength.setter
    def LatGridLength(self, value):
        self._LatGridLength = float(value) if value != '' else value

    @property
    def StartLon(self):  # ��ʼ����
        return self._StartLon

    @StartLon.setter
    def StartLon(self, value):
        self._StartLon = float(value) if value != '' else value

    @property
    def EndLon(self):  # ��ֹ����
        return self._EndLon

    @EndLon.setter
    def EndLon(self, value):
        self._EndLon = float(value) if value != '' else value

    @property
    def StartLat(self):  # ��ʼγ��
        return self._StartLat

    @StartLat.setter
    def StartLat(self, value):
        self._StartLat = float(value) if value != '' else value

    @property
    def EndLat(self):  # ��ֹγ��
        return self._EndLat

    @EndLat.setter
    def EndLat(self, value):
        self._EndLat = float(value) if value != '' else value

    @property
    def LatGridNumber(self):  # γ������
        return self._LatGridNumber

    @LatGridNumber.setter
    def LatGridNumber(self, value):
        self._LatGridNumber = int(value) if value != '' else value

    @property
    def LonGridNumber(self):  # ��������
        return self._LonGridNumber

    @LonGridNumber.setter
    def LonGridNumber(self, value):
        self._LonGridNumber = int(value) if value != '' else value

    @property
    def ContourInterval(self):  # ��ֵ�߼��
        return self._ContourInterval

    @ContourInterval.setter
    def ContourInterval(self, value):
        self._ContourInterval = float(value) if value != '' else value

    @property
    def ContourStartValue(self):  # ��ֵ����ʼֵ
        return self._ContourStartValue

    @ContourStartValue.setter
    def ContourStartValue(self, value):
        self._ContourStartValue = float(value) if value != '' else value

    @property
    def ContourEndValue(self):  # ��ֵ����ֵֹ
        return self._ContourEndValue

    @ContourEndValue.setter
    def ContourEndValue(self, value):
        self._ContourEndValue = float(value) if value != '' else value

    @property
    def SmoothnessCoefficient(self):  # ƽ��ϵ��
        return self._SmoothnessCoefficient

    @SmoothnessCoefficient.setter
    def SmoothnessCoefficient(self, value):
        self._SmoothnessCoefficient = float(value) if value != '' else value

    @property
    def ThickenedLineValue(self):  # �Ӵ���ֵ
        return self._ThickenedLineValue

    @ThickenedLineValue.setter
    def ThickenedLineValue(self, value):
        self._ThickenedLineValue = value

    @property
    def MissValue(self):  # ��Чֵ
        return self._MissValue

    @MissValue.setter
    def MissValue(self, value):
        self._MissValue = value

    @property
    def PixelValue(self):  # ���ֵ   һά����
        return self._PixelValue

    @PixelValue.setter
    def PixelValue(self, value):
        self._PixelValue = value

    @property
    def GridValue(self):  # ����λ���飬ȡֵΪ�����½ǿ�ʼ���Һ���   ...��...������[���ȸ��,γ�ȸ��]
        return self._GridValue

    @GridValue.setter
    def GridValue(self, value):
        self._GridValue = value

    @property
    def RollGridValue(self):  # ��ת����λ���飬ȡֵΪ�����½ǿ�ʼ���Һ���   ...��...������[���ȸ��,γ�ȸ��]
        return self._RollGridValue

    @RollGridValue.setter
    def RollGridValue(self, value):
        self._RollGridValue = value

    @property
    def m4data(self):  # ����
        return self._m4data

    @m4data.setter
    def m4data(self, value):
        self._m4data = value



from itertools import islice
import numpy as np
import re
import os

import wrapt
import logging


def logginginfo(level):
    logpath = os.path.join(os.path.abspath('.'), 'log')
    if not os.path.exists(logpath):
        os.makedirs(logpath)
        # print(os.path.abspath('..'))

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        import logging
        logging.basicConfig(level=logging.INFO,
                            filename=os.path.join(logpath, 'service.log'),
                            filemode='a',
                            format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

        # print "[{level}]: enter function {func}()".format(level=level, func=wrapped.__name__)
        logging.info("[{level}]: enter function {func}()".format(level=level, func=wrapped.__name__))
        return wrapped(*args, **kwargs)

    return wrapper






class DisposeM4file(Micaps4property):
    '''
    m4�ļ�����
    '''
    def __init__(self, filepath):

        self.filepath = filepath

    @staticmethod
    def not_empty(s):
        '''
        ȥ�����ַ�
        :param s:
        :return:
        '''
        return s and s.strip()



    @logginginfo(level="INFO")
    def disposeM4First(self):
        '''
        @����: ����m4�ļ�
        @����ע��: ����m4�ļ�
        @���:
            @param    path    str    �ļ�·��
        @����:
            @param  (headinfo,data)    tuple    ����ͷ�ļ�������

        @����״̬:
            @return    0    �쳣
            @return    1    �ɹ�
        @��    ��: Mr.Wang
        @����ʱ��: 20190715
        @ʹ�÷���: disposeM4('./15121008.000')
        '''
        try:
            #4/0
            if os.path.exists(self.filepath):
                with open(self.filepath, 'r', encoding='gbk') as m4f:
                    m4f.seek(0)
                    headinfo = list()
                    # ��ȡͷ��Ϣ
                    for line in islice(m4f, 0, 1):
                        info = line.replace('\n', '').lstrip()
                        headinfo.append(info)
                    self.desc = headinfo[0]
                    m4f.seek(0)
                    tmp = list()
                    # ��ȡͷ����
                    for line in islice(m4f, 1, 3):
                        info = re.split('\s+', line.replace('\n', '').lstrip())
                        tmp.extend(info)
                    headinfo.append(tmp)


                    self.year = tmp[0]
                    self.month = tmp[1]
                    self.day = tmp[2]
                    self.ftime = tmp[3]
                    self.aging = tmp[4]
                    self.level = tmp[5]
                    self.LonGridLength = tmp[6]
                    self.LatGridLength = tmp[7]
                    self.StartLon = tmp[8]
                    self.EndLon = tmp[9]
                    self.StartLat = tmp[10]
                    self.EndLat = tmp[11]
                    self.LatGridNumber = tmp[12]
                    self.LonGridNumber = tmp[13]
                    self.ContourInterval = tmp[14]
                    self.ContourStartValue =tmp[15]
                    self.ContourEndValue = tmp[16]
                    self.SmoothnessCoefficient = tmp[17]



                    data = list()
                    pdata = list()
                    m4f.seek(0)
                    # ��ȡ���ݲ���
                    for line in islice(m4f, 4, None):
                        result = re.split('\s+', line.replace('\n', '').strip())
                        # print(line.replace('\n', '').strip())
                        pdata.extend(list(filter(self.not_empty, result)))
                        if line == '\n':
                            data.append(pdata)
                            pdata = []

                    data.append(pdata)
                    a = np.array(data, dtype=np.float64)
                    self.m4data = a
                    #print(a.shape)
                    return self
            else:
                print('the path [{}] is empty!'.format(self.filepath))
        except Exception as arg:
            print('ERROR', arg.args)
            logging.error(self.filepath + ':' + str(arg.args))



    def disposeM4(self):
        '''
        @����: ����m4�ļ�
        @����ע��: ����m4�ļ�
        @���:
            @param    path    str    �ļ�·��
        @����:
            @param  (headinfo,data)    tuple    ����ͷ�ļ�������

        @����״̬:
            @return    0    �쳣
            @return    1    �ɹ�
        @��    ��: Mr.Wang
        @����ʱ��: 20190715
        @ʹ�÷���: disposeM4('./15121008.000')
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
                                        GridCount = int(self.LatGridNumber) * int(self.LonGridNumber)
                                        if GridCount == len(mf[22:]):
                                            self.m4data = np.array(mf[22:], dtype=np.float64).reshape(int(self.LatGridNumber), int(self.LonGridNumber))
                                        else:

                                            self.m4data = np.zeros((int(self.LatGridNumber), int(self.LonGridNumber)), dtype=np.int32)
                            else:
                                raise Exception
                        else:
                            raise Exception

                    return self
            else:
                print('the path [{}] is empty!'.format(self.filepath))
        except Exception as arg:
            print('ERROR', arg.args)
            logging.error(self.filepath + ':' + str(arg.args))
            return self.filepath, None
if __name__ == '__main__':

    #d = DisposeM4file(r'D:\PanoplyWin\t1\ER03\18072320.003')
    d = DisposeM4file(r'D:\PanoplyWin\18072320.009.csv')
    d.disposeM4()
    #d = DisposeM4file('./15121508.000')
    #print(d.m4data)
    #print(d.desc)