import talib
import os
import pandas as pd
import copy
import datetime
from copy import deepcopy

def stock_macd(df):

    diff, dea, macd = talib.MACD(df["close"],
                                    fastperiod=12,
                                    slowperiod=26,
                                    signalperiod=9)
    df = df.copy()
    df["diff"]=round(diff*2,2)
    df["dea"] = round(dea*2,2)
    df["macd"] = round(macd*2,2)
    df["ma5"]  = talib.MA(df['close'],timeperiod=5)
    df["ma10"] = talib.MA(df['close'], timeperiod=10)
    df["ma20"] = talib.MA(df['close'], timeperiod=20)
    df["ma60"] = talib.MA(df['close'], timeperiod=60)
    df["ma120"] = talib.MA(df['close'],timeperiod=120)
    df["ema5"] = talib.EMA(df['close'], timeperiod=5)
    df["ema10"] = talib.EMA(df['close'], timeperiod=10)
    df["ema20"] = talib.EMA(df['close'], timeperiod=20)
    df["short"] = df.iloc[:,9:12].std(axis=1)/df['close']*100
    df["mid"] = df.iloc[:,10:13].std(axis=1)/df['close']*100
    df["long"] = df.iloc[:,11:14].std(axis=1)/df['close']*100
    df["short_ma"] = talib.MA(df['short'],timeperiod=5)
    df["mid_ma"] = talib.MA(df['mid'],timeperiod=5)
    df["long_ma"] = talib.MA(df['long'],timeperiod=5)
    df["vol_ma"] = talib.MA(df['vol'],timeperiod=480)
    return df

def read_first_record(path):
    if not os.path.exists(path ):
        demo = pd.DataFrame(columns=['date','first','15m','1h','15m小转大','1h小转大','flag','loss','point','is_grid','grid','sl','direction'])
        demo.loc[len(demo)] = [ "1997","", "","", "","","","","","","","",""]
    else:
        demo = pd.DataFrame(columns=['date', 'first', '15m', '1h', '15m小转大', '1h小转大', 'flag','loss','point','is_grid','grid','sl','direction'])
        demo.loc[len(demo)] = [ "1997","", "","", "","","","","","","","",""]
        # demo = pd.read_csv(path )
    return demo

def exchange_record(path):
    if not os.path.exists(path):
        demo = pd.DataFrame(columns=['date', 'direction', 'base_num', 'loss', 'outstanding', 'balance','num','situation','close_price','assets'
                                     ,'order_1','order_1_num','order_2','order_2_num','order_3','order_3_num','order_4','order_4_num','order_5','order_5_num'])
        demo.loc[len(demo)] = ["", "", "", "", "yes",  100000,0,"","","","",0,"",0,"",0,"",0,"",0]
    else:
        demo = pd.DataFrame(columns=['date', 'direction', 'base_num', 'loss', 'outstanding', 'balance','num','situation','close_price','assets'
                                     ,'order_1','order_1_num','order_2','order_2_num','order_3','order_3_num','order_4','order_4_num','order_5','order_5_num'])
        demo.loc[len(demo)] = ["", "", "", "", "yes",  100000,0,"","","","",0,"",0,"",0,"",0,"",0]
    return demo
def comp_loss(normal,date,flag):
    index = normal[normal['date'] == date].index.tolist()[-1]
    if flag == 'rise':
        for i in range(index,len(normal)-1):
            if normal['ma5'].iloc[i] < normal['close'].iloc[i]:
                return normal['open'].iloc[i]
    else:
        for i in range(index, len(normal) - 1):
            if normal['ma5'].iloc[i] > normal['close'].iloc[i]:
                return normal['open'].iloc[i]
    return 0

def chaos(deal,flag):
    temp = copy.deepcopy(deal[-20:])
    if flag == 'rise':
        if temp["temp"].iloc[-1] =='yes' and temp["flag"].iloc[-1] =='min':
            temp.drop(temp.tail(1).index,inplace=True)
        max4,min4,max3, min3, max2, min2, _, _, max1, min1 = temp['key'][-11:-1]
        return judge(min1, max1,min2, max2, min3, max3,min4,max4,'rise')
    if flag == 'down':
        if temp["temp"].iloc[-1] =='yes' and temp["flag"].iloc[-1] =='max':
            temp.drop(temp.tail(1).index,inplace=True)
        min4,max4,min3, max3, min2, max2,_, _,  min1, max1 = temp['key'][-11:-1]
        return judge(min1, max1,min2, max2, min3, max3,min4,max4,'down')
    return False

def judge(min1, max1,min2, max2, min3, max3,min4,max4,flag):

    if flag == 'rise':
        ratio1 = calcul(min1, max1, min2, max2)
        ratio2 = calcul(min1, max1, min3, max3)
        ratio3 = calcul(min1, max1, min4, max4)

        if ratio1>0.6 or ratio2>0.6 or ratio3>0.6 :
            return True
    else:
        ratio1 = calcul(min1, max1, min2, max2)
        ratio2 = calcul(min1, max1, min3, max3)
        ratio3 = calcul(min1, max1, min4, max4)

        if ratio1>0.6 or ratio2>0.6 or ratio3>0.6 :
            return True
    return False

def calcul(min1, max1,min2, max2):
    abs1 = abs(max1 - min1)
    flag_max1 = min(max1 , max2)
    flag_min1 = max (min1 , min2)
    if flag_max1>flag_min1:
        dif = abs(flag_max1 - flag_min1)
        ratio = dif/abs1
        return ratio
    return 0
def launch(normal,flag):
    #持续性检验
    l = [-1,-3,-4,-5]
    if flag == 'rise':
        for i in range(0,len(l)-1):
            if normal['ma5'].iloc[l[i]]<normal['ma5'].iloc[l[i+1]] or normal['ma10'].iloc[l[i]]<normal['ma10'].iloc[l[i+1]]:

                # or normal['ma20'].iloc[l[i]]<normal['ma20'].iloc[l[i+1]]: 忽略20日
                return False
            else:
                continue
    else:
        for i in range(0,len(l)-1):
            if normal['ma5'].iloc[l[i]]>normal['ma5'].iloc[l[i+1]] or normal['ma10'].iloc[l[i]]>normal['ma10'].iloc[l[i+1]]:
                # or normal['ma20'].iloc[l[i]]>normal['ma20'].iloc[l[i+1]]:
                return False
            else:
                continue
    return True
def vol_confirm(normal):
    if normal[-5:]['vol'].mean() > normal['vol_ma'].iloc[-1]*1.3 or normal[-5:]['vol'].max() >normal['vol_ma'].iloc[-1]*1.8:
        return True
    return False

def start_grid(deal,flag):
    temp = copy.deepcopy(deal[-20:])
    if flag == 'rise':
        if temp["temp"].iloc[-1] =='yes' and temp["flag"].iloc[-1] =='min':
            temp.drop(temp.tail(1).index,inplace=True)
        max4, min4, max3, min3, max2, min2, max1, min1 = temp['key'][-9:-1]
        return find_grid(max4, min4, max3, min3, max2, min2, max1, min1)

def find_grid(max4, min4, max3, min3, max2, min2, max1, min1):
    abs1 = abs(max1 - min1)
    abs2 = abs(max2 - min2)
    abs3 = abs(max3 - min3)
    abs4 = abs(max4 - min4)
    l = [abs1,abs2,abs3,abs4]
    l.sort(reverse = True)
    sl =round((l[1]+l[2])/6,2)
    grid = round((max1 + min1)/3+(max2+min2)/6,2)
    return sl,grid

def judge_buy(test_15_line,record_first,test_15,test_15_deal,rise_index):
    if len(test_15_line) > 3 and len(record_first) > 1 and record_first['flag'].iloc[rise_index] != 'yes' and\
            test_15['close'].iloc[-1] > test_15['close'].iloc[-20] \
            and test_15['close'].iloc[-1] > test_15['close'].iloc[-19] and record_first['flag'].iloc[rise_index] != 'no' and\
            record_first['point'].iloc[rise_index] < test_15['low'].iloc[-1]:
        if (test_15['ma5'].iloc[-1] > test_15['ma10'].iloc[-1] or test_15['close'].iloc[-1] > test_15['close'].iloc[
            -5]) and test_15['ema5'].iloc[-1] < test_15['close'].iloc[-1] \
                and (test_15['open'].iloc[-1] < test_15['close'].iloc[-1] or test_15['close'].iloc[-1] > (
                test_15['open'].iloc[-1] + test_15['close'].iloc[-1]) / 2):
            if chaos(test_15_deal, 'rise') == False:
                loss = comp_loss(test_15, record_first.iat[rise_index, 0], 'rise')
                if loss != 0:
                    print('buy: ' + str(test_15.iat[-1, 0]) + ' price: ' + str(
                        test_15['close'].iloc[-1]) + ' loss: ' + str(loss) + ' ' + str(test_15['short'].iloc[-1]))
                    record_first['loss'].iloc[rise_index] = loss
                    record_first['flag'].iloc[rise_index] = 'yes'
                    return 'normal',loss
            else:
                if test_15['ma5'].iloc[-1]>test_15['ma10'].iloc[-1]>test_15['ma20'].iloc[-1] \
                        and test_15['ma5'].iloc[-1]>test_15['ma60'].iloc[-1] and test_15['ma5'].iloc[-1]>test_15['ma120'].iloc[-1]:
                    if launch(test_15,'rise') and vol_confirm(test_15) and test_15['short'].iloc[-1]>0.1:
                        loss = comp_loss(test_15,record_first.iat[rise_index,0],'rise')
                        if loss != 0:
                            print('buy: ' + str(test_15.iat[-1, 0]) + ' price: ' + str(test_15['close'].iloc[-1]) + ' loss: ' + str(loss) +'多头排列'+' '+str(test_15['short'].iloc[-1]))
                            record_first['loss'].iloc[rise_index] = loss
                            record_first['flag'].iloc[rise_index] = 'yes'
                            return 'special', loss
    return 'no', 0


def judge_sell(test_15_line,record_first,test_15,test_15_deal,down_index):
    if len(test_15_line) > 3 and len(record_first) > 1 and record_first['flag'].iloc[down_index] != 'yes' and\
            test_15['close'].iloc[-1] < test_15['close'].iloc[-20] \
            and test_15['close'].iloc[-1] < test_15['close'].iloc[-19] and record_first['flag'].iloc[down_index] != 'no' and\
            record_first['point'].iloc[down_index] > test_15['high'].iloc[-1]:
        if (test_15['ma5'].iloc[-1] < test_15['ma10'].iloc[-1] or test_15['close'].iloc[-1] < test_15['close'].iloc[
            -5]) and test_15['ema5'].iloc[-1] > test_15['close'].iloc[-1] \
                and (test_15['open'].iloc[-1] > test_15['close'].iloc[-1] or test_15['close'].iloc[-1] < (
                test_15['open'].iloc[-1] + test_15['close'].iloc[-1]) / 2):
            if chaos(test_15_deal, 'down') == False:
                loss = comp_loss(test_15, record_first.iat[down_index, 0], 'down')
                if loss != 0:
                    print('sell: ' + str(test_15.iat[-1, 0]) + ' price: ' + str(
                        test_15['close'].iloc[-1]) + ' loss: ' + str(loss) + ' ' + str(test_15['short'].iloc[-1]))
                    record_first['loss'].iloc[down_index] = loss
                    record_first['flag'].iloc[down_index] = 'yes'
                    return 'normal',loss

            else:
                if test_15['ma5'].iloc[-1]<test_15['ma20'].iloc[-1] \
                        and test_15['ma5'].iloc[-1]<test_15['ma60'].iloc[-1] and test_15['ma5'].iloc[-1]<test_15['ma120'].iloc[-1]:
                    if launch(test_15,'down') and vol_confirm(test_15) and test_15['short'].iloc[-1]>0.1:
                        loss = comp_loss(test_15,record_first.iat[down_index,0],'down')
                        if loss != 0:
                            print('sell: ' + str(test_15.iat[-1, 0]) + ' price: ' + str(test_15['close'].iloc[-1]) + ' loss: ' + str(loss) +'空头排列'+' '+str(test_15['short'].iloc[-1]))
                            record_first['loss'].iloc[down_index] = loss
                            record_first['flag'].iloc[down_index] = 'yes'
                            return 'special', loss
    return 'no', 0


def judge_piont(l_simple,h_line,index):
    i =index
    # 最后不能太无力
    if i ==-3:
        dif=0
    else:
        dif=1
    if (l_simple["close"].iloc[i] <= l_simple["close"].iloc[i+2+dif] or l_simple["close"].iloc[i+2+dif] >=l_simple["open"].iloc[i]) \
            and (l_simple["high"].iloc[i+2+dif] > l_simple["high"].iloc[i+1+dif] or l_simple["close"].iloc[i+2+dif] >l_simple["high"].iloc[i]
            or l_simple["close"].iloc[i+2+dif] > (l_simple["high"].iloc[i] + l_simple["close"].iloc[i]) / 2) \
            and l_simple.iat[i-1, 0] + datetime.timedelta(minutes=-60) <= h_line.iat[-1, 0] <l_simple.iat[i+2+dif, 0] + datetime.timedelta(minutes=60)\
            and h_line['flag'].iloc[-1] == 'down':
        return True
    elif (l_simple["close"].iloc[i] >= l_simple["close"].iloc[i+2+dif] or l_simple["close"].iloc[i+2+dif] <=l_simple["open"].iloc[i]) \
            and (l_simple["low"].iloc[i+2+dif] < l_simple["low"].iloc[i+1+dif] or l_simple["close"].iloc[i+2+dif] <l_simple["low"].iloc[i]
            or l_simple["close"].iloc[i+2+dif] < (l_simple["low"].iloc[i] + l_simple["close"].iloc[i]) / 2) \
            and l_simple.iat[i-1, 0] + datetime.timedelta(minutes=-60) <= h_line.iat[-1, 0] <l_simple.iat[i+2+dif, 0] + datetime.timedelta(minutes=60)\
            and h_line['flag'].iloc[-1] == 'rise':
        return True

    return False

def statistics(test_15,exchange,loss,flag):
    price = test_15['close'].iloc[-1]
    balance = float(exchange['balance'].iloc[-1])
    num = float(exchange['num'].iloc[-1])
    if flag =='long':
        num = round(num + balance/price*0.995,2)
        balance = 0
    else:
        assets = round(balance + num * price,2)
        num = round(-assets/price*1.005,2)
        balance = 2*assets

    assets = balance+num*price
    new = pd.DataFrame({"date": test_15["date"].iloc[-1], "direction": flag, "price": test_15['close'].iloc[-1], "loss":loss,
                        "outstanding":'no',"balance":balance,"num":num,"situation":"","close_price":price,"assets":assets
                        ,'order_1':'','order_1_num':'','order_2':'','order_2_num':'','order_3':'','order_3_num':''
                           ,'order_4':'','order_4_num':'','order_5':'','order_5_num':''},index=[1])
    exchange = exchange.append(new, ignore_index=True)
    return exchange

#结算
def oustanding(test_15,exchange,situation):
    flag = exchange['direction'].iloc[-1]
    price = test_15['close'].iloc[-1]
    loss = exchange['loss'].iloc[-1]
    num = exchange['num'].iloc[-1]
    balance = float(exchange['balance'].iloc[-1])
    if situation=='active':
        close_price = price
        balance = balance+num*close_price-abs(num)*close_price*0.005
    else:
        close_price = loss
        balance = balance+num*close_price-abs(num)*close_price*0.005

    new = pd.DataFrame({"date": test_15["date"].iloc[-1], "direction": flag, "price": test_15['close'].iloc[-1], "loss":loss,
                        "outstanding":'yes',"balance":balance,"num":0.0,"situation":situation,"close_price":close_price,"assets":balance
                           , 'order_1': '', 'order_1_num': '', 'order_2': '', 'order_2_num': '', 'order_3': '','order_3_num': ''
                           , 'order_4': '', 'order_4_num': '', 'order_5': '', 'order_5_num': ''},index=[1])
    exchange = exchange.append(new, ignore_index=True)
    return exchange

def type_V(normal,deal,line):
    index = deal[line['key'].iloc[-1] == deal['key']].index.tolist()[-1]
    #线段后面只有一个deal
    if index == len(deal) - 2:
        if line['flag'].iloc[-1] == 'rise':
            normal_index = normal[normal['high'] == deal['key'].iloc[index]].index.tolist()[-1]
        else:
            normal_index = normal[normal['low'] == deal['key'].iloc[index]].index.tolist()[-1]
        list_normal_pass=normal[normal_index-4:normal_index+1]['vol'].sort_values().tolist()
        list_normal_now=normal[normal_index+1:]['vol'].sort_values().tolist()
        if list_normal_pass[2] > normal['vol'].iloc[normal_index] * 2.5 and list_normal_pass[3] > normal['vol'].iloc[normal_index] * 2.5\
        and  list_normal_now[2] > normal['vol'].iloc[normal_index] * 1.8 and list_normal_now[3] > normal['vol'].iloc[normal_index] * 1.8   :
            return True
    return False
def care(deal,line):
    deal_copy = copy.deepcopy(deal)
    deal_copy.drop(deal_copy[deal_copy["temp"] == "temp"].index.tolist(), inplace=True)

    index = deal[line['key'].iloc[-1] == deal['key']].index.tolist()[-1]
    if index == len(deal_copy)-4:
        return True,deal_copy['key'].iloc[-2]
    return False,0


def init_grid(grid,sl,l,exchange):
    l =l.copy()
    close_price = l['close_price'].iloc[-1]
    balance = exchange['balance'].iloc[-1]
    num = exchange['num'].iloc[-1]
    l['num'] = num
    assets = balance + num*close_price
    each = round(assets/close_price/2,2)
    for i in range(1, 3):
        l['order_' + str(i) + '_num']=each
    for i in range(4, 6):
        l['order_' + str(i) + '_num']=-each
    for i in range(1, 6):
        l['order_' + str(i)]=round(grid+sl*(i-3),2)
    l['order_3_num' ]=0.0

    flag = 0
    for i in range(1, 6):
        num = l['order_' + str(i) + '_num'].iloc[-1]
        # put
        if num < 0:
            if close_price >= l['order_' + str(i)].iloc[-1]:
                balance = balance - num * close_price * 0.998
                l['order_' + str(i - 1) + '_num'] = abs(num)
                l['order_' + str(i) + '_num'] = 0
                l['num'] +=num
                flag = 1
    if flag==0:
        for i in range(5, 0, -1):
            num = l['order_' + str(i) + '_num'].iloc[-1]
            # long
            if num > 0:
                if close_price <= l['order_' + str(i)].iloc[-1]:
                    balance = balance - num * close_price * 1.002
                    l['order_' + str(i + 1) + '_num'] = -num
                    l['order_' + str(i) + '_num'] = 0
                    l['num'] += num
    l['balance'] = round(balance,2)
    l['num'] = round(l['num'],2)
    l['assets'] = round(assets,2)
    l['base_num'] = each
    exchange = exchange.append(l, ignore_index=True)
    return exchange



def grid_to_long(normal):
    if normal['close'].iloc[-1] > normal['close'].iloc[-20]  and normal['close'].iloc[-1] > normal['close'].iloc[-19]:
        if (normal['ma5'].iloc[-1] > normal['ma10'].iloc[-1] or normal['close'].iloc[-1] > normal['close'].iloc[
            -5]) and normal['ema5'].iloc[-1] < normal['close'].iloc[-1] \
                and (normal['open'].iloc[-1] < normal['close'].iloc[-1] or normal['close'].iloc[-1] > (
                normal['open'].iloc[-1] + normal['close'].iloc[-1]) / 2):
            if normal['ma5'].iloc[-1] > normal['ma20'].iloc[-1] \
                    and normal['ma5'].iloc[-1] > normal['ma60'].iloc[-1] and normal['ma5'].iloc[-1] >normal['ma120'].iloc[-1]:
                if launch(normal, 'rise') and vol_confirm(normal) and normal['short'].iloc[-1] > 0.1:
                    return True
    return False

def grid_to_sell(normal):
    #20向下
    if normal['close'].iloc[-1] < normal['close'].iloc[-20] and normal['close'].iloc[-1] < normal['close'].iloc[-19]  :
        #短期空头
        if (normal['ma5'].iloc[-1] < normal['ma10'].iloc[-1] or normal['close'].iloc[-1] < normal['close'].iloc[ -5]) \
                and normal['ema5'].iloc[-1] > normal['close'].iloc[-1] and (normal['open'].iloc[-1] > normal['close'].iloc[-1]
                 or normal['close'].iloc[-1] < ( normal['open'].iloc[-1] + normal['close'].iloc[-1]) / 2):
            #5日击破所有均线
            if normal['ma5'].iloc[-1] < normal['ma20'].iloc[-1] \
                    and normal['ma5'].iloc[-1] < normal['ma60'].iloc[-1] and normal['ma5'].iloc[-1] <normal['ma120'].iloc[-1]:
                #成交量 动量确认
                if launch(normal, 'down') and vol_confirm(normal) and normal['short'].iloc[-1] > 0.1:
                    return True
    return False

def update_grid(grid,sl,new,exchange):
    l = new.copy()
    close_price = l['close_price'].iloc[-1]
    balance = exchange['balance'].iloc[-1]
    num = exchange['num'].iloc[-1]
    l['num'] = num
    assets = balance + num * close_price
    each = round(assets / close_price / 2, 2)
    buy_num=0.0
    sell_num=0.0
    if num>0:
        sell_num = num/3
    else:
        buy_num = num/3
    for i in range(1, 3):
        l['order_' + str(i) + '_num'] = each-buy_num
    for i in range(4, 6):
        l['order_' + str(i) + '_num'] = -each-sell_num
    for i in range(1, 6):
        l['order_' + str(i)] = round(grid + sl * (i - 3), 2)
    l['order_3_num'] = -buy_num-sell_num

    flag = 0
    for i in range(1, 6):
        num = l['order_' + str(i) + '_num'].iloc[-1]
        # put
        if num < 0:
            if close_price >= l['order_' + str(i)].iloc[-1]:
                balance = balance - num * close_price * 0.998
                l['order_' + str(i - 1) + '_num'] += each
                l['order_' + str(i) + '_num'] = 0
                l['num'] += num
                flag = 1
    if flag == 0:
        for i in range(5, 0, -1):
            num = l['order_' + str(i) + '_num'].iloc[-1]
            # long
            if num > 0:
                if close_price <= l['order_' + str(i)].iloc[-1]:
                    balance = balance - num * close_price * 1.002
                    l['order_' + str(i + 1) + '_num'] -= each
                    l['order_' + str(i) + '_num'] = 0
                    l['num'] += num
    l['balance'] = round(balance, 2)
    l['num'] = round(l['num'], 2)
    l['assets'] = round(assets, 2)
    l['base_num'] = each
    exchange = exchange.append(l, ignore_index=True)
    return exchange












