# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 18:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_page_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='favourite',
            new_name='favorite',
        ),
        migrations.RemoveField(
            model_name='page',
            name='description',
        ),
    ]
