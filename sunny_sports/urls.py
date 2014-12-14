#-*-coding:utf-8-*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

import os

urlpatterns = patterns('',
        # Examples:
        url(r'^$', 'sunny_sports.views.login', name='login'),
        url(r'^favicon.ico$', 'sunny_sports.views.home'),
        url(r'^student/', TemplateView.as_view(template_name='student/empty.html')),
        url(r'^judge/', TemplateView.as_view(template_name='judge/empty.html')),
        url(r'^club/', TemplateView.as_view(template_name='club/empty.html')),
        url(r'^team/', TemplateView.as_view(template_name='team/empty.html')),
        url(r'^committee/', TemplateView.as_view(template_name='committee/empty.html')),
        url(r'^coach$', TemplateView.as_view(template_name='coach/home.html')),
        url(r'^centre$', TemplateView.as_view(template_name='centre/home.html')),
        url(r'^coach_org$', TemplateView.as_view(template_name='coach_org/home.html')),

        #url(r'^blog/', include('blog.urls')),

        url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'static')}),

        url(r'^admin/', include(admin.site.urls)),
        )

