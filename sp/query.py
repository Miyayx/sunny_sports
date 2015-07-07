
# -*- coding:utf-8 -*-

from g_import import *

from student.models import *

@login_required()
def find_stu(req, phone):
    print "phone-->"+phone
    try:
        st = Student.objects.get(property__user__phone=phone)
        return JsonResponse({'uuid':st.property.user.id, 'name':st.property.name})
    except Exception,e:
        print e
        return JsonResponse({})
        


