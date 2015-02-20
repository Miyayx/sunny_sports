
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.http import require_http_methods
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from sunny_sports.sp.models import *
from sunny_sports.sp.models.association import *
from sunny_sports.sp.models.role import *
from sunny_sports.sp.models.models import *
from sunny_sports.sp.forms import *
from utils import *

@login_required()
def coach(req):
    uuid = req.user.id
    u=UserRole.objects.get(user_id=uuid, role_id=3)
    if u.is_first:
        messages.error(req, u"请补全个人信息")
        return HttpResponseRedirect("coach/center")
    else:
        return HttpResponseRedirect("coach/home")

@login_required()
def home(req):
    uuid = req.user.id
    # 用这个id查信息哦
    print uuid
    coach = Coach.objects.get(property__user_id=uuid)
    coach.property.age = calculate_age(coach.property.birth) 

    return render_to_response('coach/home.html',{"coach":coach})

@login_required()
def train(req):
    uuid = req.user.id # 用这个id查信息哦
    coach = Coach.objects.get(property__user_id=uuid)
    
    if coach.t_level == 0:
        ltrain = Train.objects.filter(level=1, reg_status=0)
        return render_to_response('coach/train.html',{"coach":coach, "ltrain":ltrain})
    elif coach.t_level == 1:
        ltrain = CoachTrain.objects.filter(coach=coach, train__level=1, status=1)
        mtrain = Train.objects.filter(level=2, reg_status=0)
        return render_to_response('coach/train.html',{"coach":coach, "ltrain":ltrain[0], "mtrain":mtrain})
    elif coach.t_level == 2:
        ltrain = CoachTrain.objects.filter(coach=coach, train__level=1, status=1)
        mtrain = CoachTrain.objects.filter(coach=coach, train__level=2, status=1)
        htrain = Train.objects.filter(level=3, reg_status=0)
        hsize = len(htrain)
        return render_to_response('coach/train.html',{"coach":coach, "ltrain":ltrain[0], "mtrain":mtrain[0], "htrain":htrain})
    else:
        ltrain = CoachTrain.objects.filter(coach=coach, train__level=1, status=1)
        mtrain = CoachTrain.objects.filter(coach=coach, train__level=2, status=1)
        htrain = CoachTrain.objects.filter(coach=coach, train__level=3, status=1)
        return render_to_response('coach/train.html',{"coach":coach, "ltrain":ltrain[0], "mtrain":mtrain[0], "htrain":htrain[0]})

@login_required()
def center(req):
    uuid = req.user.id
    # 用这个id查信息哦
    u = UserRole.objects.get(user_id=uuid, role_id=3)
    if u.is_first:
        messages.error(req, u"请补全个人信息")
    coach = Coach.objects.filter(property__user_id=uuid)
    club = Club.objects.filter()
    return render_to_response('coach/center.html',{"coach":coach[0], "club":club}, RequestContext(req))

@login_required()
@transaction.atomic
def info_confirm(req):
    """
    报名后的信息确认
    """
    uuid = req.user.id
    if req.method == "POST":
        data = req.POST.copy()

        ur = UserRole.objects.get(user_id=uuid, role_id=3)
        MyUser.objects.filter(id=uuid).update(phone=data.pop("phone")[0], email=data.pop("email")[0])
        cp = CoachProperty.objects.get(user_id=uuid)
        cp.name = data.get("name","")
        cp.sex = int(data.get("sex"))
        if data.has_key("identity"):
            cp.identity = data.get("identity","")
        #cp.birth = data.get("birth","")
        if data.has_key("company"):
            cp.company = data["company"]
        if data.has_key("province"):
            cp.province = data.get("province","")
        if data.has_key("city"):
            cp.city = data.get("city","")
        if data.has_key("dist"):
            cp.dist = data.get("dist","")
        if data.has_key("address"):
            cp.address = data.get("address","")
        try:
            cp.save()
            ur.save()
        except:
            return JsonResponse({'success':False})
        return JsonResponse({'success':True})
    else:
        t_id = req.GET.get("t_id",0)
        train = Train.objects.get(id=t_id)
        coach = Coach.objects.get(property__user_id=uuid)
        club = Club.objects.filter()
        return render_to_response('coach/info_confirm.html',{"coach":coach, "club":club, "train":train}, RequestContext(req))

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
        ur = UserRole.objects.get(user_id=uuid, role_id=3)
        ur.is_first = True
        if data.has_key("nickname"):
            MyUser.objects.filter(id=uuid).update(nickname=data.pop("nickname")[0], phone=data.pop("phone")[0], email=data.pop("email")[0])
        else:
            MyUser.objects.filter(id=uuid).update(phone=data.pop("phone")[0], email=data.pop("email")[0])

        cp = CoachProperty.objects.get(user_id=uuid)
        cp.name = data.get("name","")
        cp.sex = int(data.get("sex"))
        cp.avatar = data.get("avatar","")
        if data.has_key("identity"):
            cp.identity = data.get("identity","")
        #cp.birth = data.get("birth","")
        if data.has_key("company"):
            cp.company = data["company"]
        if data.has_key("province"):
            cp.province = data.get("province","")
        if data.has_key("city"):
            cp.city = data.get("city","")
        if data.has_key("dist"):
            cp.dist = data.get("dist","")
        if data.has_key("address"):
            cp.address = data.get("address","")
        try:
            cp.save()
            ur.save()
        except:
            return JsonResponse({'success':False})
        #c = CoachPropertyForm(instance=cp, data=data)
        #print data
        #if c.is_valid():
        #    c.save()
        return JsonResponse({'success':True})
        #else:
        #    return JsonResponse({'success':False})

