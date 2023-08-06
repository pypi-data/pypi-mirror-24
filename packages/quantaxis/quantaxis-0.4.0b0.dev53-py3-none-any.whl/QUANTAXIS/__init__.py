#coding :utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
QUANTAXIS

Quantitative Financial Strategy Framework

by yutiansut    

2017/4/8
"""
__version__ = '0.4.0.b.dev53'
__author__ = 'yutiansut'

# fetch methods

from QUANTAXIS.QAFetch import (QA_fetch_get_stock_day, QA_fetch_get_trade_date, QA_fetch_get_stock_min,
                               QA_fetch_get_stock_indicator, QA_fetch_get_stock_realtime, QA_fetch_get_stock_transaction)
from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_trade_date, QA_fetch_stock_day, QA_fetch_stocklist_day, QA_fetch_index_day,
                                       QA_fetch_stock_min, QA_fetch_future_min, QA_fetch_future_day, QA_fetch_future_tick,
                                       QA_fetch_stock_list, QA_fetch_stock_full)


# save
from QUANTAXIS.QASU.main import (QA_SU_save_stock_list, QA_SU_save_stock_day, QA_SU_save_stock_info, QA_SU_save_stock_min_5,
                                 QA_SU_save_stock_day_init,  QA_SU_save_trade_date, QA_SU_update_stock_day, QA_SU_save_stock_fqfactor)
from QUANTAXIS.QASU.save_backtest import (
    QA_SU_save_account_message, QA_SU_save_backtest_message, QA_SU_save_account_to_csv)
from QUANTAXIS.QASU.save_tushare import (
    QA_save_stock_day_all, QA_SU_save_trade_date_all)


from QUANTAXIS.QASU.user import (QA_user_sign_in, QA_user_sign_up)
# event driver

# market

from QUANTAXIS.QAMarket import (QA_QAMarket_bid, QA_Market)

# Account,Risk,Portfolio

from QUANTAXIS.QAARP import QA_Account, QA_Portfolio, QA_Risk
from QUANTAXIS.QAARP.QARisk import (QA_risk_account_freeCash_currentAssest,
                                    QA_risk_account_freeCash_frozenAssest,
                                    QA_risk_account_freeCash_initAssest, QA_risk_eva_account)
# Backtest
from QUANTAXIS.QABacktest.QABacktest import QA_Backtest, QA_Backtest_min
from QUANTAXIS.QABacktest.QABacktest_stock_day import QA_Backtest_stock_day
from QUANTAXIS.QABacktest.QAAnalysis import QA_backtest_analysis_start
# task
from QUANTAXIS.QATask import QA_Queue, QA_Event

# Data
from QUANTAXIS.QAData import QA_data_fq_factor,QA_data_tick_resample


# Util
from QUANTAXIS.QAUtil.QAType import (
    QA_util_ensure_date, QA_util_ensure_dict, QA_util_ensure_ms, QA_util_ensure_timeSerires)


from QUANTAXIS.QAUtil import (QA_util_date_stamp, QA_util_time_stamp, QA_util_ms_stamp, QA_util_date_valid,
                              QA_util_realtime, QA_util_id2date, QA_util_is_trade, QA_util_get_date_index,
                              QA_util_get_index_date, QA_util_select_hours,
                              QA_util_select_min, QA_util_time_delay, QA_util_time_now, QA_util_date_str2int,
                              QA_util_date_int2str,
                              QA_util_sql_mongo_setting,
                              QA_util_log_debug, QA_util_log_expection, QA_util_log_info,
                              QA_util_cfg_initial, QA_util_get_cfg,
                              QA_Setting,
                              QA_util_web_ping,
                              trade_date_sse, QA_util_if_trade,
                              QA_util_get_real_datelist, QA_util_get_real_date,
                              QA_util_get_trade_range,
                              QA_util_save_csv,
                              QA_util_multi_demension_list, QA_util_diff_list,
                              QA_util_to_json_from_pandas, QA_util_to_list_from_numpy, QA_util_to_list_from_pandas,
                              QA_util_mongo_initial, QA_util_mongo_make_index,
                              QA_util_make_15min_bar, QA_util_make_1h_bar,
                              QA_util_make_1min_bar, QA_util_make_5min_bar,
                              QA_util_make_30min_bar, QA_util_make_bar)

from QUANTAXIS.QAIndicator import *
from QUANTAXIS.QASQL import qasql, qacold
#from QUANTAXIS.QAWeb import QA_Web
# CMD and Cli
import QUANTAXIS.QACmd

from QUANTAXIS.QACmd import QA_cmd
import argparse


# 检查python版本
import sys
if sys.version_info.major != 3 or sys.version_info.minor != 6:
    print('wrong version, should be 3.6 version')
    sys.exit()


QA_util_log_info('Welcome to QUANTAXIS, the Version is ' + __version__)
QA_util_log_info(' \n \
```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` \n \
 ``########`````##````````##``````````##`````````####````````##```##########````````#``````##``````###```##`````######`` \n \
 `##``````## ```##````````##`````````####````````##`##```````##```````##```````````###``````##````##`````##```##`````##` \n \
 ##````````##```##````````##````````##`##````````##``##``````##```````##``````````####```````#```##``````##```##``````## \n \
 ##````````##```##````````##```````##```##```````##```##`````##```````##`````````##`##```````##`##```````##````##``````` \n \
 ##````````##```##````````##``````##`````##``````##````##````##```````##````````##``###```````###````````##`````##`````` \n \
 ##````````##```##````````##``````##``````##`````##`````##```##```````##```````##````##```````###````````##``````###```` \n \
 ##````````##```##````````##`````##````````##````##``````##``##```````##``````##``````##`````##`##```````##````````##``` \n \
 ##````````##```##````````##````#############````##```````##`##```````##`````###########`````##``##``````##`````````##`` \n \
 ###```````##```##````````##```##```````````##```##```````##`##```````##````##`````````##```##```##``````##```##`````##` \n \
 `##``````###````##``````###``##`````````````##``##````````####```````##```##``````````##``###````##`````##````##`````## \n \
 ``#########``````########```##``````````````###`##``````````##```````##``##````````````##`##``````##````##`````##````## \n \
 ````````#####`````````````````````````````````````````````````````````````````````````````````````````````````````####` \n \
 ``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` \n \
 ``````````````````````````Copyright``yutiansut``2017``````QUANTITATIVE FINANCIAL FRAMEWORK````````````````````````````` \n \
 ``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` \n \
```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` \n \
```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` \n ')
