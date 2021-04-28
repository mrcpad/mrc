# -*- coding: UTF-8 -*-



from module.mrc_infrastructure.basecommand import BaseCommand
from module.mrc_command.ui.newChooseFile import ChildWindow

class ConvertCmd(BaseCommand):
    '''
    退出程序
    '''

    def Init(self):
        ui = ChildWindow(self.mainWindow, '')
        ui.exec()