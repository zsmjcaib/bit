import pandas as pd
import os


def find_point(df, df_point):

    df_point = find(df,df_point)

    return df_point


def  find(df, df_point):
    if(len(df) < 4):return
    #初始化
    if (len(df_point) < 2):
        for index in range(3,len(df)):
            if str(df.iat[index,0])=='2021-12-06 11:30:00':
                print(1)
            flag,mark,key =__deal(index, df, df_point)
            if(flag != "no"):
                # print(index)
                new = pd.DataFrame({"date":df.iat[index-1,0],"key":key,"flag":flag,"temp":"yes"},index=[1])
                df_point = df_point.append(new, ignore_index=True)
    #一般情况
    else:
        df_point.drop(df_point[df_point["temp"] == "yes"].index.tolist(), inplace=True)
        #最新位置的索引
        i ,df_point= find_index(df,df_point)
        for index in range(i,len(df)):



            flag, mark, key = __deal(index, df, df_point)
            if (flag != "no"):
                new = pd.DataFrame({"date": df.iat[index-1, 0], "key": key, "flag": flag, "temp": "yes"},index=[1])
                df_point = df_point.append(new, ignore_index=True)
    #结束添加临时顶底
    return __deal_temp(df, df_point)



def __deal(index, df, df_point):
    try:
        key,flag = df_point.iloc[-1, 1:3]

    except:
        key=0
        flag=None
    if (flag is None):
        if (df["low"].iloc[index - 1] <= df["low"].iloc[index] and df["low"].iloc[index - 1] <= df["low"].iloc[index - 2]):
            return "min", index - 1, df["low"].iloc[index - 1]
            # 判断顶点
        elif (df["high"].iloc[index - 1] >= df["high"].iloc[index] and df["high"].iloc[index - 1] >= df["high"].iloc[index - 2]):
            return "max", index - 1, df["high"].iloc[index - 1]

        return "no", -1, -1
    last_index = df[df["date"] == df_point.iat[-1, 0]].index.tolist()[0]

    #判断顶点
    if(df["high"].iloc[index-1]>=df["high"].iloc[index] and df["high"].iloc[index-1]>=df["high"].iloc[index-2]):
        if(flag == "min"):
            if last_index+3<index:
                #增加低点
                df_point.iat[-1, 3] = "no"
                return "max", index - 1, df["high"].iloc[index - 1]
            elif len(df_point)>2 and df["high"].iloc[index - 1] > df_point.iat[-2, 1]:
                if judge(last_index,index-1,df,'high') == index-1:
                    #删除最后高低点，并返回新高点
                    df_point.drop(df_point.tail(2).index, inplace=True)
                    return "max", index - 1, df["high"].iloc[index - 1]
        #更新顶点
        if(flag == "max" and key<=df["high"].iloc[index-1]):
            df_point.drop(df_point.tail(1).index, inplace=True)
            return "max", index - 1, df["high"].iloc[index - 1]

    # 判断低点
    elif(df["low"].iloc[index-1]<=df["low"].iloc[index] and df["low"].iloc[index-1]<=df["low"].iloc[index-2]):

        if(flag == "max" ):
            if last_index+3<index:
                df_point.iat[-1, 3] = "no"
                return "min", index - 1, df["low"].iloc[index - 1]
            elif len(df_point)>2 and df["low"].iloc[index - 1] < df_point.iat[-2, 1]:
                if judge(last_index,index-1,df,'low') == index-1:
                    df_point.drop(df_point.tail(2).index, inplace=True)
                    return "min", index - 1, df["low"].iloc[index - 1]
        #更新低点
        if(flag == "min" and key>=df["low"].iloc[index-1]) :
            df_point.drop(df_point.tail(1).index, inplace=True)
            return "min", index - 1, df["low"].iloc[index - 1]
       
    return "no", -1, -1
def __deal_temp(df, df_point):
    try:
        #最后一个临时关键点
        index = df[df["date"] == df_point.iat[-1,0]].index.tolist()[0]
        if df_point['flag'].iloc[-1] == 'min':
            if df['low'].iloc[-1]<df_point['key'].iloc[-1]:

                df_point.drop(df_point.tail(1).index, inplace=True)
                new = pd.DataFrame({"date": df["date"].iloc[-1], "key":df['low'].iloc[-1], "flag": "min", "temp": "yes"},index=[1])
                df_point = df_point.append(new, ignore_index=True)
            #找最后一点
            elif index+1>len(df):
                i = df['high'][index+1:].idxmax()
                new = pd.DataFrame({"date": df["date"].iloc[i], "key":df['high'].iloc[i], "flag": "max", "temp": "yes"},index=[1])
                df_point = df_point.append(new, ignore_index=True)
        else:
            if df['high'].iloc[-1]>df_point['key'].iloc[-1]:
                df_point.drop(df_point.tail(1).index, inplace=True)
                new = pd.DataFrame({"date": df["date"].iloc[-1], "key":df['high'].iloc[-1], "flag": "max", "temp": "yes"},index=[1])
                df_point = df_point.append(new, ignore_index=True)
            #找最后一点
            elif index+1>len(df):
                i = df['low'][index+1:].idxmin()
                new = pd.DataFrame({"date": df["date"].iloc[i], "key":df['low'].iloc[i], "flag": "min", "temp": "yes"},index=[1])
                df_point = df_point.append(new, ignore_index=True)
        return df_point
    except:
        print("worng:"+str(df.iat[-1,0]))
        return df_point

def find_index(df,df_point):
    while True:
        try:
            index = df[df["date"] == df_point["date"][df_point["temp"] == "no"].tolist()[-1]].index.tolist()[-1] + 2
            return index,df_point
        except:
            df_point = df_point[:-1]


def judge(last_index,index,df,direction):
    if direction == 'high':
        high = df['high'].iloc[index]
        low = df['low'].iloc[last_index]
    else:
        high = df['high'].iloc[last_index]
        low = df['low'].iloc[index]
    for i in range(last_index-1,1,-1):
        if direction == 'high':
            if df['high'].iloc[i]>high:
                return last_index
            if df['low'].iloc[i]<low:
                return index
        else:
            if df['high'].iloc[i]>high:
                return index
            if df['low'].iloc[i]<low:
                return last_index
    return last_index



if __name__ == '__main__':

    path = 'D:\project\data\stock\simple\\30\\'
    target_path = 'D:\project\data\stock\\deal\\30\\'
    file_code = '688125.csv'
    df = pd.read_csv(path + file_code)
    if not os.path.exists(target_path + file_code):
        file_object = open(target_path + file_code, 'w+')
        list = (
                "date" + "," + "key" + ","  + "flag" + ",temp"+"\n")
        file_object.writelines(list)
        file_object.close()
    df_point = pd.read_csv(target_path + file_code)
    df_point = find_point(df, df_point)
    df_point.to_csv(target_path + file_code, index=0)



    # target = ['5']
    # for i in target:
    #     path = 'D:\project\data\stock\simple\\'+i+'\\'
    #     target_path = 'D:\project\data\stock\\deal\\'+i+'\\'
    #     for file_code in os.listdir(path)[0:int((len(os.listdir(path))+1)/2)]:
    #
    #         find_point(path +file_code, target_path + file_code)