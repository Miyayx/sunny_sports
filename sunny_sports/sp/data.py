#-*- coding:utf-8 -*-

import datetime
from sunny_sports.sp.models import *
from sunny_sports.sp.models.models import *

r0 = Role(0)
r0.save()
r1 = Role(1)
r1.save()
r2 = Role(2)
r2.save()
r3 = Role(3)
r3.save()
r4 = Role(4)
r4.save()
r5 = Role(5)
r5.save()

#u0 = MyUser.objects.create_superuser("00000", "centre", "", 0, "centre")
#u1 = MyUser.objects.create_user("11111", "org1","org1@test.com", 1, "org")
#u11 = MyUser.objects.create_user("111111", "org2","org2@test.com", 1, "org")
#u2 = MyUser.objects.create_user("22222", "student","student@test.com", 2, "student")
#u3 = MyUser.objects.create_user("33333", "coach","coach@test.com", 3, "coach")
#u4 = MyUser.objects.create_user("44444", "judge","judge@test.com", 4, "judge")
#u5 = MyUser.objects.create_user("55555", "club","club@test.com", 5, "club")
u1 = MyUser.objects.get(phone="11111")
u11 = MyUser.objects.get(phone="111111")
u3 = MyUser.objects.get(phone="33333")

coach_p = role.CoachProperty(user=u3, name="kkk", sex=0, birthday="1990-9-8", identity="1234567890")
coach_p.save()

c1 = role.Coach(property=coach_p, t_level=3, p_level=3)
c1.save()

org1 = role.CoachOrg(user=u1, org_num="org111", org_name="南方机构")
org1.save()

org2 = role.CoachOrg(user=u11, org_num="org222", org_name="北方机构")
org2.save()

train1 = train.Train(org=org1, name=u"2013年第一次培训", address=u"北京体育中心", level=3, max=10, money=200, reg_stime="2015-04-01", reg_etime="2015-04-15", train_stime="2015-05-01")
train1.save()

c_t = association.CoachTrain(coach=c1, train=train1)
c_t.save()





