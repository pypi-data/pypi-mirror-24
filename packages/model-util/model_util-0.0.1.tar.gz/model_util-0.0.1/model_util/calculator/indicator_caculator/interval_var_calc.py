#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED

import numpy
import decimal
from caijiajia.model_util.calculator.indicator_caculator.base_calculator import BaseCalculator

decimal.getcontext().prec = 22



class IntervalVarCalc(BaseCalculator):
    """
    计算区间方差
    """

    def _calc(self, nav_list, profit_list, risk_free_profit_list, index_nav_list,
              index_profit_list):
        return IntervalVarCalc.value_calc(profit_list)

    @staticmethod
    def value_calc(profit_list):
        # 计算标准方差 （除以n）
        return decimal.Decimal(numpy.var(profit_list)).quantize(decimal.Decimal("0.000000"), rounding=decimal.ROUND_HALF_EVEN)
