#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright By Eric in 2020


import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class StyleChart(object):
    def __init__(self):
        self.tag_s = 6  # 设置数据标签字体大小
        self.tick_s = 9  # 设置坐标轴刻度字体大小
        self.title_s = 16  # 设置标题字体大小

    # -------------直方图样式-------------
    def dist(self, title):
        sns.despine(left=True)  # 去除图像的边框
        plt.yticks([])
        plt.xlabel('')
        plt.ylabel('')
        plt.title(title, loc='left', fontsize=self.title_s)
        return

    # -------------柱状图样式-------------
    def bar(self, title, data, space):
        sns.despine(left=True)  # 去除图像的边框
        plt.tick_params(labelsize=self.tick_s)  # 设置坐标轴刻度字体大小
        plt.xlabel('')  # 去掉x坐标轴的标签
        plt.ylabel('')  # 去掉y坐标轴的标签
        plt.yticks([])  # 去掉y坐标轴轴线
        if title[1:3] == '月份':      # 月份的数据格式同其他的不一样
            plt.title(title[:-8], loc='left', fontsize=self.title_s)  # 设置标题及位置大小
            for i in range(data.shape[0]):  # 按位置逐项输出数据标签文字
                plt.text(
                    i, data.iat[i, 1] + space, data.iat[i, 1], fontsize=self.tag_s,
                    color="black", ha="center", va='bottom'
                )
        else:
            plt.title(title, loc='left', fontsize=self.title_s)  # 设置标题及位置大小
            for i in range(data.count()):  # 按位置逐项输出数据标签文字
                plt.text(
                    i, data[i] + space, data[i], fontsize=self.tag_s,
                    color="black", ha="center", va='bottom'
                )
        return

    # --------散点图、小提琴图样式----------
    def strip(self, style, title, width):
        sns.despine()  # 去除图像的上、右边框
        if style == 'strip':
            x = np.linspace(-0.5, width, 50)
            for i in [4, 7, 8, 9]:
                y = x * 0 + i
                plt.plot(x, y, color='#aaaaaa', linewidth=1.0, linestyle='--')
        plt.tick_params(labelsize=self.tick_s)  # 设置坐标轴刻度字体大小
        plt.xlabel('')  # 去掉x坐标轴的标签
        plt.ylabel('')  # 去掉y坐标轴的标签
        plt.yticks([4, 7, 8, 9], [r'很差', r'一般', r'不错', r'很好'])      # 设置y轴的刻度为文字
        plt.title(title, loc='left', fontsize=self.title_s)  # 设置标题及位置大小
        return

    # ------线性回归图,核密度估计图样式------
    def reg(self, title):
        sns.despine()  # 去除图像的上、右边框
        plt.xlabel('我的评分')
        plt.ylabel('豆瓣评分')
        plt.title(title, loc='left', fontsize=self.title_s)
        return

    # -------------热力图样式-------------
    def heatmap(self, title):
        sns.despine()  # 去除图像的边框
        plt.tick_params(labelsize=self.tick_s)  # 设置坐标轴刻度字体大小
        plt.xlabel('')  # 去掉x坐标轴的标签
        plt.ylabel('')  # 去掉y坐标轴的标签
        # plt.yticks([])  # 去掉y坐标轴轴线
        plt.title(title, loc='left', fontsize=self.title_s)  # 设置标题及位置大小
        return
