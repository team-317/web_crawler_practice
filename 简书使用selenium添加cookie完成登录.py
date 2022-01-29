# -*- coding: utf-8 -*-
"""
Created on Sun May  2 17:00:03 2021

@author: Team317

通过selenium使用账号和密码登入简书，并保存本次会话的cookie，
再次登录时使用第一次保存的cookie来完成登录（也是使用selenium，但不用输入账户和密码了）
"""

import requests
import time
import json
from selenium import webdriver

def tr():
    #手动获取cookies
    driver = webdriver.Chrome()
    url = 'https://www.jianshu.com/sign_in'
    driver.get(url)
    time.sleep(2)
    driver.find_element_by_id("session_email_or_mobile_number").clear()
    driver.find_element_by_id("session_password").clear()
    #输入简书登录账号
    driver.find_element_by_id("session_email_or_mobile_number").send_keys("18379988116")
    #输入简书登录密码
    driver.find_element_by_id("session_password").send_keys("mao12914")
    #点击登录按钮
    driver.find_element_by_id("sign-in-form-submit-btn").click()
    #这里设置停留15秒钟，有足够的时间让我们手动去点击图片验证
    time.sleep(5)
    #获取cookie
    cookies = driver.get_cookies()
    #cookie保存到cookies.txt文件
    f1 = open("jianshu.txt","w")
    f1.write(json.dumps(cookies))
    f1.close()
    print(cookies)
    print(type(cookies))


def test():
    import requests
    import time
    import json
    from selenium import webdriver
    
    driver = webdriver.Chrome()
    url = 'https://www.jianshu.com/sign_in'
    driver.get(url)
    time.sleep(2)
    
    #从cookies.txt文件读取cookies
    f2 = open("jianshu.txt")
    cookies = json.loads(f2.read())
    #使用cookies登录
    for cook in cookies:
        driver.add_cookie(cook)
        print(cook)
        print("***********************")
    #刷新页面
    driver.refresh()
    time.sleep(2)
    driver.quit()

if __name__ == '__main__':
    tr()
    test()