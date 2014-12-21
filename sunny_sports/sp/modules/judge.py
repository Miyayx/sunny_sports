#!/usr/bin/env python
#-*-coding:utf-8-*-

from django.db import models

class JudgeProperty(models.Model):
    name = models.CharField(max_length=20)
    sex = models.CharField(max_length=4)
    email = models.EmailField()
    phone = models.IntegerField()
    birthday = models.DateField()
    age = models.IntegerField()
    identity = models.IntegerField()
    photo = models.URLField()
    company = models.CharField(max_length=50)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    county = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    
    class Meta:
        app_label='sp'
