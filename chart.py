import os
import numpy as np
#绘图相关
import pandas as pd
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Kline,Line,Bar,Grid,Scatter
import yaml



# def timestamps(t):
#     timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")
#     timestamp = time.mktime(timeArray)
#     return int(timestamp)
# start = '2020-02-01 08:00:00'
# end = '2020-02-10 09:00:00'
# start_dt = timestamps(start)
# end_dt = timestamps(end)



def draw_kline(df,deal,line):


    # -----时间处理------------------
    date = df['date'].tolist()

    # -----K线处理------------------
    ohlc = df[['open', 'close', 'low', 'high']]  # oclh结构
    df['vol']=0
    v = df['vol']
    data = np.array(ohlc).tolist()  # 通过np转为list
    volumn = np.array(v).tolist()





    kline = (
        Kline()
        .add_xaxis(date)
        .add_yaxis(
            series_name="k",
            y_axis=data,
            itemstyle_opts=opts.ItemStyleOpts(
                color0="#ef232a",
                color="#14b143",
                border_color0="#ef232a",
                border_color="#14b143",
            ),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
                ]
            ),
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="category",
                is_scale=True,
                boundary_gap=False,
                axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                split_number=20,
                min_="dataMin",
                max_="dataMax",
            ),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line"),
            datazoom_opts=[opts.DataZoomOpts(
                    is_show=False, type_="inside", xaxis_index=[0, 0], range_end=100
                ),
                opts.DataZoomOpts(is_show=True, xaxis_index=[0, 1], range_end=100)
            ],
            # title_opts=opts.TitleOpts(title=file.split('\\')[-1].split('.')[0] + '/' + file.split('\\')[-2] +'min'),
        )
    )
    if(len(deal) != 0):

        simple_date = deal['date'].tolist()
        close = np.array(deal["key"]).tolist()
        ma_line = (
            Line()
                .add_xaxis(xaxis_data=simple_date)
                .add_yaxis(
                series_name="deal",
                y_axis=close,
                is_smooth=False,
                linestyle_opts=opts.LineStyleOpts(opacity=1),
                label_opts=opts.LabelOpts(is_show=False),
            )
            #     .add_yaxis(
            #     series_name="MA10",
            #     y_axis=ma2,
            #     is_smooth=True,
            #     linestyle_opts=opts.LineStyleOpts(opacity=1),
            #     label_opts=opts.LabelOpts(is_show=False),
            # )
                .set_global_opts(
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    grid_index=1,
                    axislabel_opts=opts.LabelOpts(is_show=False),
                ),
                yaxis_opts=opts.AxisOpts(
                    grid_index=1,
                    split_number=3,
                    axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=False),
                    axislabel_opts=opts.LabelOpts(is_show=True),
                ),
            )
        )
        overlap_k_line = kline.overlap(ma_line)
    else:
        overlap_k_line = kline
    if len(line) !=0:
        # line = pd.read_csv(line)
        line_date = line['date'].tolist()
        close = np.array(line["key"]).tolist()
        __line = (
            Line()
                .add_xaxis(xaxis_data=line_date)
                .add_yaxis(
                series_name="line",
                y_axis=close,
                is_smooth=False,
                linestyle_opts=opts.LineStyleOpts(opacity=2),
                label_opts=opts.LabelOpts(is_show=False),
            )
                #     .add_yaxis(
                #     series_name="MA10",
                #     y_axis=ma2,
                #     is_smooth=True,
                #     linestyle_opts=opts.LineStyleOpts(opacity=1),
                #     label_opts=opts.LabelOpts(is_show=False),
                # )
                .set_global_opts(
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    grid_index=1,
                    axislabel_opts=opts.LabelOpts(is_show=False),
                ),
                yaxis_opts=opts.AxisOpts(
                    grid_index=1,
                    split_number=3,
                    axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=False),
                    axislabel_opts=opts.LabelOpts(is_show=True),
                ),
            )
        )
        overlap_line = overlap_k_line.overlap(__line)
    else:
        overlap_line = overlap_k_line
    bar_vol = (
        Bar()
            .add_xaxis(xaxis_data=date)
            .add_yaxis(
            series_name="",
            y_axis=volumn,
            xaxis_index=1,
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(
                color=JsCode(
                    """
                function(params) {
                    var colorList;
                    if (barData[params.dataIndex][1] > barData[params.dataIndex][0]) {
                        colorList = '#14b143';
                    } else {
                        colorList = '#ef232a';
                    }
                    return colorList;
                }
                """
                )
            )
        )
    )
    grid_chart = Grid(init_opts=opts.InitOpts(width="1400px", height="800px"))
    grid_chart.add_js_funcs("var barData = {}".format(data))
    grid_chart.add(
        overlap_line,
        grid_opts=opts.GridOpts(
            pos_left="5%", pos_right="1%", pos_top="5%", height="60%"

        ))
    grid_chart.add(
        bar_vol,
        grid_opts=opts.GridOpts(
            pos_left="5%", pos_right="1%", pos_top="70%", height="20%"
        )
    )
    # grid_chart.render(target_path + file.split('\\')[-1].split('.')[0] + ".html")
    return grid_chart

def chart_test(df,deal,line):
    grid_chart = draw_kline(df,deal,line)
    return grid_chart





if __name__ == '__main__':
    # target = ['5','30', 'day']
    target = ['5','30']
    with open('config.yaml') as f:
        content = yaml.load(f, Loader=yaml.FullLoader)
        f.close()

    for i in target:
        path = content['path']
        simple_path = content['simple_'+str(i)+'_path']
        line_path = content['line_'+str(i)+'_path']
        deal_path = content['deal_'+str(i)+'_path']
        chart_path = content['chart_'+str(i)+'_path']
        # path = 'D:\project\data\stock\\normal\\'+i+'\\'
        for file_code in os.listdir(line_path):
            df = pd.read_csv(simple_path + file_code)
            deal = pd.read_csv(deal_path + file_code)
            line = pd.read_csv(line_path+file_code)
            chart = draw_kline(df, deal,line)
            chart.render(chart_path + file_code.split('.')[0] + ".html")


    # file_code = '002627.csv'
    # i = '5'
    # path = 'D:\project\data\stock\simple\\' + i + '\\'
    # simple_path = 'D:\project\data\stock\\deal\\'+i+'\\'
    # target_path = 'D:\project\data\stock\chart\\'+i+'\\'
    # line_path = 'D:\project\data\stock\line\\'+i+'\\'
    # draw_kline(path + file_code, target_path, simple_path + file_code,line_path+file_code)


