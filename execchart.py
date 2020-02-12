#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright By Eric in 2020

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from drawchart import DrawChart


class ExecChart(object):
    def __init__(self):
        self.drawchart = DrawChart()
        self.wight = 12     # 设置画布宽度
        self.height = 6.75  # 设置画面高度
        self.dpi = 300      # 设置输出图片的dpi
        myfont = FontProperties(fname=r'C:\Windows\Fonts\msyhbd.ttc')   # 设置字体为微软雅黑
        sns.set(font=myfont.get_name(), style='white', palette="deep")  # 设置图形背景和调色板主题

    def assemble(self, name, n):
        plt.figure(num=name, figsize=(self.wight, self.height))     # 定义画布
        name_s = name.split('_')
        exec('self.drawchart.{}("{}", "{}")'.format(name_s[0], name_s[-1], n))
        plt.savefig(r'picture\{}.png'.format(name), dpi=self.dpi)   # 保存图片
        print('正在生成并保存picture\%s.png......' % name)
        plt.close()
        return
