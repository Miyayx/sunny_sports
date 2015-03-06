
# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.core.context_processors import csrf
from django.views.decorators.http import require_http_methods
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import F

from sunny_sports.sp.models import *
from sunny_sports.sp.models.association import *
from sunny_sports.sp.models.role import *
from sunny_sports.sp.models.models import *
from sunny_sports.sp.forms import *
from utils import *
from alipay_utils import alipay_payment

from sunny_sports.sp.tasks import payment_check
from django import forms
from datetime import datetime, timedelta
from PIL import Image
import os
from sunny_sports.settings import MEDIA_ROOT

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
    cts = CoachTrain.objects.filter(coach=coach)
    t_count = Train.objects.filter(level=coach.t_level+1, reg_status = 1).count()
    if len(cts):
        ct = cts.latest('id')
    else:
        ct = None
    print "t_count",t_count

    return render_to_response('coach/home.html',{"coach":coach, "ct":ct, "t_count":t_count}, RequestContext(req))

@login_required()
def train(req):
    uuid = req.user.id # 用这个id查信息哦
    coach = Coach.objects.get(property__user_id=uuid)

    old_cts = []
    ct = []
    trains = None
    if coach.t_level == 0:
        trains = Train.objects.filter(level=1, reg_status=1)
        ct = CoachTrain.objects.filter(coach=coach, train__level=1)
    elif coach.t_level == 1:
        old_ct = CoachTrain.objects.filter(coach=coach, train__level=1, status__gt=0)[0]
        old_cts.append(old_ct)
        ct = CoachTrain.objects.filter(coach=coach, train__level=2)
        trains = Train.objects.filter(level=2, reg_status=1)
    elif coach.t_level == 2:
        old_ct = CoachTrain.objects.filter(coach=coach, train__level=1, status__gt=0)[0]
        old_ct2 = CoachTrain.objects.filter(coach=coach, train__level=2, status__gt=0)[0]
        old_cts.append(old_ct)
        old_cts.append(old_ct2)
        trains = Train.objects.filter(level=3, reg_status=1)
        ct = CoachTrain.objects.filter(coach=coach, train__level=3)
    else:
        old_ct = CoachTrain.objects.filter(coach=coach, train__level=1, status__gt=0)[0]
        old_ct2 = CoachTrain.objects.filter(coach=coach, train__level=2, status__gt=0)[0]
        old_ct3 = CoachTrain.objects.filter(coach=coach, train__level=3, status__gt=0)[0]
        old_cts.append(old_ct)
        old_cts.append(old_ct2)
        old_cts.append(old_ct3)
    return render_to_response('coach/train.html',{"coach":coach, "trains":trains, "old_cts":old_cts, "ct":ct.latest("id") if len(ct) > 0 else None, "items":range(0,3) }, RequestContext(req))

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
        t_id = req.POST.get("t_id") 
        data = req.POST.copy()
        coach = Coach.objects.get(property__user_id=uuid)

        MyUser.objects.filter(id=uuid).update(phone=data.pop("phone")[0], email=data.pop("email")[0])
        cp = coach.property
        cp.name = data.get("name","")
        if data.has_key("sex"):
            cp.sex = int(data.get("sex"))
        if data.has_key("identity"):
            cp.identity = data.get("identity","")
        if data.has_key("birth"):
            cp.birth = data["birth"]
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
        except Exception,e:
            return JsonResponse({ 'success':False,'msg':'信息存储错误' })

        train = train=Train.objects.get(id=t_id)
        if train.cur_num < train.limit:
            ct = CoachTrain(coach=coach, train=train, status=1) #未缴费状态
            train.cur_num = F('cur_num') + 1
            try:
                train.save()
                ct.save()
            except Exception,e:
                return JsonResponse({ 'success':False,'msg':'信息存储错误' })
        else:
            return JsonResponse({ 'success':False,'msg':'报名人数已满' })
        #tomorrow = datetime.utcnow() + timedelta(days=1)
        #tomorrow = datetime.utcnow() + timedelta(minute=5)
        #payment_check.apply_async((ct.id,), eta=tomorrow) #24小时后进行check，若未缴费，取消

        return JsonResponse({ 'success':True })
        #return HttpResponseRedirect('/coach/train/payment?ct_id=%s'%ct.id)
    else:
        t_id = req.GET.get("t_id",0)
        train = Train.objects.get(id=t_id)
        coach = Coach.objects.get(property__user_id=uuid)
        club = Club.objects.filter()
        return render_to_response('coach/info_confirm.html',{"coach":coach, "club":club, "train":train}, RequestContext(req))

@login_required()
@transaction.atomic
def reg_cancel(req):
    """
    取消报名
    """
    if req.method == "POST":
        ct_id = req.POST.get("ct_id")
        #ct = CoachTrain.objects.filter(id=ct_id).update(status=0, train_cur_num=F('train_cur_num') - 1)
        ct = CoachTrain.objects.get(id=ct_id)
        ct.status = 0
        ct.train.cur_num = ct.train.cur_num - 1
        ct.train.save()
        ct.delete()
        #Train.objects.filter(id=ct.train.id).update(cur_num=F('cur_num') - 1)
        return JsonResponse({'success':True})
    return JsonResponse({'success':False})

@login_required()
@transaction.atomic
def payment(req):
    print req.method
    if req.method == "GET":
        ct_id = req.GET.get("ct_id")
        ct = CoachTrain.objects.get(id=ct_id)
        params = {  
                'subject'     :"快乐体操教练培训费用",  
                'body'        :"快乐体操教练培训费用",  
                'total_fee'   :ct.train.money  
                }  
        ct.status = 2
        ct.save()
        print "支付成功"
        return redirect("/coach/train")
        #rlt = alipay_payment(ct_id, params)
        #if rlt == 'success':  
        #    ct.status = 2
        #    ct.save()
        #else:
        #    pass
    else:
        pass


@login_required()
@transaction.atomic
def update_info(req):
    """
    个人中心，用户更新基本信息
    """
    if req.method == "POST":
        data = req.POST.copy()

        uuid = req.user.id
        ur = UserRole.objects.get(user_id=uuid, role_id=3)
        ur.is_first = False
        if data.has_key("nickname"):
            MyUser.objects.filter(id=uuid).update(nickname=data.pop("nickname")[0], phone=data.pop("phone")[0], email=data.pop("email")[0])
        else:
            MyUser.objects.filter(id=uuid).update(phone=data.pop("phone")[0], email=data.pop("email")[0])

        cp = CoachProperty.objects.get(user_id=uuid)
        cp.name = data.get("name","")
        if data.has_key("sex"):
            cp.sex = int(data.get("sex"))
        if data.has_key("identity"):
            cp.identity = data.get("identity","")
        if data.has_key('birth'):
            cp.birth = data.get("birth")
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
        except Exception,e:
            print e
            return JsonResponse({'success':False})
        return JsonResponse({'success':True})


@login_required()
@transaction.atomic
def update_img(request):
    uuid = request.user.id
    coach = Coach.objects.get(property__user_id=uuid)
    if request.method == "POST":
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
            headImg = uf.cleaned_data['headImg']
            temp = coach.property.avatar
            coach.property.avatar = headImg
            coach.property.save()
            path = coach.property.avatar.name
            suffix = path.split('.')[1];
            if suffix == "jpg" or suffix=="jpeg" or suffix=="gif" or suffix=="png" or suffix =="bmp":
                imgpath = os.path.join(MEDIA_ROOT,path)
                im = Image.open(imgpath)
                new_img=im.resize((200,200),Image.ANTIALIAS)
                new_img.save(imgpath)
            else:
                coach.property.avatar = temp
                coach.property.save()
    
    return HttpResponseRedirect('/coach/center')
