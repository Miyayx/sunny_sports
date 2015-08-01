#!/usr/bin/env python
#-*-coding:utf-8-*-

from django.db import models

from sp.models.models import *

# Create your models here.

class Club(models.Model):
    user = models.ForeignKey(MyUser)
    name = models.CharField(max_length=200, blank=True)
    shortname = models.CharField(max_length=100, blank=True)
    org_num  = models.CharField(max_length=50, blank=True)
    corporator = models.CharField(max_length=20, blank=True)
    office_num = models.CharField(max_length=30, blank=True)
    province = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=30, blank=True)
    dist = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100,blank=True)
    license = models.ImageField(upload_to='upload', default='')
    level = models.IntegerField(default=0)
    class Meta:
        app_label='sp'

    def __str__(self):
        return self.name

