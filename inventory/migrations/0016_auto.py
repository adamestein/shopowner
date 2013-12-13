# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field category on 'Item'
        db.delete_table(db.shorten_name(u'inventory_item_category'))

        # Removing M2M table for field seller on 'Item'
        db.delete_table(db.shorten_name(u'inventory_item_seller'))

        # Adding M2M table for field categories on 'Item'
        m2m_table_name = db.shorten_name(u'inventory_item_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'inventory.item'], null=False)),
            ('category', models.ForeignKey(orm[u'inventory.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'category_id'])

        # Adding M2M table for field sellers on 'Item'
        m2m_table_name = db.shorten_name(u'inventory_item_sellers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'inventory.item'], null=False)),
            ('seller', models.ForeignKey(orm[u'inventory.seller'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'seller_id'])


    def backwards(self, orm):
        # Adding M2M table for field category on 'Item'
        m2m_table_name = db.shorten_name(u'inventory_item_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'inventory.item'], null=False)),
            ('category', models.ForeignKey(orm[u'inventory.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'category_id'])

        # Adding M2M table for field seller on 'Item'
        m2m_table_name = db.shorten_name(u'inventory_item_seller')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'inventory.item'], null=False)),
            ('seller', models.ForeignKey(orm[u'inventory.seller'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'seller_id'])

        # Removing M2M table for field categories on 'Item'
        db.delete_table(db.shorten_name(u'inventory_item_categories'))

        # Removing M2M table for field sellers on 'Item'
        db.delete_table(db.shorten_name(u'inventory_item_sellers'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'inventory.category': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('user', 'name'),)", 'object_name': 'Category'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'remove': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'inventory.item': {
            'Meta': {'ordering': "('number',)", 'unique_together': "(('user', 'number'),)", 'object_name': 'Item'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['inventory.Category']", 'symmetrical': 'False'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'commission': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '5'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'remove': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sellers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['inventory.Seller']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'worth': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'})
        },
        u'inventory.itemimage': {
            'Meta': {'object_name': 'ItemImage'},
            'data': ('django.db.models.fields.TextField', [], {}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mimetype': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'inventory.seller': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'unique_together': "(('first_name', 'last_name', 'user'),)", 'object_name': 'Seller'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'remove': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['inventory']