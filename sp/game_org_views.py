# -*- coding:utf-8 -*-

from g_import import *

from django.core.context_processors import csrf

from sp.tasks import *

from datetime import datetime, timedelta

from convert import *

from game.models import *

@login_required()
@user_passes_test(lambda u: u.is_role(['game_org']))
def game_org(req):
    req.session['role'] = 7
    return HttpResponseRedirect("game_org/home")

@login_required()
@user_passes_test(lambda u: u.is_role(['game_org']))
def home(req):
    uuid = req.user.id
    # 用这个id查信息哦
    print uuid
    gameorg = GameOrg.objects.get(user_id=uuid)
    opengames = Game.objects.filter(org=gameorg, pub_status=0).order_by('-game_stime')#按开始时间排序
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
        game_id = req.GET.get("g_id",None)
        if game_id and len(game_id) > 0: #有编号的话就返回对应比赛的人名单
            ts = Team.objects.filter(game_id=game_id, game__pub_status=1)
            if len(ts) > 0:
                game = ts[0].game
                return render_to_response('centre/history_view2.html',{"teams":ts, "game":game, "team":t, "base":"./game_org/base.html"}, RequestContext(req))
            else:
                return HttpResponse("<h2>没有该比赛的历史信息</h2>")
        else:#否则返回比赛列表
            endgames = Game.objects.filter(org__user_id=uuid, pub_status=1).order_by('-game_stime')#按比赛开始时间排序
            return render_to_response('game_org/game_history.html',{"games":endgames}, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['game_org']))
def center(req):
    uuid = req.user.id
    game_org = GameOrg.objects.filter(user_id=uuid)
    return render_to_response('game_org/center.html',{"gameorg":game_org[0]},RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['game_org']))
def game_publish(req):
    if req.method == "POST":
        data = req.POST.copy()
        uuid = req.user.id
        g_id = data.get('g_id',0)
        if g_id: #update game
            game = Game.objects.get(id=t_id)
            data['address'] = game.address
            data['org'] = game.org.id
            data.pop('g_id')
            data['level'] = int(data['level'])
            data['money'] = int(data['money'])
            data['limit'] = int(data['limit'])
            tform = GamePublishForm(data, instance=game)
        else: # create new game
            org = GameOrg.objects.get(user_id=uuid)
            data['org'] = org.id
            data['address'] = data.get('prov','')+data.get('city','')+data.get('dist','')+data.get('addr','')
            data['level'] = int(data['level'])
            data['money'] = int(data['money'])
            data['limit'] = int(data['limit'])
            tform = GamePublishForm(data)
        
        if tform.is_valid():
            t = tform.save()
            #启动计时器
            game_reg_start.apply_async((t.id,), eta=t.reg_stime+timedelta(seconds=3))
            game_reg_end.apply_async((t.id,), eta=t.reg_etime+timedelta(seconds=3))
            game_start.apply_async((t.id,), eta=t.game_stime+timedelta(seconds=3))
            game_end.apply_async((t.id,), eta=t.game_etime+timedelta(seconds=3))
            return JsonResponse({'success':True})
        else:
            print tform.errors
            return JsonResponse({'success':False })
        
    else:
        t_id = req.GET.get('t_id',0)
        t = None
        if t_id :
            t = Game.objects.get(id=t_id)
        uuid = req.user.id
        org = GameOrg.objects.get(user_id=uuid)
        return render_to_response('game_org/game_publish.html',{'level':TRAIN_LEVEL,'org':org, 'game': t }, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['game_org']))
def game_manage(req):
    uuid = req.user.id
    opengames = Game.objects.filter(org__user_id=uuid, pub_status=0).order_by('-game_stime')#按比赛开始时间排序
    gamegames = [GameGame.objects.filter(game=t, status__gt=-1) for t in opengames]
    return render_to_response('game_org/game_manage.html',{"zipped":zip(opengames, gamegames)}, RequestContext(req))

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['game_org']))
def score_input(req):
    if req.method == "POST":
        data = req.POST.copy()
        print data
        submit = int(data.pop("submit")[0])
        t_id = data.pop("t_id")[0]
        cts = GameGame.objects.filter(game_id=t_id, status__gt=0)
        for ct in cts:
            #print data[str(int(ct.id))]
            #print "status",str2bool(data[str(int(ct.id))])
            ct.pass_status = str2bool(data[str(int(ct.id))])
            ct.save()
        if submit:
            cts[0].game.sub_status=1
            cts[0].game.save()
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

