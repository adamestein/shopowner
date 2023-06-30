# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-06-30 00:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import orders.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vendors', '0004_auto_20230629_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_number', models.CharField(blank=True, help_text='Order number/reference number', max_length=20, null=True)),
                ('date_ordered', models.DateField(help_text='Date when order was placed')),
                ('date_received', models.DateField(blank=True, help_text='Date when order was received', null=True)),
                ('net_cost', models.DecimalField(decimal_places=2, help_text='Net cost for the order', max_digits=10)),
                ('shipping_cost', models.DecimalField(decimal_places=2, default=0, help_text='Tax credit paid for the order', max_digits=10)),
                ('tax', models.DecimalField(decimal_places=2, default=0, help_text='Tax credit paid for the order', max_digits=10)),
                ('receipt', models.FileField(blank=True, help_text='Receipt file (leave empty for hardcopy)', null=True, upload_to=orders.models.update_receipt_filename)),
                ('notes', models.TextField(blank=True, help_text='Any miscellaneous information can go here')),
            ],
            options={
                'ordering': ('vendor', 'reference_number'),
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.TextField(help_text='Method of payment', max_length=30)),
            ],
            options={
                'ordering': ('label',),
            },
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.ForeignKey(blank=True, help_text='Method of payment for this order', null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.PaymentMethod'),
        ),
        migrations.AddField(
            model_name='order',
            name='vendor',
            field=models.ForeignKey(help_text='Vendor this order was purchased from', on_delete=django.db.models.deletion.CASCADE, to='vendors.Vendor'),
        ),
    ]
