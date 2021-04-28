#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: 
@author: xxf
@site: 
@software: PyCharm
@file: 自定义控件基类
@time: 2019-7-31
"""

from module.mrc_controls.basecontrol import IBaseControl

class BaseControl(IBaseControl):

    @property
    def textBrowser(self):  # 文本显示控件
        return self._textBrowser

    @textBrowser.setter
    def textBrowser(self, value):
        self._textBrowser = value

    @property
    def statusBar(self):  # 底部状态栏
        return self._statusBar

    @statusBar.setter
    def statusBar(self, value):
        self._statusBar = value

