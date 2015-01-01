# -*- coding:utf-8 -*-
from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
#from django.contrib.auth import authenticate
from django.contrib.auth import authenticate
from django.contrib import messages
from django.template import RequestContext

from django.views.decorators.http import require_http_methods

from sunny_sports.sp.models import *
from sunny_sports.sp.backend import MyBackend 

from forms import *

# Create your views here.
          
@require_http_methods(["POST"])
def regist(req):
    c = {}
    c.update(csrf(req))
    if req.method == 'POST':
        phone = req.POST.get('username')
        password = req.POST.get('password')
        role     = req.POST.get('role')                
        MyUser.objects.create(phone = phone, password = password, role = role)
        return HttpResponseRedirect('/login/')
    else:
        uf = UserForm()
    return render_to_response('login.html')
          
@require_http_methods(["POST"])
def login(req):
    if req.method == 'POST':
        un = req.POST['username']
        pw = req.POST['password']
        role = req.POST['role']
        user = None
        if un and len(un) >0: #如果用用户名
            user = MyBackend().authenticate(username=un, password=pw)#用django自带函数检验
        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
                req.session['uuid'] = user.id
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
    username = req.session.get('username', 'anybody')
    return render_to_response('index.html', {'username': username}, context_instance=RequestContext(req))
          
def logout(req):
    c = {}
    c.update(csrf(req))
    print "logout"
    session = req.session.get('username', False)
    if session:
        del req.session['username']
        return render_to_response('login.html',c)
    else:
        return HttpResponse('please login!')

