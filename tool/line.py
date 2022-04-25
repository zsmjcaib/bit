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


def __deal(index, df, df_line):
    if (len(df_line) == 0):
        i = index
    else:
        i = df[df["date"] == df_line.iat[-1, 0]].index.tolist()[0]
    while i < len(df) - 5:
        # try:
        #     print(df_line.iloc[-1]["date"])
        #     if df_line.iloc[-1]["date"] == '2022-3-11 14:35':
        #     # if i ==135:
        #         print(df_line.iloc[-1]["date"])
        # except: pass
        # 初始化
        try:

            if len(df_line) == 0:
                i+=1
                if df["key"].iloc[i + 1] > df["key"].iloc[i]:
                    # 顶点
                    if df["key"].iloc[i + 3] > df["key"].iloc[i + 1] and df["key"].iloc[i + 3] >= df["key"].iloc[i + 5]:
                        if df["key"].iloc[i + 4] >= df["key"].iloc[i + 6]:
                            df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df["key"].iloc[i + 3], "rise", "no","","",""]
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
                                        df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df["key"].iloc[i + 3], "rise", "no","","",""]
                                        i += 3
                                        break
                                    else:i += 1
                            except:
                                return

                elif df["key"].iloc[i + 1] < df["key"].iloc[i]:
                    if df["key"].iloc[i + 3] < df["key"].iloc[i + 1] and df["key"].iloc[i + 3] <= df["key"].iloc[i + 5]:
                        if df["key"].iloc[i + 4] <= df["key"].iloc[i + 6]:
                            df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df["key"].iloc[i + 3], "down", "no","","",""]
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
                                        df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df["key"].iloc[i + 3], "down", "no","","",""]
                                        i += 3
                                        break
                                    else:i+=1
                            except:
                                return

            else:
                if (df_line["flag"].iloc[-1] == "down" and df_line["temp"].iloc[-1] == "no" ) or \
                        df_line["flag"].iloc[-1] == "rise" and df_line["temp"].iloc[-1] == "yes" :
                    if (df["key"].iloc[i + 5] > df["key"].iloc[i + 3]):
                        i += 2
                        continue
                    # 第一种情况
                    elif (df["key"].iloc[i + 1] >= df["key"].iloc[i + 4]):
                        i,result = __first_case(i, df, df_line)
                        if result == "wrong":
                            return
                    elif df["key"].iloc[i + 1] < df["key"].iloc[i + 4]:
                        i,result = __second_case(i, df, df_line)
                        if result == "wrong":
                            return

                elif (df_line["flag"].iloc[-1] == "rise" and df_line["temp"].iloc[-1] == "no" ) or\
                        df_line["flag"].iloc[-1] == "down" and df_line["temp"].iloc[-1] == "yes":
                    if (df["key"].iloc[i + 5] < df["key"].iloc[i + 3]):
                        i += 2
                        continue
                    # 第一种情况
                    elif (df["key"].iloc[i + 1] <= df["key"].iloc[i + 4]):
                        i,result = __first_case(i, df, df_line)
                        if result == "wrong":
                            return
                    elif (df["key"].iloc[i + 1] > df["key"].iloc[i + 4]):
                        i,result = __second_case(i, df, df_line)
                        if result == "wrong":
                            return
                else:
                    i += 2
        except:return


def __first_case(i, df, df_line):
    df_line.drop(df_line[df_line["temp"] == "yes"].index.tolist(), inplace=True)
    if (df_line["flag"].iloc[-1] == "down"):
        try:
            j = i + 6
            while j < len(df) - 1:
                if (df["key"].iloc[j-1] > df["key"].iloc[i + 3]):
                    return i + 4, "no"
                elif (df["key"].iloc[j] < df["key"].iloc[j - 2]):
                    df_line.loc[len(df_line)]=[df.iat[i + 3, 0],df["key"].iloc[i + 3],"rise", "no","","",""]
                    df_line.loc[len(df_line)]=[df.iat[j, 0],df["key"].iloc[j],"down", "yes","","",""]
                    i = df[df["date"] == df_line["date"].iloc[-1]].index.tolist()[0] - 3
                    return i, "yes"
                j += 2
            return i+2,"out"
        except:
            return 0, "wrong"

    elif (df_line["flag"].iloc[-1] == "rise"):
        try:
            j = i + 6
            while j < len(df) - 1:
                if (df["key"].iloc[j-1] < df["key"].iloc[i + 3]):
                    return i + 4, "no"
                elif (df["key"].iloc[j] > df["key"].iloc[j - 2]):
                    df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df["key"].iloc[i + 3], "down", "no","","",""]
                    df_line.loc[len(df_line)] = [df.iat[j, 0], df["key"].iloc[j], "rise", "yes","","",""]
                    i = df[df["date"] == df_line["date"].iloc[-1]].index.tolist()[0] - 3
                    return i, "yes"
                j += 2
            return i+2,"out"
        except:
            return 0, "wrong"


def __second_case(i, df, df_line):
    df_line.drop(df_line[df_line["temp"] == "yes"].index.tolist(), inplace=True)
    if (df_line["flag"].iloc[-1] == "down"):
        index = i + 5
        while index < len(df) :
            if df["key"].iloc[index] > df["key"].iloc[i + 3]:
                return i + 4,"no"
            elif df["key"].iloc[index-1] < df["key"].iloc[i + 4]:
                df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df["key"].iloc[i + 3], "rise", "no","","",""]
                df_line.loc[len(df_line)] = [df.iat[index-1, 0], df["key"].iloc[index-1], "down", "yes","","",""]
                i = df[df["date"] == df_line["date"].iloc[-1]].index.tolist()[0] - 3
                return i,"yes"
            index +=2
        return i + 2, "out"
    elif (df_line["flag"].iloc[-1] == "rise"):
        index = i + 5
        while index < len(df) :
            if df["key"].iloc[index] < df["key"].iloc[i + 3]:
                return i + 4,"no"
            elif df["key"].iloc[index-1] > df["key"].iloc[i + 4]:
                df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df["key"].iloc[i + 3], "down", "no","","",""]
                df_line.loc[len(df_line)] = [df.iat[index-1, 0], df["key"].iloc[index-1], "rise", "yes","","",""]
                i = df[df["date"] == df_line["date"].iloc[-1]].index.tolist()[0] - 3
                return i,"yes"
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
            #找低点
            key = df["key"].iloc[index:].min()
            key_index = df[df["key"] == key].index.tolist()[-1]
            df_line.loc[len(df_line)] = [df.iat[key_index, 0], key, "down", "temp", "","",""]
            key_index+=3
            #最后高点
            if (key_index  < len(df)):
                key = df["key"].iloc[key_index:].max()
                #是最高点
                if key == df["key"].iloc[key_index-2:].max():
                    key_index = df[df["key"] == key].index.tolist()[-1]
                    df_line.loc[len(df_line)] = [df.iat[key_index, 0], key, "rise", "temp", "","",""]
        else:
            # 找高点
            key = df["key"].iloc[index:].max()
            key_index = df[df["key"] == key].index.tolist()[-1]
            df_line.loc[len(df_line)] = [df.iat[key_index, 0], key, "rise", "temp", "","",""]
            key_index += 3
            # 最后低点
            if (key_index < len(df)):
                key = df["key"].iloc[key_index:].min()
                #是最低点
                if key == df["key"].iloc[key_index-2:].min():
                    key_index = df[df["key"] == key].index.tolist()[-1]
                    df_line.loc[len(df_line)] = [df.iat[key_index, 0], key, "down", "temp", "","",""]

        # 4月12日前版本
        # while i <len(df):
        #     if df_line.iloc[-1]["flag"] == "rise" :
        #         if df.iloc[i]["key"] >df_line.iloc[-1]["key"]:
        #             #更新高点
        #             df_line.iat[-1,0] = df.iloc[i]["date"]
        #             df_line.iat[-1, 1] = df.iloc[i]["key"]
        #             df_line.iat[-1, 3] = "temp"
        #             index = i
        #
        #         elif i>index+2:
        #             #向下一段
        #             if df.iloc[i]["key"] <df.iloc[index+1]["key"]:
        #                 df_line.loc[len(df_line)] = [df.iat[i, 0], df.iloc[i]["key"], "down", "temp","","",""]
        #                 index = i
        #
        #         i+=1
        #     elif df_line.iloc[-1]["flag"] == "down" :
        #         if df.iloc[i]["key"] <df_line.iloc[-1]["key"]:
        #             #更新低点
        #             df_line.iat[-1,0] = df.iloc[i]["date"]
        #             df_line.iat[-1, 1] = df.iloc[i]["key"]
        #             df_line.iat[-1, 3] = "temp"
        #             index = i
        #
        #         elif i>index+2:
        #             #向上一段
        #             if df.iloc[i]["key"] >df.iloc[index+1]["key"]:
        #                 df_line.loc[len(df_line)] = [df.iat[i, 0], df.iloc[i]["key"], "rise", "temp","","",""]
        #                 index = i
        #         i+=1

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
