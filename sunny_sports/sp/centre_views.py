# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.http import require_http_methods

from sunny_sports.sp.models import *
from sunny_sports.sp.models.association import *
from sunny_sports.sp.models.role import *
from sunny_sports.sp.models.models import *

def test_check(req, train_id=None):
    print "test_check, id %s"%train_id
    if train_id and len(train_id) > 0: #有编号的话就返回对应课程的人名单
        c_t = Coach_Train.objects.filter(train_id=train_id)
        #train = Train.objects.get(id=train_id)
        #filter return a list
        #get return an item
        train = c_t[0].train
        return render_to_response('centre/test_check2.html',{"c_t":c_t, "train":train})
    else:#否则返回待审核列表
        c_t = Coach_Train.objects.filter(train__pub_status=0) #这里查的是Train的status，是联合两个表的查询，用两个_
        ctlist = [i.train for i in c_t]
        print ctlist[0]
        jtlist = []
        return render_to_response('centre/test_check.html',{"ctlist":ctlist, "jtlist":jtlist})

def check_pass(req):
    """
    审核批准后
    """
    pass

def check_unpass(req):
    """
    审核不批准后
    """
    pass

def history_view(req, train_id=None):
    if train_id and len(train_id) > 0: #有编号的话就返回对应课程的人名单
        c_t = Coach_Train.objects.filter(train_id=train_id)
        train = c_t[0].train
        return render_to_response('centre/history_view2.html',{"c_t":c_t, "train":train})
    else:#否则返回课程列表
        c_t = Coach_Train.objects.filter(train__pub_status=1) #这里查的是Train的status，是联合两个表的查询，用两个_
        ctlist = [i.train for i in c_t]
        jtlist = []
        print "c"
        return render_to_response('centre/history_view.html',{"ctlist":ctlist, "jtlist":jtlist})

def history_print(req, train_id=None):
    """
    生成csv表格并下载
    """
    if train_id and len(train_id) > 0:
        return csv_generate()
    else:
        return "Wrong Train id"

