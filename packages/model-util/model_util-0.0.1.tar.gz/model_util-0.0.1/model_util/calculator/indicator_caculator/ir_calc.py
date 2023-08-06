#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED


from decimal import Decimal

import numpy

from caijiajia.model_util.calculator.indicator_caculator import BaseCalculator
from caijiajia.model_util.constant.indicator_constant import FrequencyDays


class IrCalc(BaseCalculator):
    def _calc(self, nav_list, profit_list, risk_free_profit_list, index_nav_list,
              index_profit_list):
        return IrCalc.value_calc(profit_list, index_profit_list, self.frequency)

    @staticmethod
    def value_calc(profit_list, index_profit_list, frequency):
        delta_profit_list = []
        for i, profit in enumerate(profit_list):
            delta_profit_list.append(profit - index_profit_list[i])

        frequency_days = FrequencyDays.get_days(frequency)

        yearly_return_delta = numpy.mean(delta_profit_list) * frequency_days

        yearly_var_delta = numpy.cov(numpy.asarray(delta_profit_list, 'float'))

        return yearly_return_delta / Decimal(numpy.sqrt(yearly_var_delta * frequency_days))
