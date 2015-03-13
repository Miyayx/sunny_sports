# -*- coding:utf-8 -*-
import json

from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.template import Context, Template
from django.core.context_processors import csrf
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import F

from sp.models import *
from sp.models.association import *
from sp.models.role import *
from sp.models.models import *
from sp.models.status import *
from sp.forms import *
