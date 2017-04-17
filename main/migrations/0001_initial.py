# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 08:15
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified', models.DateTimeField(auto_created=True, auto_now=True)),
                ('title', models.CharField(max_length=1000, verbose_name='title')),
                ('content', models.TextField(blank=True, verbose_name='content')),
                ('order', models.SmallIntegerField(default=0, verbose_name='display order')),
                ('display', models.BooleanField(default=False, verbose_name='display?')),
                ('slug', autoslug.fields.AutoSlugField(editable=True, max_length=1000, populate_from=b'title', unique_with=(b'title',), verbose_name='slug')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]