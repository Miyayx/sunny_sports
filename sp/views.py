
# -*- coding:utf-8 -*-

from g_import import *

from django import forms
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
#from django.contrib.auth import authenticate
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from sp.models.status import get_role_id
from sp.backend import MyBackend 

from student.models import *

from utils import *

# Create your views here.

#客户端提交的post如果不加这段，会出现403error  
@csrf_exempt  
def vcode(req):
    """
    获取验证码请求
    """
    phone = req.POST.get('phone').strip()
    form = CaptchaForm(req.POST)
    if not form.is_valid():
        print form.errors
        return JsonResponse({"msg":u"图形验证码错误"})
    if not phone or len(phone) == 0:
        return JsonResponse({"msg":u"手机号码错误"})
    result, code = send_vcode(phone)
    print phone
    print code
    c = Code(phone=phone,code=code)
    c.save()
    return JsonResponse(result)

@login_required()
def get_msg(req):
    """
    header部分获取未读消息
    """
    uuid = req.user.id
    r = req.session.get('role')
    print "role-->"+str(r)
    if uuid:
        msgs = UserMessage.objects.filter(userrole__user_id=uuid, userrole__role=r, checked=False)
        print len(msgs)
        html = render_to_string('base/msg.html', {'num':len(msgs), 'msgs': msgs[:5]})
        return HttpResponse(html)
    return None

@login_required()
def get_otherrole(req):
    """
    header部分角色切换
    """
    uuid = req.user.id
    r = req.session.get('role')
    print "role-->"+str(r)
    if uuid:
        roles = UserRole.objects.filter(user_id=uuid)
        if len(roles) > 1:
            roles = [role for role in roles if not role.role_id == r]
            html = render_to_string('base/switch.html', {'roles':roles})
            return HttpResponse(html)
        return HttpResponse("")
    return HttpResponse("")

@login_required()
def inbox(req):
    base = {1:"centre/base.html",2:"coach_org/base.html", 3:"coach/base.html"}
    uuid = req.user.id
    r = req.session.get('role')
    print "role-->"+str(r)
    if uuid:
        msgs = UserMessage.objects.filter(userrole__user_id=uuid, userrole__role=r)
        print len(msgs)
        return render_to_response('inbox.html', {'msgs': msgs[:10], "base":base[r]})
    return None


@transaction.atomic
def signup(req):
    if req.method == 'POST':
        req.session.clear()
        phone = req.POST.get('phone')
        password = req.POST.get('password')
        password2 = req.POST.get('password2')
        v_code    = req.POST.get('v_code')
        #检验手机验证码
        p, msg = check_vcode(phone, v_code)
        if not p:
            messages.error(req, msg,extra_tags='regist')
            return redirect('/#signup-box')
        #检验密码是否一致
        if not password == password2:
            messages.error(req, u"两次密码输入不一致",extra_tags='regist')
            return redirect('/#signup-box')

        role = req.POST.get('role2').strip()
        r_id = get_role_id(role)
        user = MyUser.objects.create_user(phone = phone, nickname=None, email=None, role=r_id, password = password)
        u = authenticate(username=phone, password=password)#用django自带函数检验
        if u is not None:
            # the password verified for the user
            if u.is_active:
                req.session['role'] = r_id
                login(req,u) #django自带的login将userid写入session,这步之前一定有authenticate
                return HttpResponseRedirect('/%s'%role)
        messages.error(req, u"用户身份验证错误",extra_tags='regist')
        return redirect('/#signup-box')
    else:
        return redirect('/')

@transaction.atomic
def mylogin(req): #登录view，跟自带的auth.login 区分开
    if req.method == 'POST':
        next_page = req.POST.get('next',None)
        req.session.clear()
        un = req.POST['username']
        pw = req.POST['password']
        role = req.POST.get('role',None)
        if not role:
            messages.error(req, u"请选择角色")
            return redirect('/')
            #return render_to_response("login.html", context_instance=RequestContext(req))
        user = None
        if un and len(un) >0: #如果用用户名
            #user = MyBackend().authenticate(username=un, password=pw)#用django自带函数检验
            user = authenticate(username=un.encode('utf-8'), password=pw)#用django自带函数检验
        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
                req.session['role'] = user.role.all()[0].role
                login(req,user) #django自带的login将userid写入session
                roles = [r.get_role_display() for r in user.role.all()] #all()是取多对多值的办法
                print "roles:",roles
                if role == "admin":
                    form = CaptchaForm(req.POST)
                    if not form.is_valid():
                        print form.errors
                        messages.error(req, u"图形验证码错误")
                        return redirect('/login')
                    if "centre" in roles:
                        return HttpResponseRedirect(next_page) if next_page and 'centre' in next_page else HttpResponseRedirect('/centre')
                    elif "coach_org" in roles:
                        if CoachOrg.objects.get(user=user).is_active:
                            return HttpResponseRedirect(next_page) if next_page and 'coach_org' in next_page else HttpResponseRedirect('/coach_org')
                        else:
                            messages.error(req, u"该机构已禁用")
                            mylogout(req)
                elif role in roles:
                    r_id = get_role_id(role)
                    req.session['role'] = r_id
                    return HttpResponseRedirect(next_page) if next_page and role in next_page else HttpResponseRedirect('/%s'%role)
                else:
                    messages.error(req, u"请选择正确的角色")
                #return render_to_response("login.html", context_instance=RequestContext(req))
                return redirect('/login')
            else:
                messages.error(req, "The password is valid, but the account has been disabled!")
                return redirect('/login')
        else:
        # the authentication system was unable to verify the username and password
            messages.error(req, u"用户名或密码错误")
            #return render_to_response("login.html", context_instance=RequestContext(req))
            return redirect('/login')
    else:
        print "login page"
        print req.GET.items()
        form1 = CustomCaptcha("hidden1", "captcha1", "captcha-img1")
        form2 = CustomCaptcha("hidden2", "captcha2", "captcha-img2")
        form3 = CustomCaptcha("hidden3", "captcha3", "captcha-img3")
        return render_to_response("login.html", { "form1":form1, "form2":form2, "form3":form3, "next":req.GET.get('next', None) }, context_instance=RequestContext(req))
          
def index(req):
    uuid = req.user.id
    name = req.user.name
    return render_to_response('index.html', {'username': name}, context_instance=RequestContext(req))

@transaction.atomic
def more_role(req):
    if req.method == "POST":
        req.session.clear()
        un = req.POST['phone']
        pw = req.POST['password']
        role = req.POST.get('role',None)
        if not role in ["coach","student","team","club"]:
            messages.error(req, u"请选择正确的角色")
            return redirect('/morerole')

        v_code    = req.POST.get('v_code')
        #检验手机验证码
        p, msg = check_vcode(un, v_code)
        if not p:
            messages.error(req, msg,extra_tags='regist')
            return redirect('/#signup-box')

        user = None
        if un and len(un) >0: #如果用用户名
            user = authenticate(username=un.encode('utf-8'), password=pw)#用django自带函数检验
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(req, user) #django自带的login将userid写入session
                roles = [r.get_role_display() for r in user.role.all()] #all()是取多对多值的办法
                print "roles:",roles
                if role in roles:
                    messages.error(req, u"该角色已注册")
                    mylogout(req)
                    return redirect('/morerole')
                r_id = get_role_id(role)
                UserRole.objects.create(role_id=r_id, user_id=user.id)
                if role == "coach":
                    print "Create Coach"
                    cp = CoachProperty(user=user)
                    cp.save()
                    Coach(property=cp).save()
                elif role == "student":
                    print "Create Student"
                    sp = StudentProperty(user=user)
                    sp.save()
                    Student(property=sp).save()
                elif role == "team":
                    pass
                elif role == "club":
                    pass
                return HttpResponseRedirect('/%s'%role)
            else:
                return redirect('/morerole')
        else:
        # the authentication system was unable to verify the username and password
            messages.error(req, u"用户名或密码错误")
            return redirect('/morerole')
    else:
        form1 = CustomCaptcha("hidden1", "captcha1", "captcha-img1")
        return render_to_response("more_role.html", {"form1":form1}, context_instance=RequestContext(req))
          
@login_required()
def mylogout(req):
    logout(req)
    #req.session.clear()
    return redirect('/login')

def find_password(req) :
    if req.method == 'POST':
        phone = req.POST['phone']
        code = req.POST['v_code']
        # 用手机短信验证码确认身份
        c = Code.objects.filter(phone = phone).latest('time')
        if c.code == code:
            return HttpResponseRedirect('reset_password?phone='+phone)
        else:
            messages.error(req, "验证码错误")
            #return render_to_response("login.html#forgot-box", context_instance=RequestContext(req))
            return HttpResponseRedirect('/#forgot-box')
    else:
        return render_to_response("login.html", context_instance=RequestContext(req))

def reset_password(req):
    if req.method == 'POST':
        phone = req.POST['phone']
        pds = PasswordDigitalSignature.objects.filter(phone = phone).latest('time')
        if pds.signature == req.POST['signature']:
            now = timezone.now()
            if pds.time < timezone.now() and pds.time + datetime.timedelta(0,900) > timezone.now(): #当前时间要在c.time与c.time+15min之间
                u = MyUser.objects.get(phone=req.POST['phone'])
                if not req.POST["password"] == req.POST["password2"]:
                    return JsonResponse({"success":False,"msg":u"新密码不一致"}) 

                new_pw = req.POST["password"]
                u.set_password(new_pw)
                u.save()
                return JsonResponse({"success":True,"msg":u"密码已修改"}) 
            else:
                return JsonResponse({"success":False,"msg":u"网页超时"}) 
        else:
            return JsonResponse({"success":False,"msg":u"网页地址有误"}) 
        
    else:
        phone = req.GET['phone']
        uuid = MyUser.objects.get(phone=phone).id
        key = str(timezone.now())+uuid
        import sha
        sig = sha.new(key).hexdigest()
        PasswordDigitalSignature.objects.create(phone=phone, signature=sig)
        return render_to_response("reset_password.html",{"signature":sig, "phone":phone}, context_instance=RequestContext(req))

@login_required()
def password(req):
    if req.method == 'POST': #Change password 
        u = MyUser.objects.get(id=req.user.id)
        pw = req.POST['old_password']
        user = MyBackend().authenticate(username=u.phone, password=pw)#用django自带函数检验
        if user is not None:
            if pw == req.POST['password']:
                return JsonResponse({"success":False,"msg":u"原密码与新密码相同"}) 
            if not req.POST["password"] == req.POST["password2"]:
                return JsonResponse({"success":False,"msg":u"新密码不一致"}) 

            # 用手机短信验证码确认身份
            #c = Code.objects.get(phone = u.phone).latest('time')
            #if c.code == req.POST.get("vcode",0):
            #    u.set_password(new_password)
            #    u.save()
            #    return JsonResponse({"success":True,"msg":""}) 
            #else:
            #    return JsonResponse({"success":False,"msg":u"验证码错误"}) 
            new_pw = req.POST["password"]
            u.set_password(new_pw)
            u.save()
            return JsonResponse({"success":True,"msg":u"密码已修改,请重新登录"}) 
        else:
            return JsonResponse({"success":False,"msg":u"密码错误"}) 

    else: #Get page
        u = MyUser.objects.get(id=req.user.id)
        return render_to_response('password.html', {"phone":u.phone}, RequestContext(req))

@login_required()
@user_passes_test(lambda u: u.is_role(['coach_org','centre']))
def download_excel(req):
    t_id = req.GET.get("t_id",0)
    if t_id:
        coachtrains = CoachTrain.objects.filter(train_id=t_id)
        if not len(coachtrains):
            return HttpResponse(u"该培训暂无学员报名，不提供名单")
        train = coachtrains[0].train
        if train.pub_status: #如果已经发布，包括是否通过，证书号
            fields = [u"学员姓名",  u"性别", u"联系方式", u"邮箱", u"出生日期", u"年龄", u"常驻地", u"工作单位", u"证书编号"]
            rows = [(ct.coach.property.name, ct.coach.property.get_sex_display(), ct.coach.property.user.phone, ct.coach.property.user.email, ct.coach.property.birth.strftime('%Y-%m-%d'), calculate_age(ct.coach.property.birth), join_position(ct.coach), ct.coach.property.company, ct.certificate) for ct in coachtrains]
        else:
            fields = [u"学员姓名",  u"性别", u"联系方式", u"邮箱", u"出生日期", u"年龄", u"常驻地", u"工作单位", u"付费状态"]
            rows = [(ct.coach.property.name, ct.coach.property.get_sex_display(), ct.coach.property.user.phone, ct.coach.property.user.email, ct.coach.property.birth.strftime('%Y-%m-%d'), calculate_age(ct.coach.property.birth), join_position(ct.coach), ct.coach.property.company, ct.get_status_display()) for ct in coachtrains]
        return export_xls(req, "%s-%s"%(train.id,train.name), fields, rows)

@login_required()
@user_passes_test(lambda u: u.is_role(['coach','coach_org','centre']))
def download_qualification(req):
    #证书下载
    from sp.tools import cufon
    cert = req.GET.get("cert",0)
    if cert:
        try:
            uuid = req.user.id
            roles = UserRole.objects.filter(user__id=uuid).values_list('role', flat=True)
            ct = CoachTrain.objects.get(certificate=cert, pass_status=1)
            if 0 in roles or 1 in roles: #如果是管理员级别的
                js = cufon.get_js(ct.coach.property.name)
                print js
                return render_to_response('qualification.html', {"ct":ct, "cufon":js}, RequestContext(req))
            elif 3 in roles: #如果是本人
                if uuid == ct.coach.property.user.id:
                    js = cufon.get_js(ct.coach.property.name)
                    #print js
                    return render_to_response('qualification.html', {"ct":ct, "cufon":js}, RequestContext(req))
                else: return HttpResponse(u"没有下载权限")
            else: return HttpResponse(u"没有下载权限")
        except Exception,e:
            print e
            return HttpResponse(u"证书获取出错")
    return HttpResponse(u"不存在相关证书")

@login_required()
def train_info(req):
    t_id = req.GET.get("t_id",0)
    if t_id:
        try:
            train = Train.objects.get(id=t_id)
            return render_to_response('common/train_info.html', {"train":train}, RequestContext(req))
        except Exception,e:
            print e
            return HttpResponse(u"该培训不存在")
    return HttpResponse(u"该培训不存在")

@login_required()
def coach_info(req):
    c_id = req.GET.get("c_id",0)
    if c_id:
        try:
            coach = Coach.objects.get(id=c_id)
            coach.property.age = calculate_age(coach.property.birth)
            return render_to_response('common/coach_info.html', {"coach":coach}, RequestContext(req))
        except Exception,e:
            print e
            return HttpResponse(u"该教练不存在")
    return HttpResponse(u"该教练不存在")

def get_captcha(req):
    data = dict()
    data['cptch_key'] = CaptchaStore.generate_key()
    data['cptch_img'] = captcha_image_url(data['cptch_key'])
    return JsonResponse(data)
