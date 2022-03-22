# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 21:36:59 2021

@author: Team317

定时的爬取知乎热榜前十的标题，如果当前爬取的热榜较上一次有所变动，则将新增的标题打印出来。
https://blog.csdn.net/GodNotAMen/article/details/116304955

"""


import time
import requests
from bs4 import BeautifulSoup

'''
这里采用类来管理，但下次写代码时完全可以将里面需要用到的代码拆分出来，
不要觉得放到一个类里面，这些代码就是一个整体了。
'''

class Hot_list():
    def __init__(self):
        self.url = 'https://www.zhihu.com/hot'
        # 设置headers，复制headers的时候注意不要搞错了
        self.headers = {
            'cookie':'_zap=787a4cc3-5307-4***',
            'user-agent':'Mozilla/5.0 (Windows***',
        }
        self.hot_list_new = []
        self.hot_list_old = []
        
    # python的接口很方便，这么几行就能完成热榜标题的提取
    def getHot(self):
        try:
            # 简单直接的方法
            res = requests.get(self.url,headers=self.headers)
            html = res.text
            
            # 处理网页内容，提取热榜标题
            soup = BeautifulSoup(html, 'lxml')
            hot_list = soup.select('#TopstoryContent > div > div > div.HotList-list > section > div.HotItem-content > a')
            hot_list = [hot['title'] + "\n" + hot['href'] +'\n' for hot in hot_list]
            return hot_list[0:10]
        
        except:
            return []
    
    # 检查网络并获取热榜，根据参数将热榜赋给hot_list_old或hot_list_new
    def checkHot(self, mark):
        flag = 0
        hot_list = self.getHot()
        while hot_list == []:
            hot_list = self.getHot()
            if flag == 0:
                print("[",cur_time(),"]:当前网络不可用，正在尝试连接网络\n")
            flag = 1
            time.sleep(20)
        if flag == 1:
                print("[",cur_time(),"]:网络连接已恢复\n")
        if mark == 1:
            self.hot_list_new = hot_list
        elif mark == 0:
            self.hot_list_old = hot_list
            
    
    # 检查，每隔一段时间检查一次热榜，将新增的标题打印出来
    def checkUpdate(self):
        # 每10分钟检查一次更新
        print("\n*********************知乎热榜*********************\n")
        
        self.checkHot(0)

        print("当前热榜前十\t [time:" + cur_time() +']\n')
        for hot in self.hot_list_old:
            print(hot)
        print("\n\n********************每五分钟刷新一次********************\n")
        while(1):
            time.sleep(20)

            self.checkHot(1)
                
            # 对比两次热榜是否相同，将新榜中新增的标题提取出来
            for hot_new in self.hot_list_new:
                flag = 0    # 更新标记
                for hot_old in self.hot_list_old:
                    if hot_new == hot_old:
                        flag = 1
                if flag == 0:
                    print(cur_time(),"\t",hot_new)
                    
            self.hot_list_old = self.hot_list_new
        
# 获取当前时间
def cur_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 


if __name__ == '__main__':
    Hot = Hot_list()
    Hot.checkUpdate()
