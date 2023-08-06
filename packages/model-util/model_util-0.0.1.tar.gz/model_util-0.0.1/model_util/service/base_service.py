#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED

from abc import abstractmethod
from caijiajia.model_util.utils.custom_decorator import log


class BaseService(object):
    """
    服务基础类, 主要需要实现run_detail, run_history_detail两个方法
    """

    def __init__(self, params_dict):
        self.params_dict = params_dict

    @log
    def run(self, **params):
        """
        服务主函数, 支持执行某一天的数据操作
        :param params:
        :return:
        """
        return self.run_detail(**params)

    @log
    def run_history(self, **params):
        """
        服务主函数, 支持执行某一段历史的数据操作
        :param params:
        :return:
        """
        return self.run_history_detail(**params)

    @abstractmethod
    def run_detail(self, **params):
        pass

    @abstractmethod
    def run_history_detail(self, **params):
        pass
