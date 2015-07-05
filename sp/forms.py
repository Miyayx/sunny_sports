# -*- coding:utf-8 -*-

from django.forms import ModelForm
from django import forms
from django.forms.util import flatatt
from django.template import loader
from django.utils.datastructures import SortedDict
from django.utils.html import format_html, format_html_join
from django.utils.http import int_to_base36
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site

from captcha.fields import CaptchaField
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from sp.models.models import *
from sp.models import *
from game.models import *

from utils import *

class LoginForm(forms.Form):
    username = forms.CharField(label='昵称/手机号码', max_length=255)
    password = forms.CharField(label='密码', max_length=255)
    v_code = forms.CharField(label='验证码', max_length=10)

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set his/her password without entering the
    old password
    """
    error_messages = {
            'password_mismatch': _("The two password fields didn't match."),
            }
    new_password1 = forms.CharField(label=_("New password"),
            widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
            widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                        self.error_messages['password_mismatch'])
                return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change his/her password by entering
    their old password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. "
            "Please enter it again."),
        })
    old_password = forms.CharField(label=_("Old password"),
            widget=forms.PasswordInput)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                    self.error_messages['password_incorrect'])
            return old_password

PasswordChangeForm.base_fields = SortedDict([
    (k, PasswordChangeForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
    ])


class AdminPasswordChangeForm(forms.Form):
    """
    A form used to change the password of a user in the admin interface.
    """
    error_messages = {
            'password_mismatch': _("The two password fields didn't match."),
            }
    password1 = forms.CharField(label=_("Password"),
            widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password (again)"),
            widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AdminPasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                        self.error_messages['password_mismatch'])
                return password2

    def save(self, commit=True):
        """
        Saves the new password.
        """
        self.user.set_password(self.cleaned_data["password1"])
        if commit:
            self.user.save()
        return self.user

class MessagePublishForm(forms.Form):
    stu   = forms.BooleanField(initial=False, required=False)
    coach = forms.BooleanField(initial=False, required=False)
    stuorg   = forms.BooleanField(initial=False, required=False)
    coachorg = forms.BooleanField(initial=False, required=False)
    gameorg = forms.BooleanField(initial=False, required=False)
    title = forms.CharField(max_length=100)
    content = forms.CharField(max_length=1000)

   # def clean(self):
   #     """
   #     因为checkbox控件有点特殊，直接validate会不通过
   #     """
   #     cleaned_data = super(MessagePublishForm, self).clean()
   #     stu = cleaned_data.get("stu", False)
   #     coach = cleaned_data.get("coach", False)

   #     title = cleaned_data.get("title",None)
   #     if not title:
   #        raise forms.ValidationError("No Title")
   #     content = cleaned_data.get("content","")
   #     print cleaned_data
   #     return True

    def save(self):
        #消息写入数据库，选择所有学员则给所有学员与这个消息一个关联关系，教练与裁判同理
        data = self.cleaned_data

        user_list = []
        print len(user_list)
        if data.get('stu',False):
            user_list += MyUser.objects.filter(role=2)
            print len(user_list)
        if data.get('coach',False):
            user_list += MyUser.objects.filter(role=3)
            print len(user_list)

        #utils.py里
        custom_msg_publish(user_list, data['title'], data.get('content',''))

class TrainPublishForm(ModelForm):
    class Meta:
        model = Train
        fields = ['org','name','demo','address','level','limit','money','reg_stime','reg_etime','train_stime','train_etime']

    def is_valid(self):
        if super(TrainPublishForm, self).is_valid():
            if self.cleaned_data['reg_stime'] > self.cleaned_data['reg_etime']:
                self._errors['time_error'] = u"结束时间早于开始时间"
                print self._errors['time_error']
                return False
            elif self.cleaned_data['reg_etime'] > self.cleaned_data['train_stime']:
                self._errors['time_error'] = u"培训时间早于报名时间"
                print self._errors['time_error']
                return False
            elif self.cleaned_data['train_stime'] > self.cleaned_data['train_etime']:
                self._errors['time_error'] = u"结束时间早于开始时间"
                print self._errors['time_error']
                return False
            return True
        else:
            return False

    def save(self, commit=True):
        instance = super(TrainPublishForm, self).save(commit=False)
        instance.reg_status = 1 if instance.reg_stime < timezone.now() and instance.pass_status else 0
        if commit:
            instance.save()
        return instance

class GamePublishForm(ModelForm):
    class Meta:
        model = Game
        fields = ['org','name','description','sponsor','organizer','coorganizer', 'schedule', 'province', 'city', 'dist', 'address', 'events', 'limit','male_num','female_num', 'money','reg_place', 'reg_stime','reg_etime','game_stime','game_etime', 'contact_name', 'contact_phone', 'contact_email']

    def is_valid(self):
        if super(GamePublishForm, self).is_valid():
            if self.cleaned_data['reg_stime'] > self.cleaned_data['reg_etime']:
                self._errors['time_error'] = u"结束时间早于开始时间"
                print self._errors['time_error']
                return False
            elif self.cleaned_data['reg_etime'] > self.cleaned_data['game_stime']:
                self._errors['time_error'] = u"比赛时间早于报名时间"
                print self._errors['time_error']
                return False
            elif self.cleaned_data['game_stime'] > self.cleaned_data['game_etime']:
                self._errors['time_error'] = u"结束时间早于开始时间"
                print self._errors['time_error']
                return False
            return True
        else:
            return False

    def save(self, commit=True):
        instance = super(GamePublishForm, self).save(commit=False)
        instance.reg_status = 1 if instance.reg_stime < timezone.now() and instance.pass_status else 0
        if commit:
            instance.save()
        return instance

class CoachPropertyForm(ModelForm):
    class Meta:
        model = CoachProperty
        fields = ['name','sex','identity','avatar','company','province','city','dist','address']

#验证码
class CaptchaForm(forms.Form):
    captcha = CaptchaField()

    def is_valide(self):
        self.cleaned_data['captcha'] = self.cleaned_data['captcha'].upper()
        print self.cleaned_data
        return super(CaptchaForm, self).is_valid()

class CustomCaptcha():
    def __init__(self, hidden_input_id, input_id, img_id):
        self.hidden_input_id = hidden_input_id
        self.input_id =  input_id
        self.img_id = img_id
        self.cptch_key = CaptchaStore.generate_key()
        print self.cptch_key
        self.cptch_img = captcha_image_url(self.cptch_key)
        print self.cptch_img
    
     
