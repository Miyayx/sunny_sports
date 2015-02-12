#-*-coding:utf-8-*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from . import views

import os

urlpatterns = patterns('',
        url(r'^$', 'sunny_sports.views.login'),
        #url(r'^favicon.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/clear.png'}),
        url(r'^login$', 'sunny_sports.sp.views.mylogin'),
        url(r'^register$', 'sunny_sports.sp.views.regist'),
        url(r'^logout$', 'sunny_sports.sp.views.mylogout'),
        url(r'^vcode$', 'sunny_sports.sp.views.vcode'),
        url(r'^password$', 'sunny_sports.sp.views.password'),
        url(r'^student/', TemplateView.as_view(template_name='student/empty.html')),
        url(r'^judge/', TemplateView.as_view(template_name='judge/empty.html')),
        url(r'^club/', TemplateView.as_view(template_name='club/empty.html')),
        url(r'^team/', TemplateView.as_view(template_name='team/empty.html')),
        url(r'^committee/', TemplateView.as_view(template_name='committee/empty.html')),

        url(r'^msg$','sunny_sports.sp.views.get_msg'),

        url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'static')}),

        url(r'^admin/', include(admin.site.urls)),
        )

# centre
urlpatterns += patterns('sunny_sports.sp.centre_views',
        url(r'^centre$', 'centre'),
        url(r'^centre/test_check/$','test_check'),
        #url(r'^centre/test_check/(?P<train_id>\d{9-10})/$','test_check'),
        url(r'^centre/test_check/(?P<train_id>\d+)/$','test_check'),
        url(r'^centre/check_pass$','check_pass'),
        url(r'^centre/history_view$','history_view'),
        #url(r'^centre/history_view/(?P<train_id>\d{10})/$','history_view'),
        url(r'^centre/history_view/(?P<train_id>\d+)/$','history_view'),
        url(r'^centre/msg_publish$','msg_publish'),
        #url(r'^centre/', views.all),
        )

# coach_org
urlpatterns += patterns('sunny_sports.sp.coach_org_views',
        url(r'^coach_org$', 'coach_org'),
        url(r'^coach_org/home$', 'home'),
        url(r'^coach_org/train_query$', 'train'),
        url(r'^coach_org/center$', 'center'),
        url(r'^coach_org/train_publish$', 'train_publish'),
        url(r'^coach_org/up_info$', 'update_info'),
        )

# coach
urlpatterns += patterns('sunny_sports.sp.coach_views',
        url(r'^coach$', 'coach'),
        url(r'^coach/home$', 'home'),
        url(r'^coach/center$', 'center'),
        url(r'^coach/train$', 'train'),
        url(r'^coach/up_user$', 'update_info'),

        )
