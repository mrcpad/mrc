# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 't5.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import sys
sys.path.append(r'D:\workspace09\MMS2_MRC\module\algorithm\src')
from module.algorithm.src.startConvert import ffcstartProgram
from PyQt5.QtWidgets import QWidget,QFileDialog,QMessageBox,QDialog,QLineEdit,QApplication
from module.mrc_app.mainfrom import *
import re
import os
from PyQt5.QtCore import QThread, pyqtSignal
class Ui_FormChooseFile(QWidget):

    # def __init__(self,parent,flag):
    #     print(1)
    #     #super(ChildWindow, self).__init__(parent=parent)
    #
    #     self.setupUi(parent, flag)


    def setupUi(self, Form, flag):
        Form.setObjectName("Form")
        Form.resize(761, 294)
        Form.setFixedSize(Form.width(), Form.height())
        self.flag = flag
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
        self.pushButton.setGeometry(QtCore.QRect(540, 47, 71, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(540, 182, 141, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        # self.lineEdit = QtWidgets.QLineEdit(Form)
        # self.lineEdit.setGeometry(QtCore.QRect(213, 50, 281, 21))
        # self.lineEdit.setObjectName("lineEdit")

        self.lineEdit = LineEditEx(Form)
        self.lineEdit.setGeometry(QtCore.QRect(213, 50, 281, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText('Please directory  already exists')



        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(213, 118, 281, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboxdict = {'nc2hdf':'netCDF??????HDF','hdf2nc':'HDF??????netCDF','nc2m4':'netCDF??????Micaps4','m42nc':'Micaps4??????netCDF','m42hdf':'Micaps4??????HDF','hdf2m4':'HDF??????Micaps4'}
        self.ftdict = {'netCDF??????HDF':'nh','HDF??????netCDF':'hn','netCDF??????Micaps4':'nm','Micaps4??????netCDF':'mn','Micaps4??????HDF':'mh','HDF??????Micaps4':'hm',}
        #self.comboBox.addItems(['nh', 'hn', 'nm', 'mn', 'hm', 'mh'])
        #print(comboxdict[self.flag])
        #self.comboBox.addItems([comboxdict[self.flag]])
        #self.comboBox.addItem('netCDF??????HDF')
        self.comboBox.addItems(list(self.comboxdict.values()))
        #self.comboBox.setCurrentIndex(2)
        if self.flag != '':
            self.comboBox.setCurrentText(self.comboxdict[self.flag])
        self.comboBox.activated[str].connect(self.BrushPhoto)

        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(213, 185, 281, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setPlaceholderText('Please directory  already exists')
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(180, 240, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(440, 240, 93, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(620, 47, 71, 28))
        self.pushButton_5.setObjectName("pushButton_5")



        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.pushButton.clicked.connect(self.openfile)
        self.pushButton_3.clicked.connect(self.opendir)

        self.pushButton_4.clicked.connect(self.exit)
        self.pushButton_2.clicked.connect(self.okButton)
        self.pushButton_5.clicked.connect(self.opendirfile)




    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "????????????"))
        self.label.setText(_translate("Form", "????????????????????????????????????"))
        self.label_2.setText(_translate("Form", "?????????????????????"))
        self.label_3.setText(_translate("Form", "???????????????"))
        self.pushButton.setText(_translate("Form", "????????????"))
        self.pushButton_3.setText(_translate("Form", "??????"))
        self.pushButton_2.setText(_translate("Form", "??????"))
        self.pushButton_4.setText(_translate("Form", "??????"))
        self.pushButton_5.setText(_translate("Form", "????????????"))



    def openfile(self):
        #openfile_name = QFileDialog.getOpenFileNames(self, "????????????", "D:\\", "All Files (*);;Binary files(*.nc , *.hdf ,*.GRB, *.grb2)")
        openfile_name = QFileDialog.getOpenFileNames(self, "????????????", "","Binary files(*.nc , *.hdf ,*.GRB, *.grb2);;All Files (*)")

        self.lineEdit.setText(','.join(openfile_name[0]))

    def opendir(self):
        opendir_name = QtWidgets.QFileDialog.getExistingDirectory(self,"??????","")

        self.lineEdit_3.setText(opendir_name)

    def opendirfile(self):
        opendir_name = QtWidgets.QFileDialog.getExistingDirectory(self,"??????","")

        self.lineEdit.setText(opendir_name)

    def close(self):
        import sys
        sys.exit(0)

    def exit(self):
        self.form.close()


    def BrushPhoto(self):

        self.comboBoxcurrentText = self.comboBox.currentText()

    def okButton(self,event):
        try:
            ft = self.ftdict[self.comboBox.currentText()]
            src = self.lineEdit.text()
            dst = self.lineEdit_3.text()
            regex_str = ".*?([\u4E00-\u9FA5]+).*?"
            if src == '':
                QMessageBox.warning(self, '??????', '??????????????????????????????',QMessageBox.Yes | QMessageBox.No)
            else:
                srcpath = src.split(',')
                if len(srcpath) == 1:
                    if not os.path.exists(srcpath[0]):
                        QMessageBox.critical(self, '??????', '??????????????????!',QMessageBox.Yes | QMessageBox.No)
                    else:
                        match_src = re.findall(regex_str, srcpath[0])
                        if match_src:
                            QMessageBox.warning(self, '??????', '??????NetCDF??????HDF???????????????????????????!', QMessageBox.Yes | QMessageBox.No)
                        else:
                            if dst == '':
                                QMessageBox.warning(self, '??????', '??????????????????????????????',QMessageBox.Yes | QMessageBox.No)
                            else:
                                match_dst = re.findall(regex_str, dst)
                                if match_dst:
                                    QMessageBox.warning(self, '??????', '??????NetCDF??????HDF???????????????????????????!',QMessageBox.Yes | QMessageBox.No)
                                else:
                                    c = ffcstartProgram.convert(ft, 'VAR000', src, dst)
                                    if c == 0:
                                        self.form.hide()


                                    # form = QtWidgets.QDialog()
                                    # ui = Ui_FormProgressBar()
                                    # ui.setupUi(form)
                                    # ui.doAction('')
                                    # form.show()
                                    # form.exec_()
                                    #self.form.close()

                elif len(srcpath) > 1:
                    notexistpath = []
                    for path in srcpath:
                        if not os.path.exists(path):
                            notexistpath.append(path)
                    if notexistpath:
                        QMessageBox.critical(self, '??????', '??????????????????:'+','.join(notexistpath), QMessageBox.Yes | QMessageBox.No)
                    else:
                        match_src = re.findall(regex_str, src)
                        if match_src:
                            QMessageBox.warning(self, '??????', '??????NetCDF??????HDF???????????????????????????!', QMessageBox.Yes | QMessageBox.No)
                        else:
                            if dst == '':
                                QMessageBox.warning(self, '??????', '??????????????????????????????',QMessageBox.Yes | QMessageBox.No)

                            else:
                                match_obj = re.findall(regex_str, dst)
                                if match_obj:
                                    QMessageBox.warning(self, '??????', '??????NetCDF??????HDF???????????????????????????!',QMessageBox.Yes | QMessageBox.No)
                                else:
                                    c = ffcstartProgram.convert(ft, 'VAR000', src, dst)
                                    if c == 0:
                                        self.form.hide()

                                    # form = QtWidgets.QDialog()
                                    # ui = Ui_FormProgressBar()
                                    # ui.setupUi(form)
                                    # ui.doAction('')
                                    # form.show()
                                    # form.exec_()
                                    # self.form.close()






            '''reply = QMessageBox.warning(self,
                                        "???????????????",
                                        "?????????????????????",
                                        QMessageBox.Yes | QMessageBox.No)'''
            #self.echo(self, reply)
        except Exception as arge:
            print(arge)
            QMessageBox.warning(self, '??????', '??????????????????,?????????????????????!',QMessageBox.Yes | QMessageBox.No)

        '''ffcstartProgram.convert(ft,'VAR000', src, dst)
        self.form.hide()
        form = QtWidgets.QDialog()
        ui = Ui_FormProgressBar()
        ui.setupUi(form)
        ui.doAction('')
        form.show()
        form.exec_()
        self.form.close()'''

        #print(self.lineEdit.text())
        #print(self.lineEdit_3.text())
        #print(self.comboBox.currentText())
    def echo(self, value):
        '''????????????????????????'''
        QMessageBox.information(self, "?????????", "?????????{}\n\ntype: {}".format(value, type(value)),QMessageBox.Yes | QMessageBox.No)




class ParentWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)#QMainWindow????????????
        self.main_ui = MainFrom()#?????????????????????


class ChildWindow(QDialog):

    def __init__(self, parent, flag):
        super(ChildWindow, self).__init__(parent=parent)

        #QDialog.__init__(self) ?????????????????????
        self.child = Ui_FormChooseFile()#?????????????????????
        self.child.setupUi(self, flag)



class LineEditEx(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(None, parent)
        self.setGeometry(50, 50, 100, 20)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)  # ?????????????????????

    def dragEnterEvent(self, QDragEnterEvent):
        e = QDragEnterEvent  # type:QDragEnterEvent

        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.setText(e.mimeData().text().replace('file:///','')) #??????????????????ignore ???False ?????????????????????




class RunThread(QThread):
    my_signal = pyqtSignal(int)

    def __init__(self):
        super(RunThread, self).__init__()

    def run(self):
        workChildWindow()

def workChildWindow(mainWindow, flag):
    ui = ChildWindow(mainWindow, flag)
    ui.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #form = QtWidgets.QDialog()
    #ui = Ui_FormChooseFile()
    #ui.setupUi(form)
    #form.show()
    child = ChildWindow()
    child.show()
    sys.exit(app.exec_())

    '''app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())'''


    '''app = QApplication(sys.argv)
    form = QtWidgets.QDialog()
    ui = Ui_FormChooseFile()
    ui.setupUi(form)
    form.show()
    sys.exit(app.exec_())'''