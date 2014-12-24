# -*- coding:utf-8 -*-

from django.forms import ModelForm
from django import forms
from sunny_sports.sp.models.models import *

class LoginForm(forms.Form):
    username = forms.CharField(label='昵称/手机号码', max_length=255)
    password = forms.CharField(label='密码', max_length=255)
    v_code = forms.CharField(label='验证码', max_length=10)
