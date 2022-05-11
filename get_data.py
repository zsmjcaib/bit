# coding=utf-8
import yaml
import ccxt
import pandas as pd
import time
from datetime import datetime
from utils.deal import find_point
from utils.line import find_line
from chart import draw_kline
from utils.util import stock_macd
from utils.point import simpleTrend
# from binance.spot import Spot









# client = Spot()
# # Get server timestamp
# print(client.time())
# # Get klines of BTCUSDT at 1m interval
# print(client.klines("BTCUSDT", "15m", limit=10,startTime = 1587708406000,endTime = 1590300406000))
# # Get last 10 klines of BNBUSDT at 1h interval
# print(client.klines("BNBUSDT", "1h", limit=10))
def get_time_stamp(timestr):
    # timestr = '2022-04-24 14:30:00'
    datetime_obj = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
    obj_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
    return obj_stamp

def get_data(freq,strat):

        since = get_time_stamp(strat)
        data = pd.DataFrame( columns=['date', 'open', 'high', 'low', 'close', 'vol'])
        while True:
            response = exchange.fetch_ohlcv('BTC/USDT', str(freq), since=since, limit=1000)
            df = pd.DataFrame(response, columns=['date', 'open', 'high', 'low', 'close', 'vol'])
            data = data.append(df,ignore_index=True)
            since = df.iat[-1,0]
            data = data[:-1]
            if len(df)<1000:
                break

        data['date'] = pd.to_datetime(data['date'], unit='ms')
        return data

if __name__ == '__main__':
    with open('api.yaml') as f:
        api = yaml.load(f, Loader=yaml.FullLoader)
        f.close()
    # exchange_id = 'binance'
    # exchange_class = getattr(ccxt, exchange_id)
    exchange = ccxt.binance()
    for i in['15m','1h','4h']:
        data = get_data(i, '2021-04-24 14:30:00')
        data = stock_macd(data)
        data.to_csv(api['btc']+'/normal_'+str(i)+'.csv',index=False)
        # data = pd.read_csv(api['btc']+'/normal_'+str(i)+'.csv')
        # data_simple = data[:7]
        # data_simple = simpleTrend(data,data_simple)
        # data_simple.to_csv(api['btc']+'/simple_'+str(i)+'.csv',index=False)
        # data_simple = pd.read_csv(api['btc']+'/simple_'+str(i)+'.csv')
        # data_deal = pd.DataFrame(columns=['date', 'key', 'flag', 'temp'])
        # data_deal = find_point(data_simple, data_deal)
        # data_deal.to_csv(api['btc'] + '/deal_' + str(i) + '.csv', index=False)
        # data_deal = pd.read_csv(api['btc'] + '/deal_' + str(i) + '.csv')
        # data_line = pd.DataFrame(columns=['date', 'key', 'flag', 'temp','small_to_large','first','second','is_test'])
        # data_line = find_line(data_deal, data_line)
        # data_line.to_csv(api['btc']+'/line_'+str(i)+'.csv',index=False)
        # data_line = pd.read_csv(api['btc']+'/line_'+str(i)+'.csv')
        # chart = draw_kline(data_simple,data_deal,data_line)
        # chart.render(api['btc']+'/chart_'+str(i) + ".html")
