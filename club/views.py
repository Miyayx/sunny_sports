#-*- coding:utf-8 -*-
from django.shortcuts import render

from sp.g_import import *
from sp.utils import *

from club.models import *
from game.models import *
from game.forms import *
from game import views as gv
from sp.models.role import *
from photo.views import *
from sunny_sports.settings import PHOTO_ROOT

from django.contrib import messages

ROLE_ID = 4

@login_required()
@user_passes_test(lambda u: u.is_role(['club']))
def club(req):
    uuid = req.user.id
    u=UserRole.objects.get(user_id=uuid, role_id=ROLE_ID)
    req.session['role'] = ROLE_ID
    if u.is_first:
        messages.error(req, u"请补全机构信息")
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
    return render_to_response('club/center.html',{"club":c[0], "PHOTO_ROOT":PHOTO_ROOT}, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['club']))
def current_game(req, g_id=None, t_id=None):
    return gv.current_game(req, g_id, t_id, ROLE_ID)

@login_required()
@user_passes_test(lambda u: u.is_role(['club']))
@transaction.atomic
def game_apply(req, g_id=None):
    """
    报名，创建参赛队
    """
    if req.method == "POST":
        return gv.game_apply(req, g_id, ROLE_ID)
    else:
        if not g_id:
            return HttpResponse('比赛信息错误')
        game = Game.objects.get(id=g_id)
        club = Club.objects.get(user=req.user)
        #try:
        #    team = Team.objects.get(game=game,)
        #except:
        #    team = None
        return render_to_response('game/game_apply.html',{'group':club, 'game':game, 'base':'./club/base.html', 'role':'club'},RequestContext(req))

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
        return gv.history_game(req, g_id, ROLE_ID)


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

        g = Club.objects.get(user=req.user)
        g.name = data.get("name","")
        g.shortname = data["shortname"]
        g.corporator = data["corporator"]
        if data.has_key("org_num"):
            g.org_num = data.get("org_num","")
        if data.has_key("province"):
            g.province = data.get("province","")
        if data.has_key("city"):
            g.city = data.get("city","")
        if data.has_key("dist"):
            g.dist = data.get("dist","")
        if data.has_key("address"):
            g.address = data.get("address","")
        if data.has_key("office_num"):
            g.office_num = data.get("office_num","")
        try:
            g.save()
            ur.save()
        except Exception,e:
            print e
            return JsonResponse({'success':False})
        return JsonResponse({'success':True})

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['club']))
def upload_license(req):
    c = Club.objects.get(user=req.user)
    #update_photo(req, coach.property)
    upload_license_to_qiniu(req, c)
    return HttpResponseRedirect('/club/center')

