# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-01 21:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_auto_20171129_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='coleta',
            name='media_io6',
            field=models.FloatField(max_length=255, null=True),
        ),
    ]
