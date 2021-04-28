#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: ??
@author: wufeng
@site: 
@software: PyCharm
@file: FtpUtil.py
@time: 2017/11/26 13:09
"""
from ftplib import FTP
'''
连接并登录 ftp
'''
def ftp_connect(host, port, username, password):
    ftp = FTP()
    ftp.connect(host=host, port=port)
    ftp.login(user=username, passwd=password)
    return ftp

'''
下载文件
'''
def down_load_file(host, port, username, password, remotepath, localpath):
    ftp = ftp_connect(host=host, port=port, username=username, password=password)
    buf_size = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fp.write, buf_size)
    ftp.set_debuglevel(0)
    fp.close()

'''
从本地上传文件
'''
def up_load_file(host, port, username, password, remotepath, localpath):
    print('start upload file .........')
    print("localpath" + localpath)
    print("remotepath" + remotepath)
    buf_size = 1024
    fp = open(localpath, 'rb')
    import os
    remotepaths = remotepath.split('/')
    print(remotepaths)
    ftp = ftp_connect(host=host, port=port, username=username, password=password)
    temp_remotepath = "/"
    for remote in remotepaths[3:len(remotepaths)]:

        try:
            ftp.cwd(remote)
            temp_remotepath = temp_remotepath + remote + os.sep
        except:
            ftp.mkd(remote)
            temp_remotepath = temp_remotepath + remote + os.sep
            ftp.cwd(remote)
    print('start upload file .........'+ 'STOR ' + temp_remotepath + os.path.basename(localpath))
    ftp.storbinary('STOR ' + temp_remotepath+ os.path.basename(localpath), fp, buf_size)
    fp.close()

