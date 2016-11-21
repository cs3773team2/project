# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-21 01:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=20)),
                ('l_name', models.CharField(max_length=30)),
                ('dob', models.IntegerField()),
                ('age', models.IntegerField()),
                ('address', models.CharField(max_length=100)),
            ],
        ),
    ]
