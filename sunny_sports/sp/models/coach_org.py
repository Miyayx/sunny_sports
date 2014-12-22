#!/usr/bin/env python
#-*-coding:utf-8-*-

from django.db import models

class Coach_Org(models.Model):
    log_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    org_name = models.CharField(max_length=4)
    email = models.EmailField()
    phone = models.IntegerField()
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    county = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    
    class Meta:
        app_label='sp'
