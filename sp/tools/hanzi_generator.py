#-*- coding:utf-8 -*-
import codecs

HANZI = list(codecs.open('media/hanzi-6000.dat', 'r', 'utf-8').read().strip('\n').strip())

def get_word_src(name):
    pass
    name = name.strip().replace(" ","")
    words = list(name)
    name_src = ['/media/hanzi/%d.png'%HANZI.index(w) for w in words]
    return name_src

