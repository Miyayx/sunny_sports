# -*- coding:utf-8 -*-

from g_import import *
from sp.models.status import ID_TYPES

from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db import transaction
from django import forms

import os
from utils import *
from payment.models import Bill
from payment.views import pay as ali_pay
from payment.views import pay_method 
from payment.alipay_python.alipay import *

#from photo.views import update_photo
from photo.views import update_photo_in_qiniu

from sp.tasks import payment_check

from datetime import datetime, timedelta
from sunny_sports.settings import HOST, PAYMENT_LIMIT, PHOTO_ROOT

@login_required()
@user_passes_test(lambda u: u.is_role(['coach']))
def coach(req):
    uuid = req.user.id
    u=UserRole.objects.get(user_id=uuid, role_id=3)
    req.session['role'] = 3
    if u.is_first:
        messages.error(req, u"请补全个人信息")
        return HttpResponseRedirect("coach/center")
    else:
        return HttpResponseRedirect("coach/home")

@login_required()
@user_passes_test(lambda u: u.is_role(['coach']))
def home(req):
    uuid = req.user.id
    # 用这个id查信息哦
    print uuid
    coach = Coach.objects.get(property__user_id=uuid)
    coach.property.age = calculate_age(coach.property.birth) 
    cts = CoachTrain.objects.filter(coach=coach, train__pub_status=0, train__level=coach.t_level+1)
    sct = CoachTrain.objects.filter(coach=coach, train__pub_status=0, train__level=TRAIN_LEVEL.SEED)
    t_count = Train.objects.filter(level=coach.t_level+1, pass_status=1, reg_status=1, pub_status=0).count()
    if len(cts):
        ct = cts.latest('id')
    else:
        ct = None
    if len(sct):
        sct = sct[0]
    else:
        sct = None

    return render_to_response('coach/home.html',{"coach":coach, "ct":ct, "sct":sct, "t_count":t_count, "PHOTO_ROOT":PHOTO_ROOT}, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['coach']))
def train(req):
    uuid = req.user.id # 用这个id查信息哦
    coach = Coach.objects.get(property__user_id=uuid)

    old_cts = []
    ct = []
    trains = None
    time_remain = 0
    if coach.t_level == 0:
        trains = Train.objects.filter(level=1, pass_status=1, reg_status=1, pub_status=0)
        ct = CoachTrain.objects.filter(coach=coach, train__level=1, train__pub_status=0)
    elif coach.t_level == 1:
        old_ct = CoachTrain.objects.filter(coach=coach, train__level=1, status__gt=0).latest('id')
        old_cts.append(old_ct)
        ct = CoachTrain.objects.filter(coach=coach, train__level=2, train__pub_status=0)
        trains = Train.objects.filter(level=2, pass_status=1, reg_status=1, pub_status=0)
    elif coach.t_level == 2:
        old_ct = CoachTrain.objects.filter(coach=coach, train__level=1, status__gt=0).latest('id')
        old_ct2 = CoachTrain.objects.filter(coach=coach, train__level=2, status__gt=0).latest('id')
        old_cts.append(old_ct)
        old_cts.append(old_ct2)
        trains = Train.objects.filter(level=3, pass_status=1, reg_status=1, pub_status=0)
        ct = CoachTrain.objects.filter(coach=coach, train__level=3, train__pub_status=0)
    else:
        old_ct = CoachTrain.objects.filter(coach=coach, train__level=1, status__gt=0).latest('id')
        old_ct2 = CoachTrain.objects.filter(coach=coach, train__level=2, status__gt=0).latest('id')
        old_ct3 = CoachTrain.objects.filter(coach=coach, train__level=3, status__gt=0).latest('id')
        old_cts.append(old_ct)
        old_cts.append(old_ct2)
        old_cts.append(old_ct3)

    if len(ct): 
        temp = ct.latest('id')
        if temp.status == 0:
            time_remain = temp.reg_time+PAYMENT_LIMIT-timezone.now()
    print 'time_remain',time_remain

    return render_to_response('coach/train.html',{"coach":coach, 
        "trains":trains, 
        "old_cts":old_cts, 
        "ct":ct.latest("id") if len(ct) > 0 else None,
        "items":range(0,3), 
        "time_remain":int(time_remain.total_seconds()) if time_remain else 0
        }, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['coach']))
def strain(req): #辅导员页面
    uuid = req.user.id # 用这个id查信息哦
    coach = Coach.objects.get(property__user_id=uuid)

    old_ct = None
    ct = []
    trains = None
    time_remain = 0
    if coach.is_seed:
        old_ct = CoachTrain.objects.filter(coach=coach, train__level=TRAIN_LEVEL.SEED, status__gt=0).latest('id')
    else:
        trains = Train.objects.filter(level=TRAIN_LEVEL.SEED, pass_status=1, reg_status=1, pub_status=0)
        ct = CoachTrain.objects.filter(coach=coach, train__level=TRAIN_LEVEL.SEED, train__pub_status=0)

    print trains
    print ct

    if len(ct): 
        temp = ct.latest('id')
        if temp.status == 0:
            time_remain = temp.reg_time+PAYMENT_LIMIT-timezone.now()
    print 'time_remain',time_remain

    return render_to_response('coach/seed_train.html',{"coach":coach, 
        "trains":trains, 
        "old_ct":old_ct, 
        "ct":ct.latest("id") if len(ct) > 0 else None,
        "time_remain":int(time_remain.total_seconds()) if time_remain else 0
        }, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['coach']))
def center(req):
    uuid = req.user.id
    # 用这个id查信息哦
    u = UserRole.objects.get(user_id=uuid, role_id=3)
    if u.is_first:
        messages.error(req, u"请补全个人信息")
    coach = Coach.objects.filter(property__user_id=uuid)
    club = Club.objects.filter()
    return render_to_response('coach/center.html',{"coach":coach[0], "club":club, "ID_TYPES":ID_TYPES, "PHOTO_ROOT":PHOTO_ROOT}, RequestContext(req))

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['coach']))
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
            try:
                ct = CoachTrain.objects.get(coach=coach, train=train)
                return JsonResponse({'success':False, 'msg':'已报名'})
            except:
                pass
            try:
                ct = CoachTrain.objects.create_ct(coach=coach, train=train) #要用create_ct创建CoachTrain，否则报名数量不增加
                check_time = datetime.utcnow() + PAYMENT_LIMIT
                payment_check.apply_async((ct.id,), eta=check_time) #24小时后进行check，若未缴费，删除报名记录

                return JsonResponse({ 'success':True,'ct_id':ct.id })
            except Exception,e:
                print e
                return JsonResponse({ 'success':False,'msg':'信息存储错误' })
        else:
            return JsonResponse({ 'success':False,'msg':'报名人数已满' })
    else:
        t_id = req.GET.get("t_id",0)
        train = Train.objects.get(id=t_id)
        coach = Coach.objects.get(property__user_id=uuid)
        club = Club.objects.filter()
        return render_to_response('coach/info_confirm.html',{"coach":coach, "club":club, "train":train, "return_page":"/coach/strain" if train.level == TRAIN_LEVEL.SEED else "/coach/train"}, RequestContext(req))

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['coach']))
def reg_cancel(req):
    """
    取消报名
    """
    if req.method == "POST":
        ct_id = req.POST.get("ct_id")
        ct = CoachTrain.objects.get(id=ct_id)
        ct.delete()
        return JsonResponse({'success':True})
    return JsonResponse({'success':False})

@login_required()
@transaction.atomic
@csrf_exempt
@user_passes_test(lambda u: u.is_role(['coach']))
def pay(req):
    if req.method == "POST":
        ct_id = req.POST.get("order_num")
        ct = CoachTrain.objects.get(id=ct_id, status=0)
        URL = 'coach/strain' if ct.train.level == TRAIN_LEVEL.SEED else 'coach/strain'
        method = req.POST.get("channelToken")
        params = {  
                'subject'     :u"快乐体操教练培训费用",  
                'body'        :u"快乐体操教练培训费用 培训课程:%s, 培训编号:%s"%(ct.train.name, ct.train.id),
                'total_fee'   :ct.train.money,
                'return_url'  :"http://%s/%s/pay_return"%(HOST, URL),
                'notify_url'  :"http://%s/%s/pay_notify"%(HOST, URL),
                'order_num'   :ct_id,#用来生成账单编号
                'org_email'   :ct.train.org.ali_email,#分润给组织机构
                'comment'     :u"快乐体操教练培训费用 培训课程:%s, 培训编号:%s, t_id:%s, ct_id:%s"%(ct.train.name, ct.train.id, ct.train.id, ct.id)#给组织机构的备注
                }  
        if not 'alipay' == method:
            params['bank'] = method
        url, bill = ali_pay(req, 0, params)
        ct.bill = bill
        ct.save()
        print "reg time:", ct.reg_time
        return HttpResponseRedirect(url)
        #return JsonResponse({'success':True,'url':url})
    else: #GET return pay_method page
        ct_id = req.GET.get("ct_id")
        ct = CoachTrain.objects.get(id=ct_id, status=0)
        params = {  
                'subject'     :u"快乐体操教练培训费用",  
                'body'        :u"快乐体操教练培训费用 培训课程:%s, 培训编号:%s"%(ct.train.name, ct.train.id),
                'total_fee'   :ct.train.money,
                'receiver'    :u"北京快乐童年阳光体操文化发展有限责任公司",
                'order_num'   :ct_id,
                'bill_type'   :0,
                }  
        print "reg time:", ct.reg_time
        return pay_method(req, params)

@csrf_exempt
def pay_notify(req):
    #if req.GET.get('trade_status') == "TRADE_SUCCESS":
    print "notify"
    print "out_trade_no:",req.POST.get('out_trade_no')
    if notify_verify(req.POST):
        tn = req.POST.get('out_trade_no')
        trade_status = req.POST.get('trade_status')
        bill = Bill.objects.get(no=tn)
        bill.trade_status = trade_status
        bill.save()

        if trade_status == 'WAIT_SELLER_SEND_GOODS' or trade_status == "TRADE_SUCCESS":
            print ('TRADE SUCCESS, so upgrade bill')
            try:
                #ct = CoachTrain.objects.get(bill_id=tn)
                ct = CoachTrain.objects.get(id=int(tn[14:]))
                ct.status = 1
                ct.save()
                print '付款成功！'
            except:
                return HttpResponse("fail")
            return HttpResponse("success")
        else:
            return HttpResponse("success")
    else:
        return HttpResponse('fail')

@login_required()
@user_passes_test(lambda u: u.is_role(['coach']))
def pay_return(req):
    print "return"
    if notify_verify(req.GET):
        tn = req.GET.get('out_trade_no')
        trade_status = req.GET.get('trade_status')
        print 'out_trade_no:',tn
        bill = Bill.objects.get(no=tn)
        bill.trade_status = trade_status
        bill.save()
        redirect_url = '/coach/train'
        if trade_status == 'WAIT_SELLER_SEND_GOODS' or trade_status == "TRADE_SUCCESS":
            try:
                #ct = CoachTrain.objects.get(bill_id=tn)
                ct = CoachTrain.objects.get(id=int(tn[14:]))
                ct.status = 1
                ct.save()
                if ct.train.level == TRAIN_LEVEL.SEED:
                    redirect_url = '/coach/strain'
                print '付款成功！'
            except:
            #return HttpResponse(u'付款成功！')
                return HttpResponse(u'找不到报名信息！若已付款，请联系网络平台负责人')
            return HttpResponseRedirect(redirect_url)
        else:
            return HttpResponse(u'付款失败')
    else:
        return HttpResponse(u'信息验证错误')


@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['coach']))
def update_info(req):
    """
    个人中心，用户更新基本信息
    """
    if req.method == "POST":
        data = req.POST.copy()

        uuid = req.user.id
        ur = UserRole.objects.get(user_id=uuid, role_id=3)
        ur.is_first = False
        if data.has_key("nickname") and len(data["nickname"].strip()):
            MyUser.objects.filter(id=uuid).update(nickname=data.pop("nickname")[0], phone=data.pop("phone")[0], email=data.pop("email")[0])
        else:
            MyUser.objects.filter(id=uuid).update(phone=data.pop("phone")[0], email=data.pop("email")[0])

        cp = CoachProperty.objects.get(user_id=uuid)
        cp.name = data.get("name","")
        if data.has_key("sex"):
            cp.sex = int(data.get("sex"))
        cp.id_type = int(data["id_type"])
        if cp.id_type == 0 and data.has_key("identity"):
            cp.identity = data.get("identity","")
        if cp.id_type == 1 and data.has_key("passport"):
            cp.identity = data.get("passport","")
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
@user_passes_test(lambda u: u.is_role(['coach']))
def update_img(req):
    uuid = req.user.id
    coach = Coach.objects.get(property__user_id=uuid)
    #update_photo(req, coach.property)
    update_photo_in_qiniu(req, coach.property)
    return HttpResponseRedirect('/coach/center')
