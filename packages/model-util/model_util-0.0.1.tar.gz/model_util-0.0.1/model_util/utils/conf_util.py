#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED

import os


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class Conf(Singleton):
    def __init__(self):
        dir_home = os.path.split(os.path.realpath(__file__))[0][:-26]
        self.props = Conf.load_properties(dir_home + 'spring-config.properties')

    @staticmethod
    def load_properties(filepath, sep='=', comment_char='#'):
        """
        Read the file passed as parameter as a properties file.
        """
        props = {}
        with open(filepath, "rt") as f:
            for line in f:
                l = line.strip()
                if l and not l.startswith(comment_char):
                    key_value = l.split(sep)
                    key = key_value[0].strip()
                    value = sep.join(key_value[1:]).strip().strip('"')
                    props[key] = value
        return props


DB_WIND = 'wind'
DB_PRIVATE_BANK_MODEL = 'private_bank_model'
DB_STRATEGY_BACKTEST = 'strategy_backtest'
CHARSET = 'utf8'


class ConfUtil(object):
    conf = Conf()

    @staticmethod
    def get_wind_db_conf():
        address = ConfUtil.conf.props['mysql.address.wind']
        user = ConfUtil.conf.props['mysql.username.wind']
        password = ConfUtil.conf.props['mysql.password.wind']
        host = address.split(':')[0]
        port = int(address.split(':')[1])
        return host, user, password, DB_WIND, CHARSET, port

    @staticmethod
    def get_pbm_db_conf():
        address = ConfUtil.conf.props['mysql.address.privatebankmodel']
        user = ConfUtil.conf.props['mysql.username.privatebankmodel']
        password = ConfUtil.conf.props['mysql.password.privatebankmodel']
        host = address.split(':')[0]
        port = int(address.split(':')[1])
        return host, user, password, DB_PRIVATE_BANK_MODEL, CHARSET, port

    @staticmethod
    def get_strategybacktest_db_conf():
        address = ConfUtil.conf.props['mysql.address.strategybacktest']
        user = ConfUtil.conf.props['mysql.username.strategybacktest']
        password = ConfUtil.conf.props['mysql.password.strategybacktest']
        host = address.split(':')[0]
        port = int(address.split(':')[1])
        return host, user, password, DB_STRATEGY_BACKTEST, CHARSET, port
