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


from module.mrc_infrastructure.basecommand import BaseCommand

class ExitSystemCmd(BaseCommand):
    '''
    退出程序
    '''

    def Init(self):
        print(self.action)