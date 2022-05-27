import pandas as pd
import talib
import os

from utils.long_to_grid import long_to_grid_test
from utils.point import simpleTrend
from utils.deal import find_point
from utils.line import find_line
from utils.strategy_buy import strategy_test_buy
from chart import draw_kline
import numpy as np
from utils.small_to_large import check
from utils.strategy_sell import strategy_test_sell
from utils.util import read_first_record, exchange_record, comp_loss, chaos, launch, vol_confirm, start_grid, judge_buy, \
    judge_sell, statistics, oustanding, type_V, care, exchange_grid
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
    df["ma5"]  = talib.MA(df['close'],timeperiod=5)
    df["ma10"] = talib.MA(df['close'], timeperiod=10)
    df["ma20"] = talib.MA(df['close'], timeperiod=20)
    df["ma60"] = talib.MA(df['close'], timeperiod=60)
    df["ma120"] = talib.MA(df['close'],timeperiod=120)
    df["ema5"] = talib.EMA(df['close'], timeperiod=5)

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
    record_first = read_first_record(api['test_'+str(type)]+'/record_first.csv')
    exchange = exchange_record(api['test_' + str(type)] + '/exchange_record.csv')
    record_small = (api['test_'+str(type)]+'/record_small.csv')





    test_15 = real_data[:3000]
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


    for i, row in real_data[3000:5000].iterrows():
        if i%500 ==0:
            print(test_15.iat[-1,0])
            grid_15_chart = chart_test(test_15_simple, test_15_deal, test_15_line)
            grid_15_chart.render(api['test_' + str(type)] + '15_' + 'last' + ".html")
            grid_1h_chart = chart_test(test_1h_simple, test_1h_deal, test_1h_line)
            grid_1h_chart.render(api['test_' + str(type)] + '1h_' + 'last' + ".html")
            a =time.time()
            # print(b-a)
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
        now_close =test_15['close'].iloc[-1]

        if str(test_15.iat[-1,0]) == '2021-06-09 06:45:00':#震荡未识别 2021-12-18 21:30:00#为何买入 2022-04-25 11:45:00止损价 2022-04-30 00:00:00
            print(1)
        if str(test_15.iat[-1,0]) == '2021-06-04 00:30:00':#震荡未识别
            print(1)
        if str(test_15.iat[-1,0]) == '2021-06-04 02:15:00':#震荡未识别
            print(1)
        if test_15_line['is_test'].iloc[-1] != 'yes':
            if test_15_line['flag'].iloc[-1] =='down':
                l,result,mark_price = strategy_test_buy(test_15_simple[-1500:].reset_index(drop=True),test_15[-1500:].reset_index(drop=True),test_15_deal,test_15_line,test_1h,test_1h_deal,
                                                  test_1h_line,test_4h,test_4h_deal,test_4h_line)
            else:
                l,result,mark_price = strategy_test_sell(test_15_simple[-1500:].reset_index(drop=True),test_15[-1500:].reset_index(drop=True),test_15_deal,test_15_line,test_1h,test_1h_deal,
                                                  test_1h_line,test_4h,test_4h_deal,test_4h_line)
            if  result == 'yes':
                record_first = record_first.append(l, ignore_index=True)
                record_first.iat[-1,0] = str(test_15_line.iat[-1,0])
        rise_index = record_first[record_first['direction'] == 'min'].index.tolist()
        down_index = record_first[record_first['direction'] == 'max'].index.tolist()
        if len(rise_index)>0:
            rise_index = rise_index[-1]
        else:
            rise_index ='wrong'
        if len(down_index) > 0:
            down_index = down_index[-1]
        else:
            down_index ='wrong'

        if rise_index !='wrong'  and record_first['flag'].iloc[rise_index] == ('yes' or 'prepare') and test_15['low'].iloc[-1] < record_first['loss'].iloc[rise_index] != '':
            if exchange['direction'].iloc[-1] == 'long' and exchange['outstanding'].iloc[-1] == 'no':
                exchange['loss'].iloc[-1]=record_first['loss'].iloc[rise_index]
                exchange = oustanding(test_15, exchange, 'passive')
            record_first['flag'].iloc[rise_index] = ''
            record_first['loss'].iloc[rise_index] = ''

        if down_index !='wrong'  and record_first['flag'].iloc[down_index] == ('yes' or 'prepare') and test_15['high'].iloc[-1] > record_first['loss'].iloc[down_index] != '':
            if exchange['direction'].iloc[-1] == 'short' and exchange['outstanding'].iloc[-1] == 'no':
                exchange['loss'].iloc[-1] = record_first['loss'].iloc[down_index]
                exchange = oustanding(test_15, exchange, 'passive')
            record_first['flag'].iloc[down_index] = ''
            record_first['loss'].iloc[down_index] = ''

        if rise_index !='wrong' and record_first['flag'].iloc[rise_index] != 'no' and record_first['point'].iloc[rise_index]>test_15['low'].iloc[-1]:
            record_first['flag'].iloc[rise_index] = 'no'
        if down_index !='wrong' and record_first['flag'].iloc[down_index] != 'no' and record_first['point'].iloc[down_index]<test_15['high'].iloc[-1]:
            record_first['flag'].iloc[down_index] = 'no'

        if rise_index != 'wrong' and record_first['flag'].iloc[rise_index] == 'prepare':
            result, new_loss = care(test_15_deal, test_15_line)
            if result:
                if len(exchange)>1 and exchange['outstanding'].iloc[-1]=='no':
                    exchange = oustanding(test_15,exchange,'active')
                loss = record_first['loss'].iloc[rise_index]
                if loss>test_15['low'].iloc[-1]:
                    loss = new_loss
                #开启网格
                sl, grid = start_grid(test_15_deal, 'rise')
                if sl / now_close > 0.005 and record_first['grid'].iloc[-1] != grid:
                    record_first.loc[len(record_first)] = [str(test_15.iat[-1,0]),"", "","", "","","yes",loss,"","yes",grid,sl,0]

                else:
                    exchange = statistics(test_15,exchange,loss,'long')
                    record_first['flag'].iloc[rise_index] = 'yes'

        if down_index != 'wrong' and record_first['flag'].iloc[down_index] == 'prepare':
            result,new_loss = care(test_15_deal,test_15_line)
            if result:
                if len(exchange)>1 and exchange['outstanding'].iloc[-1]=='no':
                    exchange = oustanding(test_15,exchange,'active')
                loss = record_first['loss'].iloc[down_index]
                if loss<test_15['high'].iloc[-1]:
                    loss = new_loss
                # 开启网格
                sl, grid = start_grid(test_15_deal, 'rise')
                if sl / now_close > 0.005 and record_first['grid'].iloc[-1] != grid:
                    record_first.loc[len(record_first)] = [str(test_15.iat[-1, 0]), "", "", "", "", "", "yes", loss,
                                                           "", "yes", grid, sl, 0]
                else:
                    exchange = statistics(test_15,exchange,loss,'short')
                    record_first['flag'].iloc[down_index] = 'yes'

        if rise_index != 'wrong' and record_first['flag'].iloc[rise_index] == '':
            result,loss = judge_buy(test_15_line,record_first,test_15,test_15_deal,rise_index)
            if result == 'special' or (type_V(test_15,test_15_deal,test_15_line) == True and result == 'normal'):
                if len(exchange)>1 and exchange['outstanding'].iloc[-1]=='no':
                    exchange = oustanding(test_15,exchange,'active')
                exchange = statistics(test_15,exchange,loss,'long')
                record_first['flag'].iloc[rise_index] = 'yes'
                record_first['loss'].iloc[rise_index] = loss
            elif result == 'normal':
                record_first['flag'].iloc[rise_index] = 'prepare'
                record_first['loss'].iloc[rise_index] = loss

        if down_index != 'wrong' and record_first['flag'].iloc[down_index] == '' :
            result,loss = judge_sell(test_15_line,record_first,test_15,test_15_deal,down_index)
            if result == 'special' or (type_V(test_15,test_15_deal,test_15_line) == True and result == 'normal')  :
                if len(exchange)>1 and exchange['outstanding'].iloc[-1]=='no':
                    exchange = oustanding(test_15,exchange,'active')
                exchange = statistics(test_15,exchange,loss,'short')
                record_first['flag'].iloc[down_index] = 'yes'
                record_first['loss'].iloc[down_index] = loss

            elif result == 'normal':
                record_first['flag'].iloc[down_index] = 'prepare'
                record_first['loss'].iloc[down_index] = loss


        if record_first['is_grid'].iloc[-1] =='yes':

            gear = record_first['direction'].iloc[-1]
            grid = record_first['grid'].iloc[-1]
            sl = record_first['sl'].iloc[-1]
            base_price = grid+sl*gear
            new_gear = exchange_grid(gear,grid,sl,now_close)
            balance = int(exchange['balance'].iloc[-1])
            num = exchange['num'].iloc[-1]
            if new_gear!=gear:
                while new_gear!=gear:
                    #减/沽
                    if new_gear>gear:
                        base_price = base_price + sl
                        if gear==-2:
                            num = num * 0.5
                            balance = balance + num*base_price
                            gear+=1
                            continue
                        elif gear ==-1:
                            balance = balance + num*base_price
                            num = 0
                            gear+=1
                            continue
                        elif gear==0:
                            num = -0.5*balance/base_price
                            balance = balance*1.5
                            gear+=1
                            continue
                        elif gear==1:
                            jing = balance + num *base_price
                            num = num - 0.5*(jing)/base_price
                            balance = balance+0.5*(jing)
                            gear+=1
                            continue
                    else:
                        #买/平
                        base_price = base_price - sl

                        if gear ==-1:
                            num = num + balance/base_price
                            balance = 0
                            gear-=1
                            continue
                        elif gear==0:
                            num = 0.5*balance/base_price
                            balance = balance*0.5
                            gear-=1
                            continue
                        elif gear==1:
                            balance = balance+num*base_price
                            num = 0
                            gear-=1
                            continue
                        elif gear==2:
                            jing = balance +num*base_price
                            num = num + jing*0.5/base_price
                            balance = balance-jing*0.5
                            gear-=1
                            continue
                new = pd.DataFrame(
                    {"date": test_15["date"].iloc[-1], "direction": gear, "price": test_15['close'].iloc[-1], "loss": "",
                     "outstanding": 'no', "balance": balance, "num": num, "situation": "active", "close_price": ""}, index=[1])
                exchange = exchange.append(new, ignore_index=True)
                record_first['direction'].iloc[-1] = gear










        # if len(exchange)>1:
        #     if exchange['loss'].iloc[-1]==31466.19 and exchange['direction'].iloc[-1]=='short':
        #         print(test_15.iat[-1,0])



        # if exchange['outstanding'].iloc[-1]!='no':
        #     if exchange['direction'].iloc[-1]=='long' and exchange['loss'].iloc[-1]<test_15['low'].iloc[-1]:
        #         exchange = oustanding(test_15, exchange, 'passive')
        #     elif exchange['direction'].iloc[-1]=='short' and exchange['loss'].iloc[-1]>test_15['high'].iloc[-1]:
        #         exchange = oustanding(test_15, exchange, 'passive')

        # long_to_grid_test(test_15_simple[-1500:].reset_index(drop=True),test_15[-1500:].reset_index(drop=True),test_15_deal,test_15_line,test_1h_line,record_first)
        # # if record_first['flag'].iloc[-1] == 'yes' and test_15['close'].iloc[-1] < test_15['close'].iloc[-19] :
        # #     print('准备网格 '+str(test_15.iat[-1, 0]) )
        #
        #
        # if len(test_15_line) > 3 and len(record_first) > 1 and record_first['flag'].iloc[-1] != 'yes' and\
        #          chaos(test_15_deal,'rise') == True and record_first['flag'].iloc[-1] != 'no' and test_15_deal["flag"].iloc[-1] =='max':
        #         sl, grid = grid(test_15_deal, 'rise')
        #         if sl / test_15['close'].iloc[-1] > 0.005 and record_first['grid'].iloc[-1] != grid:
        #             print('网格: ' + str(test_15.iat[-1, 0]) + ' 点位:' + str(grid) + ' 密度:' + str(sl) + ' ' + str(
        #                 grid + sl) + ' ' + str(grid + 2 * sl) + ' ' + str(grid - sl) + ' ' + str(grid - 2 * sl))
        #             record_first['grid'].iloc[-1] = grid


    grid_15_chart = chart_test(test_15_simple, test_15_deal, test_15_line)
    grid_15_chart.render(api['test_'+str(type)] + '15_' + 'last' + ".html")
    grid_1h_chart = chart_test(test_1h_simple, test_1h_deal, test_1h_line)
    grid_1h_chart.render(api['test_'+str(type)] + '1h_' + 'last' + ".html")
    grid_4h_chart = chart_test(test_4h_simple, test_4h_deal, test_4h_line)
    grid_4h_chart.render(api['test_'+str(type)] + '4h_' + 'last' + ".html")
    record_first.to_csv(api['test_'+str(type)]+'/record_first.csv', index=False)
    exchange.to_csv(api['test_'+str(type)]+'/exchange_record.csv', index=False)


