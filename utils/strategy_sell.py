import pandas as pd
import datetime

from utils.util import judge_piont


def strategy_test_sell(test_15_simple,test_15,test_15_deal,test_15_line,test_1h,test_1h_deal,test_1h_line,test_4h,test_4h_deal,test_4h_line):
    l = pd.DataFrame({'date':'','first':'yes','15m':'','1h':'','15m小转大':'','1h小转大':'','flag':'','loss':'','point':'','is_gird':'','gird':'','sl':'','direction':''}, index=[1])
    if  test_15_line['is_test'].iloc[-1]!='yes':
        index = test_15_simple[test_15_simple["date"] == test_15_line.iloc[-1]["date"]].index.tolist()[0]
        if index == len(test_15_simple) - 3:
            #判断端点
            result=judge_piont(test_15_simple,test_1h_line,-3)
            if result and test_15_line.iat[-1, 7] != 'yes':
                l,result, mark_price = calculate(test_15,test_15_deal,test_15_line,test_1h,test_1h_deal,test_1h_line)
                return l,result, mark_price
        elif index == len(test_15_simple) - 4:
            #判断端点
            result=judge_piont(test_15_simple,test_1h_line,-4)
            if result and test_15_line.iat[-1, 7] != 'yes':
                l,result, mark_price = calculate(test_15, test_15_deal, test_15_line, test_1h, test_1h_deal,test_1h_line)
                return l,result, mark_price

    return l, 'no',0

def calculate(low,low_deal,low_line,test_1h,high,test_1h_line):
    l = pd.DataFrame({'date':'','first':'yes','15m':'','1h':'','15m小转大':'','1h小转大':'','flag':'','loss':'','point':'','is_gird':'','gird':'','sl':'','direction':''}, index=[1])
    result = 'no'
    mark_price =0
    if low_line.iat[-1, 7] != 'yes':
        h_flag, h_mark_price, h_result, h_l_to_h,mark,h_point = first_test(test_1h, high, test_1h_line, -1, ['1h','less_1h'])
        if mark!='no':
            l_flag, l_mark_price, l_result, l_l_to_h,_,l_point = first_test(low, low_deal, low_line, -1, ['15m','less_15m'])
            low_line.iat[-1, 7] = 'yes'
            if h_flag + l_flag > 4 :
                print(h_result + ' ' + l_result)
                mark_price = l_mark_price
                l.iat[-1,3]='y'
                l.iat[-1,2]='y'
                l['direction'].iloc[-1]='max'
                result = 'yes'
                if l_point!='' and l_flag >2:
                    l['point'].iloc[-1] = l_point
                elif h_point!='':
                    l['point'].iloc[-1] = h_point

            if h_l_to_h == 'yes':
                print('1h小转大： '+ h_result + ' ' + l_result)
                mark_price = l_mark_price
                l.iat[-1,5]='y'
                result = 'yes'
                l['direction'].iloc[-1]='max'
                if l_point!='':
                    l['point'].iloc[-1] = l_point
                elif h_point!='':
                    l['point'].iloc[-1] = h_point
            if l_l_to_h == 'yes':
                print('15m小转大： '+h_result + ' ' + l_result)
                mark_price = l_mark_price
                l.iat[-1,4]='y'
                result = 'yes'
                l['direction'].iloc[-1]='max'
                if l_point!='':
                    l['point'].iloc[-1] = l_point
                elif h_point!='':
                    l['point'].iloc[-1] = h_point

    return l,result, mark_price


def first_test(normal,deal,line,index,level):
    zhigh, zlow, high, low = volume_case(line, index+1)
    last_start_index = measure(line,index)
    i = index
    flag =0
    if last_start_index !=-1:
        if line.iloc[i]["key"] > high and line.iloc[i]["flag"] == "rise":
            now_end_index = normal[normal["date"] == line.iloc[i]["date"]].index.tolist()[0]
            now_start_index = normal[normal["date"] == line["date"].iloc[i - 1]].index.tolist()[0]
            df = normal.iloc[now_start_index:now_end_index + 1]

            last_end_index = normal[normal["date"] == line["date"].iloc[last_start_index + 1]].index.tolist()[0]
            last_start_index = normal[normal["date"] == line["date"].iloc[last_start_index]].index.tolist()[0]
            df_1 = normal.iloc[last_start_index:last_end_index + 1]

            str_1 = level[0] + ' macd不行 '
            str_2 = level[0] + ' diff不行 '
            str_3 = level[0] + ' macd值不行 '

            str_4 = level[0] + ' macd不背离 '
            str_5 = level[1] + ' macd值不行 '
            now_diff = df[df['diff'] > 0]["diff"].max() * 1.2
            now_macd = df[df['macd'] > 0]['macd'].sum() * 1.2
            now_macd_max = df['macd'].max()
            last_macd = df_1[df_1['macd'] > 0]["macd"].sum()
            last_macd_max = df_1['macd'].max()
            last_diff = df_1[df_1['diff'] > 0]["diff"].max()

            if __deal(now_macd, last_macd) == 1:
                str_1 = level[0] + ' macd '
                flag += 1
            if __deal(now_diff, last_diff) == 1:
                str_2 = level[0] + ' diff '
                flag += 1
            macd_result = 1 if now_macd_max * 1.1 < last_macd_max else 0
            if macd_result == 1:
                flag += 1
                str_3 = level[0] + ' macd值 '

            if level[1]!='':
                l_flag = 0
                str_6 = level[1] + ' 不背离 '
                str_7 = level[1] + ' diff不背离 '
                l_to_h = 'no'
                now_deal_lowest_end_index = deal[deal["date"] == line["date"].iloc[i]].index.tolist()[0]
                now_lowest_start_index = normal[normal["date"] == deal["date"].iloc[now_deal_lowest_end_index - 1]].index.tolist()[0]

                df_4 = normal.iloc[now_lowest_start_index:now_end_index + 1]
                now_lowest_macd = df_4[df_4['macd'] > 0]['macd'].sum() * 1.6
                now_lowest_macd_vaule = normal.iloc[now_end_index + 1 if level[1] == 'less_15m' else now_end_index]['macd']
                now_lowest_diff = normal.iloc[now_end_index + 1 if level[1] == 'less_15m' else now_end_index]['diff']
                last_lowest_start_index = deal[deal["date"] == line["date"].iloc[i - 1]].index.tolist()[0]
                last_lowest = deal[last_lowest_start_index:now_deal_lowest_end_index - 1].reset_index(drop=True)
                last_lowest_macd = find_last_1_macd(last_lowest, normal, "rise")
                if __deal(now_lowest_macd, last_lowest_macd) == 1:
                    str_5 = level[1]+'  macd面积 '
                    l_flag += 1
                    l_to_h='yes'
                if now_lowest_macd_vaule < 0 or now_lowest_macd_vaule < now_macd_max * 0.3:
                    l_flag += 1
                    str_6 = level[1] + ' macd严重背离 '
                    l_to_h='yes'
                if  now_lowest_diff < now_diff *0.3:
                    l_flag += 1
                    str_7 = level[1] + ' diff严重背离 '
                    l_to_h='yes'
                if l_flag > 0 :
                    line.iat[-1, 5] = 'yes'
                    # print('first buy :' + str(line["date"].iloc[-1]) + ' ' + str_1 + str_2 + str_3 + str_4 + str_5 + str_6 + str_7+' '+str(normal["date"].iloc[-1]))
                    result = 'first sell :' + str(line["date"].iloc[-1]) + ' ' + str_1 + str_2 + str_3 + str_4 + str_5 + str_6 + str_7+' '+str(normal["date"].iloc[-1])
                    return flag, line["key"].iloc[-1],result,l_to_h,'',line["key"].iloc[-1]

            if flag > 1 :
                # print('first buy :' + str(line["date"].iloc[-1]) + ' ' + str_1 + str_2 + str_3 +' '+str(normal["date"].iloc[-1]) )
                result = 'first sell :' + str(line["date"].iloc[-1]) + ' ' + str_1 + str_2 + str_3 +' '+str(normal["date"].iloc[-1])
                return flag, line["key"].iloc[-1],result,'no','',''
            else:
                # print('first buy :' + str( line["date"].iloc[-1]) + ' ' + str_1 + str_2 + str_3 )
                result = '1h :' + str( line["date"].iloc[-1]) + ' ' + str_1 + str_2 + str_3
                return flag, 0,'','no','',''
    return 0, 0,'','no','no',''

def volume_case(line, i):


    i2 = line["key"].iloc[i-2]
    i3 = line["key"].iloc[i-3]
    i4 = line["key"].iloc[i-4]
    i5 = line["key"].iloc[i-5]
    high = max(i2, i3, i4, i5)
    low = min(i2, i3, i4, i5)
    if line["flag"].iloc[i-2] == 'rise':
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
            #不是最高点
            if df["key"].iloc[i]>df["key"].iloc[index]:
                return -1
            if df["key"].iloc[i]<df["key"].iloc[index] and df["key"].iloc[i-1]<df["key"].iloc[index-1]:
                return i-1
    return -1

def __assess(high,low):
    if high>low:
        return "yes"
    else:
        return "no"



def __deal(gt,lt):
    if gt>lt:
        return 1
    else:
        return 0

def find_last_1_macd(df,data,flag):
    i = 0
    macd = 0
    temp = 0
    if flag =='down':
        while i<len(df)-1:
            first = data[data["date"] == df["date"].iloc[i]].index.tolist()[0]
            second = data[data["date"] == df["date"].iloc[i+1]].index.tolist()[0]
            new_data = data.iloc[first:second]
            macd = new_data[new_data['macd'] < 0]['macd'].sum()
            if macd >temp:
                macd = temp
            temp = macd
            i += 2
    else:
        while i<len(df)-1:
            first = data[data["date"] == df["date"].iloc[i]].index.tolist()[0]
            second = data[data["date"] == df["date"].iloc[i+1]].index.tolist()[0]
            new_data = data.iloc[first:second]
            macd = new_data[new_data['macd'] > 0]['macd'].sum()
            if macd <temp:
                macd = temp
            temp = macd
            i += 2
    return macd