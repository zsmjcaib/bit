import pandas as pd
import os
from chart import chart_test
import datetime

def judge_piont(test_15_simple,test_1h_line,index):
    i =index
    # 最后不能太无力
    if (test_15_simple["close"].iloc[i] <= test_15_simple["close"].iloc[i+2] or test_15_simple["close"].iloc[i+2] >=test_15_simple["open"].iloc[i]) \
            and (test_15_simple["high"].iloc[i+2] > test_15_simple["high"].iloc[i+1] or test_15_simple["close"].iloc[i+2] >test_15_simple["high"].iloc[i]
            or test_15_simple["close"].iloc[i+2] > (test_15_simple["high"].iloc[i] + test_15_simple["close"].iloc[i]) / 2) \
            and test_15_simple.iat[i-1, 0] + datetime.timedelta(minutes=-30) <= test_1h_line.iat[i+2, 0] <test_15_simple.iat[i+2, 0] + datetime.timedelta(minutes=30):
        return True

def __assess(high,low):
    if high>low:
        return "yes"
    else:
        return "no"

def __volume_case(data,i = 0):

    i2 = data["key"].iloc[i-2]
    i3 = data["key"].iloc[i-3]
    i4 = data["key"].iloc[i-4]
    i5 = data["key"].iloc[i-5]
    high = max(i2, i3, i4, i5)
    low = min(i2, i3, i4, i5)
    if data["flag"].iloc[i-2] == 'rise':
        if __assess(i2,i5) == "yes":
            zhigh = min(i2, i4)
            zlow = max(i5, i3)

            return zhigh,zlow,high,low
    else:
        if __assess(i5, i2) == "yes":
            zhigh = min(i5, i3)
            zlow = max(i2, i4)

            return zhigh,zlow,high,low
    return 0,0,high,low

def measure(df,index):
    if index>=0:
        index = index - len(df)
    if df["flag"].iloc[index]=='down':
        for i in range(len(df)-2 + index,2,-2):
            #不是最低点
            if df["key"].iloc[i]<df["key"].iloc[index]:
                return -1
            if df["key"].iloc[i]>df["key"].iloc[index] and df["key"].iloc[i-1]>df["key"].iloc[index-1]:
                return i-1
    else:
        for i in range(len(df)-2 + index,2,-2):
            #不是最低点
            if df["key"].iloc[i]>df["key"].iloc[index]:
                return -1
            if df["key"].iloc[i]>df["key"].iloc[index] and df["key"].iloc[i-1]<df["key"].iloc[index-1]:
                return i-1
    return -1

def find_last_1_macd(df,data,flag):
    i = 0
    macd = 0
    temp = 0
    if flag =='down':
        while i<len(df):
            first = data[data["date"] == df["date"].iloc[i]].index.tolist()[0]
            second = data[data["date"] == df["date"].iloc[i+1]].index.tolist()[0]
            new_data = data.iloc[first:second]
            macd = new_data[new_data['macd'] < 0]['macd'].sum()
            if macd >temp:
                macd = temp
            temp = macd
            i += 2
    else:
        while i<len(df):
            first = data[data["date"] == df["date"].iloc[i]].index.tolist()[0]
            second = data[data["date"] == df["date"].iloc[i+1]].index.tolist()[0]
            new_data = data.iloc[first:second]
            macd = new_data[new_data['macd'] > 0]['macd'].sum()
            if macd <temp:
                macd = temp
            temp = macd
            i += 2
    return macd

def __deal(gt,lt):
    if gt>lt:
        return 1
    else:
        return 0

def first_situation(l_normal,l_deal,l_line,h_normal,h_deal,h_line,index,flag = False):
    zhigh, zlow, high, low = __volume_case(l_line, index + 1)
    i = index  # -1

    last_l_start_index = measure(l_line, i)
    last_h_start_index = measure(h_line, i)
    #判断升降
    if last_l_start_index != -1 and last_h_start_index != -1:
        if (l_line.iloc[i]["key"] < low and l_line.iloc[i]["flag"] == "down") or \
                (l_line.iloc[i]["key"] > high and l_line.iloc[i]["flag"] == "rise"):
            now_l_end_index = l_normal[l_normal["date"] == l_line.iloc[i]["date"]].index.tolist()[0]
            now_l_start_index = l_normal[l_normal["date"] == l_line["date"].iloc[i - 1]].index.tolist()[0]
            df = l_normal.iloc[now_l_start_index:now_l_end_index + 1]

            last_l_end_index = l_normal[l_normal["date"] == l_line["date"].iloc[last_l_start_index + 1]].index.tolist()[0]
            last_l_start_index = l_normal[l_normal["date"] == l_line["date"].iloc[last_l_start_index]].index.tolist()[0]
            df_1 = l_normal.iloc[last_l_start_index:last_l_end_index + 1]
            now_h_start_index = h_normal[h_normal["date"] == h_line["date"].iloc[i - 1]].index.tolist()[0]
            now_h_end_index = h_normal[h_normal["date"] == h_line["date"].iloc[i]].index.tolist()[0]
            df_2 = h_normal.iloc[now_h_start_index:now_h_end_index + 1]
            last_h_end_index = h_normal[h_normal["date"] == h_line["date"].iloc[last_h_start_index + 1]].index.tolist()[0]
            last_h_start_index = h_normal[h_normal["date"] == h_line["date"].iloc[last_h_start_index]].index.tolist()[0]
            df_3 = h_normal.iloc[last_h_start_index:last_h_end_index + 1]
            now_lowest_end_index = l_deal[l_deal["date"] == l_line["date"].iloc[i]].index.tolist()[0]
            now_lowest_start_index = l_normal[l_normal["date"] == l_deal["date"].iloc[now_lowest_end_index - 1]].index.tolist()[0]
            df_4 = l_normal.iloc[now_lowest_start_index:now_lowest_end_index + 1]

            if l_line.iloc[i]["key"] < low and l_line.iloc[i]["flag"] == "down":
                now_l_diff = df[df['diff'] < 0]["diff"].min() * 1.2
                now_l_macd = df[df['macd'] < 0]['macd'].sum() * 1.2
                now_l_macd_min = df['macd'].min()
                last_l_macd = df_1[df_1['macd'] < 0]["macd"].sum()
                last_l_macd_min = df_1['macd'].min()
                last_l_diff = df_1[df_1['diff'] < 0]["diff"].min()
                now_h_macd = df_2[df_2['macd'] < 0]["macd"].sum() * 1.2
                now_h_macd_min = df_2['macd'].min()
                now_h_diff = df_2[df_2['diff'] < 0]["diff"].min() * 1.2
                last_h_macd = df_3[df_3['macd'] < 0]["macd"].sum()
                last_h_macd_min = df_3['macd'].min()
                last_h_diff = df_3[df_3['diff'] < 0]["diff"].min()
                str_1 = '5分钟macd不行 '
                str_2 = '5分钟diff不行 '
                str_3 = '30分钟macd不行 '
                str_4 = '30分钟diff不行 '
                str_5 = '1分钟macd不行 '
                str_6 = '1分钟macd不背离 '
                str_7 = '5分钟macd值不行 '
                str_8 = '30分钟macd值不行 '
                str_9 = '1分钟macd不背离 '
                if flag:
                    now_lowest_macd = df_4[df_4['macd'] < 0]['macd'].sum() * 1.2
                    now_lowest_macd_vaule = l_normal.iloc[now_lowest_end_index + 1]['macd']
                    last_lowest_start_index = l_deal[l_deal["date"] == l_line["date"].iloc[i - 1]].index.tolist()[0]
                    last_lowest_end_index = now_lowest_end_index
                    last_lowest = l_deal[last_lowest_start_index:last_lowest_end_index - 1].reset_index()
                    last_lowest_macd = find_last_1_macd(last_lowest, l_normal, "down")
                    if __deal(now_lowest_macd, last_lowest_macd) == 1:
                        str_5 = '1分钟macd '
                        flag += 1
                    if now_lowest_macd_vaule > 0 or now_lowest_macd_vaule > now_l_macd_min * 0.3:
                        flag += 1
                        str_6 = '1分钟macd严重背离 '

                if __deal(now_l_macd, last_l_macd) == 1:
                    str_1 = '5分钟macd '
                    flag += 1
                if __deal(now_l_diff, last_l_diff) == 1:
                    str_2 = '5分钟diff '
                    flag += 1
                if __deal(now_h_macd, last_h_macd) == 1:
                    str_3 = '30分钟macd '
                    flag += 1
                if __deal(now_h_diff, last_h_diff) == 1:
                    str_4 = '30分钟diff '
                    flag += 1

                if now_l_macd_min * 1.1 > last_l_macd_min:
                    flag += 1
                    str_7 = '5分钟macd值 '
                if now_h_macd_min * 1.1 > last_h_macd_min:
                    flag += 1
                    str_8 = '30分钟macd值 '
                if flag > 4 and (__deal(now_h_macd, last_h_macd) == 1 or __deal(now_h_diff, last_h_diff) == 1):
                    return 'yes'
                else:
                    return 'no'
            else:
                now_l_diff = df[df['diff'] > 0]["diff"].max() * 1.2
                now_l_macd = df[df['macd'] > 0]['macd'].sum() * 1.2
                now_l_macd_max = df['macd'].max()
                last_l_macd = df_1[df_1['macd'] > 0]["macd"].sum()
                last_l_macd_max = df_1['macd'].max()
                last_l_diff = df_1[df_1['diff'] > 0]["diff"].max()
                now_h_macd = df_2[df_2['macd'] > 0]["macd"].sum() * 1.2
                now_h_macd_max = df_2['macd'].max()
                now_h_diff = df_2[df_2['diff'] > 0]["diff"].max() * 1.2
                last_h_macd = df_3[df_3['macd'] > 0]["macd"].sum()
                last_h_macd_max = df_3['macd'].max()
                last_h_diff = df_3[df_3['diff'] > 0]["diff"].max()
                now_lowest_macd = df_4[df_4['macd'] > 0]['macd'].sum() * 1.2
                now_lowest_macd_vaule = l_normal.iloc[now_lowest_end_index + 1]['macd']
                if flag:
                    last_lowest_start_index = l_deal[l_deal["date"] == l_line["date"].iloc[i - 1]].index.tolist()[0]
                    last_lowest_end_index = now_lowest_end_index
                    last_lowest = l_deal[last_lowest_start_index:last_lowest_end_index - 1].reset_index()
                    last_lowest_macd = find_last_1_macd(last_lowest, l_normal, "rise")


def strategy_test(test_15_simple,test_15,test_15_deal,test_15_line,test_1h,test_1h_deal,test_1h_line,test_4h,test_4h_deal,test_4h_line):
    index = test_15_simple[test_15_simple["date"] == test_15_line.iloc[-1]["date"]].index.tolist()[0]
    result = False
    if index == len(test_15_simple) - 3:
        #判断端点
        result=judge_piont(test_15_simple,test_1h_line,-3)
    elif index == len(test_15_simple) - 4:
        #判断端点
        result=judge_piont(test_15_simple,test_1h_line,-4)
        if result:
            first_situation(test_15,test_15_deal,test_15_line,test_1h,test_1h_deal,test_1h_line,-1)
