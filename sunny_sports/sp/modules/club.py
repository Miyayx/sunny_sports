#!/usr/bin/env python
#-*-coding:utf8-*-
from django.db import models

class Club(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.IntegerField()
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    county = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    level = models.IntegerField()