import pandas as pd
import datetime
import copy





def long_to_grid_test(test_15_simple,date,test_15_deal,test_15_line,test_1h_line,record_first):
    if record_first['flag'].iloc[-1] == 'yes' :
        #and test_15['ma60'].iloc[-1] > test_15['ma5'].iloc[-1]
        if str(test_15_line['date'].iloc[-1])>=date:
            if test_15_line['flag'].iloc[-1] == 'down':
                st = 'rise'
            else: st = 'down'
        else:
            if test_15_line['flag'].iloc[-1] == 'down':
                st = 'down'
            else: st = 'rise'
        if chaos(test_15_deal,st) == True:
            return True

def chaos(deal, flag):
    temp = copy.deepcopy(deal[-20:])
    if flag == 'rise':
        if temp["temp"].iloc[-1] == 'yes' and temp["flag"].iloc[-1] == 'min':
            temp.drop(temp.tail(1).index, inplace=True)
            if temp['is_test'].iloc[-1]=='yes':
                print(str(temp['date'].iloc[-1])+' 已检测')
                return False
        max3, min3, max2, min2, max1, min1 = temp['key'][-7:-1]
        return judge(min1, max1, min2, max2, min3, max3, 'rise')
    if flag == 'down':
        if temp["temp"].iloc[-1] == 'yes' and temp["flag"].iloc[-1] == 'max':
            temp.drop(temp.tail(1).index, inplace=True)
            if temp['is_test'].iloc[-1]=='yes':
                print(str(temp['date'].iloc[-1])+' 已检测')
                return False
        min3, max3, min2, max2,min1, max1 = temp['key'][-7:-1]
        return judge(min1, max1, min2, max2, min3, max3, 'rise')

    return False

def judge(min1, max1,min2, max2, min3, max3,flag):

    if flag == 'rise':
        ratio1 = calcul(min1, max1, min2, max2)
        ratio2 = calcul(min1, max1, min3, max3)

        if ratio1>0.6 or ratio2>0.6  :
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