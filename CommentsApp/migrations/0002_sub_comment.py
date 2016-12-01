# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-26 21:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CommentsApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sub_Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now=True)),
                ('comment', models.CharField(max_length=500, null=True)),
                ('comment_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CommentsApp.Comment')),
            ],
        ),
    ]