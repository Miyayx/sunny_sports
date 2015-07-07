#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from sp.g_import import *

from payment.models import Bill
from payment.views import pay as ali_pay
from payment.views import pay_method 
from payment.alipay_python.alipay import *

from sunny_sports.settings import HOST
from sunny_sports.settings import PAYMENT_LIMIT

from game.models import *

@login_required()
@transaction.atomic
@csrf_exempt
@user_passes_test(lambda u: u.is_role(['group','club']))
def pay(req, t_id=None):
    if req.method == "POST":
        t_id = req.POST.get("order_num")
        team = Team.objects.get(id=t_id, pay_status=0)
        mem = len(StudentTeam.objects.filter(team=team)) #报名人数
        method = req.POST.get("channelToken")
        params = {  
                'subject'     :u"%s报名费用"%(team.game.name),  
                'body'        :u"%s报名费用 参赛队:%s 参赛人数:%d"%(team.game.name, team.name, mem),
                'total_fee'   :team.game.money*mem,
                'return_url'  :"http://%s/game/pay_return"%HOST,
                'notify_url'  :"http://%s/game/pay_notify"%HOST,
                'order_num'   :t_id,#用来生成账单编号
                'org_email'   :team.game.org.ali_email,#分润给组织机构
                'comment'     :u"%s报名费用 参赛队:%s 参赛队编号:%s 参赛人数:%d"%(team.game.name, team.name, team.id, mem)#给组织机构的备注
                }  
        if not 'alipay' == method:
            params['bank'] = method
        url, bill = ali_pay(req, 0, params)
        team.bill = bill
        team.save()
        print "reg time:", team.reg_time
        return HttpResponseRedirect(url)
    else: #GET return pay_method page
        team = Team.objects.get(id=t_id, pay_status=0)
        mem = len(StudentTeam.objects.filter(team=team)) #报名人数
        params = {  
                'subject'     :u"%s报名费用"%(team.game.name),  
                'body'        :u"%s报名费用  参赛队:%s  参赛人数:%d"%(team.game.name, team.name, mem),
                'total_fee'   :team.game.money*mem,
                'receiver'    :u"北京快乐童年阳光体操文化发展有限责任公司",
                'order_num'   :t_id,
                'bill_type'   :1, #比赛费用， 0是培训费用
                }  
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
                t = Team.objects.get(id=int(tn[14:]))
                t.pay_status = 1
                t.save()
                print '付款成功！'
            except:
                return HttpResponse("fail")
            return HttpResponse("success")
        else:
            return HttpResponse("success")
    else:
        return HttpResponse('fail')

@login_required()
@user_passes_test(lambda u: u.is_role(['group','club']))
def pay_return(req):
    print "return"
    if notify_verify(req.GET):
        tn = req.GET.get('out_trade_no')
        trade_status = req.GET.get('trade_status')
        print 'out_trade_no:',tn
        bill = Bill.objects.get(no=tn)
        bill.trade_status = trade_status
        bill.save()
        if trade_status == 'WAIT_SELLER_SEND_GOODS' or trade_status == "TRADE_SUCCESS":
            t = None
            try:
                #ct = CoachTrain.objects.get(bill_id=tn)
                t = Team.objects.get(id=int(tn[14:]))
                t.pay_status = 1
                t.save()
                print '付款成功！'
            except:
            #return HttpResponse(u'付款成功！')
                return HttpResponse(u'找不到报名信息！若已付款，请联系网络平台负责人')
            return HttpResponseRedirect('/%s/cur_game'%t.contestant.get_role_display())
        else:
            return HttpResponse(u'付款失败')
    else:
        return HttpResponse(u'信息验证错误')



