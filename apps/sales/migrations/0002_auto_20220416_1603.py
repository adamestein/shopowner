# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-04-16 20:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sale',
            options={'ordering': ('item__sku', 'date', 'item__desc')},
        ),
    ]
