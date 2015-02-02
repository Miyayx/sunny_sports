#!/usr/bin/env python3

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse,HttpResponseRedirect
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

from .mapping import PAGE_MAPPING

def home(req):
    c = {}
    c.update(csrf(req))
    return render_to_response(PAGE_MAPPING["index"], c)

def all(req):
    url = req.path[req.path.index("/"):].strip("/")
    print ("url:",url)

    c = {}
    c.update(csrf(req))
    return render_to_response(PAGE_MAPPING[url], c)

def login(req):
    c = {}
    c.update(csrf(req))
    return render_to_response("login.html", c)

def a_group_detail(req):
    checked = int(req.GET['checked'])
    t = get_template("admin/group_detail.html")
    c = Context({'checked':checked})
    html = t.render(c)
    return HttpResponse(html)

def a_score_elist(req):
    pass

def a_score_event_group(req):
    event = req.GET['event']
    t = get_template("admin/score_event_group.html")
    c = Context({'event':event})
    html = t.render(c)
    return HttpResponse(html)

def a_score_event_person(req):
    event = req.GET['event']
    t = get_template("admin/score_event_person.html")
    c = Context({'event':event})
    html = t.render(c)
    return HttpResponse(html)

