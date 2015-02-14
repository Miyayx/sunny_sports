
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.http import require_http_methods
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from sunny_sports.sp.models import *
from sunny_sports.sp.models.association import *
from sunny_sports.sp.models.role import *
from sunny_sports.sp.models.models import *
from sunny_sports.sp.models.status import *
from sunny_sports.sp.forms import *

@login_required()
def coach_org(req):
    return HttpResponseRedirect("coach_org/home")

@login_required()
def home(req):
    uuid = req.user.id
    # 用这个id查信息哦
    print uuid
    coachorg = CoachOrg.objects.filter(user_id=uuid)
    trains = Train.objects.filter(org__user_id=uuid)
    return render_to_response('coach_org/home.html',{"coachorg":coachorg[0],"coachorgtrains":trains} ,RequestContext(req))

@login_required()
def train(req):
    uuid = req.user.id
    # 用这个id查信息哦
    trains = Train.objects.filter(org__user_id=uuid)
    return render_to_response('coach_org/train_query.html',{"coachorgtrains":trains},RequestContext(req))

@login_required()
def center(req):
    uuid = req.user.id
    # 用这个id查信息哦
    coach_org = CoachOrg.objects.filter(user_id=uuid)
    return render_to_response('coach_org/center.html',{"coachorg":coach_org[0]},RequestContext(req))

@login_required()
def train_publish(req):
    if req.method == "POST":
        data = req.POST.copy()
        uuid = req.user.id
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
        uuid = req.user.id
        org = CoachOrg.objects.get(user_id=uuid)
        return render_to_response('coach_org/train_publish.html',{'level':TRAIN_LEVEL,'org':org}, RequestContext(req))

@login_required()
def score_input(req):
    if req.method == "POST":
        pass
    else:
        return render_to_response('coach_org/score_input.html',{}, RequestContext(req))
        
@login_required()
@transaction.atomic
def update_info(req):
    """
    个人中心，用户更新基本信息
    """
    if req.method == "POST":
        data = req.POST.copy()
        #if not data.get("province"):
        #    data["province"] = ""
        #if not data.get("city"):
        #    data["city"] = ""
        #if not data.get("dist"):
        #    data["dist"] = ""
        #data["sex"] = int(data["sex"])
        #data.pop("csrfmiddlewaretoken")
        #data.pop("birth")

        uuid = req.user.id
        MyUser.objects.filter(id=uuid).update(phone=data.pop("phone")[0], email=data.pop("email")[0])
        co = CoachOrg.objects.get(user_id=uuid)
        if data.has_key("orgname"):
            co.company = data["orgname"]
        if data.has_key("province"):
            co.province = data.get("province","")
        if data.has_key("city"):
            co.city = data.get("city","")
        if data.has_key("dist"):
            co.dist = data.get("dist","")
        if data.has_key("address"):
            co.address = data.get("address","")

        try:
            co.save()
        except:
            return JsonResponse({'success':False})
        return JsonResponse({'success':True})
