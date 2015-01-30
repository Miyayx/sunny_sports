
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
    
    if coach[0].p_level == 0:
        ltrain = Train.objects.filter(level=1)
        return render_to_response('coach/train.html',{"coach":coach[0], "ltrain":ltrain})
    elif coach[0].p_level == 1:
        ltrain = CoachTrain.objects.filter(coach_id=coach[0].id, train__level=1)
        #ltrain = Train.objects.filter(id=ctrain[0].train_id)
        mtrain = Train.objects.filter(level=2)
        return render_to_response('coach/train.html',{"coach":coach[0], "ltrain":ltrain[0], "mtrain":mtrain})
    elif coach[0].p_level == 2:
        ltrain = CoachTrain.objects.filter(coach_id=coach[0].id, train__level=1)
        mtrain = CoachTrain.objects.filter(coach_id=coach[0].id, train__level=2)
        htrain = Train.objects.filter(level=3)
        return render_to_response('coach/train.html',{"coach":coach[0], "ltrain":ltrain[0], "mtrain":mtrain[0], "htrain":htrain})
    else:
        ltrain = CoachTrain.objects.filter(coach_id=coach[0].id, train__level=1)
        mtrain = CoachTrain.objects.filter(coach_id=coach[0].id, train__level=2)
        htrain = CoachTrain.objects.filter(coach_id=coach[0].id, train__level=3)
        return render_to_response('coach/train.html',{"coach":coach[0], "ltrain":ltrain[0], "mtrain":mtrain[0], "htrain":htrain[0]})

def center(req):
    uuid = req.session.get('uuid',0)
    # 用这个id查信息哦
    print uuid
    coach = Coach.objects.filter(property__user_id=uuid)
    club = Club.objects.filter()
    return render_to_response('coach/center.html',{"coach":coach[0], "club":club})




















