# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Season'
        db.create_table('core_season', (
            ('season', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('has_full_data', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_no_data', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Season'])


    def backwards(self, orm):
        # Deleting model 'Season'
        db.delete_table('core_season')


    models = {
        'core.season': {
            'Meta': {'object_name': 'Season'},
            'has_full_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_no_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'season': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['core']