#!/usr/bin/env python
#coding=utf-8

from pyecharts.base import Base
from pyecharts.option import get_all_options

class Line(Base):
    """
    <<< 折线/面积图 >>>
    折线图是用折线将各个数据点标志连接起来的图表，用于展现数据的变化趋势。
    """
    def __init__(self, title="", subtitle="", **kwargs):
        super(Line, self).__init__(title, subtitle, **kwargs)

    def add(self, *args, **kwargs):
        self.__add(*args, **kwargs)

    def __add(self, name, x_axis, y_axis,
              is_symbol_show=True,
              is_smooth=False,
              is_stack=False,
              is_step=False,
              is_fill=False,
              **kwargs):
        """

        :param name:
            图例名称
        :param x_axis:
            x 坐标轴数据
        :param y_axis:
            y 坐标轴数据
        :param is_symbol_show:
            是否显示标记图形
        :param is_smooth:
            是否平滑曲线显示
        :param is_stack:
            数据堆叠，同个类目轴上系列配置相同的 stack 值可以堆叠放置
        :param is_step:
            是否是阶梯线图。可以设置为 true 显示成阶梯线图。
            也支持设置成 start, middle, end 分别配置在当前点，当前点与下个点的中间点，下个点拐弯。
        :param is_fill:
            是否填充曲线所绘制面积
        :param kwargs:
        """
        if isinstance(x_axis, list) and isinstance(y_axis, list):
            assert len(x_axis) == len(y_axis)
            kwargs.update(x_axis=x_axis, type="line")
            chart = get_all_options(**kwargs)
            xaxis, yaxis = chart['xy_axis']
            is_stack = "stack" if is_stack else ""
            _area_style = {"normal": chart['area_style']} if is_fill else {}
            self._option.update(xAxis=xaxis, yAxis=yaxis)
            self._option.get('legend')[0].get('data').append(name)
            self._option.get('series').append({
                "type": "line",
                "name": name,
                "symbol": chart['symbol'],
                "smooth": is_smooth,
                "step": is_step,
                "stack": is_stack,
                "showSymbol": is_symbol_show,
                "data": y_axis,
                "label": chart['label'],
                "lineStyle": chart['line_style'],
                "areaStyle": _area_style,
                "markPoint": chart['mark_point'],
                "markLine": chart['mark_line'],
                "indexflag": self._option.get('_index_flag')
            })
            self._legend_visualmap_colorlst(**kwargs)
        else:
            raise TypeError("x_axis and y_axis must be list")
