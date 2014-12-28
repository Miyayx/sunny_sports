
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

def home(req):
    uuid = req.session['uuid']
    # 用这个id查信息哦

    return render_to_response('coach/home.html',{})

def train(req):
    uuid = req.session['uuid']
    # 用这个id查信息哦

    return render_to_response('coach/train.html',{})

def centre(req):
    uuid = req.session['uuid']
    # 用这个id查信息哦

    return render_to_response('coach/center.html',{})




















