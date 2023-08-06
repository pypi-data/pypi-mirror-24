#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED

import math
from decimal import *
from itertools import combinations
from caijiajia.model_util.constant.constant import Constant
from caijiajia.model_util.constant.horizon import Horizon


class MvoUtil(object):
    DISTANCE_NUM = 8

    def __init__(self):
        pass

    @staticmethod
    def calc_horizon_portfolio_profit(market_profit_dict, portfolio_ratio_dict):
        """
        计算组合的收益率
        :param market_profit_dict:
        :param portfolio_ratio_dict:
        :return:
        """
        profit = 0
        for market_code, ratio in portfolio_ratio_dict.items():
            profit += float(ratio) * float(market_profit_dict[market_code])
        return round(float(profit), Constant.PROFIT_NUM)

    @staticmethod
    def calc_horizon_portfolio_risk(horizon, market_cov_dict, portfolio_ratio_dict, market_codes):
        """
        计算组合风险
        :param horizon: Horizon类型
        :param market_cov_dict: {(market1,market2):<value>,...}
        :param portfolio_ratio_dict:{<market>:<value>}
        :param market_codes: 市场列表[market1,market2,...]
        :return:
        """
        temp = range(0, len(market_codes))
        m1m2_list = list(combinations(temp, 2))
        for i in temp:
            m1m2_list.append((i, i))

        weekly_risk = 0
        for i in m1m2_list:
            market1 = market_codes[i[0]]
            market2 = market_codes[i[1]]
            if market1 == market2:
                weekly_risk += Decimal(portfolio_ratio_dict[market1]) * Decimal(portfolio_ratio_dict[market1]) * Decimal(market_cov_dict[(market1, market2)][0])
            else:
                weekly_risk += Decimal(2) * Decimal(portfolio_ratio_dict[market1]) * Decimal(portfolio_ratio_dict[market2]) * Decimal(market_cov_dict[(market1, market2)][0])

        horizon_risk = round(math.pow(float(weekly_risk) * Horizon.to_weeks(horizon), 0.5), Constant.RISK_NUM)
        return horizon_risk

    @staticmethod
    def calc_annualized_portfolio_risk(market_cov_dict, portfolio_ratio_dict, market_codes):
        """
        计算组合年化风险
        :param market_cov_dict: {(market1,market2):<value>,...}
        :param portfolio_ratio_dict:{<market>:<value>}
        :param market_codes: 市场列表[market1,market2,...]
        :return:
        """
        temp = range(0, len(market_codes))
        m1m2_list = list(combinations(temp, 2))
        for i in temp:
            m1m2_list.append((i, i))

        weekly_risk = 0
        for i in m1m2_list:
            market1 = market_codes[i[0]]
            market2 = market_codes[i[1]]
            if market1 == market2:
                weekly_risk += Decimal(portfolio_ratio_dict[market1]) * Decimal(portfolio_ratio_dict[market1]) * Decimal(market_cov_dict[(market1, market2)][0])
            else:
                weekly_risk += Decimal(2) * Decimal(portfolio_ratio_dict[market1]) * Decimal(portfolio_ratio_dict[market2]) * Decimal(market_cov_dict[(market1, market2)][0])

        horizon_risk = round(math.pow(float(weekly_risk) * 52, 0.5), Constant.RISK_NUM)
        return horizon_risk

    @staticmethod
    def calc_max_loss(horizon_ror, horizon_risk):
        """
        计算最大亏损
        :param horizon_ror:
        :param horizon_risk:
        :return:
        """
        return round(horizon_ror - 1.65 * horizon_risk, Constant.PROFIT_NUM)

    @staticmethod
    def calc_rebalance_deviation_radius(saa_list, deviation_points, risk_code):
        """
        计算再平衡的偏离半径
        :param saa_list: [1-11]风险点一定要有, 如果对应风险点下无组合,为None. [(profit,risk),...]
        :param deviation_points: 计算偏离的风险点
        :param risk_code: 当前组合的code
        :return:
        """
        min_portfolio = saa_list[0]
        max_portfolio = filter(lambda e: e is not None, saa_list)[-1]

        print 'calc radius, min_portfolio:%s, max_portfolio:%s!' % (min_portfolio, max_portfolio)

        left_code = risk_code - deviation_points
        right_code = risk_code + deviation_points

        left_portfolio = left_code > 0 and saa_list[left_code - 1] or None
        right_portfolio = right_code < 12 and saa_list[right_code - 1] or None

        cur_portfolio = saa_list[risk_code - 1]

        left_distance = None
        right_distance = None

        if left_portfolio is not None:
            left_distance = MvoUtil._calc_distance_for_norm(cur_portfolio[0], cur_portfolio[1], left_portfolio[0], left_portfolio[1], min_portfolio[0], max_portfolio[0], min_portfolio[1], max_portfolio[1])

        if right_portfolio is not None:
            right_distance = MvoUtil._calc_distance_for_norm(cur_portfolio[0], cur_portfolio[1], right_portfolio[0], right_portfolio[1], min_portfolio[0], max_portfolio[0], min_portfolio[1], max_portfolio[1])

        distance = None
        if left_distance is not None and right_distance is not None:
            print 'calc radius, left_distance:%s, right_distance:%s' % (left_distance, right_distance)
            distance = min(left_distance, right_distance)
        elif left_distance is not None:
            distance = left_distance
        elif right_distance is not None:
            distance = right_distance
        return round(float(distance), MvoUtil.DISTANCE_NUM)

    @staticmethod
    def calc_poins_distance(p1, p2, saa_list):
        """
        计算两个风险点的欧式距离
        :param p1: (profit, risk)
        :param p2: (profit, risk)
        :param saa_list: [1-11]风险点一定要有, 如果对应风险点下无组合,为None. [(profit,risk),...]
        :return:
        """
        min_portfolio = saa_list[0]
        max_portfolio = filter(lambda e: e is not None, saa_list)[-1]
        # print 'min_portfolio', min_portfolio, "max_portfolio", max_portfolio

        return round(float(MvoUtil._calc_distance_for_norm(p1[0], p1[1], p2[0], p2[1], min_portfolio[0], max_portfolio[0], min_portfolio[1], max_portfolio[1])), MvoUtil.DISTANCE_NUM)

    @staticmethod
    def _calc_distance_for_norm(x1, y1, x2, y2, min_x, max_x, min_y, max_y):
        x1_norm = MvoUtil._normalization(x1, min_x, max_x)
        x2_norm = MvoUtil._normalization(x2, min_x, max_x)
        y1_norm = MvoUtil._normalization(y1, min_y, max_y)
        y2_norm = MvoUtil._normalization(y2, min_y, max_y)
        return Decimal(math.sqrt(pow(x1_norm - x2_norm, 2) + pow(y1_norm - y2_norm, 2)))

    @staticmethod
    def _normalize_points(points, min_point, max_point):
        return MvoUtil._normalization(points[0], min_point[0], max_point[0]), MvoUtil._normalization(points[1], min_point[1], max_point[1])

    @staticmethod
    def _normalization(target, min_value, max_value):
        return (target - min_value) / (max_value - min_value)

    @staticmethod
    def calc_distance_without_norm(x1, y1, x2, y2):
        return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
