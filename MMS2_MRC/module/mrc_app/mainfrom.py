# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!


#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version:
@author:
@site:
@software: PyCharm
@file: mianFrom界面层
@time: 2019-7-24
"""


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication as qApp
from PyQt5.QtGui import QGuiApplication as qGuiApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect
from module.mrc_app.menuloader import MenuLoader
from module.mrc_app.toolbarloader import ToolBarLoader
from module.mrc_controls.treewidget import MrcTreeWidget
from module.mrc_controls.textbrowser import MrcTextBrowser
from module.mrc_controls.tabWidget import MrcTabWidget

#from logs.log import logger


class MainFrom(QMainWindow):


    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        screen = qGuiApp.primaryScreen()
        MainWindow.resize(screen.size().width(), screen.size().height()-100)
        #MainWindow.setStyleSheet("#MainWindow{background-color: #F0FC9D}")
        #MainWindow.setStyleSheet("#MainWindow{border-image:url(./timg.jpg);}")
        self.mianWindow=MainWindow
        self.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.textBrowser = MrcTextBrowser(self.centralwidget)

        self.textBrowser.hide()

        self.tabWidget = MrcTabWidget(self.centralwidget)

        self.tabWidget.setObjectName("tabWidget")

        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        #self.horizontalLayout_2.addWidget(self.textBrowser)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.mianWindow.setWindowIcon(QIcon('D:\\workspace09\\MMS2_MRC\\config\\image\\globe.ico'))


        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        #self.statusbar.showMessage('准备中...')
        #MainWindow.statusBar().showMessage('准备中...')

        self.dockWidget_3 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_3.setFloating(False)
        self.dockWidget_3.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.dockWidget_3.setObjectName("dockWidget_3")
        #self.dockWidget_3.setGeometry(QRect(0,66,780,758))
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.dockWidgetContents_3.setGeometry(QRect(0,66,780,758))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.dockWidgetContents_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treewidget = MrcTreeWidget(self.dockWidgetContents_3)#单独写个类，返回QTableView对象，在这里加载
        self.treewidget.setObjectName("QTreeWidget")
        self.treewidget.setStyleSheet("#QTreeWidget{background-color: #F0FC9D}")
        self.treewidget.textBrowser = self.textBrowser#设置文本框
        self.treewidget.statusBar = self.statusbar#设置底部状态栏
        self.treewidget.settabWidget(self.tabWidget)
        #self.treewidget.SetStatusBar()
        #self.treewidget.setObjectName("treewidget")
        self.treewidget.setMinimumSize(QtCore.QSize(785, 703))
        self.horizontalLayout.addWidget(self.treewidget)
        self.dockWidget_3.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_3)
        self.dockWidget_3.raise_()


        #加载菜单栏
        menu_loader = MenuLoader(MainWindow, self.textBrowser, self.treewidget, self.tabWidget)
        self.menubar= menu_loader.CreateQMenu()
        MainWindow.setMenuBar(self.menubar)
        #加载工具栏
        toolbar_loader = ToolBarLoader(MainWindow, self.textBrowser, self.treewidget, self.tabWidget)
        self.toolBar = toolbar_loader.CreateQToolBar()
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

















        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        '''
        初始化主界面属性，要改为从app.config配置文件中读取
        :param MainWindow:
        :return:
        '''
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "模式产品读书器"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.dockWidget_3.setWindowTitle(_translate("MainWindow", "文件列表"))










