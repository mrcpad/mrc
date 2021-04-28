#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: v0.1
@author: xxf
@site: 
@software: PyCharm
@file: 执行命令接口
@time: 2019-7-26
"""


class ICommand(object):

    @property
    def mainWindow(self):
        return self._mainWindow

    @mainWindow.setter
    def mainWindow(self, value):
        self._mainWindow=value

    @property
    def textBrowser(self):#文本显示控件
        return self._textBrowser

    @textBrowser.setter
    def textBrowser(self, value):
        self._textBrowser = value

    @property
    def treeWidget(self):#树形结构控件
        return self._treeWidget

    @treeWidget.setter
    def treeWidget(self, value):
        self._treeWidget = value

    @property
    def tabWidget(self):
        return self._tabWidget

    @tabWidget.setter
    def tabWidget(self, value):
        self._tabWidget = value




    def InitCmd(self,actionQ):
        '''
        命令接口
        :param actionQ:注入指定的Action
        :return:
        '''
        pass
