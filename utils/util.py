import talib
import os
import pandas as pd
def stock_macd(df):

    diff, dea, macd = talib.MACD(df["close"],
                                    fastperiod=12,
                                    slowperiod=26,
                                    signalperiod=9)
    df = df.copy()
    df["diff"]=round(diff*10,2)
    df["dea"] = round(dea*10,2)
    df["macd"] = round(macd*100,2)
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