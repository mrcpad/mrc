
# -*- coding: UTF-8 -*-



from module.mrc_infrastructure.basecommand import BaseCommand
from module.mrc_core.actionQ import ActionQ
from module.algorithm.src.startConvert import ffcstart
import os
from PyQt5.QtWidgets import QWidget, QMainWindow,QMessageBox,QFileDialog,QApplication
import shutil
import re

from PyQt5.QtCore import QThread, pyqtSignal
import threading


class SaveFileCmd(BaseCommand,QWidget):
    '''
    打开文件命令
    '''

    def Init(self):
        if not isinstance(self.action, ActionQ) or not isinstance(self.mainWindow, QMainWindow):
            return None

        self.infoFlag = 0
        self.FileCmd = {'NCHDF':'nh','NCTXT':'nm','NCGRB':'ng','NCGRB2':'ng','HDFNC':'hn','HDFTXT':'hm','GRBNC':'gn','GRB2NC':'gn',
                        'GRBHDF':'gh','GRB2HDF':'gh','GRBTXT':'gm','GRB2TXT':'gm','000NC':'mn','000HDF':'mh'}
        files = self.OpenFile()
        #self.wt = RunThread(files, self.currentText)
        #self.wt.start()


        try:


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

                            srcFileName = os.path.split(self.currentText)[1]
                            srcExtent = os.path.splitext(srcFileName)[1].replace('.','')
                            if srcExtent.isdigit() and len(srcExtent.replace('.', '')) == 3:
                                srcExtent = '000'
                            dstExtent = files[1].split('.')[1]
                            convertMode = srcExtent + dstExtent.replace(')','')
                            #print(os.path.getsize(self.currentText))
                            mode = self.FileCmd.get(convertMode.upper(),'')

                            if mode:

                                #t = threading.Thread(target=ffcstart.convert, args=(mode, 'VAR000', self.currentText, files[0]))
                                #t.start()
                                ffcstart.convert(mode, 'VAR000', self.currentText, files[0])
                            else:
                                shutil.copy(self.currentText, files[0])
        except Exception as arge:
            print(arge)
            QMessageBox.warning(self, '警告', '文件转化失败,请检查文件格式!', QMessageBox.Yes | QMessageBox.No)











    def OpenFile(self):
        if not isinstance(self.action, ActionQ):
            message = QMessageBox(title="错误", text="执行错误")
            message.show()
            return

        try:
            if self.treeWidget.currentItem():
                src = self.treeWidget.currentItem().text(2)
                self.currentText = src
                (filepath, tempfilename) = os.path.split(src)
                (filename, extension) = os.path.splitext(tempfilename)
                #files = QFileDialog.getSaveFileName(self.mainWindow, "文件另存为...", "/" + filename,"*.nc ;; *.hdf ;;*.GRB;; *.grb2;;*.txt")
                files = QFileDialog.getSaveFileName(self.mainWindow, "文件另存为...", "/" + filename,"NetCDF文件(*.nc);;HDF文件(*.hdf);;Micaps文件(*.txt)")
            else:
                if self.treeWidget.files:
                    self.currentText = self.treeWidget.files[0]
                    (filepath, tempfilename) = os.path.split(self.treeWidget.files[0])
                    (filename, extension) = os.path.splitext(tempfilename)
                    #files = QFileDialog.getSaveFileName(self.mainWindow, "文件另存为...", "/" + filename,"*.nc ;; *.hdf ;;*.GRB;; *.grb2;;*.txt")
                    files = QFileDialog.getSaveFileName(self.mainWindow, "文件另存为...", "/" + filename,
                                                        "NetCDF文件(*.nc);;HDF文件(*.hdf);;Micaps文件(*.txt)")
                else:
                    reply = QMessageBox.warning(self, '警告', '请先打开文件，然后再执行另存功能.',
                                                QMessageBox.Yes | QMessageBox.No)

                    if reply == QMessageBox.Yes:
                        return
                    else:
                        return



            return files
        except Exception as arg:
            print(arg)
            QMessageBox.warning(self, '警告', '另存文件异常,请检查文件！', QMessageBox.Yes, QMessageBox.No)
class RunThread(QThread):
    my_signal = pyqtSignal(int)
    p = 0

    def __init__(self,sfile, current):
        super(RunThread, self).__init__()
        self.sfile = sfile
        self.currentText = current

    def run(self):
        sf = ThreadSaveFile(self.sfile, self.currentText)
        sf.savefile()


class ThreadSaveFile(QWidget):
    def __init__(self, files, current):
        super(ThreadSaveFile, self).__init__()
        self.files = files
        self.currentText = current
        self.saveinit()
    def saveinit(self):
        self.infoFlag = 0
        self.FileCmd = {'NCHDF': 'nh', 'NCTXT': 'nm', 'NCGRB': 'ng', 'NCGRB2': 'ng', 'HDFNC': 'hn', 'HDFTXT': 'hm',
                        'GRBNC': 'gn', 'GRB2NC': 'gn',
                        'GRBHDF': 'gh', 'GRB2HDF': 'gh', 'GRBTXT': 'gm', 'GRB2TXT': 'gm', '000NC': 'mn', '000HDF': 'mh'}


    def savefile(self):
        try:
            if self.files:
                if self.files[0]:
                    regex_str = ".*?([\u4E00-\u9FA5]+).*?"
                    match_obj = re.findall(regex_str, self.files[0])
                    if match_obj:
                        QMessageBox.warning(self, '警告', '您的NetCDF或者HDF文件路径中包含中文,切换英文路径重试!',
                                            QMessageBox.Yes | QMessageBox.No)
                    else:
                        if self.infoFlag == 0:
                            self.infoFlag = 1

                            srcFileName = os.path.split(self.currentText)[1]
                            srcExtent = os.path.splitext(srcFileName)[1].replace('.', '')
                            if srcExtent.isdigit() and len(srcExtent.replace('.', '')) == 3:
                                srcExtent = '000'
                            dstExtent = self.files[1].split('.')[1]
                            convertMode = srcExtent + dstExtent.replace(')', '')
                            # print(os.path.getsize(self.currentText))
                            mode = self.FileCmd.get(convertMode.upper(), '')

                            if mode:
                                # t = threading.Thread(target=ffcstart.convert, args=(mode, 'VAR000', self.currentText, files[0]))
                                # t.start()
                                ffcstart.convert(mode, 'VAR000', self.currentText, self.files[0])
                            else:
                                shutil.copy(self.currentText, self.files[0])
        except Exception as arge:
            print(arge)




