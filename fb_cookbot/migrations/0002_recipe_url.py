# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-30 08:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_cookbot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]
