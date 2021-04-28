# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from PyQt5 import QtCore, QtGui, QtWidgets

class LoadingGifWin(QWidget):
    def __init__(self, parent=None):
        super(LoadingGifWin, self).__init__(parent)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        #Form.resize(347, 271)
        self.form = Form
        self.label = QLabel(Form)
        self.label.setObjectName("label")
        # self.label.setGeometry(QtCore.QRect(0, 0, 300, 300))
        Form.setAttribute(Qt.WA_TranslucentBackground)
        Form.setFixedSize(300, 300)
        Form.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.movie = QMovie(r"D:\workspace11\mrc\test\gif\wait.gif")
        self.label.setMovie(self.movie)
        self.movie.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = QtWidgets.QDialog()
    ui = LoadingGifWin()
    ui.setupUi(form)
    form.show()
    sys.exit(app.exec_())

