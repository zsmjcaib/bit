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

def read_record(path):
    if not os.path.exists(path ):
        demo = pd.DataFrame(columns=['date','mark_buy','buy_price','mark_sell','sell_price','high_price','net'])
        demo.loc[len(demo)] = [ "", "","", "","", "","1"]
    else:
        demo = pd.DataFrame(columns=['date', 'mark_buy', 'buy_price', 'mark_sell', 'sell_price', 'high_price', 'net'])
        demo.loc[len(demo)] = ["", "", "", "", "", "", "1"]
        # demo = pd.read_csv(path )
    return demo