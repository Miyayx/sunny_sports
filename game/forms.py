#-*-coding:utf-8-*-
from django.forms import ModelForm
from django import forms

from game.models import *

class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['game','contestant','name','leader','contact_name','contact_phone','contact_email','contact_qq','contact_wx','address','postno']

    def is_valid(self):
        if super(TeamForm, self).is_valid():
            return True
        return False

    def save(self, commit=True):
        instance = super(TeamForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance
