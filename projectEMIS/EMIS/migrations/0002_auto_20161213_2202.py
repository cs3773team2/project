# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-13 22:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EMIS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalrecord',
            name='height',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='medicalrecord',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
