# -*- coding:utf-8 -*-
from django.shortcuts import render

from PIL import Image
import os
import StringIO
import uuid

from qiniu import Auth
from qiniu import put_data
from qiniu import BucketManager

from sunny_sports.settings import MEDIA_ROOT
from sunny_sports.settings import DEFAULT_PHOTO
from forms import *
from config import *

def update_photo(request, obj):
    if request.method == "POST":
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
            headImg = uf.cleaned_data['headImg']
            suffix = headImg.name.split('.')[-1]; #check if it's an image
            if suffix == "jpg" or suffix=="jpeg" or suffix=="gif" or suffix=="png" or suffix =="bmp":
                old = obj.avatar.name
                print "old-->"+old
                obj.avatar = headImg
                obj.save() #保存到数据库
                path = obj.avatar.name
                imgpath = os.path.join(MEDIA_ROOT, path) #图片真实路径
                print "imgpath-->"+imgpath
                im = Image.open(imgpath)
                new_img=im.resize((200,200),Image.ANTIALIAS)
                new_img.save(imgpath) #保存图片
                old = os.path.join(MEDIA_ROOT, old)
                if os.path.isfile(old):
                    os.remove(old) #删除旧头像
                print "delete-->"+os.path.join(MEDIA_ROOT, old)

def update_photo_in_qiniu(request, obj):
    if request.method == "POST":
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
            headImg = uf.cleaned_data['headImg']
            suffix = headImg.name.split('.')[-1]; #check if it's an image
            if suffix == "jpg" or suffix=="jpeg" or suffix=="gif" or suffix=="png" or suffix =="bmp":
                old = obj.avatar
                print "old-->"+old.name
                obj.avatar = headImg
                #obj.avatar.name = obj.avatar.name.rsplit('.',1)[0]+'_'+str(uuid.uuid1())+'.'+obj.avatar.name.rsplit('.',1)[1]
                obj.avatar.name = obj.avatar.name.rsplit('.',1)[0]+'_'+gen_random_str(10)+'.'+suffix
                obj.save() 
                path = obj.avatar.name
                imgpath = os.path.join(MEDIA_ROOT, path) #图片真实路径
                print "imgpath-->"+imgpath
                im = Image.open(imgpath)
                new_img=im.resize((200,200),Image.ANTIALIAS)
                buf = StringIO.StringIO()
                new_img.save(buf, format=suffix)
                if(update_to_qiniu(buf.getvalue(), path, old.name)):
                    obj.save() #保存到数据库
                else:
                    obj.avatar = old
                    obj.save()
                if os.path.isfile(imgpath):
                    os.remove(imgpath) #删除头像

def upload_license_to_qiniu(request, obj):
    if request.method == "POST":
        print request.POST
        lf = LicenseForm(request.POST,request.FILES)
        if lf.is_valid():
            img = lf.cleaned_data['license']
            suffix = img.name.split('.')[-1]; #check if it's an image
            if suffix == "jpg" or suffix=="jpeg" or suffix=="gif" or suffix=="png" or suffix =="bmp":
                old = obj.license
                print "old-->"+old.name
                obj.license = img
                obj.license.name = obj.license.name.rsplit('.',1)[0]+'_'+gen_random_str(10)+'.'+suffix
                obj.save() 
                path = obj.license.name
                imgpath = os.path.join(MEDIA_ROOT, path) #图片真实路径
                print "imgpath-->"+imgpath
                im = Image.open(imgpath)
                buf = StringIO.StringIO()
                im.save(buf, format=suffix)
                if(update_to_qiniu(buf.getvalue(), path, old.name)):
                    obj.save() #保存到数据库
                else:
                    obj.license = old
                    obj.save()
                if os.path.isfile(imgpath):
                    os.remove(imgpath) #删除头像

def update_to_qiniu(data, newkey, oldkey):
    bucket_name = QINIU_PHOTO_BUCKET
    q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
    token = q.upload_token(bucket_name)
    ret, info = put_data(token, newkey, data)
    print(info)
    assert ret['key'] == newkey

    if oldkey == DEFAULT_PHOTO:
        return True
    bucket = BucketManager(q)
    print "delete-->"+oldkey
    ret, info = bucket.delete(bucket_name, oldkey)
    print(info)
    print ret
    print info.status_code
    assert ret is None or len(ret) == 0
    assert info.status_code == 612 or info.status_code == 200
    print "delete-->"+oldkey

    return True

#生成随机密码
import random
import string
#python3中为string.ascii_letters,而python2下则可以使用string.letters和string.ascii_letters
def gen_random_str(n):
    chars=string.ascii_letters+string.digits
    return ''.join([random.choice(chars) for i in range(n)])#得出的结果中字符会有重复的
    #return ''.join(random.sample(chars, 15))#得出的结果中字符不会有重复的
