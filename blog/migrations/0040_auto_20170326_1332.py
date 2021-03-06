# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-26 13:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0039_auto_20170325_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='authors',
            field=models.ManyToManyField(default=0, related_name='authors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='subscribers',
            field=models.ManyToManyField(default=0, related_name='subscribers', to=settings.AUTH_USER_MODEL),
        ),
    ]
