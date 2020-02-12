#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright By Eric in 2020

import random
import pandas as pd
from pymongo import MongoClient


class DataChart(object):
    def __init__(self):
        client = MongoClient('localhost', port=27017)
        db = client.movies
        collection = db.AllMovies
        self.data = pd.DataFrame(collection.find())

    # -------------柱状图数据-------------
    def bardata(self, field, n):
        if field == 'story':
            temp_type = self.data[['country', 'type']].query('type == "剧情"')   # 在数据库中提取两列数据使用query进行筛选
            bardata = temp_type['country'].value_counts()[0:10].sample(frac=1.0)   # 数据查重、打乱
        elif field == 'usa':
            temp_country = self.data[['country', 'type']].query('country == "美国"')
            bardata = temp_country['type'].value_counts()[0:10].sample(frac=1.0)    # 数据查重、打乱
        elif field == 'china':
            temp_country = self.data[['country', 'type']].query('country == "中国"')
            bardata = temp_country['type'].value_counts()[0:10].sample(frac=1.0)    # 数据查重、打乱
        elif field == 'actors':
            actors_data_list = []
            for m in self.data.actors.values.tolist():
                x = m.replace('[', '').replace(']', '').replace("'", '').replace(' ', '').split(',')
                for q in x:
                    actors_data_list.append(q)
            bardata = pd.DataFrame(actors_data_list)[0].value_counts()[0:int(n)].sample(frac=1.0)    # 数据查重、打乱
        elif field == 'year':       # 年份不需要打乱数据
            temp_date = self.data[['date']].dropna()            # 清理空值的行
            temp_date['year'] = temp_date['date'].dt.year       # 从date列中新生成year列
            temp_date['year'] = temp_date['year'].astype('str')   # 将year列转换为str类型
            temp_date.drop(temp_date[temp_date['year'] == '2020'].index, inplace=True)  # 去掉2020年的数据行
            bardata = temp_date[field].value_counts()          # 提取一列数据用value_counts查重统计
        elif field == 'month':       # 月份不需要查重、打乱数据
            temp_date = self.data[['date']].dropna()            # 清理空值的行
            temp_date['month'] = temp_date['date'].dt.month     # 从date列中新生成month列
            temp_date['month'] = temp_date['month'].astype('str')   # 将month列转换为str类型
            temp_list = []
            for i in range(1, 13):      # 用temp_list把1-12月份的数据排列
                temp_list.append((i, temp_date[field].value_counts().at[str(i)]))
            bardata = pd.DataFrame(temp_list)
        else:
            bardata = self.data[field].value_counts()[0: int(n)].sample(frac=1.0)   # 数据查重、打乱
        return bardata

    # --------散点图、小提琴图数据---------
    def stripdata(self, field, n):
        temp_data = self.bardata(field, n)
        if field == 'type':
            stripdata = self.data[[field, 'value']]
        elif field == 'country':
            # 用电影最多的前十个国家来对DataFrame进行筛选
            stripdata = self.data[[field, 'value']].query('country in @temp_data.index.tolist()')
        elif field == 'director':
            # 用电影最多的前十个国家来对DataFrame进行筛选
            stripdata = self.data[[field, 'value']].query('director in @temp_data.index.tolist()')
        else:
            a_v_data = pd.DataFrame(columns=['actors', 'value'])  # 定义一个空的DataFrame
            actors_data = self.bardata(field, n)
            for i in actors_data.index.tolist():  # 在已生成的actors_data中遍历数据
                temp_a_v_data = self.data[['actors', 'value']].query('actors.str.contains(@i)')  # 在data中按i筛选
                x = temp_a_v_data.copy()  # 用copy是为了不报错，不明白
                x.loc[:, 'actors'] = x.loc[:, 'actors'].map(lambda actors: i)  # 把筛选的结果整列替换成i
                a_v_data = a_v_data.append(x)  # 用append()添加到定义的DataFrame中
            stripdata = a_v_data
        return stripdata

    # -------------直方图数据-------------
    def distdata(self, field):
        distdata = self.data[field].dropna()
        return distdata

    # ------线性回归图,核密度估计图数据------
    def regdata(self, field):
        temp_data = self.data[['myvalue', field]]       # 取出字段
        regdata = temp_data.drop(temp_data[temp_data.myvalue == ""].index)      # 去掉含空值的行
        regdata['myvalue'] = regdata['myvalue'].astype('float')         # 把myvalue列转换为浮点型
        regdata['myvalue'].replace(1.0, 2.0, inplace=True)              # 去myvalue列中掉1分和2分的值
        for row in range(regdata.shape[0]):
            regdata.iat[row, 0] = (regdata.iat[row, 0]-random.random()) * 2     # 将myvalue列的值随机下浮动微处理
        return regdata

    # -------------热力图数据-------------
    def heatmapdata(self, field, n):
        m = 2 if field == 'country' else 0      # 如果字段名是国家，把美国、中国单独取出去
        if field == 'year':
            temp_date = self.data[['date', 'type']].dropna()  # 清理空值的行
            temp_date['year'] = temp_date['date'].dt.year  # 从date列中新生成year列
            temp_date['year'] = temp_date['year'].astype('str')  # 将year列转换为str类型
            temp_date.drop(temp_date[temp_date['year'] == '2020'].index, inplace=True)  # 去掉2020年的数据行
            temp_date.drop(['date'], inplace=True, axis=1)  # 删除date列
            temp_data = temp_date
        elif field == 'actors':
            a_v_data = pd.DataFrame(columns=['actors', 'type'])
            actors_data = self.bardata(field, n)        # 调用柱形图中的演员数据
            for i in actors_data.index.tolist():  # 在已生成的actors_data中遍历数据
                temp_a_v_data = self.data[['actors', 'type']].query('actors.str.contains(@i)')  # 在data中按i筛选
                x = temp_a_v_data.copy()  # 用copy是为了不报错，不明白
                x.loc[:, 'actors'] = x.loc[:, 'actors'].map(lambda actors: i)  # 把筛选的结果整列替换成i
                a_v_data = a_v_data.append(x)  # 用append()添加到定义的DataFrame中
            temp_data = a_v_data
        else:
            temp_data = self.data[[field, 'type']]  # 取出字段
        temp_data = temp_data.groupby([field, 'type']).size().reset_index(name="sum")   # 对两列进行统计去重
        heatmapdata = temp_data.pivot_table(index=field, columns='type', values='sum',
                                            fill_value=0, aggfunc='sum', margins=True)      # 生成数据透视表
        heatmapdata.drop(['All'], inplace=True)        # 删除合计行
        heatmapdata = heatmapdata.sort_values(by=['All'], ascending=False)[m:int(n)+m]      # 对数据透视表按合计进行排序
        heatmapdata.drop(['All'], inplace=True, axis=1)     # 删除合计列
        return heatmapdata
