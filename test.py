import time
from datetime import datetime



# timestr = '2022-04-24 14:30:00'
# datetime_obj = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
# obj_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
# print(obj_stamp)
i =0
while True:
    i+=1
    if i>3:
        print('braek')
        break