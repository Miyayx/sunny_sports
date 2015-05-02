#!/usr/bin/env python
#-*-coding:utf-8-*-

from django.db import models

import datetime

from role import *
from game import *
from train import *
from status import *

from payment.models import Bill

def make_ct_num():
    import random
    return random.randint(0,100)

class CoachTrainManager(models.Manager):
    def create_ct(self, coach, train):
        ct = self.create(coach=coach, train=train)
        ct.save()
        train.cur_num = train.cur_num + 1
        train.save()
        return ct


class CoachTrain(models.Model):
    number = models.IntegerField(default=0)
    coach = models.ForeignKey(Coach)
    train = models.ForeignKey(Train)
    score = models.IntegerField(default=0) 
    status = models.IntegerField(default=0,choices=ROLE_TRAIN_STATUS)
    pass_status = models.IntegerField(default=0,choices=ROLE_TRAIN_PASS_STATUS) #是否通过
    certificate = models.CharField(max_length=100, null=True) #证书编号
    reg_time = models.DateTimeField(default=datetime.datetime.now) #报名时间
    get_time = models.DateTimeField(null=True) #通过时间
    bill = models.OneToOneField(Bill, null=True)
    
    objects = CoachTrainManager()

    class Meta:
        app_label='sp'

    def __str__(self):
        return "coach:%s,  train:%s"%(self.coach, self.train)

    #def save(self, *args, **kwargs):
    #    #if self.number == 0: #生成学号
    #    #    self.number = CoachTrain.objects.filter(train=self.train).count()

    #    super(CoachTrain, self).save(*args, **kwargs)

    def check_pass(self, num):
        """
        num:当前此级别的证书数量
        """
        self.certificate = "{0}{1:0>6d}".format(self.train.level, num)
        self.get_time=datetime.datetime.now()
        self.pass_status=1
        self.save()

    def delete(self, *args, **kwargs):
        print "delete"
        self.train.cur_num = self.train.cur_num - 1
        self.train.save()
        super(CoachTrain, self).delete(*args, **kwargs)

