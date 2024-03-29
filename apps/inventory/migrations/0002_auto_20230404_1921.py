# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-04-04 23:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='vendor',
            field=models.ForeignKey(help_text='Vendor this item was purchased from', on_delete=django.db.models.deletion.CASCADE, to='inventory.Vendor'),
        ),
        migrations.AlterUniqueTogether(
            name='inventory',
            unique_together=set([('label', 'product_number', 'stock_number', 'user', 'vendor')]),
        ),
    ]
