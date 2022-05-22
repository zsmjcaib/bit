import talib
import os
import pandas as pd
import copy
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
        demo = pd.DataFrame(columns=['date','first','15m','1h','15m小转大','1h小转大','flag','loss','point'])
        demo.loc[len(demo)] = [ "1997","", "","", "","","","",""]
    else:
        demo = pd.DataFrame(columns=['date', 'first', '15m', '1h', '15m小转大', '1h小转大', 'flag','loss','point'])
        demo.loc[len(demo)] = ["1997", "", "", "", "", "", "","",""]
        # demo = pd.read_csv(path )
    return demo

def read_buy_record(path):
    if not os.path.exists(path):
        demo = pd.DataFrame(columns=['date', 'mark_price', 'buy_price', 'mark_sell', 'sell_price', 'net'])
        demo.loc[len(demo)] = ["", "", "", "", "",  "1"]
    else:
        demo = pd.DataFrame(columns=['date', 'mark_price', 'buy_price', 'mark_sell', 'sell_price', 'net'])
        demo.loc[len(demo)] = ["", "", "", "", "",  "1"]
    return demo
def comp_loss(normal,date,flag):
    index = normal[normal['date'] == date].index.tolist()[-1]
    if flag == 'rise':
        for i in range(index,len(normal)-1):
            if normal['ma5'].iloc[i] < normal['close'].iloc[i]:
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
        min4,max4,min3, max3, min2, max2,_, _,  min1, max1 = temp['key'][-11:-1]
    return False

def judge(min1, max1,min2, max2, min3, max3,min4,max4,flag):

    if flag == 'rise':
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
            if normal['ma5'].iloc[l[i]]<normal['ma5'].iloc[l[i+1]] or normal['ma10'].iloc[l[i]]<normal['ma10'].iloc[l[i+1]]\
                or normal['ma20'].iloc[l[i]]<normal['ma20'].iloc[l[i+1]]:
                return False
            else:
                continue
    return True
def vol_confirm(normal):
    if normal[-5:]['vol'].mean() > normal['vol_ma'].iloc[-1]*1.3 or normal[-5:]['vol'].max() >normal['vol_ma'].iloc[-1]*1.8:
        return True
    return False

def grid(deal,flag):
    temp = copy.deepcopy(deal[-20:])
    if flag == 'rise':
        if temp["temp"].iloc[-1] =='yes' and temp["flag"].iloc[-1] =='min':
            temp.drop(temp.tail(1).index,inplace=True)
        max4, min4, max3, min3, max2, min2, max1, min1 = temp['key'][-9:-1]
        return find_gird(max4, min4, max3, min3, max2, min2, max1, min1)
def find_gird(max4, min4, max3, min3, max2, min2, max1, min1):
    abs1 = abs(max1 - min1)
    abs2 = abs(max2 - min2)
    abs3 = abs(max3 - min3)
    abs4 = abs(max4 - min4)
    l = [abs1,abs2,abs3,abs4]
    l.sort(reverse = True)
    gird =l[1]/4
    zreo = abs(max1 + min1)/2
    return zreo,gird
