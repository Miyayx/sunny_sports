# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
        ('payment', '0015_auto_20150502_2212'),
        ('sp', '0012_auto_20150430_1936'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentTeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stu_number', models.CharField(max_length=20)),
                ('student', models.ForeignKey(to='sp.Student')),
                ('team', models.ForeignKey(to='sp.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeamEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('award', models.IntegerField(default=0, choices=[(0, b'\xe7\xbc\xba\xe8\xb5\x9b'), (1, b'\xe4\xb8\x80\xe7\xad\x89\xe5\xa5\x96'), (2, b'\xe4\xba\x8c\xe7\xad\x89\xe5\xa5\x96'), (3, b'\xe4\xb8\x89\xe7\xad\x89\xe5\xa5\x96')])),
                ('certificate', models.CharField(max_length=100, null=True)),
                ('get_time', models.DateTimeField(null=True)),
                ('event', models.ForeignKey(to='sp.Event')),
                ('team', models.ForeignKey(to='sp.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Umpire',
        ),
        migrations.RenameField(
            model_name='studentproperty',
            old_name='county',
            new_name='dist',
        ),
        migrations.RemoveField(
            model_name='game',
            name='begin_time',
        ),
        migrations.RemoveField(
            model_name='game',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='game',
            name='sign_time',
        ),
        migrations.RemoveField(
            model_name='game',
            name='status',
        ),
        migrations.RemoveField(
            model_name='game',
            name='team_max',
        ),
        migrations.RemoveField(
            model_name='game',
            name='team_min',
        ),
        migrations.RemoveField(
            model_name='team',
            name='city',
        ),
        migrations.RemoveField(
            model_name='team',
            name='code',
        ),
        migrations.RemoveField(
            model_name='team',
            name='company',
        ),
        migrations.RemoveField(
            model_name='team',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='team',
            name='principal',
        ),
        migrations.RemoveField(
            model_name='team',
            name='province',
        ),
        migrations.RemoveField(
            model_name='team',
            name='regtime',
        ),
        migrations.RemoveField(
            model_name='team',
            name='team_id',
        ),
        migrations.AddField(
            model_name='game',
            name='address',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='city',
            field=models.CharField(default='', max_length=30, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='contact_email',
            field=models.EmailField(default='', max_length=20, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='contact_name',
            field=models.CharField(default='', max_length=20, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='contact_phone',
            field=models.CharField(default='', max_length=20, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='dist',
            field=models.CharField(default='', max_length=50, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='events',
            field=models.ManyToManyField(to='sp.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='female_num',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='game_etime',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='game_status',
            field=models.IntegerField(default=0, choices=[(0, b'\xe6\x9c\xaa\xe5\xbc\x80\xe5\xa7\x8b'), (1, b'\xe8\xbf\x9b\xe8\xa1\x8c\xe4\xb8\xad'), (2, b'\xe7\xbb\x93\xe6\x9d\x9f')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='game_stime',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='limit',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='male_num',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='money',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='organizer',
            field=models.CharField(default='', max_length=500, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='pass_status',
            field=models.IntegerField(default=0, choices=[(0, b'\xe6\x9c\xaa\xe5\xae\xa1\xe6\xa0\xb8'), (1, b'\xe5\xae\xa1\xe6\xa0\xb8\xe9\x80\x9a\xe8\xbf\x87'), (2, b'\xe5\xae\xa1\xe6\xa0\xb8\xe6\x9c\xaa\xe9\x80\x9a\xe8\xbf\x87')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='province',
            field=models.CharField(default='', max_length=20, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='pub_status',
            field=models.IntegerField(default=0, choices=[(0, b'not_published'), (1, b'published')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='reg_etime',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='reg_place',
            field=models.CharField(default='', max_length=300, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='reg_status',
            field=models.IntegerField(default=0, choices=[(0, b'regist not start'), (1, b'registing'), (2, b'regist end')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='reg_stime',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='schedule',
            field=models.TextField(default='', max_length=2000, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='sub_status',
            field=models.IntegerField(default=0, choices=[(0, b'not_submitted'), (1, b'submitted'), (2, b'not_pass')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='address',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='bill',
            field=models.OneToOneField(null=True, to='payment.Bill'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='contact_email',
            field=models.EmailField(max_length=20, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='contact_name',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='contact_phone',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='contact_qq',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='contact_weixin',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='contestant',
            field=models.ForeignKey(default='', to='game.Contestant'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='game',
            field=models.ForeignKey(default='', to='sp.Game'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='leader',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='pay_status',
            field=models.IntegerField(default=0, choices=[(0, b'\xe6\x9c\xaa\xe4\xbb\x98\xe8\xb4\xb9'), (1, b'\xe5\xb7\xb2\xe4\xbb\x98\xe8\xb4\xb9')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='postno',
            field=models.CharField(max_length=10, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='reg_time',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='coorganizer',
            field=models.CharField(max_length=500, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='description',
            field=models.TextField(max_length=500, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='id',
            field=models.CharField(max_length=16, serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='sponsor',
            field=models.CharField(max_length=500, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='team',
            name='id',
            field=models.CharField(max_length=16, serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=30, null=True),
            preserve_default=True,
        ),
    ]
