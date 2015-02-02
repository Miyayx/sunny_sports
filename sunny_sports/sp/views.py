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
#from sunny_sports.sp.backend import MyBackend 

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
def regist(req):
    c = {}
    c.update(csrf(req))
    if req.method == 'POST':
        phone = req.POST.get('phone')
        password = req.POST.get('password')
        password2 = req.POST.get('password2')
        verify    = req.POST.get('v_code')
        if not password == password2:
            messages.error(req, u"两次密码输入不一致",extra_tags='regist')
            return render_to_response('login.html', context_instance=RequestContext(req))
        role     = req.POST.get('role2').strip()                
        r_id = get_role_id(role)
        user = MyUser.objects.create_user(phone = phone, nickname=None, email=None, role=r_id, password = password)
        return HttpResponseRedirect('/%s'%role)
    else:
        return render_to_response('login.html')

@require_http_methods(["POST"])
def mylogin(req): #登录view，跟自带的auth.login 区分开
    uuid = req.user.id
    if req.method == 'POST':
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
          
def index(req):
    uuid = req.user.id
    name = req.user.name
    return render_to_response('index.html', {'username': name}, context_instance=RequestContext(req))
          
@login_required()
def mylogout(req):
    print "logout"
    logout(req)
    return render_to_response("login.html")

@login_required()
def password(req):
    if req.method == 'POST': #Change password 
        u = MyUser.objects.get(id=req.user.id)
        pw = req.POST['old_password']
        user = MyBackend().authenticate(username=u.phone, password=pw)#用django自带函数检验
        if user is not None:
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
            u.set_password(new_password)
            u.save()
            return JsonResponse({"success":True,"msg":"密码已修改"}) 
        else:
            return JsonResponse({"success":False,"msg":u"密码错误"}) 

    else: #Get page
        u = MyUser.objects.get(id=req.user.id)
        return render_to_response('password.html', {"phone":u.phone}, RequestContext(req))

