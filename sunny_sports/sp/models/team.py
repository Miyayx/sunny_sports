#!/usr/bin/env python
#-*-coding:utf-8-*-
from django.db import models

class Team(models.Model):
    team_id = models.CharField(max_length=15)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    company = models.CharField(max_length=50)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=30)
    principal = models.CharField(max_length=20)
    contact = models.CharField(max_length=30)
    regtime = models.DateTimeField()

