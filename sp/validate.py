# -*- coding:utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.core.context_processors import csrf
from django.template import RequestContext

from sp.models import *
from sp.models.models import *
from sp.models.status import get_role_id

def is_phone_exists(req):
    #检验该手机号是否已注册
    phone = req.GET.get('phone')
    u = MyUser.objects.filter(phone=phone)
    if len(u) > 0:
        return JsonResponse({"exists":True})
    else:
        return JsonResponse({"exists":False})

def is_nickname_exists(req):
    #检验该昵称是否已注册
    nickname = req.GET.get('nickname')
    u = MyUser.objects.filter(nickname=nickname)
    if len(u) > 0:
        return JsonResponse({"exists":True})
    else:
        return JsonResponse({"exists":False})

def is_orgshortname_exists(req):
    #检验该组织机构简称是否已注册
    osn = req.GET.get('shortname')
    u = CoachOrg.objects.filter(shortname=osn)
    if len(u) > 0:
        return JsonResponse({"exists":True})
    else:
        return JsonResponse({"exists":False})

def is_email_exists(req):
    #检验该邮箱是否已注册
    email = req.GET.get('email')
    u = MyUser.objects.filter(email=email)
    if len(u) > 0:
        return JsonResponse({"exists":True})
    else:
        return JsonResponse({"exists":False})



