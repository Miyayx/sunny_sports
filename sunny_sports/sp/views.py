# -*- coding:utf-8-*-
from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
          
# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)
          
def regist(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            User.objects.create(username = username, password = password)
            return HttpResponseRedirect('/login/')
    else:
        uf = UserForm()
    return render_to_response('regist.html', {'uf': uf}, context_instance=RequestContext(req))
          
def login(req):
    c = {}
    c.update(csrf(req))
    if req.method == 'POST':
        username = req.POST.get('username','Unknow')              #用户名
        password = req.POST.get('password')                #密码
        role     = req.POST.get('role')                #
        #user = User.objects.filter(username = username, password = password, role=role)
        #if user:
        print role
        print req.POST.keys()
        req.session['username'] = username
        if role in ["student","coach","judge","club"]:
            return HttpResponseRedirect('/'+role)
        elif role == "admin":
            return HttpResponseRedirect('/'+role)
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
          
def index(req):
    username = req.session.get('username', 'anybody')
    return render_to_response('index.html', {'username': username}, context_instance=RequestContext(req))
          
def logout(req):
    session = req.session.get('username', False)
    if session:
        del req.session['username']
        return render_to_response('login.html',context_instance=RequestContext(req))
    else:
        return HttpResponse('please login!')

