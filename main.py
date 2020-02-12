#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright By Eric in 2020

import time
import json
from execchart import ExecChart


def main():
    time_start = time.time()
    chart = ExecChart()
    with open('chartname.json', 'r', encoding='utf-8') as file:
        chart_name = json.load(file)
    for k, n in chart_name.items():
        t1 = time.time()
        chart.assemble(k, n)
        t2 = time.time()
        print('----执行时间：{:.04f}'.format(t2 - t1))
    print('----全部图片保存完毕。')
    time_end = time.time()
    print('全部程序的执行时间：{:.04f}'.format(time_end - time_start))


if __name__ == '__main__':
    main()
