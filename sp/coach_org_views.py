
# -*- coding:utf-8 -*-

from g_import import *

from django.core.context_processors import csrf

from sp.tasks import *

from datetime import datetime, timedelta

from convert import *

@login_required()
@user_passes_test(lambda u: u.is_role(['coach_org']))
def coach_org(req):
    return HttpResponseRedirect("coach_org/home")

@login_required()
@user_passes_test(lambda u: u.is_role(['coach_org']))
def home(req):
    uuid = req.user.id
    # 用这个id查信息哦
    print uuid
    coachorg = CoachOrg.objects.get(user_id=uuid)
    opentrains = Train.objects.filter(org=coachorg, pub_status=0).order_by('-train_stime')#按培训开始时间排序
    endtrains = Train.objects.filter(org=coachorg, pub_status=1).order_by('-train_stime')#按培训开始时间排序
    return render_to_response('coach_org/home.html',{"coachorg":coachorg,"opentrains":opentrains, "endtrains":endtrains[:5]} ,RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['coach_org']))
def train(req):
    """
    历史培训查看
    """
    uuid = req.user.id
    if req.method == "GET":
        train_id = req.GET.get("t_id",None)
        if train_id and len(train_id) > 0: #有编号的话就返回对应培训的人名单
            c_t = CoachTrain.objects.filter(train_id=train_id, train__pub_status=1)
            if len(c_t) > 0:
                train = c_t[0].train
                return render_to_response('centre/history_view2.html',{"c_t":c_t, "train":train, "base":"./coach_org/base.html"}, RequestContext(req))
            else:
                return HttpResponse("<h2>没有该培训的历史信息</h2>")
        else:#否则返回培训列表
            endtrains = Train.objects.filter(org__user_id=uuid, pub_status=1).order_by('-train_stime')#按培训开始时间排序
            return render_to_response('coach_org/train_query.html',{"coachorgtrains":endtrains}, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['coach_org']))
def center(req):
    uuid = req.user.id
    # 用这个id查信息哦
    coach_org = CoachOrg.objects.filter(user_id=uuid)
    return render_to_response('coach_org/center.html',{"coachorg":coach_org[0]},RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['coach_org']))
def train_publish(req):
    if req.method == "POST":
        data = req.POST.copy()
        uuid = req.user.id
        t_id = data.get('t_id',0)
        if t_id: #update train
            train = Train.objects.get(id=t_id)
            data['address'] = train.address
            data['org'] = train.org.id
            data.pop('t_id')
            data['level'] = int(data['level'])
            data['money'] = int(data['money'])
            data['limit'] = int(data['limit'])
            tform = TrainPublishForm(data, instance=train)
        else: # create new train
            org = CoachOrg.objects.get(user_id=uuid)
            data['org'] = org.id
            data['address'] = data.get('prov','')+data.get('city','')+data.get('dist','')+data.get('addr','')
            data['level'] = int(data['level'])
            data['money'] = int(data['money'])
            data['limit'] = int(data['limit'])
            tform = TrainPublishForm(data)
        
        if tform.is_valid():
            t = tform.save()
            #启动计时器
            train_reg_start.apply_async((t.id,), eta=t.reg_stime+timedelta(seconds=3))
            train_reg_end.apply_async((t.id,), eta=t.reg_etime+timedelta(seconds=3))
            train_start.apply_async((t.id,), eta=t.train_stime+timedelta(seconds=3))
            train_end.apply_async((t.id,), eta=t.train_etime+timedelta(seconds=3))
            return JsonResponse({'success':True})
        else:
            print tform.errors
            return JsonResponse({'success':False })
        
    else:
        t_id = req.GET.get('t_id',0)
        t = None
        if t_id :
            t = Train.objects.get(id=t_id)
        uuid = req.user.id
        org = CoachOrg.objects.get(user_id=uuid)
        return render_to_response('coach_org/train_publish.html',{'level':TRAIN_LEVEL,'org':org, 'train': t }, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['coach_org']))
def train_manage(req):
    uuid = req.user.id
    opentrains = Train.objects.filter(org__user_id=uuid, pub_status=0).order_by('-train_stime')#按培训开始时间排序
    coachtrains = [CoachTrain.objects.filter(train=t, status__gt=0) for t in opentrains]
    return render_to_response('coach_org/train_manage.html',{"zipped":zip(opentrains, coachtrains)}, RequestContext(req))

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['coach_org']))
def score_input(req):
    if req.method == "POST":
        data = req.POST.copy()
        print data
        submit = int(data.pop("submit")[0])
        t_id = data.pop("t_id")[0]
        cts = CoachTrain.objects.filter(train_id=t_id, status__gt=0)
        for ct in cts:
            print data[str(int(ct.number))]
            print "status",str2bool(data[str(int(ct.number))])
            ct.pass_status = str2bool(data[str(int(ct.number))])
            ct.save()
        
        if submit:
            cts[0].train.sub_status=1
            cts[0].train.save()
        return JsonResponse({"success":True})

        
@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['coach_org']))
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

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['coach_org']))
def add_member(req):
    if req.method == "GET":
        phone = req.GET.get("phone")
        print phone
        c = Coach.objects.filter(property__user__phone=phone)
        if len(c) > 0:
            return JsonResponse({"name":c[0].property.name })
        else:
            return JsonResponse({"name":None})

    else:
        phone = req.POST.get("phone")
        name = req.POST.get("name")
        t_id = req.POST.get("t_id")
        print t_id
        c = Coach.objects.filter(property__user__phone=phone, property__name=name)
        if len(c) > 0:
            c = c[0]
            ct = CoachTrain.objects.create(coach=c, train=Train.objects.get(id=t_id), status=2)
            ct.train.cur_num = ct.train.cur_num + 1
            ct.train.save()
            ct.save()
            return JsonResponse({'success':True})
        else:
            return JsonResponse({'success':False})

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['coach_org']))
def del_member(req):

    if req.method == "POST":
        ct_id = req.POST.get("ct_id")
        ct = CoachTrain.objects.get(id=ct_id)
        ct.train.cur_num = ct.train.cur_num - 1
        ct.train.save()
        ct.delete()
        return JsonResponse({'success':True})
    else:
        return JsonResponse({'success':False})
