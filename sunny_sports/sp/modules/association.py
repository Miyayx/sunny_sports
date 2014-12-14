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

class Student(models.Model):
    property = models.ForeignKey(StudentProperty)
    club_id = models.IntegerField()
    level = models.IntegerField()
    status = models.IntegerField()
    regtime = models.DateTimeField()

    class Meta:
        app_label='sp'
    
class Judge(models.Model):
    property = models.ForeignKey(StudentProperty)
    club_id = models.IntegerField()
    level = models.IntegerField()
    status = models.IntegerField()
    regtime = models.DateTimeField()
    class Meta:
        app_label='sp'

class Coach(models.Model):
    property = models.ForeignKey(StudentProperty)
    club_id = models.IntegerField()
    level = models.IntegerField()
    status = models.IntegerField()
    regtime = models.DateTimeField()
    class Meta:
        app_label='sp'
