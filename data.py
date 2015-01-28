#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import django

def init():
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
    
    u0 = MyUser.objects.create_superuser("00000", "centre", "", role=0, password="centre")
    u1 = MyUser.objects.create_user("11111", "org1","org1@test.com", 1, "org")
    u11 = MyUser.objects.create_user("111111", "org2","org2@test.com", 1, "org")
    u2 = MyUser.objects.create_user("22222", "student","student@test.com", 2, "student")
    u3 = MyUser.objects.create_user("33333", "coach","coach@test.com", 3, "coach")
    u4 = MyUser.objects.create_user("44444", "judge","judge@test.com", 4, "judge")
    u5 = MyUser.objects.create_user("55555", "club","club@test.com", 5, "club")
    u1 = MyUser.objects.get(phone="11111")
    u11 = MyUser.objects.get(phone="111111")
    u3 = MyUser.objects.get(phone="33333")
    
    coach_p = role.CoachProperty(user=u3, name="kkk", sex=0, birthday="1990-9-8", identity="1234567890")
    coach_p.save()
    
    c1 = role.Coach(property=coach_p, t_level=3, p_level=3)
    c1.save()
    
    org1 = role.CoachOrg(user=u1, org_num="org111", org_name=u"南方机构", province=u"北京", city=u"北京市", county=u"海淀区",address=u"西土城路15号")
    org1.save()
    org2 = role.CoachOrg(user=u11, org_num="org222", org_name=u"北方机构") #注意导入中文的时候要加unicode转码，不然admin页面大不开呢
    org2.save()
    
    train1 = train.Train(org=org1, name=u"2013年第一次培训", address=u"北京体育中心", level=3, max=10, money=200, reg_stime="2015-04-01", reg_etime="2015-04-15", train_stime="2015-05-01")
    train1.save()
    
    c_t = association.CoachTrain(coach=c1, train=train1)
    c_t.save()
    
def new_data():
    #pass #新数据的添加写在这里，把pass删掉
    org1 = CoachOrg.objects.filter(id=1)
    org2 = CoachOrg.objects.filter(id=2)
    train1 = train.Train(org=org2[0], name=u"2013年第二次培训", address=u"北京体育中心", level=3, max=10, money=200, reg_stime="2013-10-01", reg_etime="2013-10-15", train_stime="2013-11-01")
    train1.save()
    train2 = train.Train(org=org1[0], name=u"2014年第一次培训", address=u"北京体育中心", level=2, max=20, money=300, reg_stime="2014-04-01", reg_etime="2014-04-15", train_stime="2014-05-01")
    train2.save()
    train3 = train.Train(org=org2[0], name=u"2014年第二次培训", address=u"北京体育中心", level=2, max=20, money=300, reg_stime="2014-10-01", reg_etime="2014-10-15", train_stime="2014-11-01")
    train3.save()
    train4 = train.Train(org=org1[0], name=u"2015年第一次培训", address=u"北京体育中心", level=1, max=30, money=500, reg_stime="2015-04-01", reg_etime="2015-04-15", train_stime="2015-05-01")
    train4.save()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sunny_sports.settings")
    django.setup()

    import datetime
    from sunny_sports.sp.models import *
    from sunny_sports.sp.models.models import *

    #init()
    new_data()
    
