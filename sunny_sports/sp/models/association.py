#!/usr/bin/env python
#-*-coding:utf-8-*-

from django.db import models

from role import *
from club import *
from game import *
from train import *
from committee import *
from coach_org import *

class Student(models.Model):
    property = models.ForeignKey(StudentProperty)
    #club_id = models.IntegerField()
    club = models.ForeignKey(Club)
    level = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        app_label='sp'
    
class Judge(models.Model):
    property = models.ForeignKey(JudgeProperty)
    #club_id = models.IntegerField()
    club = models.ForeignKey(Club)
    level = models.IntegerField()
    status = models.IntegerField()
    ifreg = models.BooleanField(default=False)#今年是否注册
    class Meta:
        app_label='sp'

class Coach(models.Model):
    property = models.ForeignKey(CoachProperty)
    #club_id = models.IntegerField()
    club = models.ForeignKey(Club)
    t_level = models.IntegerField() #教学等级
    p_level = models.IntegerField() #专业等级
    status = models.IntegerField()
    ifreg = models.BooleanField(default=False) #今年是否注册
    class Meta:
        app_label='sp'

class Coach_Train(models.Model):
    #coach_id = models.IntegerField()
    #train_id = models.IntegerField()
    coach = models.ForeignKey(Coach)
    train = models.ForeignKey(Train)
    number = models.IntegerField()
    score = models.IntegerField()
    status = models.IntegerField()
    certificate = models.CharField(max_length=100)
    get_time = models.DateTimeField()
    class Meta:
        app_label='sp'
    
class StudentTeam(models.Model):
    team = models.ForeignKey(Team)
    student = models.ForeignKey(Student)
    game = models.ForeignKey(Game)
    stu_number = models.CharField(max_length=20)
    stu_status = models.IntegerField()
    class Meta:
        app_label='sp'
    
class GameEvent(models.Model):
    game = models.ForeignKey(Game)
    event = models.ForeignKey(Event)
    property = models.IntegerField()
    umpires = models.CharField(max_length=20)
    class Meta:
        app_label='sp'
    
class TeamGame(models.Model):
    team = models.ForeignKey(Team)
    game = models.ForeignKey(Game)
    team_num = models.CharField(max_length=20)
    team_name = models.CharField(max_length=30)
    team_principal = models.CharField(max_length=20)
    prin_contact = models.CharField(max_length=30)
    team_status = models.IntegerField()
    score = models.IntegerField()
    award = models.CharField(max_length=50)
    pay_status = models.IntegerField()
    members = models.CharField(max_length=100)
    class Meta:
        app_label='sp'
    
class StudentEvent(models.Model):
    event = models.ForeignKey(GameEvent)
    stu_number = models.CharField(max_length=20)
    team_num = models.CharField(max_length=20)
    score = models.IntegerField()
    award = models.CharField(max_length=50)
    class Meta:
        app_label='sp'
