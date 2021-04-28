# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 't2.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import sys
sys.path.append(r'D:\workspace09\MMS2_MRC\module\algorithm\src')
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from module.mrc_command.ui.progressBar import Ui_FormProgressBar
from module.algorithm.src.startConvert import ffcstartProgram


class Ui_Form(QWidget):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(644, 294)
        self.form = Form
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(11, 47, 195, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(11, 118, 105, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(11, 182, 75, 16))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(540, 47, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(540, 182, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(213, 50, 281, 21))
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(213, 185, 281, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(180, 240, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(400, 240, 93, 28))
        self.pushButton_4.setObjectName("pushButton_4")


        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(213, 118, 271, 21))
        self.comboBox.setObjectName("comboBox")
        #self.comboBox.activated['A','B'].connect(self.BrushPhoto)
        self.comboBox.addItems(['nh','hn','nm','mn','hm','mh'])
        self.comboBox.activated[str].connect(self.BrushPhoto)




        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.pushButton.clicked.connect(self.openfile)
        self.pushButton_3.clicked.connect(self.opendir)

        self.pushButton_4.clicked.connect(self.exit)
        self.pushButton_2.clicked.connect(self.okButton)



    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "格式转换"))
        self.label.setText(_translate("Form", "选择多单个文件或多个文件："))
        self.label_2.setText(_translate("Form", "转换目标格式："))
        self.label_3.setText(_translate("Form", "另存目录："))
        self.pushButton.setText(_translate("Form", "选择"))
        self.pushButton_3.setText(_translate("Form", "选择"))
        self.pushButton_2.setText(_translate("Form", "确定"))
        self.pushButton_4.setText(_translate("Form", "取消"))

    def openfile(self):
        #openfile_name = QFileDialog.getOpenFileName(self,'选择文件','','files(*.nc , *.hdf ,*.GRB, *.grb2)')
        openfile_name = QFileDialog.getOpenFileName(self, "选取文件", "D:\\", "All Files (*);;Binary files(*.nc , *.hdf ,*.GRB, *.grb2)")
        print(openfile_name)
        self.lineEdit.setText(openfile_name[0])

    def opendir(self):
        opendir_name = QtWidgets.QFileDialog.getExistingDirectory(self,"浏览","D:\\")

        self.lineEdit_3.setText(opendir_name)

    def close(self):
        import sys
        sys.exit(0)

    def exit(self):
        self.form.close()


    def BrushPhoto(self):
        self.comboBoxcurrentText = self.comboBox.currentText()
    def okButton(self):
        ft = self.comboBox.currentText()
        src = self.lineEdit.text()
        dst = self.lineEdit_3.text()

        ffcstartProgram.convert(ft,'vn', src, dst)
        self.form.hide()
        form = QtWidgets.QDialog()
        ui = Ui_FormProgressBar()
        ui.setupUi(form)
        ui.doAction('')
        form.show()
        form.exec_()
        self.form.close()

        print(self.lineEdit.text())
        print(self.lineEdit_3.text())
        print(self.comboBox.currentText())




class MyWindow(QMainWindow, Ui_Form):

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)



if __name__ == '__main__':
    '''app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())'''
    app = QApplication(sys.argv)
    form = QtWidgets.QDialog()
    ui = Ui_Form()
    ui.setupUi(form)
    form.show()
    sys.exit(app.exec_())




