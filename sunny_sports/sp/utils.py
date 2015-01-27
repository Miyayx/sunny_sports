#!/usr/bin/env/python
#-*-coding:utf-8-*-

import requests
import json
import random

from sunny_sports.sp.models.models import *

def gen_vcode():
    return random.randint(1000,9999)

def send_vcode(mobile):
    vcode = gen_vcode()
    #resp = requests.post(
    #        ("https://sms-api.luosimao.com/v1/send.json"),
    #        auth=("api", "b0e0056374704a22f46f9166df13868e"),
    #        data={
    #            "mobile": mobile,
    #            "message": "验证码：%d。验证码有效时间为15分钟，请勿将此验证码发给任何号码及其他人【快乐体操】"%vcode
    #            },
    #        timeout=3, 
    #        verify=False)

    #result = json.loads(resp.content)
    result = {u'msg': u'ok', u'error': 0}

    return result,vcode


def custom_msg_publish(user_list, title, content):
    msg = Message.objects.create(title=title, cont=content)
    msg.save()

    insert_list = []
    for u in user_list:
        insert_list.append(UserMessage(user=u, msg=msg))
    UserMessage.objects.bulk_create(insert_list)
