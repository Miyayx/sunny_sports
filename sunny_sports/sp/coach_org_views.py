
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.http import require_http_methods
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import F

from sunny_sports.sp.models import *
from sunny_sports.sp.models.association import *
from sunny_sports.sp.models.role import *
from sunny_sports.sp.models.models import *
from sunny_sports.sp.models.status import *
from sunny_sports.sp.forms import *

from convert import *

@login_required()
def coach_org(req):
    return HttpResponseRedirect("coach_org/home")

@login_required()
def home(req):
    uuid = req.user.id
    # 用这个id查信息哦
    print uuid
    coachorg = CoachOrg.objects.get(user_id=uuid)
    opentrains = Train.objects.filter(org=coachorg, pub_status=0).order_by('train_stime')
    endtrains = Train.objects.filter(org=coachorg, pub_status=1).order_by('train_stime')
    return render_to_response('coach_org/home.html',{"coachorg":coachorg,"opentrains":opentrains, "endtrains":endtrains[:5]} ,RequestContext(req))

@login_required()
def train(req):
    uuid = req.user.id
    if req.method == "GET":
        train_id = req.GET.get("t_id",None)
        if train_id and len(train_id) > 0: #有编号的话就返回对应课程的人名单
            c_t = CoachTrain.objects.filter(train_id=train_id, train__pub_status=1)
            if len(c_t) > 0:
                train = c_t[0].train
                return render_to_response('centre/history_view2.html',{"c_t":c_t, "train":train, "base":"./coach_org/base.html"}, RequestContext(req))
            else:
                return HttpResponse("<h2>没有该课程的历史信息</h2>")
        else:#否则返回课程列表
            endtrains = Train.objects.filter(org__user_id=uuid, pub_status=1).order_by('train_stime')
            return render_to_response('coach_org/train_query.html',{"coachorgtrains":endtrains}, RequestContext(req))

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
def train_manage(req):
    if req.method == "POST":
        pass
    else:
        uuid = req.user.id
        # 用这个id查信息哦
        print uuid
        opentrains = Train.objects.filter(org__user_id=uuid, pub_status=0).order_by('-train_stime')
        coachtrains = [CoachTrain.objects.filter(train=t, status__gt=0) for t in opentrains]
        return render_to_response('coach_org/train_manage.html',{"zipped":zip(opentrains, coachtrains)}, RequestContext(req))

@login_required()
@transaction.atomic
def score_input(req):
    if req.method == "POST":
        data = req.POST.copy()
        print data
        submit = int(data.pop("submit")[0])
        t_id = data.pop("t_id")[0]
        cts = CoachTrain.objects.filter(train_id=t_id)
        for ct in cts:
            print data[str(int(ct.number))]
            print "status",str2bool(data[str(int(ct.number))])
            ct.status = str2bool(data[str(int(ct.number))])
            ct.save()
        #cts.update(status=str2bool(data[str(int(F('number')))]))
        
        if submit:
            cts[0].train.sub_status=1
            cts[0].train.save()
        return JsonResponse({"success":True})

        
@login_required()
@transaction.atomic
def update_info(req):
    """
    个人中心，用户更新基本信息
    """
    if req.method == "POST":
        data = req.POST.copy()
        uuid = req.user.id
        MyUser.objects.filter(id=uuid).update(phone=data.pop("phone")[0], email=data.pop("email")[0])
        co = CoachOrg.objects.get(user_id=uuid)
        if data.has_key("orgname"):
            co.name = data["orgname"]
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
