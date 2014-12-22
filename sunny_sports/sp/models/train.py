#-*-coding:utf-8-*-

from django.db import models

class Train(models.Model):
    name = models.CharField(max_length=30)
    demo = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    level = models.IntegerField()
    max = models.IntegerField()
    money = models.IntegerField()
    org_id = models.IntegerField()
    reg_stime = models.DateTimeField()
    reg_etime = models.DateTimeField()
    train_stime = models.DateTimeField()
    
    class Meta:
        app_label='sp'
