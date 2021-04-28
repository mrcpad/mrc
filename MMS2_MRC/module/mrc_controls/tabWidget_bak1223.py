from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from module.mrc_controls.controlbase import BaseControl
from PyQt5 import QtCore, QtGui, QtWidgets
from module.mrc_controls.textbrowser import MrcTextBrowser
from PyQt5.QtWidgets import QLabel
from netCDF4 import Dataset,num2date
import os
import pandas as pd
import numpy as np
import time
import datetime
from qtpandas.views.DataTableView import DataTableWidget
from qtpandas.models.DataFrameModel import DataFrameModel

class MrcTabWidget(QTabWidget, BaseControl):


    def __init__(self, parent=None):
        super(QTabWidget, self).__init__(parent)
        #QTabWidget.__init__(self)
        #self.tabWidget = QTabWidget(parent)


        # 创建3个选项卡小控件窗口
        self.tab1 = QWidget()
        self.tab1.setObjectName('showInfo')
        #self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab3.setObjectName('dataInfo')
        # 将三个选项卡添加到顶层窗口中
        self.addTab(self.tab1, "Tab 1")
        #self.addTab(self.tab2, "Tab 2")
        self.addTab(self.tab3, "Tab 3")

        self.layout = QVBoxLayout()

        self.textBrowser = MrcTextBrowser()
        self.textBrowser.setObjectName("textBrowser")
        self.TableWidget = QTableWidget()
        self.TableWidget.setObjectName("TableWidget")




        self.initSetGribLayout()

        self.tab1UI()
        #self.tab2UI()
        self.tab3UI()



        self.setStyleSheet(
            '''QWidget#showInfo{
                background:#F0F0F0;
            border-top:1px solid white;
            border-bottom:1px solid white;
            border-left:1px solid white;
            border-top-left-radius:10px;
            border-bottom-left-radius:10px;
                }

                QWidget#dataInfo{
                background:#F0F0F0;
            border-top:1px solid white;
            border-bottom:1px solid white;
            border-left:1px solid white;
            border-top-left-radius:10px;
            border-bottom-left-radius:10px;
                }
                
            QWidget#textBrowser{
                background:#F0F0F0;
            border-top:1px solid white;
            border-bottom:1px solid white;
            border-left:1px solid white;
            border-top-left-radius:10px;
            border-bottom-left-radius:10px;
                }
            #QComboBox{border:none;color:white;}
            QPushButton {
                background-color: palegoldenrod;
                border-width: 2px;
                border-color: darkkhaki;
                border-style: solid;
                border-radius: 5;
                padding: 3px;
                min-width: 9ex;
                min-height: 2.5ex;
            }
            
            QPushButton:hover {
                background-color: khaki;
                border-color: #444444;
            }
            
            QPushButton:pressed {
                padding-left: 5px;
                padding-top: 5px;
                background-color: #d0d67c;
            }
            
            QPushButton:disabled {
                color: #333333;
            }
               
               
            QLabel {
            border: none;
            padding: 0;
            background: none;
            }
               
            QComboBox {
            background-color: 	#FFFFF0;
            border: 1px solid #555;
            color: black;
        }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                border-left: 1px solid #333333;
            }'''
        )




    def initSetGribLayout(self):
        self.table__layout=QtWidgets.QGridLayout()#表布局
        #self.datainfo_layout.setSpacing(5)
        #self.datainfo_layout.setHorizontalSpacing(50)

        self.datainfo_tool_layout = QtWidgets.QGridLayout()#表工具布局


        self.datainfo_layout = QtWidgets.QVBoxLayout()#数据表信息整体布局


        self.tab3.setLayout(self.datainfo_layout)
        self.forecast_time_label=QLabel('预报时长：')
        self.level_label = QLabel('层次：')
        self.analysis_label = QLabel('数据分析：')
        self.format_label  = QLabel('数据格式化：')
        self.comboBox = QComboBox()
        self.comboBox_2 = QComboBox()
        self.comboBox_3 = QComboBox()
        self.comboBox_3.addItems(['平均值', '最大值', '无效值', '偏差'])
        self.comboBox_4 = QComboBox()
        self.comboBox_4.addItems(['%f','%.0f','%.1f','%.2f','%.3f','%.4f'])
        self.comboBox_4.setCurrentText('%.2f')
        self.pushButton=QPushButton('导出数据')



        self.datainfo_tool_layout.addWidget(self.forecast_time_label,0,0,0,1)
        self.datainfo_tool_layout.addWidget(self.comboBox, 0, 1, 0, 1)
        self.datainfo_tool_layout.addWidget(self.level_label, 0, 2, 0, 1)
        self.datainfo_tool_layout.addWidget(self.comboBox_2, 0, 3, 0, 1)
        self.datainfo_tool_layout.addWidget(self.analysis_label, 0, 4, 0, 1)
        self.datainfo_tool_layout.addWidget(self.comboBox_3, 0,5, 0, 1)
        self.datainfo_tool_layout.addWidget(self.format_label, 0, 6, 0, 1)
        self.datainfo_tool_layout.addWidget(self.comboBox_4, 0, 7, 0, 1)
        self.datainfo_tool_layout.addWidget(self.pushButton, 0,8, 0, 1)

        self.datainfo_tool_layout.setColumnStretch(1, 10)
        self.datainfo_tool_layout.setColumnStretch(3, 10)
        self.datainfo_tool_layout.setColumnStretch(5, 10)
        self.datainfo_tool_layout.setColumnStretch(7, 10)
        #self.table__layout.addWidget(self.TableWidget, 0, 0, 9, 9)

        #############################################################
        self.dfmodel = DataFrameModel()
        self.pandastablewidget = DataTableWidget()
        self.pandastablewidget.setViewModel(self.dfmodel)
        self.table__layout.addWidget(self.pandastablewidget, 0, 0, 9, 9)
        ##########################################################


        self.datainfo_layout.addLayout(self.datainfo_tool_layout)
        self.datainfo_layout.addLayout(self.table__layout)

        self.pushButton.clicked.connect(self.exportData)
        self.comboBox.activated[str].connect(self.chargeTime)
        self.comboBox_2.activated[str].connect(self.chargeLevel)
        #self.checkBox.stateChanged.connect(self.chargelat)
        #self.checkBox_2.stateChanged.connect(self.chargelon)
        self.comboBox_3.activated[str].connect(self.chargeMean)
        self.comboBox_4.activated[str].connect(self.chargeformat)

        self.flagExD = 1


    def tab1UI(self,context=''):

        self.textBrowser.setText(context)
        #self.textBrowser.setFont(QFont('Times', 9, ))

        self.layout.addWidget(self.textBrowser)
        self.setTabText(0, '文件说明')
        self.tab1.setLayout(self.layout)


    def tab2UI(self, *args, **kwargs):


        self.setTabText(1, '数据绘图')


    def tab3UI(self, *args, **kwargs):
        self.args = args
        self.flagModel = kwargs.get('model', '')
        if self.flagModel == 'MICAPS4':
            if self.args:
                self.Micaps()

        elif self.flagModel == 'HDF':
            if self.args:
                self.HDF()
        elif self.flagModel == 'NetCDF':
            if self.args:
                self.NetCDF()
        elif self.flagModel == 'GRIB':


            pass


    # 设置小标题与布局方式
        self.setTabText(1, '数据内容')
        #self.tab3.setLayout(layout)
        #self.tab3.setLayout(self.vlayout)



    def Micaps(self):

        self.TableWidget.clear()
        self.comboBox.clear()
        self.comboBox_2.clear()
        self.comboBox_3.clear()
        self.TableWidget.setRowCount(0)
        self.TableWidget.setColumnCount(0)

        self.time = []
        self.level = []
        self.latitude = []
        self.longitude = []

        self.m4 = self.args[0]






        londistance = self.m4.LonGridLength
        latdistance = self.m4.LatGridLength
        startlon = self.m4.StartLon
        endlon = self.m4.EndLon
        startlat = self.m4.StartLat
        endlat = self.m4.EndLat
        LonGridNumber = self.m4.LonGridNumber
        LatGridNumber = self.m4.LatGridNumber

        longitudes = np.arange(startlon, endlon + londistance, londistance)

        self.longitudes = longitudes[0:LonGridNumber]
        latitudes = np.arange(startlat, endlat + latdistance, latdistance)
        self.latitudes = latitudes[0:LatGridNumber]
        self.m4data = self.m4.m4data

        self.tdate = datetime.datetime.strptime(self.m4.year + self.m4.month + self.m4.day + self.m4.ftime, '%y%m%d%H')
        self.tdate = self.tdate.strftime('%Y-%m-%d %H:%M:%S')

        txt = (max([self.tdate], key=len))
        metrics = QFontMetrics(self.comboBox.font())
        w = metrics.width(txt)
        self.comboBox.setMinimumWidth(w + 40)
        self.comboBox.maxVisibleItems()


        self.tlevel = self.m4.level


        if self.comboBox.count() > 0:
            self.comboBox.clear()
            self.comboBox.addItem(self.tdate)
            if self.comboBox.count() <= 1:
                self.comboBox.setDisabled(True)
        elif self.comboBox.count() <= 1:
            self.comboBox.addItem(self.tdate)
            self.comboBox.setDisabled(True)



        self.comboBox_3.addItems(['平均值', '最大值', '最小值', '中位数', '方差', '标准差'])
        self.comboBox_3.setCurrentText('平均值')

        if self.comboBox_3.count() > 0:
            self.comboBox_3.clear()
            self.comboBox_3.addItems(['平均值', '最大值', '最小值', '中位数', '方差', '标准差'])
            self.comboBox_3.setCurrentText('平均值')

        self.comboBox_2.addItem(self.tlevel)
        if self.comboBox_2.count() > 0:
            self.comboBox_2.clear()
            self.comboBox_2.addItem(self.tlevel)
            if self.comboBox_2.count() == 1:
                self.comboBox_2.setDisabled(True)

        self.longitude = [format(s, '.2f') for s in self.longitudes]
        self.latitude = [format(s, '.2f') for s in self.latitudes]


        # 展示第一个数据


        df = pd.DataFrame(self.m4data,index=self.latitude,columns=self.longitude)



        df['平均值'] = df.mean(axis=1).round(decimals=2)
        self.dfmodel.setDataFrame(df)



    def NetCDF(self):

        self.comboBox.clear()
        self.comboBox_2.clear()
        self.comboBox_3.clear()


        if len(self.args) > 1:
            self.time = []
            self.level = []
            self.latitude = []
            self.longitude = []
            self.currentVal = []
            self.v = self.args[1].get(self.args[0])
            self.varName = self.args[0]
            if len(self.v.shape) == 1:

                if self.args[0] == 'time' and self.v.dtype != np.str:
                    for j, val in enumerate(self.v[:]):
                        nd = num2date(self.v[::].data, self.v.units)
                        self.TableWidget.setItem(0, j, QTableWidgetItem(str(nd[j])))
                else:
                    for j, val in enumerate(self.v[:]):
                        self.TableWidget.setItem(0, j, QTableWidgetItem(str(val)))



            elif len(self.v.shape) == 2:

                self.latitude = self.args[1].get(self.v.dimensions[0], np.array([np.nan]))[:].astype(np.str)
                self.longitude = self.args[1].get(self.v.dimensions[1], np.array([np.nan]))[:].astype(np.str)
                if len(self.latitude) == 1 and len(self.longitude) == 1:
                    self.latitude = [str(i + 1) for i in range(self.v.shape[0])]
                    self.longitude = [str(i + 1) for i in range(self.v.shape[1])]

                self.comboBox_3.addItems(['平均值', '最大值', '最小值', '中位数', '方差', '标准差'])
                self.comboBox_3.setCurrentText('平均值')

                if self.comboBox_3.count() > 0:
                    self.comboBox_3.clear()
                    self.comboBox_3.addItems(['平均值', '最大值', '最小值', '中位数', '方差', '标准差'])
                    self.comboBox_3.setCurrentText('平均值')


                self.val = self.v[:].data if isinstance(self.v[:], np.ma.core.MaskedArray) else self.v[:]
                self.currentVal = self.val

                df = pd.DataFrame(self.val, columns=self.longitude)
                # if self.v.shape[0] > 1000 and self.v.shape[1] > 1000:
                #     df = df.iloc[0:1000, 0:1000]

                df['平均值'] = df.mean(axis=1)
                self.dfmodel.setDataFrame(df)





            elif len(self.v.shape) == 3:

                print(self.v.dimensions)
                self.comboBox.setDisabled(False)
                self.comboBox_2.setDisabled(False)

                if 'time' in self.v.dimensions:
                    self.time = self.args[1].get('time')
                    self.comboBox.setMinimumWidth(150)
                    # print(self.v.dimensions.index('time'))
                    if self.time:
                        if self.time.dtype != np.str:
                            td = num2date(self.time[::].data, self.time.units)
                            self.timedict = dict(zip([str(tds) for tds in td.tolist()], range(len(td.tolist()))))

                            self.comboBox.addItems([str(d) for d in self.timedict.keys()])
                            if self.comboBox.count() > 0:
                                self.comboBox.clear()
                                self.comboBox.addItems([str(d) for d in self.timedict.keys()])
                                if self.comboBox.count() <= 1:
                                    self.comboBox.setDisabled(True)
                        else:
                            self.timedict = dict(
                                zip([str(td) for td in self.time[:].tolist()], range(len(self.time[:].tolist()))))
                            self.comboBox.addItems([str(d) for d in self.timedict.keys()])
                            if self.comboBox.count() > 0:
                                self.comboBox.clear()
                                self.comboBox.addItems([str(d) for d in self.timedict.keys()])
                                if self.comboBox.count() <= 1:
                                    self.comboBox.setDisabled(True)
                    else:
                        self.time = []
                if 'level' in self.v.dimensions:
                    self.level = self.args[1].get('level')
                    if self.level:
                        self.leveldict = dict(
                            zip([str(lv) for lv in self.level[:].tolist()], range(len(self.level[:].tolist()))))
                        self.comboBox_2.addItems([str(d) for d in self.leveldict.keys()])
                        if self.comboBox_2.count() > 0:
                            self.comboBox_2.clear()
                            self.comboBox_2.addItems([str(d) for d in self.leveldict.keys()])
                            if self.comboBox_2.count() <= 1:
                                self.comboBox_2.setDisabled(True)
                else:
                    self.level = []
                if 'latitude' in self.v.dimensions or 'lat' in self.v.dimensions or 'lats' in self.v.dimensions:
                    for lat in ['latitude', 'lat', 'lats']:
                        for dim in self.v.dimensions:
                            if lat == dim:
                                self.latitude = self.args[1].get(lat, np.array([np.nan]))[:].astype(np.str)
                    # self.latitude = args[1].get('latitude', '')[:].astype(np.str)
                if 'longitude' in self.v.dimensions or 'lon' in self.v.dimensions or 'lons' in self.v.dimensions:
                    for lon in ['longitude', 'lon', 'lons']:
                        for dim in self.v.dimensions:
                            if lon == dim:
                                self.longitude = self.args[1].get(lon, np.array([np.nan]))[:].astype(np.str)

                if len(self.latitude) == 1 or len(self.longitude) == 1:
                    self.latitude = self.args[1].get(self.v.dimensions[1], np.array([np.nan]))[:].astype(np.str)
                    self.longitude = self.args[1].get(self.v.dimensions[2], np.array([np.nan]))[:].astype(np.str)

                if len(self.latitude) == 0 or len(self.longitude) == 0:
                    self.latitude = [str(i + 1) for i in range(self.v.shape[1])]
                    self.longitude = [str(i + 1) for i in range(self.v.shape[2])]

                if len(self.time) == 0 and len(self.level) == 0:
                    self.firstcomX = self.args[1].get(self.v.dimensions[0], np.array([np.nan]))[:].astype(np.str)

                    if len(self.firstcomX) == 1 and self.firstcomX == 'nan':
                        self.firstcomX = np.array(
                            [str(i + 1) + ' of ' + str(self.v.shape[0]) for i in range(self.v.shape[0])])
                    self.firstcomXdict = dict(
                        zip([str(lv) for lv in self.firstcomX[:].tolist()], range(len(self.firstcomX[:].tolist()))))
                    self.comboBox.addItems([str(d) for d in self.firstcomXdict.keys()])
                    if self.comboBox.count() > 0:
                        self.comboBox.clear()
                        self.comboBox.addItems([str(d) for d in self.firstcomXdict.keys()])
                        if self.comboBox.count() <= 1:
                            self.comboBox.setDisabled(True)
                self.comboBox_3.addItems(['平均值', '最大值', '最小值', '中位数', '方差', '标准差'])
                self.comboBox_3.setCurrentText('平均值')

                if self.comboBox_3.count() > 0:
                    self.comboBox_3.clear()
                    self.comboBox_3.addItems(['平均值', '最大值', '最小值', '中位数', '方差', '标准差'])
                    self.comboBox_3.setCurrentText('平均值')



                if isinstance(self.latitude, np.ndarray):
                    self.latitude = list(map(lambda x: ('%.3f') % float(x), self.latitude.astype(np.float64)))

                # 展示第一个数据
                #self.val = self.v[:].data if isinstance(self.v[:], np.ma.core.MaskedArray) else self.v[:]
                # self.val = self.v[::]
                # self.val = self.val[::][0]
                # self.currentVal = self.val
                if isinstance(self.latitude, np.ndarray):
                    self.longitude = list(map(lambda x: ('%.3f') % float(x), self.longitude.astype(np.float64)))

                df = pd.DataFrame(self.v[::][0], columns=self.longitude)
                df['平均值'] = df.mean(axis=1).round(decimals=3)
                self.dfmodel.setDataFrame(df)

                # if self.v.shape[1] > 1000 and self.v.shape[2] > 1000:
                #     df = df.iloc[0:1000, 0:1000]
                #
                # df['平均值'] = df.mean(axis=1).round(decimals=3)
                # # print(df.columns.values.tolist())
                # self.columns = [str(c) for c in df.columns.values.tolist()]
                #
                # self.TableWidget.setHorizontalHeaderLabels(self.columns)
                # self.TableWidget.setVerticalHeaderLabels(self.latitude)
                #
                #
                # for i, v0 in enumerate(df.values.tolist()):
                #     for j, v1 in enumerate(v0):
                #         self.TableWidget.setItem(i, j, QTableWidgetItem(str(v1)))








            elif len(self.v.shape) == 4:
                self.comboBox.setDisabled(False)
                self.comboBox_2.setDisabled(False)
                print(self.v.dimensions)
                if 'time' in self.v.dimensions:
                    self.time = self.args[1].get('time')
                    if self.time:
                        self.comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

                        if self.time.dtype != np.str:
                            td = num2date(self.time[::].data, self.time.units)
                            self.timedict = dict(zip([str(tds) for tds in td.tolist()], range(len(td.tolist()))))


                            self.comboBox.addItems([str(d) for d in self.timedict.keys()])
                            self.comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

                            if self.comboBox.count() > 0:
                                self.comboBox.clear()
                                self.comboBox.addItems([str(d) for d in self.timedict.keys()])
                                self.comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
                                if self.comboBox.count() <= 1:
                                    self.comboBox.setDisabled(True)
                        else:
                            self.timedict = dict(
                                zip([str(td) for td in self.time[:].tolist()], range(len(self.time[:].tolist()))))
                            self.comboBox.addItems([str(d) for d in self.timedict.keys()])
                            if self.comboBox.count() > 0:
                                self.comboBox.clear()
                                self.comboBox.addItems([str(d) for d in self.timedict.keys()])
                                if self.comboBox.count() <= 1:
                                    self.comboBox.setDisabled(True)
                    else:
                        self.time = []

                if 'level' in self.v.dimensions:
                    self.level = self.args[1].get('level')
                    if self.level:
                        self.leveldict = dict(
                            zip([str(lv) for lv in self.level[:].tolist()], range(len(self.level[:].tolist()))))
                        self.comboBox_2.addItems([str(d) for d in self.leveldict.keys()])
                        if self.comboBox_2.count() > 0:
                            self.comboBox_2.clear()
                            self.comboBox_2.addItems([str(d) for d in self.leveldict.keys()])
                            if self.comboBox_2.count() <= 1:
                                self.comboBox_2.setDisabled(True)
                    else:
                        self.level = []

                if 'latitude' in self.v.dimensions or 'lat' in self.v.dimensions or 'lats' in self.v.dimensions:
                    for lat in ['latitude', 'lat', 'lats']:
                        for dim in self.v.dimensions:
                            if lat == dim:
                                self.latitude = self.args[1].get(lat, np.array([np.nan]))[:].astype(np.str)

                if 'longitude' in self.v.dimensions or 'lon' in self.v.dimensions or 'lons' in self.v.dimensions:
                    for lon in ['longitude', 'lon', 'lons']:
                        for dim in self.v.dimensions:
                            if lon == dim:
                                self.longitude = self.args[1].get(lon, np.array([np.nan]))[:].astype(np.str)

                if len(self.latitude) == 1 or len(self.longitude) == 1:
                    self.latitude = self.args[1].get(self.v.dimensions[2], np.array([np.nan]))[:].astype(np.str)
                    self.longitude = self.args[1].get(self.v.dimensions[3], np.array([np.nan]))[:].astype(np.str)

                if len(self.latitude) == 0 or len(self.longitude) == 0:
                    self.latitude = [str(i + 1) for i in range(self.v.shape[2])]
                    self.longitude = [str(i + 1) for i in range(self.v.shape[3])]

                if len(self.time) == 0:
                    self.label.setText(str(self.v.dimensions[0]))
                    self.firstcomX = self.args[1].get(self.v.dimensions[0], np.array([np.nan]))[:].astype(np.str)
                    if self.firstcomX == 'nan':
                        self.firstcomX = np.array(
                            [str(i + 1) + ' of ' + str(self.v.shape[0]) for i in range(self.v.shape[0])])
                    self.firstcomXdict = dict(
                        zip([str(lv) for lv in self.firstcomX[:].tolist()], range(len(self.firstcomX[:].tolist()))))
                    self.comboBox.addItems([str(d) for d in self.firstcomXdict.keys()])
                    if self.comboBox.count() > 0:
                        self.comboBox.clear()
                        self.comboBox.addItems([str(d) for d in self.firstcomXdict.keys()])
                        if self.comboBox.count() == 1:
                            self.comboBox.setDisabled(True)
                if len(self.level) == 0:
                    if len(self.time) > 0:
                        findex = self.v.dimensions.index('time')
                        secindex = [i for i in [0, 1] if i != findex][0]
                    else:
                        secindex = 1
                    self.label_2.setText(str(self.v.dimensions[secindex]))
                    self.seccomX = self.args[1].get(self.v.dimensions[secindex], np.array([np.nan]))[:].astype(np.str)
                    self.seccomX = self.seccomX.data if isinstance(self.seccomX,
                                                                   np.ma.core.MaskedArray) else self.seccomX
                    self.seccomXdict = dict(
                        zip([str(lv) for lv in self.seccomX[:].tolist()], range(len(self.seccomX[:].tolist()))))
                    self.comboBox_2.addItems([str(d) for d in self.seccomXdict.keys()])
                    if self.comboBox_2.count() > 0:
                        self.comboBox_2.clear()
                        self.comboBox_2.addItems([str(d) for d in self.seccomXdict.keys()])
                        if self.comboBox_2.count() == 1:
                            self.comboBox_2.setDisabled(True)

                if len(self.time) == 0 and len(self.level) == 0:

                    self.label.setText(str(self.v.dimensions[0]))
                    self.firstcomX = self.args[1].get(self.v.dimensions[0], np.array([np.nan]))[:].astype(np.str)
                    self.firstcomXdict = dict(
                        zip([str(lv) for lv in self.firstcomX[:].tolist()], range(len(self.firstcomX[:].tolist()))))
                    self.comboBox.addItems([str(d) for d in self.firstcomXdict.keys()])
                    if self.comboBox.count() > 0:
                        self.comboBox.clear()
                        self.comboBox.addItems([str(d) for d in self.firstcomXdict.keys()])
                        if self.comboBox.count() == 1:
                            self.comboBox.setDisabled(True)

                    self.label_2.setText(str(self.v.dimensions[1]))
                    self.seccomX = self.args[1].get(self.v.dimensions[1], np.array([np.nan]))[:].astype(np.str)
                    self.seccomX = self.seccomX.data if isinstance(self.seccomX,
                                                                   np.ma.core.MaskedArray) else self.seccomX
                    self.seccomXdict = dict(
                        zip([str(lv) for lv in self.seccomX[:].tolist()], range(len(self.seccomX[:].tolist()))))
                    self.comboBox_2.addItems([str(d) for d in self.seccomXdict.keys()])
                    if self.comboBox_2.count() > 0:
                        self.comboBox_2.clear()
                        self.comboBox_2.addItems([str(d) for d in self.seccomXdict.keys()])
                        if self.comboBox_2.count() == 1:
                            self.comboBox_2.setDisabled(True)

                self.comboBox_3.addItems(['平均值', '最大值', '最小值', '中位数', '方差', '标准差'])
                self.comboBox_3.setCurrentText('平均值')
                # print(self.comboBox_3.count())
                if self.comboBox_3.count() > 0:
                    self.comboBox_3.clear()
                    self.comboBox_3.addItems(['平均值', '最大值', '最小值', '中位数', '方差', '标准差'])
                    self.comboBox_3.setCurrentText('平均值')


                self.latitude = list(map(lambda x: ('%.3f') % float(x), self.latitude.astype(np.float64)))

                # 展示第一个数据
                if len(self.v.shape) == 4:
                    self.val = self.v[:].data if isinstance(self.v[:], np.ma.core.MaskedArray) else self.v[:]
                    self.val = self.v[:][0][0]
                    self.currentVal = self.val

                    self.longitude = list(map(lambda x: ('%.3f') % float(x), self.longitude.astype(np.float64)))

                    df = pd.DataFrame(self.val, columns=self.longitude)
                    df['平均值'] = df.mean(axis=1).round(decimals=3)
                    self.dfmodel.setDataFrame(df)




                self.flagExD = 0



        elif len(self.args) == 0:
            pass

    def HDF(self):


        self.comboBox.clear()
        self.comboBox_2.clear()
        self.comboBox_3.clear()


        if len(self.args) > 1:
            self.time = []
            self.level = []
            self.latitude = []
            self.longitude = []
            self.currentVal = []
            self.v = self.args[1].get(self.args[0])
            self.varName = self.args[0]
            # print(self.v.dtype == np.float64)
            if len(self.v.shape) == 1:
                self.TableWidget.setRowCount(1)
                self.TableWidget.setColumnCount(len(self.v[:]))
                if self.args[0] == 'time' and self.v.dtype != np.str:
                    for j, val in enumerate(self.v[:]):
                        nd = num2date(self.v[::].data, self.v.units)
                        self.TableWidget.setItem(0, j, QTableWidgetItem(str(nd[j])))
                else:
                    for j, val in enumerate(self.v[:]):
                        self.TableWidget.setItem(0, j, QTableWidgetItem(str(val)))



            elif len(self.v.shape) == 2:

                self.latitude = self.args[1].get(self.v.dimensions[0], np.array([np.nan]))[:].astype(np.str)
                self.longitude = self.args[1].get(self.v.dimensions[1], np.array([np.nan]))[:].astype(np.str)
                if len(self.latitude) == 1 and len(self.longitude) == 1:
                    self.latitude = [str(i + 1) for i in range(self.v.shape[0])]
                    self.longitude = [str(i + 1) for i in range(self.v.shape[1])]

                self.comboBox_3.addItems(['平均值', '最大值', '最小值', '中位数', '方差', '标准差'])
                self.comboBox_3.setCurrentText('平均值')
                self.TableWidget.clear()
                self.TableWidget.setRowCount(0)
                self.TableWidget.setColumnCount(0)
                if self.comboBox_3.count() > 0:
                    self.comboBox_3.clear()
                    self.comboBox_3.addItems(['平均值', '最大值', '最小值', '中位数', '方差', '标准差'])
                    self.comboBox_3.setCurrentText('平均值')

                if len(self.latitude) > 1 and len(self.longitude) > 1:

                    self.TableWidget.setRowCount(len(self.latitude) + 1)
                    self.TableWidget.setColumnCount(len(self.longitude) + 1)
                    # self.model = QStandardItemModel(len(self.latitude) + 1, len(self.longitude) + 1)
                else:
                    self.TableWidget.setRowCount(self.v.shape[0])
                    self.TableWidget.setColumnCount(self.v.shape[1] + 1)

                # self.TableWidget.setVerticalHeaderLabels(self.latitude)

                # 展示第一个数据
                self.val = self.v[:].data if isinstance(self.v[:], np.ma.core.MaskedArray) else self.v[:]
                self.currentVal = self.val

                df = pd.DataFrame(self.val, columns=self.longitude)
                if self.v.shape[0] > 1000 and self.v.shape[1] > 1000:
                    df = df.iloc[0:1000, 0:1000]
                    # self.TableWidget.setRowCount(1000)
                    # self.TableWidget.setColumnCount(1000 + 1)
                # df['平均值'] = df.mean(axis=1).round(decimals=3)
                df['平均值'] = df.mean(axis=1)
                # print(df.columns.values.tolist())
                self.columns = [str(c) for c in df.columns.values.tolist()]
                self.TableWidget.setHorizontalHeaderLabels(self.columns)
                self.TableWidget.setVerticalHeaderLabels(self.latitude)


                for i, v0 in enumerate(df.values):
                    for j, v1 in enumerate(v0):
                        self.TableWidget.setItem(i, j, QTableWidgetItem(str(v1)))



                self.TableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.flagExD = 0


            elif len(self.v.shape) == 3:

                print(self.v.dimensions)
                self.comboBox.setDisabled(False)
                self.comboBox_2.setDisabled(False)

                if 'time' in self.v.dimensions:
                    self.time = self.args[1].get('time')
                    self.comboBox.setMinimumWidth(150)
                    # print(self.v.dimensions.index('time'))
                    if self.time:
                        if self.time.dtype != np.str:
                            td = num2date(self.time[::].data, self.time.units)
                            # print(td.tolist())
                            self.timedict = dict(zip([str(tds) for tds in td.tolist()], range(len(td.tolist()))))
                            txt = (max([str(d) for d in self.timedict.keys()], key=len))
                            metrics = QFontMetrics(self.comboBox.font())
                            w = metrics.width(txt)
                            self.comboBox.setMinimumWidth(w + 40)
                            self.comboBox.maxVisibleItems()
                            self.comboBox.addItems([str(d) for d in self.timedict.keys()])
                            if self.comboBox.count() > 0:
                                self.comboBox.clear()
                                self.comboBox.addItems([str(d) for d in self.timedict.keys()])
                                if self.comboBox.count() <= 1:
                                    self.comboBox.setDisabled(True)
                        else:
                            self.timedict = dict(
                                zip([str(td) for td in self.time[:].tolist()], range(len(self.time[:].tolist()))))
                            self.comboBox.addItems([str(d) for d in self.timedict.keys()])
                            if self.comboBox.count() > 0:
                                self.comboBox.clear()
                                self.comboBox.addItems([str(d) for d in self.timedict.keys()])
                                if self.comboBox.count() <= 1:
                                    self.comboBox.setDisabled(True)
                    else:
                        self.time = []
                if 'level' in self.v.dimensions:
                    self.level = self.args[1].get('level')
                    if self.level:
                        self.leveldict = dict(
                            zip([str(lv) for lv in self.level[:].tolist()], range(len(self.level[:].tolist()))))
                        self.comboBox_2.addItems([str(d) for d in self.leveldict.keys()])
                        if self.comboBox_2.count() > 0:
                            self.comboBox_2.clear()
                            self.comboBox_2.addItems([str(d) for d in self.leveldict.keys()])
                            if self.comboBox_2.count() <= 1:
                                self.comboBox_2.setDisabled(True)
                else:
                    self.level = []
                if 'latitude' in self.v.dimensions or 'lat' in self.v.dimensions or 'lats' in self.v.dimensions:
                    for lat in ['latitude', 'lat', 'lats']:
                        for dim in self.v.dimensions:
                            if lat == dim:
                                self.latitude = self.args[1].get(lat, np.array([np.nan]))[:].astype(np.str)
                    # self.latitude = args[1].get('latitude', '')[:].astype(np.str)
                if 'longitude' in self.v.dimensions or 'lon' in self.v.dimensions or 'lons' in self.v.dimensions:
                    for lon in ['longitude', 'lon', 'lons']:
                        for dim in self.v.dimensions:
                            if lon == dim:
                                self.longitude = self.args[1].get(lon, np.array([np.nan]))[:].astype(np.str)

                if len(self.latitude) == 1 or len(self.longitude) == 1:
                    self.latitude = self.args[1].get(self.v.dimensions[1], np.array([np.nan]))[:].astype(np.str)
                    self.longitude = self.args[1].get(self.v.dimensions[2], np.array([np.nan]))[:].astype(np.str)

                if len(self.latitude) == 0 or len(self.longitude) == 0:
                    self.latitude = [str(i + 1) for i in range(self.v.shape[1])]
                    self.longitude = [str(i + 1) for i in range(self.v.shape[2])]

                if len(self.time) == 0 and len(self.level) == 0:
                    #self.label.setText(str(self.v.dimensions[0]))
                    self.firstcomX = self.args[1].get(self.v.dimensions[0], np.array([np.nan]))[:].astype(np.str)

                    if len(self.firstcomX) == 1 and self.firstcomX == 'nan':
                        self.firstcomX = np.array(
                            [str(i + 1) + ' of ' + str(self.v.shape[0]) for i in range(self.v.shape[0])])
                    self.firstcomXdict = dict(
                        zip([str(lv) for lv in self.firstcomX[:].tolist()], range(len(self.firstcomX[:].tolist()))))
                    self.comboBox.addItems([str(d) for d in self.firstcomXdict.keys()])
                    if self.comboBox.count() > 0:
                        self.comboBox.clear()
                        self.comboBox.addItems([str(d) for d in self.firstcomXdict.keys()])
                        if self.comboBox.count() <= 1:
                            self.comboBox.setDisabled(True)
                self.comboBox_3.addItems(['平均值', '最大值', '最小值', '中位数', '方差', '标准差'])
                self.comboBox_3.setCurrentText('平均值')
                self.TableWidget.clear()
                self.TableWidget.setRowCount(0)
                self.TableWidget.setColumnCount(0)
                if self.comboBox_3.count() > 0:
                    self.comboBox_3.clear()
                    self.comboBox_3.addItems(['平均值', '最大值', '最小值', '中位数', '方差', '标准差'])
                    self.comboBox_3.setCurrentText('平均值')

                if len(self.latitude) > 1 and len(self.longitude) > 1:

                    self.TableWidget.setRowCount(len(self.latitude) + 1)
                    self.TableWidget.setColumnCount(len(self.longitude) + 1)
                else:
                    self.TableWidget.setRowCount(self.v.shape[1])
                    self.TableWidget.setColumnCount(self.v.shape[2] + 1)

                # self.TableWidget.setVerticalHeaderLabels(self.latitude)
                if isinstance(self.latitude, np.ndarray):
                    self.latitude = list(map(lambda x: ('%.3f') % float(x), self.latitude.astype(np.float64)))

                # 展示第一个数据
                self.val = self.v[:].data if isinstance(self.v[:], np.ma.core.MaskedArray) else self.v[:]
                self.val = self.val[:][0]
                self.currentVal = self.val
                if isinstance(self.latitude, np.ndarray):
                    self.longitude = list(map(lambda x: ('%.3f') % float(x), self.longitude.astype(np.float64)))

                df = pd.DataFrame(self.val, columns=self.longitude)

                if self.v.shape[1] > 1000 and self.v.shape[2] > 1000:
                    df = df.iloc[0:1000, 0:1000]

                df['平均值'] = df.mean(axis=1).round(decimals=3)
                # print(df.columns.values.tolist())
                self.columns = [str(c) for c in df.columns.values.tolist()]

                self.TableWidget.setHorizontalHeaderLabels(self.columns)
                self.TableWidget.setVerticalHeaderLabels(self.latitude)


                for i, v0 in enumerate(df.values.tolist()):
                    for j, v1 in enumerate(v0):
                        self.TableWidget.setItem(i, j, QTableWidgetItem(str(v1)))



                self.TableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.flagExD = 0





            elif len(self.v.shape) == 4:
                self.comboBox.setDisabled(False)
                self.comboBox_2.setDisabled(False)
                print(self.v.dimensions)
                if 'time' in self.v.dimensions:
                    self.time = self.args[1].get('time')
                    if self.time:
                        # self.comboBox.setMinimumWidth(190)
                        self.comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

                        # print(self.v.dimensions.index('time'))
                        if self.time.dtype != np.str:
                            td = num2date(self.time[::].data, self.time.units)
                            # print(td.tolist())
                            self.timedict = dict(zip([str(tds) for tds in td.tolist()], range(len(td.tolist()))))
                            txt = (max([str(d) for d in self.timedict.keys()], key=len))

                            metrics = QFontMetrics(self.comboBox.font())
                            w = metrics.width(txt)
                            self.comboBox.setMinimumWidth(w + 40)
                            self.comboBox.maxVisibleItems()

                            self.comboBox.addItems([str(d) for d in self.timedict.keys()])
                            self.comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

                            if self.comboBox.count() > 0:
                                self.comboBox.clear()
                                self.comboBox.addItems([str(d) for d in self.timedict.keys()])
                                self.comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
                                if self.comboBox.count() <= 1:
                                    self.comboBox.setDisabled(True)
                        else:
                            self.timedict = dict(
                                zip([str(td) for td in self.time[:].tolist()], range(len(self.time[:].tolist()))))
                            self.comboBox.addItems([str(d) for d in self.timedict.keys()])
                            if self.comboBox.count() > 0:
                                self.comboBox.clear()
                                self.comboBox.addItems([str(d) for d in self.timedict.keys()])
                                if self.comboBox.count() <= 1:
                                    self.comboBox.setDisabled(True)
                    else:
                        self.time = []

                if 'level' in self.v.dimensions:
                    self.level = self.args[1].get('level')
                    if self.level:
                        self.leveldict = dict(
                            zip([str(lv) for lv in self.level[:].tolist()], range(len(self.level[:].tolist()))))
                        self.comboBox_2.addItems([str(d) for d in self.leveldict.keys()])
                        if self.comboBox_2.count() > 0:
                            self.comboBox_2.clear()
                            self.comboBox_2.addItems([str(d) for d in self.leveldict.keys()])
                            if self.comboBox_2.count() <= 1:
                                self.comboBox_2.setDisabled(True)
                    else:
                        self.level = []

                if 'latitude' in self.v.dimensions or 'lat' in self.v.dimensions or 'lats' in self.v.dimensions:
                    for lat in ['latitude', 'lat', 'lats']:
                        for dim in self.v.dimensions:
                            if lat == dim:
                                self.latitude = self.args[1].get(lat, np.array([np.nan]))[:].astype(np.str)
                    # self.latitude = args[1].get('latitude', '')[:].astype(np.str)

                if 'longitude' in self.v.dimensions or 'lon' in self.v.dimensions or 'lons' in self.v.dimensions:
                    for lon in ['longitude', 'lon', 'lons']:
                        for dim in self.v.dimensions:
                            if lon == dim:
                                self.longitude = self.args[1].get(lon, np.array([np.nan]))[:].astype(np.str)
                    # self.longitude = args[1].get('longitude', '')[:].astype(np.str)

                if len(self.latitude) == 1 or len(self.longitude) == 1:
                    self.latitude = self.args[1].get(self.v.dimensions[2], np.array([np.nan]))[:].astype(np.str)
                    self.longitude = self.args[1].get(self.v.dimensions[3], np.array([np.nan]))[:].astype(np.str)

                if len(self.latitude) == 0 or len(self.longitude) == 0:
                    self.latitude = [str(i + 1) for i in range(self.v.shape[2])]
                    self.longitude = [str(i + 1) for i in range(self.v.shape[3])]

                if len(self.time) == 0:
                    #self.label.setText(str(self.v.dimensions[0]))
                    self.firstcomX = self.args[1].get(self.v.dimensions[0], np.array([np.nan]))[:].astype(np.str)
                    if self.firstcomX == 'nan':
                        self.firstcomX = np.array(
                            [str(i + 1) + ' of ' + str(self.v.shape[0]) for i in range(self.v.shape[0])])
                    self.firstcomXdict = dict(
                        zip([str(lv) for lv in self.firstcomX[:].tolist()], range(len(self.firstcomX[:].tolist()))))
                    self.comboBox.addItems([str(d) for d in self.firstcomXdict.keys()])
                    if self.comboBox.count() > 0:
                        self.comboBox.clear()
                        self.comboBox.addItems([str(d) for d in self.firstcomXdict.keys()])
                        if self.comboBox.count() == 1:
                            self.comboBox.setDisabled(True)
                if len(self.level) == 0:
                    if len(self.time) > 0:
                        findex = self.v.dimensions.index('time')
                        secindex = [i for i in [0, 1] if i != findex][0]
                    else:
                        secindex = 1
                    self.label_2.setText(str(self.v.dimensions[secindex]))
                    self.seccomX = self.args[1].get(self.v.dimensions[secindex], np.array([np.nan]))[:].astype(np.str)
                    self.seccomX = self.seccomX.data if isinstance(self.seccomX,
                                                                   np.ma.core.MaskedArray) else self.seccomX
                    self.seccomXdict = dict(
                        zip([str(lv) for lv in self.seccomX[:].tolist()], range(len(self.seccomX[:].tolist()))))
                    self.comboBox_2.addItems([str(d) for d in self.seccomXdict.keys()])
                    if self.comboBox_2.count() > 0:
                        self.comboBox_2.clear()
                        self.comboBox_2.addItems([str(d) for d in self.seccomXdict.keys()])
                        if self.comboBox_2.count() == 1:
                            self.comboBox_2.setDisabled(True)

                if len(self.time) == 0 and len(self.level) == 0:

                    #self.label.setText(str(self.v.dimensions[0]))
                    self.firstcomX = self.args[1].get(self.v.dimensions[0], np.array([np.nan]))[:].astype(np.str)
                    self.firstcomXdict = dict(
                        zip([str(lv) for lv in self.firstcomX[:].tolist()], range(len(self.firstcomX[:].tolist()))))
                    self.comboBox.addItems([str(d) for d in self.firstcomXdict.keys()])
                    if self.comboBox.count() > 0:
                        self.comboBox.clear()
                        self.comboBox.addItems([str(d) for d in self.firstcomXdict.keys()])
                        if self.comboBox.count() == 1:
                            self.comboBox.setDisabled(True)

                    #self.label_2.setText(str(self.v.dimensions[1]))
                    self.seccomX = self.args[1].get(self.v.dimensions[1], np.array([np.nan]))[:].astype(np.str)
                    self.seccomX = self.seccomX.data if isinstance(self.seccomX,
                                                                   np.ma.core.MaskedArray) else self.seccomX
                    self.seccomXdict = dict(
                        zip([str(lv) for lv in self.seccomX[:].tolist()], range(len(self.seccomX[:].tolist()))))
                    self.comboBox_2.addItems([str(d) for d in self.seccomXdict.keys()])
                    if self.comboBox_2.count() > 0:
                        self.comboBox_2.clear()
                        self.comboBox_2.addItems([str(d) for d in self.seccomXdict.keys()])
                        if self.comboBox_2.count() == 1:
                            self.comboBox_2.setDisabled(True)

                self.comboBox_3.addItems(['平均值', '最大值', '最小值', '中位数', '方差', '标准差'])
                self.comboBox_3.setCurrentText('平均值')
                # print(self.comboBox_3.count())
                if self.comboBox_3.count() > 0:
                    self.comboBox_3.clear()
                    self.comboBox_3.addItems(['平均值', '最大值', '最小值', '中位数', '方差', '标准差'])
                    self.comboBox_3.setCurrentText('平均值')

                if len(self.latitude) > 1 and len(self.longitude) > 1:

                    self.TableWidget.setRowCount(len(self.latitude))
                    self.TableWidget.setColumnCount(len(self.longitude) + 1)
                else:
                    self.TableWidget.setRowCount(self.v.shape[1])
                    self.TableWidget.setColumnCount(self.v.shape[2] + 1)

                # self.TableWidget.setRowCount(len(self.latitude) + 1)
                # self.TableWidget.setColumnCount(len(self.longitude) + 1)

                # 设置水平方向的表头标签与垂直方向上的表头标签，注意必须在初始化行列之后进行，否则，没有效果

                # self.TableWidget.setHorizontalHeaderLabels(self.longitude)
                # self.TableWidget.setHorizontalHeaderLabels(lon)
                # Todo 优化1 设置垂直方向的表头标签
                # print(self.latitude.map(lambda x:('%.2f')%x))
                self.latitude = list(map(lambda x: ('%.3f') % float(x), self.latitude.astype(np.float64)))

                self.TableWidget.setVerticalHeaderLabels(self.latitude)
                # 展示第一个数据
                if len(self.v.shape) == 4:
                    self.val = self.v[:].data if isinstance(self.v[:], np.ma.core.MaskedArray) else self.v[:]
                    self.val = self.v[:][0][0]
                    self.currentVal = self.val

                    self.longitude = list(map(lambda x: ('%.3f') % float(x), self.longitude.astype(np.float64)))

                    df = pd.DataFrame(self.val, columns=self.longitude)
                    df['平均值'] = df.mean(axis=1).round(decimals=3)
                    # print(df.columns.values.tolist())
                    self.columns = [str(c) for c in df.columns.values.tolist()]

                    self.TableWidget.setHorizontalHeaderLabels(self.columns)


                    for i, v0 in enumerate(df.values.tolist()):
                        for j, v1 in enumerate(v0):
                            self.TableWidget.setItem(i, j, QTableWidgetItem(str(v1)))




                elif len(self.v.shape) == 3:
                    self.val = self.v[:][0]
                    df = pd.DataFrame(self.val)
                    df['平均值'] = df.mean(axis=1).round(decimals=3)
                    self.columns = [str(c) for c in df.columns.values.tolist()]
                    self.TableWidget.setHorizontalHeaderLabels(self.columns)
                    for i, v0 in enumerate(df.values.tolist()):
                        for j, v1 in enumerate(v0):
                            self.TableWidget.setItem(i, j, QTableWidgetItem(str(v1)))


                # TODO 优化 2 设置水平方向表格为自适应的伸缩模式
                ##TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

                # TODO 优化3 将表格变为禁止编辑
                self.TableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.flagExD = 0



        elif len(self.args) == 0:
            # 初始状态
            self.TableWidget.clear()
            self.TableWidget.setRowCount(0)
            self.TableWidget.setColumnCount(0)
            # self.TableWidget.setHorizontalHeaderLabels('')
    def GRIB(self):
        pass




    def chargeTime(self):
        fmt = self.comboBox_4.currentText()
        if len(self.v.shape) == 4:
            if self.comboBox_2.currentText() != '' and self.comboBox.currentText() != '':
                if 'time' in self.v.dimensions and 'level' in self.v.dimensions:
                    if len(self.time) > 0 and len(self.level) > 0:
                        ftindex = self.v.dimensions.index('time')
                        flindex = self.v.dimensions.index('level')
                        self.levelIndex = self.leveldict[self.comboBox_2.currentText()]
                        self.timeIndex = self.timedict[self.comboBox.currentText()]
                        if flindex == 0:
                            self.currentVal = self.v[:][self.levelIndex, self.timeIndex, :, :]
                        else:
                            self.currentVal = self.v[:][self.timeIndex, self.levelIndex, :, :]

                if 'time' in self.v.dimensions:
                    if len(self.time) > 0 and len(self.level) == 0:
                        ftindex = self.v.dimensions.index('time')
                        self.timeIndex = self.timedict[self.comboBox.currentText()]
                        self.levelIndex = self.seccomXdict[self.comboBox_2.currentText()]
                        if ftindex == 0:
                            self.currentVal = self.v[:][self.timeIndex, self.levelIndex, :, :]
                        else:
                            self.currentVal = self.v[:][self.levelIndex, self.timeIndex, :, :]

                if len(self.time) == 0 and len(self.level) == 0:

                    self.firstIndex = self.firstcomXdict[self.comboBox.currentText()]
                    self.secIndex = self.seccomXdict[self.comboBox_2.currentText()]
                    self.currentVal = self.v[:][self.firstIndex, self.secIndex, :, :]


            for case in switch(self.comboBox_3.currentText()):
                if case('平均值'):
                    self.mean(fmt,self.flagModel)
                    break
                if case('最大值'):
                    self.max(fmt,self.flagModel)
                    break
                if case('最小值'):
                    self.min(fmt,self.flagModel)
                    break
                if case('方差'):
                    self.var(fmt,self.flagModel)
                    break
                if case('标准差'):
                    self.std(fmt,self.flagModel)
                    break
                if case('中位数'):
                    self.median(fmt,self.flagModel)
                    break

                if case():  # default, could also just omit condition or 'if True'
                    print("something else!")
                    break

        elif len(self.v.shape) == 3:

            if len(self.time) > 0:
                self.timeIndex = self.timedict[self.comboBox.currentText()]
                self.currentVal = self.v[:][self.timeIndex, :, :]
            if len(self.level) > 0:
                self.levelIndex = self.leveldict[self.comboBox_2.currentText()]
                self.currentVal = self.v[:][self.levelIndex, :, :]
            if len(self.time) == 0 and len(self.level) == 0:
                self.firstIndex = self.firstcomXdict[self.comboBox.currentText()]
                self.currentVal = self.v[:][self.firstIndex, :, :]

            for case in switch(self.comboBox_3.currentText()):
                if case('平均值'):
                    self.mean(fmt,self.flagModel)
                    break
                if case('最大值'):
                    self.max(fmt,self.flagModel)
                    break

                if case('最小值'):
                    self.min(fmt,self.flagModel)
                    break
                if case('方差'):
                    self.var(fmt,self.flagModel)
                    break
                if case('标准差'):
                    self.std(fmt,self.flagModel)
                    break
                if case('中位数'):
                    self.median(fmt,self.flagModel)
                    break

                if case():  # default, could also just omit condition or 'if True'
                    print("something else!")
                    break


        elif len(self.v.shape) == 2:
            self.currentVal = self.val
            for case in switch(self.comboBox_3.currentText()):
                if case('平均值'):
                    self.mean(fmt,self.flagModel)
                    break
                if case('最大值'):
                    self.max(fmt,self.flagModel)
                    break

                if case('最小值'):
                    self.min(fmt,self.flagModel)
                    break
                if case('方差'):
                    self.var(fmt,self.flagModel)
                    break
                if case('标准差'):
                    self.std(fmt,self.flagModel)
                    break
                if case('中位数'):
                    self.median(fmt,self.flagModel)
                    break

                if case():  # default, could also just omit condition or 'if True'
                    print("something else!")
                    break





    def chargeLevel(self):
        fmt = self.comboBox_4.currentText()
        if len(self.v.shape) == 4:
            if self.comboBox_2.currentText() != '' and self.comboBox.currentText() != '':
                if 'time' in self.v.dimensions and 'level' in self.v.dimensions:
                    if len(self.time) > 0 and len(self.level) > 0:
                        ftindex = self.v.dimensions.index('time')
                        flindex = self.v.dimensions.index('level')
                        self.levelIndex = self.leveldict[self.comboBox_2.currentText()]
                        self.timeIndex = self.timedict[self.comboBox.currentText()]
                        if flindex == 0:
                            self.currentVal = self.v[:][self.levelIndex, self.timeIndex, :, :]
                        else:
                            self.currentVal = self.v[:][self.timeIndex, self.levelIndex, :, :]

                if 'time' in self.v.dimensions:
                    if len(self.time) > 0 and len(self.level) == 0:
                        ftindex = self.v.dimensions.index('time')
                        self.timeIndex = self.timedict[self.comboBox.currentText()]
                        self.levelIndex = self.seccomXdict[self.comboBox_2.currentText()]
                        if ftindex == 0:
                            self.currentVal = self.v[:][self.timeIndex, self.levelIndex, :, :]
                        else:
                            self.currentVal = self.v[:][self.levelIndex, self.timeIndex, :, :]

                if len(self.time) == 0 and len(self.level) == 0:

                    self.firstIndex = self.firstcomXdict[self.comboBox.currentText()]
                    self.secIndex = self.seccomXdict[self.comboBox_2.currentText()]
                    self.currentVal = self.v[:][self.firstIndex, self.secIndex, :, :]


            for case in switch(self.comboBox_3.currentText()):
                if case('平均值'):
                    self.mean(fmt,self.flagModel)
                    break
                if case('最大值'):
                    self.max(fmt,self.flagModel)
                    break
                if case('最小值'):
                    self.min(fmt,self.flagModel)
                    break
                if case('方差'):
                    self.var(fmt,self.flagModel)
                    break
                if case('标准差'):
                    self.std(fmt,self.flagModel)
                    break
                if case('中位数'):
                    self.median(fmt,self.flagModel)
                    break

                if case():  # default, could also just omit condition or 'if True'
                    print("something else!")
                    break

        elif len(self.v.shape) == 3:

            if len(self.time) > 0:
                self.timeIndex = self.timedict[self.comboBox.currentText()]
                self.currentVal = self.v[:][self.timeIndex, :, :]
            if len(self.level) > 0:
                self.levelIndex = self.leveldict[self.comboBox_2.currentText()]
                self.currentVal = self.v[:][self.levelIndex, :, :]
            if len(self.time) == 0 and len(self.level) == 0:
                self.firstIndex = self.firstcomXdict[self.comboBox.currentText()]
                self.currentVal = self.v[:][self.firstIndex, :, :]

            for case in switch(self.comboBox_3.currentText()):
                if case('平均值'):
                    self.mean(fmt,self.flagModel)
                    break
                if case('最大值'):
                    self.max(fmt,self.flagModel)
                    break

                if case('最小值'):
                    self.min(fmt,self.flagModel)
                    break
                if case('方差'):
                    self.var(fmt,self.flagModel)
                    break
                if case('标准差'):
                    self.std(fmt,self.flagModel)
                    break
                if case('中位数'):
                    self.median(fmt,self.flagModel)
                    break

                if case():  # default, could also just omit condition or 'if True'
                    print("something else!")
                    break


        elif len(self.v.shape) == 2:
            self.currentVal = self.val
            for case in switch(self.comboBox_3.currentText()):
                if case('平均值'):
                    self.mean(fmt,self.flagModel)
                    break
                if case('最大值'):
                    self.max(fmt,self.flagModel)
                    break

                if case('最小值'):
                    self.min(fmt,self.flagModel)
                    break
                if case('方差'):
                    self.var(fmt,self.flagModel)
                    break
                if case('标准差'):
                    self.std(fmt,self.flagModel)
                    break
                if case('中位数'):
                    self.median(fmt,self.flagModel)
                    break

                if case():  # default, could also just omit condition or 'if True'
                    print("something else!")
                    break









    def chargeMean(self):

        fmt = self.comboBox_4.currentText()
        if self.flagModel == 'MICAPS4':


            for case in switch(self.comboBox_3.currentText()):
                if case('平均值'):
                    self.mean(fmt, self.flagModel)
                    break
                if case('最大值'):
                    self.max(fmt, self.flagModel)
                    break

                if case('最小值'):
                    self.min(fmt, self.flagModel)
                    break
                if case('方差'):
                    self.var(fmt, self.flagModel)
                    break
                if case('标准差'):
                    self.std(fmt, self.flagModel)
                    break
                if case('中位数'):
                    self.median(fmt, self.flagModel)
                    break

                if case():  # default, could also just omit condition or 'if True'
                    print("something else!")
                    break


        elif self.flagModel == 'HDF':
            if len(self.v.shape) == 4:
                if self.comboBox_2.currentText() != '' and self.comboBox.currentText() != '':
                    if 'time' in self.v.dimensions and 'level' in self.v.dimensions:
                        if len(self.time) > 0 and len(self.level) > 0:
                            ftindex = self.v.dimensions.index('time')
                            flindex = self.v.dimensions.index('level')
                            self.levelIndex = self.leveldict[self.comboBox_2.currentText()]
                            self.timeIndex = self.timedict[self.comboBox.currentText()]
                            if flindex == 0:
                                self.currentVal = self.v[:][self.levelIndex, self.timeIndex, :, :]
                            else:
                                self.currentVal = self.v[:][self.timeIndex, self.levelIndex, :, :]

                    if 'time' in self.v.dimensions:
                        if len(self.time) > 0 and len(self.level) == 0:
                            ftindex = self.v.dimensions.index('time')
                            self.timeIndex = self.timedict[self.comboBox.currentText()]
                            self.levelIndex = self.seccomXdict[self.comboBox_2.currentText()]
                            if ftindex == 0:
                                self.currentVal = self.v[:][self.timeIndex, self.levelIndex, :, :]
                            else:
                                self.currentVal = self.v[:][self.levelIndex, self.timeIndex, :, :]

                    if len(self.time) == 0 and len(self.level) == 0:
                        self.firstIndex = self.firstcomXdict[self.comboBox.currentText()]
                        self.secIndex = self.seccomXdict[self.comboBox_2.currentText()]
                        self.currentVal = self.v[:][self.firstIndex, self.secIndex, :, :]

                for case in switch(self.comboBox_3.currentText()):
                    if case('平均值'):
                        self.mean(fmt, self.flagModel)
                        break
                    if case('最大值'):
                        self.max(fmt, self.flagModel)
                        break
                    if case('最小值'):
                        self.min(fmt, self.flagModel)
                        break
                    if case('方差'):
                        self.var(fmt, self.flagModel)
                        break
                    if case('标准差'):
                        self.std(fmt, self.flagModel)
                        break
                    if case('中位数'):
                        self.median(fmt, self.flagModel)
                        break

                    if case():  # default, could also just omit condition or 'if True'
                        print("something else!")
                        break




            elif len(self.v.shape) == 3:

                if len(self.time) > 0:
                    self.timeIndex = self.timedict[self.comboBox.currentText()]
                    self.currentVal = self.v[:][self.timeIndex, :, :]
                if len(self.level) > 0:
                    self.levelIndex = self.leveldict[self.comboBox_2.currentText()]
                    self.currentVal = self.v[:][self.levelIndex, :, :]
                if len(self.time) == 0 and len(self.level) == 0:
                    self.firstIndex = self.firstcomXdict[self.comboBox.currentText()]
                    self.currentVal = self.v[:][self.firstIndex, :, :]

                for case in switch(self.comboBox_3.currentText()):
                    if case('平均值'):
                        self.mean(fmt, self.flagModel)
                        break
                    if case('最大值'):
                        self.max(fmt, self.flagModel)
                        break

                    if case('最小值'):
                        self.min(fmt, self.flagModel)
                        break
                    if case('方差'):
                        self.var(fmt, self.flagModel)
                        break
                    if case('标准差'):
                        self.std(fmt, self.flagModel)
                        break
                    if case('中位数'):
                        self.median(fmt, self.flagModel)
                        break

                    if case():  # default, could also just omit condition or 'if True'
                        print("something else!")
                        break


            elif len(self.v.shape) == 2:
                self.currentVal = self.val
                for case in switch(self.comboBox_3.currentText()):
                    if case('平均值'):
                        self.mean(fmt, self.flagModel)
                        break
                    if case('最大值'):
                        self.max(fmt, self.flagModel)
                        break

                    if case('最小值'):
                        self.min(fmt, self.flagModel)
                        break
                    if case('方差'):
                        self.var(fmt, self.flagModel)
                        break
                    if case('标准差'):
                        self.std()
                        break
                    if case('中位数'):
                        self.median(fmt, self.flagModel)
                        break

                    if case():  # default, could also just omit condition or 'if True'
                        print("something else!")
                        break
        elif self.flagModel == 'NetCDF':
            if len(self.v.shape) == 4:
                if self.comboBox_2.currentText() != '' and self.comboBox.currentText() != '':
                    if 'time' in self.v.dimensions and 'level' in self.v.dimensions:
                        if len(self.time) > 0 and len(self.level) > 0:
                            ftindex = self.v.dimensions.index('time')
                            flindex = self.v.dimensions.index('level')
                            self.levelIndex = self.leveldict[self.comboBox_2.currentText()]
                            self.timeIndex = self.timedict[self.comboBox.currentText()]
                            if flindex == 0:
                                self.currentVal = self.v[:][self.levelIndex, self.timeIndex, :, :]
                            else:
                                self.currentVal = self.v[:][self.timeIndex, self.levelIndex, :, :]

                    if 'time' in self.v.dimensions:
                        if len(self.time) > 0 and len(self.level) == 0:
                            ftindex = self.v.dimensions.index('time')
                            self.timeIndex = self.timedict[self.comboBox.currentText()]
                            self.levelIndex = self.seccomXdict[self.comboBox_2.currentText()]
                            if ftindex == 0:
                                self.currentVal = self.v[:][self.timeIndex, self.levelIndex, :, :]
                            else:
                                self.currentVal = self.v[:][self.levelIndex, self.timeIndex, :, :]

                    if len(self.time) == 0 and len(self.level) == 0:
                        self.firstIndex = self.firstcomXdict[self.comboBox.currentText()]
                        self.secIndex = self.seccomXdict[self.comboBox_2.currentText()]
                        self.currentVal = self.v[:][self.firstIndex, self.secIndex, :, :]

                for case in switch(self.comboBox_3.currentText()):
                    if case('平均值'):
                        self.mean(fmt, self.flagModel)
                        break
                    if case('最大值'):
                        self.max(fmt, self.flagModel)
                        break
                    if case('最小值'):
                        self.min(fmt, self.flagModel)
                        break
                    if case('方差'):
                        self.var(fmt, self.flagModel)
                        break
                    if case('标准差'):
                        self.std(fmt, self.flagModel)
                        break
                    if case('中位数'):
                        self.median(fmt, self.flagModel)
                        break

                    if case():  # default, could also just omit condition or 'if True'
                        print("something else!")
                        break




            elif len(self.v.shape) == 3:

                if len(self.time) > 0:
                    self.timeIndex = self.timedict[self.comboBox.currentText()]
                    self.currentVal = self.v[:][self.timeIndex, :, :]
                if len(self.level) > 0:
                    self.levelIndex = self.leveldict[self.comboBox_2.currentText()]
                    self.currentVal = self.v[:][self.levelIndex, :, :]
                if len(self.time) == 0 and len(self.level) == 0:
                    self.firstIndex = self.firstcomXdict[self.comboBox.currentText()]
                    self.currentVal = self.v[:][self.firstIndex, :, :]

                for case in switch(self.comboBox_3.currentText()):
                    if case('平均值'):
                        self.mean(fmt, self.flagModel)
                        break
                    if case('最大值'):
                        self.max(fmt, self.flagModel)
                        break

                    if case('最小值'):
                        self.min(fmt, self.flagModel)
                        break
                    if case('方差'):
                        self.var(fmt, self.flagModel)
                        break
                    if case('标准差'):
                        self.std(fmt, self.flagModel)
                        break
                    if case('中位数'):
                        self.median(fmt, self.flagModel)
                        break

                    if case():  # default, could also just omit condition or 'if True'
                        print("something else!")
                        break


            elif len(self.v.shape) == 2:
                self.currentVal = self.val
                for case in switch(self.comboBox_3.currentText()):
                    if case('平均值'):
                        self.mean(fmt, self.flagModel)
                        break
                    if case('最大值'):
                        self.max(fmt, self.flagModel)
                        break

                    if case('最小值'):
                        self.min(fmt, self.flagModel)
                        break
                    if case('方差'):
                        self.var(fmt, self.flagModel)
                        break
                    if case('标准差'):
                        self.std()
                        break
                    if case('中位数'):
                        self.median(fmt, self.flagModel)
                        break

                    if case():  # default, could also just omit condition or 'if True'
                        print("something else!")
                        break
        elif self.flagModel == 'GRIB':
            pass





        # if len(self.v.shape) == 4:
        #     if self.comboBox_2.currentText() != '' and self.comboBox.currentText() != '':
        #         if 'time' in self.v.dimensions and 'level' in self.v.dimensions:
        #             if len(self.time) > 0 and len(self.level) > 0:
        #                 ftindex = self.v.dimensions.index('time')
        #                 flindex = self.v.dimensions.index('level')
        #                 self.levelIndex = self.leveldict[self.comboBox_2.currentText()]
        #                 self.timeIndex = self.timedict[self.comboBox.currentText()]
        #                 if flindex == 0:
        #                     self.currentVal = self.v[:][self.levelIndex, self.timeIndex, :, :]
        #                 else:
        #                     self.currentVal = self.v[:][self.timeIndex, self.levelIndex, :, :]
        #
        #         if 'time' in self.v.dimensions:
        #             if len(self.time) > 0 and len(self.level) == 0:
        #                 ftindex = self.v.dimensions.index('time')
        #                 self.timeIndex = self.timedict[self.comboBox.currentText()]
        #                 self.levelIndex = self.seccomXdict[self.comboBox_2.currentText()]
        #                 if ftindex == 0:
        #                     self.currentVal = self.v[:][self.timeIndex, self.levelIndex, :, :]
        #                 else:
        #                     self.currentVal = self.v[:][self.levelIndex, self.timeIndex, :, :]
        #
        #
        #         if len(self.time) == 0 and len(self.level) == 0:
        #
        #             self.firstIndex = self.firstcomXdict[self.comboBox.currentText()]
        #             self.secIndex = self.seccomXdict[self.comboBox_2.currentText()]
        #             self.currentVal = self.v[:][self.firstIndex, self.secIndex, :, :]
        #
        #
        #
        #
        #     for case in switch(self.comboBox_3.currentText()):
        #         if case('平均值'):
        #             self.mean(fmt,self.flagModel)
        #             break
        #         if case('最大值'):
        #             self.max(fmt,self.flagModel)
        #             break
        #         if case('最小值'):
        #             self.min(fmt,self.flagModel)
        #             break
        #         if case('方差'):
        #             self.var(fmt,self.flagModel)
        #             break
        #         if case('标准差'):
        #             self.std(fmt,self.flagModel)
        #             break
        #         if case('中位数'):
        #             self.median(fmt,self.flagModel)
        #             break
        #
        #         if case():  # default, could also just omit condition or 'if True'
        #             print("something else!")
        #             break
        #
        #
        #
        #
        # elif len(self.v.shape) == 3:
        #
        #
        #     if len(self.time) > 0:
        #         self.timeIndex = self.timedict[self.comboBox.currentText()]
        #         self.currentVal = self.v[:][self.timeIndex, :, :]
        #     if len(self.level) > 0:
        #         self.levelIndex = self.leveldict[self.comboBox_2.currentText()]
        #         self.currentVal = self.v[:][self.levelIndex, :, :]
        #     if len(self.time) == 0 and len(self.level) == 0:
        #         self.firstIndex = self.firstcomXdict[self.comboBox.currentText()]
        #         self.currentVal = self.v[:][self.firstIndex, :, :]
        #
        #
        #
        #
        #     for case in switch(self.comboBox_3.currentText()):
        #         if case('平均值'):
        #             self.mean(fmt,self.flagModel)
        #             break
        #         if case('最大值'):
        #             self.max(fmt,self.flagModel)
        #             break
        #
        #         if case('最小值'):
        #             self.min(fmt,self.flagModel)
        #             break
        #         if case('方差'):
        #             self.var(fmt,self.flagModel)
        #             break
        #         if case('标准差'):
        #             self.std(fmt,self.flagModel)
        #             break
        #         if case('中位数'):
        #             self.median(fmt,self.flagModel)
        #             break
        #
        #         if case():  # default, could also just omit condition or 'if True'
        #             print("something else!")
        #             break
        #
        #
        # elif len(self.v.shape) == 2:
        #     self.currentVal = self.v
        #     print(self.v.shape)
        #     for case in switch(self.comboBox_3.currentText()):
        #         if case('平均值'):
        #             self.mean(fmt,self.flagModel)
        #             break
        #         if case('最大值'):
        #             self.max(fmt,self.flagModel)
        #             break
        #
        #         if case('最小值'):
        #             self.min(fmt,self.flagModel)
        #             break
        #         if case('方差'):
        #             self.var(fmt,self.flagModel)
        #             break
        #         if case('标准差'):
        #             self.std()
        #             break
        #         if case('中位数'):
        #             self.median(fmt,self.flagModel)
        #             break
        #
        #         if case():  # default, could also just omit condition or 'if True'
        #             print("something else!")
        #             break
        #







    def exportData(self):
        if self.flagExD == 0:
            openfileName = QFileDialog.getSaveFileName(self, "选取文件", r"D:\PanoplyWin\{varName}.csv".format(varName=self.varName),"Binary files(*.nc , *.hdf ,*.GRB, *.grb2);;All Files (*)")
            #df = pd.DataFrame(self.v[:][0][0], index=self.latitude, columns=self.longitude)
            if openfileName[0]:
                if len(self.currentVal) > 0 and len(self.latitude) > 0 and len(self.longitude) > 0:
                    df = pd.DataFrame(self.currentVal, index=self.latitude, columns=self.longitude)
                    df.to_csv(openfileName[0])
                else:
                    if len(self.latitude) > 0 and len(self.longitude) > 0:
                        df = pd.DataFrame(self.val, index=self.latitude, columns=self.longitude)
                        df.to_csv(openfileName[0])




        '''
        writer=pd.ExcelWriter('test.xlsx')
        
        df1.to_excel(writer,sheet_name='Data1',startcol=0,index=False)
        df2.to_excel(writer,sheet_name='Data1',startcol=1,index=False)
        df3.to_excel(writer,sheet_name='Data3',index=False)

        
        
        '''


    def chargelat(self):
        if self.checkBox.isChecked():
            self.TableWidget.verticalHeader().setVisible(False)
        else:
            self.TableWidget.verticalHeader().setVisible(True)

    def chargelon(self):
        if self.checkBox_2.isChecked():
            self.TableWidget.horizontalHeader().setVisible(False)
        else:
            self.TableWidget.horizontalHeader().setVisible(True)


    def setPropertyInfo(self):

        self.TableWidget.verticalHeader().setVisible(False)
        self.TableWidget.horizontalHeader().setVisible(False)

    def sliderval_h(self):
        print(self.TableWidget.horizontalScrollBar().value())
        self.TableWidget.horizontalScrollBar().value()

    def sliderval_v(self):
        print(self.TableWidget.verticalScrollBar().value())


    def mean(self,fmt=None,model=None):

        if model == 'MICAPS4':
            df = pd.DataFrame(self.m4data, columns=self.longitude)
            df['平均值'] = df.mean(axis=1).round(decimals=2)
            if fmt:
                df = df.applymap(lambda x: fmt % x)
            self.dfmodel.setDataFrame(df)




        elif model == 'HDF':
            df = pd.DataFrame(self.currentVal, columns=self.longitude)
            if self.v.shape[0] > 1000 and self.v.shape[1] > 1000:
                df = df.iloc[0:1000, 0:1000]
            df['平均值'] = df.mean(axis=1).round(decimals=3)
            if fmt:
                df = df.applymap(lambda x: fmt % x)
            self.dfmodel.setDataFrame(df)
        elif model == 'NetCDF':
            df = pd.DataFrame(self.currentVal, columns=self.longitude)
            if self.v.shape[0] > 1000 and self.v.shape[1] > 1000:
                df = df.iloc[0:1000, 0:1000]
            df['平均值'] = df.mean(axis=1).round(decimals=3)
            if fmt:
                df = df.applymap(lambda x: fmt % x)
            self.dfmodel.setDataFrame(df)


        elif model == 'GRIB':
            pass




    def max(self,fmt=None,model=None):

        if model == 'MICAPS4':
            df = pd.DataFrame(self.m4data, columns=self.longitude)
            df['最大值'] = df.max(axis=1)
            if fmt:
                df = df.applymap(lambda x: fmt % x)
            self.dfmodel.setDataFrame(df)

        elif model == 'HDF':
            df = pd.DataFrame(self.currentVal, columns=self.longitude)

            df['最大值'] = df.max(axis=1)
            if fmt:
                df = df.applymap(lambda x: fmt % x)
            self.dfmodel.setDataFrame(df)

        elif model == 'NetCDF':
            df = pd.DataFrame(self.currentVal, columns=self.longitude)

            df['最大值'] = df.max(axis=1)
            if fmt:
                df = df.applymap(lambda x: fmt % x)
            self.dfmodel.setDataFrame(df)
        elif model == 'GRIB':
            pass








    def min(self,fmt=None,model=None):

        if model == 'MICAPS4':
            df = pd.DataFrame(self.m4data, columns=self.longitude)
            df['最小值'] = df.min(axis=1)
            if fmt:
                df = df.applymap(lambda x: fmt % x)
            self.dfmodel.setDataFrame(df)

        elif model == 'HDF':
            df = pd.DataFrame(self.currentVal, columns=self.longitude)
            if self.v.shape[0] > 1000 and self.v.shape[1] > 1000:
                df = df.iloc[0:1000, 0:1000]
            df['最小值'] = df.min(axis=1)
            if fmt:
                df = df.applymap(lambda x: fmt % x)
            self.dfmodel.setDataFrame(df)

        elif model == 'NetCDF':
            df = pd.DataFrame(self.currentVal, columns=self.longitude)
            if self.v.shape[0] > 1000 and self.v.shape[1] > 1000:
                df = df.iloc[0:1000, 0:1000]
            df['最小值'] = df.min(axis=1)
            if fmt:
                df = df.applymap(lambda x: fmt % x)
            self.dfmodel.setDataFrame(df)
        elif model == 'GRIB':
            pass



    def var(self,fmt=None,model=None):

        if model == 'MICAPS4':
            df = pd.DataFrame(self.m4data, columns=self.longitude)
            df['方差'] = df.var(axis=1).round(decimals=3)
            if fmt:
                df = df.applymap(lambda x: fmt % x)
            self.dfmodel.setDataFrame(df)

        elif model == 'HDF':
            df = pd.DataFrame(self.currentVal, columns=self.longitude)

            df['方差'] = df.var(axis=1).round(decimals=3)
            if fmt:
                df = df.applymap(lambda x: fmt % x)
            self.dfmodel.setDataFrame(df)

        elif model == 'NetCDF':
            df = pd.DataFrame(self.currentVal, columns=self.longitude)

            df['方差'] = df.var(axis=1).round(decimals=3)
            if fmt:
                df = df.applymap(lambda x: fmt % x)
            self.dfmodel.setDataFrame(df)
        elif model == 'GRIB':
            pass


    def std(self,fmt=None,model=None):
        if model == 'MICAPS4':
            df = pd.DataFrame(self.m4data, columns=self.longitude)
            df['标准差'] = df.std(axis=1).round(decimals=3)
            if fmt:
                df = df.applymap(lambda x: fmt % x)
            self.dfmodel.setDataFrame(df)

        elif model == 'HDF':
            df = pd.DataFrame(self.currentVal, columns=self.longitude)
            df['标准差'] = df.std(axis=1).round(decimals=3)
            if fmt:
                df = df.applymap(lambda x: fmt % x)
            self.dfmodel.setDataFrame(df)

        elif model == 'NetCDF':
            df = pd.DataFrame(self.currentVal, columns=self.longitude)

            df['标准差'] = df.std(axis=1).round(decimals=3)
            if fmt:
                df = df.applymap(lambda x: fmt % x)
            self.dfmodel.setDataFrame(df)
        elif model == 'GRIB':
            pass



    def median(self,fmt=None,model=None):

        if model == 'MICAPS4':
            df = pd.DataFrame(self.m4data, columns=self.longitude)
            df['中位数'] = df.median(axis=1)
            if fmt:
                df = df.applymap(lambda x: fmt % x)
            self.dfmodel.setDataFrame(df)

        elif model == 'HDF':
            df = pd.DataFrame(self.currentVal, columns=self.longitude)

            df['中位数'] = df.median(axis=1)
            if fmt:
                df = df.applymap(lambda x: fmt % x)
            self.dfmodel.setDataFrame(df)

        elif model == 'NetCDF':
            df = pd.DataFrame(self.currentVal, columns=self.longitude)

            df['中位数'] = df.median(axis=1)
            if fmt:
                df = df.applymap(lambda x: fmt % x)
            self.dfmodel.setDataFrame(df)
        elif model == 'GRIB':
            pass




    def chargeformat(self):
        fmt = self.comboBox_4.currentText()

        for case in switch(self.comboBox_3.currentText()):
            if case('平均值'):
                self.mean(fmt,self.flagModel)
                break
            if case('最大值'):
                self.max(fmt,self.flagModel)
                break
            if case('最小值'):
                self.min(fmt,self.flagModel)
                break
            if case('方差'):
                self.var(fmt,self.flagModel)
                break
            if case('标准差'):
                self.std(fmt,self.flagModel)
                break
            if case('中位数'):
                self.median(fmt,self.flagModel)
                break

            if case():  # default, could also just omit condition or 'if True'
                print("something else!")
                break












    def exportAllData(self):
        openfileName = QFileDialog.getSaveFileName(self, "选取文件", r"D:\PanoplyWin\{varName}.csv".format(varName=self.varName),"Binary files(*.nc , *.hdf ,*.GRB, *.grb2);;All Files (*)")

        '''
        writer=pd.ExcelWriter('test.xlsx')
        
        df1.to_excel(writer,sheet_name='Data1',startcol=0,index=False)
        df2.to_excel(writer,sheet_name='Data1',startcol=1,index=False)
        df3.to_excel(writer,sheet_name='Data3',index=False)

        '''

        if openfileName[0]:

            if len(self.currentVal) > 0 and len(self.latitude) > 0 and len(self.longitude) > 0:
                df = pd.DataFrame(self.currentVal, index=self.latitude, columns=self.longitude)
                df.to_csv(openfileName[0])
            else:
                if len(self.latitude) > 0 and len(self.longitude) > 0:
                    df = pd.DataFrame(self.val, index=self.latitude, columns=self.longitude)
                    df.to_csv(openfileName[0])





    def removeTableconx(self):

        self.textBrowser.clear()
        self.TableWidget.clear()
        self.TableWidget.setRowCount(0)
        self.TableWidget.setColumnCount(0)

        self.comboBox.clear()
        self.comboBox_2.clear()
        self.comboBox_3.clear()
        self.time = []
        self.level = []
        self.latitude = []
        self.longitude = []
        self.currentVal = []
        self.flagExD = 1

class switch(object):

    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False




