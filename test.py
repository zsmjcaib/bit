import time
from datetime import datetime
import pandas as pd



# timestr = '2022-04-24 14:h:00'
# datetime_obj = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
# obj_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
# print(obj_stamp)
i =0
l = ['1','4','2']
a,b=l[0:2]
print('3' in l)
l = pd.DataFrame({'15m': '', '1h': '', '15m小转大': '', '1h小转大': ''}, index=[1])
print(len(l))
