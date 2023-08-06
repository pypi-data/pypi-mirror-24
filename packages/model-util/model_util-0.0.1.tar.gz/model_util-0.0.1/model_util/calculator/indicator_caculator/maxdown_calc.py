#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED
import decimal
from caijiajia.model_util.calculator.indicator_caculator.base_calculator import BaseCalculator
from caijiajia.model_util.constant.constant import Constant

decimal.getcontext().prec = 22


class MaxdownCalc(BaseCalculator):
    def _calc(self, nav_list, profit_list, risk_free_profit_list, index_nav_list,
              index_profit_list):
        return MaxdownCalc.value_calc(nav_list)

    @staticmethod
    def value_calc(nav_list):
        item_list = [(x, y) for i, x in enumerate(nav_list) for j, y in enumerate(nav_list) if i < j]
        return decimal.Decimal(max(map(lambda (item1, item2): 1 - item2 / item1, item_list))).quantize(
            decimal.Decimal("0.000000"), rounding=decimal.ROUND_HALF_EVEN)