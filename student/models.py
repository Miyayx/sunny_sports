#-*- coding:utf-8 -*-
from django.db import models

# Create your models here.

from sp.models.models import *
from sp.models.role import *

STUDENT_LEVEL=(
        (9, '9级'),
        (8, '8级'),
        (7, '7级'),
        (6, '6级'),
        (5, '5级'),
        (4, '4级'),
        (3, '3级'),
        (2, '2级'),
        (1, '1级'),
        (0, '0级'),
        )


class StudentProperty(PersonProperty):
    """
    继承于PersonProperty
    """
    height = models.IntegerField(null=True, default=0)
    weight = models.IntegerField(null=True, default=0)
    company = models.CharField(max_length=50, blank=True)
    province = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=30, blank=True)
    dist = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    
    class Meta:
        app_label='sp'

class Student(models.Model):
    property = models.ForeignKey(StudentProperty)
    club = models.ForeignKey(Club, null=True)
    level = models.IntegerField(choices=STUDENT_LEVEL, default=0)
    status = models.IntegerField(default=0)

    class Meta:
        app_label='sp'

    def __str__(self):
        return str(self.property)

