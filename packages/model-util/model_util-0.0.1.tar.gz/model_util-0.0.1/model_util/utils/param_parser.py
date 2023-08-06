#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED

import datetime


class InputArgument(object):
    """
    输入参数枚举, 格式(参数名,描述,默认值)
    如无默认值, None
    """
    private_bank_model_db_type = ('pbm_db_type', "-pbm_db_type: private_bank_model database type, 'prod' or 'test', default value: 'prod'; \n", 'prod')
    strategy_backtest_db_type = ('sbt_db_type', "-sbt_db_type: strategy_database_type', 'prod' or 'test', default value: 'prod'; \n", 'prod')
    wind_db_type = ('wind_db_type', "-wind_db_type: wind database type, 'prod' or 'test', default value: 'prod'; \n", 'prod')
    date = ('date', "-date: run date, default value: <today>; \n", datetime.date.today().strftime('%Y-%m-%d'))
    op_type = ('op_type', "-op_type: operation type, immediately running or running controlled by code, 'prod' or 'test', default value: 'prod'; \n", 'prod')
    from_date = ('from_date', "-from_date: start date of the data, default value: yesterday; \n", (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d"))
    to_date = ('to_date', "-to_date: end date of the data, default value: today; \n", datetime.date.today().strftime("%Y-%m-%d"))
    run_time = ('run_time', "-run_time: supporting running for a period of time or one day, 'current' or 'history', default is 'current'", 'current')
    filename = ('filename', "-filename: strategy file name; \n", None)
    strategy_name = ('strategy_name', "-stg_name: strategy name; \n", None)
    benchmark_type = ('benchmark_type', "-benchmark_type: 'strategy', 'fund' or 'index'; \n", 'index')
    frquency = ('frquency', "-frquency: 'DAILY', 'WEEKLY' or 'YEARLY' '\n", 'WEEKLY')
    portfolio_type = ('portfolio_type', "-portfolio_type  \n", None)
    market_type = ('market_type', "-market_type 'large' or 'small' \n", 'large')
    base_data_type = ('base_data_type', "-base_data_type 'fund' or 'index'\n", 'index')
    calc_with_fee = ('calc_with_fee', "-calc_with_fee 'True' or 'False' \n", 'False')
    is_transfer = ('is_transfer', "-is_transfer 'True' or 'False' \n", 'False')


NEED_INPUT_ARGUMENT = [InputArgument.run_time]


class ParamParser(object):
    """
    解析参数类
    输入参数格式: -env UAT -wind_db_typ prod -date 2017-06-05
    注: 支持数组类型, 例如: -code_list 000001 000002 000003
    """

    def __init__(self):
        self.env = None
        self.private_bank_model_db_type = None
        self.wind_db_type = None
        self.run_date = None
        self.from_date = None
        self.to_date = None
        self.op_type = None

        # macd cal input
        self.macd_type = None

    @staticmethod
    def parse(args, checked_args=()):
        """
        解析参数
        :param args: list, ['-env','UAT']
        :param checked_args: 需要输入的参数
        :return: dict, ['key':'value']
        """
        params_dict = dict()
        param_list = None
        error_info = ''

        for checked_arg in checked_args:
            error_info += checked_arg[1]

        if len(args) == 0:
            raise IOError("No arguments input! Please check your arguments! \nInput format: '-env UAT -wind_db_type prod'\nNeed input Arguments:\n%s" % error_info)

        arg_name = ''
        for arg in args:
            if arg.startswith('-'):
                ParamParser._set_params(params_dict, arg_name, param_list)
                arg_name = arg.replace('-', '')
                param_list = list()
            else:
                param_list.append(arg)

        # 设置最后一个参数
        ParamParser._set_params(params_dict, arg_name, param_list)

        ParamParser._fill_default_args(checked_args, params_dict)

        ParamParser._add_default_args(params_dict)

        ParamParser._check_arg(checked_args, params_dict, error_info)

        return params_dict

    @staticmethod
    def _set_params(params_dict, arg_name, param_list):
        if param_list is not None:
            if not len(param_list):
                raise IOError('Please check your argument: %s is None!' % arg_name)
            if len(param_list) == 1:
                params_dict[arg_name] = param_list[0]
            else:
                params_dict[arg_name] = param_list

    @staticmethod
    def _fill_default_args(checked_args, params_dict):
        for arg in checked_args:
            if arg[0] not in params_dict and arg[2]:
                params_dict[arg[0]] = arg[2]

    @staticmethod
    def _check_arg(checked_args, params_dict, error_info):
        for arg in checked_args:
            if arg[0] not in params_dict:
                raise ValueError("Please check your arguments and input following arguments: \n%s" % error_info)

    @staticmethod
    def _add_default_args(params_dict):
        for arg in NEED_INPUT_ARGUMENT:
            if arg[0] not in params_dict:
                params_dict[arg[0]] = arg[2]

    @staticmethod
    def param_deco(fixed_params_dict, **kwargs):
        params_dict = kwargs['params_dict']
        for key, value in fixed_params_dict.iteritems():
            params_dict[key] = value
        print kwargs


# 测试
if __name__ == '__main__':
    import sys

    ParamParser.parse(sys.argv[1:], (InputArgument.private_bank_model_db_type, InputArgument.wind_db_type))
