# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20170206_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='description',
            field=models.CharField(default='All information within article', max_length=255),
        ),
    ]
