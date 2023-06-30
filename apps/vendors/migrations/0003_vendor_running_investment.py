# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-06-30 00:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0002_move_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='running_investment',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Total amount spent with this vendor', max_digits=10),
        ),
    ]
