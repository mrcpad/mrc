#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: 
@author: xxf
@site: 
@software: PyCharm
@file: 通过配置动态加载菜单栏，通过springpython 实现菜单按钮注册点击事件
@time: 2019-7-26
"""

import os
from module.mrc_core.gloalConfig import GloalConfig
from logs.log import logger
import xml.dom.minidom as dom
from module.mrc_infrastructure.iCommandActive import CommandActive
from module.mrc_core.applicationContext import AppContext
import PyQt5.QtWidgets as QtWidgets,PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMenuBar,QMenu
from PyQt5.QtCore import QRect,QCoreApplication
from PyQt5.QtGui import QGuiApplication
from module.mrc_infrastructure.iCommand import ICommand
from module.mrc_core.actionQ import ActionQ
from module.mrc_command.menu.convert import *
from module.mrc_command.menu import *

class MenuLoader(CommandActive):
    # 菜单配置路径
    config_path = os.path.join(GloalConfig().config, 'menu.xml')

    def __init__(self,mainWindow,treeWidget,tabWidget):
        super(MenuLoader,self).__init__()
        #self.config_path=""
        # 菜单配置路径
        #self.config_path = os.path.join(GloalConfig().config, 'menu.xml')
        self.mainWindow = mainWindow
        #self.textBrowser = textBrowser
        self.treeWidget = treeWidget
        self.tabWidget = tabWidget


    def CreateQMenu(self):
        _translate = QCoreApplication.translate
        screen=QGuiApplication.primaryScreen()#主屏幕信息
        dom_tree=dom.parse(self.config_path)
        dom_coll=dom_tree.documentElement
        if dom_coll.hasAttribute("menuItems"):
            logger.info("Root element : %s" % dom_coll.getAttribute("menuItems"))


        menubar_name= dom_coll.getAttribute("name")
        # 创建QMenuBar
        self.menubar = QMenuBar(self.mainWindow)
        self.menubar.setObjectName(menubar_name)
        self.menubar.setGeometry(QRect(0, 0, screen.size().width(), 30))
        menus=dom_coll.getElementsByTagName("menuItem")
        for menu in menus:
            menu_id=menu.getAttribute("id")
            menu_name=menu.getAttribute("name")
            menu_caption=menu.getAttribute("caption")

            # 创建QMenu
            menu_c = QMenu(self.menubar)
            menu_c.setObjectName(menu_name)
            menu_c.setTitle(_translate("MainWindow",menu_caption))

            #创建QAction，将QAction绑定到QMenu
            buttons=menu.getElementsByTagName('button')
            for btn in buttons:
                btn_caption = btn.getAttribute("caption")
                btn_name = btn.getAttribute("name")  # 图片路径
                #btn_icon = btn.getAttribute("iconPath")  # 图片路径
                btn_toolTip = btn.getAttribute("toolTip")
                btn_shortcut = btn.getAttribute("shortcut")  # 快捷键
                btn_visible = btn.getAttribute("visible")  # 是否可见
                btn_enable = btn.getAttribute("enable")  # 是否可用
                btn_command = btn.getAttribute("command")  # 命令

                # 创建QAction
                action = ActionQ(self.mainWindow)  # 创建ActionQ信号,继承Action
                action.setObjectName(btn_name)
                action.setText(_translate("MainWindow", btn_caption))
                action.setToolTip(_translate("MainWindow", btn_toolTip))

                action.setVisible(True if btn_visible.lower() == "true" else False)
                action.setEnabled(True if btn_enable.lower() == "true" else False)
                action.setShortcut(_translate("MainWindow", btn_shortcut))
                action.setShortcutContext(QtCore.Qt.WindowShortcut)
                action.setPriority(QtWidgets.QAction.NormalPriority)
                action.tag=btn_command
                command = AppContext.GetObject(btn_command)#springpython 实现Ioc控制翻转

                if isinstance(command, ICommand):
                    command.mainWindow = self.mainWindow
                    #command.textBrowser = self.textBrowser#设置文本显示控件
                    command.treeWidget = self.treeWidget#设置树形结构控件
                    command.tabWidget = self.tabWidget

                    command.InitCmd(action)#注册action
                menu_c.addAction(action)

            self.menubar.addAction(menu_c.menuAction())

        logger.info("Root element : %s" % dom_coll.getAttribute("menuItems")+"   OK")
        return self.menubar

    def closelog(self):
        logger
