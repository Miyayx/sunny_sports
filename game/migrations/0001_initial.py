# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fullname', models.CharField(max_length=200, blank=True)),
                ('org_num', models.CharField(max_length=20, blank=True)),
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
    ]
