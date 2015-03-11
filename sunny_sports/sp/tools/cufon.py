#!/usr/bin/python
#-*-coding:utf-8-*-
import urllib
import urllib2
import django
import os
from bs4 import BeautifulSoup

def get_all_letters():
    names = Coach.objects.all().values_list('property__name', flat='True')
    letters = set()
    for n in names:
        for i in n:
            letters.add(i)
    return "".join(letters)

def get_js(letters):
    """
    Get cufun js from website
    letters: a string of all letters
    """
    data = {'letter' : "0123456789"+letters.encode('utf-8')}
    f = urllib2.urlopen(
        #url = 'http://www.cufon-font.com/font.php?mod=render&fid=5', #楷体
        url = 'http://www.cufon-font.com/font.php?mod=render&fid=11', #华文行楷
        data = urllib.urlencode(data)
    )
    soup=BeautifulSoup(f.read())
    return soup.find(id="jscode").text.replace('&quot;','"')
    #print soup.find(id="showarea")
    
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sunny_sports.settings")
    django.setup()

    import datetime
    from sunny_sports.sp.models import *
    from sunny_sports.sp.models.models import *

    js = get_js(get_all_letters())
    print js
    with open('../../static/js/cufon/Kaiti.font.js') as f:
        f.write(js)

