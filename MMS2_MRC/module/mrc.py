# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mrc.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import clr
import sys
sys.path.append(r'E:\Work\Hitec\MyCode\PythonNet\PythonNet\PythonNet\bin\Debug')
#clr.FindAssembly("PythonNet.dll")
a=clr.AddReference('PythonNet')
print(a)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1121, 842)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout_2.addWidget(self.textBrowser)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1121, 26))
        self.menubar.setObjectName("menubar")
        self.fileMenu = QtWidgets.QMenu(self.menubar)
        self.fileMenu.setObjectName("fileMenu")
        self.toolsMenu = QtWidgets.QMenu(self.menubar)
        self.toolsMenu.setObjectName("toolsMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setFloating(False)
        self.dockWidget.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeView = QtWidgets.QTreeView(self.dockWidgetContents)
        self.treeView.setMinimumSize(QtCore.QSize(785, 703))
        self.treeView.setObjectName("treeView")
        self.horizontalLayout.addWidget(self.treeView)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.fileOpenAction = QtWidgets.QAction(MainWindow)
        self.fileOpenAction.setObjectName("fileOpenAction")
        self.convertAction = QtWidgets.QAction(MainWindow)
        self.convertAction.setObjectName("convertAction")
        self.fileOpenActionTool = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/xuxuefeng/config/image/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fileOpenActionTool.setIcon(icon)
        self.fileOpenActionTool.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.fileOpenActionTool.setAutoRepeat(True)
        self.fileOpenActionTool.setVisible(True)
        self.fileOpenActionTool.setMenuRole(QtWidgets.QAction.TextHeuristicRole)
        self.fileOpenActionTool.setIconVisibleInMenu(False)
        self.fileOpenActionTool.setShortcutVisibleInContextMenu(True)
        self.fileOpenActionTool.setPriority(QtWidgets.QAction.NormalPriority)
        self.fileOpenActionTool.setObjectName("fileOpenActionTool")
        self.convertActionTool = QtWidgets.QAction(MainWindow)
        self.convertActionTool.setCheckable(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("C:/Users/xuxuefeng/config/image/convert.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.convertActionTool.setIcon(icon1)
        self.convertActionTool.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.convertActionTool.setAutoRepeat(True)
        self.convertActionTool.setVisible(True)
        self.convertActionTool.setMenuRole(QtWidgets.QAction.TextHeuristicRole)
        self.convertActionTool.setIconVisibleInMenu(False)
        self.convertActionTool.setShortcutVisibleInContextMenu(True)
        self.convertActionTool.setPriority(QtWidgets.QAction.NormalPriority)
        self.convertActionTool.setObjectName("convertActionTool")
        self.dockWidget.raise_()
        self.fileMenu.addAction(self.fileOpenAction)
        self.toolsMenu.addAction(self.convertAction)
        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.toolsMenu.menuAction())
        self.toolBar.addAction(self.fileOpenActionTool)
        self.toolBar.addAction(self.convertActionTool)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "模式产品读书器"))
        self.fileMenu.setTitle(_translate("MainWindow", "文件(F)"))
        self.toolsMenu.setTitle(_translate("MainWindow", "工具(T)"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.dockWidget.setWindowTitle(_translate("MainWindow", "文件列表"))
        self.fileOpenAction.setText(_translate("MainWindow", "打开"))
        self.fileOpenAction.setToolTip(_translate("MainWindow", "打开一个文件"))
        self.fileOpenAction.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.convertAction.setText(_translate("MainWindow", "格式转换"))
        self.convertAction.setToolTip(_translate("MainWindow", "不同格式数据之间相互转换"))
        self.fileOpenActionTool.setText(_translate("MainWindow", "打开"))
        self.convertActionTool.setText(_translate("MainWindow", "格式转换"))





