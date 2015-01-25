
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
    uuid = req.session.get('uuid',0)
    # 用这个id查信息哦
    print uuid
    coach = Coach.objects.filter(property__user_id=uuid)

    return render_to_response('coach/home.html',{"coach":coach[0]})

def train(req):
    uuid = req.session.get('uuid',0)
    # 用这个id查信息哦
    print uuid
    coach = Coach.objects.filter(property__user_id=uuid)
    #if coach[0].p_level = 0:
     #   train = Train.objects.filter()
    #else if 
        
    
    return render_to_response('coach/train.html',{"coach":coach[0], "train":train})

def center(req):
    uuid = req.session.get('uuid',0)
    # 用这个id查信息哦
    print uuid
    coach = Coach.objects.filter(property__user_id=uuid)
    club = Club.objects.filter()
    return render_to_response('coach/center.html',{"coach":coach[0], "club":club})




















