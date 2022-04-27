import pandas as pd
import os
from chart import chart_test
import datetime

def judge_piont():


def strategy_test(test_15_simple,test_15_deal,test_15_line,test_1h_simple,test_1h_deal,test_1h_line,test_4h_simple,test_4h_deal,test_4h_line):
    index = test_15_simple[test_15_simple["date"] == test_15_line.iloc[-1]["date"]].index.tolist()[0]

    #判断端点
    judge_piont()