# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0017_auto_20150621_2221'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameOrg',
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
                ('is_active', models.BooleanField(default=True)),
                ('ali_email', models.EmailField(max_length=254, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
