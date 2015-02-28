# -*- coding:utf-8 -*-
from django import forms
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
#from django.contrib.auth import authenticate
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import RequestContext

from django.views.decorators.http import require_http_methods

from sunny_sports.sp.models import *
from sunny_sports.sp.models.models import *
from sunny_sports.sp.models.status import get_role_id
from sunny_sports.sp.backend import MyBackend 

from forms import *
from utils import *

# Create your views here.

#客户端提交的post如果不加这段，会出现403error  
@csrf_exempt  
def vcode(req):
    """
    获取验证码请求
    """
    phone = req.POST.get('phone').strip()
    if not phone or len(phone) == 0:
        return None
    result, code = send_vcode(phone)
    print phone
    print code
    c = Code(phone=phone,code=code)
    c.save()
    return JsonResponse(result)

@login_required()
def get_msg(req):
    """
    header部分获取未读消息
    """
    uuid = req.user.id
    if uuid:
        msgs = UserMessage.objects.filter(user_id=uuid, checked=False)
        print len(msgs)
        html = render_to_string('base/msg.html', {'num':len(msgs), 'msgs': msgs[:5]})
        return HttpResponse(html)
    return None

@require_http_methods(["POST"])
@transaction.atomic
def regist(req):
    if req.method == 'POST':
        req.session.clear()
        phone = req.POST.get('phone')
        password = req.POST.get('password')
        password2 = req.POST.get('password2')
        v_code    = req.POST.get('v_code')
        #检验手机验证码
        p, msg = check_vcode(phone, v_code)
        if not p:
            messages.error(req, msg,extra_tags='regist')
            return render_to_response('login.html', context_instance=RequestContext(req))
        #检验密码是否一致
        if not password == password2:
            messages.error(req, u"两次密码输入不一致",extra_tags='regist')
            return render_to_response('login.html', context_instance=RequestContext(req))

        role = req.POST.get('role2').strip()
        r_id = get_role_id(role)
        user = MyUser.objects.create_user(phone = phone, nickname=None, email=None, role=r_id, password = password)
        u = authenticate(username=phone, password=password)#用django自带函数检验
        if u is not None:
            # the password verified for the user
            if u.is_active:
                login(req,u) #django自带的login将userid写入session,这步之前一定有authenticate
                return HttpResponseRedirect('/%s'%role)
        messages.error(req, u"用户身份验证错误",extra_tags='regist')
        return render_to_response('login.html', context_instance=RequestContext(req))
    else:
        return render_to_response('login.html')

@transaction.atomic
def mylogin(req): #登录view，跟自带的auth.login 区分开
    if req.method == 'POST':
        req.session.clear()
        un = req.POST['username']
        pw = req.POST['password']
        role = req.POST['role']
        user = None
        if un and len(un) >0: #如果用用户名
            #user = MyBackend().authenticate(username=un, password=pw)#用django自带函数检验
            user = authenticate(username=un, password=pw)#用django自带函数检验
        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
                login(req,user) #django自带的login将userid写入session
                roles = [r.get_role_display() for r in user.role.all()] #all()是取多对多值的办法
                print "roles:",roles
                if role == "admin" and "centre" in roles:
                    return HttpResponseRedirect('/centre')
                elif role == "admin" and "coach_org" in roles:
                    return HttpResponseRedirect('/coach_org')
                elif role in roles:
                    return HttpResponseRedirect('/%s'%role)
                else:
                    messages.error(req, u"请选择正确的角色")
                return render_to_response("login.html", context_instance=RequestContext(req))
            else:
                messages.error(req, "The password is valid, but the account has been disabled!")
                return render_to_response("login.html", context_instance=RequestContext(req))
        else:
        # the authentication system was unable to verify the username and password
            messages.error(req, u"用户名或密码错误")
            return render_to_response("login.html", context_instance=RequestContext(req))
    return render_to_response("login.html", context_instance=RequestContext(req))
          
def index(req):
    uuid = req.user.id
    name = req.user.name
    return render_to_response('index.html', {'username': name}, context_instance=RequestContext(req))
          
@login_required()
def mylogout(req):
    logout(req)
    #req.session.clear()
    return render_to_response("login.html" ,context_instance=RequestContext(req))

def find_password(req) :
    if req.method == 'POST':
        phone = req.POST['phone']
        code = req.POST['v_code']
        # 用手机短信验证码确认身份
        c = Code.objects.filter(phone = phone).latest('time')
        if c.code == code:
            return HttpResponseRedirect('reset_password?phone='+phone)
        else:
            messages.error(req, "验证码错误")
            return render_to_response("login.html", context_instance=RequestContext(req))
    else:
        return render_to_response("login.html", context_instance=RequestContext(req))

def reset_password(req):
    if req.method == 'POST':
        u = MyUser.objects.get(id=req.POST['uuid'])
        if not req.POST["password"] == req.POST["password2"]:
            return JsonResponse({"success":False,"msg":u"密码不一致"}) 

        new_pw = req.POST["password"]
        u.set_password(new_pw)
        u.save()
        return JsonResponse({"success":True,"msg":u"密码已修改"}) 
    else:
        phone = req.GET['phone']
        uuid = MyUser.objects.get(phone=phone).id
        return render_to_response("reset_password.html",{"uuid":uuid}, context_instance=RequestContext(req))

@login_required()
def password(req):
    if req.method == 'POST': #Change password 
        u = MyUser.objects.get(id=req.user.id)
        pw = req.POST['old_password']
        user = MyBackend().authenticate(username=u.phone, password=pw)#用django自带函数检验
        if user is not None:
            if pw == req.POST['password']:
                return JsonResponse({"success":False,"msg":u"原密码与新密码相同"}) 
            if not req.POST["password"] == req.POST["password2"]:
                return JsonResponse({"success":False,"msg":u"密码不一致"}) 

            # 用手机短信验证码确认身份
            #c = Code.objects.get(phone = u.phone).latest('time')
            #if c.code == req.POST.get("vcode",0):
            #    u.set_password(new_password)
            #    u.save()
            #    return JsonResponse({"success":True,"msg":""}) 
            #else:
            #    return JsonResponse({"success":False,"msg":u"验证码错误"}) 
            new_pw = req.POST["password"]
            u.set_password(new_pw)
            u.save()
            return JsonResponse({"success":True,"msg":u"密码已修改"}) 
        else:
            return JsonResponse({"success":False,"msg":u"密码错误"}) 

    else: #Get page
        u = MyUser.objects.get(id=req.user.id)
        return render_to_response('password.html', {"phone":u.phone}, RequestContext(req))

@login_required()
def download_excel(req):
    t_id = req.GET.get("t_id",0)
    if t_id:
        coachtrains = CoachTrain.objects.filter(train_id=t_id)
        train = coachtrains[0].train
        if train.pub_status: #如果已经发布，包括是否通过，证书号
            fields = [u"学员姓名", u"学号", u"性别", u"联系方式", u"邮箱", u"出生日期", u"年龄", u"常驻地", u"工作单位", u"证书编号"]
            rows = [(ct.coach.property.name, ct.number, ct.coach.property.get_sex_display(), ct.coach.property.user.phone, ct.coach.property.user.email, ct.coach.property.birth.strftime('%Y-%m-%d'), calculate_age(ct.coach.property.birth), join_position(ct.coach), ct.coach.property.company, ct.certificate) for ct in coachtrains]
        else:
            fields = [u"学员姓名", u"学号", u"性别", u"联系方式", u"邮箱", u"出生日期", u"年龄", u"常驻地", u"工作单位"]
            rows = [(ct.coach.property.name, ct.number, ct.coach.property.get_sex_display(), ct.coach.property.user.phone, ct.coach.property.user.email, ct.coach.property.birth.strftime('%Y-%m-%d'), calculate_age(ct.coach.property.birth), join_position(ct.coach), ct.coach.property.company) for ct in coachtrains]
        return export_xls(req, train.name, fields, rows)

        
