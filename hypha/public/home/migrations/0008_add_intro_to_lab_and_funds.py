# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-20 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_add_labs_and_funds_homepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='funds_intro',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='labs_intro',
            field=models.TextField(blank=True),
        ),
    ]