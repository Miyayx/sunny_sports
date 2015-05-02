#!/usr/bin/python
#-*- coding:utf-8 -*-
from django.db import models

import datetime

from sp.models.models import MyUser

def generate_order_num(_id):
    """
    Generate order number
    Format:year(4)month(2)day(2)hour(2)minute(2)coachtrainid
    """
    now = datetime.datetime.now()
    return "{0:0>4d}{1:0>2d}{2:0>2d}{3:0>2d}{4:0>2d}{5:0>2d}{6}".format(now.year, now.month, now.day, now.hour, now.minute, now.second, _id)

BILL_TYPE = (
        (0, u'快乐体操教练培训费用'),
        (1, u'快乐体操比赛报名费用'),
        )
PAY_TYPE = (
        (0, 'alipay_direct_pay'),
        (1, 'alipay_bank'),
        )

# Create your models here.
class Bill (models.Model):
    no = models.CharField(max_length=36,primary_key=True)
    user = models.ForeignKey(MyUser)
    bill_type = models.IntegerField(choices=BILL_TYPE, default=0)#账单类型
    pay_type = models.IntegerField(choices=PAY_TYPE, default=0)#支付类型

  # It'll be one of the 4 status ('WAIT_BUYER_PAY', 'WAIT_SELLER_SEND_GOODS',
  # 'WAIT_BUYER_CONFIRM_GOODS', 'TRADE_FINISHED', 'TRADE_CLOSED'), the inital
  # status will be 'INIT'.
    trade_status = models.CharField(max_length=50, default='INIT')
    total_fee = models.FloatField(default=0.0)
    start_date = models.DateTimeField(default=datetime.datetime.now())
    body = models.CharField(max_length=1000, null=True)
    
    class Meta:
        app_label='payment'

