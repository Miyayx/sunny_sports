#!/usr/bin/env python
#-*-coding:utf-8-*-
from django.db import models

from student import *
from coach import *
from judge import *
from club import *
from team import *
from committee import *
from coach_org import *
from association import *

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=10)
    
class User(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=32)
    role = models.ForeignKey(Role)
    
class Game(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    sponsor = models.CharField(max_length=50)
    coorganizer = models.CharField(max_length=200)
    begin_time = models.DateTimeField()
    sign_time = models.DateTimeField()
    end_time = models.DateTimeField()
    team_max = models.IntegerField()
    team_min = models.IntegerField()
    status = models.IntegerField()
    
class StudentTeam(models.Model):
    team = models.ForeignKey(Team)
    student = models.ForeignKey(Student)
    game = models.ForeignKey(Game)
    stu_number = models.CharField(max_length=20)
    stu_status = models.IntegerField()
    
class Event(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=200)
    
class Umpire(models.Model):
    name = models.CharField(max_length=10)
    level = models.IntegerField()
    
class GameEvent(models.Model):
    game = models.ForeignKey(Game)
    event = models.ForeignKey(Event)
    property = models.IntegerField()
    umpires = models.CharField(max_length=20)
    
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
    
class StudentEvent(models.Model):
    event = models.ForeignKey(GameEvent)
    stu_number = models.CharField(max_length=20)
    team_num = models.CharField(max_length=20)
    score = models.IntegerField()
    award = models.CharField(max_length=50)
    
class Code(models.Model):
    phone = models.IntegerField()
    code = models.CharField(max_length=10)
    time = models.DateTimeField()
    
class Train(models.Model):
    name = models.CharField(max_length=30)
    demo = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    level = models.IntegerField()
    max = models.IntegerField()
    money = models.IntegerField()
    org_id = models.IntegerField()
    reg_stime = models.DateTimeField()
    reg_etime = models.DateTimeField()
    train_stime = models.DateTimeField()
    
    
class Coach_Train(models.Model):
    coach_id = models.IntegerField()
    train_id = models.IntegerField()
    number = models.IntegerField()
    score = models.IntegerField()
    status = models.IntegerField()
    certificate = models.CharField(max_length=100)
    get_time = models.DateTimeField()
    
