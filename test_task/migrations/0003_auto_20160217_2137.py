# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_task', '0002_auto_20160217_1802'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-pub_date']},
        ),
        migrations.RenameField(
            model_name='likes',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='likes',
            old_name='user_id',
            new_name='user',
        ),
    ]
