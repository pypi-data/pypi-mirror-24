# #!/usr/bin/env python
# # encoding: utf-8
# # Author caijiajia.cn
# # @ ALL RIGHTS RESERVED
#
# from caijiajia.model_util.utils.json_util import JsonUtil
# from caijiajia.strategybacktest.constant.constant import PortfolioType
# from caijiajia.strategybacktest.constant.constant import TransferType
# from caijiajia.strategybacktest.constant.constant import Constant
# import copy
# import logging
#
#
# class TransferRecord(object):
#     def __init__(self, transfer_type, target_weight):
#         self.transfer_type = transfer_type
#         self.target_weight = target_weight
#
#
# class PortfolioNav(object):
#     def __init__(self):
#         self.nav = 0
#         self.fund_vol = {}
#         self.fund_amount = {}
#         self.market_weight = {}
#
#
# class PortfolioNavCalcUtil(object):
#     def __init__(self, date, portfolio_code, portfolio_type, portfolio_last_nav, last_fund_vol, last_fund_amount, last_fund_weight, cur_fund_nav, last_fund_nav, transfer_record, fund_rate):
#         self.date = date
#         self.portfolio_code = portfolio_code
#         self.portfolio_type = portfolio_type
#         self.portfolio_last_nav = portfolio_last_nav
#         self.last_fund_vol = last_fund_vol
#         self.last_fund_amount = last_fund_amount
#
#         # {market:{fund_code:weight}}
#         self.last_fund_weight = last_fund_weight
#
#         self.cur_fund_nav = cur_fund_nav
#         self.last_fund_nav = last_fund_nav
#
#         self.transfer_record = transfer_record
#         self.fund_rate = fund_rate
#
#         if self.portfolio_type == PortfolioType.mvo:
#             self.is_transfer = False
#         else:
#             self.is_transfer = True
#
#         self.market_fund_dict = {}
#         if self.last_fund_weight is not None:
#             for market_code, fund_weight in self.last_fund_weight.iteritems():
#                 for fund_code, weight in fund_weight.iteritems():
#                     self.market_fund_dict[fund_code] = market_code
#
#         if self.transfer_record is not None:
#             for market_code, fund_weight in self.transfer_record.target_weight.iteritems():
#                 for fund_code, weight in fund_weight.iteritems():
#                     self.market_fund_dict[fund_code] = market_code
#
#     def calc_nav(self, ori_fund_weight, use_rate):
#         """
#         计算组合净值
#         :return:
#         """
#         if self.transfer_record is not None and self.transfer_record.transfer_type == TransferType.first:
#             return self._calc_for_first(ori_fund_weight), None, None
#         else:
#             return self._calc_for_normal(ori_fund_weight, use_rate)
#
#     def _calc_for_first(self, ori_fund_weight):
#         """
#         计算组合第一天净值,首次计算组合净值,默认投资金额为1,份额保留四位小数 金额保留六位小数
#         :return:
#         """
#         fund_vol = {}
#         fund_amount = {}
#         market_amount = {}
#         sum_assets = 1
#         for market_code, fund_weight in self.transfer_record.target_weight.iteritems():
#             for fund_code, weight in fund_weight.iteritems():
#                 temp_assets = weight * sum_assets
#                 fund_vol[fund_code] = round(temp_assets / float(self.cur_fund_nav[fund_code]), Constant.VOL_NUM)
#                 fund_amount[fund_code] = weight
#                 market_amount.setdefault(market_code, {})[fund_code] = temp_assets
#         nav = 1
#         market_weight = PortfolioNavCalcUtil._to_market_weight(market_amount, self.market_fund_dict, ori_fund_weight)
#         return self.portfolio_code, self.date, self.portfolio_type, nav, JsonUtil.encode_json(fund_vol), JsonUtil.encode_json(market_weight), JsonUtil.encode_json(fund_amount)
#
#     def _calc_for_normal(self, ori_fund_weight, use_rate):
#         """
#         计算组合的净值, 非第一天
#         :return:
#         """
#         transfer = None
#         transfer_detail = None
#         nav = 0
#         fund_amount = {}
#         market_amount = {}
#
#         # 如有调仓信息, 求当天份额
#         fund_vol = copy.deepcopy(self.last_fund_vol)
#         if self.transfer_record is not None:
#             if self.transfer_record.transfer_type == TransferType.faa:
#                 # 仅适用产品调仓
#                 fund_vol = PortfolioNavCalcUtil._calc_transfer_for_faa(self.last_fund_weight, self.last_fund_amount, self.transfer_record.target_weight, self.last_fund_nav, self.last_fund_vol)
#             else:
#                 # 市场比例变更
#                 target_fund_assets = PortfolioNavCalcUtil._calc_target_fund_assets(self.portfolio_last_nav, self.transfer_record.target_weight)
#                 transfer_out, transfer_assets_record, no_changed_codes = PortfolioNavCalcUtil._calc_transfer(self.last_fund_amount, target_fund_assets)
#                 fund_vol, transfer_detail = self._calc_transfer_detail(transfer_out, transfer_assets_record, no_changed_codes, use_rate)
#
#         # 计算当天组合净值
#         for fund_code, vol in fund_vol.iteritems():
#             temp_assets = round(vol * float(self.cur_fund_nav[fund_code]), Constant.AMOUNT_NUM)
#             nav += temp_assets
#             fund_amount[fund_code] = temp_assets
#             market_amount.setdefault(self.market_fund_dict[fund_code], {})[fund_code] = temp_assets
#
#         fund_weight = PortfolioNavCalcUtil._to_market_weight(market_amount, self.market_fund_dict, ori_fund_weight)
#
#         if transfer_detail is not None:
#             transfer = (self.portfolio_code, self.date, self.portfolio_type, JsonUtil.encode_json(self.last_fund_weight), JsonUtil.encode_json(self.last_fund_vol), JsonUtil.encode_json(self.last_fund_amount),
#                         JsonUtil.encode_json(fund_weight), JsonUtil.encode_json(fund_vol), JsonUtil.encode_json(fund_amount))
#         return (self.portfolio_code, self.date, self.portfolio_type, nav, JsonUtil.encode_json(fund_vol), JsonUtil.encode_json(fund_weight), JsonUtil.encode_json(fund_amount)), transfer, transfer_detail
#
#     @staticmethod
#     def _to_market_weight(market_amount, market_fund_dict, ori_fund_weight):
#         market_weight = {}
#         sum_assets = 0
#         for market_code, funds_amount in market_amount.iteritems():
#             sum_assets += sum(funds_amount.values())
#
#         sum_weight = 0
#         fund_weight = []
#
#         for market_code, funds_amount in market_amount.iteritems():
#             for fund_code, amount in funds_amount.iteritems():
#                 fund_weight.append((fund_code, round(amount / sum_assets, 4)))
#
#         fund_weight.sort(key=lambda e: e[1])
#         for i in range(len(fund_weight)):
#             if i == len(fund_weight) - 1:
#                 left_weight = round(1 - sum_weight, 4)
#             else:
#                 left_weight = round(fund_weight[i][1], 4)
#             market_weight.setdefault(market_fund_dict[fund_weight[i][0]], {})[fund_weight[i][0]] = round(left_weight, 4)
#             sum_weight += fund_weight[i][1]
#
#         if ori_fund_weight is not None:
#             for market_code, fund_weight in ori_fund_weight.items():
#                 for fund_code, weight in fund_weight.items():
#                     if market_code not in market_weight or fund_code not in market_weight[market_code]:
#                         market_weight.setdefault(market_code, {})[fund_code] = 0.0
#         return market_weight
#
#     @staticmethod
#     def _calc_target_fund_assets(sum_assets, target_fund_weight_dict):
#         target_market_fund_assets = {}
#         for market_code, fund_weight in target_fund_weight_dict.iteritems():
#             for fund_code, weight in fund_weight.iteritems():
#                 target_market_fund_assets.setdefault(market_code, {})[fund_code] = round(float(sum_assets) * float(weight), Constant.AMOUNT_NUM)
#         return target_market_fund_assets
#
#     @staticmethod
#     def _calc_transfer_for_faa(last_fund_weight, last_fund_assets_dict, target_fund_weight_dict, last_fund_nav_dict, last_fund_vol_dict):
#         """
#         计算FAA变更, 计算产品变更后份额
#         FAA类型的调仓，目前只限于市场占比不变，只有基金之间的替换，且替换后的基金占比，与替换之前的基金占比完全一致
#         :param last_fund_assets_dict:
#         :param target_fund_weight_dict:
#         :return:
#         """
#
#         target_fund_vol_dict = {}
#         for market_code, fund_weight_dict in target_fund_weight_dict.iteritems():
#             if sum(fund_weight_dict.values()) == 0:
#                 continue
#             # 市场下产品按比例从大到小排序, 依次替换
#             if not last_fund_weight.__contains__(market_code):
#                 print 'Can not find marketCode in last fund weight!', market_code
#                 # print JsonUtil.encode_json(last_fund_weight)
#                 # print JsonUtil.encode_json(target_fund_weight_dict)
#             no_change_codes = filter(lambda e: fund_weight_dict.__contains__(e[0]), last_fund_weight[market_code].items())
#
#             need_change_codes = filter(lambda e: not fund_weight_dict.__contains__(e[0]), last_fund_weight[market_code].items())
#             replace_codes = filter(lambda e: not last_fund_weight[market_code].__contains__(e[0]), fund_weight_dict.items())
#
#             if need_change_codes is not None and len(need_change_codes) > 0:
#
#                 # todo: @laiqian 基金资产赋值给基金份额变量 ？？
#                 for code, weight in no_change_codes:
#                     target_fund_vol_dict[code] = last_fund_assets_dict[code]
#
#                 sorted(need_change_codes, key=lambda e: e[1], reverse=True)
#                 sorted(replace_codes, key=lambda e: e[1], reverse=True)
#
#                 # todo： @laiqian 不正常的FAA调仓，需要继续计算吗？
#                 if len(need_change_codes) != len(replace_codes):
#                     logging.error('fund size is not equal!', exc_info=True)
#
#                 for code, weight in no_change_codes:
#                     target_fund_vol_dict[code] = last_fund_vol_dict[code]
#
#                 for i in range(len(replace_codes)):
#                     target_fund_vol_dict[replace_codes[i][0]] = round(last_fund_assets_dict[need_change_codes[i][0]] / float(last_fund_nav_dict[replace_codes[i][0]]), Constant.VOL_NUM)
#
#             else:
#                 for fund_code, weight in fund_weight_dict.items():
#                     target_fund_vol_dict[fund_code] = last_fund_vol_dict.get(fund_code, 0)
#         return target_fund_vol_dict
#
#     def _calc_transfer_detail(self, transfer_out, transfer_record, no_changes_codes, use_rate):
#         """
#         计算转出,转入方案及调仓后份额
#         :param transfer_out:
#         :param transfer_record:
#         :return:
#         """
#         out_fund_vol, out_fund_fee, out_detail = PortfolioNavCalcUtil._calc_out_fee(self.date, self.portfolio_code, self.portfolio_type, transfer_out, self.last_fund_vol, self.last_fund_nav, self.cur_fund_nav, self.fund_rate, self.market_fund_dict, use_rate)
#         in_fund_vol, in_detail = PortfolioNavCalcUtil._calc_in_fee(self.date, self.portfolio_code, self.portfolio_type, transfer_record, out_fund_fee, self.last_fund_vol, self.last_fund_nav, self.cur_fund_nav, self.fund_rate, self.market_fund_dict, use_rate, self.is_transfer)
#
#         in_fund_vol.update(out_fund_vol)
#         in_detail.extend(out_detail)
#
#         for fund_code in no_changes_codes:
#             in_fund_vol[fund_code] = self.last_fund_vol[fund_code]
#         return in_fund_vol, in_detail
#
#     @staticmethod
#     def _calc_transfer(last_fund_assets_dict, target_fund_assets_dict):
#         """
#         计算转化后份额,及转换费率
#         适用调仓信号: 市场比例发生变化, 市场比例,产品均发生变化
#         :param last_fund_assets_dict:
#         :param target_fund_assets_dict:
#         :return:
#         """
#
#         transfer_out_dict = {}
#         transfer_in_dict = {}
#
#         no_change_list = list()
#
#         target_fund_assets_list = list()
#
#         # 计算基金转出,转入金额
#         for market_code, target_assets_dict in target_fund_assets_dict.iteritems():
#             target_fund_assets_list.extend(target_assets_dict.keys())
#
#             # todo: 不清楚这里两处排序的作用是什么？
#             target_funds_assets = sorted(target_assets_dict.items(), key=lambda e: e[0])
#             # todo: @laiqian last_fund_assets_dict资产排序可以移动到for循环之前
#             ori_funds_assets = sorted(last_fund_assets_dict.items(), key=lambda e: e[0])
#
#             for fund_code, ori_assets in ori_funds_assets:
#                 if target_assets_dict.__contains__(fund_code):
#                     if ori_assets > target_assets_dict[fund_code]:
#                         transfer_out_dict[fund_code] = round(ori_assets - target_assets_dict[fund_code], Constant.AMOUNT_NUM)
#                     elif ori_assets < target_assets_dict[fund_code]:
#                         transfer_in_dict[fund_code] = round(target_assets_dict[fund_code] - ori_assets, Constant.AMOUNT_NUM)
#
#             for fund_code, target_assets in target_funds_assets:
#                 if not last_fund_assets_dict.__contains__(fund_code):
#                     transfer_in_dict[fund_code] = target_assets
#
#         for fund_code, assets in last_fund_assets_dict.items():
#             if not transfer_out_dict.__contains__(fund_code) and (not transfer_in_dict.__contains__(fund_code) and assets != 0):
#                 if fund_code not in target_fund_assets_list:
#                     transfer_out_dict[fund_code] = assets
#                 else:
#                     no_change_list.append(fund_code)
#
#         transfer_out = sorted(transfer_out_dict.items(), key=lambda e: e[1], reverse=True)
#         transfer_in = sorted(transfer_in_dict.items(), key=lambda e: e[1])
#
#         # 计算基金一一对应的转出转入记录
#         transfer_assets_record = []
#         left_transfer_out_dict = copy.deepcopy(transfer_out_dict)
#         for in_fund, in_assets in transfer_in:
#             left_in_assets = in_assets
#             for out_fund, out_assets in transfer_out:
#                 if left_transfer_out_dict.__contains__(out_fund):
#                     left_out_assets = left_transfer_out_dict[out_fund]
#                     if left_out_assets > left_in_assets:
#                         transfer_assets_record.append((out_fund, in_fund, left_in_assets))
#                         left_transfer_out_dict[out_fund] = left_out_assets - left_in_assets
#                         break
#                     else:
#                         transfer_assets_record.append((out_fund, in_fund, round(left_out_assets, Constant.AMOUNT_NUM)))
#                         left_transfer_out_dict.pop(out_fund)
#                         left_in_assets -= left_out_assets
#                         if left_in_assets == 0:
#                             break
#                         else:
#                             continue
#         return transfer_out, transfer_assets_record, no_change_list
#
#     @staticmethod
#     def _calc_in_fee(date, portfolio_code, portfolio_type, transfer_assets_record, transfer_out_fee, last_fund_vol, last_funds_nav, cur_funds_nav, fund_rate_dict, fund_market_dict, use_rate, is_transfer=True):
#         """
#         计算转入后份额及费用
#         :param portfolio_code:
#         :param transfer_assets_record:
#         :param transfer_out_fee:
#         :param last_fund_vol:
#         :param last_funds_nav:
#         :param cur_funds_nav:
#         :param fund_rate_dict:
#         :param fund_market_dict:
#         :param is_transfer:
#         :return:
#         """
#         target_fund_vol = {}
#         transfer_program_detail = []
#         for out_fund, in_fund, transfer_assets in transfer_assets_record:
#             if not use_rate:
#                 in_rate = 0.0
#             else:
#                 in_rate = float(is_transfer and max(fund_rate_dict[in_fund]['sg'] - fund_rate_dict[out_fund]['sg'], 0) or fund_rate_dict[in_fund]['sg'])
#             # 求出赎回费中 转入这支基金所花费的赎回费
#             out_fee = transfer_assets / transfer_out_fee[out_fund][1] * transfer_out_fee[out_fund][2]
#
#             ideal_in_assets = round(transfer_assets / float(last_funds_nav[out_fund]) * float(cur_funds_nav[out_fund]) - out_fee, Constant.AMOUNT_NUM)
#             actual_in_assets = round(ideal_in_assets / (1 + in_rate), Constant.AMOUNT_NUM)
#
#             in_fee = ideal_in_assets - actual_in_assets
#             op_vol = round(actual_in_assets / float(cur_funds_nav[in_fund]), Constant.VOL_NUM)
#
#             if in_fund in target_fund_vol:
#                 target_vol = round(target_fund_vol[in_fund] + op_vol, Constant.VOL_NUM)
#             else:
#                 target_vol = round(last_fund_vol.get(in_fund, 0) + op_vol, Constant.VOL_NUM)
#
#             target_fund_vol[in_fund] = round(target_vol, Constant.VOL_NUM)
#             transfer_program_detail.append((portfolio_type, portfolio_code, date, fund_market_dict[in_fund], in_fund, is_transfer and 'zr' or 'sg', round(transfer_assets, Constant.AMOUNT_NUM), op_vol, in_fee))
#         new_transfer_program_detail = PortfolioNavCalcUtil.merge_in_fund(transfer_program_detail)
#         return target_fund_vol, new_transfer_program_detail
#
#     @staticmethod
#     def merge_in_fund(transfer_program_detail):
#         tmp_dict = dict()
#         for item in transfer_program_detail:
#             portfolio_type, portfolio_code, date, market_code, in_fund, op_type, op_amount, op_vol, in_fee = item
#             if in_fund not in tmp_dict.keys():
#                 tmp_dict[in_fund] = list(item)
#             else:
#                 tmp_dict[in_fund][-3] += op_amount
#                 tmp_dict[in_fund][-2] += op_vol
#                 tmp_dict[in_fund][-1] += in_fee
#
#         new_transfer_program_detail = [item for item in tmp_dict.values()]
#         return new_transfer_program_detail
#
#     @staticmethod
#     def _calc_out_fee(date, portfolio_code, portfolio_type, transfer_out, last_fund_vol, last_funds_nav, cur_funds_nav, fund_rate_dict, fund_market_dict, use_rate):
#         """
#         计算转出后份额及费用
#         :param portfolio_code:
#         :param transfer_out:
#         :param last_fund_vol:
#         :param last_funds_nav:
#         :param cur_funds_nav:
#         :param fund_rate_dict:
#         :param fund_market_dict:
#         :return:
#         """
#         target_fund_vol = {}
#         transfer_program_detail = []
#         transfer_out_fee = {}
#         for fund_code, out_assets in transfer_out:
#             ideal_out_vol = round(out_assets / float(last_funds_nav[fund_code]), Constant.VOL_NUM)
#             if not use_rate:
#                 out_fee = 0.0
#             else:
#                 out_fee = round(ideal_out_vol * float(cur_funds_nav[fund_code]) * float(fund_rate_dict[fund_code].get('sh', 0)), Constant.AMOUNT_NUM)
#             op_vol = round(out_assets / float(last_funds_nav[fund_code]), Constant.VOL_NUM)
#             target_vol = round(last_fund_vol[fund_code] - op_vol, Constant.VOL_NUM)
#             if out_assets != round(last_fund_vol[fund_code] * float(last_funds_nav[fund_code]), Constant.AMOUNT_NUM):
#                 target_fund_vol[fund_code] = target_vol
#             transfer_program_detail.append((portfolio_type, portfolio_code, date, fund_market_dict[fund_code], fund_code, 'sh', round(out_assets, Constant.AMOUNT_NUM), op_vol, out_fee))
#             transfer_out_fee[fund_code] = (fund_code, out_assets, out_fee)
#         return target_fund_vol, transfer_out_fee, transfer_program_detail
