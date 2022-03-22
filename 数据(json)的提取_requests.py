# -*- coding: utf-8 -*-
"""
Created on Sat May  1 09:35:20 2021

@author: Team317
"""

import time
import requests
import json
from bs4 import BeautifulSoup

base_url = 'https://www.zhihu.com/api/v3/feed/topstory/recommend?'
headers = {
    'cookie':'_zap=787a4cc3-5307-4***',
    'user-agent':'Mozilla/5.0 (Windows***',
}
# page和after_id可根据需要进行调整
page = 0
after_id = 6
params = {
    'session_token':'7ff1929781f57d1262b18480fe3011c2',
    'desktop':'true',
    'page_number':page,
    'limit':'6',
    'action':'down',
    'after_id':after_id,
    'ad_interval':'1'
}

def get_page(params, base_url, headers):

    # 附加参数
    extra_url = '&'.join(['{key}={val}'.format(key=key,val=params[key]) for key in params])
    # 合成url
    url = base_url + extra_url
    # 尝试获取json数据
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error',e.args)
        return []
        
# 获取json数据
data = get_page(params, base_url, headers)

with open('recommend.json', 'w', encoding='utf-8') as file:
    str = json.dumps(data, indent = 2, ensure_ascii = False)
    file.write(str)

with open('recommend.json', 'r', encoding='utf-8') as file:
    str = file.read()
    data = json.loads(str)['data']
    num = len(data)
    # 接下来就是提取其中的信息，这需要观察json数据的格式，了解你所需要的数据的位置，然后一步步定位
    # 由于json中没有找到每条推荐对应的链接，所以需要自己根据json数据自己合成链接
    # 链接形如：https://www.zhihu.com/question/377886499/answer/1849697584
    for i in range(num):
        # 获取target字段，里面包含主要的链接信息
        target = data[i].get('target')
        id = target.get('id')
        # 尝试获取question字段，如果失败则该条推荐不是文章类型
        question = target.get('question', -1)
        if question != -1:
            question_id = question.get('id')
            # 合成推荐内容的链接
            url = 'https://www.zhihu.com/question/{q_id}/answer/{id}'.format(q_id = question_id, id = id)
            
            title = question.get('title')
            print('{title}\n{url}\n'.format(title=title, url=url))
            



