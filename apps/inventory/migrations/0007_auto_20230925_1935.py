# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-09-25 23:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20230629_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='qty_bought',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='wholesale_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
