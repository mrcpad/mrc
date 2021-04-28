# -*- coding: UTF-8 -*-

from module.algorithm.src.startConvert import ffcstart
import os
from PyQt5.QtWidgets import QWidget, QMainWindow,QMessageBox,QFileDialog
import shutil
import re
from PyQt5.QtCore import QThread, pyqtSignal


class SaveFileCmd(QWidget):
    def __init__(self,fileName):
        super(SaveFileCmd, self).__init__()
        self.fileName = fileName
    def Init(self):
        try:

            self.infoFlag = 0
            self.FileCmd = {'NCHDF':'nh','NCTXT':'nm','NCGRB':'ng','NCGRB2':'ng','HDFNC':'hn','HDFTXT':'hm','GRBNC':'gn','GRB2NC':'gn',
                            'GRBHDF':'gh','GRB2HDF':'gh','GRBTXT':'gm','GRB2TXT':'gm','000NC':'mn','000HDF':'mh'}
            files = self.OpenFile()
            #wt = WorkThread()
            #wt.start()
            if files:
                if files[0]:
                    regex_str = ".*?([\u4E00-\u9FA5]+).*?"
                    match_obj = re.findall(regex_str, files[0])
                    if match_obj:
                        QMessageBox.warning(self, '警告', '您的NetCDF或者HDF文件路径中包含中文,切换英文路径重试!',
                                            QMessageBox.Yes | QMessageBox.No)
                    else:
                        if self.infoFlag == 0:
                            self.infoFlag = 1

                            srcFileName = os.path.split(self.fileName)[1]
                            srcExtent = os.path.splitext(srcFileName)[1].replace('.','')
                            if srcExtent.isdigit() and len(srcExtent.replace('.', '')) == 3:
                                srcExtent = '000'
                            dstExtent = files[1].split('.')[1]
                            convertMode = srcExtent + dstExtent.replace(')','')
                            #print(os.path.getsize(self.currentText))
                            mode = self.FileCmd.get(convertMode.upper(),'')

                            if mode:
                                #t = threading.Thread(target=ffcstart.convert, args=(mode, 'VAR000', self.fileName, files[0]))
                                #t.start()
                                ffcstart.convert(mode, 'VAR000', self.fileName, files[0])
                            else:
                                shutil.copy(self.fileName, files[0])
        except Exception as arge:
            print(arge)
            QMessageBox.warning(self, '警告', '文件转化失败,请检查文件格式!',QMessageBox.Yes | QMessageBox.No)











    def OpenFile(self):

        try:
            files = QFileDialog.getSaveFileName(self, "文件另存为...", "/" + self.fileName,"NetCDF文件(*.nc);;HDF文件(*.hdf);;Micaps文件(*.txt)")
            return files
        except Exception as arg:
            print(arg)
            QMessageBox.warning(self, '警告', '另存文件异常！', QMessageBox.Yes, QMessageBox.No)


class WorkThread(QThread):
    trigger = pyqtSignal()

    def __int__(self):
        super(WorkThread, self).__init__()

    def run(self):
        pass





