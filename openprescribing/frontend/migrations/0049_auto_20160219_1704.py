# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-19 17:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0048_auto_20160219_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='practice',
            name='join_provider_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='practice',
            name='leave_provider_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]