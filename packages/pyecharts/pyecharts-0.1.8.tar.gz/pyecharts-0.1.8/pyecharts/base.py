#!/usr/bin/env python
#coding=utf-8

import json
import random
import datetime

from pprint import pprint
from jinja2 import Template
from pyecharts.option import get_all_options
from pyecharts import temple as Tp


class Base(object):

    def __init__(self, title, subtitle,
                 width=800,
                 height=400,
                 title_pos="auto",
                 title_top="auto",
                 title_color="#000",
                 subtitle_color="#aaa",
                 title_text_size=18,
                 subtitle_text_size=12,
                 background_color="#fff",
                 is_grid=False):
        """

        :param title:
            主标题文本，支持 \n 换行
        :param subtitle:
            副标题文本，支持 \n 换行
        :param width:
            画布宽度
        :param height:
            画布高度
        :param title_pos:
            标题距离左侧距离，有'auto', 'left', 'right', 'center'可选，也可为百分比或整数
        :param title_top:
            标题距离顶部距离，有'top', 'middle', 'bottom'可选，也可为百分比或整数
        :param title_color:
            主标题文本颜色
        :param subtitle_color:
            副标题文本颜色
        :param title_text_size:
            主标题文本字体大小
        :param subtitle_text_size:
            副标题文本字体大小
        :param background_color:
            画布背景颜色
        :param is_grid:
            是否使用 grid 组件，用于并行显示图表。
        """
        self._option = {}
        if is_grid:
            self._option.update(grid=[])
        self._width, self._height = width, height
        self._colorlst = ['#c23531', '#2f4554', '#61a0a8', '#d48265', '#749f83',
                          '#ca8622', '#bda29a', '#6e7074', '#546570', '#c4ccd3',
                          '#f05b72', '#ef5b9c', '#f47920', '#905a3d', '#fab27b',
                          '#2a5caa', '#444693', '#726930', '#b2d235', '#6d8346',
                          '#ac6767', '#1d953f', '#6950a1', '#918597', '#f6f5ec']
        self._option.update(
            title=[{
                "text": title,
                "subtext": subtitle,
                "left": title_pos,
                "top": title_top,
                "textStyle": {"color": title_color, "fontSize": title_text_size},
                "subtextStyle": {"color": subtitle_color, "fontSize": subtitle_text_size}
            }],
            toolbox={
                "show": True,
                "orient": "vertical",
                "left": "right",
                "top": "center",
                "feature": {"saveAsImage": {"show": True}}
            },
            _index_flag=random.randint(1000000, 2000000),
            tooltip={},
            series=[],
            legend=[{"data": []}],
            backgroundColor=background_color
        )

    def add(self, angle_data=None,
            angle_range=None,
            area_color=None,
            area_opacity=None,
            axis_range=None,
            border_color=None,
            boundary_gap=None,
            center=None,
            clockwise=None,
            datazoom_type=None,
            datazoom_range=None,
            edge_length=None,
            effect_brushtype=None,
            effect_period=None,
            effect_scale=None,
            formatter=None,
            geo_emphasis_color=None,
            geo_normal_color=None,
            grid_width=None,
            grid_height=None,
            grid_top=None,
            grid_bottom=None,
            grid_left=None,
            grid_right=None,
            gravity=None,
            interval=None,
            is_angleaxis_show=None,
            is_area_show=None,
            is_axisline_show=None,
            is_calculable=None,
            is_convert=None,
            is_datazoom_show=None,
            is_emphasis=None,
            is_fill=None,
            is_focusnode=None,
            is_label_show=None,
            is_legend_show=None,
            is_liquid_animation=None,
            is_liquid_outline_show=None,
            is_radiusaxis_show=None,
            is_random=None,
            is_roam=None,
            is_rotatelabel=None,
            is_smooth=None,
            is_splitline_show=None,
            is_stack=None,
            is_step=None,
            is_symbol_show=None,
            is_visualmap=None,
            item_color=None,
            label_color=None,
            label_pos=None,
            label_text_color=None,
            label_text_size=None,
            layout=None,
            legend_orient=None,
            legend_pos=None,
            legend_top=None,
            line_curve=None,
            line_opacity=None,
            line_type=None,
            line_width=None,
            liquid_color=None,
            maptype=None,
            mark_line=None,
            mark_point=None,
            mark_point_symbol=None,
            mark_point_symbolsize=None,
            mark_point_textcolor=None,
            namegap=None,
            rader_text_color=None,
            radius_data=None,
            radius=None,
            repulsion=None,
            rosetype=None,
            rotate_step=None,
            scale_range=None,
            shape=None,
            start_angle=None,
            symbol_size=None,
            symbol=None,
            type=None,
            visual_orient=None,
            visual_range_color=None,
            visual_range_text=None,
            visual_range=None,
            visual_text_color=None,
            visual_pos=None,
            visual_top=None,
            word_gap=None,
            word_size_range=None,
            x_axis=None,
            xaxis_name_pos=None,
            xaxis_name=None,
            xy_text_size=None,
            yaxis_formatter=None,
            yaxis_name_pos=None,
            yaxis_name=None):
        """ base 父类的 add 方法只是为了提供提示选项 """
        pass

    def custom(self, series):
        """ 追加自定义图表类型

        :param series:
            追加图表类型的 series 数据
        """
        _name, _series, _xaxis, _yaxis, _legend, _title = series
        for n in _name:
            self._option.get('legend')[0].get('data').append(n)
        for s in _series:
            self._option.get('series').append(s)

    def __custom_for_grid(self, series):
        """

        :param series:
            追加图表类型的 series 数据
        :return:
        """
        _name, _series, _xaxis, _yaxis, _legend, _title = series
        for s in _series:
            self._option.get('series').append(s)
        return len(self._option.get('series')), len(_series), _xaxis, _yaxis, _legend, _title

    def grid(self, series,
             grid_width=None,
             grid_height=None,
             grid_top=None,
             grid_bottom=None,
             grid_left=None,
             grid_right=None):
        """ 并行显示图表

        :param series:
            追加图表类型的 series 数据
        :param grid_width:
            grid 组件的宽度。默认自适应。
        :param grid_height:
            grid 组件的高度。默认自适应。
        :param grid_top:
            grid 组件离容器顶部的距离。
        :param grid_bottom:
            grid 组件离容器底部的距离。
        :param grid_left:
            grid 组件离容器左侧的距离。
        :param grid_right:
            grid 组件离容器右侧的距离。
        :return:
        """
        from pyecharts.option import grid
        _index, _index_once, _xaxis, _yaxis, _legned, _title = self.__custom_for_grid(series)
        self._option.get('legend').append(_legned)
        self._option.get('title').append(_title)
        if _xaxis and _yaxis is not None:
            try:
                _xaxis[0].update(gridIndex=_index - 1)
                _yaxis[0].update(gridIndex=_index - 1)
                self._option.get('xAxis').append(_xaxis[0])
                self._option.get('yAxis').append(_yaxis[0])
            except:
                pass
            # indexflag 为每个图例唯一标识
            _flag = self._option.get('series')[0].get('indexflag')
            _series_index = 0
            for s in self._option.get('series'):
                if _flag == s.get('indexflag'):
                    s.update(xAxisIndex=_series_index, yAxisIndex=_series_index)
                else:
                    _series_index += 1
                    s.update(xAxisIndex=_series_index, yAxisIndex=_series_index)
                _flag = s.get('indexflag')

        _grid = grid(grid_width, grid_height, grid_top,
                     grid_bottom, grid_left, grid_right)
        for _ in range(_index_once):
            self._option.get('grid').append(_grid)

    def get_series(self):
        """ 获取图表的 series 数据 """
        return self._option.get('legend')[0].get('data'), self._option.get('series'),\
               self._option.get('xAxis', None), self._option.get('yAxis', None),\
               self._option.get('legend')[0], self._option.get('title')[0]

    def show_config(self):
        """ 打印输出 option 所有配置项 """
        pprint(self._option)

    @staticmethod
    def cast(seq):
        """ 转换数据序列，将带字典和元祖类型的序列转换为 k_lst,v_lst 两个列表
        1.[(A1, B1),(A2, B2),(A3, B3),(A4, B4)] --> k_lst[A[i1,i2...]], v_lst[B[i1,i2...]]
        2.[{A1: B1},{A2: B2},{A3: B3},{A4: B4}] --> k_lst[A[i1,i2...]], v_lst[B[i1,i2...]]
        3.{A1: B1, A2: B2, A3: B3, A4: B4} -- > k_lst[A[i1,i2...]], v_lst[B[i1,i2...]]

        :param seq:
            转换的序列
        :return:
        """
        k_lst, v_lst = [], []
        if isinstance(seq, list):
            for s in seq:
                try:
                    if isinstance(s, tuple):
                        _attr, _value = s
                        k_lst.append(_attr)
                        v_lst.append(_value)
                    elif isinstance(s, dict):
                        for k, v in s.items():
                            k_lst.append(k)
                            v_lst.append(v)
                except:
                    raise
        elif isinstance(seq, dict):
            for k, v in seq.items():
                k_lst.append(k)
                v_lst.append(v)
        return k_lst, v_lst

    def _legend_visualmap_colorlst(self, is_visualmap=False, **kwargs):
        """ 配置 legend，visualmap 以及 colorlst

        :param is_visualmap:
            是否显示 visualmap 组件
        :param kwargs:
        """
        kwargs.update(colorlst=self._colorlst)
        chart = get_all_options(**kwargs)
        if is_visualmap:
            self._option.update(visualMap=chart['visual_map'])
        self._option.get('legend')[0].update(chart['legend'])
        if chart['grid']:
            self._option.get('grid').append(chart['grid'])
        self._option.update(color=chart['color'])
        if kwargs.get('is_datazoom_show', None) is True:
            self._option.update(dataZoom=chart['datazoom'])

    def render(self, path="render.html"):
        """ 渲染数据项，生成 html 文件

        :param path:
            生成 html 文件保存路径
        """
        temple = Tp._temple
        series = self._option.get("series")
        for s in series:
            if s.get('type') == "wordCloud":
                temple = Tp._temple_wd
                break
            if s.get('type') == "liquidFill":
                temple = Tp._temple_lq
                break
        my_option = json.dumps(self._option, indent=4, ensure_ascii=False)
        tmp = Template(temple)
        html = tmp.render(myOption=my_option, myWidth=self._width, myHeight=self._height)
        try:        # for Python3
            with open(path, "w+", encoding="utf-8") as fout:
                fout.write(html)
        except:     # for Python2
            with open(path, "w+") as fout:
                fout.write(html)

    def render_notebook(self):
        """ 渲染数据项，在 notebook 中显示

        :return:
        """
        from IPython.display import HTML

        divid = datetime.datetime.now()
        my_option = json.dumps(self._option, indent=4)
        temple = Tp._temple_notebook
        series = self._option.get("series")
        for s in series:
            if s.get('type') == "wordCloud":
                temple = Tp._temple_wd_notebook
                break
            if s.get('type') == "liquidFill":
                temple = Tp._temple_lq_notebook
                break
            if s.get('type') == 'map':
                temple = Tp.get_map(self._option.get('series')[0].get('mapType'))
                break
        tmp = Template(temple)
        try:
            html = tmp.render(myOption=my_option, chartId=divid, myWidth=self._width, myHeight=self._height)
        except:
            html = tmp.render(mtOption=my_option.decode('utf8'), chartId=divid, myWidth=self._width,
                              myHeight=self._height)
        return HTML(html)

    @property
    def _geo_cities(self):
        """ 返回 geo 组件中国各大城市经纬度 """
        return {
            "海门": [121.15, 31.89],
            "鄂尔多斯": [109.781327, 39.608266],
            "招远": [120.38, 37.35],
            "舟山": [122.207216, 29.985295],
            "齐齐哈尔": [123.97, 47.33],
            "盐城": [120.13, 33.38],
            "赤峰": [118.87, 42.28],
            "青岛": [120.33, 36.07],
            "乳山": [121.52, 36.89],
            "金昌": [102.188043, 38.520089],
            "泉州": [118.58, 24.93],
            "莱西": [120.53, 36.86],
            "日照": [119.46, 35.42],
            "胶南": [119.97, 35.88],
            "南通": [121.05, 32.08],
            "拉萨": [91.11, 29.97],
            "云浮": [112.02, 22.93],
            "梅州": [116.1, 24.55],
            "文登": [122.05, 37.2],
            "上海": [121.48, 31.22],
            "攀枝花": [101.718637, 26.582347],
            "威海": [122.1, 37.5],
            "承德": [117.93, 40.97],
            "厦门": [118.1, 24.46],
            "汕尾": [115.375279, 22.786211],
            "潮州": [116.63, 23.68],
            "丹东": [124.37, 40.13],
            "太仓": [121.1, 31.45],
            "曲靖": [103.79, 25.51],
            "烟台": [121.39, 37.52],
            "福州": [119.3, 26.08],
            "瓦房店": [121.979603, 39.627114],
            "即墨": [120.45, 36.38],
            "抚顺": [123.97, 41.97],
            "玉溪": [102.52, 24.35],
            "张家口": [114.87, 40.82],
            "阳泉": [113.57, 37.85],
            "莱州": [119.942327, 37.177017],
            "湖州": [120.1, 30.86],
            "汕头": [116.69, 23.39],
            "昆山": [120.95, 31.39],
            "宁波": [121.56, 29.86],
            "湛江": [110.359377, 21.270708],
            "揭阳": [116.35, 23.55],
            "荣成": [122.41, 37.16],
            "连云港": [119.16, 34.59],
            "葫芦岛": [120.836932, 40.711052],
            "常熟": [120.74, 31.64],
            "东莞": [113.75, 23.04],
            "河源": [114.68, 23.73],
            "淮安": [119.15, 33.5],
            "泰州": [119.9, 32.49],
            "南宁": [108.33, 22.84],
            "营口": [122.18, 40.65],
            "惠州": [114.4, 23.09],
            "江阴": [120.26, 31.91],
            "蓬莱": [120.75, 37.8],
            "韶关": [113.62, 24.84],
            "嘉峪关": [98.289152, 39.77313],
            "广州": [113.23, 23.16],
            "延安": [109.47, 36.6],
            "太原": [112.53, 37.87],
            "清远": [113.01, 23.7],
            "中山": [113.38, 22.52],
            "昆明": [102.73, 25.04],
            "寿光": [118.73, 36.86],
            "盘锦": [122.070714, 41.119997],
            "长治": [113.08, 36.18],
            "深圳": [114.07, 22.62],
            "珠海": [113.52, 22.3],
            "宿迁": [118.3, 33.96],
            "咸阳": [108.72, 34.36],
            "铜川": [109.11, 35.09],
            "平度": [119.97, 36.77],
            "佛山": [113.11, 23.05],
            "海口": [110.35, 20.02],
            "江门": [113.06, 22.61],
            "章丘": [117.53, 36.72],
            "肇庆": [112.44, 23.05],
            "大连": [121.62, 38.92],
            "临汾": [111.5, 36.08],
            "吴江": [120.63, 31.16],
            "石嘴山": [106.39, 39.04],
            "沈阳": [123.38, 41.8],
            "苏州": [120.62, 31.32],
            "茂名": [110.88, 21.68],
            "嘉兴": [120.76, 30.77],
            "长春": [125.35, 43.88],
            "胶州": [120.03336, 36.264622],
            "银川": [106.27, 38.47],
            "张家港": [120.555821, 31.875428],
            "三门峡": [111.19, 34.76],
            "锦州": [121.15, 41.13],
            "南昌": [115.89, 28.68],
            "柳州": [109.4, 24.33],
            "三亚": [109.511909, 18.252847],
            "自贡": [104.778442, 29.33903],
            "吉林": [126.57, 43.87],
            "阳江": [111.95, 21.85],
            "泸州": [105.39, 28.91],
            "西宁": [101.74, 36.56],
            "宜宾": [104.56, 29.77],
            "呼和浩特": [111.65, 40.82],
            "成都": [104.06, 30.67],
            "大同": [113.3, 40.12],
            "镇江": [119.44, 32.2],
            "桂林": [110.28, 25.29],
            "张家界": [110.479191, 29.117096],
            "宜兴": [119.82, 31.36],
            "北海": [109.12, 21.49],
            "西安": [108.95, 34.27],
            "金坛": [119.56, 31.74],
            "东营": [118.49, 37.46],
            "牡丹江": [129.58, 44.6],
            "遵义": [106.9, 27.7],
            "绍兴": [120.58, 30.01],
            "扬州": [119.42, 32.39],
            "常州": [119.95, 31.79],
            "潍坊": [119.1, 36.62],
            "重庆": [106.54, 29.59],
            "台州": [121.420757, 28.656386],
            "南京": [118.78, 32.04],
            "滨州": [118.03, 37.36],
            "贵阳": [106.71, 26.57],
            "无锡": [120.29, 31.59],
            "本溪": [123.73, 41.3],
            "克拉玛依": [84.77, 45.59],
            "渭南": [109.5, 34.52],
            "马鞍山": [118.48, 31.56],
            "宝鸡": [107.15, 34.38],
            "焦作": [113.21, 35.24],
            "句容": [119.16, 31.95],
            "北京": [116.46, 39.92],
            "徐州": [117.2, 34.26],
            "衡水": [115.72, 37.72],
            "包头": [110, 40.58],
            "绵阳": [104.73, 31.48],
            "乌鲁木齐": [87.68, 43.77],
            "枣庄": [117.57, 34.86],
            "杭州": [120.19, 30.26],
            "淄博": [118.05, 36.78],
            "鞍山": [122.85, 41.12],
            "溧阳": [119.48, 31.43],
            "库尔勒": [86.06, 41.68],
            "安阳": [114.35, 36.1],
            "开封": [114.35, 34.79],
            "济南": [117, 36.65],
            "德阳": [104.37, 31.13],
            "温州": [120.65, 28.01],
            "九江": [115.97, 29.71],
            "邯郸": [114.47, 36.6],
            "临安": [119.72, 30.23],
            "兰州": [103.73, 36.03],
            "沧州": [116.83, 38.33],
            "临沂": [118.35, 35.05],
            "南充": [106.110698, 30.837793],
            "天津": [117.2, 39.13],
            "富阳": [119.95, 30.07],
            "泰安": [117.13, 36.18],
            "诸暨": [120.23, 29.71],
            "郑州": [113.65, 34.76],
            "哈尔滨": [126.63, 45.75],
            "聊城": [115.97, 36.45],
            "芜湖": [118.38, 31.33],
            "唐山": [118.02, 39.63],
            "平顶山": [113.29, 33.75],
            "邢台": [114.48, 37.05],
            "德州": [116.29, 37.45],
            "济宁": [116.59, 35.38],
            "荆州": [112.239741, 30.335165],
            "宜昌": [111.3, 30.7],
            "义乌": [120.06, 29.32],
            "丽水": [119.92, 28.45],
            "洛阳": [112.44, 34.7],
            "秦皇岛": [119.57, 39.95],
            "株洲": [113.16, 27.83],
            "石家庄": [114.48, 38.03],
            "莱芜": [117.67, 36.19],
            "常德": [111.69, 29.05],
            "保定": [115.48, 38.85],
            "湘潭": [112.91, 27.87],
            "金华": [119.64, 29.12],
            "岳阳": [113.09, 29.37],
            "长沙": [113, 28.21],
            "衢州": [118.88, 28.97],
            "廊坊": [116.7, 39.53],
            "菏泽": [115.480656, 35.23375],
            "合肥": [117.27, 31.86],
            "武汉": [114.31, 30.52],
            "大庆": [125.03, 46.58]
        }