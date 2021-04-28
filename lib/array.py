#!/usr/bin/env python
# !-*-coding:utf-8 -*-

'''
版本 ：v1.0.0
创建 ：xxf at 2019/03/13 12:56
更新内容 ：创建数组

版本 ：v1.0.1
更新 ：xxf at 2019/
更新内容 ：

'''

import numpy as np


def zeros(x, y, type):
    '''
    create array from function
    all data =0
    :param x:
    :param y:
    :param type:
    :return:
    '''
    return from_lambda(lambda a, b: (a + b) * 0, x, y, type)


def from_lambda(lambda_fun, x, y, type):
    '''
    create array from function
    :param lambda_fun:
    :param x:行
    :param y:列
    :param type:数据类型
    :return:
    '''
    array = np.fromfunction(lambda_fun, (x, y), dtype=type)
    return array
