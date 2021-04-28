#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: 
@author: 
@site: 
@software: PyCharm
@file: 
@time: 
"""

from grib.write.wGRIB.nwfd_g2lib import Data2Grib
from m4.m4property import DisposeM4file
import os


def m4_2_grib_smilpe_files(micapsfiles):
    '''
    将多个micaps文件转成grib2
    :param micapsfiles:文件数组
    :param category:产品种类
    :param element:产品编号
    :param statistical:统计方式
    :param leveltype:层次类型
    :param level:层次值
    :param istimepoint:是否是时间点产品
    :param generating_method:生成方式
    :param status:产品状态
    :param discipline:学科
    :return:
    '''

    messages = []
    for file in micapsfiles:
        message = m4_2_grib_smilped(file)

        messages.append(message)

    return messages


def m4_2_grib_smilped(micapsfile):
    '''
    将一个micaps转码为grib2 message
    :param micapsfile:
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
    m4 = DisposeM4file(micapsfile)
    m4 = m4.disposeM4()
    field = m4.m4data  # 格点场数据

    # 读取配置获取产品编码信息
    # discipline = 0  # 学科
    year = (2000 + int(m4.year)) if len(str(m4.year)) == 2 else m4.year
    month = m4.month
    day = m4.day
    hour = m4.ftime
    minute = 0
    second = 0
    level = m4.level

    # status = 0  # 产品状态
    # category = 0 #产品种类
    # element = 0 #产品编号
    # statistical = 0 #统计方式 （模板4.8）
    # leveltype = 103 #层次类型
    # level = 2   #层次值
    forecasttime = int(m4.aging)  # 距离预报基准日期时间的预报起报小时，如，0，3,6,9,12等

    # isforecast = True #是否是预报； True:是预报； False:为实况
    # istimepoint = True  #预报数据是否是某个时间点的数据； Ture:为某个时间点，False:为某个时间段
    timerange = 3  # 预报间隔小时数，如3,6,12,24等   ? 暂时写3,20191119
    curPath = os.path.abspath(os.path.dirname(__file__))
    g2lib = Data2Grib(os.path.join(curPath, 'grib_stb_config.conf'))

    if g2lib.cfg == 0:
        ngrdpts = m4.LatGridNumber * m4.LonGridNumber

        g2lib.data2grib_info(m4.StartLat, m4.StartLon, m4.EndLat, m4.EndLon, m4.LatGridLength, m4.LonGridLength,
                             m4.LatGridNumber, m4.LonGridNumber)

        g2lib.data2grib_smiple(year, month, day, hour, minute, second,forecasttime, timerange, field, ngrdpts, level)

        return g2lib.message
    else:
        return




def get_m4_fileName(path):
    gz_fileName = list()
    for root, dirs, files in os.walk(path):
        for gzfile in files:
            if len(os.path.splitext(gzfile)[1].split('.')[1]) == 3 and os.path.splitext(gzfile)[1].split('.')[1].isdigit():
                gz_fileName.append(os.path.join(root, gzfile))
    return sorted(gz_fileName)

def generateFile(m4path,outpath):
    files = get_m4_fileName(m4path)
    messages = m4_2_grib_smilpe_files(files)
    if messages:
        with open(outpath,'wb') as grbs:
            for msg in messages:
                if msg is not None:
                    grbs.write(msg.msg)
        print('inner: GRIB file generated successfully')
        return 0



if __name__ == '__main__':
    generateFile(r'/home/trywangdao/mrcpysrc/m4/ER03', r'ER03.grb')



    #f = open('test_masked_RH.grb', 'wb')

    # directorys=[r'/home/mrcadmin/xxf/m4/',r'/home/mrcadmin/xxf/m4_tm/']
    # for directory in directorys:
    #files = get_m4_fileName(r'/home/trywangdao/mrcpysrc/m4/RH')

    #files = gp.get_files(r'/home/trywangdao/mrcpysrc/m4/ER03/')
    #messages = m4_2_grib_smilpe_files(files, 0, 224, 0, 1, 20, 99,True)

    #for msg in messages:
        # write it to the file.
        #f.write(msg.msg)

    # files = get_m4_fileName(r'/home/trywangdao/mrcpysrc/m4/ER03/')
    # messages = m4_2_grib_smilpe_files(files, 0, 0, 0, 103, 2, 100,True)
    #
    # for msg in messages:
    #     # write it to the file.
    #     f.write(msg.msg)
    # # close the output file
    # files = get_m4_fileName(r'/home/trywangdao/mrcpysrc/m4/ER03/')
    # messages = m4_2_grib_smilpe_files(files, 19, 0, 0, 103, 2, 101, True)
    #
    # for msg in messages:
    #     # write it to the file.
    #     f.write(msg.msg)
    # files = get_m4_fileName(r'/home/trywangdao/mrcpysrc/m4/ER03/')
    # messages = m4_2_grib_smilpe_files(files, 6, 1, 0, 103, 2, 102, True)
    #
    # for msg in messages:
    #     # write it to the file.
    #     f.write(msg.msg)

    #f.close()

    # s = pygrib.Grib2Decode('test_masked.grb')
    # print(s)
    # print(s.values)
