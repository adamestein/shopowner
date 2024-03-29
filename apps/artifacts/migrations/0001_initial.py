# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-07-03 19:17
from __future__ import unicode_literals

import artifacts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artifact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('receipt', 'Receipt')], help_text='Artifact category', max_length=7)),
                ('directory', models.CharField(blank=True, help_text='Relative directory from /home/adam/Src/ShopOwner/upload which is the default', max_length=50)),
                ('original_filename', models.CharField(help_text='Name of uploaded file', max_length=200)),
                ('file', models.FileField(blank=True, help_text='Uploaded file', null=True, upload_to=artifacts.models.update_filename)),
            ],
            options={
                'ordering': ('original_filename',),
            },
        ),
    ]
