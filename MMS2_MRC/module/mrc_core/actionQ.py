#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: 
@author: xxf
@site: 
@software: PyCharm
@file: 创建ActionQ继承QAction,增加tag属性
@time: 2019-07-26
"""

from PyQt5.QtWidgets import QAction

class ActionQ(QAction):

    @property
    def tag(self):  #command命令
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value
