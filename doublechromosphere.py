#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time : 2019/11/16 19:35:00
# @Email : jtyoui@qq.com
# @Software : PyCharm
"""爬取福利彩票官方双色球数据"""
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import pprint


def double_data_chart(start: str = None, end: str = None):
    """爬取双色球数据

    :param start: 开始期号：默认是最早的一期
    :param end:   结束期号：默认是最新的一期
    :return: 二维列表: '红1', '红2', '红3', '红4', '红5', '红6', '篮球'
    """
    header, charts = ['期号', '红1', '红2', '红3', '红4', '红5', '红6', '篮球'], []
    url = 'https://datachart.500.com/ssq/history/newinc/history.php'
    start = start or '03001'
    if end is None:
        text = requests.get(url=url, params={'user-agent': UserAgent().random}).text
        soup = BeautifulSoup(text, 'html.parser')
        end = soup.find(name='input', id='end').get('value')
    reptile_url = url + f'?start={start}&end={end}'
    text = requests.get(url=reptile_url, params={'user-agent': UserAgent().random}).text
    soup = BeautifulSoup(text, 'html.parser')
    for data in soup.find_all(name='tr', class_='t_tr1'):
        ls = [int(content.text) for content in data.contents[1:9]]
        charts.append(ls)
    charts.reverse()
    charts.insert(0, header)
    return charts


if __name__ == '__main__':
    pprint.pprint(double_data_chart())
