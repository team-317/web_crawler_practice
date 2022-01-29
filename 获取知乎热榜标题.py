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
        'cookie':'q_c1=2e59e7954ea94fe5924ea20acd9b6906|1602777000000|1602777000000; _zap=787a4cc3-5307-4e01-ba1f-70e51eff25ce; d_c0="AFARRgNOCxKPTs8Lr5vtuz4-ghqxFDqRB7U=|1602776293"; __utmv=51854390.100-1|2=registration_date=20180924=1^3=entry_date=20180924=1; _xsrf=of8PFFx3WpgIXx9MM1nj9nmvS6wRJYV1; __snaker__id=OKZWwbMvZhPTMdYK; _9755xjdesxxd_=32; YD00517437729195%3AWM_TID=NBzML%2BWSfAtBFFBVAVcrfwN37rMrfYPA; gdxidpyhxdE=DOtPJ9oQM732hHw2%2FNPhoSswqjloNnZBK%5CAqoLnf4XrXCRrT1bBn%5CH%2FSQ%2BMVdMg6kRYcuq%5CN%2BWzOqzBw4xo0gadV7GRjhQuiVH6aoTQudHD0EUdZb5jUe81Jlx8UOxICNEqY29nf5Kj%5CgAB5UsZCGRfqnz%2F1Hy3tWOf%2FBI7%5CdsupL0NL%3A1611113079288; YD00517437729195%3AWM_NI=MKZVhCkP9M%2F4Ml1GS4zubxIB%2FjHZX%2F%2BtoQIuwQPtDlF6M4rjV0JuaUDD88DbV8vcWm5Cj%2Fol2ZpvbSN9lTaI0H3gT6XBfxldlOl%2BwEXMBbzZTL5bNHiFoH7zMfb%2BvU5ReDU%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eedac63fb5ab97a7dc59a7b08aa7d15b839e9a85b66ff3bfa295d650aee9a6bad62af0fea7c3b92a8f9596b7eb49a990f7aeae408fb4ffa8d240baabae99cc4aedb688bbdb25e9aca1b2cc7fb58fa095c76886ea83d5f16296f08696e45f889cf8d9c76a96e8ba84d667f79da6d0ee68f286c097e1598ee7a4b5e443f498fd88d73e9c9eaa99ef70b091a4ccf64f9c938e83f9529894fb83cd44ab9aa1a9b6728fbaaeccf55ff78eaba5d837e2a3; z_c0="2|',
        'referer':'http',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile':'?0',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-origin',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',

    }
    test(headers)