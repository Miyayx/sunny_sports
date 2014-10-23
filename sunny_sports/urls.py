from django.conf.urls import patterns, include, url
from django.contrib import admin

import os

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'sunny_sports.views.login', name='login'),
     url(r'^favicon.ico$', 'sunny_sports.views.home'),
     url(r'^admin/score_event_person', 'sunny_sports.views.a_score_event_person'),
     url(r'^admin/score_event_group', 'sunny_sports.views.a_score_event_group'),
     url(r'^admin/group_detail', 'sunny_sports.views.a_group_detail'),
     url(r'^w*', 'sunny_sports.views.all', name='all'),
     #url(r'^blog/', include('blog.urls')),
     #url(r'^student/', include('student.urls')),
     #url(r'^group/', include('group.urls')),
     #url(r'^admin_/', include('admin_.urls')),
     url(r'login','sunny_sports.views.login'),
     url(r'password','sunny_sports.views.password'),
     url(r'^student$', 'sunny_sports.views.stu_games'),
     url(r'^student/sign_up$', 'sunny_sports.views.stu_sign_up'),
     url(r'^student/complete_info$', 'sunny_sports.views.stu_complete_info'),
     url(r'^student/games$', 'sunny_sports.views.stu_games'),
     url(r'^student/join$', 'sunny_sports.views.stu_join'),
     url(r'^student/new_game$', 'sunny_sports.views.stu_new_game_info'),
     url(r'^student/old_game$', 'sunny_sports.views.stu_old_game_info'),
     url(r'^student/event$', 'sunny_sports.views.stu_event'),
     url(r'^student/center$', 'sunny_sports.views.stu_center'),

     ### 参赛队 ###
     url(r'^group/sign_up$', 'sunny_sports.views.g_sign_up'),
     url(r'^group/games$', 'sunny_sports.views.g_games'),
     url(r'^group/join$', 'sunny_sports.views.g_join'),
     url(r'^group/new_game$', 'sunny_sports.views.g_new_game_info'),
     url(r'^group/old_game$', 'sunny_sports.views.g_old_game_info'),
     url(r'^group/event$', 'sunny_sports.views.g_event'),
     url(r'^group/center$', 'sunny_sports.views.g_center'),

     ### 管理员 ###
     url(r'^admin/games$', 'sunny_sports.views.a_games'),
     url(r'^admin/publish$', 'sunny_sports.views.a_publish'),
     url(r'^admin/game_admin$', 'sunny_sports.views.a_game_admin'),
     url(r'^admin/group_check$', 'sunny_sports.views.a_group_check'),
     url(r'^admin/group_detail$', 'sunny_sports.views.a_group_detail'),
     url(r'^admin/score_elist$', 'sunny_sports.views.a_score_elist'),
     url(r'^admin/score_group$', 'sunny_sports.views.a_score_group'),
     url(r'^admin/center$', 'sunny_sports.views.a_center'),
     url(r'^admin/old_game$', 'sunny_sports.views.a_old_game_info'),

     url(r'^static/(?P<path>.*)$)','django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'static')}),

    url(r'^admin/', include(admin.site.urls)),
)

