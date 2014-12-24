#!/usr/bin/env python
#-*-coding:utf-8-*-

from django.db import models
from models import *

class PersonProperty(models.Model):
    user = models.ForeignKey(MyUser)
    name = models.CharField(max_length=20)
    sex = models.CharField(max_length=4)
    email = models.EmailField()
    phone = models.IntegerField()
    birthday = models.DateField()
    age = models.IntegerField()
    identity = models.IntegerField()
    photo = models.URLField()
    regtime = models.DateTimeField()
    class Meta:
        abstract = True

class StudentProperty(PersonProperty):
    stu_id = models.CharField(max_length=15)
    height = models.IntegerField()
    weight = models.IntegerField()
    company = models.CharField(max_length=50)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    county = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    
    class Meta:
        app_label='sp'

class CoachProperty(PersonProperty):
    company = models.CharField(max_length=50)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    county = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    
    class Meta:
        app_label='sp'

class JudgeProperty(PersonProperty):
    company = models.CharField(max_length=50)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    county = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    
    class Meta:
        app_label='sp'
