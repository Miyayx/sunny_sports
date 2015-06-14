# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('id', models.CharField(max_length=40, serialize=False, primary_key=True, db_index=True)),
                ('nickname', models.CharField(max_length=255, unique=True, null=True, blank=True)),
                ('email', models.EmailField(max_length=255, unique=True, null=True, blank=True)),
                ('phone', models.CharField(unique=True, max_length=15, db_index=True)),
                ('regist_time', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Centre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('real_name', models.CharField(max_length=4)),
                ('email', models.EmailField(max_length=75)),
                ('phone', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('province', models.CharField(max_length=20, blank=True)),
                ('city', models.CharField(max_length=30, blank=True)),
                ('county', models.CharField(max_length=50, blank=True)),
                ('address', models.CharField(max_length=100, blank=True)),
                ('level', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('t_level', models.IntegerField(default=0, choices=[(1, b'\xe5\x88\x9d\xe7\xba\xa7'), (2, b'\xe4\xb8\xad\xe7\xba\xa7'), (3, b'\xe9\xab\x98\xe7\xba\xa7'), (0, b'\xe6\x97\xa0\xe7\xba\xa7\xe5\x88\xab')])),
                ('p_level', models.IntegerField(default=0, choices=[(1, b'\xe5\x88\x9d\xe7\xba\xa7'), (2, b'\xe4\xb8\xad\xe7\xba\xa7'), (3, b'\xe9\xab\x98\xe7\xba\xa7'), (0, b'\xe6\x97\xa0\xe7\xba\xa7\xe5\x88\xab')])),
                ('status', models.IntegerField(default=0)),
                ('isreg', models.BooleanField(default=False)),
                ('club', models.ForeignKey(to='sp.Club', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CoachOrg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('org_num', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=256)),
                ('shortname', models.CharField(max_length=10)),
                ('director', models.CharField(default=b'', max_length=256, blank=True)),
                ('province', models.CharField(max_length=20, blank=True)),
                ('city', models.CharField(max_length=30, blank=True)),
                ('dist', models.CharField(max_length=50, blank=True)),
                ('address', models.CharField(max_length=100, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CoachProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, blank=True)),
                ('sex', models.IntegerField(default=0, choices=[(0, b'\xe7\x94\xb7'), (1, b'\xe5\xa5\xb3')])),
                ('birth', models.DateField(default=b'1990-01-01')),
                ('age', models.IntegerField(null=True)),
                ('identity', models.CharField(max_length=20, unique=True, null=True)),
                ('avatar', models.ImageField(default=b'upload/default.jpg', upload_to=b'upload')),
                ('company', models.CharField(max_length=50, blank=True)),
                ('province', models.CharField(max_length=20, blank=True)),
                ('city', models.CharField(max_length=30, blank=True)),
                ('dist', models.CharField(max_length=50, blank=True)),
                ('address', models.CharField(max_length=100, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CoachTrain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0, choices=[(0, b'\xe6\x9c\xaa\xe6\x8a\xa5\xe5\x90\x8d'), (1, b'\xe6\x9c\xaa\xe7\xbc\xb4\xe8\xb4\xb9'), (2, b'\xe5\xb7\xb2\xe7\xbc\xb4\xe8\xb4\xb9')])),
                ('pass_status', models.IntegerField(default=0, choices=[(0, b'\xe6\x9c\xaa\xe9\x80\x9a\xe8\xbf\x87'), (1, b'\xe5\xb7\xb2\xe9\x80\x9a\xe8\xbf\x87')])),
                ('certificate', models.CharField(max_length=100, null=True)),
                ('reg_time', models.DateTimeField(auto_now=True)),
                ('get_time', models.DateTimeField(null=True)),
                ('coach', models.ForeignKey(to='sp.Coach')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=15)),
                ('code', models.CharField(max_length=10)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500)),
                ('sponsor', models.CharField(max_length=50)),
                ('coorganizer', models.CharField(max_length=200)),
                ('begin_time', models.DateTimeField()),
                ('sign_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('team_max', models.IntegerField()),
                ('team_min', models.IntegerField()),
                ('status', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Judge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField(default=0, choices=[(1, b'\xe5\x88\x9d\xe7\xba\xa7'), (2, b'\xe4\xb8\xad\xe7\xba\xa7'), (3, b'\xe9\xab\x98\xe7\xba\xa7'), (0, b'\xe6\x97\xa0\xe7\xba\xa7\xe5\x88\xab')])),
                ('status', models.IntegerField(default=0)),
                ('ifreg', models.BooleanField(default=False)),
                ('club', models.ForeignKey(to='sp.Club', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JudgeProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, blank=True)),
                ('sex', models.IntegerField(default=0, choices=[(0, b'\xe7\x94\xb7'), (1, b'\xe5\xa5\xb3')])),
                ('birth', models.DateField(default=b'1990-01-01')),
                ('age', models.IntegerField(null=True)),
                ('identity', models.CharField(max_length=20, unique=True, null=True)),
                ('avatar', models.ImageField(default=b'upload/default.jpg', upload_to=b'upload')),
                ('company', models.CharField(max_length=50, blank=True)),
                ('province', models.CharField(max_length=20, blank=True)),
                ('city', models.CharField(max_length=30, blank=True)),
                ('county', models.CharField(max_length=50, blank=True)),
                ('address', models.CharField(max_length=100, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1000)),
                ('cont', models.CharField(max_length=3000)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PasswordDigitalSignature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=15)),
                ('signature', models.CharField(max_length=200)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role', models.IntegerField(unique=True, serialize=False, primary_key=True, choices=[(0, b'centre'), (1, b'coach_org'), (2, b'student'), (3, b'coach'), (4, b'judge'), (5, b'club'), (6, b'team'), (7, b'committee')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField(default=0, choices=[(9, b'9\xe7\xba\xa7'), (8, b'8\xe7\xba\xa7'), (7, b'7\xe7\xba\xa7'), (6, b'6\xe7\xba\xa7'), (5, b'5\xe7\xba\xa7'), (4, b'4\xe7\xba\xa7'), (3, b'3\xe7\xba\xa7'), (2, b'2\xe7\xba\xa7'), (1, b'1\xe7\xba\xa7'), (0, b'0\xe7\xba\xa7')])),
                ('status', models.IntegerField(default=0)),
                ('club', models.ForeignKey(to='sp.Club', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StudentProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, blank=True)),
                ('sex', models.IntegerField(default=0, choices=[(0, b'\xe7\x94\xb7'), (1, b'\xe5\xa5\xb3')])),
                ('birth', models.DateField(default=b'1990-01-01')),
                ('age', models.IntegerField(null=True)),
                ('identity', models.CharField(max_length=20, unique=True, null=True)),
                ('avatar', models.ImageField(default=b'upload/default.jpg', upload_to=b'upload')),
                ('height', models.IntegerField(default=0, null=True)),
                ('weight', models.IntegerField(default=0, null=True)),
                ('company', models.CharField(max_length=50, blank=True)),
                ('province', models.CharField(max_length=20, blank=True)),
                ('city', models.CharField(max_length=30, blank=True)),
                ('county', models.CharField(max_length=50, blank=True)),
                ('address', models.CharField(max_length=100, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('team_id', models.CharField(max_length=15)),
                ('province', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=30)),
                ('company', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=30)),
                ('principal', models.CharField(max_length=20)),
                ('contact', models.CharField(max_length=30)),
                ('regtime', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.CharField(default=b'', max_length=20, unique=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('demo', models.CharField(max_length=100, blank=True)),
                ('address', models.CharField(max_length=100)),
                ('level', models.IntegerField(choices=[(1, b'\xe5\x88\x9d\xe7\xba\xa7'), (2, b'\xe4\xb8\xad\xe7\xba\xa7'), (3, b'\xe9\xab\x98\xe7\xba\xa7')])),
                ('limit', models.IntegerField()),
                ('cur_num', models.IntegerField(default=0)),
                ('money', models.IntegerField()),
                ('reg_stime', models.DateTimeField()),
                ('reg_etime', models.DateTimeField()),
                ('train_stime', models.DateField()),
                ('train_etime', models.DateField()),
                ('reg_status', models.IntegerField(default=0, choices=[(0, b'regist not start'), (1, b'registing'), (2, b'regist end')])),
                ('train_status', models.IntegerField(default=0, choices=[(0, b'\xe6\x9c\xaa\xe5\xbc\x80\xe5\xa7\x8b'), (1, b'\xe8\xbf\x9b\xe8\xa1\x8c\xe4\xb8\xad'), (2, b'\xe7\xbb\x93\xe6\x9d\x9f')])),
                ('sub_status', models.IntegerField(default=0, choices=[(0, b'not_submitted'), (1, b'submitted'), (2, b'not_pass')])),
                ('pub_status', models.IntegerField(default=0, choices=[(0, b'not_published'), (1, b'published')])),
                ('org', models.ForeignKey(to='sp.CoachOrg')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Umpire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
                ('level', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('checked', models.BooleanField(default=False)),
                ('msg', models.ForeignKey(to='sp.Message')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_first', models.BooleanField(default=True, choices=[(0, b'not_complete'), (1, b'completed')])),
                ('role', models.ForeignKey(to='sp.Role')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='student',
            name='property',
            field=models.ForeignKey(to='sp.StudentProperty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='judge',
            name='property',
            field=models.ForeignKey(to='sp.JudgeProperty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coachtrain',
            name='train',
            field=models.ForeignKey(to='sp.Train'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coach',
            name='property',
            field=models.ForeignKey(to='sp.CoachProperty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='myuser',
            name='role',
            field=models.ManyToManyField(to='sp.Role', through='sp.UserRole'),
            preserve_default=True,
        ),
    ]
