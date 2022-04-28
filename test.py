import time
from datetime import datetime



# timestr = '2022-04-24 14:h:00'
# datetime_obj = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
# obj_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
# print(obj_stamp)
i =0
while True:
    i+=1
    if i>3:
        print('braek')
        break

now_lowest_macd = df_4[df_4['macd'] > 0]['macd'].sum() * 1.2
now_lowest_macd_vaule = l_normal.iloc[now_lowest_end_index + 1]['macd']
last_lowest_start_index = l_deal[l_deal["date"] == l_line["date"].iloc[i - 1]].index.tolist()[0]
last_lowest_end_index = now_lowest_end_index
last_lowest = l_deal[last_lowest_start_index:last_lowest_end_index - 1].reset_index()
last_lowest_macd = find_last_1_macd(last_lowest, l_normal, "down")