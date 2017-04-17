# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-17 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('last_modified',)},
        ),
        migrations.AddField(
            model_name='post',
            name='comments_count',
            field=models.IntegerField(default=0, verbose_name='Comments count'),
        ),
    ]