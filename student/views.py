#-*- coding:utf-8 -*-
from django.shortcuts import render

from sp.g_import import *
from sp.utils import *

from student.models import *
from game.models import *
from sunny_sports.settings import PHOTO_ROOT

#from photo.views import update_photo
from photo.views import update_photo_in_qiniu

from django.contrib import messages

ROLE_ID=2

@login_required()
@user_passes_test(lambda u: u.is_role(['student']))
def student(req):
    uuid = req.user.id
    u=UserRole.objects.get(user_id=uuid, role_id=2)
    req.session['role'] = 2
    if u.is_first:
        messages.error(req, u"请补全个人信息")
        return HttpResponseRedirect("student/center")
    else:
        return HttpResponseRedirect("student/home")

@login_required()
@user_passes_test(lambda u: u.is_role(['student']))
def home(req):
    uuid = req.user.id
    stu = Student.objects.get(property__user_id=uuid)
    stu.property.age = calculate_age(stu.property.birth) 

    game = None
    try:
        st = StudentTeam.objects.get(student=stu, team__game__pub_status = 0)
        cur_game = st.team.game
    except:
        cur_game = None

    sts = StudentTeam.objects.filter(student=stu, team__game__pub_status=1)[:3]
    games = [st.team.game for st in sts]
    
    return render_to_response('student/home.html',{"student":stu, "cur_game":cur_game, "games":games, "PHOTO_ROOT":PHOTO_ROOT}, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['student']))
def center(req):
    uuid = req.user.id
    # 用这个id查信息哦
    ur = UserRole.objects.get(user_id=uuid, role_id=2)
    if ur.is_first:
        messages.error(req, u"请补全个人信息")
    stu = Student.objects.filter(property__user_id=uuid)
    return render_to_response('student/center.html',{"student":stu[0], "PHOTO_ROOT":PHOTO_ROOT}, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['student']))
def current_game(req):
    return render_to_response('student/cur_game.html', RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['student']))
def history_game(req):
    if req.method == "GET":
        g_id = req.GET.get("g_id",None)
        if g_id and len(g_id) > 0: #有编号的话就返回对应比赛信息
            try:
                game = Game.objects.get(id=g_id, pub_status=1)
                team = StudentTeam.objects.filter(team__game=game, student__property__user_id=req.user.id)[0].team
                sts = StudentTeam.objects.filter(team=team)
                tes = TeamEvent.objects.filter(team=team)
            except:
                return HttpResponse("<h2>没有该比赛的历史信息</h2>")

            return render_to_response('game/single_game.html',{'base':'./student/base.html', 'game':game, 'team':team, 'sts':sts, 'tes':tes, 'role':'student'}, RequestContext(req))
        else:#否则返回历史比赛列表
            uuid = req.user.id
            sts = StudentTeam.objects.filter(student__property__user_id=uuid)
            teams = [st.team for st in sts] 
            return render_to_response('game/history_team.html', {"teams":teams, "base":"./student/base.html", "role":"student"}, RequestContext(req))

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['student']))
def update_info(req):
    """
    个人中心，用户更新基本信息
    """
    if req.method == "POST":
        data = req.POST.copy()

        uuid = req.user.id
        ur = UserRole.objects.get(user_id=uuid, role_id=2)
        ur.is_first = False
        if data.has_key("nickname") and len(data['nickname'].strip()):
            MyUser.objects.filter(id=uuid).update(nickname=data.pop("nickname")[0], phone=data.pop("phone")[0], email=data.pop("email")[0])
        else:
            MyUser.objects.filter(id=uuid).update(phone=data.pop("phone")[0], email=data.pop("email")[0])

        sp = StudentProperty.objects.get(user_id=uuid)
        sp.name = data.get("name","")
        if data.has_key("sex"):
            sp.sex = int(data.get("sex"))
        if data.has_key("identity"):
            sp.identity = data.get("identity","")
        if data.has_key('birth'):
            sp.birth = data.get("birth")
        if data.has_key("company"):
            sp.company = data["company"]
        if data.has_key("province"):
            sp.province = data.get("province","")
        if data.has_key("city"):
            sp.city = data.get("city","")
        if data.has_key("dist"):
            sp.dist = data.get("dist","")
        if data.has_key("address"):
            sp.address = data.get("address","")
        if data.has_key("height"):
            sp.height = data.get("height","")
        if data.has_key("weight"):
            sp.weight = data.get("weight","")
        try:
            sp.save()
            ur.save()
        except Exception,e:
            print e
            return JsonResponse({'success':False})
        return JsonResponse({'success':True})

@login_required()
@transaction.atomic
@user_passes_test(lambda u: u.is_role(['student']))
def update_img(req):
    uuid = req.user.id
    stu = Student.objects.get(property__user_id=uuid)
    #update_photo(req, coach.property)
    update_photo_in_qiniu(req, stu.property)
    return HttpResponseRedirect('/student/center')
