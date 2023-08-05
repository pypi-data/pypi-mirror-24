#!/usr/bin/env python
#coding=utf-8

from pyecharts import Map

def test_map():

    # map_0
    value = [155, 10, 66, 78]
    attr = ["福建", "山东", "北京", "上海"]
    map = Map("全国地图示例", width=1200, height=600)
    map.add("", attr, value, maptype='china')
    map.show_config()
    map.render()

    # map_1
    value = [155, 10, 66, 78, 33, 80, 190, 53, 49.6]
    attr = ["福建", "山东", "北京", "上海", "甘肃", "新疆", "河南", "广西", "西藏"]
    map = Map("Map 结合 VisualMap 示例", width=1200, height=600)
    map.add("", attr, value, maptype='china', is_visualmap=True, visual_text_color='#000')
    map.show_config()
    map.render()

    # # map_2
    value = [20, 190, 253, 77, 65]
    attr = ['汕头市', '汕尾市', '揭阳市', '阳江市', '肇庆市']
    map = Map("广东地图示例", width=1200, height=600)
    map.add("", attr, value, maptype='广东', is_visualmap=True, visual_text_color='#000')
    map.show_config()
    map.render()