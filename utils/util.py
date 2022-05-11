import talib
import os
import pandas as pd
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
    # df["short"] = df.iloc[:,9:12].std(axis=1)/df['close']*100
    # df["mid"] = df.iloc[:,10:13].std(axis=1)/df['close']*100
    # df["long"] = df.iloc[:,11:14].std(axis=1)/df['close']*100
    # df["short_ma"] = talib.MA(df['short'],timeperiod=5)
    # df["mid_ma"] = talib.MA(df['mid'],timeperiod=5)
    # df["long_ma"] = talib.MA(df['long'],timeperiod=5)
    return df

def read_first_record(path):
    if not os.path.exists(path ):
        demo = pd.DataFrame(columns=['date','first','15m','1h','15m小转大','1h小转大','flag'])
        demo.loc[len(demo)] = [ "1997","", "","", "","",""]
    else:
        demo = pd.DataFrame(columns=['date', 'first', '15m', '1h', '15m小转大', '1h小转大', 'flag'])
        demo.loc[len(demo)] = ["1997", "", "", "", "", "", ""]
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