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
            'cookie':'_zap=787a4cc3-5307-4e01-ba1f-70e51eff25ce; d_c0="AFARRgNOCxKPTs8Lr5vtuz4-ghqxFDqRB7U=|1602776293"; __utmv=51854390.100-1|2=registration_date=20180924=1^3=entry_date=20180924=1; _xsrf=of8PFFx3WpgIXx9MM1nj9nmvS6wRJYV1; __snaker__id=OKZWwbMvZhPTMdYK; _9755xjdesxxd_=32; YD00517437729195%3AWM_TID=NBzML%2BWSfAtBFFBVAVcrfwN37rMrfYPA; gdxidpyhxdE=DOtPJ9oQM732hHw2%2FNPhoSswqjloNnZBK%5CAqoLnf4XrXCRrT1bBn%5CH%2FSQ%2BMVdMg6kRYcuq%5CN%2BWzOqzBw4xo0gadV7GRjhQuiVH6aoTQudHD0EUdZb5jUe81Jlx8UOxICNEqY29nf5Kj%5CgAB5UsZCGRfqnz%2F1Hy3tWOf%2FBI7%5CdsupL0NL%3A1611113079288; YD00517437729195%3AWM_NI=MKZVhCkP9M%2F4Ml1GS4zubxIB%2FjHZX%2F%2BtoQIuwQPtDlF6M4rjV0JuaUDD88DbV8vcWm5Cj%2Fol2ZpvbSN9lTaI0H3gT6XBfxldlOl%2BwEXMBbzZTL5bNHiFoH7zMfb%2BvU5ReDU%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eedac63fb5ab97a7dc59a7b08aa7d15b839e9a85b66ff3bfa295d650aee9a6bad62af0fea7c3b92a8f9596b7eb49a990f7aeae408fb4ffa8d240baabae99cc4aedb688bbdb25e9aca1b2cc7fb58fa095c76886ea83d5f16296f08696e45f889cf8d9c76a96e8ba84d667f79da6d0ee68f286c097e1598ee7a4b5e443f498fd88d73e9c9eaa99ef70b091a4ccf64f9c938e83f9529894fb83cd44ab9aa1a9b6728fbaaeccf55ff78eaba5d837e2a3; z_c0="2|1:0|10:1611112264|4:z_c0|92:Mi4xOUNWaERBQUFBQUFBVUJGR0EwNExFaVlBQUFCZ0FsVk5TTzMwWUFDcU83MHFGMlZWeDc4T0ZfVFJKeGNvam5fQkNB|6949db527f5a96387b04152afff1fea51af8ddd1438de96ecf5e44302263b7a0"; __utmc=51854390; tshl=; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1619169247,1619329696,1619329713,1619489516; SESSIONID=rc8T4H5BVM29cgjPXA64aSjaYUp4RWYKbqH6aTlbVJJ; JOID=UFsdCkzalSeMy99fdtHBO6jAmlBuqf0e1vqWYTWJ2R60pr00LY_Uo-fP1VV5AWojscBXF9Zu-uRyG3k5AriNRsI=; osd=W1AWBk_RniyAyNRUfd3CMKPLllNlovYS1fGdajmK0hW_qr4_JoTYoOzE3ll6CmEovcNcHN1i-e95EHU6CbOGSsE=; q_c1=69494c9115bf44898de96e93ac95a38b|1619741823000|1602778089000; __utma=51854390.1560770201.1604719254.1619014447.1619745325.10; __utmz=51854390.1619745325.10.10.utmcsr=link.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/; tst=h; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1619747775; KLBRSID=031b5396d5ab406499e2ac6fe1bb1a43|1619747774|1619739133',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.3',
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
