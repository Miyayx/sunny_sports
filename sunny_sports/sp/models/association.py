#!/usr/bin/env python
#-*-coding:utf-8-*-

from django.db import models

from role import *
from club import *
from game import *
from train import *
from committee import *
from status import *

def make_ct_num():
    import random
    return random.randint(0,100)


class CoachTrain(models.Model):
    number = models.IntegerField(default=make_ct_num())
    coach = models.ForeignKey(Coach)
    train = models.ForeignKey(Train)
    score = models.IntegerField(default=0) 
    status = models.IntegerField(default=0,choices=ROLE_TRAIN_STATUS)
    pass_status = models.BooleanField(default=0,choices=ROLE_TRAIN_PASS_STATUS)
    certificate = models.CharField(max_length=100, null=True) #证书编号
    reg_time = models.DateTimeField(null=True) #报名时间
    get_time = models.DateTimeField(null=True) #通过时间
    class Meta:
        app_label='sp'

    def __str__(self):
        return "coach:%s,  train:%s"%(self.coach, self.train)

    
#class StudentTeam(models.Model):
#    team = models.ForeignKey(Team)
#    student = models.ForeignKey(Student)
#    game = models.ForeignKey(Game)
#    stu_number = models.CharField(max_length=20)
#    stu_status = models.IntegerField()
#    class Meta:
#        app_label='sp'
#    
#class GameEvent(models.Model):
#    game = models.ForeignKey(Game)
#    event = models.ForeignKey(Event)
#    property = models.IntegerField()
#    umpires = models.CharField(max_length=20)
#    class Meta:
#        app_label='sp'
#    
#class TeamGame(models.Model):
#    team = models.ForeignKey(Team)
#    game = models.ForeignKey(Game)
#    team_num = models.CharField(max_length=20)
#    team_name = models.CharField(max_length=30)
#    team_principal = models.CharField(max_length=20)
#    prin_contact = models.CharField(max_length=30)
#    team_status = models.IntegerField()
#    score = models.IntegerField()
#    award = models.CharField(max_length=50)
#    pay_status = models.IntegerField()
#    members = models.CharField(max_length=100)
#    class Meta:
#        app_label='sp'
#    
#class StudentEvent(models.Model):
#    event = models.ForeignKey(GameEvent)
#    stu_number = models.CharField(max_length=20)
#    team_num = models.CharField(max_length=20)
#    score = models.IntegerField()
#    award = models.CharField(max_length=50)
#    class Meta:
#        app_label='sp'
