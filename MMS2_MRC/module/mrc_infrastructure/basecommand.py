#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: v0.1
@author: xxf
@site: 
@software: PyCharm
@file: 命令抽象类，所有命令都实现该类，完成命令调用
@time: 2019-7-26
"""


from module.mrc_infrastructure.iCommand import ICommand


class BaseCommand(ICommand):


    def InitCmd(self,actionQ):
        '''
        实现接口，绑定Action
        :param actionQ:
        :return:
        '''
        actionQ.triggered['bool'].connect(self.Init)#Action信号连接Init槽函数
        self.action=actionQ


    def Init(self):
        '''
        子类重写
        :return:
        '''
        pass

