# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0030_auto_20150829_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='game',
            name='address',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='contact_email',
            field=models.EmailField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='contact_name',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='contact_phone',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='coorganizer',
            field=models.CharField(max_length=800, blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='description',
            field=models.TextField(max_length=1000, blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='id',
            field=models.CharField(default=b'', max_length=50, unique=True, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='organizer',
            field=models.CharField(max_length=800, blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='reg_place',
            field=models.CharField(max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='sponsor',
            field=models.CharField(max_length=800, blank=True),
        ),
    ]
