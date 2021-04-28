# !/home/ynairport/python3/bin/python3
# !-*-coding:utf-8 -*-

# company hitec
# projectName ynjc
# by XXf at 
# describe 

'''
版本 ：v1.0.0
创建 ：xxf at 2019/03/22 11:09
更新内容 ：
subprocess库 执行shell命令
(1) call
执行命令，返回状态码(命令正常执行返回0，报错则返回1)
(2) check_call
执行命令，如果执行成功则返回状态码0，否则抛异常
(3) check_output
(4)subprocess.Popen(...)
用于执行复杂的系统命令执行命令，如果执行成功则返回执行结果，否则抛异常


版本 ：v1.0.1
更新 ：xxf at 2019/
更新内容 ：

'''

import subprocess as sp


def call(cmd):
    '''
    执行命令，返回状态码(命令正常执行返回0，报错则返回1)
    :return:
    '''
    result=sp.call(cmd)
    return result


def check_call(cmd,shell=True):
    '''
    执行命令，如果执行成功则返回状态码0，否则抛异常
    :return:
    '''

    return sp.check_call(cmd,shell)

def check_output(cmd):
    '''
    执行命令，如果执行成功则返回执行结果，否则抛异常
    :return:
    '''
    try:
        return sp.check_output(cmd)
    except:
        #print "subprocess check_output error "
        return None


def po_pon(cmd,shell,cwd):
    '''
    在cwd目录下执行cmd命令
    :param cmd:
    :param shell:
    :param cwd:
    :return:
    '''
    obj=sp.Popen(cmd,shell=shell,cwd=cwd)
    # cmd_output=obj.stdout.mrc_app()
    return obj




