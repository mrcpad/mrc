# !-*-coding:utf-8 -*-

# company hitec
# projectName ynjc
# by XXf at 2019/02/14 09:29
# describe Get different categories of directories


'''
版本 ：v1.0.0
创建 ：xxf
更新内容 ：
一、路径获取辅助类
版本 ：v1.0.1
at 2019/03/13 10:11
更新内容 ：
增加方法filename_add_extension：将文件路径解析出文件名，并合同成指定扩展名的文件名

'''

import os
import sys
#getpath.py

def createdirifnotexists(directory):
    # 去除首位空格
    directory = directory.strip()
    # 去除尾部 \ 符号
    directory = directory.rstrip("\\")
    isexists = os.path.exists(directory)
    if isexists == False:
        try:
            os.makedirs(directory)
            return True
        except OSError as oserr:
            print("OSError:")
            return False


def filename_add_extension(filepath, extension):
    '''
    将文件路径解析出文件名，并合同成指定扩展名的文件名
    :param filepath:
    :param extension:扩展名
    :return:
    '''
    name_no_extension = get_filename_without_extension(filepath)
    if name_no_extension != 'No extension':
        return name_no_extension + "." + extension
    else:
        return filepath


def get_filename_without_extension(filepath):
    '''
    将文件路径解析出不带扩展名的文件名
    :param filepath:
    :return:
    '''

    filename = os.path.basename(filepath)
    name_no_extension = filename.split('.')
    if len(name_no_extension) == 1:
        return 'No extension'
    else:
        return name_no_extension[0]


def get_extension(filepath):
    '''
        返回文件扩展名
        :param filepath:
        :return:
    '''

    filename = os.path.basename(filepath)
    name_no_extension = filename.split('.')
    if len(name_no_extension) == 1:
        return 'No extension'
    else:
        return name_no_extension[1]


def get_filename(filepath):
    '''
    将文件路径解析出文件名
    :param filepath:
    :return:
    '''

    filename = os.path.basename(filepath)
    return filename

def get_files(directory,extension):
    '''
    指定目录筛选extension类型的文件
    :param directory:
    :param extension:
    :return:
    '''

    file_path_list=[]
    file_list= os.listdir(directory)
    for file in file_list:
        if get_extension(file)!=extension:
            continue
        file_path=directory+'/'+file
        if os.path.isfile(file_path):
            file_path_list.append(file_path)

    return file_path_list

def get_path(filepath):
    '''
    将文件路径解析出不包含文件名的路径
    :param filepath:
    :return:
    '''

    path = os.path.dirname(filepath)
    return path


def get_element_at_index(file, split, index):
    '''
    返回文件名被split分割后在index索引处的值
    :param file:
    :param index:索引
    :return:
    '''

    if os.path.isdir(file):
        return None

    if os.path.isfile(file):
        file_name = get_filename_without_extension(file)
        file_name_split = file_name.split(split)
        result = file_name_split[index]
        return result


def combine_path_name(filepath, filename):
    return filepath + '/' + filename
