# coding: utf-8
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

import json

import tushare as QATs

from QUANTAXIS.QAUtil import QA_util_date_stamp, QA_util_log_info


def QA_fetch_get_stock_day(name, startDate='', endDate='', if_fq='01'):
    if (len(name) != 6):
        name = str(name)[0:6]

    if if_fq in ['qfq', '01']:
        if_fq = 'qfq'
    elif if_fq in ['hfq', '02']:
        if_fq = 'hfq'
    elif if_fq in ['bfq', '00']:
        if_fq = 'bfq'
    else:
        QA_util_log_info('wrong with fq_factor! using qfq')
    data = QATs.get_k_data(str(name), startDate, endDate,
                           ktype='D', autype=if_fq).sort_index()

    data_json = json.loads(data.to_json(orient='records'))

    for j in range(0, len(data_json), 1):
        data_json[j]['date_stamp'] = QA_util_date_stamp(
            list(data['date'])[j])
        data_json[j]['fqtype']=if_fq
    return data_json

    """
    if (len(name) != 6):
        name = str(name)[0:6]
    data = QATs.get_hist_data(str(name), startDate, endDate).sort_index()

    data_json = json.loads(data.to_json(orient='records'))

    for j in range(0, len(data_json), 1):
        data_json[j]['date_stamp'] = QA_util_date_stamp(
            list(data.index)[j])
        data_json[j]['date'] = list(data.index)[j]
        data_json[j]['code'] = str(name)

    return data_json
    """


def QA_fetch_get_stock_realtime():
    data = QATs.get_today_all()
    data_json = json.loads(data.to_json(orient='records'))
    return data_json


def QA_fetch_get_stock_info(name):
    data = QATs.get_stock_basics()
    data_json = json.loads(data.to_json(orient='records'))

    for i in range(0, len(data_json) - 1, 1):
        data_json[i]['code'] = data.index[i]
    return data_json


def QA_fetch_get_stock_tick(name, date):
    if (len(name) != 6):
        name = str(name)[0:6]
    return QATs.get_tick_data(name, date)


def QA_fetch_get_stock_list():
    df = QATs.get_stock_basics()
    return list(df.index)


def QA_fetch_get_trade_date(endDate, exchange):
    data = QATs.trade_cal()
    da = data[data.isOpen > 0]
    data_json = json.loads(da.to_json(orient='records'))
    message = []
    for i in range(0, len(data_json) - 1, 1):
        date = data_json[i]['calendarDate']
        num = i + 1
        exchangeName = 'SSE'
        data_stamp = QA_util_date_stamp(date)
        mes = {'date': date, 'num': num,
               'exchangeName': exchangeName, 'date_stamp': data_stamp}
        message.append(mes)
    return message

# test

# print(get_stock_day("000001",'2001-01-01','2010-01-01'))
# print(get_stock_tick("000001.SZ","2017-02-21"))
