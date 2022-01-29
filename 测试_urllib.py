# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 20:42:16 2021

@author: Team317
"""

'''
学会urllib的简单使用，简单的访问网页并获取页面内容
'''
import socket
import urllib.request
import urllib.error

# 简单情况
# 使用read函数来获取response中的数据
# urlopen中可以设置timeout参数，当服务器响应时间超过timeout时，产生超时异常
timeout = 10
try:
    response = urllib.request.urlopen('http://httpbin.org/get', timeout = timeout)
    print(response.read())
except urllib.error.URLError as e:
    if isinstance(e.reason, socket.timeout):
        print("TIME OUT!!!")
        
# 当需要用到headers时，则需要使用Request类
# 构建Request对象，并传递给urlopen
def R2():
    request = urllib.request.Request('http://python.org')
    response = urllib.request.urlopen(request)
    print(response.read().decode('utf-8'))

#当需要使用到Cookie时，则需要使用更高级的Handler
