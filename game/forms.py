#-*-coding:utf-8-*-
from django.forms import ModelForm, Textarea
from django import forms

from game.models import *

class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['game','contestant','name','leader','contact_name','contact_phone','contact_email','contact_qq','contact_wx','address','postno', 'other_info']

    def is_valid(self):
        if super(TeamForm, self).is_valid():
            return True
        return False

    def save(self, commit=True):
        instance = super(TeamForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance

class TeamContactForm(ModelForm):
    class Meta:
        model = Team
        fields = ['leader','contact_name','contact_phone','contact_email','contact_qq','contact_wx','address','postno', 'other_info']
        widgets = {
                'other_info': Textarea(attrs={'cols': 50, 'rows': 8, 'placeholder':'其他信息，如教练、医生等随队人员信息'}),
                }
        # Edit by bryan
    def __init__(self, *args, **kwargs):
        super(TeamContactForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['address'].widget.attrs['style'] = 'width:415px' 

