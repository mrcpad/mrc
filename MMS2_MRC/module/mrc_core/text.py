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
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QMainWindow,QTextBrowser
from module.mrc_core.actionQ import ActionQ
from logs.log import logger
import lib.getpath as gp
from module.mrc_core.algorithmfactory import AlgorithmFactory
from module.algorithm.algorithmbase import PyMeteoObject



class OpenFileCmd(BaseCommand):
    '''
    打开文件命令
    '''

    def Init(self):
        print("")
        if not isinstance(self.action, ActionQ) or not isinstance(self.mainWindow,QMainWindow):
            return None

        self.error = "menu.openfilecmd,we have a error : "
        files = self.OpenFile()  # 打开文件

        algorithmList={}

        # 执行解码算法
        for file in files:
            algorithmObject = PyMeteoObject()
            algorithmObject.file=file
            algorithmObject.fileName=gp.get_filename(file)
            algorithmObject.meteoDataInfo=AlgorithmFactory.create_algorithm(file)
            if algorithmObject.meteoDataInfo==None:
                QMessageBox.warning(self.mainWindow,"错误","Unknown file format: %s"%(algorithmObject.fileName))
                continue
            else:
                algorithmList.setdefault(algorithmObject.fileName,algorithmObject)

        self.treeWidget.SetTreeWidgetItem(algorithmList)


    def OpenFile(self):
        if not isinstance(self.action, ActionQ):
            message = QMessageBox(title="错误", text="执行错误")
            message.show()
            return

        try:
            fileDialog = QFileDialog(parent=self.mainWindow, caption=self.action.toolTip())

            # v=QFileDialog.FileMode(2)
            # fileDialog.setFileMode(v)

            files = fileDialog.getOpenFileNames(parent=self.mainWindow, caption=self.action.toolTip())

            return files[0]
        except:
            logger.error(self.error, exc_info=1)










