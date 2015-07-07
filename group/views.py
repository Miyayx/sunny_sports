#-*- coding:utf-8 -*-
from django.shortcuts import render

from sp.g_import import *
from sp.utils import *

from group.models import *
from game.models import *
from game.forms import *
from sp.models.role import *

from django.contrib import messages

ROLE_ID = 5

@login_required()
@user_passes_test(lambda u: u.is_role(['group']))
def group(req):
    uuid = req.user.id
    u=UserRole.objects.get(user_id=uuid, role_id=ROLE_ID)
    req.session['role'] = ROLE_ID
    if u.is_first:
        messages.error(req, u"请补全个人信息")
        return HttpResponseRedirect("group/center")
    else:
        return HttpResponseRedirect("group/home")

@login_required()
@user_passes_test(lambda u: u.is_role(['group']))
def home(req):
    uuid = req.user.id
    g = Group.objects.get(user_id=uuid)
    ur = UserRole.objects.get(user = req.user, role_id=ROLE_ID)

    game = None
    try:
        cur_game = Team.objects.get(contestant=ur, game__pub_status = 0)
    except:
        cur_game = None

    games = Team.objects.filter(contestant=ur, game__pub_status=1)[:3]
    
    return render_to_response('group/home.html',{"group":g, "cur_game":cur_game, "games":games}, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['group']))
def center(req):
    uuid = req.user.id
    # 用这个id查信息哦
    ur = UserRole.objects.get(user_id=uuid, role_id=ROLE_ID)
    if ur.is_first:
        messages.error(req, u"请补全个人信息")
    g = Group.objects.filter(user_id=uuid)
    return render_to_response('group/center.html',{"group":g[0]}, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['group']))
def current_game(req, g_id=None):
     if not g_id:
         games = Game.objects.filter(pass_status=1, pub_status=0)
         for g in games:
             g.cur_num = len(Team.objects.filter(game=g))
             try:
                 ur = UserRole.objects.get(user=req.user, role_id=ROLE_ID)
                 g.team = Team.objects.get(game=g, contestant=ur)
             except:
                 g.team = None
             
         return render_to_response('game/group_gamelist.html',{'base':'./group/base.html', 'role':'group', "games":games}, RequestContext(req))
     else:
         game = Game.objects.get(id=g_id)
         try:
             ur = UserRole.objects.get(user=req.user, role_id=ROLE_ID)
             team = Team.objects.get(game=g, contestant=ur)
             sts = StudentTeam.objects.filter(team=team)
             tes = TeamEvent.objects.filter(team=team)
         except:
             team = None
             sts = None
             tes = None
         
         return render_to_response('game/new_game_info.html',{'base':'./group/base.html', 'game':game, 'team':team, 'sts':sts, 'tes':tes, 'role':'group'}, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['group']))
@transaction.atomic
def game_apply(req, g_id=None):
    """
    报名，创建参赛队
    """
    if req.method == "POST":
        data = req.POST.copy()
        uuid = req.user.id
        # create new team
        members = data.pop('member')[0]
        data['contestant'] = UserRole.objects.get(user=req.user, role_id=ROLE_ID).id
        tform = TeamForm(data)
        if tform.is_valid():
            t = tform.save()
            ms = members.strip().split(',')
            stus = Student.objects.filter(property__user__id__in=ms)
            sts = []
            for s in stus:
                sts.append(StudentTeam(student=s, team=t))
            StudentTeam.objects.bulk_create(sts)

            return JsonResponse({'success':True})
        else:
            print tform.errors
            return JsonResponse({'success':False })
    else:
        if not g_id:
            return HttpResponse('比赛信息错误')
        game = Game.objects.get(id=g_id)
        group = Group.objects.get(user=req.user)
        #try:
        #    team = Team.objects.get(game=game,)
        #except:
        #    team = None
        return render_to_response('game/game_apply.html',{'group':group, 'game':game, 'base':'./group/base.html', 'role':'group'},RequestContext(req))


@login_required()
@user_passes_test(lambda u: u.is_role(['group']))
def history_game(req):
    if req.method == "GET":
        game_id = req.GET.get("g_id",None)
        if game_id and len(game_id) > 0: #有编号的话就返回对应比赛信息
            sts = StudentTeam.objects.filter(team__game_id=game_id)
            if len(sts) > 0:
                st = sts[0]
                tes = TeamEvent.objects.filter(team=st.team)
                return render_to_response('game/history_game2.html',{"st":st, "tes":tes, "base":"./group/base.html"})
            else:
                return HttpResponse("<h2>没有该比赛的历史信息</h2>")
        else:#否则返回历史比赛列表
            uuid = req.user.id
            ur = UserRole(user=req.user, role_id=ROLE_ID)
            teams = Team.objects.filter(contestant=ur, game__pub_status=1)
            return render_to_response('game/history_game.html', {"teams":teams, "base":"./group/base.html"}, RequestContext(req))

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['group']))
def update_info(req):
    """
    个人中心，用户更新基本信息
    """
    if req.method == "POST":
        data = req.POST.copy()

        uuid = req.user.id
        ur = UserRole.objects.get(user_id=uuid, role_id=ROLE_ID)
        ur.is_first = False
        if data.has_key("nickname") and len(data['nickname'].strip()):
            MyUser.objects.filter(id=uuid).update(nickname=data.pop("nickname")[0], phone=data.pop("phone")[0], email=data.pop("email")[0])
        else:
            MyUser.objects.filter(id=uuid).update(phone=data.pop("phone")[0], email=data.pop("email")[0])

        g = Group.objects.get(user=req.user)
        g.name = data.get("name","")
        g.org_num = data.get("org_num","")
        if data.has_key("province"):
            g.province = data.get("province","")
        if data.has_key("city"):
            g.city = data.get("city","")
        if data.has_key("dist"):
            g.dist = data.get("dist","")
        if data.has_key("address"):
            g.address = data.get("address","")
        try:
            g.save()
            ur.save()
        except Exception,e:
            print e
            return JsonResponse({'success':False})
        return JsonResponse({'success':True})

