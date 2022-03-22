# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 19:57:49 2022

@author: DELL

从labuladong的仓库中获取精选的算法文章列表
这些文章连接位于多个页面中，需使用循环进行多次提取
推荐使用方式二，用selenium提取

"""

import requests
from bs4 import BeautifulSoup
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

#%%  方式一：使用request和bs4进行提取
'''
由于提取过程中没有注意访问频率，最后
似乎出现ip被封，访问时服务器无应答，解封后可正常使用
'''
# 提取文章标题和对应的链接
def extract(url, data_id):
    # 请求标头
    headers = {
        ':authority':'github.com',
        ':method':'GET',
        ':path':'/labuladong/challenge/issues/25',
        ':scheme':'https',
        'accept':'text/html,applicatio***',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9',
        'cache-control':'max-age=0',
        'cookie':'_octo=GH1.1.74094463***',
        'if-none-match':'W/"452823babcd8b7073***',
        'referer':'https://github.com/labuladong',
        'sec-ch-ua':'" Not;A Brand";v="99***',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'sec-fetch-dest':'document',
        'sec-fetch-mode':'navigate',
        'sec-fetch-site':'same-origin',
        'sec-fetch-user':'?1',
        'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (Windows***',
    }
    try:
        # 注意是"https": 'http://127.0.0.1:4780'，而不是"https": 'https://127.0.0.1:4780'
        proxies = { "http": 'http://127.0.0.1:4780', "https": 'http://127.0.0.1:4780'}
        request = requests.get(url,headers,verify=False,proxies=proxies)
        
        html = request.text
        soup = BeautifulSoup(html, 'lxml')
        content = soup.select("#issue-{} > div > div.edit-comment-hide > task-lists > table > tbody > tr:nth-child(1) > td > p:nth-child(1) > a".format(data_id))
        return content[0].text, content[0].attrs['href']
        
    except:
        print("Failed to get text and link !!!  \n  url:{url} data_id:{data_id}".format(url=url, data_id=data_id))
        return False

# 获取每一个issue的data-id，data-id在使用选择器筛选信息时需要使用到
def get_id_list(issue_ids):
    headers = {
        ':authority': 'github.com',
        ':method': 'GET',
        ':path': '/labuladong/challenge/issues',
        ':scheme': 'https',
        'accept': 'text/html,applicatio***',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': '_octo=GH1.1.74094463***',
        'if-none-match': 'W/"f2b45a3570d32256b***',
        'referer': 'https://github.com/labuladong',
        'sec-ch-ua': '" Not;A Brand";v="99***',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows***',
        }
    try:
        # 注意是"https": 'http://127.0.0.1:4780'，而不是"https": 'https://127.0.0.1:4780'
        proxies = { "http": 'http://127.0.0.1:4780', "https": 'http://127.0.0.1:4780'}
        #proxies = {"http":None, "https":None}
        url = "https://github.com/labuladong/challenge/issues"
        response = requests.get(url,headers,verify=False,proxies=proxies)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        # 提取出data-id，并存放在列表中
        id_list = []
        for issue_id in issue_ids:
            content = soup.select("#issue_%d"%issue_id)
            id_list.append(content[0].attrs['data-id'])
            
        return id_list
    except:
        print("Failed to get data-id !!!")
        return []
        
# 获取全部的文章标题和链接，处理后保存当文件中
def get_info():
    # 由于issue编号中没有28，所以不能使用range(25,46)的方式来得到issue_id
    issue_ids = [25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46]
    id_list = get_id_list(issue_ids)
    index = 0
    for issue_id in issue_ids:
        data_id = id_list[index]
        url = "https://github.com/labuladong/challenge/issues/%d"%issue_ids[index]
        text, link = extract(url,data_id)
        print(text, link)
        # 等待4~10秒再进行下一次访问
        #wait_time = random.random()*6 + 4
        time.sleep(0.2)
        index += 1
        
#%%  方式二：使用selenium
'''
由于ip被封，改用selenium，其中issue-id和data-id在对网页html文本
使用正则表达式提取得到

在使用selenium时，不需要管header的设置，在访问外网时浏览器会使用可用的VPN，
无需手动设置代理，方便了很多
'''
def get_info_by_selenium():
    
    id_list = [{'issue_id': 46, 'data_id': 1112893683},
                {'issue_id': 45, 'data_id': 1111895236},
                {'issue_id': 44, 'data_id': 1111613887},
                {'issue_id': 43, 'data_id': 1111194536},
                {'issue_id': 42, 'data_id': 1109520975},
                {'issue_id': 41, 'data_id': 1108632725},
                {'issue_id': 40, 'data_id': 1107117260},
                {'issue_id': 39, 'data_id': 1106066770},
                {'issue_id': 38, 'data_id': 1105322273},
                {'issue_id': 37, 'data_id': 1104886301},
                {'issue_id': 36, 'data_id': 1104179494},
                {'issue_id': 35, 'data_id': 1102051261},
                {'issue_id': 34, 'data_id': 1100528865},
                {'issue_id': 33, 'data_id': 1099335683},
                {'issue_id': 32, 'data_id': 1098054599},
                {'issue_id': 31, 'data_id': 1097206181},
                {'issue_id': 30, 'data_id': 1096966902},
                {'issue_id': 29, 'data_id': 1096445353},
                {'issue_id': 27, 'data_id': 1095457418},
                {'issue_id': 26, 'data_id': 1094512019},
                {'issue_id': 25, 'data_id': 1093495976},]
    
    
    browser = webdriver.Chrome()
    content = []
    
    try:
        for item in id_list:
            data_id = item['data_id']
            url = "https://github.com/labuladong/challenge/issues/%d"%item['issue_id']
            browser.get(url)
            target = browser.find_element_by_css_selector("#issue-%d > div > div.edit-comment-hide > task-lists > table > tbody > tr:nth-child(1) > td > p:nth-child(1) > a"%item['data_id'])
            text, link = target.text, target.get_attribute('href')
            print(text, link)
            content.append([text,link])
            
            # 等待4~10秒再进行下一次访问
            wait_time = random.random()*6 + 4
            time.sleep(wait_time)
            
            
    finally:
        browser.close()
    
if __name__ == "__main__":
    get_info()             # 方式一
    # get_info_by_selenium()  # 方式二
    
'''
使用VScode正则处理后结果如下：
[单链表的六大解题套路，你都见过么？](https://mp.weixin.qq.com/s/dVqXEMKZ6_tuB7J-leLmtg)
[小而美的算法技巧：前缀和数组](https://mp.weixin.qq.com/s/EwAH3JDs5WFO6-LFmI3-2Q)
[小而美的算法技巧：差分数组技巧](https://mp.weixin.qq.com/s/123QujqVn3--gyeZRhxR-A)
[二维数组花式遍历技巧盘点](https://mp.weixin.qq.com/s/8jkzRKLNT-6CnEkvHp0ztA)
[滑动窗口技巧](https://mp.weixin.qq.com/s/ioKXTMZufDECBUwRRp3zaA)
[二分搜索技巧](https://labuladong.gitee.io/algo/1/9/)
[递归反转链表：如何拆解复杂问题](https://labuladong.gitee.io/algo/2/16/16/)
[如何在数组中以 O(1) 删除元素](https://labuladong.gitee.io/algo/2/20/61/)
[LRU 算法设计](https://labuladong.gitee.io/plugin-v3/?qno=146&target=gitee&_=1642200488200)
[二叉树算法入门](https://labuladong.gitee.io/plugin-v3/?qno=116&target=gitee)
[二叉搜索树基础操作](https://labuladong.gitee.io/plugin-v3/?qno=450)
[图论算法基础](https://labuladong.gitee.io/plugin-v3/?qno=797&target=gitee&_=1642288864543)
[二分图判定算法](https://labuladong.gitee.io/plugin-v3/?qno=785&target=gitee&_=1642389518965)
[BFS 算法基础](https://labuladong.gitee.io/plugin-v3/?qno=752)
[回溯算法核心原理](https://labuladong.gitee.io/plugin-v3/?qno=51)
[回溯算法解决排列/组合/子集问题](https://labuladong.gitee.io/plugin-v3/?qno=77)
[子集划分问题](https://labuladong.gitee.io/plugin-v3/?qno=698&target=gitee&_=1642696536440)
[动态规划核心原理](https://labuladong.gitee.io/plugin-v3/?qno=322)
[最长递增子序列](https://labuladong.gitee.io/plugin-v3/?qno=300)
[编辑距离](https://labuladong.gitee.io/plugin-v3/?qno=72)
[魔塔游戏](https://labuladong.gitee.io/plugin-v3/?qno=174)
'''

