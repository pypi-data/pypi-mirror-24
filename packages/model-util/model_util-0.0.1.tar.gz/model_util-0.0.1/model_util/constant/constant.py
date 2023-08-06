#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED

class Constant(object):
    index_format_daily_closing_price = 'i_%s_daily_closing_price'
    index_format_daily_profit_ratio = 'i_%s_daily_profit_ratio'
    index_format_weekly_closing_price = 'i_%s_weekly_closing_price'
    index_format_weekly_profit_ratio = 'i_%s_weekly_profit_ratio'
    index_format_monthly_closing_price = 'i_%s_monthly_closing_price'
    index_format_monthly_profit_ratio = 'i_%s_monthly_profit_ratio'
    index_format_yearly_profit_ratio = 'i_%s_yearly_profit_ratio'
    index_format_1440_closing_price = 'i_%s_1440_closing_price'

    macro_index_format_daily_closing_price = 'mi_%s_daily_closing_price'
    macro_index_format_monthly_closing_price = 'mi_%s_monthly_closing_price'

    fund_format_daily_closing_price = 'f_%s_daily_closing_price'
    fund_format_daily_profit_ratio = 'f_%s_daily_profit_ratio'
    fund_format_weekly_closing_price = 'f_%s_weekly_closing_price'
    fund_format_weekly_profit_ratio = 'f_%s_weekly_profit_ratio'
    fund_format_yearly_profit_ratio = 'f_%s_yearly_profit_ratio'
    fund_format_monthly_profit_ratio = 'f_%s_monthly_profit_ratio'
    fund_format_3y_max_downside = 'f_%s_3y_max_downside'
    fund_format_1y_max_downside = 'f_%s_1y_max_downside'

    market_format_weekly_profit_ratio = '%s_weekly_profit_ratio'
    market_format_history_yearly_profit_ratio = '%s_history_yearly_profit_ratio'
    market_format_history_yearly_risk_ratio = '%s_history_yearly_risk_ratio'

    market_format_prospective_yearly_profit_ratio = '%s_prospective_yearly_profit_ratio'
    market_format_prospective_yearly_risk_ratio = '%s_prospective_yearly_risk_ratio'

    fund_star_company_list = ['易方达基金管理有限公司', '嘉实基金管理有限公司', '汇添富基金管理股份有限公司', '博时基金管理有限公司', '华夏基金管理有限公司']

    fund_profit_rank_format = '%s/%s'

    wind_fund_code_format_suffix = '.OF'

    wind_fund_code_format = '%s.OF'

    daily_profit_ratio_suffix = "_daily_profit_ratio"
    daily_closing_price_suffix = "_daily_closing_price"

    fund_order_dict = {"sharpe_last_year": 4, "yearly_profit_ratio_last_year": 5, "yearly_profit_ratio_last_three_years": 6, "latte_score": 7, "star_rank": 8, "profit_rank": 9}

    DEFAULT_FUND_START_DATE = '1996-01-01'

    VOL_NUM = 10

    NAV_NUM = 6

    AMOUNT_NUM = 6

    PROFIT_NUM = 6

    PROBABILITY_NUM = 6

    RISK_NUM = 6

    MAX_DOWNSIDE_NUM = 6

    CLOSE_NUM = 6

    DEVIATION_NUM = 6

    RATE_NUM = 4

    @staticmethod
    def encode_wind_fund_code(code):
        return code + Constant.wind_fund_code_format_suffix

    @staticmethod
    def decode_wind_fund_code(code):
        return code.replace(Constant.wind_fund_code_format_suffix, '')

    @staticmethod
    def decode_indicator_code(code):
        return code[2:].replace('_' + '_'.join(code.split('_')[-3:]), '')


# Sort config dict
class StockLatteScoreOrder(object):
    (company_rank, manager_rank, star_rank, last_year_profit_ratio, last_year_sharpe, last_six_months_profit_ratio, last_six_months_sharpe) = range(0, 7)


# Sort stock values dict
class StockLatteScoreDictOrder(object):
    (large_market_code, company, manager, star_rank, last_year_profit_ratio, last_year_sharpe, last_six_months_profit_ratio, last_six_months_sharpe) = [0, 1, 2, 3, 7, 7, 7, 7]


class FundBlackReason(object):
    (manager_changed, invalid_class, max_buy, market_change, hqb, key_stock_suspension, bond_defaults, exclude_topn) \
        = ('MANAGER_CHANGED', "INVALID_CLASS", "MAX_BUY", "MARKET_CHANGE", "HQB", "KEY_STOCK_SUSPENSION", "BOND_DEFAULTS", "EXCLUDE_TOPN")


class SyncStatus(object):
    (initial, success, fail) = ('INITIAL', 'SUCCESSFUL', 'FAILED')


class FundSelectedOrder(object):
    (min_amount, establish_date, sh_rate, fegm, star_rank, huoqibao_enabled, bond_scale, cash_scale, profit_window, half_risk_ratio_history, target, fee_times_thresh, max_amount, min_append, sh_rate_up_limit) = range(0, 15)


class ReportType(object):
    (TAA, FAA, SAA, MARKET, PORTFOLIO_INDICATOR) = ('TAA', 'FAA', 'SAA', 'MARKET', 'PORTFOLIO_INDICATOR')


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


class ChangeType(object):
    normal = 'NORMAL'
    increase = 'INCREASE'
    decrease = 'DECREASE'


class CodeType(object):
    # fund = "FUND"
    fund = 'FUND'
    currency_fund = 'CURRENCY_FUND'
    index = 'INDEX'
    market = 'MARKET'
    risk_less = 'RISK_LESS'


class ValueType(object):
    daily_closing_price = 'DAILY_CLOSING_PRICE'
    daily_profit_ratio = 'DAILY_PROFIT_RATIO'
    weekly_closing_price = 'WEEKLY_CLOSING_PRICE'
    weekly_profit_ratio = 'WEEKLY_PROFIT_RATIO'
    monthly_closing_price = 'MONTHLY_CLOSING_PRICE'
    monthly_profit_ratio = 'MONTHLY_PROFIT_RATIO'
    yearly_profit_ratio = 'YEARLY_PROFIT_RATIO'
    closing_price_1440 = 'CLOSING_PRICE_1440'
    max_downside_3y = '3Y_MAX_DOWNSIDE'
    max_downside_1y = '1Y_MAX_DOWNSIDE'
    yearly_risk_ratio = 'YEARLY_RISK_RATIO'
    prospective_yearly_profit_ratio = 'PROSPECTIVE_YEARLY_PROFIT_RATIO'


class PortfolioType(object):
    stock_bond_balance = 'SBB'
    stock_bond_round = 'SBR'
    mvo = 'MVO'
    mvo_2 = 'MVO_2'

    benchmark_sbb = 'BENCHMARK_SBB'
    benchmark_sbr = 'BENCHMARK_SBR'
    benchmark_mvo = 'BENCHMARK_MVO'
    benchmark_mvo_800 = 'BENCHMARK_MVO_800'  # 新增对标组合，中证800
    mvo_taa = 'MVO_TAA'
    mvo_saa = 'MVO_SAA'

    mvo_rebalance_1603 = "MVO_REBALANCE_1603"
    mvo_rebalance_1606 = "MVO_REBALANCE_1606"
    mvo_rebalance_1609 = "MVO_REBALANCE_1609"
    mvo_rebalance_1611 = "MVO_REBALANCE_1611"

    PORTFOLIO_SL_SBB_FLAG = ("portfolio_sl_sbb_1", "portfolio_sl_sbb_2")
    PORTFOLIO_SL_SBR_FLAG = ("portfolio_sl_sbr_1", "portfolio_sl_sbr_2")
    PORTFOLIO_HISTORY_PROFIT_SBB_FLAG = ("portfolio_history_profit_sbb_1", "portfolio_history_profit_sbb_2")
    PORTFOLIO_HISTORY_PROFIT_SBR_FLAG = ("portfolio_history_profit_sbr_1", "portfolio_history_profit_sbr_2")

    # 上线sl和portfolio_history_profit使用
    SL = "SL"
    HISTORY_PROFIT = "HISTORY_PROFIT"

    @staticmethod
    def get_non_calc_type():
        return [PortfolioType.benchmark_mvo, PortfolioType.benchmark_sbb, PortfolioType.benchmark_sbr, PortfolioType.mvo_taa,
                PortfolioType.mvo_saa, PortfolioType.mvo_rebalance_1609, PortfolioType.mvo_rebalance_1603, PortfolioType.mvo_rebalance_1606,
                PortfolioType.mvo_rebalance_1611, PortfolioType.mvo]

    @staticmethod
    def get_online_type():
        return [PortfolioType.stock_bond_balance, PortfolioType.stock_bond_round]

    @staticmethod
    def get_portfolio_type_flag(strategy_type, data_type):
        if strategy_type == PortfolioType.stock_bond_balance and data_type == PortfolioType.SL:
            return PortfolioType.PORTFOLIO_SL_SBB_FLAG
        elif strategy_type == PortfolioType.stock_bond_round and data_type == PortfolioType.SL:
            return PortfolioType.PORTFOLIO_SL_SBR_FLAG
        elif strategy_type == PortfolioType.stock_bond_balance and data_type == PortfolioType.HISTORY_PROFIT:
            return PortfolioType.PORTFOLIO_HISTORY_PROFIT_SBB_FLAG
        elif strategy_type == PortfolioType.stock_bond_round and data_type == PortfolioType.HISTORY_PROFIT:
            return PortfolioType.PORTFOLIO_HISTORY_PROFIT_SBR_FLAG


class TransferType(object):
    rebalance = 'REBALANCE'
    macd_1440 = 'MACD_1440'
    macd_daily = "MACD_DAILY"
    taa = 'TAA'
    faa = 'FAA'
    first = 'FIRST'
    saa = 'SAA'
    ror = 'ROR'
    pe = 'PE'

    @staticmethod
    def get_online_transfer():
        return [TransferType.rebalance, TransferType.macd_1440, TransferType.macd_daily]


class SyncName(object):
    taa_online = 'TAA_ONLINE'


class WindDataFieldType(object):
    nav_adj = 'NAV_adj'
    close = 'close'
    mmf_unityield = 'mmf_unityield'
    mmf_annualizedyield = 'mmf_annualizedyield'


class FundType(object):
    non_currency = "NON_CURRENCY_FUND"
    currency = "CURRENCY_FUND"


class Valuetype2FundCodeFormat(object):
    valuetype_to_code_format_dict = {
        ValueType.daily_closing_price: Constant.fund_format_daily_closing_price,
        ValueType.daily_profit_ratio: Constant.fund_format_daily_profit_ratio,
        ValueType.weekly_profit_ratio: Constant.fund_format_weekly_profit_ratio
    }


class MarketCode(object):
    M_INTERNATIONAL_BOND = 'm_international_bond'
    M_DOMESTIC_PURE_BOND = 'm_domestic_pure_bond'
    M_DOMESTIC_DEBT_LIKE_BOND = 'm_domestic_debt_like_bond'
    M_DOMESTIC_MIDDLE_SMALL_CAP_STOCK = 'm_domestic_middle_small_cap_stock'
    M_DOMESTIC_TOTAL_STOCK = 'm_domestic_total_stock'
    M_CURRENCY = 'm_currency'
    M_US_STOCK = 'm_us_stock'
    M_HK_STOCK = 'm_hk_stock'
    M_GOLD = 'm_gold'
    M_OIL = 'm_oil'
    M_DOMESTIC_STOCK = 'm_domestic_stock'
    M_FIXED_INCOME = 'm_fixed_income'


class RetryType(object):
    RETRY_FUND_TYPE = 'fund'
    RETRY_INDEX_TYPE = 'index'
    RETRY_OTHER_TYPE = 'other'
