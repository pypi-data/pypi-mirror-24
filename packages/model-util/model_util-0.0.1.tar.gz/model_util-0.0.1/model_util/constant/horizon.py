#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED


class Horizon(object):
    # horizons = ('ONE_MONTH', 'THREE_MONTH', 'HALF_YEAR', 'ONE_YEAR', 'TWO_YEAR', 'THREE_YEAR')
    horizons = ('THREE_MONTH', 'HALF_YEAR', 'ONE_YEAR', 'THREE_YEAR')

    @staticmethod
    def to_month_code(horizon):
        if horizon == 'ONE_MONTH':
            return 1
        elif horizon == 'THREE_MONTH':
            return 3
        elif horizon == 'HALF_YEAR':
            return 6
        elif horizon == 'ONE_YEAR':
            return 0
        elif horizon == 'TWO_YEAR':
            return 24
        elif horizon == 'THREE_YEAR':
            return 36

    @staticmethod
    def to_horizon(month):
        if month == 3:
            return Horizon.horizons[0]
        elif month == 6:
            return Horizon.horizons[1]
        elif month == 0:
            return Horizon.horizons[2]
        elif month == 36:
            return Horizon.horizons[3]

    @staticmethod
    def to_days(horizon):
        if horizon == 'ONE_MONTH':
            return 30
        elif horizon == 'THREE_MONTH':
            return 90
        elif horizon == 'HALF_YEAR':
            return 180
        elif horizon == 'ONE_YEAR':
            return 365
        elif horizon == 'TWO_YEAR':
            return 365 * 2
        elif horizon == 'THREE_YEAR':
            return 365 * 3
        else:
            return -1

    @staticmethod
    def to_months(horizon):
        if horizon == 'ONE_MONTH':
            return 1
        elif horizon == 'THREE_MONTH':
            return 3
        elif horizon == 'HALF_YEAR':
            return 6
        elif horizon == 'ONE_YEAR':
            return 12
        elif horizon == 'TWO_YEAR':
            return 24
        elif horizon == 'THREE_YEAR':
            return 36

    @staticmethod
    def to_weeks(horizon):
        if horizon == 'ONE_MONTH':
            return 4
        elif horizon == 'THREE_MONTH':
            return 13
        elif horizon == 'HALF_YEAR':
            return 26
        elif horizon == 'ONE_YEAR':
            return 52
        elif horizon == 'TWO_YEAR':
            return 52 * 2
        elif horizon == 'THREE_YEAR':
            return 52 * 3
        else:
            return -1