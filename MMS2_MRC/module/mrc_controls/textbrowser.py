#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: v0.1
@author: xxf
@site: 
@software: PyCharm
@file: 文本展示控件，继承QTextBrowser
@time: 2019-7-31
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from module.mrc_controls.basecontrol import IBaseControl


class MrcTextBrowser(QTextBrowser,IBaseControl):


    def __init__(self, parent=None):
        super(MrcTextBrowser,self).__init__(parent)
        #self.setPropertyInfo()  # 初始化属性信息
        self.setStyleSheet('''
                        QTextBrowser{
                        background:white;
                    border-top:1px solid white;
                    border-bottom:1px solid white;
                    border-left:1px solid white;
                    border-top-left-radius:20px;
                    border-bottom-left-radius:20px;
                    border-top-right-radius:20px;
                    border-bottom-right-radius:20px;
                    font-size:14px;
                    font-weight:700;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                        }

                        ''')
        pass



    def setPropertyInfo(self):
        pass
        #self.setText('解码信息展示')
