import pandas as pd
import talib
import os
from utils.point import simpleTrend
from utils.deal import find_point
from utils.line import find_line
from utils.strategy_buy import strategy_test
from chart import draw_kline
import numpy as np
from utils.small_to_large import check
from utils.util import read_record
import time

def chart_test(df,deal,line):
    grid_chart = draw_kline(df,deal,line)
    return grid_chart

def stock_macd(df) -> pd.DataFrame:
    if len(df)<36:
        return df
    if 'macd' not in df.columns:
        df = macd(df)
        return df
    else:
        df_temp = df[33:]
        index = df_temp[df_temp['macd'] == ''].index.tolist()
        if index!=[]:
            df_normal = df[index[0]-33:]
            df_normal = macd(df_normal)
            df = df[:index[0]].append(df_normal[33:])
        else:
            index = np.isnan(df_temp['macd'])
            index = index[index == True].index.tolist()
            if index != []:
                df_normal = df[index[0] - 33:]
                df_normal = macd(df_normal)
                df = df[:index[0]].append(df_normal[33:])
        return df

def macd(df):
    df = df.copy()
    diff, dea, macd = talib.MACD(df["close"],
                                 fastperiod=12,
                                 slowperiod=26,
                                 signalperiod=9)
    df["diff"] = round(diff, 2)
    df["dea"] = round(dea, 2)
    df["macd"] = round(macd * 2, 2)
    return df

def csv_resample(df, rule) -> pd.DataFrame:
    # 重新采样Open列数据
    df_open = round(df['open'].resample(rule=rule, closed='left', label='left').first(), 2)
    df_high = round(df['high'].resample(rule=rule, closed='left', label='left').max(), 2)
    df_low = round(df['low'].resample(rule=rule, closed='left', label='left').min(), 2)
    df_close = round(df['close'].resample(rule=rule, closed='left', label='left').last(), 2)
    df_volume = round(df['vol'].resample(rule=rule, closed='left', label='left').sum(), 2)
    # print("新周期数据已生成")
    # 生成新周期数据
    df_15t = pd.DataFrame()
    df_15t = df_15t.assign(open=df_open)
    df_15t = df_15t.assign(high=df_high)
    df_15t = df_15t.assign(low=df_low)
    df_15t = df_15t.assign(close=df_close)
    df_15t = df_15t.assign(vol=df_volume)
    # 去除空值
    df_15t = df_15t.dropna()

    return df_15t


def import_csv(df,rule,data =pd.DataFrame(),flag = '') -> pd.DataFrame:
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    if flag =='init':
        df =df.copy()
        df = df.set_index(['date'])
        df = csv_resample(df, rule)
        df = stock_macd(df)
        df.reset_index(inplace=True)
        return df
    else:
        i=-2
        try:
            index = df[df['date'] == data['date'].iloc[i]].index.tolist()[0]
        except:
            i=-4
            index = df[df['date'] == data['date'].iloc[i]].index.tolist()[0]
        df = df[index:].copy()
        df = df.set_index(['date'])
        df = csv_resample(df, rule)
        data.drop(data.tail(abs(i)).index, inplace=True)
        df.reset_index(inplace=True)
        df = data.append(df).reset_index(drop=True)
        df = stock_macd(df)
        return df


def test(type,api):
    real_data = pd.read_csv(api[str(type)]+'/normal_15m.csv')
    test_normal_15_path = api['test_'+str(type)]+'/normal_15m.csv'
    test_normal_1h_path = api['test_'+str(type)]+'/normal_1h.csv'
    test_normal_4h_path = api['test_'+str(type)]+'/normal_4h.csv'
    test_simple_15_path = api['test_'+str(type)]+'/simple_15m.csv'
    test_simple_1h_path = api['test_'+str(type)]+'/simple_1h.csv'
    test_simple_4h_path = api['test_'+str(type)]+'/simple_4h.csv'
    test_deal_15_path = api['test_'+str(type)]+'/deal_15m.csv'
    test_deal_1h_path = api['test_'+str(type)]+'/deal_1h.csv'
    test_deal_4h_path = api['test_'+str(type)]+'/deal_4h.csv'
    test_line_15_path = api['test_'+str(type)]+'/line_15m.csv'
    test_line_1h_path = api['test_'+str(type)]+'/line_1h.csv'
    test_line_4h_path = api['test_'+str(type)]+'/line_4h.csv'
    record_first = read_record(api['test_'+str(type)]+'/record_first.csv')
    record_second = (api['test_'+str(type)]+'/record_second.csv')
    record_small = (api['test_'+str(type)]+'/record_small.csv')





    test_15 = real_data[:5500]
    test_15 = test_15.reset_index(drop=True)
    test_1h = import_csv(test_15, '1H','','init')
    test_4h = import_csv(test_15, '4H','','init')

    test_15_simple = test_15.iloc[0:10, 0:7].copy()
    test_1h_simple = test_1h.iloc[0:10, 0:7].copy()
    test_4h_simple = test_4h.iloc[0:10, 0:7].copy()

    if not os.path.exists(test_deal_15_path ):
        test_15_deal = pd.DataFrame(columns=['date','key','flag','temp'])
        test_1h_deal = pd.DataFrame(columns=['date','key','flag','temp'])
        test_4h_deal = pd.DataFrame(columns=['date','key','flag','temp'])
        test_15_line = pd.DataFrame(columns=['date', 'key', 'flag', 'temp','small_to_large','first','second','is_test'])
        test_1h_line = pd.DataFrame(columns=['date', 'key', 'flag', 'temp','small_to_large','first','second','is_test'])
        test_4h_line = pd.DataFrame(columns=['date', 'key', 'flag', 'temp','small_to_large','first','second','is_test'])

    else:
        test_15_deal = pd.read_csv(test_deal_15_path)
        test_1h_deal = pd.read_csv(test_deal_1h_path)
        test_4h_deal = pd.read_csv(test_deal_4h_path)
        test_15_line = pd.read_csv(test_line_15_path)
        test_1h_line = pd.read_csv(test_line_1h_path)
        test_4h_line = pd.read_csv(test_line_4h_path)


    test_1h = import_csv(test_15, '1H', test_1h)
    test_15_simple = simpleTrend(test_15, test_15_simple)
    test_1h_simple = simpleTrend(test_1h, test_1h_simple)
    test_15_deal = find_point(test_15_simple, test_15_deal)
    test_1h_deal = find_point(test_1h_simple, test_1h_deal)
    test_15_line = find_line(test_15_deal, test_15_line)
    test_1h_line = find_line(test_1h_deal, test_1h_line)
    b =time.time()


    for i, row in real_data[5500:].iterrows():
        if i%500 ==0:
            print(test_15.iat[-1,0])
            grid_15_chart = chart_test(test_15_simple, test_15_deal, test_15_line)
            grid_15_chart.render(api['test_' + str(type)] + '15_' + 'last' + ".html")
            grid_1h_chart = chart_test(test_1h_simple, test_1h_deal, test_1h_line)
            grid_1h_chart.render(api['test_' + str(type)] + '1h_' + 'last' + ".html")
            a =time.time()
            print(b-a)
            b=time.time()
        # if i == 4307:
            print(i)
        test_15 = test_15.append(row).reset_index(drop=True)

        test_15_simple =simpleTrend(test_15,test_15_simple)
        if str(test_15.iat[-1,0]).endswith('15:00'):
            test_1h_simple =simpleTrend(test_1h[:-1],test_1h_simple[:-2])
        else:
            test_1h_simple = test_1h_simple[:-1]
        test_1h = import_csv(test_15, '1H', test_1h)
        test_1h_simple = test_1h_simple.append(test_1h.iloc[-1], ignore_index=True)
        test_15_deal = find_point(test_15_simple[-1000:].reset_index(drop=True), test_15_deal)
        test_1h_deal = find_point(test_1h_simple[-1000:].reset_index(drop=True), test_1h_deal)
        # append_index = test_1h[test_1h['date']>test_1h_simple['date'].iloc[-1]].index.tolist()

        test_15_line = find_line(test_15_deal , test_15_line)
        test_1h_line = find_line(test_1h_deal , test_1h_line)
        # test_4h = import_csv(test_15, '4H')
        # test_4h_simple =simpleTrend(test_4h,test_4h_simple)
        # test_4h_deal = find_point(test_4h_simple, test_4h_deal)
        #
        # test_4h_line = find_line(test_4h_deal , test_4h_line)

        if str(test_15.iat[-1,0]) == '2021-06-22 14:00:00':
            print(1)
        if str(test_15.iat[-1,0]) == '2022-01-01 02:45:00':
            print(1)
        if str(test_15.iat[-1,0]) == '2022-01-01 03:00:00':
            print(1)

        result,mark_price = strategy_test(test_15_simple[-1500:].reset_index(drop=True),test_15[-1500:].reset_index(drop=True),test_15_deal,test_15_line,test_1h,test_1h_deal,
                                          test_1h_line,test_4h,test_4h_deal,test_4h_line)
        # if  result == 'yes':
        #     record_first.loc[len(record_first)] = [test_15.iat[- 1, 0], mark_price,test_15.iat[- 1, 2],"", "", test_15.iat[- 2, 2], ""]
        # if test_15_line.iloc[-1]["small_to_large"] =='yes' or test_15_line.iloc[-2]["small_to_large"] =='yes':
        #     result ,date,mark_price = check(test_15_deal,test_15_line)
        #     if result == 'yes':
        #         record_small.loc[len(record_small)] = [test_15.iat[- 1, 0], mark_price, test_15.iat[- 1, 2],"", "", test_15.iat[- 2, 2], ""]
        #         print('small to buy :' + ' '+str(i) + ' '+date+' now date'+ str(test_15.iat[-1,0]))


    grid_15_chart = chart_test(test_15_simple, test_15_deal, test_15_line)
    grid_15_chart.render(api['test_'+str(type)] + '15_' + 'last' + ".html")
    grid_1h_chart = chart_test(test_1h_simple, test_1h_deal, test_1h_line)
    grid_1h_chart.render(api['test_'+str(type)] + '1h_' + 'last' + ".html")
    # grid_4h_chart = chart_test(test_4h_simple, test_4h_deal, test_4h_line)
    # grid_4h_chart.render(api['test_'+str(type)] + '4h_' + 'last' + ".html")
    record_first.to_csv(api['test_'+str(type)]+'/record_first.csv', index=False)

