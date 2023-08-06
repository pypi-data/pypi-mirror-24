#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED


import logging
import decimal
from caijiajia.model_util.calculator.indicator_caculator.annualized_risk_calc import AnnualizedRiskCalc
from caijiajia.model_util.calculator.indicator_caculator.annualized_ror_calc import AnnualizedRorCalc
from caijiajia.model_util.calculator.indicator_caculator.base_calculator import BaseCalculator

decimal.getcontext().prec = 22


class SharpeCalc(BaseCalculator):
    """
    计算夏普比
    """

    def _calc(self, nav_list, profit_list, risk_free_profit_list, index_nav_list, index_profit_list):
        return SharpeCalc.value_calc(profit_list, risk_free_profit_list, self.frequency)

    def _check_data(self, nav_list, profit_list, risk_free_profit_list, index_nav_list, index_profit_list):
        if len(nav_list) == (self.end_date - self.start_date).days + 1 and len(profit_list) == len(risk_free_profit_list):
            return True
        return False

    @staticmethod
    def check_data(nav_list, profit_list, risk_free_profit_list, from_date, to_date):
        if len(nav_list) == (to_date - from_date).days + 1 and len(profit_list) == len(risk_free_profit_list):
            return True
        return False

    @staticmethod
    def value_calc(profit_list, risk_free_profit_list, frequency):
        yearly_return_a = AnnualizedRorCalc.value_calc(profit_list, frequency)
        yearly_return_f = AnnualizedRorCalc.value_calc(risk_free_profit_list, frequency)
        yearly_var_a = AnnualizedRiskCalc.value_calc(profit_list, frequency)

        if yearly_var_a == 0:
            logging.warn("calc sharpe: annualized risk is zero! profit length:%s" % len(profit_list))
            return None
        return ((yearly_return_a - yearly_return_f) / yearly_var_a).quantize(decimal.Decimal("0.000000"),
                                                                             rounding=decimal.ROUND_HALF_EVEN)
