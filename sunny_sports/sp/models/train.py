#-*-coding:utf-8-*-

import datetime
from django.db import models

from status import *
from role import *

import random


def make_id():
    """
    Generate id for train
    Format:year(4)month(2)num(4)
    """
    #_id = Train.objects.latest('_id')._id#get latest train id
    #ym,i = _id[:6],_id[6:] #get yearmonth and id
    now = datetime.datetime.now()
    nym = str(now.year)+str(now.month) 
    #if ym == nym:
    #    i += 1 #如果是同一月份id+1
    #else:
    i = random.randint(0,10000) #否则重新编号
    return "{0}{1:0>4d}".format(nym,i)

class Train(models.Model):
    id = models.CharField(max_length=10, primary_key=True, default=make_id)
    org = models.ForeignKey(Coach_Org) #组织机构
    name = models.CharField(max_length=30) #培训名称
    demo = models.CharField(max_length=100, blank=True) #??
    address = models.CharField(max_length=100) #培训地点
    level = models.IntegerField(choices=COACH_LEVEL)#培训等级
    max = models.IntegerField() #人数上限
    money = models.IntegerField() #费用
    reg_stime = models.DateTimeField() #报名开始时间
    reg_etime = models.DateTimeField() #报名截止时间
    train_stime = models.DateTimeField() #培训开始时间
    sub_status = models.IntegerField(choices=SUB_STATUS, default=0) #成绩是否提交
    pub_status = models.IntegerField(choices=PUB_STATUS, default=0) #成绩是否发布
    
    class Meta:
        app_label='sp'
