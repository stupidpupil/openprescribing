# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-11 16:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0043_auto_20160211_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurevalue',
            name='pct',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.PCT'),
        ),
    ]
