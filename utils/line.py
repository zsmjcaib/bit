import pandas as pd
import os
import yaml


def find_line(df, df_line):


    __find(df, df_line)
    return df_line


def __find(df, df_line):
    if (len(df) < 5): return
    small=''
    try:
        if df_line["small_to_large"].iloc[-1] == 'yes' or df_line["small_to_large"].iloc[-1] == 'second':
            small_date = df_line["date"].iloc[-1]
            small = df_line["small_to_large"].iloc[-1]
            # print("small out :" + str(df_line.iloc[-1]["date"])+" now "+ str(df.iloc[-1]["date"]))
        elif df_line["small_to_large"].iloc[-2] == 'yes' or df_line["small_to_large"].iloc[-2] == 'second':
            small_date = df_line["date"].iloc[-2]
            small = df_line["small_to_large"].iloc[-2]
            # print("small out :" + str(df_line.iloc[-2]["date"]) + " now " + str(df.iloc[-1]["date"]))
        else:small_date=''
    except:
        small_date=''
    try:
        if df_line["first"].iloc[-1] == 'yes':
            # print("first out :"+str(df_line.iloc[-1]["date"]))
            first_date = df_line["date"].iloc[-1]
        elif df_line["first"].iloc[-2] == 'yes':
            # print("first out :"+str(df_line.iloc[-2]["date"]))
            first_date = df_line["date"].iloc[-2]
        else:first_date=''
    except:
        first_date=''
    try:
        if df_line["second"].iloc[-1] == 'yes':
            second_date = df_line["date"].iloc[-1]
        else:second_date=''
    except:
        second_date=''
    if len(df_line)>0:
        last = df_line.iloc[-1].copy()
    else:
        last = pd.DataFrame(columns=['date', 'key', 'flag', 'temp','small_to_large','first','second','is_test'])
    df_line.drop(df_line[df_line["temp"] == "temp"].index.tolist(), inplace=True)
    df_line.drop(df_line[df_line["temp"] == "yes"].index.tolist(), inplace=True)
    # 初始化
    if (len(df_line) == 0):
        index = -1
        __deal(index, df, df_line)

    else:
        index = df[df["date"] == df_line.iat[-1, 0]].index.tolist()[0]
        __deal(index, df, df_line)
    __last(df, df_line,small_date,first_date,second_date,small)
    if len(last)>0 :
        if df_line['date'].iloc[-1] == last['date']:
            df_line.iat[-1,7] = last['is_test']


def __deal(index, df, df_line):
    if (len(df_line) == 0):
        i = index
    else:
        i = df[df["date"] == df_line.iat[-1, 0]].index.tolist()[0]
    df_line.drop(df_line[df_line["temp"] == "yes"].index.tolist(), inplace=True)
    while i < len(df) - 5:

        if len(df_line) == 0:
            i+=1
            if df["key"].iloc[i + 1] > df["key"].iloc[i]:
                # 顶点
                if df["key"].iloc[i + 3] > df["key"].iloc[i + 1] and df["key"].iloc[i + 3] >= df["key"].iloc[i + 5]:
                    if df["key"].iloc[i + 4] >= df["key"].iloc[i + 6]:
                        df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df["key"].iloc[i + 3], "rise", "no","","","",""]
                        i += 3
                    else:
                        try:
                            flag = df["key"].iloc[i + 6]
                            j = i + 8
                            while j < len(df) - 1:
                                if df["key"].iloc[j - 1] > df["key"].iloc[i + 3]:
                                    i += 3
                                    break
                                elif df["key"].iloc[j] < flag:
                                    df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df["key"].iloc[i + 3], "rise", "no","","","",""]
                                    i += 3
                                    break
                                else:i += 1
                        except:
                            print('line ' + df_line.iat[-1, 0])
                            return

            elif df["key"].iloc[i + 1] < df["key"].iloc[i]:
                if df["key"].iloc[i + 3] < df["key"].iloc[i + 1] and df["key"].iloc[i + 3] <= df["key"].iloc[i + 5]:
                    if df["key"].iloc[i + 4] <= df["key"].iloc[i + 6]:
                        df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df["key"].iloc[i + 3], "down", "no","","","",""]
                        i += 3
                    else:
                        try:
                            flag = df["key"].iloc[i + 6]
                            j = i + 8
                            while j < len(df) - 1:
                                if (df["key"].iloc[j - 1] < df["key"].iloc[i + 3]):
                                    i += 3
                                    break
                                elif (df["key"].iloc[j] > flag):
                                    df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df["key"].iloc[i + 3], "down", "no","","","",""]
                                    i += 3
                                    break
                                else:i+=1
                        except:
                            print('line ' + df_line.iat[-1, 0])
                            return

        else:
            if str(df_line.iat[-1,0]) == '2021-07-10 16:30:00':
                print(df_line.iat[-1,0])
            # print(df_line.iat[-1, 0])
            #单独判断
            if df_line["temp"].iloc[-1] == "yes":
                i = check(df,df_line,i)
            if i >= len(df) - 5:
                break
            if df_line["flag"].iloc[-1] == "down" :
                if (df["key"].iloc[i + 5] > df["key"].iloc[i + 3]) and df["key"].iloc[i + 4]>df_line["key"].iloc[-1]:
                    i += 2
                    continue
                # 第一种情况
                elif status(df_line,df,i) and df["key"].iloc[i + 3] >= df["key"].iloc[i + 1]:
                    i,result = __first_case(i, df, df_line)
                    if result == "wrong":
                        return
                elif df["key"].iloc[i + 1] < df["key"].iloc[i + 4]:
                    i,result = __second_case(i, df, df_line)
                    if result == "wrong":
                        return
                else:
                    i += 2

            elif (df_line["flag"].iloc[-1] == "rise" and df_line["temp"].iloc[-1] == "no" ) or\
                    df_line["flag"].iloc[-1] == "down" and df_line["temp"].iloc[-1] == "yes":
                if (df["key"].iloc[i + 5] < df["key"].iloc[i + 3]) and df["key"].iloc[i + 4]<df_line["key"].iloc[-1]:
                    i += 2
                    continue
                # 第一种情况

                elif status(df_line,df,i) and df["key"].iloc[i + 3] <= df["key"].iloc[i + 1]:
                    i,result = __first_case(i, df, df_line)
                    if result == "wrong":
                        return
                elif (df["key"].iloc[i + 1] > df["key"].iloc[i + 4]):
                    i,result = __second_case(i, df, df_line)
                    if result == "wrong":
                        return
                else:
                    i += 2
            else:
                i += 2



def __first_case(i, df, df_line):
    if (df_line["flag"].iloc[-1] == "down"):
        try:
            j = i + 6
            break_point = df_line["key"].iloc[-1]
            while j < len(df) - 1:
                #笔破前低
                if break_point >= df["key"].iloc[j - 2]:
                    #判断是否是极值点
                    if  judge(i+3,df, df_line,'rise') == 'yes':
                        df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df["key"].iloc[i + 3], "rise", "yes","","","",""]
                        i = i+3
                        return i, "yes"
                if (df["key"].iloc[j-1] > df["key"].iloc[i + 3]):
                    return i + 4, "no"
                elif (df["key"].iloc[j] < df["key"].iloc[j - 2]):
                    df_line.loc[len(df_line)]=[df.iat[i + 3, 0],df["key"].iloc[i + 3],"rise", "no","","","",""]
                    # df_line.loc[len(df_line)]=[df.iat[j, 0],df["key"].iloc[j],"down", "yes","","","",""]
                    # i = df[df["date"] == df_line["date"].iloc[-1]].index.tolist()[0] - 3
                    return i+3, "yes"
                j += 2
            return i+2,"out"
        except:
            print('line ' + df_line.iat[-1,0])
            return 0, "wrong"

    elif (df_line["flag"].iloc[-1] == "rise"):
        j = i + 6
        break_point = df_line["key"].iloc[-1]
        while j < len(df) - 1:
            #笔破前高
            if break_point <= df["key"].iloc[j - 2]:
                #判断是否是极值点
                if  judge(i+3,df, df_line,'down') == 'yes':
                    df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df["key"].iloc[i + 3], "down", "yes","","","",""]
                    i = i+3
                    return i, "yes"
            if (df["key"].iloc[j-1] < df["key"].iloc[i + 3]):
                return i + 4, "no"
            elif (df["key"].iloc[j] > df["key"].iloc[j - 2]):
                df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df["key"].iloc[i + 3], "down", "no","","","",""]
                # df_line.loc[len(df_line)] = [df.iat[j, 0], df["key"].iloc[j], "rise", "yes","","","",""]
                # i = df[df["date"] == df_line["date"].iloc[-1]].index.tolist()[0] - 3
                return i+3, "yes"
            j += 2
        return i+2,"out"



def __second_case(i, df, df_line):
    df_line.drop(df_line[df_line["temp"] == "yes"].index.tolist(), inplace=True)
    break_point = df_line["key"].iloc[-1]
    if (df_line["flag"].iloc[-1] == "down"):
        # 笔破前低
        if break_point >= df["key"].iloc[i] and df_line.iat[-1,0] != df.iat[i,0]:
            # 判断是否是极值点
            if judge(i, df, df_line, 'rise') == 'yes':
                df_line.drop(df_line.tail(1).index, inplace=True)
                df_line.loc[len(df_line)] = [df.iat[i, 0], df["key"].iloc[i], "rise", "no", "", "", "", ""]
        index = i + 5
        low = df["key"].iloc[i + 4]
        high = df["key"].iloc[i + 5]
        while index < len(df) :
            if index>i+6 and df['key'].iloc[index] <low and df['key'].iloc[index-1] > high:
                low = df["key"].iloc[i + 5]
            if df["key"].iloc[index] > df["key"].iloc[i + 3]:
                return i + 4,"no"
            elif df["key"].iloc[index-1] < low:
                df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df["key"].iloc[i + 3], "rise", "no","","","",""]
                # df_line.loc[len(df_line)] = [df.iat[index-1, 0], df["key"].iloc[index-1], "down", "yes","","","",""]
                # i = df[df["date"] == df_line["date"].iloc[-1]].index.tolist()[0] - 3
                return i+3,"yes"
            index +=2
        return i + 2, "out"
    elif (df_line["flag"].iloc[-1] == "rise"):
        # 笔破前高
        if break_point <= df["key"].iloc[i] and df_line.iat[-1,0] != df.iat[i,0]:
            # 判断是否是极值点
            if judge(i, df, df_line, 'down') == 'yes':
                df_line.drop(df_line.tail(1).index, inplace=True)
                df_line.loc[len(df_line)] = [df.iat[i, 0], df["key"].iloc[i], "down", "no", "", "", "", ""]

        index = i + 5
        high = df["key"].iloc[i + 4]
        low = df["key"].iloc[i + 5]
        while index < len(df) :
            #处理包含关系
            if index>i+6 and df['key'].iloc[index] >low and df['key'].iloc[index-1] < high:
                high = df["key"].iloc[i + 5]
            if df["key"].iloc[index] < df["key"].iloc[i + 3]:
                return i + 4,"no"
            elif df["key"].iloc[index-1] > high:
                df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df["key"].iloc[i + 3], "down", "no","","","",""]
                # df_line.loc[len(df_line)] = [df.iat[index-1, 0], df["key"].iloc[index-1], "rise", "yes","","","",""]
                # i = df[df["date"] == df_line["date"].iloc[-1]].index.tolist()[0] - 3
                return i+3,"yes"
            index += 2
        return i + 2, "out"


def  __last(df, df_line,small_date,first_date,second_date,small ):
    if len(df_line) == 0:
        return
    if df[df["date"] == df_line.iat[-1,0]].index.tolist()[0] +3 > len(df):
        if small_date == df_line["date"].iloc[-1]:
            df_line.iat[-1, 4] = small
            # print("small in :" + str(df_line.iloc[-1]["date"]))
        if small_date == df_line["date"].iloc[-2]:
            df_line.iat[-2, 4] = small
            # print("small in :" + str(df_line.iloc[-2]["date"]))
        if first_date == df_line["date"].iloc[-1]:
            df_line.iat[-1, 5] = "yes"
            # print("first in :" + str(df_line.iloc[-1]["date"]))

        if second_date == df_line["date"].iloc[-1]:
            df_line.iat[-1, 6] = "yes"
        return
    else:
        #后面第一个点
        index = df[df["date"] == df_line.iat[-1, 0]].index.tolist()[0]+1
        flag = df_line["flag"].iloc[-1]
        if flag == "rise":
            #先看有没有更高的
            key = df["key"].iloc[index:].max()

            if df_line['key'].iloc[-1] <= key:
                i = df["key"].iloc[index:].idxmax()
                low_index = df["key"].iloc[index:i].idxmin()
                #有更高的
                #判断更高的与现在之间有没有线段
                if index +1 < low_index:
                    df_line.loc[len(df_line)] = [df.iat[low_index, 0], df.iat[low_index, 1], "down", "temp", "", "", "", ""]
                    if low_index+2<i:
                        df_line.loc[len(df_line)] = [df.iat[i, 0], df.iat[i, 1], "rise", "temp", "", "", "", ""]
                else:
                    df_line.drop(df_line.tail(1).index, inplace=True)
                    df_line.loc[len(df_line)] = [df.iat[i, 0], df.iat[i, 1], "rise", "temp", "", "", "", ""]
                #再看能否找到低点
                if i < len(df) - 3:
                    key = df["key"].iloc[i+2:].min()
                    if key < df["key"].iloc[i+1]:
                        i = df["key"].iloc[i+2:].idxmin()
                        df_line.loc[len(df_line)] = [df.iat[i, 0], df.iat[i, 1], "down", "temp", "", "", "", ""]

            #没有更高的
            else:
            # #找低点
                index += 2
                if index<=len(df):
                    key_min = df["key"].iloc[index-2]
                    key = df["key"].iloc[index:].min()
                    if key_min >= key:
                        key_index = df[df["key"] == key].index.tolist()[-1]
                        df_line.loc[len(df_line)] = [df.iat[key_index, 0], key, "down", "temp", "","","",""]
                        key_index+=3
                    # #最后高点
                        if (key_index  <= len(df)):
                            key = df["key"].iloc[key_index:].max()
                            #是最高点
                            if key == df["key"].iloc[key_index-2:].max():
                                key_index = df[df["key"] == key].index.tolist()[-1]
                                df_line.loc[len(df_line)] = [df.iat[key_index, 0], key, "rise", "temp", "","","",""]

        else:
            if flag == "down":
                # 先看有没有更低的
                key = df["key"].iloc[index:].min()
                if df_line['key'].iloc[-1] >= key:
                    # 有更低的
                    # 判断更低的与现在之间有没有线段

                    i = df["key"].iloc[index:].idxmin()
                    high_index = df["key"].iloc[index:i].idxmax()
                    if index + 1 < high_index:
                        df_line.loc[len(df_line)] = [df.iat[high_index, 0], df.iat[high_index, 1], "rise", "temp", "", "","", ""]
                        if high_index + 2 < i:
                            df_line.loc[len(df_line)] = [df.iat[i, 0], df.iat[i, 1], "down", "temp", "", "", "", ""]
                    else:
                        df_line.drop(df_line.tail(1).index, inplace=True)
                        df_line.loc[len(df_line)] = [df.iat[i, 0], df.iat[i, 1], "down", "temp", "", "", "", ""]
                    # 再看能否找到高点
                    if i < len(df) - 3:
                        key = df["key"].iloc[i + 2:].max()
                        if key < df["key"].iloc[i + 1]:
                            i = df["key"].iloc[i + 2:].idxmax()
                            df_line.loc[len(df_line)] = [df.iat[i, 0], df.iat[i, 1], "rise", "temp", "", "", "", ""]

                else:
                    # 找高点
                    index += 2
                    if index <= len(df):
                        key_max = df["key"].iloc[index - 2]
                        key = df["key"].iloc[index:].max()
                        if key_max <= key:
                            key_index = df[df["key"] == key].index.tolist()[-1]
                            df_line.loc[len(df_line)] = [df.iat[key_index, 0], key, "rise", "temp", "", "", "", ""]
                            key_index += 3
                            # 最后低点
                            if (key_index <= len(df)):
                                key = df["key"].iloc[key_index:].min()
                                # 是最低点
                                if key == df["key"].iloc[key_index - 2:].min():
                                    key_index = df[df["key"] == key].index.tolist()[-1]
                                    df_line.loc[len(df_line)] = [df.iat[key_index, 0], key, "down", "temp", "", "", "", ""]



    if small_date == df_line["date"].iloc[-1] :
        df_line.iat[-1,4]=small
        # print("small in :" + str(df_line.iloc[-1]["date"]))
    if small_date == df_line["date"].iloc[-2]:
        df_line.iat[-2, 4] = small
        # print("small in :" + str(df_line.iloc[-2]["date"]))
    if first_date == df_line["date"].iloc[-1] :
        df_line.iat[-1,5]="yes"
        # print("first in :" + str(df_line.iloc[-1]["date"]))

    if second_date == df_line["date"].iloc[-1]:
        df_line.iat[-1, 6] = "yes"

def judge(index,df, df_line,direction):
    if direction == 'down':
        high = df['key'].iloc[index+1]
        low = df['key'].iloc[index]
    else:
        high = df['key'].iloc[index]
        low = df['key'].iloc[index+1]
    for i in range(len(df_line)-2, 0, -1):
        if direction == 'down':
            if df_line['key'].iloc[i]>high:
                return 'no'
            if df_line['key'].iloc[i]<low:
                #高点是极值点
                return 'yes'
        else:
            if df_line['key'].iloc[i]>high:
                #低点是极值点
                return 'yes'
            if df_line['key'].iloc[i]<low:
                return 'no'

def check(df,df_line,i):
    if df_line["flag"].iloc[-1] == "down":
        high = df['key'].iloc[i+1]
        low = df['key'].iloc[i]
        for j in range(i+3,len(df)-2):
            if df['key'].iloc[j] <=low:
                df_line.drop(df_line.tail(2).index,inplace=True)
                df_line.loc[len(df_line)] = [df.iat[i+1, 0], df.iat[i+1, 1], "rise", "no", "", "", "", ""]
                # df_line.drop(df_line.tail(1).index,inplace=True)
                return i + 1

            if df['key'].iloc[j] > high:
                # df_line.drop(df_line.tail(1).index,inplace=True)
                df_line.iat[-1,3] = 'no'
                return i

    else:
        high = df['key'].iloc[i]
        low = df['key'].iloc[i+1]
        for j in range(i+3,len(df)-2):
            if df['key'].iloc[j] >=high:
                df_line.drop(df_line.tail(2).index,inplace=True)
                df_line.loc[len(df_line)] = [df.iat[i+1, 0], df.iat[i+1, 1], "down", "no", "", "", "", ""]
                # df_line.drop(df_line.tail(1).index,inplace=True)

                return i + 1

            if df['key'].iloc[j] < low:
                # df_line.drop(df_line.tail(1).index,inplace=True)
                df_line.iat[-1,3] = 'no'
                return i
    return i

def status(df_line,df,i):
    index = df[df["date"] == df_line.iat[-1, 0]].index.tolist()[0]
    if df_line['flag'].iloc[-1] == 'rise':
        for j in range(index ,i+4):
            if df['key'].iloc[j]>=df["key"].iloc[i + 4]:
                return True
    else:
        for j in range(index ,i+4):
            if df['key'].iloc[j]<=df["key"].iloc[i + 4]:
                return True
    return False

if __name__ == '__main__':
    with open('../config.yaml') as f:
        content = yaml.load(f, Loader=yaml.FullLoader)
        f.close()
    file=content['deal_30_path']+'688125.csv'
    line = pd.DataFrame(columns=['date', 'key', 'flag', 'temp', 'small_to_large', 'first', 'second'])
    df = pd.read_csv(file)

    find_line(df, line)
    # target = ['5','30']
    # for i in target:
    #     path = 'D:\project\data\stock\\deal\\' + i + '\\'
    #     target_path = 'D:\project\data\stock\\line\\' + i + '\\'
    #     for file_code in os.listdir(path):
    #         if file_code not in os.listdir(target_path):
    #             df = pd.read_csv(path + file_code)
    #             if not os.path.exists(target_path+file_code):
    #                 df_line = pd.DataFrame(columns=['date', 'key', 'flag', 'temp', 'small_to_large', 'first', 'second'])
    #             else:
    #                 df_line = pd.read_csv(target_path+file_code)
    #
    #
    #             df_line = find_line(df, df_line)
                # df_line.to_csv(target_path +file_code, index=0)
