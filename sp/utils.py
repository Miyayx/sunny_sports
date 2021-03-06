#!/usr/bin/env/python
#-*-coding:utf-8-*-

import requests
import json
import random
import datetime

from django.utils import timezone

from sp.models.models import *
from sp.models import *

from django.conf import settings

def send_phone_message(mobile, msg):
    if settings.MSG_CODE and not mobile in settings.IGNORE_PHONE:
        resp = requests.post(
                ("https://sms-api.luosimao.com/v1/send.json"),
                auth=("api", ""),
                data={
                    "mobile": mobile,
                    "message": msg
                    },
                timeout=6, 
                verify=False)
        print "send message",msg
        result = json.loads(resp.content)
    else:
        result = {u'msg': u'ok', u'error': 0}
    return result

def gen_vcode():
    return random.randint(100000,999999)

def send_vcode(mobile):
    vcode = gen_vcode()
    result = send_phone_message(mobile, "验证码：%d。验证码有效时间为15分钟，请勿将此验证码发给任何号码及其他人。【快乐体操网络平台】"%vcode)
    return result,vcode

def check_vcode(phone, vcode):
    cs = Code.objects.filter(phone = phone)
    if not len(cs):
        return False,"验证码错误"
    c = cs.latest('time')
    print "c.code:",c.code
    print "vcode",vcode
    if c.code == vcode:
        now = timezone.now()
        print now
        print c.time

        if c.time < timezone.now() and c.time + datetime.timedelta(0,900) > timezone.now(): #当前时间要在c.time与c.time+15min之间
            return True,"OK"
        else:
            return False, "超时"
    else:
        return False,"验证码错误"


def custom_msg_publish(user_list, title, content):
    msg = Message.objects.create(title=title, cont=content)
    msg.save()

    insert_list = []
    for u in user_list:
        insert_list.append(UserMessage(user=u, msg=msg))
    UserMessage.objects.bulk_create(insert_list)


def calculate_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def join_position(a):
    return u"%s省%s市%s区/县%s"%(a.property.province, a.property.city, a.property.dist, a.property.address)

def export_xls(req, name, fields, rows):
    import xlwt
    from django.http import HttpResponse
    import urllib
    import sys

    code="utf-8"
    if req.META.has_key('HTTP_USER_AGENT'):
        user_agent = req.META['HTTP_USER_AGENT'].lower()
        print user_agent
        if 'trident' in user_agent or 'msie' in user_agent: #如果是IE浏览器发来的请求
            code="gb2312"

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s.xls'%urllib.unquote(urllib.quote(name.encode(code)))
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(name.split('-')[0])
    
    row_num = 0
    
    columns = [(f,6000) for f in fields]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    
    for row in rows:
        row_num += 1
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response
