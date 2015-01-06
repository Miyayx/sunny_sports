#!/usr/bin/env python
#-*-coding:utf-8-*-

from django.db import models
from models import *
from status import *

class PersonProperty(models.Model):
    """
    这是一个父类,所有个人角色继承于它
    """
    user = models.ForeignKey(MyUser, unique=True)
    name = models.CharField(max_length=20)
    sex = models.IntegerField(choices=SEX)
    birthday = models.DateField()
    age = models.IntegerField(null=True)
    identity = models.CharField(max_length=20, unique=True)
    photo = models.URLField(null=True)
    class Meta:
        abstract = True

class StudentProperty(PersonProperty):
    """
    继承于PersonProperty
    """
    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    company = models.CharField(max_length=50, null=True)
    province = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=30, null=True)
    county = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=100, null=True)
    
    class Meta:
        app_label='sp'

class CoachProperty(PersonProperty):
    """
    继承于PersonProperty
    """
    company = models.CharField(max_length=50, blank=True)
    province = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=30, blank=True)
    county = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    
    class Meta:
        app_label='sp'

class JudgeProperty(PersonProperty):
    """
    继承于PersonProperty
    """
    company = models.CharField(max_length=50, blank=True)
    province = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=30, blank=True)
    county = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    
    class Meta:
        app_label='sp'

class Student(models.Model):
    property = models.ForeignKey(StudentProperty)
    club = models.ForeignKey(Club)
    level = models.IntegerField()
    status = models.IntegerField(default=0)

    class Meta:
        app_label='sp'
    
class Judge(models.Model):
    property = models.ForeignKey(JudgeProperty)
    club = models.ForeignKey(Club)
    level = models.IntegerField()
    status = models.IntegerField(default=0)
    ifreg = models.BooleanField(default=False)#今年是否注册
    class Meta:
        app_label='sp'

class Coach(models.Model):
    property = models.ForeignKey(CoachProperty)
    club = models.ForeignKey(Club, null=True)
    t_level = models.IntegerField() #教学等级
    p_level = models.IntegerField() #专业等级
    status = models.IntegerField(default=0)
    ifreg = models.BooleanField(default=False) #今年是否注册
    class Meta:
        app_label='sp'

class CoachOrg(models.Model):
    user = models.ForeignKey(MyUser)
    org_num  = models.CharField(max_length=20)
    org_name = models.CharField(max_length=256)
    province = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=30, blank=True)
    county = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    
    class Meta:
        app_label='sp'
