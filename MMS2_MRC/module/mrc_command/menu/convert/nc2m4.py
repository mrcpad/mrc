# -*- coding: UTF-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from module.mrc_infrastructure.basecommand import BaseCommand
import sys
sys.path.append(r'D:\workspace09\MMS2_MRC\module\algorithm\src')
from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtWidgets import *

from module.mrc_command.ui.newChooseFile import ChildWindow
class NC2M4Cmd(BaseCommand):


    def Init(self):

        ui = ChildWindow(self.mainWindow, 'nc2m4')
        ui.exec()






