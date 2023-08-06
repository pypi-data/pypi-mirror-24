#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED

from caijiajia.model_util.utils.param_parser import InputArgument
from caijiajia.model_util.utils.custom_decorator import params
from caijiajia.model_util.utils.custom_decorator import conf
from caijiajia.model_util.utils.custom_decorator import log
from caijiajia.model_util.service.base_service import BaseService


class BaseJob(object):
    """
    Job基础类
    """

    def __init__(self):
        pass

    @params
    @conf
    @log
    def run(self, *args, **kwargs):
        """
        主函数, 获取配置, 初始化log, 调用base_service的run方法
        :param kwargs:
        :return:
        """
        params_dict = kwargs['params_dict']

        self.reset_arguments(params_dict)
        # execute_class_list = kwargs['execute_class_list']

        run_time = params_dict[InputArgument.run_time[0]]

        if run_time == 'current':
            self.run_one_day(*args, **kwargs)
        else:
            self.run_history(*args, **kwargs)

    @log
    def run_one_day(self, *args, **kwargs):
        """
        主函数, 获取配置, 初始化log, 调用base_service的run方法
        :param kwargs:
        :return:
        """
        params_dict = kwargs['params_dict']
        execute_class_list = kwargs['execute_class_list']
        for execute_class in execute_class_list:
            if type(execute_class) != type(BaseService):
                raise Exception(u'调用服务类型错误!')

            result = execute_class(params_dict).run()

            if result is not None and not result:
                break

    @log
    def run_history(self, *args, **kwargs):
        """
        主函数, 执行历史任务, 获取配置, 初始化log, 调用base_service的run_history的方法
        :param args:
        :param kwargs:
        :return:
        """
        params_dict = kwargs['params_dict']
        execute_class_list = kwargs['execute_class_list']

        for execute_class in execute_class_list:
            if type(execute_class) != type(BaseService):
                raise Exception(u'调用服务类型错误!')

            result = execute_class(params_dict).run_history()

            if result is not None and not result:
                break

    def reset_arguments(self, params_dict):
        """
        提供可重置输入参数的抽象方法
        :param params_dict:
        :return:
        """
        pass
