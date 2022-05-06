import pandas as pd

def check(df_deal,df_line):
    if df_line["small_to_large"].iloc[-1] =='yes' :
        index = df_deal[df_deal["date"]==df_line["date"].iloc[-1]].index.tolist()[0]
        if len(df_deal)>index+1:
            if df_deal["key"].iloc[index-1]<df_deal["key"].iloc[index+1]:
                df_line.iat[-1,4] = 'second'
                return 'yes',str(df_line["date"].iloc[-1]),df_line["key"].iloc[-1]
    elif  df_line["small_to_large"].iloc[-2] =='yes':
        df_line.iat[-2, 4] = 'second'
        return 'yes',str(df_line["date"].iloc[-2]),df_line.iat[-2,1]
    return 'no','0',0

def check_second(df_deal,df_line):
    if df_line.iat[-1,6] =='yes' and df_deal.iat[-1,2]=='max':
        index = df_deal[df_deal["date"]==df_line["date"].iloc[-1]].index.tolist()[0]
        if len(df_deal)>index+2:
            # if df_deal.iloc[index-1]["key"]<df_deal.iloc[index+1]["key"]:
            if df_deal.iat[-1,1]>df_deal.iat[-3,1]:
                df_line.iat[-1,6] = ''
                return 'yes',str(df_line["date"].iloc[-1]),df_line["key"].iloc[-1]
    elif  df_line.iat[-2,6] =='yes':

        return 'yes',str(df_line["date"].iloc[-2]),df_line.iat[-2,1]
    return 'no','0',0

def check_sell(df,data,flag):
    #更新高点
    # if df.iloc[-1]['high_price'] ==''or df.iloc[-1]['high_price'] < data["high"].iloc[-1]:
    #     df.iloc[-1]['high_price'] = data["high"].iloc[-1]
    if df.iat[-1,5] == '' or df.iat[-1,5] < data["high"].iloc[-1]:
        df.iat[-1, 5] = data["high"].iloc[-1]
    if str(df.iat[-1,0])[:10]==  str(data.iat[-1,0])[:10]:
        return ''
    #强制
    if df.iat[-1,1]>data["close"].iloc[-1] and df.iat[-1,4]=='':
        df.iat[-1,4] = str(data.iat[-1,0])+'_'+str(data["close"].iloc[-1])
        df.iat[-1,3] =str(data.iat[-1,0])+'_'+str(data["close"].iloc[-1])
        return '止损' + str(data.iat[-1,0])+'_'+str(data["close"].iloc[-1])
    #退出等待
    high_profit = df.iat[-1, 5] /df.iat[-1, 2]
    if high_profit>1.1:
        if df.iat[-1, 5]/data["close"].iloc[-1]>(high_profit-1)/3+1:
            df.iat[-1, 4] = str(data.iat[-1, 0]) + '_' + str(data["close"].iloc[-1])
            df.iat[-1, 3] = str(data.iat[-1, 0]) + '_' + str(data["close"].iloc[-1])
            return '止盈' + str(data.iat[-1, 0]) + '_' + str(data["close"].iloc[-1])
    return ''




