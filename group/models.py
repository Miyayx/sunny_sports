#!/usr/bin/env python
#-*-coding:utf-8-*-
from django.db import models

from sp.models.models import *

# Create your models here.

class Group(models.Model):
    user = models.ForeignKey(MyUser)
    fullname = models.CharField(max_length=200, blank=True)
    org_num  = models.CharField(max_length=20, blank=True)
    province = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=30, blank=True)
    dist = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100,blank=True)

    class Meta:
        app_label='sp'

