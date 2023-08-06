#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED

import numpy
import decimal
from caijiajia.model_util.calculator.indicator_caculator.base_calculator import BaseCalculator

decimal.getcontext().prec = 22

class IntervalCovCalc(BaseCalculator):
    """
    计算区间样本方差
    """

    def _calc(self, nav_list, profit_list, risk_free_profit_list, index_nav_list,
              index_profit_list):
        # 指标计算期用的是样本方差
        return IntervalCovCalc.value_calc(profit_list)

    def _check_data(self, nav_list, profit_list, risk_free_profit_list, index_nav_list, index_profit_list):
        if len(nav_list) == (self.end_date - self.start_date).days:
            return True
        return False

    @staticmethod
    def value_calc(profit_list):
        return decimal.Decimal(numpy.cov(numpy.asarray(profit_list, 'float'))).quantize(
            decimal.Decimal("0.000000"), rounding=decimal.ROUND_HALF_EVEN)
