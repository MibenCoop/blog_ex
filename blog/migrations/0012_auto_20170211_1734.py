# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-11 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20170211_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_print',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='date_print',
            field=models.DateField(auto_now_add=True),
        ),
    ]
