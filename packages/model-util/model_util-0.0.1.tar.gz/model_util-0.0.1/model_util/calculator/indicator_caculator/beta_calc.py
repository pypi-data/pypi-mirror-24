#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED


import decimal

import numpy

from caijiajia.model_util.calculator.indicator_caculator.base_calculator import BaseCalculator
from caijiajia.model_util.constant.indicator_constant import FrequencyDays

decimal.getcontext().prec = 22

def cov_util(l1, l2):
    return numpy.cov(numpy.asarray(l1), numpy.asarray(l2))


class BetaCalc(BaseCalculator):
    def _calc(self, nav_list, profit_list, risk_free_profit_list, index_nav_list,
              index_profit_list):
        # yearly_cov_a_index_arr = numpy.cov(numpy.asarray(profit_list, 'float'),
        #                                    numpy.asarray(index_profit_list, 'float'))
        # yearly_cov_a_index = yearly_cov_a_index_arr[0][1]
        # logging.info('指标与对标的协方差：')
        # logging.info(yearly_cov_a_index)
        #
        # yearly_var_index = numpy.cov(numpy.asarray(index_profit_list, 'float')) * FrequencyDays.get_days(self.frequency)
        # logging.info('对标的方差：%s' % yearly_var_index)
        #
        # return Decimal(yearly_cov_a_index) / Decimal(yearly_var_index)

        return BetaCalc.value_calc(profit_list, index_profit_list, self.frequency)

    @staticmethod
    def value_calc(profit_list, index_profit_list, frequency):
        yearly_cov_a_index_arr = numpy.cov(numpy.asarray(profit_list, 'float'),
                                           numpy.asarray(index_profit_list, 'float'))
        yearly_cov_a_index = yearly_cov_a_index_arr[0][1]

        yearly_var_index = numpy.cov(numpy.asarray(index_profit_list, 'float')) * FrequencyDays.get_days(frequency)

        return (decimal.Decimal(yearly_cov_a_index) / decimal.Decimal(yearly_var_index)).quantize(
            decimal.Decimal("0.000000"), rounding=decimal.ROUND_HALF_EVEN)
