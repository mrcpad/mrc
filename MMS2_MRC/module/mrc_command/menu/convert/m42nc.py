# -*- coding: UTF-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from module.mrc_infrastructure.basecommand import BaseCommand
import sys
sys.path.append(r'D:\workspace09\MMS2_MRC\module\algorithm\src')
from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtWidgets import *
from module.mrc_command.ui.progressBar import Ui_FormProgressBar
from module.algorithm.src.startConvert import ffcstartProgram
from module.mrc_command.ui.newChooseFile import ChildWindow

class M42NCCmd(BaseCommand):


    def Init(self):

        ui = ChildWindow(self.mainWindow, 'm42nc')
        #print(self.menubar)
        ui.exec()







