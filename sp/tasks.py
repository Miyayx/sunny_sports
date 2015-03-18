# -*- coding:utf-8 -*-

from django.utils import timezone

from celery import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from sp.models.association import *
from sp.models.role import *
from sp.models.models import *
from sp.models.status import *
from sp.models.train import *

#@periodic_task(run_every=crontab(hour=0, minute=0))
@periodic_task(run_every=crontab(minute='*/30'))
def train_reg_start_p():
    print("%d trains start"%len(Train.objects.filter(reg_status=0, reg_stime__lte=timezone.now())))
    Train.objects.filter(reg_status=0, reg_stime__lte=timezone.now()).update(reg_status=1)

#@periodic_task(run_every=crontab(hour=0, minute=0))
@periodic_task(run_every=crontab(minute='*/30'))
def train_reg_end_p():
    print("%d trains end"%len(Train.objects.filter(reg_status=1, reg_etime__lte=timezone.now())))
    Train.objects.filter(reg_status=1, reg_etime__lte=timezone.now()).update(reg_status=2)

@task
def train_reg_start(t_id):
    print("%s train reg start at %s"%(t_id, timezone.now()))
    Train.objects.filter(id=t_id, pass_status=1, reg_status=0, reg_stime__lte=timezone.now()).update(reg_status=1)

@task
def train_reg_end(t_id):
    print("%s train reg end at %s"%(t_id, timezone.now()))
    Train.objects.filter(id=t_id, pass_status=1, reg_status__lte=2, reg_etime__lte=timezone.now()).update(reg_status=2)

@task
def train_start(t_id):
    print("%s train start at %s"%(t_id, timezone.now()))
    Train.objects.filter(id=t_id, pass_status=1, train_stime__lte=timezone.now()).update(train_status=1)

@task
def train_end(t_id):
    print("%s train end at %s"%(t_id, timezone.now()))
    Train.objects.filter(id=t_id, pass_status=1, train_etime__lte=timezone.now()).update(train_status=2)

@task
def payment_check(ct_id):
    #规定时间进行检查，若还未缴费，状态改成未报名
    # 若缴费前报名已经截止？
    print("payment check")
    CoachTrain.objects.filter(id = ct_id, status=1).update(status=0)
