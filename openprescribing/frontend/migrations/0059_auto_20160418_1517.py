# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-18 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0058_measure_is_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentation',
            name='active_quantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='presentation',
            name='adq',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='presentation',
            name='adq_unit',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='presentation',
            name='percent_of_adq',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
