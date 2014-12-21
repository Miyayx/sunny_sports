#!/usr/bin/env python
#-*-coding:utf8-*-
from django.db import models

class Centre(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    real_name = models.CharField(max_length=4)
    email = models.EmailField()
    phone = models.IntegerField()
    
    class Meta:
        app_label='sp'
