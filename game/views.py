#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils import timezone

from payment.models import Bill
from payment.views import pay as ali_pay
from payment.views import pay_method 
from payment.alipay_python.alipay import *

from sunny_sports.settings import HOST
from sunny_sports.settings import PAYMENT_LIMIT
from sunny_sports.settings import PHOTO_ROOT

from sp.g_import import *
from sp.models.status import get_role
from game.models import *
from student.models import *
from forms import *
from game.tasks import *
from group.models import *
from club.models import *

@login_required()
@user_passes_test(lambda u: u.is_role(['group','club']))
def find_stu(req, phone, gender=None):
    print "phone-->"+phone
    try:
        s = None
        if gender == None:
            s = Student.objects.get(property__user__phone=phone)
        elif int(gender) == 0:
            s = Student.objects.get(property__user__phone=phone, property__sex=0)
        elif int(gender) == 1:
            s = Student.objects.get(property__user__phone=phone, property__sex=1)

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
        games = Game.objects.filter(pass_status=1, reg_status=1, game_status=0, pub_status=0) #可报名的比赛
        for g in games: #报名的比赛
            g.cur_num = len(Team.objects.filter(game=g))
        #与自己相关的进行中比赛
        ur = UserRole.objects.get(user=req.user, role_id=ROLE_ID)
        teams = Team.objects.filter(contestant=ur, game__pub_status=0)
        games = list(games)
        for t in teams: #剔除已报名的
            games.remove(t.game)
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
@user_passes_test(lambda u: u.is_role(['group', 'club']))
def history_game(req, g_id, ROLE_ID):
    role = get_role(ROLE_ID)
    if req.method == "GET":
        if g_id and len(g_id) > 0: #有编号的话就返回对应比赛信息
            game = Game.objects.get(id=g_id)
            try:
                ur = UserRole.objects.get(user=req.user, role_id=ROLE_ID)
                team = Team.objects.get(game=game, contestant=ur)
                sts = StudentTeam.objects.filter(team=team)
                tes = TeamEvent.objects.filter(team=team)
            except Exception,e:
                print e
                team = None
                sts = None
                tes = None

            return render_to_response('game/single_game.html',{'base':'./%s/base.html'%role, 'game':game, 'team':team, 'sts':sts, 'tes':tes, 'role':role}, RequestContext(req))
        else:#否则返回历史比赛列表
            uuid = req.user.id
            teams = Team.objects.filter(contestant__user=req.user, contestant__role_id=ROLE_ID, game__pub_status=1)
            return render_to_response('game/history_team.html', {"teams":teams, "base":"./%s/base.html"%role, "role":role}, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['group','club']))
@transaction.atomic
def game_apply(req, g_id, ROLE_ID):
    """
    报名，创建参赛队
    """
    if req.method == "POST":
        data = req.POST.copy()
        uuid = req.user.id
        # create new team
        members = data.pop('member')[0]
        data['contestant'] = UserRole.objects.get(user=req.user, role_id=ROLE_ID).id
        if len(Team.objects.filter(game_id=data['game'], contestant_id=data['contestant'])):
            return JsonResponse({'success':False, 'msg':'您已报名该比赛' })
        if len(Team.objects.filter(game_id=data['game'])) >= Game.objects.get(id=data['game']):
            return JsonResponse({'success':False, 'msg':'参赛队已报满' })

        tform = TeamForm(data)
        if tform.is_valid():
            t = tform.save()
            ms = members.strip().split(',')
            print len(ms)
            print len(set(ms))
            if not len(ms) == len(set(ms)):
                return JsonResponse({'success':False, 'msg':'队员有重复' })
            #stus = Student.objects.filter(property__user__id__in=ms)
            stus = Student.objects.filter(property__user__phone__in=ms)
            boys = 0
            girls = 0
            game = Game.objects.get(id=g_id)
            for s in stus:
                if s.property.sex == 0:
                    boys += 1
                else:
                    girls += 1
            if not boys == game.male_num or not girls == game.female_num:
                return JsonResponse({'success':False, 'msg':'队员数量不符'})

            sts = []
            for s in stus:
                StudentTeam.objects.get_or_create(student=s, team=t)

                #sts.append(StudentTeam(student=s, team=t))
            #StudentTeam.objects.bulk_create(sts)

            tes = []
            for e in Event.objects.all():
                TeamEvent.objects.get_or_create(event=e, team=t)
                #tes.append(TeamEvent(event=e, team=t))
            #TeamEvent.objects.bulk_create(tes)

            check_time = timezone.now() + PAYMENT_LIMIT
            payment_check.apply_async((t.id,), eta=check_time) #24小时后进行check，若未缴费，删除报名记录

            return JsonResponse({'success':True, 't_id':t.id})
        else:
            print tform.errors
            return JsonResponse({'success':False, 'msg':str(tform.errors) })

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

@login_required()
def team_info(req, t_id):
    if t_id and len(t_id) > 0: #有编号的话就返回对应比赛信息
        try:
            team = Team.objects.get(id=t_id)
            group = None
            if team.contestant.role.get_role_display() == "group":
                group = Group.objects.get(user=team.contestant.user)
            elif team.contestant.role.get_role_display() == "club":
                group = Club.objects.get(user=team.contestant.user)

            return render_to_response('common/team_info.html', {"team":team, "group": group, "PHOTO_ROOT":PHOTO_ROOT}, RequestContext(req))
        except Exception,e:
            print e
            return HttpResponse(u"该参赛队不存在")
    return HttpResponse(u"该参赛队不存在")



