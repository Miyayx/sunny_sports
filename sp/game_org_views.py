# -*- coding:utf-8 -*-

from g_import import *

from django.core.context_processors import csrf

from datetime import datetime, timedelta

from convert import *

from game.models import *
from game.tasks import *
from game.utils import wrap_schedule
from group.models import *

ROLE_ID = 7

@login_required()
@user_passes_test(lambda u: u.is_role(['game_org']))
def game_org(req):
    req.session['role'] = ROLE_ID
    return HttpResponseRedirect("game_org/home")

@login_required()
@user_passes_test(lambda u: u.is_role(['game_org']))
def home(req):
    uuid = req.user.id
    gameorg = GameOrg.objects.get(user_id=uuid)
    opengames = Game.objects.filter(org=gameorg, submit_status=1, pub_status=0).order_by('-game_stime')#按开始时间排序
    endgames = Game.objects.filter(org=gameorg, pub_status=1).order_by('-game_stime')#按开始时间排序
    return render_to_response('game_org/home.html',{"gameorg":gameorg,"opengames":opengames, "endgames":endgames[:5]} ,RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['game_org']))
def game_history(req):
    """
    历史比赛查看
    """
    uuid = req.user.id
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
                s_t = StudentTeam.objects.filter(team=t) #队员
                t.tes = t_e
                t.sts = s_t
            if len(t_e) > 0:
                return render_to_response('game/history_game2.html',{"teams":teams, "game":game, "base":"./game_org/base.html", "role":"game_org"})
        else:#否则返回比赛列表
            games = Game.objects.filter(org__user_id=uuid, pub_status=1).order_by('-game_stime')#按比赛开始时间排序
            return render_to_response('game/history_game.html',{"games":games, "base":"game_org/base.html", "role":"game_org"}, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['game_org']))
def center(req):
    uuid = req.user.id
    game_org = GameOrg.objects.filter(user_id=uuid)
    return render_to_response('game_org/center.html',{"gameorg":game_org[0]},RequestContext(req))

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['game_org']))
def game_publish(req):

    if req.method == "POST":
        data = req.POST.copy()
        uuid = req.user.id
        g_id = data.get('g_id',0)
        save = data.get('save',0)
        if g_id: #update game
            print "Update game%s"%g_id
            game = Game.objects.get(id=g_id)
            data['org'] = game.org.id
            data.pop('g_id')
            data['money'] = int(data['money'])
            data['limit'] = int(data['limit'])
            data['male_num'] = int(data['male_num'])
            data['female_num'] = int(data['female_num'])
            data['total_num'] = data['male_num']+data['female_num']
            data['sponsor'] = data['sponsor']
            data['organizer'] = data['organizer']
            data['coorganizer'] = data['coorganizer']
            data['schedule'] = data['schedule'].strip('#;;;;')
            data['description'] = data['description']
            data['province'] = data['prov'].strip()
            gform = GamePublishForm(data, instance=game)
        else: # create new game
            org = GameOrg.objects.get(user_id=uuid)
            data['org'] = org.id
            data['money'] = int(data['money'])
            data['limit'] = int(data['limit'])
            data['male_num'] = int(data['male_num'])
            data['female_num'] = int(data['female_num'])
            data['total_num'] = data['male_num']+data['female_num']
            data['sponsor'] = data['sponsor']
            data['organizer'] = data['organizer']
            data['coorganizer'] = data['coorganizer']
            data['schedule'] = data['schedule'].strip().strip('#;;;;')
            data['description'] = data['description']
            data['province'] = data['prov'].strip()
            gform = GamePublishForm(data)
        
        if gform.is_valid():
            g = gform.save()
            if not save: #如果是提交审核
                g.submit_status=1
                g.save()
                #启动计时器
                game_reg_start.apply_async((g.id,), eta=g.reg_stime+timedelta(seconds=1))
                game_reg_end.apply_async((g.id,), eta=g.reg_etime+timedelta(seconds=1))
                game_start.apply_async((g.id,), eta=g.game_stime+timedelta(seconds=1))
                game_end.apply_async((g.id,), eta=g.game_etime+timedelta(seconds=1))
            return JsonResponse({'success':True})
        else:
            print gform.errors
            return JsonResponse({'success':False, 'msg':str(gform.errors['error']) })
        
    else:

        g_id = req.GET.get('g_id',0)
        uuid = req.user.id
        org = GameOrg.objects.get(user_id=uuid)
        g = None
        if g_id :
            g = Game.objects.get(id=g_id)
        else:
            try:
                g = Game.objects.filter(org=org, submit_status=0)[0]
                g.schedule = wrap_schedule(g.schedule)
            except Exception,e:
                print e
                g = None
        return render_to_response('game_org/game_publish.html',{'events':EVENTS,'org':org, 'game': g }, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['game_org']))
def game_manage(req):
    uuid = req.user.id
    games = Game.objects.filter(org__user_id=uuid, submit_status=1, pub_status=0).order_by('-game_stime')#按比赛开始时间排序
    for g in games:
        teams = Team.objects.filter(game=g)
        g.cur_num = len(teams)
        g.teams = teams
        for t in g.teams:
            role = str(t.contestant.role)
            if role == 'group':
                t.Contestant = Group.objects.get(user=t.contestant.user)
            elif role == 'club':
                t.Contestant = Club.objects.get(user=t.contestant.user)

            t.tes = TeamEvent.objects.filter(team=t)
    return render_to_response('game_org/game_manage.html',{"games":games, "award":AWARD}, RequestContext(req))

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['game_org']))
def result_input(req):
    if req.method == "POST":
        data = req.POST.copy()
        print data
        submit = int(data.pop("submit")[0])
        g_id = data.pop("g_id")[0]
        teams = Team.objects.filter(game_id=g_id, pay_status=1)
        result = json.loads(data.pop('res')[0])
        print result
        for t in teams:
            tes = TeamEvent.objects.filter(team=t)
            for te in tes:
                te.award = int(result[t.id][str(te.event.id)])
                te.save()
            #TeamEvent.objects.filter(team=t).update(award=int(result[t.id][str(F('event_id'))]))
        if submit:
            teams[0].game.sub_status=1
            teams[0].game.save()
        return JsonResponse({"success":True})
        
@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['game_org']))
def update_info(req):
    """
    个人中心，用户更新基本信息
    """
    if req.method == "POST":
        data = req.POST.copy()
        uuid = req.user.id
        MyUser.objects.filter(id=uuid).update(phone=data.pop("phone")[0], email=data.pop("email")[0])
        co = GameOrg.objects.get(user_id=uuid)
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
        if data.has_key("ali_email"):
            co.ali_email = data.get("ali_email","")
        try:
            co.save()
        except:
            return JsonResponse({'success':False})
        return JsonResponse({'success':True})

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['game_org']))
def del_team(req):
    if req.method == "POST":
        t_id = req.POST.get("t_id")
        Team.objects.get(id=t_id).delete() #这里studentteam, teamevent的删除写在了team的重载delete里
        return JsonResponse({'success':True})
    else:
        return JsonResponse({'success':False})
