# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 19:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_page_dislikes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='dislikes',
            field=models.ManyToManyField(default=0, related_name='dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='page',
            name='likes',
            field=models.ManyToManyField(default=0, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]