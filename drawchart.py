#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright By Eric in 2020

import seaborn as sns
from datachart import DataChart
from stylechart import StyleChart


class DrawChart(object):
    def __init__(self):
        self.datachart = DataChart()
        self.stylechart = StyleChart()
        self.color = ["#293a80", "#537ec5", "#5f6769", "#90303d", "#c93756",
                      "#ed8240", "#018383", "#02a8a8", "#ee8572", "#bac7a7"]      # 设置自定义颜色序列
        self.field_dict = {'country': ['国家', 5], 'type': ['类型', 5], 'story': ['剧情', 5], 'china': ['中国', 3],
                           'usa': ['美国', 5], 'date': ['观看日期', 0], 'director': ['导演', 0.3],
                           'actors': ['演员', 0.3], 'value': ['评分', 0], 'year': ['年份', 3], 'month': ['月份', 2]}

    def bar(self, field, n):
        title = '【{}】柱状图(TOP {})'.format(self.field_dict[field][0], n)
        bar_data = self.datachart.bardata(field, n)
        if field == 'month':
            sns.barplot(x=bar_data[0], y=bar_data[1], palette=self.color)
        else:
            sns.barplot(x=bar_data.index, y=bar_data.values, palette=self.color)
        self.stylechart.bar(title, bar_data, self.field_dict[field][1])
        return

    def strip(self, field, n):
        title = '【{}】散点图(TOP {})'.format(self.field_dict[field][0], n)
        strip_data = self.datachart.stripdata(field, n).sample(frac=1)
        strip = sns.stripplot(x=field, y='value', data=strip_data, jitter=1, palette=self.color)
        width = strip_data[field].value_counts().count() - 1   # 在数据中提取元素个数控制线宽
        self.stylechart.strip('strip', title, width)
        return strip

    def violin(self, field, n):
        title = '【{}】小提琴图(TOP {})'.format(self.field_dict[field][0], n)
        violin_data = self.datachart.stripdata(field, n).sample(frac=1)     # 调用散点图的数据和样式表
        violin = sns.violinplot(x=field, y='value', data=violin_data, palette=self.color)
        width = violin_data[field].value_counts().count()-1     # 在数据中提取元素个数控制线宽
        self.stylechart.strip('violin', title, width)
        return violin

    def stripviolin(self, field, n):
        title = '【{}】散点图+小提琴图(TOP {})'.format(self.field_dict[field][0], n)
        s_v_data = self.datachart.stripdata(field, n).sample(frac=1)     # 调用散点图的数据和样式表
        violin = sns.violinplot(x=field, y='value', data=s_v_data, palette=self.color)
        strip = sns.stripplot(x=field, y='value', data=s_v_data, size=6, jitter=1, color='black')
        width = s_v_data[field].value_counts().count() - 1
        self.stylechart.strip('strip-violin', title, width)
        return [strip, violin]

    def dist(self, field, n):
        title = '【{}】直方图'.format(self.field_dict[field][0])
        distdata = self.datachart.distdata(field)
        dist = sns.distplot(distdata, kde_kws={'color': 'r'})
        self.stylechart.dist(title)
        return dist

    def reg(self, field, n):
        title = '【{}】线性回归图'.format(self.field_dict[field][0])
        regdata = self.datachart.regdata(field)
        reg = sns.regplot(x='my{}'.format(field), y=field, data=regdata, color='#293a80')
        self.stylechart.reg(title)
        return reg

    def kde(self, field, n):
        title = '【{}】核密度估计图'.format(self.field_dict[field][0])
        regdata = self.datachart.regdata(field)
        kde = sns.kdeplot(regdata['my{}'.format(field)], regdata[field])
        self.stylechart.reg(title)
        return kde

    def heatmap(self, field, n):
        title = '【{}】热力图(TOP {})'.format(self.field_dict[field][0], n)
        heatmapdata = self.datachart.heatmapdata(field, n)
        heatmap = sns.heatmap(data=heatmapdata, linewidths=.5, annot=True, cmap='YlGnBu')
        self.stylechart.heatmap(title)
        return heatmap
