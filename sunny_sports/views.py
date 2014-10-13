#!/usr/bin/env python3

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

from .mapping import PAGE_MAPPING

def home(req):

    t = get_template(PAGE_MAPPING["login"])
    c = Context({})
    html = t.render(c)
    return HttpResponse(html)

def all(req):
    url = req.path[req.path.index("/"):].strip("/")
    print (url)

    t = get_template(PAGE_MAPPING[url])
    c = Context({})
    html = t.render(c)
    return HttpResponse(html)

def login(req):
    pass

def password(req):
    pass

def stu_sign_up(req):
    pass

def stu_complete_info(req):
    pass

def stu_games(req):
    pass

def stu_join(req):
    pass

def stu_new_game_info(req):
    pass

def stu_old_game_info(req):
    pass

def stu_event(req):
    pass

def stu_center(req):
    pass

def g_sign_up(req):
    pass

def g_games(req):
    pass

def g_join(req):
    pass

def g_new_game_info(req):
    pass

def g_old_game_info(req):
    pass

def g_event(req):
    pass

def g_center(req):
    pass

def a_games(req):
    pass

def a_publish(req):
    pass

def a_game_admin(req):
    pass

def a_group_check(req):
    pass

def a_group_detail(req):
    pass

def a_score_elist(req):
    pass

def a_score_event(req):
    pass

def a_score_group(req):
    pass

def a_center(req):
    pass

def a_old_game_info(req):
    pass

