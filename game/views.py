#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from payment.models import Bill
from payment.views import pay as ali_pay
from payment.views import pay_method 
from payment.alipay_python.alipay import *

from sunny_sports.settings import HOST
from sunny_sports.settings import PAYMENT_LIMIT

from sp.g_import import *
from sp.models.status import get_role
from game.models import *
from student.models import *

@login_required()
@user_passes_test(lambda u: u.is_role(['group','club']))
def find_stu(req, phone):
    print "phone-->"+phone
    try:
        s = Student.objects.get(property__user__phone=phone)
        if len(StudentTeam.objects.filter(student=s, team__game__pub_status=0)) > 0: #该学生已报名其他队
            return JsonResponse({'success':False})
        return JsonResponse({'uuid':s.property.user.id, 'name':s.property.name, 'gender':s.property.get_sex_display(), 'success':True})
    except Exception,e:
        print e
        return JsonResponse({})

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['group','club']))
def edit_member(req):
    if req.method == "POST":
        st_id = req.POST['st_id'].strip()
        phone = req.POST['phone'].strip()
        try:
            s = Student.objects.get(property__user__phone=phone)
            if len(StudentTeam.objects.filter(student=s, team__game__pub_status=0)) > 0: 
                return JsonResponse({'success':False})
            else:
                StudentTeam.objects.filter(id=st_id).update(student=s)
                return JsonResponse({'st_id':st_id, 'name':s.property.name, 'gender':s.property.get_sex_display(), 'success':True})
        except Exception,e:
            print e
            return JsonResponse({})

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['group','club']))
def add_member(req):
    if req.method == "POST":
        phone = req.POST['phone'].strip()
        t_id = req.POST['team'].strip()
        try:
            s = Student.objects.get(property__user__phone=phone)
            if len(StudentTeam.objects.filter(student=s, team__game__pub_status=0)) > 0: 
                return JsonResponse({'success':False, 'msg':'该学员已报名比赛'})
            else:
                t = Team.objects.get(id=t_id)
                StudentTeam.objects.create(student=s, team=t )
                return JsonResponse({'success':True})
        except Exception,e:
            print e 
            return JsonResponse({'success':False, 'msg':'未找到相应学员'})

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['group','club']))
def del_member(req):
    if req.method == "POST":
        st_id = req.POST['st_id'].strip()
        try:
            StudentTeam.objects.filter(id=st_id).delete() 
            return JsonResponse({'success':True})
        except Exception,e:
            print e
            return JsonResponse({})

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['group','club','game_org']))
def reg_cancel(req):
    """
    取消报名
    """
    if req.method == "POST":
        t_id = req.POST.get("t_id")
        t = Team.objects.get(id=t_id)
        t.delete()
        return JsonResponse({'success':True})
    return JsonResponse({'success':False})


@login_required()
@user_passes_test(lambda u: u.is_role(['group','club']))
def current_game(req, g_id, t_id, ROLE_ID):
    role = get_role(ROLE_ID)
    if not g_id: #显示game list
        games = Game.objects.filter(pass_status=1, reg_status__lt=2, game_status=0, pub_status=0) #报名的比赛
        for g in games: #报名的比赛
            g.cur_num = len(Team.objects.filter(game=g))
        #与自己相关的进行中比赛
        ur = UserRole.objects.get(user=req.user, role_id=ROLE_ID)
        teams = Team.objects.filter(contestant=ur, game__pub_status=0)
        return render_to_response('game/group_gamelist.html',{'base':'./%s/base.html'%role, 'role':role,  "games":games, "teams":teams}, RequestContext(req))
    elif g_id and not t_id: #显示单个game状况
        game = Game.objects.get(id=g_id)
        game.cur_num = len(Team.objects.filter(game=game))
        #events = Event.objects.filter(id__in=game.events.split(','))#项目列表
        events = Event.objects.all()
        return render_to_response('game/single_game.html',{'base':'./%s/base.html'%role, 'role':role, 'game':game, 'events':events}, RequestContext(req))
    else:
        time_remain = 0
        team = Team.objects.get(id=t_id)
        sts = StudentTeam.objects.filter(team=team)
        print "sts len:",len(sts)
        tes = TeamEvent.objects.filter(team=team)
        if team.pay_status == 0:
            time_remain = team.reg_time+PAYMENT_LIMIT-timezone.now()
            print 'time_remain',time_remain
            time_remain = int(time_remain.total_seconds())
        return render_to_response('game/single_game.html',{'base':'./%s/base.html'%role, 'game':team.game, 'team':team, 'sts':sts, 'tes':tes, 'time_remain':time_remain, 'role':role}, RequestContext(req))

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
                'return_url'  :"http://%s/game/pay_return"%req.META['HTTP_HOST'],
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
                t = Team.objects.get(id=tn[14:])
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
                t = Team.objects.get(id=tn[14:])
                t.pay_status = 1
                t.save()
                print '付款成功！'
            except:
            #return HttpResponse(u'付款成功！')
                return HttpResponse(u'找不到报名信息！若已付款，请联系网络平台负责人')
            return HttpResponseRedirect('/%s/cur_game'%t.contestant.role.get_role_display())
        else:
            return HttpResponse(u'付款失败')
    else:
        return HttpResponse(u'信息验证错误')



