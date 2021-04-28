#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: 
@author: 
@site: 
@software: PyCharm
@file: 
@time: 
"""


from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow
import sys
from module.mrc_app.menuloader import MenuLoader
from module.mrc_app.toolbarloader import ToolBarLoader
from module.mrc_controls.treewidget import MrcTreeWidget
from module.mrc_controls.tabWidget import MrcTabWidget
from PyQt5.QtGui import QGuiApplication as qGuiApp
from module.mrc_core.gloalConfig import GloalConfig
import functools
import os
import shutil
from logs.log import eh,fh
from module.algorithm.src.startConvert.MessageBox import MyMessageBox



class MainUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        #screen = qGuiApp.primaryScreen()

        #self.setFixedSize(screen.size().width(), screen.size().height())
        #self.showMaximized()
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.left_widget,1,0,12,2) # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget,1,2,12,10) # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget) # 设置窗口主部件

        #tabWidget
        self.tabWidget = MrcTabWidget()
        self.tabWidget.setObjectName("tabWidget")
        # self.statusbar = QtWidgets.QStatusBar()
        # self.statusbar.setObjectName("statusbar")
        # self.setStatusBar(self.statusbar)


        #添加textBrowser


        #添加treewidget
        self.treewidget = MrcTreeWidget()
        self.treewidget.setObjectName("treeWidget")
        self.treewidget.setMinimumWidth(500)
        self.treewidget.settabWidget(self.tabWidget)
        # 加载菜单栏
        menu_loader = MenuLoader(self, self.treewidget, self.tabWidget)
        self.menubar = menu_loader.CreateQMenu()

        # 加载工具栏
        toolbar_loader = ToolBarLoader(self,  self.treewidget, self.tabWidget)
        self.toolBar = toolbar_loader.CreateQToolBar()


        #添加菜单，工具栏，树形列表，Tab页
        self.setMenuBar(self.menubar)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)

        self.left_layout.addWidget(self.treewidget,1,0,12,2)
        self.right_layout.addWidget(self.tabWidget,1,2,12,10)
        self.main_layout.setSpacing(0)
        #self.main_layout.setVerticalSpacing(50)
        #self.main_layout.setHorizontalSpacing(0)
        self.setStyleSheet('''
        
        QWidget#left_widget{
    background:#F0F0F0;
    border-top:1px solid white;
    border-bottom:1px solid white;
    border-left:1px solid white;
    border-top-left-radius:10px;
    border-bottom-left-radius:10px;
}
 QWidget#right_widget{
    background:#F0F0F0;
    border-top:1px solid white;
    border-bottom:1px solid white;
    border-left:1px solid white;
    border-top-right-radius:10px;
    border-bottom-right-radius:10px;
}
    QWidget#treeWidget{
    background:#F0F0F0;
    border-top:1px solid #F0F0F0;
    border-bottom:1px solid #F0F0F0;
    border-left:1px solid #F0F0F0;
    border-top-right-radius:30px;
    border-bottom-right-radius:30px;
}  
QWidget#tabWidget{
    background:#F8F8FF;
    border:none;
    border-top:1px solid #F0F0F0;
    border-bottom:1px solid #F0F0F0;
    border-left:1px solid #F0F0F0;
    border-top-right-radius:20px;
    border-bottom-right-radius:20px;
}  
QTreeWidgetItem{
    background:#F0F0F0;
    border-top:1px solid white;
    border-bottom:1px solid white;
    border-left:1px solid white;
    border-top-left-radius:10px;
    border-bottom-left-radius:10px;
        }  
        
    QTreeWidgetItem{
    background:#F0F0F0;
    border-top:1px solid white;
    border-bottom:1px solid white;
    border-left:1px solid white;
    border-top-left-radius:10px;
    border-bottom-left-radius:10px;
        }  
 
 QMenuBar {
    background-color: #F0F8FF;
    #color: white;
}

QMenuBar::item {
    background: #F0F8FF;
}

QMenuBar::item:disabled {
    color: #F0F0F0;
}

QMenuBar::item:selected {
    background: #222222;
}

QMenuBar::item:pressed {
    background: #444444;
}
     
    QTabBar::tab:selected {
    border-color: #9B9B9B;
    border-bottom-color: #C2C7CB; /* same as pane color */
}

QTabBar::tab:!selected {
    margin-top: 2px; /* make non-selected tabs look smaller */
}
QDialogButtonBox {
    button-layout: 0;
}
''')

        self.setWindowOpacity(1)  # 设置窗口透明度
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        #self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框


    def closeEvent(self, event):
        yes = QMessageBox.question(self, '系统退出提示', '您是否确认退出!', QMessageBox.Yes | QMessageBox.No)
        if yes == QMessageBox.Yes:
            event.accept()
            self.treewidget.removeTree()
            logpath = os.path.join(os.path.abspath('.'), 'log')
            tmppath = os.path.join(logpath, 'temp')
            if os.path.exists(tmppath):
                shutil.rmtree(tmppath)
            # reply = QMessageBox.question(self, '信息提示', '您是否删除运行日志文件!', QMessageBox.Yes | QMessageBox.No)
            # if reply == QMessageBox.Yes:
            #     if eh:
            #         eh.close()
            #     if fh:
            #         fh.close()
            #     if os.path.exists(logpath):
            #         shutil.rmtree(logpath)
            # else:
            #     pass
        else:
            event.ignore()




def just_one_instance(func):


    @functools.wraps(func)
    def f(*args,**kwargs):
        import socket
        try:
            global s
            s = socket.socket()
            host = socket.gethostname()
            s.bind((host, 60123))


        except Exception as arg:
            print('ERROR', arg.args)
            return None
        return func(*args,**kwargs)

    return f





@just_one_instance
def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.setWindowTitle('模式产品读数器')
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(GloalConfig.ImagePath()+"/globe.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    gui.setWindowIcon(icon)
    gui.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()