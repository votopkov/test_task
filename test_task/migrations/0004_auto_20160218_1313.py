# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_task', '0003_auto_20160217_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='product',
            field=models.ForeignKey(related_name='product_like', to='test_task.Product'),
        ),
    ]
