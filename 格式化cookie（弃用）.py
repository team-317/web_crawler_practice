# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 21:13:34 2021

@author: Team317
"""

# 待处理的header
header = []
with open('header.txt','r+') as file:
    lines = file.readlines()
    for line in lines:
        for i in range(len(line)):
            if line[i] == ':':
                line_t = "'" + line[0:i] +"':'" + line[i+2:-1] +"',\n"
                break
        header.append(line_t)
    # print(header)
    file.writelines(header)
