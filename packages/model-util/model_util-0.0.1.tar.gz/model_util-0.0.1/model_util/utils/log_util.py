#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED


import logging
import logging.config
import logging.handlers
import os
import urllib2
from caijiajia.model_util.utils.log_handlers.syslog_handler import SyslogHandler


class LogConfig(object):
    @staticmethod
    def get_app_name():
        return 'strategybacktest'

    @staticmethod
    def get_server_ip():
        try:
            server_ip = urllib2.urlopen("http://169.254.169.254/latest/meta-data/local-ipv4", timeout=2).read()
        except urllib2.URLError, e:
            server_ip = 'localhost'
        return server_ip


dir_home = os.path.split(os.path.realpath(__file__))[0][:-26]
try:
    server_ip = urllib2.urlopen("http://169.254.169.254/latest/meta-data/local-ipv4", timeout=2).read()
except urllib2.URLError, e:
    server_ip = 'localhost'
logging.config.fileConfig(dir_home + "logging.conf")

# 重置format参数
log_format = "%(asctime)-15s [strategybacktest|server_ip|0000] [%(threadName)s] [%(module)s] [%(levelname)s] [%(lineno)d] - %(message)s".replace("server_ip", server_ip)
for handler in logging.getLogger('').handlers:
    handler.formatter = logging.Formatter(log_format)

# 重置文件输出的文件路径
file_handler = logging.handlers.RotatingFileHandler(filename=os.path.join(dir_home, 'strategybacktest.log'), maxBytes=logging.getLogger('').handlers[1].maxBytes,
                                                    backupCount=logging.getLogger('').handlers[1].backupCount, encoding=logging.getLogger('').handlers[1].encoding)
file_handler.setFormatter(logging.Formatter(log_format))
file_handler.setLevel(logging.INFO)
logging.getLogger('').handlers[1] = file_handler

# 重置server的Ip地址
syslog_handler = SyslogHandler(address=(server_ip, 5140), facility=logging.getLogger('').handlers[2].facility, socktype=logging.getLogger('').handlers[2].socktype)
syslog_handler.setFormatter(logging.Formatter(log_format))
syslog_handler.setLevel(logging.INFO)
logging.getLogger('').handlers[2] = syslog_handler
