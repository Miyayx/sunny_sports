#!/usr/bin/env python
#-*-coding:utf-8-*-

from django.db import models

from student.models import *
from sp.models.status import *
from payment.models import *

import datetime

AWARD = (
        (0, '暂无结果'),
        (1, '一等奖'),
        (2, '二等奖'),
        (3, '三等奖'),
        (4, '参赛奖'),
        (5, '缺赛'),
        )

EVENTS = (
        (0, '接力通关赛'),
        (1, '男团体赛'),
        (2, '女团体赛'),
        (3, '快乐集体舞'),
        )

class Event(models.Model):
    name = models.IntegerField(choices=EVENTS)
    description = models.CharField(max_length=1000)
    class Meta:
        app_label='sp'
    
class Game(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default="", unique=True)
    org = models.ForeignKey(GameOrg) #组织机构
    name = models.CharField(max_length=50, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    sponsor = models.CharField(max_length=800, blank=True) #主办单位 ;分隔
    organizer = models.CharField(max_length=800, blank=True) #承办单位 ;分隔
    coorganizer = models.CharField(max_length=800, blank=True)#协办单位 ;分隔
    schedule = models.TextField(max_length=2000, blank=True) #日程安排，
    province = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=30, blank=True)
    dist = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=200, blank=True)
    events = models.TextField(max_length=20, blank=True) #比赛项目
    limit = models.IntegerField(default=0) #参赛队数
    male_num = models.IntegerField(default=0) #每队男生人数
    female_num = models.IntegerField(default=0) #每队女生人数
    total_num = models.IntegerField(default=0) #每队总人数
    money = models.IntegerField(default=0) #每人参赛费用
    reg_place = models.CharField(max_length=500, blank=True) #报名地点
    reg_stime = models.DateTimeField(null=True) #报名开始时间
    reg_etime = models.DateTimeField(null=True) #报名截止时间
    game_stime = models.DateTimeField(null=True) #比赛开始时间
    game_etime = models.DateTimeField(null=True) #比赛结束时间
    submit_status = models.IntegerField(choices=SUBMIT_STATUS, default=0)#是否提交审核状态
    pass_status = models.IntegerField(choices=PASS_STATUS, default=0)#审核状态
    reg_status = models.IntegerField(choices=REG_STATUS, default=0) #报名状态
    game_status = models.IntegerField(choices=TRAIN_STATUS, default=0) #比赛状态
    sub_status = models.IntegerField(choices=SUB_STATUS, default=0) #成绩是否提交
    pub_status = models.IntegerField(choices=PUB_STATUS, default=0) #成绩是否发布
    contact_name = models.CharField(max_length=50, blank=True) #联系人
    contact_phone = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(max_length=100, blank=True)

    class Meta:
        app_label='sp'

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        """
        编号生成规则：组织机构缩写+当前年份+今年比赛数量
        """
        if len(self.id) == 0:
            now = datetime.datetime.now()
            self.id = "{0}{1}{2:0>2d}".format(self.org.shortname, now.year, Game.objects.filter(org=self.org, game_stime__year=now.year).count()+1)
            print self.id

        super(Game, self).save(*args, **kwargs)

class Team(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    contestant = models.ForeignKey(UserRole) #所属参赛单位
    game = models.ForeignKey(Game)
    name = models.CharField(max_length=50, null=True) #队名
    leader = models.CharField(max_length=50, null=True, blank=True)# 领队
    contact_name = models.CharField(max_length=50, null=True, blank=True) #联系人
    contact_phone = models.CharField(max_length=100, null=True, blank=True)
    contact_email = models.EmailField(max_length=100, null=True, blank=True)
    contact_qq = models.CharField(max_length=100, null=True, blank=True)
    contact_wx = models.CharField(max_length=100, null=True, blank=True)#微信
    address = models.CharField(max_length=500,null=True, blank=True)
    postno = models.CharField(max_length=80, null=True, blank=True)#邮编
    reg_time = models.DateTimeField(default=datetime.datetime.now) #报名时间
    pay_status = models.IntegerField(choices=PAY_STATUS, default=0) #是否付款
    bill = models.OneToOneField(Bill, null=True) #账单编号
    other_info = models.CharField(max_length=5000, null=True, blank=True) #备注，其他成员信息

    class Meta:
        app_label='sp'

    def save(self, *args, **kwargs):
        """
        编号生成规则：game_id+contestant_id+当前分钟与秒数
        """
        if len(self.id) == 0:
            now = datetime.datetime.now()
            self.id = "{0}{1}{2}".format(self.game.id, self.contestant.id, str(now.minute)+str(now.second))
            print self.id

        super(Team, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        print "delete team", self.id
        StudentTeam.objects.filter(team_id=self.id).delete()
        TeamEvent.objects.filter(team_id=self.id).delete()
        super(Team, self).delete(*args, **kwargs)

class StudentTeam(models.Model):
    team = models.ForeignKey(Team)
    student = models.ForeignKey(Student)
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

    def check_pass(self, num):
        """
        num:当前的证书数量
        """
        self.certificate = "{0}{1:0>6d}".format(self.event.id, num)
        self.get_time=datetime.datetime.now()
        self.pass_status=1
        self.save()

