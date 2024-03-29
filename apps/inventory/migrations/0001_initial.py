# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-03-27 18:21
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='Item label for display', max_length=100)),
                ('notes', models.TextField(help_text='Any miscellaneous information can go here')),
                ('qty_bought', models.PositiveIntegerField(help_text='Quantity of this item purchased', validators=[django.core.validators.MinValueValidator(1)])),
                ('qty_sold', models.PositiveIntegerField(default=0, help_text='Quantity of this item sold')),
                ('product_number', models.CharField(help_text="Vendor's product number for this item", max_length=50)),
                ('stock_number', models.CharField(help_text='My stock number for this item', max_length=50)),
                ('wholesale_price', models.DecimalField(decimal_places=2, help_text='Wholesale price per item unit', max_digits=10)),
                ('user', models.ForeignKey(help_text='User account this item belongs to', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Inventories',
                'ordering': ('label',),
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Vendor's name", max_length=50)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='inventory',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Vendor'),
        ),
    ]
