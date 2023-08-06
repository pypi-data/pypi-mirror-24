#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED


import decimal

import numpy

from caijiajia.model_util.calculator.indicator_caculator.annualized_ror_calc import AnnualizedRorCalc
from caijiajia.model_util.calculator.indicator_caculator.base_calculator import BaseCalculator
from caijiajia.model_util.constant.indicator_constant import FrequencyDays

decimal.getcontext().prec = 22

class SortinoCalc(BaseCalculator):
    def _calc(self, nav_list, profit_list, risk_free_profit_list, index_nav_list, index_profit_list):
        return SortinoCalc.value_calc(profit_list, risk_free_profit_list, self.frequency)

    @staticmethod
    def value_calc(profit_list, risk_free_profit_list, frequency):

        delta_profit_list = []

        for i, profit in enumerate(profit_list):
            delta_profit = profit - risk_free_profit_list[i]
            if delta_profit > 0:
                delta_profit = 0
            delta_profit_list.append(delta_profit)

        yearly_var_delta = numpy.cov(numpy.asarray(delta_profit_list, 'float'))

        yearly_return_a = AnnualizedRorCalc.value_calc(profit_list, frequency)

        yearly_return_f = AnnualizedRorCalc.value_calc(risk_free_profit_list, frequency)

        return ((yearly_return_a - yearly_return_f) / decimal.Decimal(numpy.sqrt(yearly_var_delta * FrequencyDays.get_days(frequency)))).quantize(
            decimal.Decimal("0.000000"), rounding=decimal.ROUND_HALF_EVEN)
