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
    未用到
    """
    #_id = Train.objects.latest('_id')._id#get latest train id
    #ym,i = _id[:6],_id[6:] #get yearmonth and id
    now = datetime.datetime.now()
    nym = "{0:0>4d}{1:0>2d}".format(now.year, now.month)
    #if ym == nym:
    #    i += 1 #如果是同一月份id+1
    #else:
    i = random.randint(0,10000) #否则重新编号
    return "{0}{1:0>4d}".format(nym,i)

class Train(models.Model):
    id = models.CharField(max_length=20, primary_key=True, default="", unique=True)
    org = models.ForeignKey(CoachOrg) #组织机构
    name = models.CharField(max_length=30) #培训名称
    demo = models.CharField(max_length=100, blank=True) #??
    address = models.CharField(max_length=100) #培训地点
    level = models.IntegerField(choices=TRAIN_LEVEL)#培训等级
    limit = models.IntegerField() #人数上限
    cur_num = models.IntegerField(default=0) #当前报名人数
    money = models.IntegerField() #费用
    reg_stime = models.DateTimeField() #报名开始时间
    reg_etime = models.DateTimeField() #报名截止时间
    train_stime = models.DateTimeField() #培训开始时间
    train_etime = models.DateTimeField() #培训结束时间
    pass_status = models.IntegerField(choices=PASS_STATUS, default=0)#审核状态
    reg_status = models.IntegerField(choices=REG_STATUS, default=0) #报名状态
    train_status = models.IntegerField(choices=TRAIN_STATUS, default=0) #培训状态
    sub_status = models.IntegerField(choices=SUB_STATUS, default=0) #成绩是否提交
    pub_status = models.IntegerField(choices=PUB_STATUS, default=0) #成绩是否发布
    
    class Meta:
        app_label='sp'

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        """
        编号生成规则：组织机构缩写+当前年份+今年培训数量
        """
        if len(self.id) == 0:
            now = datetime.datetime.now()
            self.id = "{0}{1}{2:0>2d}".format(self.org.shortname, now.year, Train.objects.filter(org=self.org, train_stime__year=now.year).count()+1)

        super(Train, self).save(*args, **kwargs)
