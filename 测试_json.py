# -*- coding: utf-8 -*-
"""
Created on Sat May  1 08:29:46 2021
json文件的写入和读取
@author: Team317
"""

import json
# 一个json的字符串，注意里面的字段要用双引号而非单引号括起来
str = '''
[{
  "name":"Bob",
  "gender":"male",
  "birthday":"1992-10-18"
},{
   "name":"Selina",
   "gender":"female",
   "birthday":"1995-10-18"
},{
   "name":"张伟",
   "gender":"男",
   "birthday":"1999-12-30"
}]
'''

data = json.loads(str)  # 转为json类型的数据
name = data[0]['name']         # 获取第一个用户的名字

# 尝试获取第一个用户的age，当不存在这个字段时返回参数-1
# 如果使用 age = data[0]['age'], 则会直接报错
age = data[0].get('age',-1)   

# json文件的写操作
with open('data.txt','w') as file:
    # 将json格式的数据写入文件中，参数indent表示缩进字符数
    # json.dumps将data转为json字符
    file.write(json.dumps(data, indent = 2))
    
    
# 如果数据中存在中文，则需要指定编码方式
with open('data.txt', 'w', encoding='utf-8') as file:
    # 将ensure_ascii置为False
    file.write(json.dumps(data, indent=2, ensure_ascii = False))
    
    
# json文件的读操作，注意打开文件时要指定编码方式为utf-8
with open('data.txt','r', encoding='utf-8') as file:
    # 以字符的形式读取数据
    str = file.read()
    # 再将字符格式转为json格式
    data = json.loads(str)
    print(data)
    