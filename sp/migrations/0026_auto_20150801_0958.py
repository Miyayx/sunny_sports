# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0025_auto_20150729_0915'),
    ]

    operations = [
        migrations.RenameField(
            model_name='club',
            old_name='county',
            new_name='dist',
        ),
        migrations.AddField(
            model_name='club',
            name='corporator',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='club',
            name='license',
            field=models.ImageField(default=b'', upload_to=b'upload'),
        ),
        migrations.AddField(
            model_name='club',
            name='office_num',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='club',
            name='shortname',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='coachorg',
            name='profit_ratio',
            field=models.FloatField(default=0.95),
        ),
        migrations.AddField(
            model_name='gameorg',
            name='profit_ratio',
            field=models.FloatField(default=0.95),
        ),
        migrations.AddField(
            model_name='group',
            name='corporator',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='license',
            field=models.ImageField(default=b'', upload_to=b'upload'),
        ),
        migrations.AddField(
            model_name='group',
            name='office_num',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='shortname',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='club',
            name='org_num',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='org_num',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
