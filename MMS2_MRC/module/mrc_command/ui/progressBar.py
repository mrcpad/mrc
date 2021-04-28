# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 't4.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QBasicTimer
import sys
class Ui_FormProgressBar(QWidget):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(347, 271)
        self.form = Form
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(30, 70, 321, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(190, 140, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 140, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.pushButton_2.setEnabled(False)

        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.close)

        self.timer = QBasicTimer()
        self.step = 0


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "执行格式转换中"))
        self.pushButton.setText(_translate("Form", "取消"))
        self.pushButton_2.setText(_translate("Form", "完成"))


    def timerEvent(self, e):

        if self.step >= 100:
            self.timer.stop()
            self.pushButton_2.setEnabled(True)
            return
        self.step = self.step+1
        self.progressBar.setValue(self.step)

    def doAction(self, value):
        pass

        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(10, self)

    def exit(self):
        sys.exit(0)


    def close(self):
        self.form.close()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    form = QtWidgets.QDialog()
    ui = Ui_FormProgressBar()
    ui.setupUi(form)
    form.show()
    sys.exit(app.exec_())

