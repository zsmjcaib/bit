import pandas as pd
import os
import yaml
def simpleTrend(df,df_simple):



    #找第一个新增数据
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df_simple = df_simple.copy()
    df_simple['date'] = pd.to_datetime(df_simple['date'], format='%Y-%m-%d')

    tem_data=df[df["date"]>df_simple.iloc[-1]["date"]]
    dfSimple = compare(df_simple,tem_data)
    dfSimple.reset_index(drop=True, inplace=True)
    return dfSimple



def compare(dfSimple,tem_data) -> pd.DataFrame:
    for index,row in tem_data.iterrows():
        before = len(dfSimple)
        dfSimple =calculation(row,dfSimple)
        after = len(dfSimple)
        if after == before:
            while True:
                before = len(dfSimple)
                dfSimple = calculation(dfSimple.iloc[-1], dfSimple[:-1])
                after = len(dfSimple)
                if after == before:
                    break
    return dfSimple


def calculation(row,dfSimple) -> pd.DataFrame:
    #右包左
    if(row["high"]>=dfSimple["high"].iloc[-1] and row["low"]<=dfSimple["low"].iloc[-1]):
        dfSimple.iat[-1, 0] = row["date"]
        #判断升降
        result = rise_down(row,dfSimple,'right')
        #上升
        # if(dfSimple["high"].iloc[-1]>=dfSimple["high"].iloc[-2]):
        if result == 'rise':
            dfSimple.iat[-1, 2] = row["high"]
            #dfSimple.iat[-1, 4] = max(row["close"],dfSimple.at[-1, "low"])
            dfSimple.iat[-1, 4] = max(row["close"],dfSimple.iat[-1, 3])

        #下降
        else:
            dfSimple.iat[-1, 3] = row["low"]
            #dfSimple.iat[-1, 4] = min(row["close"],dfSimple.at[-1, "high"])
            dfSimple.iat[-1, 4] = min(row["close"],dfSimple.iat[-1, 2])

    #左包右
    elif(row["high"]<=dfSimple["high"].iloc[-1] and row["low"]>=dfSimple["low"].iloc[-1]):
        dfSimple.iat[-1, 0] = row["date"]
        result = rise_down(row,dfSimple,'left')
        #上升
        # if(dfSimple["high"].iloc[-1]>=dfSimple["high"].iloc[-2]):
        if result == 'rise':
            #dfSimple.iat[-1, 1] = max(row["low"],dfSimple.at[-1, "open"])
            dfSimple.iat[-1, 1] = max(row["low"],dfSimple.iat[-1, 1])
            dfSimple.iat[-1, 3] = row["low"]
        #下降
        else:
            #dfSimple.iat[-1, 1] = min(row["high"],dfSimple.at[-1, "open"])
            dfSimple.iat[-1, 1] = min(row["high"],dfSimple.iat[-1, 1])
            dfSimple.iat[-1, 2] = row["high"]
    else:
        dfSimple = dfSimple.append(row[0:7])
    return dfSimple

def rise_down(row,dfSimple,flag):
    if flag == 'right':
        for i in (range(len(dfSimple)-1,1,-1)):
            if dfSimple['high'].iloc[i]>row['high']:
                return 'down'
            if dfSimple['low'].iloc[i]<row['low']:
                return 'rise'
    else:
        new = dfSimple.iloc[-1]
        df = dfSimple[:-1]
        for i in (range(len(df)-1,1,-1)):
            if df['high'].iloc[i]>new['high']:
                return 'down'
            if df['low'].iloc[i]<new['low']:
                return 'rise'
    return 'rise'





if __name__ == '__main__':
    with open('../config.yaml') as f:
        content = yaml.load(f, Loader=yaml.FullLoader)
        f.close()
    i='5'
    path = content['normal_30_path']+'688125.csv'
    target_path = content['simple_30_path']+'688125.csv'
    df = pd.read_csv(path)
    df_simple = pd.read_csv(target_path)




    df = simpleTrend(df,df_simple)
    df.to_csv(target_path,index=False)





