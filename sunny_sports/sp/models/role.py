#!/usr/bin/env python
#-*-coding:utf-8-*-

from django.db import models
from models import *

class PersonProperty(models.Model):
    """
    这是一个父类,所有个人角色继承于它
    """
    user = models.ForeignKey(MyUser)
    name = models.CharField(max_length=20)
    sex = models.CharField(max_length=4)
    birthday = models.DateField()
    age = models.IntegerField()
    identity = models.IntegerField()
    photo = models.URLField()
    regtime = models.DateTimeField()
    class Meta:
        abstract = True

class StudentProperty(PersonProperty):
    """
    继承于PersonProperty
    """
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
    """
    继承于PersonProperty
    """
    company = models.CharField(max_length=50)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    county = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    
    class Meta:
        app_label='sp'

class JudgeProperty(PersonProperty):
    """
    继承于PersonProperty
    """
    company = models.CharField(max_length=50)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    county = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    
    class Meta:
        app_label='sp'

class Student(models.Model):
    property = models.ForeignKey(StudentProperty)
    club = models.ForeignKey(Club)
    level = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        app_label='sp'
    
class Judge(models.Model):
    property = models.ForeignKey(JudgeProperty)
    club = models.ForeignKey(Club)
    level = models.IntegerField()
    status = models.IntegerField()
    ifreg = models.BooleanField(default=False)#今年是否注册
    class Meta:
        app_label='sp'

class Coach(models.Model):
    property = models.ForeignKey(CoachProperty)
    club = models.ForeignKey(Club)
    t_level = models.IntegerField() #教学等级
    p_level = models.IntegerField() #专业等级
    status = models.IntegerField()
    ifreg = models.BooleanField(default=False) #今年是否注册
    class Meta:
        app_label='sp'

class Coach_Org(models.Model):
    user = models.ForeignKey(MyUser)
    org_num  = models.CharField(max_length=20)
    org_name = models.CharField(max_length=128)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    county = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    
    class Meta:
        app_label='sp'
