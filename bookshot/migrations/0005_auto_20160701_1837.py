# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-01 18:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookshot', '0004_auto_20160701_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='readers',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='book',
        ),
    ]
