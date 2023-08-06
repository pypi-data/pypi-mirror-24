# coding :utf-8
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

#from .market_config import stock_market,future_market,HK_stock_market,US_stock_market
import datetime
import random

from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_future_day,
                                       QA_fetch_future_min,
                                       QA_fetch_future_tick,
                                       QA_fetch_index_day, QA_fetch_stock_day,
                                       QA_fetch_stock_min)
from QUANTAXIS.QAUtil import (QA_Setting, QA_util_log_info,
                              QA_util_sql_mongo_setting)

from .QAMarket_engine import (market_future_day_engine,
                              market_future_min_engine,
                              market_future_tick_engine,
                              market_stock_day_engine, market_stock_min_engine)


class QA_Market():

    # client=QA_Setting.client
    # client=QA.QA_util_sql_mongo_setting()
    # db= client.market
    def __init__(self):
        self.engine = {'stock_day': QA_fetch_stock_day, 'stock_min': QA_fetch_stock_min,
                       'future_day': QA_fetch_future_day, 'future_min': QA_fetch_future_min, 'future_tick': QA_fetch_future_tick}

    def _choice_trading_market(self, __bid, client):
        assert isinstance(__bid['status'], str)
        if __bid['status'] == '0x01':
            return market_stock_day_engine(__bid, fp=None)
        elif __bid['status'] == '0x02':
            return market_stock_min_engine(__bid, client)
        elif __bid['status'] == '1x01':
            return market_future_day_engine(__bid, client)
        elif __bid['status'] == '1x02':
            return market_future_min_engine(__bid, client)
        elif __bid['status'] == '1x03':
            return market_future_tick_engine(__bid, client)

    def receive_bid(self, __bid, client):
        """
        get the bid and choice which market to trade

        """
        def __confirm_bid(__bid):
            assert isinstance(__bid, dict)
            if isinstance(__bid['price'], str):
                if __bid['price'] == 'market_price':
                    return __bid
                elif __bid['price'] == 'close_price':
                    return __bid
                elif __bid['price'] == 'strict' or 'strict_model' or 'strict_price':
                    __bid['price']='strict_price'
                    return __bid
                else:
                    QA_util_log_info('unsupport type:' + __bid['price'])
                    return __bid
            else:
                return __bid
        return self._choice_trading_market(__confirm_bid(__bid), client)

    def trading_engine(self):
        pass
