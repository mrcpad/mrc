# -*- coding: UTF-8 -*-



from module.mrc_infrastructure.basecommand import BaseCommand

class OneRemoveCmd(BaseCommand):
    '''
    退出程序
    '''

    def Init(self):
        pass
        self.treeWidget.OneremoveTree()


class RemoveCmd(BaseCommand):
    '''
    退出程序
    '''

    def Init(self):
        pass
        self.treeWidget.removeTree()