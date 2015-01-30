
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.http import require_http_methods
from django.template import RequestContext

from sunny_sports.sp.models import *
from sunny_sports.sp.models.association import *
from sunny_sports.sp.models.role import *
from sunny_sports.sp.models.models import *
from sunny_sports.sp.models.status import *
from sunny_sports.sp.forms import *

def home(req):
    uuid = req.session.get('uuid',0)
    # 用这个id查信息哦
    print uuid
    coachorg = CoachOrg.objects.filter(user_id=uuid)
    return render_to_response('coach_org/home.html',{"coachorg":coachorg[0]})

def train(req):
    uuid = req.session.get('uuid',0)
    # 用这个id查信息哦
    trains = Train.objects.filter(org__user_id=uuid)
    return render_to_response('coach_org/train_query.html',{"coachorgtrains":trains})

def center(req):
    uuid = req.session.get('uuid',0)
    # 用这个id查信息哦
   # coach_org = CoachOrg.objects.filter(user_id=uuid)
   # return render_to_response('coach_org/center.html',{"coachorg":coach_org[0]})
     return render_to_response('coach_org/center.html',{})

def train_publish(req):
    if req.method == "POST":
        data = req.POST.copy()
        uuid = req.session.get('uuid',0)
        org = CoachOrg.objects.get(user_id=uuid)
        data['org'] = org.id
        data['level'] = int(data['level'])
        data['money'] = int(data['money'])
        data['limit'] = int(data['limit'])
        data['address'] = data.get('prov','')+data.get('city','')+data.get('dist','')+data.get('addr','')
        print data
        
        t = TrainPublishForm(data)
        if t.is_valid():
            t.save()
            return JsonResponse({'success':True})
        else:
            return JsonResponse({'success':False})
        
    else:
        uuid = req.session.get('uuid',0)
        print uuid
        org = CoachOrg.objects.get(user_id=uuid)
        print org.name
        return render_to_response('coach_org/train_publish.html',{'level':TRAIN_LEVEL,'org':org}, RequestContext(req))
        



