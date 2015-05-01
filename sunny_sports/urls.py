#-*-coding:utf-8-*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from . import settings

import os

urlpatterns = patterns('',
        url(r'^$', 'sp.views.mylogin'),
        url(r'^/$', 'sp.views.mylogin'),
        #url(r'^favicon.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/clear.png'}),
        url(r'^login$', 'sp.views.mylogin'),
        url(r'^signup$', 'sp.views.signup'),
        url(r'^logout$', 'sp.views.mylogout'),
        url(r'^vcode$', 'sp.views.vcode'),
        url(r'^find_password$', 'sp.views.find_password'),
        url(r'^reset_password$', 'sp.views.reset_password'),
        url(r'^password$', 'sp.views.password'),
        url(r'^service_term$', TemplateView.as_view(template_name='service_term.html')),
        url(r'^download$', 'sp.views.download_excel'),
        url(r'^dl_qual$', 'sp.views.download_qualification'),
        url(r'^train_info$', 'sp.views.train_info'),
        url(r'^coach_info$', 'sp.views.coach_info'),
        url(r'^inbox$', 'sp.views.inbox'),

        url(r'^student/', TemplateView.as_view(template_name='student/empty.html')),
        url(r'^club/', TemplateView.as_view(template_name='club/empty.html')),
        url(r'^team/', TemplateView.as_view(template_name='team/empty.html')),
        url(r'^committee/', TemplateView.as_view(template_name='committee/empty.html')),

        url(r'^msg$','sp.views.get_msg'),
        url(r'^get_captcha$','sp.views.get_captcha'),

        url(r'^tutorial/coach$', 'sp.help_views.coach_help'),

        url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'static')}),
        url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
        url(r'^admin/', include(admin.site.urls)),
        )


urlpatterns += patterns('',
            url(r'^captcha/', include('captcha.urls')),
            )

urlpatterns += patterns('sp.validate',
            url(r'^validate/phone', 'is_phone_exists'),
            url(r'^validate/nickname', 'is_nickname_exists'),
            url(r'^validate/shortname', 'is_orgshortname_exists'),
            url(r'^validate/email', 'is_email_exists'),
            )

# centre
urlpatterns += patterns('sp.centre_views',
        url(r'^centre$', 'centre'),
        url(r'^centre/train_check$','train_check'),
        url(r'^centre/train_pass$','train_pass'),
        url(r'^centre/test_check$','test_check'),
        #url(r'^centre/test_check/(?P<train_id>\d{9-10})/$','test_check'),
        #url(r'^centre/test_check/(?P<train_id>\d+)/$','test_check'),
        url(r'^centre/check_pass$','check_pass'),
        url(r'^centre/current_view$','current_view'),
        url(r'^centre/history_view$','history_view'),
        url(r'^centre/msg_publish$','msg_publish'),
        url(r'^centre/org_manage$', 'org_manage'),
        url(r'^centre/org_del$', 'org_del'),
        url(r'^centre/org_info$', 'org_info'),
        url(r'^centre/password$','password_page'),
        )

# coach_org
urlpatterns += patterns('sp.coach_org_views',
        url(r'^coach_org$', 'coach_org'),
        url(r'^coach_org/home$', 'home'),
        url(r'^coach_org/train_query$', 'train'),
        url(r'^coach_org/center$', 'center'),
        url(r'^coach_org/train_publish$', 'train_publish'),
        url(r'^coach_org/train_edit$', 'train_publish'),
        url(r'^coach_org/train_manage$', 'train_manage'),
        url(r'^coach_org/score_input$', 'score_input'),
        url(r'^coach_org/up_info$', 'update_info'),
        url(r'^coach_org/add_member$', 'add_member'),
        url(r'^coach_org/del_member$', 'del_member'),
        )

# coach
urlpatterns += patterns('sp.coach_views',
        url(r'^coach$', 'coach'),
        url(r'^coach/home$', 'home'),
        url(r'^coach/center$', 'center'),
        url(r'^coach/train$', 'train'),
        url(r'^coach/train/info_confirm$', 'info_confirm'),
        url(r'^coach/train/reg_cancel$', 'reg_cancel'),
        url(r'^coach/train/pay$', 'pay'),
        url(r'^coach/train/pay_notify$', 'pay_notify'),
        url(r'^coach/train/pay_return$', 'pay_return'),
        url(r'^coach/up_info$', 'update_info'),
        url(r'^coach/up_img$', 'update_img'),
        )
