import time
from datetime import datetime
import pandas as pd



# timestr = '2022-04-24 14:h:00'
# datetime_obj = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
# obj_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
# print(obj_stamp)
demo = pd.DataFrame(
    columns=['date', 'first', '15m', '1h', '15m小转大', '1h小转大', 'flag', 'loss', 'point', 'is_grid', 'grid', 'sl',
             'direction', 'extremum'])

l = pd.DataFrame(
    {'date': '', 'first': 'yes', '15m': '', '1h': '', '15m小转大': '', '1h小转大': '', 'flag': '', 'loss': '', 'point': '',
     'is_grid': '', 'grid': '', 'sl': '', 'direction': ''}, index=[1])
print(1)
