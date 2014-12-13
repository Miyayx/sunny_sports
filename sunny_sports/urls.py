#-*-coding:utf-8-*-
from django.conf.urls import patterns, include, url
from django.contrib import admin

import os

urlpatterns = patterns('',
        # Examples:
        url(r'^$', 'sunny_sports.views.login', name='login'),
        url(r'^favicon.ico$', 'sunny_sports.views.home'),
        url(r'^student/', direct_to_template, {'template':'student/empty.html'}),
        url(r'^judge/', direct_to_template, {'template':'judge/empty.html'}),
        url(r'^club/', direct_to_template, {'template':'club/empty.html'}),
        url(r'^group/', direct_to_template, {'template':'group/empty.html'}),
        url(r'^committee/', direct_to_template, {'template':'committee/empty.html'}),
        url(r'^coach/', include('coach/urls')),
        url(r'^centre/', include('centre/urls')),
        url(r'^coach_org/', include('coach_org/urls')),

        #url(r'^blog/', include('blog.urls')),

        url(r'^admin_/', include('admin_.urls')),

        url(r'^static/(?P<path>.*)$)','django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'static')}),

        url(r'^admin/', include(admin.site.urls)),
        )

