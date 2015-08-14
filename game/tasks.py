# -*- coding:utf-8 -*-

from django.utils import timezone

from celery import task
from celery.task.schedules import crontab

from game.models import *

import datetime
from django.utils import timezone

from sunny_sports import settings

@task(acks_late=True)
def game_reg_start(g_id):
    print("%s game reg start at %s"%(g_id, timezone.now()))
    Game.objects.filter(id=g_id, pass_status=1, reg_status=0, reg_stime__lte=timezone.now()).update(reg_status=1)

@task(acks_late=True)
def game_reg_end(g_id):
    print("%s game reg end at %s"%(g_id, timezone.now()))
    Game.objects.filter(id=g_id, pass_status=1, reg_status__lte=2, reg_etime__lte=timezone.now()).update(reg_status=2)

@task(acks_late=True)
def game_start(g_id):
    print("%s game start at %s"%(g_id, timezone.now()))
    Game.objects.filter(id=g_id, pass_status=1, game_stime__lte=timezone.now()).update(game_status=1)

@task(acks_late=True)
def game_end(g_id):
    print("%s game end at %s"%(g_id, timezone.now()))
    Game.objects.filter(id=g_id, pass_status=1, game_etime__lte=timezone.now()).update(game_status=2)

@task(acks_late=True)
def payment_check(t_id):
    #规定时间进行检查，若还未缴费,删除报名记录
    # 若缴费前报名已经截止？
    print("payment check")
    try:
        t = Team.objects.get(id=t_id, pay_status=0)
        t.delete()
    except:
        print "t_id:",t_id,"has paid or doesn't exist"
        
