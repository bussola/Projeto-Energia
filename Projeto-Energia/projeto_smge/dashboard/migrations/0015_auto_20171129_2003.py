# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-29 22:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_auto_20171128_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coleta',
            name='io6',
            field=models.FloatField(max_length=255, null=True),
        ),
    ]