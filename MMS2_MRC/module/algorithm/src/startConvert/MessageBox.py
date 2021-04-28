# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMessageBox,QApplication,QWidget
import sys

class MyMessageBox(QMessageBox):
    def __init__(self,parent=None):
        super(MyMessageBox, self).__init__(parent)



    def mrcinfo(self,msg=''):
        reply = self.information(self, '运行提示',msg,QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            return 0
        else:
            return 1

    def mrcwarning(self, msg=''):
        reply = self.warning(self, '警告', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            return 0
        else:
            return 1

    def mrccritical(self,msg=''):
        reply = self.critical(self, '错误', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            return 0
        else:
            return 1
    def mrcquestion(self,msg=''):
        reply = self.question(self, '标题', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            return 0
        else:
            return 1
if __name__ == '__main__':
    app=QApplication(sys.argv)
    myshow=MyMessageBox()
    myshow.mrcinfo(msg='ddddddddd')
    myshow.show()
    sys.exit(app.exec_())