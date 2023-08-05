# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-15 23:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djeddit', '0002_thread_locked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='score',
        ),
        migrations.AddField(
            model_name='post',
            name='_downvotes',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='_upvotes',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='wsi',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
