#!/usr/bin/env python
#-*-coding:utf-8-*-
from django.db import models

from role import *
from club import *
from game import *
from committee import *
from coach_org import *
from association import *

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=10)
    class Meta:
        app_label='sp'
    
class User(models.Model):
    username = models.CharField(max_length=15)
    phone    = models.CharField(max_length=15)
    password = models.CharField(max_length=32)
    role = models.ForeignKey(Role)
    class Meta:
        app_label='sp'
    
    
class Code(models.Model):
    phone = models.IntegerField()
    code = models.CharField(max_length=10)
    time = models.DateTimeField()
    class Meta:
        app_label='sp'
    
