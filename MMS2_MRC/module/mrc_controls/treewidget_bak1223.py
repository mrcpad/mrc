#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: v0.1
@author: xxf
@site: 
@software: PyCharm
@file: 树形节点控件，展示文件列表信息
@time: 2019-7-31
"""


from module.mrc_controls.controlbase import BaseControl
import netCDF4 as nct
import lib.getpath as gp
from module.algorithm.algorithmbase import PyMeteoObject
from module.algorithm.src.dispose.showinfo import DisposeNetCDF
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
from module.Factory.algorithm import AlgorithmFactorytz
from lib.judgetype import ModelDataType
import lib.judgetype as jt
from module.algorithm.src.m4.m4property import DisposeM4file


class MrcTreeWidget(QTreeWidget, BaseControl):
    '''
    继承QTreeWidget
    '''

    @property
    def algorithmObject(self):
        return self._algorithmObject

    @algorithmObject.setter
    def algorithmObject(self, value):
        self._algorithmObject = value if isinstance(value, dict) else None

    # @property
    # def tabWidget(self):
    #     return self._tabWidget
    #
    # @tabWidget.setter
    # def tabWidget(self, value):
    #     self._tabWidget = value

    def __init__(self, parent=None):
        super(MrcTreeWidget, self).__init__(parent)
        self.rootlist = list()
        self.fdict = dict()
        self.removeFlag = 1
        self.grpvar = None
        self.files = []
        self.setPropertyInfo()  # 初始化属性信息、
        self.clicked.connect(self.OnTreeClicked)  # 点击信号连接槽信号
        #self.doubleClicked.connect(self.doubleTreeClicked)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.generateMenu)

        self.setObjectName("QTreeWidget")
        #self.setStyleSheet("#QTreeWidget{background-color: #F0FC9D}")
        self.setAcceptDrops(True)

        # 鼠标拖入事件
    def dragEnterEvent(self, evn):

        # 鼠标放开函数事件
        evn.accept()


    # 鼠标放开执行
    def dropEvent(self, evn):

        file = evn.mimeData().text().replace('file:///','')
        extent = os.path.splitext(file)[1]
        if extent.upper() in ['.HDF', '.NC', '.GRB', '.GRB2']:
            self.AlgorithmFactory = AlgorithmFactorytz
            self.SetTreeWidgetItem([file])
            self.removeFlag = 0


    def dragMoveEvent(self, evn):
        pass
        #print('鼠标移入')
    def settabWidget(self,tabWidget):
        print(1111)
        self.tabWidget = tabWidget

    def setPropertyInfo(self):
        # self.setProperty(name=None,value=None)

        self.setColumnCount(3)
        self.setHeaderLabels(['名称', '类型','数据路径','备注'])  # 展示3个要素
        # 将第一列的单元宽度设置为150
        self.setColumnWidth(0,400)
        self.setColumnWidth(1,50)

        self.setColumnHidden(2, True)#隐藏‘数据路径’
        self.setColumnHidden(3, True)  # 隐藏‘备注’
        #print(self.width())
        #self.setMaximumWidth(202)
        self.algorithmObject = {}
        self.setStyleSheet('''
                QTreeWidgetItem{
                background:#F0F0F0;
            border-top:1px solid white;
            border-bottom:1px solid white;
            border-left:1px solid white;
            border-top-left-radius:20px;
            border-bottom-left-radius:20px;
            border-top-right-radius:20px;
            border-bottom-right-radius:20px;
                }
                ''')



    def SetTreeWidgetItem(self, files):


        self.files = files

        for file in self.files:
            algorithmObject = PyMeteoObject()
            algorithmObject.file = file
            algorithmObject.fileName = gp.get_filename(file)
            algorithmObject.meteoDataInfo,modelDataType = self.AlgorithmFactory.create_algorithm(file)

            #modelDataType = jt.judge_model_data_type(file)

            if modelDataType == ModelDataType.NETCDF:
                grpvar = DisposeNetCDF(file)
                self.grpvar = grpvar
                self.grpinfo = grpvar.getgrpAndVariableInfo()
                textContext = algorithmObject.meteoDataInfo.print_property_info()
                self.tabWidget.tab1UI(textContext)
                self.fdict[str(file)] = [self.grpinfo, textContext]
                root = QTreeWidgetItem(self)
                self.rootlist.append(root)
                root.setText(0, algorithmObject.fileName)
                #root.setText(1, algorithmObject.fileName)
                root.setText(1, 'Local File')
                root.setText(2, file)
                root.setText(3, 'NETCDF')
                # brush_red = QBrush(Qt.red)
                root.setBackground(0, QBrush(QColor(237, 243, 254)))
                # brush_blue = QBrush(Qt.blue)
                root.setBackground(1, QBrush(QColor(237, 243, 254)))
                root.setBackground(2, QBrush(QColor(237, 243, 254)))
                tmp = list(self.grpinfo.values())[0]
                if isinstance(tmp, nct.Variable):
                    for k, v in self.grpinfo.items():
                        child1 = QTreeWidgetItem()
                        child1.setText(0, k)
                        #child1.setText(1, k)
                        child1.setText(1, 'Geo2D' if len(v.shape) > 1 else '1D')
                        child1.setText(2, file)
                        child1.setText(3, 'NETCDF Child')
                        root.addChild(child1)



                elif isinstance(tmp, dict):
                    for k, v in self.grpinfo.items():
                        child1 = QTreeWidgetItem()
                        child1.setText(0, k)
                        #child1.setText(1, k)
                        child1.setText(1, '    ***  ')
                        child1.setText(2, file)
                        child1.setText(3, 'NETCDF Group')
                        root.addChild(child1)
                        for val in v:
                            child3 = QTreeWidgetItem(child1)
                            child3.setText(0, val)
                            #child3.setText(1, val)
                            child3.setText(1, 'Geo2D' if len(v[val].shape) > 1 else '1D')
                            child3.setText(2, file)
                            child3.setText(3, 'NETCDF Chlid')

            elif modelDataType == ModelDataType.HDF:
                grpvar = DisposeNetCDF(file)
                self.grpvar = grpvar
                self.grpinfo = grpvar.getgrpAndVariableInfo()
                textContext = algorithmObject.meteoDataInfo.print_property_info()
                self.tabWidget.tab1UI(textContext)
                self.fdict[str(file)] = [self.grpinfo, textContext]
                root = QTreeWidgetItem(self)
                self.rootlist.append(root)
                root.setText(0, algorithmObject.fileName)
                #root.setText(1, algorithmObject.fileName)
                root.setText(1, 'Local File')
                root.setText(2, file)
                root.setText(3, 'HDF')
                # brush_red = QBrush(Qt.red)
                root.setBackground(0, QBrush(QColor(237, 243, 254)))
                # brush_blue = QBrush(Qt.blue)
                root.setBackground(1, QBrush(QColor(237, 243, 254)))
                root.setBackground(2, QBrush(QColor(237, 243, 254)))
                tmp = list(self.grpinfo.values())[0]
                if isinstance(tmp, nct.Variable):
                    for k, v in self.grpinfo.items():
                        child1 = QTreeWidgetItem()
                        child1.setText(0, k)
                        #child1.setText(1, k)
                        child1.setText(1, 'Geo2D' if len(v.shape) > 1 else '1D')
                        child1.setText(2, file)
                        child1.setText(3, 'HDF Chlid')
                        root.addChild(child1)




                elif isinstance(tmp, dict):
                    for k, v in self.grpinfo.items():
                        child1 = QTreeWidgetItem()
                        child1.setText(0, k)
                        #child1.setText(1, k)
                        child1.setText(1, '    ***  ')
                        child1.setText(2, file)
                        child1.setText(3, 'HDF Group')
                        root.addChild(child1)
                        for val in v:
                            child3 = QTreeWidgetItem(child1)
                            child3.setText(0, val)
                            #child3.setText(1, val)
                            child3.setText(1, 'Geo2D' if len(v[val].shape) > 1 else '1D')
                            child3.setText(2, file)
                            child3.setText(3, 'HDF Chlid')

            elif modelDataType == ModelDataType.MICAPS4:
                self.headcontext = algorithmObject.meteoDataInfo.print_property_info()
                self.tabWidget.tab1UI(self.headcontext)
                root = QTreeWidgetItem(self)
                self.rootlist.append(root)
                root.setText(0, algorithmObject.fileName)
                #root.setText(1, algorithmObject.fileName)
                root.setText(1, 'Local File')
                root.setText(2, file)
                root.setText(3, 'Micaps4')
                m4 = DisposeM4file(file).disposeM4()
                self.fdict[str(file)] = [m4, self.headcontext]
                # brush_red = QBrush(Qt.red)
                root.setBackground(0, QBrush(QColor(237, 243, 254)))
                # brush_blue = QBrush(Qt.blue)
                root.setBackground(1, QBrush(QColor(237, 243, 254)))
                root.setBackground(2, QBrush(QColor(237, 243, 254)))
                self.tabWidget.tab3UI(m4, model='MICAPS4')


            elif modelDataType == ModelDataType.GRIB:
                grib_property = algorithmObject.meteoDataInfo.print_property_info()
                self.tabWidget.tab1UI(grib_property)
                self.headcontext = grib_property
                #self.fdict[str(file)] = [self.grpinfo, self.headcontext]
                root = QTreeWidgetItem(self)
                self.rootlist.append(root)
                root.setText(0, algorithmObject.fileName)
                # root.setText(1, algorithmObject.fileName)
                root.setText(1, 'Local File')
                root.setText(2, file)
                root.setText(3, 'GRIB')#MessageID






        self.expandAll()  # 全部展开节点






    def IsRoot(self, index):
        '''
        判断当前节点是否是根节点
        :param index:
        :return:
        '''
        return True if index == self.rootIndex() else False

    def OnTreeClicked(self):

        item = self.currentItem()

        if self.currentIndex().parent() == self.rootIndex():
            self.tabWidget.tab1UI(self.fdict[item.text(2)][1])
            self.tabWidget.flagExD = 1
            self.tabWidget.tab3UI()
            modelDataType = jt.judge_model_data_type(item.text(2))
            if modelDataType == ModelDataType.MICAPS4:
                self.tabWidget.tab1UI(str(self.fdict.get(item.text(2), '')[1]))
                self.tabWidget.tab3UI(self.fdict[item.text(2)][0], model='MICAPS4')

        else:

            modelDataType = jt.judge_model_data_type(item.text(2))
            if modelDataType == ModelDataType.NETCDF or modelDataType == ModelDataType.HDF:
                tmp = list(self.fdict[item.text(2)][0].values())[0]
                if isinstance(tmp, nct.Variable):
                    s = self.fdict[item.text(2)][0].get(item.text(0), '')

                    self.tabWidget.tab1UI(str(s))
                    self.tabWidget.tab3UI(item.text(0), self.fdict[item.text(2)][0],model='NetCDF')

                elif isinstance(tmp, dict):
                    for k, v in self.fdict[item.text(2)][0].items():
                        if item.text(0) == k:
                            self.tabWidget.tab1UI(str(k))
                            self.tabWidget.tab3UI()
                        for val in v:
                            if item.text(0) == val:
                                self.tabWidget.tab1UI(str(v[val]))
                                self.tabWidget.tab3UI(item.text(0), self.fdict[item.text(2)][0][k], model='HDF')
            elif modelDataType == ModelDataType.GRIB:
                pass






    def SetTextBrower(self, text_str):
        self.textBrowser.setText(text_str)

    def removeTree(self):
        self.clear()
        self.files = []
        self.grpinfo = None
        self.fdict = dict()
        self.headcontext = ''
        if self.grpvar:
            self.grpvar.close()

        if self.removeFlag == 0:
            self.tabWidget.removeTableconx()



        #for i in range(self.currentItem().childCount()):
            #self.currentItem().removeChild(self.currentItem().child(0))
    def OneremoveTree(self):
        if self.currentIndex().parent() == self.rootIndex():
            if self.currentItem():
                self.currentItem().setHidden(True)
                if self.currentItem().text(3) != '':
                    if self.fdict.get(self.currentItem().text(3),''):
                        del self.fdict[self.currentItem().text(3)]
                if self.removeFlag == 0:
                    self.tabWidget.removeTableconx()
        # if self.currentItem():
        #     if self.currentIndex().parent() == self.rootIndex():
        #         ctxt = self.currentItem().text(0)
        #         for txt in self.rootlist:
        #             if txt == ctxt:
        #                 print(txt.text(0))
        #         for i in range(self.currentItem().childCount()):
        #             self.currentItem().removeChild(self.currentItem().child(0))
        #         self.rootlist[0].setText(0, '')
        #         self.rootlist[0].setText(1, '')
        #         self.rootlist[0].setText(2, '')


    def doubleTreeClicked(self):
        if self.currentItem():
            if self.currentIndex().parent() == self.rootIndex():
                ctxt = self.currentItem().text(0)
                for txt in self.rootlist:
                    if txt == ctxt:
                        print(txt.text(0))
                for i in range(self.currentItem().childCount()):
                    self.currentItem().removeChild(self.currentItem().child(0))
                self.rootlist[0].setText(0, '')
                self.rootlist[0].setText(1, '')
                self.rootlist[0].setText(2, '')

    def recvInfo(self,tabWidget, AlgorithmFactory):

        self.tabWidget = tabWidget
        self.AlgorithmFactory = AlgorithmFactory
        self.removeFlag = 0

    def generateMenu(self, pos):
        if self.currentItem():

            item = self.currentItem()

            if self.currentIndex().parent() == self.rootIndex():

                if item.text(0) != '':
                    menu = QMenu()
                    opt1 = menu.addAction("导出数据")
                    opt2 = menu.addAction("移除数据")
                    opt1.setEnabled(False)
                    action = menu.exec_(self.mapToGlobal(pos))
                    if action == opt1:
                        #print("导出数据")
                        self.tabWidget.exportData()
                        # do something
                        return
                    elif action == opt2:
                        # do something
                        self.OneremoveTree()
                        #print("移除数据")
                        return
                    else:
                        return
            else:
                if item.text(0) != '':
                    menu = QMenu()
                    opt1 = menu.addAction("导出数据")
                    opt2 = menu.addAction("移除数据")
                    opt2.setEnabled(False)
                    opt1.setEnabled(False)
                    if item.text(2) == 'Geo2D':
                        opt1.setEnabled(True)
                    action = menu.exec_(self.mapToGlobal(pos))
                    if action == opt1:
                        #print("导出数据")
                        self.tabWidget.exportData()
                        # do something
                        return
                    elif action == opt2:
                        # do something
                        #print("移除数据")
                        self.OneremoveTree()
                        return
                    else:
                        return





    def SetStatusBar(self):
        '''
        底部状态栏信心展示
        :param text_str:属兔信息
        :param msecs:显示持续时间
        :return:
        '''
        #self.statusBar.showMessage(text_str,msecs)
        self.statusBar.showMessage('准备中...')
        self.progressBar = QProgressBar()
        self.label = QLabel()
        self.label2 = QLabel()
        self.label.setText("正在计算： ")
        self.label2.setText("正在计算： ")

        self.statusBar.addPermanentWidget(self.label)
        self.statusBar.addPermanentWidget(self.label2)
        self.statusBar.addPermanentWidget(self.progressBar)
        # self.statusBar().addWidget(self.progressBar)

        # This is simply to show the bar
        self.progressBar.setGeometry(0, 0, 100, 5)
        self.progressBar.setRange(0, 500)  # 设置进度条的范围
        self.progressBar.setValue(499)



