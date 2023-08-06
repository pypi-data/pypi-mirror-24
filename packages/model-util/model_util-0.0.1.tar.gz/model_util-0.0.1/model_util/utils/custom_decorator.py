#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED

import logging
from functools import wraps
import caijiajia.model_util.utils.log_util
from caijiajia.model_util.utils.conf_util import ConfUtil
from caijiajia.model_util.utils.param_parser import ParamParser


def params(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        params_list = args[1]
        checked_args = args[2]
        params_dict = ParamParser.parse(params_list, checked_args)
        return func(*args, params_dict=params_dict, **kwargs)

    return wrapper


def static_params(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        params_list = args[0]
        checked_args = args[1]
        params_dict = ParamParser.parse(params_list, checked_args)
        return func(*args, params_dict=params_dict, **kwargs)

    return wrapper


def conf(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(u'环境配置设置完毕...')
        return func(*args, **kwargs)

    return wrapper


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) == 0 or args[0].__class__.__name__[0].islower():
            class_name = func.func_code.co_filename
        else:
            class_name = args[0].__class__.__name__
        logging.info(u"%s开始执行%s方法..." % (class_name, func.func_name))
        result = func(*args, **kwargs)
        logging.info(u"%s结束执行%s方法..." % (class_name, func.func_name))
        return result

    return wrapper


def register_mapper(obj_type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            return map(obj_type._make, res)

        return wrapper

    return decorator
