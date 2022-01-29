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
似乎出现ip被封，访问时服务器无应答
'''
# 提取文章标题和对应的链接
def extract(url, data_id):
    # 请求标头
    headers = {
        ':authority':'github.com',
        ':method':'GET',
        ':path':'/labuladong/challenge/issues/25',
        ':scheme':'https',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9',
        'cache-control':'max-age=0',
        'cookie':'_octo=GH1.1.740944638.1628754231; _device_id=5f57192446afa215a977844d244be53f; tz=Asia%2FShanghai; tz=Asia%2FShanghai; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; user_session=Zij1dWQXpFTr_0a9RT0Wd5bOhctB0MPTu53pjhqg6aNPnfAu; __Host-user_session_same_site=Zij1dWQXpFTr_0a9RT0Wd5bOhctB0MPTu53pjhqg6aNPnfAu; logged_in=yes; dotcom_user=Tom-DaLin; has_recent_activity=1; _gh_sess=cT9g7DaV5JolHAjb7PXX%2B%2FNkkUnIWZiq564qMjy2hJ7%2B1aJRIfOxXwizNVPccwBW1VuenFwmubj2nNipGjVfMhA4F2o5VNvnRyCcCARH6Jf%2FBUS0sSDmGcL5Cxw3PmXXFhiQl92VSg8e8MxLy0ZsnuRTgoauf8%2Bkk8xXCBW%2BuberJ9PSv3lB4%2BJwP4ZddLw2ZcWEiuPgAumSnrWa6jc4Jl4vdGt7Jgm6Yg8%2BrLg67%2FOyI7JXnzlmRyf9rCXSBVM8mtYVWGCmJyrFbQvDrUB8xsttQeqw4SyvReH8e1c09XcKmIdcNjYY95Zig5%2Bh0E7oZtMFE9J9APLWvfjHvWxkSMf%2FTj0crC%2FP8pqT9mlnxWI5aBogU%2FFDeIe5aafvV%2Fmdu658Lrhqga5rK4GAqiMzOBMIONoA7%2BLSKUXaIaxC9z7bDMwWGbB7mTZTb6Mfo57Uxng2V%2FqoGWSoFvNE%2BaXqOqTLTaotqUrYmfinmHdxqgZXIXz%2FdrFOKuxgdp4Z3ThtEctP1tnwNNZi4eQzbipGMOnyKdWuuPyEXHHWwgy3rc50nKhhImPHO2CEFo1eIBfwvaFKR8isK%2Fc%2Ffg8%2FntZ2JjrckRpNX%2FSStO0w8Cj6rq0fT2tWXwnhMgV%2F5srNcQUA2BGxNKdZE6r%2F6XMpC82ebOyGYKTPPU1sIHI1oK7V0e%2B17e1YNnirwGiKU2kPAy2t5CKnObK55Zt2MgJVkU1T78SRDYiBmdN%2F3hgHmIiMzm97kLXA14uxCFTAza81Bq4mYfcQWczGLPBw4MZy--EL%2BDk9%2BA3OcdLM9K--lGw5LN6MubhPB4VQbL3Chw%3D%3D',
        'if-none-match':'W/"452823babcd8b7073074c66793e09fa8"',
        'referer':'https://github.com/labuladong',
        'sec-ch-ua':'" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'sec-fetch-dest':'document',
        'sec-fetch-mode':'navigate',
        'sec-fetch-site':'same-origin',
        'sec-fetch-user':'?1',
        'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    }
    try:
        proxies = { "http": None, "https": None}
        request = requests.get(url,headers,verify=False,proxies=proxies)
        
        html = request.text
        soup = BeautifulSoup(html, 'lxml')
        content = soup.select("#issue-%d > div > div.edit-comment-hide > task-lists > table > tbody > tr:nth-child(1) > td > p:nth-child(1) > a"%data_id)
        return content[0].text, content[0].attrs['href']
        
    except:
        print("Failed to get text and link !!!")
        return False

# 获取每一个issue的data-id，data-id在使用选择器筛选信息时需要使用到
def get_id_list():
    headers = {
        ':authority': 'github.com',
        ':method': 'GET',
        ':path': '/labuladong/challenge/issues',
        ':scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': '_octo=GH1.1.740944638.1628754231; _device_id=5f57192446afa215a977844d244be53f; tz=Asia%2FShanghai; tz=Asia%2FShanghai; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; user_session=Zij1dWQXpFTr_0a9RT0Wd5bOhctB0MPTu53pjhqg6aNPnfAu; __Host-user_session_same_site=Zij1dWQXpFTr_0a9RT0Wd5bOhctB0MPTu53pjhqg6aNPnfAu; logged_in=yes; dotcom_user=Tom-DaLin; has_recent_activity=1; _gh_sess=KtV7HbYJDlcbmcuqhRH97no4VQ8AYk%2F1mf5P1p3j7enBC2nrji5OMvjkFI1azQSNMbaEGLEkeEZAbrAleZ6za6gN4hQKdXf9pXlNQVxG50XsfIebLEqo9jbJPyLKfz3YHoCTdDYFiPkDzqgm3MHcCh9Ys3m%2FxPJINzbV85H1iSKZHxAr8w3%2Be5c0VTABHHTvba7WqxRDWbvzjyDVhDAIgkwAmpxhl8bd9VMFaYPTdmtgWJ%2BttobThk9lfPKwCVf9orGIjtshbpmM5CZkssRmdMd4v3ohxAF7UCbNGFs7e%2BHvBUJLh2qKTAPZ%2BmC8VXaBWgik2gdT2AqAWFaXEwPmhO95zG1WMAXvGebEjMmsNtgAVbCZVfZAKlmhylYoXbvZVFaIqXz%2Bwi2J9%2B%2FOOyDbjHtIqPfTqqQXd0sqevEgNuA5QQpq3xApcBXd%2BNPRze3Z4SvQB%2BAYjerMqp%2BM%2FLLO5uSDHNJIy55BjKIw1o6djoTPPYFnauDgqNc2fWf64OMOrw3ZC0pX%2BavISE2Au1Cr%2BKvORXA9zzZw7hpZrI2fJaamt%2BJvd0q67yTS8uf7I%2F7hA1QxsyPCxXlZGnz3ioCSdXofl3geQ%2FVItoP%2FhZRTCvQaq8TURwcPcSx63C8Z7F8rgFuaSk%2FspsHoGgo2UbiOsL%2Bx45tAPVlOUHpsm9D8NAVlQIvKS0yxF2jTPIasL8gi6m7aEffuvmzvBRZga5%2FqOens6dEWKtJJBnLgomeF5fVn0rg9ljy%2F%2BqLGOM%2Fitc6SCCrjKkhELHXg0kow--dhT8%2FWGHzTwKDb2T--xbX%2BeX%2BS5ptPPdShkOQgUA%3D%3D',
        'if-none-match': 'W/"f2b45a3570d32256bcd64fc3ee226d0a"',
        'referer': 'https://github.com/labuladong',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        }
    try:
        proxies = { "http": 'http://127.0.0.1:4780', "https": 'https://127.0.0.1:4780'}
        proxies = {"http":None, "https":None}
        url = "https://github.com/labuladong/challenge/issues"
        response = requests.get(url,headers,verify=False,proxies=proxies)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        # 提取出data-id，并存放在列表中
        id_list = []
        for issue_id in range(25,46):
            content = soup.select("#issue_%d"%issue_id)
            id_list.append(content[0].attrs['data-id'])
            
        return id_list
    except:
        print("Failed to get data-id !!!")
        
# 获取全部的文章标题和链接，处理后保存当文件中
def get_info():
    id_list = get_id_list()
    issue_id = 25
    for issue_id in range(25,46):
        data_id = id_list[issue_id-25]
        url = "https://github.com/labuladong/challenge/issues/%d"%issue_id
        text, link = extract(url,data_id)
        print(text, link)
        
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
    #get_info()             # 方式一
    get_info_by_selenium()  # 方式二
    
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

