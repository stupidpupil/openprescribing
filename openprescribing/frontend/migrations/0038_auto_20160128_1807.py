# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-28 18:07
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0037_practicelist_star_pu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practicelist',
            name='star_pu',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
