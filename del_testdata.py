
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import django

def delete():
    u = MyUser.objects.filter(phone="15110099952")
    UserRole.objects.filter(user=u).delete()
    Coach.objects.filter(property__user=u).delete()
    Student.objects.filter(property__user=u).delete()
    Club.objects.filter(user=u).delete()
    Group.objects.filter(user=u).delete()
    u.delete()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sunny_sports.settings")
    django.setup()

    import datetime
    from sp.models import *
    from sp.models.models import *

    from game.models import *
    from club.models import *
    from group.models import *
    from student.models import *

    delete()
    
