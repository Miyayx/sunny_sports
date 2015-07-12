# -*- coding:utf-8 -*-
from g_import import *
from django.core.context_processors import csrf
from django.utils.encoding import smart_text
import datetime

from group.models import *

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['centre']))
def centre(req):
    return render_to_response('centre/base.html')

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['centre']))
def train_check(req, train_id=None):
    """
    发布培训待审核页面
    """
    if req.method == "GET":
        train_id = req.GET.get("t_id", None)
        print "train_check, id %s"%train_id
        if train_id and len(train_id) > 0: #有编号的话就返回对应培训的页面
            try:
                train = Train.objects.get(id=train_id)
                return render_to_response('centre/train_check2.html',{"train":train})
            except:
                return HttpResponse("<h2>没有该培训的审核请求</h2>")
        else:#否则返回待审核列表
            ctlist = Train.objects.filter(pass_status=0).order_by('reg_stime')
            return render_to_response('centre/train_check.html',{"ctlist":ctlist})

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['centre']))
def train_pass(req):
    """
    审核批准后
    """
    if req.method == "POST":
        t_id = req.POST.get("t_id")
        if int(req.POST.get("pass", 0)): #审核通过
            t = Train.objects.get(id=t_id)
            t.pass_status = 1
            if t.reg_stime < timezone.now():
                t.reg_status = 1
            t.save()
        else: #审核不通过,该培训直接删除
            Train.objects.filter(id=t_id).delete()
        return JsonResponse({"success":True})
    else:
        return JsonResponse({"success":False})

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['centre']))
def test_check(req, train_id=None):
    """
    培训结果待审核页面
    """
    if req.method == "GET":
        train_id = req.GET.get("t_id",None)
        print "test_check, id %s"%train_id
        if train_id and len(train_id) > 0: #有编号的话就返回对应培训的人名单
            c_t = CoachTrain.objects.filter(train_id=train_id, train__pub_status=0, train__sub_status=1, status__gt=0) #已提交但未发表
            #train = Train.objects.get(id=train_id)
            #filter return a list
            #get return an item
            if len(c_t) > 0:
                train = c_t[0].train
                return render_to_response('centre/test_check2.html',{"c_t":c_t, "train":train})
            else:
                return HttpResponse("<h2>没有该培训的审核请求</h2>")
        else:#否则返回待审核列表
            ctlist = Train.objects.filter(pub_status=0, sub_status=1).order_by('train_stime') #这里查的是Train的status，是联合两个表的查询，用两个_
            jtlist = []
            return render_to_response('centre/test_check.html',{"ctlist":ctlist, "jtlist":jtlist})

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['centre']))
def check_pass(req):
    """
    审核批准后
    """
    if req.method == "POST":
        t_id = req.POST.get("t_id")
        if int(req.POST.get("pass", 0)): #审核通过
            train = Train.objects.filter(id=t_id)
            train.update(pub_status=1, sub_status=1)
            # generate certificate
            #ns = json.loads(req.POST.get("cert","")).keys() #get number list获得审核通过的学号列表 
            ids = json.loads(req.POST.get("ids","")) #get number list获得审核通过的学号列表 
            #not_pass_c_t = CoachTrain.objects.filter(train_id=t_id).exclude(number__in=ns)
            pass_c_t = CoachTrain.objects.filter(id__in=ids, train_id=t_id, status__gt=0)            
            if len(pass_c_t):
                #pass_c_t.update(get_time=datetime.datetime.now(), pass_status=1)
                cur = CoachTrain.objects.exclude(certificate__isnull=True).exclude(certificate__exact='').filter(train__level=train[0].level).count()
                #cur = CoachTrain.objects.filter(pass_status=1, train__level=train[0].level).count()
                for i in range(len(pass_c_t)):
                    pass_c_t[i].check_pass(num=cur+i+1) #编号从1开始计数
                    coach = pass_c_t[i].coach
                    coach.t_level = train[0].level
                    coach.save()

            # 发布消息通知
            title = u"考试结果"
            content = u"恭喜培训%s考试通过"%t_id
        else: #审核不通过
            Train.objects.filter(id=t_id).update(sub_status=2, pub_status=0)
        return JsonResponse({"success":True})
    else:
        return JsonResponse({"success":False})


@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['centre']))
def history_view(req):
    if req.method == "GET":
        train_id = req.GET.get("t_id",None)
        if train_id and len(train_id) > 0: #有编号的话就返回对应培训的人名单
            c_t = CoachTrain.objects.filter(train_id=train_id, train__pub_status=1, status__gt=0)
            if len(c_t) > 0:
                train = c_t[0].train
                return render_to_response('centre/history_view2.html',{"c_t":c_t, "train":train, "base":"./centre/base.html"})
            else:
                return HttpResponse("<h2>没有该培训的历史信息</h2>")
        else:#否则返回培训列表
            ctlist = Train.objects.filter(pub_status=1).order_by('-train_stime')
            jtlist = []
            return render_to_response('centre/history_view.html',{"ctlist":ctlist, "jtlist":jtlist})

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['centre']))
def current_view(req):
    if req.method == "GET":
        train_id = req.GET.get("t_id",None)
        if train_id and len(train_id) > 0: #有编号的话就返回对应培训的人名单
            c_t = CoachTrain.objects.filter(train_id=train_id)
            train = Train.objects.get(id=train_id)
            return render_to_response('centre/current_view2.html',{"c_t":c_t, "train":train, "base":"./centre/base.html"}, RequestContext(req))
        else:
            trains = Train.objects.filter(pass_status=1, pub_status=0).exclude(sub_status=1).order_by('train_stime') #未提交审核的，未成历史的
            return render_to_response('centre/current_view.html',{"trains":trains}, RequestContext(req))

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['centre']))
def game_check(req, game_id=None):
    """
    发布比赛待审核页面
    """
    if req.method == "GET":
        game_id = req.GET.get("g_id", None)
        print "game_check, id %s"%game_id
        if game_id and len(game_id) > 0: #有编号的话就返回对应比赛页面
            try:
                game = Game.objects.get(id=game_id)
                return render_to_response('centre/game_check2.html',{"game":game})
            except:
                return HttpResponse("<h2>没有该比赛的审核请求</h2>")
        else:#否则返回待审核列表
            glist = Game.objects.filter(submit_status=1, pass_status=0).order_by('reg_stime')
            return render_to_response('centre/game_check.html',{"glist":glist})
    else:
        g_id = req.POST.get("g_id")
        if int(req.POST.get("pass", 0)): #审核通过
            g = Game.objects.get(id=g_id)
            g.pass_status = 1
            if g.reg_stime < timezone.now():
                g.reg_status = 1
            g.save()
        else: #审核不通过,该比赛直接删除
            Game.objects.filter(id=g_id).delete()
        return JsonResponse({"success":True})

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['centre']))
def game_val(req, g_id=None):
    """
    比赛结果待审核页面
    g_id: game id
    """
    if req.method == "GET":
        g_id = req.GET.get("g_id",None)
        print "game_val, game id %s"%g_id
        if g_id and len(g_id) > 0: #有编号的话就返回对应比赛参赛队名单
            game = Game.objects.get(id=g_id, pub_status=0, sub_status=1)
            teams = Team.objects.filter(game=game)
            for t in teams:
                if str(t.contestant.role) == 'group':
                    t.Contestant = Group.objects.get(user=t.contestant.user)
                elif role == 'club':
                    t.Contestant = Club.objects.get(user=t.contestant.user)
                t_e = TeamEvent.objects.filter(team=t) #已提交但未发表
                t.tes = t_e
            if len(t_e) > 0:
                return render_to_response('centre/game_val2.html',{"teams":teams, "game":game, "award":AWARD})
            else:
                return HttpResponse("<h2>没有该队的审核请求</h2>")
        else:#否则返回待审核列表
            games = Game.objects.filter(pub_status=0, sub_status=1).order_by('game_stime') 
            return render_to_response('centre/game_val.html',{"games":games})

    if req.method == "POST":# 审核批准后
        g_id = req.POST.get("g_id")
        if int(req.POST.get("pass", 0)): #审核通过
            game = Game.objects.filter(id=g_id)
            game.update(pub_status=1, sub_status=1)
            # generate certificate
            tes = TeamEvent.objects.filter(team__game=game)
            if len(tes):
                cur = TeamEvent.objects.exclude(certificate__isnull=True).exclude(certificate__exact='').count()
                for i in range(len(tes)):
                    tes[i].check_pass(num=cur+i+1) #编号从1开始计数

        else: #审核不通过
            print g_id
            Game.objects.filter(id=g_id).update(sub_status=2, pub_status=0)
        return JsonResponse({"success":True})
    else:
        return JsonResponse({"success":False})

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['centre']))
def history_game(req):
    if req.method == "GET":
        g_id = req.GET.get("g_id",None)
        if g_id and len(g_id) > 0: #有编号的话就返回对应培训的人名单
            try:
                game = Game.objects.get(id=g_id, pub_status=1)
            except:
                return HttpResponse("<h2>没有该比赛的历史信息</h2>")
            teams = Team.objects.filter(game=game)
            game.cur_num = len(teams)
            for t in teams:
                if str(t.contestant.role) == 'group':
                    t.Contestant = Group.objects.get(user=t.contestant.user)
                elif role == 'club':
                    t.Contestant = Club.objects.get(user=t.contestant.user)
                t_e = TeamEvent.objects.filter(team=t) #已提交但未发表
                t.tes = t_e
            if len(t_e) > 0:
                return render_to_response('game/history_game2.html',{"teams":teams, "game":game, "base":"./centre/base.html", "role":"centre"})

        else:#否则返回列表
            games = Game.objects.filter(pub_status=1).order_by('-game_stime')
            return render_to_response('game/history_game.html',{"games":games, "base":"./centre/base.html", "role":"centre"})

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['centre']))
def current_game(req):
    if req.method == "GET":
        g_id = req.GET.get("g_id", None)
        if g_id and len(g_id) > 0: #有编号的话就返回对应培训的人名单
            teams = Team.objects.filter(game_id=g_id)
            game = teams[0].game if len(teams) > 0 else None
            return render_to_response('centre/current_game2.html',{"game":game, "teams":teams, "base":"./centre/base.html"}, RequestContext(req))
        else:
            games = Game.objects.filter(pass_status=1, pub_status=0).exclude(sub_status=1).order_by('game_stime') #未提交审核的，未成历史的
            for g in games:
                g.cur_num = len(Team.objects.filter(game=g))
            return render_to_response('centre/current_game.html',{"games":games}, RequestContext(req))

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['centre']))
def change_payment_status(req):
    if req.method == "POST":
        ct_id = req.POST.get('ct_id', None)
        if ct_id:
            CoachTrain.objects.filter(id=ct_id, status=0).update(status=1)
            return JsonResponse({'success':True})
        return JsonResponse({'success':False})

@login_required()
def history_print(req, train_id=None):
    """
    生成csv表格并下载
    """
    if train_id and len(train_id) > 0:
        return csv_generate()
    else:
        return "Wrong Train id"

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['centre']))
def msg_publish(req):
    """
    """
    if req.method == 'POST': #如果是提交表单内容
        print req.POST
        post = req.POST.copy()
        if post.get("stu", False):
            post["stu"] = True
        if post.get("coach", False):
            post["coach"] = True
        print post
        form = MessagePublishForm(post)
        print form.is_valid()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("msg_publish")
    else: # GET 方法请求消息发送页面
        form = MessagePublishForm()
        return render_to_response('centre/msg_publish.html', {'form':form}, RequestContext(req))


@login_required()
def password_page(req):
    """
    """
    return render_to_response('centre/password.html', RequestContext(req))

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['centre']))
def coach_org_manage(req):
    if req.method == "GET":
        orgs = CoachOrg.objects.all()
        return render_to_response('centre/org_manage.html', {"orgs":orgs,"orgtype":"coach"}, RequestContext(req))

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['centre']))
def game_org_manage(req):
    if req.method == "GET":
        orgs = GameOrg.objects.all()
        return render_to_response('centre/org_manage.html', {"orgs":orgs,"orgtype":"game"}, RequestContext(req))

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['centre']))
def org_info(req):
    Org = CoachOrg
    orgtype = 'coach'
     
    if req.method == "GET" and req.GET.get('orgtype', 'coach') == 'game':
        Org = GameOrg
        orgtype = 'game'
    if req.method == "POST" and req.POST.get('orgtype','coach') == 'game':
        Org = GameOrg
        orgtype = 'game'

    if req.method == "GET":
        num = req.GET.get("orgnum")
        print num
        co = None
        if num:
            co = Org.objects.filter(org_num=num)
        if num and len(co) > 0:
            return render_to_response('centre/org_info.html', {"org":co[0], "orgtype":req.GET.get('orgtype')}, RequestContext(req))
        else:
            return render_to_response('centre/org_info.html', {"orgtype":req.GET.get('orgtype')}, RequestContext(req))
    else:
        data = req.POST.copy()
        orgnum = data.get("orgnum")
        for k in ["orgnum",'phone','orgname']:
            if not data.has_key(k) or len(data[k].strip()) == 0:
                return JsonResponse({},status=400)
        co = Org.objects.filter(org_num=orgnum) | Org.objects.filter(user__phone=data.get('phone'))
        #如果数据库里没有记录，证明是添加新组织
        if len(co) == 0:
            print "add coachorg"
            phone = data.get('phone')
            email = data.get('email',None)
            r_id = 1 if not orgtype=='game' else 7
            user = MyUser.objects.create_user(phone = phone, nickname=orgnum, email=email if email and len(email.strip()) > 0 else None, role=r_id, password = orgnum)
            co = Org(user=user)
        else:
            co = co[0]
            co.user.phone = data["phone"]
            email = data.get("email",None)
            print "email-->"+email
            co.user.email = email if email and len(email.strip()) > 0 else None

        co.org_num = orgnum
        co.name = data["orgname"]
        co.shortname = data["orgshortname"]
        if data.has_key("director"):
            co.director = data["director"]
        if data.has_key("province"):
            co.province = data.get("province","")
        if data.has_key("city"):
            co.city = data.get("city","")
        if data.has_key("dist"):
            co.dist = data.get("dist","")
        if data.has_key("address"):
            co.address = data.get("address","")
        try:
            co.user.save()
            co.save()
        except Exception,e:
            print e
            return JsonResponse({'success':False})
        return JsonResponse({'success':True})

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['centre']))
def org_del(req):
    Org = CoachOrg
    if req.method == "POST" and req.POST.get('orgtype') == 'game':
        Org = GameOrg
    if req.method == "POST":
        orgnum = req.POST.get("orgnum")
        co = Org.objects.get(org_num=orgnum)
        co.is_active = False if co.is_active else True
        co.save()
        return JsonResponse({'success':True})
    else:
        return JsonResponse({'success':False})

