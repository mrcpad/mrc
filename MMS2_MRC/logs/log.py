# !-*-coding:utf-8 -*-

# describe loggering module
'''
版本 ：v1.0.0
创建 ：xxf
更新内容 ：
日志类


版本 ：v1.0.1
创建 ：xxf
at 2019/03/01 10:14
更新内容 ：
增加错误日志单独输出到日志

'''
import os
import logging
import time
logpath = os.path.join(os.path.abspath('.'), 'log')
if not os.path.exists(logpath):
        os.makedirs(logpath)
        log_path = logpath
error_path = logpath + '/' + 'errorlogs'
if not os.path.exists(error_path):
    os.makedirs(error_path)
log_path = logpath

error_path = log_path + '/' + 'errorlogs'

fh = None
eh = None

def get_log(logger_name):
    global fh
    global eh
    all_log_path = log_path
    error_log_path = error_path

    # 创建一个logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # 设置日志存放路径，日志文件名
    # 获取本地时间，转换为设置的格式
    rq = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    # getpath.py文件拼接日志存放路径
    # all_log_path = getpath.getdirectory(getpath.DirectoryType.LOGS)
    # error_log_path = getpath.getdirectory(getpath.DirectoryType.ERRORLOGS)
    # 设置日志文件名
    all_log_name = all_log_path + '/' + rq + '.log'

    error_log_name = error_log_path + '/' + rq + '.log'

    # 创建handler
    # 创建一个handler写入所有日志
    fh = logging.FileHandler(all_log_name)
    fh.setLevel(logging.INFO)
    # 创建一个handler写入错误日志
    eh = logging.FileHandler(error_log_name)
    eh.setLevel(logging.ERROR)
    # 创建一个handler输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # 定义日志输出格式
    # 以时间-日志器名称-日志级别-日志内容的形式展示
    all_log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # 以时间-日志器名称-日志级别-文件名-函数行号-错误内容
    error_log_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(module)s  - %(lineno)s - %(message)s')
    # 将定义好的输出形式添加到handler
    fh.setFormatter(all_log_formatter)
    ch.setFormatter(all_log_formatter)
    eh.setFormatter(error_log_formatter)

    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(eh)
    logger.addHandler(ch)
    return logger


logger = get_log("mylog")
