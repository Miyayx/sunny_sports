#!/usr/bin/env python
#-*-coding:utf-8-*-

from uuid import uuid4

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

class MyUserManager(BaseUserManager):

    def create_user(self, phone, nickname, email, role, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone:
            raise ValueError('Users must have an phone number')

        user = self.model(
            phone=phone,
            email=email,
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        r = Role(role=int(role))
        r.save()
        user.role.add(r)
        user.save(using=self._db)
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
    id = models.CharField(default=uuid4(), primary_key=True, max_length=40)
    role = models.ManyToManyField(Role)
    nickname = models.CharField(max_length=255, unique=True, null=True, blank=True)
    email    = models.EmailField(max_length=255, unique=True, blank=True)
    phone    = models.CharField(max_length=15, unique=True, db_index=True)
    #password = models.CharField(max_length=64) #password 在abstract class里有

    regist_time = models.DateTimeField(auto_now_add=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['role','nickname','email'] #除了phone和password以外传给manager的
    USERNAME_FIELD = 'phone'

    objects = MyUserManager()

    class Meta:
        app_label='sp'

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def get_full_name(self):
        return "Fullname"

    def get_short_name(self):
        return "Shortname"


class Code(models.Model):
    phone = models.IntegerField()
    code = models.CharField(max_length=10)
    time = models.DateTimeField()
    class Meta:
        app_label='sp'

