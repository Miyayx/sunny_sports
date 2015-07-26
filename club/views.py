#-*- coding:utf-8 -*-
from django.shortcuts import render

from sp.g_import import *
from sp.utils import *

from club.models import *
from game.models import *
from game.forms import *
from sp.models.role import *

from django.contrib import messages

ROLE_ID = 4

@login_required()
@user_passes_test(lambda u: u.is_role(['club']))
def club(req):
    uuid = req.user.id
    u=UserRole.objects.get(user_id=uuid, role_id=ROLE_ID)
    req.session['role'] = ROLE_ID
    if u.is_first:
        messages.error(req, u"请补全个人信息")
        return HttpResponseRedirect("club/center")
    else:
        return HttpResponseRedirect("club/home")

@login_required()
@user_passes_test(lambda u: u.is_role(['club']))
def home(req):
    uuid = req.user.id
    c = Club.objects.get(user_id=uuid)
    ur = UserRole.objects.get(user=req.user, role_id=ROLE_ID)

    teams = None
    old_teams = None
    try:
        teams = Team.objects.filter(contestant=ur, game__pub_status = 0)
    except:
        teams = None

    old_teams = Team.objects.filter(contestant=ur, game__pub_status=1)[:5]
    
    return render_to_response('club/home.html',{"club":c, "teams":teams, "old_teams":old_teams}, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['club']))
def center(req):
    uuid = req.user.id
    # 用这个id查信息哦
    ur = UserRole.objects.get(user_id=uuid, role_id=ROLE_ID)
    if ur.is_first:
        messages.error(req, u"请补全个人信息")
    c = Club.objects.filter(user_id=uuid)
    return render_to_response('club/center.html',{"club":c[0]}, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['club']))
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
             
         return render_to_response('game/group_gamelist.html',{'base':'./club/base.html', 'role':'club', "games":games}, RequestContext(req))
     else:
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
         
         return render_to_response('game/single_game.html',{'base':'./club/base.html', 'game':game, 'team':team, 'sts':sts, 'tes':tes, 'role':'club'}, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['club']))
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

            tes = []
            for e in Event.objects.all():
                tes.append(TeamEvent(event=e, team=t))
            TeamEvent.objects.bulk_create(tes)

            return JsonResponse({'success':True})
        else:
            print tform.errors
            return JsonResponse({'success':False })
    else:
        if not g_id:
            return HttpResponse('比赛信息错误')
        game = Game.objects.get(id=g_id)
        club = Club.objects.get(user=req.user)
        #try:
        #    team = Team.objects.get(game=game,)
        #except:
        #    team = None
        return render_to_response('game/game_apply.html',{'club':club, 'game':game, 'base':'./club/base.html', 'role':'club'},RequestContext(req))

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['club']))
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
@user_passes_test(lambda u: u.is_role(['club']))
def history_game(req):
    if req.method == "GET":
        g_id = req.GET.get("g_id",None)
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
            
            return render_to_response('game/single_game.html',{'base':'./club/base.html', 'game':game, 'team':team, 'sts':sts, 'tes':tes, 'role':'club'}, RequestContext(req))
        else:#否则返回历史比赛列表
            uuid = req.user.id
            teams = Team.objects.filter(contestant__user=req.user, contestant__role_id=ROLE_ID, game__pub_status=1)
            return render_to_response('game/history_team.html', {"teams":teams, "base":"./club/base.html", "role":"club"}, RequestContext(req))

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['club']))
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

        g = Role.objects.get(user=req.user)
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

