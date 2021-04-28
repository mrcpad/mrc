#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: 
@author: 
@site: 
@software: PyCharm
@file: 启动主程序
@time: 2019/7/18
"""

import sys
from PyQt5.QtWidgets import *
from module.mrc_app.mainfrom import *
#import startup as sp



# def setGloalConfig():



if __name__ == "__main__":



    app = QApplication(sys.argv)
    mian = QMainWindow()
    mian_from = MainFrom()
    mian_from.setupUi(mian)
    #mian.statusBar().showMessage('准备中...')

    # mian=QWidget()
    #mian.resize(300,300)
    # mian.move(300,300)

    icon = QtGui.QIcon()
    # icon.addPixmap(QtGui.QPixmap("D:\\workspace09\\MMS2_MRC\\config\\image\\globe.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    mian.setWindowIcon(icon)


    mian.show()

    sys.exit(app.exec_())