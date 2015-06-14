# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.CharField(max_length=36, serialize=False, primary_key=True)),
                ('bill_type', models.IntegerField(default=0, choices=[(0, b'coach_train'), (1, b'game')])),
                ('pay_type', models.IntegerField(default=0, choices=[(0, b'alipay_direct_pay'), (1, b'alipay_bank')])),
                ('total_fee', models.FloatField(default=0.0)),
                ('start_date', models.DateTimeField(default=datetime.datetime(2015, 4, 11, 14, 42, 20, 622468))),
                ('expire_date', models.DateTimeField(default=datetime.datetime(2015, 4, 12, 6, 42, 20, 622529))),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
