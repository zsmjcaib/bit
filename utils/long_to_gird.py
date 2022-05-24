import pandas as pd
import datetime
import copy





def long_to_gird_test(test_15_simple,test_15,test_15_deal,test_15_line,test_1h_line,record_first):
    if record_first['flag'].iloc[-1] == 'yes' and test_15['ma60'].iloc[-1] > test_15['ma5'].iloc[-1]:
        if chaos(test_15_deal,'down') == True:


def chaos(deal, flag):
    temp = copy.deepcopy(deal[-20:])
    if flag == 'rise':
        if temp["temp"].iloc[-1] == 'yes' and temp["flag"].iloc[-1] == 'min':
            temp.drop(temp.tail(1).index, inplace=True)
        max4, min4, max3, min3, max2, min2, _, _, max1, min1 = temp['key'][-11:-1]
        return judge(min1, max1, min2, max2, min3, max3, min4, max4, 'rise')
    if flag == 'down':
        if temp["temp"].iloc[-1] == 'yes' and temp["flag"].iloc[-1] == 'max':
            temp.drop(temp.tail(1).index, inplace=True)
        min4, max4, min3, max3, min2, max2, _, _, min1, max1 = temp['key'][-11:-1]
    return False

def judge(min1, max1,min2, max2, min3, max3,min4,max4,flag):

    if flag == 'rise':
        ratio1 = calcul(min1, max1, min2, max2)
        ratio2 = calcul(min1, max1, min3, max3)
        ratio3 = calcul(min1, max1, min4, max4)

        if ratio1>0.6 or ratio2>0.6 or ratio3>0.6 :
            return True
    return False