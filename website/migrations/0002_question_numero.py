# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-21 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='numero',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
