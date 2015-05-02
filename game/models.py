#!/usr/bin/env python
#-*-coding:utf-8-*-

from django.db import models

# Create your models here.

from student.models import *
from sp.models.status import *
from payment.models import *

AWARD = (
        (0, '缺赛'),
        (1, '一等奖'),
        (2, '二等奖'),
        (3, '三等奖'),
        )

class Event(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=200)
    class Meta:
        app_label='sp'
    
class Contestant(models.Model):
    user = models.ForeignKey(MyUser)
    fullname = models.CharField(max_length=200)
    org_num  = models.CharField(max_length=20)
    province = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=30, blank=True)
    dist = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100,blank=True)

class Game(models.Model):
    id = models.CharField(max_length=16)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    sponsor = models.CharField(max_length=500) #主办单位 ;分隔
    organizer = models.CharField(max_length=500) #承办单位 ;分隔
    coorganizer = models.CharField(max_length=500)#协办单位 ;分隔
    schedule = models.TextField(max_length=2000) #日程安排，
    province = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=30, blank=True)
    dist = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100,blank=True)
    events = models.ManyToManyField(Event) #比赛项目
    limit = models.IntegerField(default=0) #参赛队数
    male_num = models.IntegerField(default=0) #每队男生人数
    female_num = models.IntegerField(default=0) #每队女生人数
    money = models.IntegerField(default=0) #每人参赛费用
    reg_place = models.CharField(max_length=300) #报名地点
    reg_stime = models.DateTimeField() #报名开始时间
    reg_etime = models.DateTimeField() #报名截止时间
    game_stime = models.DateTimeField() #比赛开始时间
    game_etime = models.DateTimeField() #比赛结束时间
    pass_status = models.IntegerField(choices=PASS_STATUS, default=0)#审核状态
    reg_status = models.IntegerField(choices=REG_STATUS, default=0) #报名状态
    game_status = models.IntegerField(choices=TRAIN_STATUS, default=0) #比赛状态
    sub_status = models.IntegerField(choices=SUB_STATUS, default=0) #成绩是否提交
    pub_status = models.IntegerField(choices=PUB_STATUS, default=0) #成绩是否发布
    contact_name = models.CharField(max_length=20) #联系人
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField(max_length=20)

    class Meta:
        app_label='sp'

class Team(models.Model):
    id = models.CharField(max_length=16)
    contestant = models.ForeignKey(Contestant) #所属参赛单位
    game = models.ForeignKey(Game)
    name = models.CharField(max_length=30) #队名
    leader = models.CharField(max_length=20)# 领队
    contact_name = models.CharField(max_length=20) #联系人
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField(max_length=20)
    contact_qq = models.CharField(max_length=20)
    contact_weixin = models.CharField(max_length=20)#微信
    address = models.CharField(max_length=100)#地址
    postno = models.CharField(max_length=10)#邮编
    reg_time = models.DateTimeField(auto_now=True) #报名时间
    pay_status = models.IntegerField(choices=PAY_STATUS, default=0) #是否付款
    bill = models.OneToOneField(Bill, null=True) #账单编号

    class Meta:
        app_label='sp'

class StudentTeam(models.Model):
    team = models.ForeignKey(Team)
    student = models.ForeignKey(Student)
    stu_number = models.CharField(max_length=20)
    class Meta:
        app_label='sp'

class TeamEvent(models.Model):
    event = models.ForeignKey(Event)
    team = models.ForeignKey(Team)
    award = models.IntegerField(choices=AWARD, default=0)
    certificate = models.CharField(max_length=100, null=True) #证书编号
    get_time = models.DateTimeField(null=True) #通过时间
    class Meta:
        app_label='sp'

