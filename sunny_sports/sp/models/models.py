#!/usr/bin/env python
#-*-coding:utf-8-*-

from uuid import uuid1

from django.db import models
from django.contrib.auth.models import (
        UserManager, BaseUserManager, AbstractBaseUser
        )

from role import *
from club import *
from game import *
from committee import *
from association import *
from status import *

# Create your models here.

class Role(models.Model):
    role = models.IntegerField(choices=ROLE_LIST, unique=True, primary_key=True)
    class Meta:
        app_label='sp'

    def __str__(self):
        return self.get_role_display()


class MyUserManager(BaseUserManager):

    def create_user(self, phone, nickname, email, role, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone:
            raise ValueError('Users must have an phone number')

        print phone

        user = self.model(
            phone=phone,
            email=email,
            nickname=nickname,
        )

        user.id = uuid1()
        user.set_password(password)
        user.save()
        r = Role.objects.get(role=int(role))
        ur = UserRole.objects.create(user=user, role=r) #用objects.create可以不用save()
        return user

    def create_superuser(self, phone, nickname, email, role, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(phone, nickname, email, role, password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    id = models.CharField(primary_key=True, max_length=40, db_index=True)
    role = models.ManyToManyField(Role, through='UserRole')
    nickname = models.CharField(max_length=255, unique=True, null=True, blank=True)
    email    = models.EmailField(max_length=255, blank=True, unique=False)
    phone    = models.CharField(max_length=15, unique=True, db_index=True)
    #password = models.CharField(max_length=64) #password 在abstract class里有

    regist_time = models.DateTimeField(auto_now=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['role','nickname','email'] #除了phone和password以外传给manager的
    USERNAME_FIELD = 'phone'

    objects = MyUserManager()

    class Meta:
        app_label='sp'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def get_full_name(self):
        return "Fullname"

    def get_short_name(self):
        return "Shortname"

class UserRole(models.Model):
    user = models.ForeignKey(MyUser)
    role = models.ForeignKey(Role)
    class Meta:
        app_label='sp'


class Code(models.Model):
    phone = models.IntegerField()
    code = models.CharField(max_length=10)
    time = models.DateTimeField()
    class Meta:
        app_label='sp'

