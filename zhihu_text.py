# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 18:44:05 2021

@author: Team317
"""

import requests
import re
from lxml import etree

content_re = re.compile('"excerptArea":{"text":"(.*?)"}')
url_re = re.compile('"link":{"url":"(.*?)"')

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59"}

def get_hot(url):
    html = requests.get(url,headers=headers)
    soup = etree.HTML(html.text)
    hots = soup.xpath('//a[@class="HotList-item"]')
    for h in hots:
        title = "标题："+h.xpath('div/div[@class="HotList-itemTitle"]/text()')[0]+'\n'
        with open("./知乎热榜.txt",'at') as f:
            f.write(title)
    images = soup.xpath('//div[@class="HotList-itemImgContainer"]/img/@src')
    for i in images:
        with open("./知乎图片链接.txt", 'at') as f:
            f.write(i+'\n')
    urls = url_re.findall(html.text)
    for url in urls:
        url = url+'\n'
        with open("./知乎热榜.txt",'at') as f:
            f.write(url)
    contents = content_re.findall(html.text)
    for c in contents:
        with open("./知乎热榜.txt",'at') as f:
            f.write('#'+c+'\n')

if __name__ == '__main__':
    url = "https://www.zhihu.com/billboard"
    get_hot(url)
