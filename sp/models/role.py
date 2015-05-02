#!/usr/bin/env python
#-*-coding:utf-8-*-

from django.db import models
from models import *
from status import *

class PersonProperty(models.Model):
    """
    这是一个父类,所有个人角色继承于它
    """
    user = models.ForeignKey(MyUser, unique=True, db_index=True)
    name = models.CharField(max_length=20, blank=True)
    sex = models.IntegerField(choices=SEX, default=0)
    birth = models.DateField(default="1990-01-01")
    identity = models.CharField(max_length=20, unique=True, null=True)
    avatar = models.ImageField(upload_to = 'upload', default='upload/default.jpg')
    class Meta:
        abstract = True

    def __str__(self):
        return "user:%s, name:%s"%(self.user, self.name)


class CoachProperty(PersonProperty):
    """
    继承于PersonProperty
    """
    company = models.CharField(max_length=50, blank=True )
    province = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=30, blank=True)
    dist = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    
    class Meta:
        app_label='sp'

class Club(models.Model):
    user = models.ForeignKey(MyUser, unique=True, db_index=True)
    province = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=30, blank=True)
    county = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100,blank=True)
    level = models.IntegerField(default=0)
    class Meta:
        app_label='sp'

    def __str__(self):
        return self.user.nickname

    
class Coach(models.Model):
    property = models.ForeignKey(CoachProperty)
    club = models.ForeignKey(Club, null=True)
    t_level = models.IntegerField(choices=COACH_LEVEL, default=0) #教学等级
    p_level = models.IntegerField(choices=COACH_LEVEL,default=0) #专业等级
    status = models.IntegerField(default=0)
    isreg = models.BooleanField(default=False) #今年是否注册
    class Meta:
        app_label='sp'

    def __str__(self):
        return str(self.property)


class CoachOrg(models.Model):
    user = models.ForeignKey(MyUser)
    org_num  = models.CharField(max_length=20)
    name = models.CharField(max_length=256)
    shortname = models.CharField(max_length=10)
    director = models.CharField(max_length=256, blank=True, default="")
    province = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=30, blank=True)
    dist = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True) 
    ali_email = models.EmailField(null=True)
    
    class Meta:
        app_label='sp'

    def __str__(self):
        return "num:%s, name:%s"%(self.org_num,self.name)

