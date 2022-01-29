from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 打开一个空白的浏览器
browser = webdriver.Chrome()
try:
    # 访问百度页面
    browser.get('https://www.baidu.com')
    # 找到输入框
    input = browser.find_element_by_id('kw')
    # 输入关键字Python
    input.send_keys('Python')
    # 回车
    input.send_keys(Keys.ENTER)
    # 等待结果
    wait = WebDriverWait(browser,100)
    wait.until(EC.presence_of_element_located((By.ID, 'content_left')))

    print(browser.current_url)
    # print(browser.page_source)

# except:
#     print("finish")

finally:
    browser.close()
