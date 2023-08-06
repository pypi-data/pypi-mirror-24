#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED

import logging
import decimal
from caijiajia.model_util.calculator.indicator_caculator.base_calculator import BaseCalculator

decimal.getcontext().prec = 22


class IntervalReturnCalc(BaseCalculator):
    """
    计算区间回报
    """

    def _calc(self, nav_list, profit_list, risk_free_profit_list, index_nav_list,
              index_profit_list):
        return IntervalReturnCalc.value_calc(nav_list)

    def _check_data(self, nav_list, profit_list, risk_free_profit_list, index_nav_list, index_profit_list):
        if len(nav_list) == (self.end_date - self.start_date).days + 1:
            return True
        logging.warn("Can not calculate the interval return! code:%s, start_date:%s, end_date:%s" % (self.code, self.start_date, self.end_date))
        return False

    @staticmethod
    def check_data(nav_list, start_date, end_date):
        if len(nav_list) == (end_date - start_date).days + 1:
            return True
        return False

    @staticmethod
    def value_calc(nav_list):
        return decimal.Decimal(nav_list[-1] / nav_list[0] - 1).quantize(decimal.Decimal("0.000000"),
                                                                        rounding=decimal.ROUND_HALF_EVEN)
