# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0015_auto_20150502_2222'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fullname', models.CharField(max_length=200, blank=True)),
                ('org_num', models.CharField(max_length=20, blank=True)),
                ('province', models.CharField(max_length=20, blank=True)),
                ('city', models.CharField(max_length=30, blank=True)),
                ('dist', models.CharField(max_length=50, blank=True)),
                ('address', models.CharField(max_length=100, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='centre',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='coachorg',
            name='ali_email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='coachproperty',
            name='avatar',
            field=models.ImageField(default=b'upload/default00.jpg', upload_to=b'upload'),
        ),
        migrations.AlterField(
            model_name='coachtrain',
            name='reg_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='code',
            name='time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='message',
            name='time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='last login', blank=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='regist_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
        migrations.AlterField(
            model_name='passworddigitalsignature',
            name='time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='role',
            name='role',
            field=models.IntegerField(unique=True, serialize=False, primary_key=True, choices=[(0, b'centre'), (1, b'coach_org'), (2, b'student'), (3, b'coach'), (4, b'club'), (5, b'group'), (6, b'committee')]),
        ),
        migrations.AlterField(
            model_name='studentproperty',
            name='avatar',
            field=models.ImageField(default=b'upload/default00.jpg', upload_to=b'upload'),
        ),
        migrations.AlterField(
            model_name='team',
            name='contestant',
            field=models.ForeignKey(to='sp.UserRole'),
        ),
        migrations.AddField(
            model_name='group',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
