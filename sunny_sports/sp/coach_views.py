
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
    coach = Coach.objects.filter(property__user_id=uuid)

    return render_to_response('coach/home.html',{"coach":coach[0]})

@login_required()
def train(req):
    uuid = req.user.id
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

@login_required()
def center(req):
    uuid = req.user.id
    # 用这个id查信息哦
    u=UserRole.objects.get(user_id=uuid, role_id=3)
    if u.is_first:
        messages.error(req, u"请补全个人信息")
    coach = Coach.objects.filter(property__user_id=uuid)
    club = Club.objects.filter()
    return render_to_response('coach/center.html',{"coach":coach[0], "club":club}, RequestContext(req))

@login_required()
@transaction.atomic
def update_user(req):
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
        MyUser.objects.filter(id=uuid).update(nickname=data.pop("nickname")[0], phone=data.pop("phone")[0], email=data.pop("email")[0])
        cp = CoachProperty.objects.get(user_id=uuid)
        cp.name = data.get("name","")
        cp.sex = int(data.get("sex"))
        cp.identity = data.get("identity","")
        cp.avatar = data.get("avatar","")
        #cp.birth = data.get("birth","")
        cp.company = data.get("company","")
        cp.province = data.get("province","")
        cp.city = data.get("city","")
        cp.dist = data.get("dist","")
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

