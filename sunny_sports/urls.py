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
        url(r'^morerole$', 'sp.views.more_role'),
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

        #url(r'^student/', include('student.urls')),
        url(r'^team/', TemplateView.as_view(template_name='team/empty.html')),
        url(r'^committee/', TemplateView.as_view(template_name='committee/empty.html')),

        url(r'^msg$','sp.views.get_msg'),
        url(r'^switch$','sp.views.get_otherrole'),
        url(r'^get_captcha$','sp.views.get_captcha'),

        url(r'^tutorial/coach$', 'sp.help_views.coach_help'),

        url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'static')}),
        #url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
        url(r'^photo/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.PHOTO_ROOT}),
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

        url(r'^centre/game_check$','game_check'),
        url(r'^centre/game_val$','game_val'),
        url(r'^centre/current_game$','current_game'),
        url(r'^centre/history_game$','history_game'),

        url(r'^centre/msg_publish$','msg_publish'),
        url(r'^centre/coach_org_manage$', 'coach_org_manage'),
        url(r'^centre/game_org_manage$', 'game_org_manage'),
        url(r'^centre/org_del$', 'org_del'),
        url(r'^centre/org_info$', 'org_info'),
        url(r'^centre/password$','password_page'),
        url(r'^centre/ch_payment_st$','change_payment_status'),
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

# game_org
urlpatterns += patterns('sp.game_org_views',
        url(r'^game_org$', 'game_org'),
        url(r'^game_org/home$', 'home'),
        url(r'^game_org/center$', 'center'),
        url(r'^game_org/history_game$', 'game_history'),
        url(r'^game_org/game_publish$', 'game_publish'),
        url(r'^game_org/game_edit$', 'game_publish'),
        url(r'^game_org/game_manage$', 'game_manage'),
        url(r'^game_org/result_input$', 'result_input'),
        url(r'^game_org/up_info$', 'update_info'),
        url(r'^game_org/del_team$', 'del_team'),
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

# student
urlpatterns += patterns('student.views',
        url(r'^student$', 'student'),
        url(r'^student/home$', 'home'),
        url(r'^student/cur_game$', 'current_game'),
        url(r'^student/history_game$', 'history_game'),
        url(r'^student/center$', 'center'),
        url(r'^student/up_info$', 'update_info'),
        url(r'^student/up_img$', 'update_img'),
        )

# club
urlpatterns += patterns('club.views',
        url(r'^club$', 'club'),
        url(r'^club/home$', 'home'),
        url(r'^club/cur_game$', 'current_game'),
        url(r'^club/cur_game/(?P<g_id>\w+)$','current_game'),
        url(r'^club/cur_game/(?P<g_id>\w+)/(?P<t_id>\w+)$','current_game'),
        url(r'^club/game_apply/(?P<g_id>\w+)$','game_apply'),
        url(r'^club/game_apply$','game_apply'),
        url(r'^club/history_game$', 'history_game'),
        url(r'^club/center$', 'center'),
        url(r'^club/up_info$', 'update_info'),
        )

# group
urlpatterns += patterns('group.views',
        url(r'^group$', 'group'),
        url(r'^group/home$', 'home'),
        url(r'^group/cur_game$', 'current_game'),
        url(r'^group/cur_game/(?P<g_id>\w+)$','current_game'),
        url(r'^group/cur_game/(?P<g_id>\w+)/(?P<t_id>\w+)$','current_game'),
        url(r'^group/game_apply/(?P<g_id>\w+)$','game_apply'),
        url(r'^group/game_apply$','game_apply'),
        url(r'^group/history_game$', 'history_game'),
        url(r'^group/center$', 'center'),
        url(r'^group/up_info$', 'update_info'),
        )
#game
urlpatterns += patterns('game.views',
        url(r'^game/pay/(?P<t_id>\w+)$','pay'),
        url(r'^game/pay$','pay'),
        url(r'^game/pay_notify$', 'pay_notify'),
        url(r'^game/pay_return$', 'pay_return'),
        url(r'^find_stu/(?P<phone>\w+)', 'find_stu'),
        url(r'^game/add_stu$','add_member'),
        url(r'^game/del_stu$','del_member'),
        url(r'^game/edit_stu$','edit_member'),
        url(r'^game/reg_cancel$','reg_cancel'),
        )
