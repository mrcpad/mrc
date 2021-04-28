# -*- coding: UTF-8 -*-



from module.mrc_infrastructure.basecommand import BaseCommand

class QuitCmd(BaseCommand):
    '''
    退出程序
    '''

    def Init(self):
        import sys
        sys.exit(0)