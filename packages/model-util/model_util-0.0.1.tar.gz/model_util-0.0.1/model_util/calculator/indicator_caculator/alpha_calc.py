#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED

import decimal
from caijiajia.model_util.calculator.indicator_caculator.annualized_ror_calc import AnnualizedRorCalc
from caijiajia.model_util.calculator.indicator_caculator.base_calculator import BaseCalculator
from caijiajia.model_util.calculator.indicator_caculator.beta_calc import BetaCalc

decimal.getcontext().prec = 22


class AlphaCalc(BaseCalculator):
    def _calc(self, nav_list, profit_list, risk_free_profit_list, index_nav_list,
              index_profit_list):
        return AlphaCalc.value_calc(profit_list, risk_free_profit_list, index_profit_list, self.frequency)

    @staticmethod
    def value_calc(profit_list, risk_free_profit_list,
                   index_profit_list, frequency):
        yearly_return_a = AnnualizedRorCalc.value_calc(profit_list, frequency)
        yearly_return_index = AnnualizedRorCalc.value_calc(index_profit_list, frequency)
        yearly_return_f = AnnualizedRorCalc.value_calc(risk_free_profit_list, frequency)
        beta_code_index = BetaCalc.value_calc(profit_list, index_profit_list, frequency)

        res = (yearly_return_a - yearly_return_f - beta_code_index * (yearly_return_index - yearly_return_f)).quantize(
            decimal.Decimal("0.000000"), rounding=decimal.ROUND_HALF_EVEN)

        return res