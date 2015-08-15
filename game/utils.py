#!/usr/bin/env/python
#-*-coding:utf-8-*-

def wrap_schedule(s):
    #把字符串格式的schedule形式化
    return [i.split('#;;') for i in s.split('#;;;;')]
