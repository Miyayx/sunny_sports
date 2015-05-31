# -*- coding:utf-8 -*-

from django import forms
#头像上传
class UserForm(forms.Form):
    headImg = forms.FileField()

