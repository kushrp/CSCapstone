# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 03:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationApp', '0003_auto_20161129_0300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='contact',
            field=models.IntegerField(null=True),
        ),
    ]