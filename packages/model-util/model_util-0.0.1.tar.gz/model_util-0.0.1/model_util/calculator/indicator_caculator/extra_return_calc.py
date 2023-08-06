#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED
from caijiajia.model_util.calculator.indicator_caculator.base_calculator import BaseCalculator
from caijiajia.model_util.calculator.indicator_caculator.interval_return_calc import IntervalReturnCalc


class ExtraReturnCalc(BaseCalculator):
    def _calc(self, nav_list, profit_list, risk_free_profit_list, index_nav_list,
              index_profit_list):
        return ExtraReturnCalc.value_calc(nav_list, index_nav_list)

    @staticmethod
    def value_calc(nav_list, index_nav_list):
        return_a = IntervalReturnCalc.value_calc(nav_list)
        return_index = IntervalReturnCalc.value_calc(index_nav_list)

        return return_a - return_index
