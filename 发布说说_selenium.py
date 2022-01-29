# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:06:56 2021

@author: Team317
"""
"""
需下载msedgedriver并加入环境变量中，还需下载（可能需要更新）selenium
"""


from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
import time
from random import randint,random
import datetime
import json

def get_cookie():
    
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 5)
    
    # 先访问登录页面手动登录
    login_url = 'https://i.qq.com/'
    browser.get(login_url)
    cookies = browser.get_cookies()
    input("Are you OK?")
    # url = 'https://user.qzone.qq.com/2629757717'
    # browser.get(url)
    
    # cookie = browser.get_cookies()
    # for cook in cookie:
    #     cookies.append(cook)
        
    # 保存cookies信息
    with open("qq_cookies.txt","w") as file:
        file.write(json.dumps(cookies))
    # input("Are you OK?")
    
    return browser, wait

def load_cookie():
    browser = webdriver.Chrome()
    # 每次跳转请求页面的等待时间为20秒，超出20秒时产生超时异常
    wait = WebDriverWait(browser, 10)
    # 读取cookies
    with open("qq_cookies.txt") as file:
        cookies = json.loads(file.read())
        
    # 首先访问登录页面
    login_url = 'https://i.qq.com/'
    browser.get(login_url)
    
    # 然后加载cookies
    count = 0
    for cook in cookies:
        try:
            count += 1
            print("********{count}*********".format(count=count))
            browser.add_cookie(cook)
        except:
            # 打印被舍弃的cookie
            # print(cook)
            # print("*********************")
            pass
    url = 'https://user.qzone.qq.com/2629757717'
    browser.get(url)
    time.sleep(5)
    
    return browser, wait
    
# 发说说
def send_message(browser, wait, times):
    url = 'https://user.qzone.qq.com/2629757717'
    # browser.get(url)
    try:
        # time.sleep(5)
        # 找到输入框并聚焦
        box_selector = '#\$1_content_content'
        text_box = browser.find_element_by_css_selector(box_selector)
        text_box.clear()
        text_box.click()
        
        
        # 将文本输入到输入框
        words = get_words(times)
        # time.sleep(5)
        browser.find_element_by_id("$1_content_content").send_keys(words) 
        
        # time.sleep(5)
        
        # input("可见权限")
        
        # 获取提交按钮
        selector = '#QM_Mood_Poster_Inner > div > div.qz-poster-ft > div.op > a.btn-post.gb_bt.evt_click > span'
        submit = browser.find_element_by_css_selector(selector)
        send = input("send it?[Y/N]")
        if send == 'Y':
            submit.click()
            
        # time.sleep(5)
        # 等待页面被加载出来
        
        print("成功发送：",words)
        # browser.close()
    except:
        # 出现超时时不再继续，结束程序
        print('超时重传')
        # time.sleep(10)
        # send_message(browser, wait, times)
        # browser.close()

def get_words(index):
    with open('说说内容.txt', 'r', encoding = 'utf-8') as file:
        words = file.readlines()
        
    return words[index]
    
def cur_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

if __name__ == '__main__':
    # 首次登录标志
    browser, wait = get_cookie()
    
    # 之后自动化的抓取页面信息
    for i in range(0,20):
        if cur_time()[-1:] == '9' or cur_time()[-1:] == '0' or True:
            # browser,wait = load_cookie()
            send_message(browser, wait, i)
    
    browser.close()
    

