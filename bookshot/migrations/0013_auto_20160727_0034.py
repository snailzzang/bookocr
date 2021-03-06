# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-26 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshot', '0012_auto_20160724_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='_raw_response',
            field=models.TextField(blank=True, default='{}', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover_url',
            field=models.URLField(blank=True, default='', max_length=300, null=True),
        ),
    ]
