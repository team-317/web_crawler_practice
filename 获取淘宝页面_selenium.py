# -*- coding: utf-8 -*-
"""
Created on Sun May  2 15:12:44 2021

@author: Team317
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
import json
import time
from pyquery import PyQuery as pq
import sys
from random import randint,random

def get_cookie():
    #手动获取cookies
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 10)
    # 先访问登录页面
    login_url = 'https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fs.taobao.com%2Fsearch%3Fq%3DiPad&uuid=6b5f203675de0dfb1d09899a2572b80b'
    browser.get(login_url)
    # 得到登录页面的cookie
    cookies = browser.get_cookies()
    
    # 访问搜索页面
    KEYWORD = 'iPad'
    url = 'https://s.taobao.com/search?q={keyword}'.format(keyword = KEYWORD)
    # 手动登录成功后输入Y继续
    ok = input("Are you ok?[Y/N]")
    # 输入N时退出程序
    if ok != 'Y':
        browser.close()
        sys.exit()
        
    browser.get(url)
    # 获取搜索页面的cookie
    cookie = browser.get_cookies()
    for cook in cookie:
        cookies.append(cook)
        
    # 保存cookies信息
    with open("taobao_cookies.txt","w") as file:
        file.write(json.dumps(cookies))
        
    # # 关闭浏览器
    # browser.close()
    
    return browser, wait
    
def load_cookie():
    browser = webdriver.Edge()
    # 每次跳转请求页面的等待时间为20秒，超出20秒时产生超时异常
    wait = WebDriverWait(browser, 10)
    # 读取cookies
    with open("taobao_cookies.txt") as file:
        cookies = json.loads(file.read())
        
    # 首先访问登录页面
    login_url = 'https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fs.taobao.com%2Fsearch%3Fq%3DiPad&uuid=6b5f203675de0dfb1d09899a2572b80b'
    browser.get(login_url)
    
    # 然后加载cookies
    for cook in cookies:
        try:
            browser.add_cookie(cook)
        except:
            # 打印被舍弃的cookie
            print(cook)
            print("*********************")
    return browser, wait
    
# 访问第index个页面
def index_page(browser, wait, page, keyword):
    
    print("正在爬取第{page}页".format(page = page))
    try:
        # 访问搜索页面
        url = 'https://s.taobao.com/search?q={keyword}'.format(keyword = keyword)
        time.sleep(random()*10 + 2)
        browser.get(url)
        if page > 1:
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input')))
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
            time.sleep(random()*10 + 2)
            input.clear()
            time.sleep(random()*10 + 2)
            input.send_keys(page)
            time.sleep(random()*10 + 2)
            submit.click()
        time.sleep(random()*10 + 2)
        # 等待页面被加载出来
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page)))
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist > div > div > div')))
        time.sleep(random()*10 + 4)
        # 获取页面信息
        get_products(browser)
        print("第{page}页抓取完成".format(page=page))
    except TimeoutException:
        # 出现超时时不再继续，结束程序
        print('超时')
        browser.close()
        sys.exit()

def get_products(browser):
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist > div > div > div:nth-child(1) > div').items()
    
    with open("products_info.txt", 'a+') as file:
        for item in items:
            product = {
                'image':item.find('.pic .img').attr('data-src'),
                'price':item.find('price').text(),
                'deal':item.find('.deal-cnt').text(),
                'title':item.find('.title').text(),
                'shop':item.find('.shop').text(),
                'location':item.find('.location').text()
            }
            # print(product)
            # print("************")
            info = json.dumps(product) + '\n'
            file.write(info)
    
        

if __name__ == '__main__':
    # 首次登录标志
    is_first = True
    if is_first == True:
        # 首次登录时，手动扫码淘宝，获取cookies
        browser,wait = get_cookie()
    else:
        # 如果之前登录过，则从文件中加载cookies
        browser,wait = load_cookie()
    
    # 之后自动化的抓取页面信息
    for i in range(1,10):
        index_page(browser, wait, i, 'iPad')
        
        # 等待几秒再访问，以防被察觉
        time.sleep(random()*10 + 10)
    
    browser.close()
    

