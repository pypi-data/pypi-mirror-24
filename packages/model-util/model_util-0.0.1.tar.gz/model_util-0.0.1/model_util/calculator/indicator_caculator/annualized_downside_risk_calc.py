#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED

import decimal
import logging

import numpy

from caijiajia.model_util.calculator.indicator_caculator.base_calculator import BaseCalculator
from caijiajia.model_util.constant.indicator_constant import FrequencyDays

decimal.getcontext().prec = 22


class AnnualizedDownsideRiskCalc(BaseCalculator):
    """
    计算区间年化半方差
    """

    def _calc(self, nav_list, profit_list, risk_free_profit_list, index_nav_list,
              index_profit_list):
        return AnnualizedDownsideRiskCalc.value_calc(profit_list, self.frequency)

    def _check_data(self, nav_list, profit_list, risk_free_profit_list, index_nav_list, index_profit_list):
        if len(nav_list) == (self.end_date - self.start_date).days + 1 and len(profit_list) > 1:
            return True
        logging.warn("Can not calculate the yearly profit ratio! code:%s, start_date:%s, end_date:%s" % (self.code, self.start_date, self.end_date))
        return False

    @staticmethod
    def check_data(nav_list, profit_list, from_date, to_date):
        if len(nav_list) == (to_date - from_date).days + 1 and len(profit_list) > 1:
            return True
        return False

    @staticmethod
    def value_calc(profit_list, frequency):
        avg_p = numpy.mean(profit_list)
        half_var = sum((min(0, p) - avg_p) ** 2 for p in profit_list) / (len(profit_list) - 1)
        return decimal.Decimal(numpy.sqrt(half_var * FrequencyDays.get_days(frequency))).quantize(
            decimal.Decimal("0.000000"), rounding=decimal.ROUND_HALF_EVEN)
