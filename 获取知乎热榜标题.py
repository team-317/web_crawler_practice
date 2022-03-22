'''
title: 
author: team317
Date: 2022-03-22
categories:  
  - ""
tags:  
  - ""
'''
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 17:58:02 2021

@author: Team317
"""


# 获取热榜
import requests
from bs4 import BeautifulSoup
from lxml import etree
from pyquery import PyQuery as pq

def test1(headers):
    r = requests.get("https://www.zhihu.com/hot",headers = headers)
    print(r.text)
if __name__ == '__main__':
    headers = {
        'accept':'*/*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9',
        'cookie':'q_c1=2e59e7954ea94fe***',
        'referer':'http',
        'sec-ch-ua':'" Not A;Brand";v="99***',
        'sec-ch-ua-mobile':'?0',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-origin',
        'user-agent':'Mozilla/5.0 (Windows***',

    }
    test(headers)