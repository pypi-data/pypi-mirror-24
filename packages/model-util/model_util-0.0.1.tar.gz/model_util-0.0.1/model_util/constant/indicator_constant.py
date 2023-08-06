#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED


class Constant(object):
    risk_free_rate_code = 'S0059749'


class IndicatorType(object):
    index = 'INDEX'
    fund = 'FUND'
    portfolio = 'PORTFOLIO'


class Frequency(object):
    daily = 'DAILY'
    weekly = 'WEEKLY'
    monthly = 'MONTHLY'


class CalcType(object):
    interval_return = 'INTERVAL_RETURN'
    maxdown = 'MAXDOWN'
    sharpe = 'SHARPE'
    interval_var = 'INTERVAL_VAR'
    interval_cov = 'INTERVAL_COV'
    yearly_profit = 'YEARLY_PROFIT'
    extra_return = 'EXTRA_RETURN'
    beta = 'BETA'
    alpha = 'ALPHA'
    ir = 'IR'
    treynor = 'TREYNOR'
    sortino = 'SORTINO'


class FrequencyDays(object):
    day = 250
    week = 52
    month = 12

    @staticmethod
    def get_days(frequency):
        if frequency == Frequency.daily:
            return FrequencyDays.day
        elif frequency == Frequency.weekly:
            return FrequencyDays.week
        elif frequency == Frequency.monthly:
            return FrequencyDays.month
        else:
            return FrequencyDays.day
