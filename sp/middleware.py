#!/usr/bin/python
#-*- coding:utf-8 -*-

from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import logout


class AutoLogout:
    def process_request(self, request):
        if not request.user.is_authenticated() :
        #Can't log out if not logged in
            return
        try:
            if datetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
                logout(request)
                del request.session['last_touch']
                return
        except KeyError:
            pass
        request.session['last_touch'] = datetime.now()
