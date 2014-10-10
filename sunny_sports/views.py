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

