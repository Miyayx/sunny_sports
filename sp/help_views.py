
# -*- coding:utf-8 -*-

from g_import import *

from django import forms
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str

@csrf_exempt  
def coach_help(req):
    f = open('media/coach_help.pdf')
    response = HttpResponse(f.read())
    f.close()
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('快乐体操教练报名与付款教程.pdf')
    response['Content-Type'] = 'application/pdf'
# It's usually a good idea to set the 'Content-Length' header too.
# You can also set any other required headers: Cache-Control, etc.
    return response

@csrf_exempt  
def game_group_help(req):
    f = open('media/game_group_help.pdf')
    response = HttpResponse(f.read())
    f.close()
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('快乐体操参赛队报名与付款教程.pdf')
    response['Content-Type'] = 'application/pdf'
    return response
