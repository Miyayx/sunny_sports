# -*- coding:utf-8 -*-
from g_import import *
from django.core.context_processors import csrf

@login_required()
@transaction.atomic
def centre(req):
    return render_to_response('centre/base.html')

@login_required()
@transaction.atomic
def test_check(req, train_id=None):
    """
    待审核页面
    """
    if req.method == "GET":
        train_id = req.GET.get("t_id",None)
        print "test_check, id %s"%train_id
        if train_id and len(train_id) > 0: #有编号的话就返回对应培训的人名单
            c_t = CoachTrain.objects.filter(train_id=train_id, train__pub_status=0, train__sub_status=1, status__gt=0) #已提交但未发表
            #train = Train.objects.get(id=train_id)
            #filter return a list
            #get return an item
            if len(c_t) > 0:
                train = c_t[0].train
                return render_to_response('centre/test_check2.html',{"c_t":c_t, "train":train})
            else:
                return HttpResponse("<h2>没有该培训的审核请求</h2>")
        else:#否则返回待审核列表
            ctlist = Train.objects.filter(pub_status=0, sub_status=1).order_by('train_stime') #这里查的是Train的status，是联合两个表的查询，用两个_
            jtlist = []
            return render_to_response('centre/test_check.html',{"ctlist":ctlist, "jtlist":jtlist})

@login_required()
@transaction.atomic
def check_pass(req):
    """
    审核批准后
    """
    if req.method == "POST":
        t_id = req.POST.get("t_id")
        if int(req.POST.get("pass", 0)): #审核通过
            train = Train.objects.filter(id=t_id)
            train.update(pub_status=1)
            train.update(sub_status=1)
            # generate certificate
            #ns = json.loads(req.POST.get("cert","")).keys() #get number list获得审核通过的学号列表 
            ids = json.loads(req.POST.get("ids","")) #get number list获得审核通过的学号列表 
            #not_pass_c_t = CoachTrain.objects.filter(train_id=t_id).exclude(number__in=ns)
            pass_c_t = CoachTrain.objects.filter(id__in=ids, train_id=t_id, status__gt=0)            
            if len(pass_c_t):
                #pass_c_t.update(get_time=datetime.datetime.now(), pass_status=1)
                cur = CoachTrain.objects.filter(pass_status=1, train__level=train.level).count()
                for i in range(len(pass_c_t)):
                    pass_c_t[i].check_pass(cert=cur+i+1) #编号从1开始计数
                    coach = pass_c_t[i].coach
                    coach.t_level = train[0].level
                    coach.save()

            # 发布消息通知
            title = u"考试结果"
            content = u"恭喜培训%s考试通过"%t_id
        else: #审核不通过
            Train.objects.filter(id=t_id).update(sub_status=2)
            Train.objects.filter(id=t_id).update(pub_status=0)
        return JsonResponse({"success":True})
    else:
        return JsonResponse({"success":False})


@login_required()
@transaction.atomic
def history_view(req):
    if req.method == "GET":
        train_id = req.GET.get("t_id",None)
        if train_id and len(train_id) > 0: #有编号的话就返回对应培训的人名单
            c_t = CoachTrain.objects.filter(train_id=train_id, train__pub_status=1, status__gt=0)
            if len(c_t) > 0:
                train = c_t[0].train
                return render_to_response('centre/history_view2.html',{"c_t":c_t, "train":train, "base":"./centre/base.html"})
            else:
                return HttpResponse("<h2>没有该培训的历史信息</h2>")
        else:#否则返回培训列表
            ctlist = Train.objects.filter(pub_status=1).order_by('-train_stime')
            jtlist = []
            return render_to_response('centre/history_view.html',{"ctlist":ctlist, "jtlist":jtlist})

@login_required()
@transaction.atomic
def current_view(req):
    if req.method == "GET":
        trains = Train.objects.filter(pub_status=0).exclude(sub_status=1).order_by('train_stime') #未提交审核的，未成历史的
        return render_to_response('centre/current_view.html',{"trains":trains})

@login_required()
def history_print(req, train_id=None):
    """
    生成csv表格并下载
    """
    if train_id and len(train_id) > 0:
        return csv_generate()
    else:
        return "Wrong Train id"

@login_required()
@transaction.atomic
def msg_publish(req):
    """
    """
    if req.method == 'POST': #如果是提交表单内容
        print req.POST
        post = req.POST.copy()
        if post.get("stu", False):
            post["stu"] = True
        if post.get("coach", False):
            post["coach"] = True
        if post.get("judge", False):
            post["judge"] = True
        print post
        form = MessagePublishForm(post)
        print form.is_valid()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("msg_publish")
    else: # GET 方法请求消息发送页面
        form = MessagePublishForm()
        return render_to_response('centre/msg_publish.html', {'form':form}, RequestContext(req))


@login_required()
def password_page(req):
    """
    """
    return render_to_response('centre/password.html', RequestContext(req))

@login_required()
@transaction.atomic
def org_manage(req):
    if req.method == "GET":
        orgs = CoachOrg.objects.all()
        return render_to_response('centre/org_manage.html', {"orgs":orgs}, RequestContext(req))

@login_required()
@transaction.atomic
def org_info(req):
    if req.method == "GET":
        num = req.GET.get("org_num")
        co = None
        if num:
            co = CoachOrg.objects.filter(org_num=num)
        if num and len(co) > 0:
            return render_to_response('centre/org_info.html', {"coachorg":co[0]}, RequestContext(req))
        else:
            return render_to_response('centre/org_info.html', {}, RequestContext(req))
    else:
        data = req.POST.copy()
        orgnum = data.get("orgnum")
        for k in ["orgnum",'phone','orgname']:
            if not data.has_key(k) or len(data[k].strip()) == 0:
                return JsonResponse({},status=400)
        co = CoachOrg.objects.filter(org_num=orgnum) | CoachOrg.objects.filter(user__phone=data.get('phone'))
        #如果数据库里没有记录，证明是添加新组织
        if len(co) == 0:
            print "add coachorg"
            phone = data.get('phone')
            r_id = 1
            user = MyUser.objects.create_user(phone = phone, nickname=orgnum, email=None, role=r_id, password = orgnum)
            co = CoachOrg(user=user)
        else:
            co = co[0]

        co.org_num = orgnum
        co.name = data["orgname"]
        co.shortname = data["orgshortname"]
        co.user.phone = data["phone"]
        if data.has_key("director"):
            co.director = data["director"]
        if data.has_key("province"):
            co.province = data.get("province","")
        if data.has_key("city"):
            co.city = data.get("city","")
        if data.has_key("dist"):
            co.dist = data.get("dist","")
        if data.has_key("address"):
            co.address = data.get("address","")
        try:
            co.save()
        except:
            return JsonResponse({'success':False})
        return JsonResponse({'success':True})

@login_required()
@transaction.atomic
def org_del(req):

    if req.method == "POST":
        orgnum = req.POST.get("orgnum")
        co = CoachOrg.objects.get(org_num=orgnum)        
        u = co.user
        print u
        co.delete()
        u.delete()
        return JsonResponse({'success':True})
    else:
        return JsonResponse({'success':False})

