# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-02 01:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_buddy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='trip',
            name='start_date',
            field=models.DateField(),
        ),
    ]
