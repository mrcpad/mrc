# -*- coding: utf-8 -*-

import sys
import time
import os
from module.algorithm.src import *
ppath = os.path.abspath('..')
ppath = os.path.join(ppath,'algorithm\src')
sys.path.append(ppath)
from module.algorithm.src.m4_to_nc.m4_to_nc import m4_to_nc_batGenNCfile, m4_to_ncGenNCfile
from module.algorithm.src.m4_to_hdf.m4_to_hdf import m4_to_hdf_batGenNCfile, m4_to_hdfGenNCfile
from module.algorithm.src.hdf_to_m4.hdf_m4_v2 import HDF_to_M4, batHDF_to_M4
from module.algorithm.src.nc_to_m4.nc_m4_v2 import NC_to_M4, batNC_to_M4

from module.algorithm.src.netcdf.convert2netCDF import nc2hdf, hdf2nc


import threading

from module.algorithm.src.startConvert.MessageBox import MyMessageBox



class switch(object):

    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False




value = 1

def convert(ft,vn, src, dst):
    global value

    """This script Implementing different files File Format Conversion.  Commands:--help"""


    if src:

        v = ft
        src = src.split(',')
        box = MyMessageBox()
        for case in switch(v):
            if case('nh'):
                try:
                    if len(src) == 1:
                        if os.path.isdir(src[0]):
                            ncList = getNCBatFiles(src[0])
                            batNCToHDFFileDeal(ncList, dst)
                            box.mrcinfo(msg='运行完成!')
                        elif os.path.isfile(src[0]):
                            if os.path.exists(dst):
                                (filepath, tempfilename) = os.path.split(src[0])
                                (filename, extension) = os.path.splitext(tempfilename)
                                ncflag = nc2hdf(src[0], os.path.join(dst, filename + '.hdf'))
                                if ncflag == 0:
                                    value = 0
                                    box.mrcinfo(msg='运行完成!')
                                else:
                                    value = 1
                                    box.mrccritical(msg='文件生成失败,请检查文件!')

                            else:
                                ncflag = nc2hdf(src[0], dst)
                                if ncflag == 0:
                                    value = 0
                                    box.mrcinfo(msg='运行完成!')
                                else:
                                    value = 1
                                    box.mrccritical(msg='文件生成失败,请检查文件!')


                    elif len(src) > 1:
                        batNCToHDFFileDeal(src, dst)
                        box.mrcinfo(msg='运行完成!')
                except:
                    box.mrccritical(msg='文件生成失败,解析文件出错，请检查文件!')

                break
            if case('hn'):
                try:
                    if len(src) == 1:
                        if os.path.isdir(src[0]):
                            hdfList = getHDFBatFiles(src[0])
                            batHDFToNCFileDeal(hdfList, dst)
                            box.mrcinfo(msg='运行完成!')
                        elif os.path.isfile(src[0]):
                            if os.path.exists(dst):
                                (filepath, tempfilename) = os.path.split(src[0])
                                (filename, extension) = os.path.splitext(tempfilename)
                                hdfflag = hdf2nc(src[0], os.path.join(dst, filename + '.nc'))
                                if hdfflag == 0:
                                    value = 0
                                    box.mrcinfo(msg='运行完成!')
                                else:
                                    value = 1
                                    box.mrccritical(msg='文件生成失败,请检查文件!')
                            else:
                                hdfflag = hdf2nc(src[0], dst)
                                if hdfflag == 0:
                                    value = 0
                                    box.mrcinfo(msg='运行完成!')
                                else:
                                    value = 1
                                    box.mrccritical(msg='文件生成失败,请检查文件!')

                    elif len(src) > 1:
                        batHDFToNCFileDeal(src, dst)
                        box.mrcinfo(msg='运行完成!')
                except:
                    box.mrccritical(msg='文件生成失败,解析文件出错，请检查文件!')
                break
            if case('nm'):
                if len(src) == 1:
                    if os.path.isdir(src[0]):
                        ncflag = batNC_to_M4(src[0], dst)
                        if ncflag[0] == 0:
                            value = 0
                            box.mrcinfo(msg='{count}个生成文件成功'.format(count=str(ncflag[1])))
                        else:
                            value = 1
                            box.mrcinfo(msg='生成文件失败')
                    elif os.path.isfile(src[0]):
                        flag = NC_to_M4(src[0], dst, '')
                        flag.ncclose()
                        if flag.flag == 0:
                            value = 0
                            box.mrcinfo(msg='生成文件成功')
                        else:
                            value = 1
                            box.mrcinfo(msg='生成文件失败')
                    else:
                        box.mrccritical(msg='源文件不存在!')
                elif len(src) > 1:
                    ncflag = batNC_to_M4(src, dst)
                    if ncflag[0] == 0:
                        value = 0
                        box.mrcinfo(msg='{count}个生成文件成功'.format(count=str(ncflag[1])))
                    else:
                        value = 1
                        box.mrcinfo(msg='生成文件失败')

                break
            if case('mn'):
                if len(src) == 1:
                    if os.path.isdir(src[0]):
                        flag = m4_to_nc_batGenNCfile(src[0], dst, 'variable000')
                        if flag == 0:
                            value = 0
                            box.mrcinfo(msg='生成文件成功')
                        else:
                            value = 1
                            box.mrcinfo(msg='生成文件失败,' + str(flag))
                    elif os.path.isfile(src[0]):
                        flag = m4_to_ncGenNCfile(src, dst, 'variable000')
                        if flag == 0:
                            value = 0
                            box.mrcinfo(msg='生成文件成功')
                        else:
                            value = 1
                            box.mrcinfo(msg='生成文件失败,' + str(flag))
                    else:
                        box.mrccritical(msg='源文件不存在!')
                elif len(src) > 1:
                    flag = m4_to_ncGenNCfile(src, dst, 'variable000')
                    if flag == 0:
                        value = 0
                        box.mrcinfo(msg='生成文件成功')
                    else:
                        value = 1
                        box.mrcinfo(msg='生成文件失败,' + str(flag))


                break
            if case('hm'):
                if len(src) == 1:
                    if os.path.isdir(src[0]):
                        hdfflag = batHDF_to_M4(src[0], dst)
                        if hdfflag[0] == 0:
                            value = 0
                            box.mrcinfo(msg='{count}个生成文件成功'.format(count=str(hdfflag[1])))
                        else:
                            value = 1
                            box.mrcinfo(msg='生成文件失败')
                    elif os.path.isfile(src[0]):
                        flag = HDF_to_M4(src[0], dst, '')
                        flag.hdfclose()
                        if flag.flag == 0:
                            value = 0
                            box.mrcinfo(msg='生成文件成功')
                        else:
                            value = 1
                            box.mrcinfo(msg='生成文件失败')
                    else:
                        box.mrccritical(msg='源文件不存在!')
                elif len(src) > 1:
                    hdfflag = batHDF_to_M4(src, dst)
                    if hdfflag[0] == 0:
                        value = 0
                        box.mrcinfo(msg='{count}个生成文件成功'.format(count=str(hdfflag[1])))
                    else:
                        value = 1
                        box.mrcinfo(msg='生成文件失败')



                break
            if case('mh'):
                if len(src) == 1:
                    if os.path.isdir(src[0]):
                        flag = m4_to_hdf_batGenNCfile(src[0], dst, 'variable000')
                        if flag == 0:
                            value = 0
                            box.mrcinfo(msg='生成文件成功')
                        else:
                            value = 1
                            box.mrcinfo(msg='生成文件失败,' + str(flag))
                    elif os.path.isfile(src[0]):
                        flag = m4_to_hdfGenNCfile(src, dst, 'variable000')
                        if flag == 0:
                            value = 0
                            box.mrcinfo(msg='生成文件成功')
                        else:
                            value = 1
                            box.mrcinfo(msg='生成文件失败,' + str(flag))
                elif len(src) > 1:
                    flag = m4_to_hdfGenNCfile(src, dst, 'variable000')
                    if flag == 0:
                        value = 0
                        box.mrcinfo(msg='生成文件成功')
                    else:
                        value = 1
                        box.mrcinfo(msg='生成文件失败,' + str(flag))
                break
            if case('gm'):
                break
            if case('gn'):
                break
            if case('gh'):
                break
            if case('ng'):
                print('Successful file generation')
                break
            if case('hg'):
                print('Successful file generation')
                break
            if case('mg'):
                print('Successful file generation')
                break
            if case():  # default, could also just omit condition or 'if True'
                print('ERROR KEY:"%s"!'%v)
                break


    else:
        print('src:%s not exist!'%src)
    return value







def batNCToHDFFileDeal(flist,dst):
    if flist:
        thread_list = []

        for file in flist:
            (filepath, tempfilename) = os.path.split(file)
            (filename, extension) = os.path.splitext(tempfilename)
            t = threading.Thread(target=nc2hdf, args=(file, os.path.join(dst, filename + '.hdf')))

            t.start()
            t.join()
        for t in thread_list:
            t.join()


def batHDFToNCFileDeal(flist,dst):
    if flist:
        thread_list = []

        for file in flist:
            (filepath, tempfilename) = os.path.split(file)
            (filename, extension) = os.path.splitext(tempfilename)

            t = threading.Thread(target=hdf2nc, args=(file, os.path.join(dst, filename + '.nc')))

            t.start()
        for t in thread_list:
            t.join()




def getGRBBatFiles(path):

    flist = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.grb' or os.path.splitext(file)[1] == '.GRB' or os.path.splitext(file)[1] == '.grb2':
                flist.append(os.path.join(root, file))
    return flist

def getNCBatFiles(path):

    flist = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.nc' or os.path.splitext(file)[1] == '.NC':
                flist.append(os.path.join(root, file))
    return flist

def getHDFBatFiles(path):

    flist = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.hdf' or os.path.splitext(file)[1] == '.HDF':
                flist.append(os.path.join(root, file))
    return flist

if __name__ == '__main__':
    pass
    ft = 'nh'
    vn = ''
    src = r'D:\PanoplyWin\ncfile.nc'
    dst = r'D:\PanoplyWin\t1\tmp'
    #convert(ft, vn, src, dst)





