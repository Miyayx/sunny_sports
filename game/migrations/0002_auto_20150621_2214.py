# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0016_auto_20150621_2214'),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestant',
            name='user',
        ),
        migrations.DeleteModel(
            name='Contestant',
        ),
    ]
