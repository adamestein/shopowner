# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Constants'
        db.create_table(u'sales_constants', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tax_rate', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'sales', ['Constants'])


    def backwards(self, orm):
        # Deleting model 'Constants'
        db.delete_table(u'sales_constants')


    models = {
        u'sales.constants': {
            'Meta': {'object_name': 'Constants'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax_rate': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['sales']