#-*-coding:utf-8-*-
from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    sponsor = models.CharField(max_length=50)
    coorganizer = models.CharField(max_length=200)
    begin_time = models.DateTimeField()
    sign_time = models.DateTimeField()
    end_time = models.DateTimeField()
    team_max = models.IntegerField()
    team_min = models.IntegerField()
    status = models.IntegerField()
    class Meta:
        app_label='sp'

class Event(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=200)
    class Meta:
        app_label='sp'
    
class Umpire(models.Model):
    name = models.CharField(max_length=10)
    level = models.IntegerField()
    class Meta:
        app_label='sp'
    
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

    class Meta:
        app_label='sp'

