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
        url(r'^service_term$', TemplateView.as_view(template_name='service_term.html')),
        url(r'^download$', 'sunny_sports.sp.views.download_excel'),
        url(r'^student/', TemplateView.as_view(template_name='student/empty.html')),
        url(r'^judge/', TemplateView.as_view(template_name='judge/empty.html')),
        url(r'^club/', TemplateView.as_view(template_name='club/empty.html')),
        url(r'^team/', TemplateView.as_view(template_name='team/empty.html')),
        url(r'^committee/', TemplateView.as_view(template_name='committee/empty.html')),

        url(r'^msg$','sunny_sports.sp.views.get_msg'),

        url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'static')}),

        url(r'^admin/', include(admin.site.urls)),
        )


urlpatterns += patterns('',
            url(r'^captcha/', include('captcha.urls')),
            )

urlpatterns += patterns('sunny_sports.sp.validate',
            url(r'^validate/phone', 'is_phone_exists'),
            )

# centre
urlpatterns += patterns('sunny_sports.sp.centre_views',
        url(r'^centre$', 'centre'),
        url(r'^centre/test_check/$','test_check'),
        #url(r'^centre/test_check/(?P<train_id>\d{9-10})/$','test_check'),
        #url(r'^centre/test_check/(?P<train_id>\d+)/$','test_check'),
        url(r'^centre/check_pass$','check_pass'),
        url(r'^centre/history_view$','history_view'),
        url(r'^centre/msg_publish$','msg_publish'),
        url(r'^centre/org_manage$', 'org_manage'),
        url(r'^centre/org_del$', 'org_del'),
        url(r'^centre/org_info$', 'org_info'),
        url(r'^centre/password$','password_page'),
        )

# coach_org
urlpatterns += patterns('sunny_sports.sp.coach_org_views',
        url(r'^coach_org$', 'coach_org'),
        url(r'^coach_org/home$', 'home'),
        url(r'^coach_org/train_query$', 'train'),
        url(r'^coach_org/center$', 'center'),
        url(r'^coach_org/train_publish$', 'train_publish'),
        url(r'^coach_org/train_manage$', 'train_manage'),
        url(r'^coach_org/score_input$', 'score_input'),
        url(r'^coach_org/up_info$', 'update_info'),
        url(r'^coach_org/add_member$', 'add_member'),
        url(r'^coach_org/del_member$', 'del_member'),
        )

# coach
urlpatterns += patterns('sunny_sports.sp.coach_views',
        url(r'^coach$', 'coach'),
        url(r'^coach/home$', 'home'),
        url(r'^coach/center$', 'center'),
        url(r'^coach/train$', 'train'),
        url(r'^coach/train/info_confirm$', 'info_confirm'),
        url(r'^coach/train/reg_cancel$', 'reg_cancel'),
        url(r'^coach/train/payment$', 'payment'),
        url(r'^coach/up_info$', 'update_info'),

        )
