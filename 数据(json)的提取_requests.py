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
    'cookie':'_zap=787a4cc3-5307-4e01-ba1f-70e51eff25ce; d_c0="AFARRgNOCxKPTs8Lr5vtuz4-ghqxFDqRB7U=|1602776293"; __utmv=51854390.100-1|2=registration_date=20180924=1^3=entry_date=20180924=1; _xsrf=of8PFFx3WpgIXx9MM1nj9nmvS6wRJYV1; __snaker__id=OKZWwbMvZhPTMdYK; _9755xjdesxxd_=32; YD00517437729195%3AWM_TID=NBzML%2BWSfAtBFFBVAVcrfwN37rMrfYPA; gdxidpyhxdE=DOtPJ9oQM732hHw2%2FNPhoSswqjloNnZBK%5CAqoLnf4XrXCRrT1bBn%5CH%2FSQ%2BMVdMg6kRYcuq%5CN%2BWzOqzBw4xo0gadV7GRjhQuiVH6aoTQudHD0EUdZb5jUe81Jlx8UOxICNEqY29nf5Kj%5CgAB5UsZCGRfqnz%2F1Hy3tWOf%2FBI7%5CdsupL0NL%3A1611113079288; YD00517437729195%3AWM_NI=MKZVhCkP9M%2F4Ml1GS4zubxIB%2FjHZX%2F%2BtoQIuwQPtDlF6M4rjV0JuaUDD88DbV8vcWm5Cj%2Fol2ZpvbSN9lTaI0H3gT6XBfxldlOl%2BwEXMBbzZTL5bNHiFoH7zMfb%2BvU5ReDU%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eedac63fb5ab97a7dc59a7b08aa7d15b839e9a85b66ff3bfa295d650aee9a6bad62af0fea7c3b92a8f9596b7eb49a990f7aeae408fb4ffa8d240baabae99cc4aedb688bbdb25e9aca1b2cc7fb58fa095c76886ea83d5f16296f08696e45f889cf8d9c76a96e8ba84d667f79da6d0ee68f286c097e1598ee7a4b5e443f498fd88d73e9c9eaa99ef70b091a4ccf64f9c938e83f9529894fb83cd44ab9aa1a9b6728fbaaeccf55ff78eaba5d837e2a3; z_c0="2|1:0|10:1611112264|4:z_c0|92:Mi4xOUNWaERBQUFBQUFBVUJGR0EwNExFaVlBQUFCZ0FsVk5TTzMwWUFDcU83MHFGMlZWeDc4T0ZfVFJKeGNvam5fQkNB|6949db527f5a96387b04152afff1fea51af8ddd1438de96ecf5e44302263b7a0"; __utmc=51854390; tshl=; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1619169247,1619329696,1619329713,1619489516; SESSIONID=rc8T4H5BVM29cgjPXA64aSjaYUp4RWYKbqH6aTlbVJJ; JOID=UFsdCkzalSeMy99fdtHBO6jAmlBuqf0e1vqWYTWJ2R60pr00LY_Uo-fP1VV5AWojscBXF9Zu-uRyG3k5AriNRsI=; osd=W1AWBk_RniyAyNRUfd3CMKPLllNlovYS1fGdajmK0hW_qr4_JoTYoOzE3ll6CmEovcNcHN1i-e95EHU6CbOGSsE=; q_c1=69494c9115bf44898de96e93ac95a38b|1619741823000|1602778089000; __utma=51854390.1560770201.1604719254.1619014447.1619745325.10; __utmz=51854390.1619745325.10.10.utmcsr=link.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/; tst=h; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1619747775; KLBRSID=031b5396d5ab406499e2ac6fe1bb1a43|1619747774|1619739133',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.3',
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
            



