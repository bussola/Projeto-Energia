# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 20:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20170821_1641'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='constantes',
            options={},
        ),
        migrations.RemoveField(
            model_name='question',
            name='pub_date',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_text',
        ),
    ]