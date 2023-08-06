#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED

import logging
import sys
from abc import abstractmethod

from dateutil.relativedelta import *

from caijiajia.model_util.constant.indicator_constant import Frequency, Constant
from caijiajia.model_util.utils.date_util import DateUtil
from caijiajia.strategybacktest.dao.privatebankmodel.meta_indicator_nav_dao import MetaIndicatorNavDao
from caijiajia.strategybacktest.dao.privatebankmodel.model_portfolio_nav_dao import ModelPortfolioNavDao

reload(sys)
sys.setdefaultencoding('utf8')


# 所有需要计算方差的，使用样本方差计算器（IntervalCovCalc）, 不用总体方差计算器（IntervalVarCalc）
class BaseCalculator(object):
    """
    计算器基础类
    """

    def __init__(self,db_type, code, frequency, start_date_str, end_date_str, nav_result, profit_result, benchmark_nav_result,
                 benchmark_profit_result, portfolio_type=None, benchmark_type=None, weekday=None):
        """
        初始化
        :param code:
        :param frequency:
        :param start_date_str:
        :param end_date_str:
        :param portfolio_type:
        :param benchmark_type:
        :param weekday: 如果不为None, 可以指定使用date=weekday周收益率作为计算数据源, 如果为None, weekday默认为end_date.weekday()
        :return:
        """
        self.code = code
        self.frequency = frequency
        self.start_date = DateUtil.to_date(start_date_str)
        self.end_date = DateUtil.to_date(end_date_str)

        self.portfolio_type = portfolio_type
        self.benchmark_type = benchmark_type

        self.nav_result = nav_result
        self.profit_result = profit_result

        self.benchmark_nav_result = benchmark_nav_result
        self.benchmark_profit_result = benchmark_profit_result

        self.db_type = db_type

        if weekday is None:
            self.weekday = self.end_date.weekday()
        else:
            self.weekday = weekday

        self.month = self.end_date.month
        self.day = self.end_date.day

        if frequency == Frequency.monthly:
            self.col = 'monthly_profit_ratio'
        elif frequency == Frequency.weekly:
            self.col = 'weekly_profit_ratio'
        elif frequency == Frequency.daily:
            self.col = 'daily_profit_ratio'
        else:
            self.col = 'weekly_profit_ratio'

        self._load_data()

    def _load_data(self):
        risk_free_nav_result, risk_free_profit_result = self._read_base_data(self.col, Constant.risk_free_rate_code, self.start_date, self.end_date)

        nav_list, profit_list = self._get_calc_data(self.nav_result, self.profit_result)

        # 注意： 十年期国债收益率，并不是一个指数，所以并没有nav数值，所以risk_free_nav_list是不可用的
        risk_free_nav_list, risk_free_profit_list = self._get_calc_data(risk_free_nav_result, risk_free_profit_result)

        benchmark_nav_list, benchmark_profit_list = self._get_calc_data(self.benchmark_nav_result, self.benchmark_profit_result)

        self.nav_list = nav_list
        self.profit_list = profit_list
        self.risk_free_profit_list = risk_free_profit_list
        self.benchmark_nav_list = benchmark_nav_list
        self.benchmark_profit_list = benchmark_profit_list

    def calc(self):
        """
        计算入口
        :return:
        """
        if not self._check_data(self.nav_list, self.profit_list, self.risk_free_profit_list, self.benchmark_nav_list, self.benchmark_profit_list):
            return None

        calc_result = self._calc(self.nav_list, self.profit_list, self.risk_free_profit_list, self.benchmark_nav_list, self.benchmark_profit_list)
        logging.info("%s 计算结果: %s" % (self.__class__.__name__, calc_result))
        return calc_result

    @abstractmethod
    def _calc(self, nav_list, profit_list, risk_free_profit_list, index_nav_list,
              index_profit_list):
        """
        算法逻辑
        nav_list: 指标净值数据列表
        profit_list: 指标收益率数据列表
        risk_free_nav_list: 无风险指标净值列表
        risk_free_profit_list: 无风险指标收益率列表
        :return:
        """
        pass

    def _check_data(self, nav_list, profit_list, risk_free_profit_list, index_nav_list, index_profit_list):
        """
        检查数据是否符合计算条件
        :param nav_list:
        :param profit_list:
        :param risk_free_profit_list:
        :param index_nav_list:
        :param index_profit_list:
        :return:
        """
        return True

    def _get_calc_data(self, nav_result, profit_result):
        nav_list = []
        profit_list = []
        # 检查日期范围内数据足够
        if nav_result and len(nav_result) > 0:
            for code, date, nav in nav_result:
                if nav:
                    nav_list.append(nav)

        if profit_result and len(profit_result) > 0:
            diff_year = self.end_date.year - self.start_date.year
            diff_month = self.end_date.month - self.start_date.month
            interval_month = diff_year * 12 + diff_month

            month_dates = []
            for i in range(interval_month + 1):
                month_dates.append(self.end_date + relativedelta(months=-i))

            for code, date, profit in profit_result:
                if self.frequency == Frequency.monthly:
                    if date in month_dates:
                        profit_list.append(profit)
                elif self.frequency == Frequency.weekly:
                    if date.weekday() == self.weekday:
                        profit_list.append(profit)
                elif self.frequency == Frequency.daily:
                    if date != self.start_date:
                        profit_list.append(profit)
        return nav_list, profit_list

    @staticmethod
    def get_calc_nav(nav_result):
        nav_list = []
        # 检查日期范围内数据足够
        if nav_result and len(nav_result) > 0:
            for code, date, nav in nav_result:
                if nav:
                    nav_list.append(nav)
        return nav_list

    @staticmethod
    def get_calc_profit(profit_result, start_date, end_date, frequency, weekday):
        profit_list = []

        if profit_result and len(profit_result) > 0:
            diff_year = end_date.year - start_date.year
            diff_month = end_date.month - start_date.month
            interval_month = diff_year * 12 + diff_month

            month_dates = []
            for i in range(interval_month + 1):
                month_dates.append(end_date + relativedelta(months=-i))

            for code, date, profit in profit_result:
                if frequency == Frequency.monthly:
                    if date in month_dates:
                        profit_list.append(profit)
                elif frequency == Frequency.weekly:
                    if date.weekday() == weekday:
                        profit_list.append(profit)
                elif frequency == Frequency.daily:
                    if date != start_date:
                        profit_list.append(profit)
        return profit_list

    def _read_portfolio_data(self, portfolio_type, code, start_date, end_date, col):
        dao = ModelPortfolioNavDao(self.db_type)
        profit_result = dao.get_by_range_date(portfolio_type, code, start_date, end_date, col)
        nav_result = dao.get_nav_by_range_date(portfolio_type, code, start_date, end_date)
        dao.close()
        return nav_result, profit_result

    def _read_base_data(self, col, code, start_date, end_date):
        dao = MetaIndicatorNavDao(self.db_type)
        profit_result = dao.read_by_range_date(col, code, start_date, end_date)
        nav_result = dao.read_nav_by_range_date(code, start_date, end_date)
        return nav_result, profit_result

    def _read_risk_less(self, code, start_date, end_date):
        pass
