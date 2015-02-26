# -*- coding:utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.core.context_processors import csrf
from django.template import RequestContext

from sunny_sports.sp.models import *
from sunny_sports.sp.models.models import *
from sunny_sports.sp.models.status import get_role_id

def is_phone_exists(req):
    #检验该手机号是否已注册
    phone = req.GET.get('phone')
    u = MyUser.objects.filter(phone=phone)
    if len(u) > 0:
        return JsonResponse({"pass":False})
    else:
        return JsonResponse({"pass":True})
