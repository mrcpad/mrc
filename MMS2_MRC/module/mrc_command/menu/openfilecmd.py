#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: v0.1
@author: xxf
@site: 
@software: PyCharm
@file: 打开文件菜单命令
@time: 2019-7-26
"""

from module.mrc_infrastructure.basecommand import BaseCommand
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMainWindow,QWidget
from module.mrc_core.actionQ import ActionQ
from logs.log import logger
from module.algorithmfactory import AlgorithmFactory
import re
import lib.judgetype as jt
from lib.judgetype import ModelDataType
import os
import datetime
import shutil


class OpenFileCmd(BaseCommand,QWidget):
    '''
    打开文件命令
    '''
    save_path = ''
    def Init(self):
        if not isinstance(self.action, ActionQ) or not isinstance(self.mainWindow,QMainWindow):
            return None

        self.error = "menu.openfilecmd,we have a error : "
        self.infoFlag = 0
        files = self.OpenFile()


        # 执行解码算法
        try:
            if files:
                if self.infoFlag == 0:
                    self.sendInfo()
                    self.infoFlag = 1
                self.treeWidget.SetTreeWidgetItem(files)

        except Exception as arg:
            print(arg)
            QMessageBox.warning(self, '警告', '打开文件执行异常,请检查文件！', QMessageBox.Yes, QMessageBox.No)
    def sendInfo(self):
        self.treeWidget.recvInfo(self.tabWidget, AlgorithmFactory)



    def OpenFile(self):
        global save_path
        save_path = ''
        if not isinstance(self.action, ActionQ):
            message = QMessageBox(title="错误", text="执行错误")
            message.show()
            return

        try:
            #fileDialog = QFileDialog(parent=self.mainWindow, caption=self.action.toolTip())
            # v=QFileDialog.FileMode(2)
            # fileDialog.setFileMode(v)

            #files = fileDialog.getOpenFileNames(parent=self.mainWindow, caption=self.action.toolTip())
            #files = QFileDialog.getOpenFileNames(self.mainWindow, "选取文件", r"/","Binary files(*.nc , *.hdf ,*.GRB, *.grb2);;All Files (*)")
            fileList = list()
            files = QFileDialog.getOpenFileNames(self.mainWindow, "选取文件", save_path,"Binary files(*.nc , *.hdf ,*.GRB, *.grb2);;All Files (*)")
            save_path = files[0]
            for file in files[0]:
                modelDataType = jt.judge_model_data_type(file)
                if modelDataType == ModelDataType.NETCDF or modelDataType == ModelDataType.HDF:
                    regex_str = ".*?([\u4E00-\u9FA5]+).*?"
                    match_obj = re.findall(regex_str, file)
                    if match_obj:
                        reply = QMessageBox.information(self, '提示', '您的NetCDF或者HDF文件路径中包含中文,继续执行请点击确认!',QMessageBox.Yes | QMessageBox.No)

                        if reply == QMessageBox.Yes:
                            logpath = os.path.join(os.path.abspath('.'), 'log')
                            if not os.path.exists(logpath):
                                os.makedirs(logpath)
                            tmppath = os.path.join(logpath, 'temp')
                            if not os.path.exists(tmppath):
                                os.makedirs(tmppath)
                            #ncfile = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                            ncfile = datetime.datetime.now().strftime('%Y%m%d%H')
                            tmpdir = os.path.join(tmppath, ncfile)
                            if not os.path.exists(tmpdir):
                                os.makedirs(tmpdir)
                            shutil.copy(file, tmpdir)
                            (filepath, tempfilename) = os.path.split(file)
                            file = os.path.join(tmpdir, tempfilename)
                            fileList.append(file)

                        else:
                            pass
                    else:
                        fileList.append(file)
                else:
                    fileList.append(file)




            return fileList
            #return files[0]
        except Exception as arg:
            logger.error(str(arg), exc_info=1)
            print(arg)
            QMessageBox.warning(self, '警告', '打开文件异常,请检查文件！', QMessageBox.Yes, QMessageBox.No)










