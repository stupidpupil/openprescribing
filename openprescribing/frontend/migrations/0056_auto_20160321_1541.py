# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-21 15:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0055_auto_20160321_1403'),
    ]

    operations = [
        migrations.RenameField(
            model_name='measurevalue',
            old_name='cost_saving_median',
            new_name='cost_saving_50th',
        ),
    ]
