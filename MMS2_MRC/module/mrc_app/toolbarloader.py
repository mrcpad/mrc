#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: 
@author: xxf
@site: 
@software: PyCharm
@file: 工具栏按钮初始化，创建工具栏按钮，实现依赖注入
@time: 2019-7-29
"""

import os
from module.mrc_core.gloalConfig import GloalConfig
from logs.log import logger
import xml.dom.minidom as dom
from module.mrc_core.applicationContext import AppContext
# from PyQt5.QtWidgets import QToolBar
# from PyQt5.QtCore import QCoreApplication
# from PyQt5.QtGui import QIcon, QGuiApplication
from module.mrc_infrastructure.iCommand import ICommand
from module.mrc_core.actionQ import ActionQ
from module.mrc_infrastructure.iCommandActive import CommandActive
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.Qt import *
#from module.mrc_command.tool import *


class ToolBarLoader(CommandActive):
    # 菜单配置路径
    config_path = os.path.join(GloalConfig().config, 'toolbar.xml')
    image_dir = GloalConfig().image

    def __init__(self, mainWindow, treeWidget, tabWidget):
        self.mainWindow = mainWindow
        #self.textBrowser = textBrowser
        self.treeWidget = treeWidget
        self.tabWidget = tabWidget

    def CreateQToolBar(self):
        _translate = QCoreApplication.translate
        screen = QGuiApplication.primaryScreen()  # 主屏幕信息
        dom_tree = dom.parse(self.config_path)
        dom_coll = dom_tree.documentElement
        if dom_coll.hasAttribute("toolbars"):
            logger.info("Root element : %s" % dom_coll.getAttribute("toolbars"))
        toolbar_name = dom_coll.getAttribute("name")
        self.toolbar = QToolBar(self.mainWindow)
        self.toolbar.setObjectName(toolbar_name)
        self.toolbar.setIconSize(QtCore.QSize(60, 60))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle(0))
        self.toolbar.setStyleSheet('''
                QToolBar{background:#F0F0F0;border-radius:50px;}
                QToolBar:hover{background:#F0F0F0;}
                QToolButton{border:none;border-radius:50px;}
                QToolButton:hover{border-bottom:2px solid #F0F0F0;}
                ''')


        tools = dom_coll.getElementsByTagName("toolbar")
        for tool in tools:
            tool_caption = tool.getAttribute("caption")
            tool_name = tool.getAttribute("name")

            buttons = tool.getElementsByTagName("button")
            for btn in buttons:
                btn_caption = btn.getAttribute("caption")
                btn_name = btn.getAttribute("name")  # 图片路径
                btn_icon = btn.getAttribute("iconPath")  # 图片路径
                btn_toolTip = btn.getAttribute("toolTip")
                btn_shortcut = btn.getAttribute("shortcut")  # 快捷键
                btn_visible = btn.getAttribute("visible")  # 是否可见
                btn_enable = btn.getAttribute("enable")  # 是否可用
                btn_command = btn.getAttribute("command")  # 命令

                # 创建QAction
                action = ActionQ(self.mainWindow)  # 创建ActionQ信号,继承Action
                action.setObjectName(btn_name)
                action.setText(_translate("MainWindow", btn_caption))
                icon = QIcon()
                icon.addPixmap(QtGui.QPixmap(self.image_dir + '/' + btn_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                action.setIcon(icon)  # 设置图片
                action.setToolTip(_translate("MainWindow", btn_toolTip))
                action.setVisible(True if btn_visible.lower() == "true" else False)
                action.setEnabled(True if btn_enable.lower() == "true" else False)
                action.setShortcut(_translate("MainWindow", btn_shortcut))
                action.setShortcutContext(QtCore.Qt.WindowShortcut)
                action.setPriority(QtWidgets.QAction.NormalPriority)
                # QActionGroup()
                # action.setActionGroup()
                action.tag = btn_command
                command = AppContext.GetObject(btn_command)  # springpython 实现Ioc控制翻转
                if isinstance(command, ICommand):
                    command.mainWindow = self.mainWindow
                    #command.textBrowser = self.textBrowser  # 设置文本显示控件
                    command.treeWidget = self.treeWidget  # 设置树形结构控件
                    command.tabWidget = self.tabWidget
                    command.InitCmd(action)  # 注册action

                self.toolbar.addAction(action)

        logger.info("Root element : %s" % dom_coll.getAttribute("toolbars")+"   OK")
        return self.toolbar
