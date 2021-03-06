# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-11 13:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_userprofile_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.IntegerField(default=0)),
                ('author', models.CharField(max_length=128)),
                ('date_print', models.DateField(auto_now_add=True)),
                ('content', models.CharField(max_length=5000)),
            ],
        ),
    ]
