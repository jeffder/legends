# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Captain'
        db.delete_table('core_captain')


    def backwards(self, orm):
        # Adding model 'Captain'
        db.create_table('core_captain', (
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(related_name='club_captain', to=orm['core.Club'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player_captain', to=orm['core.Player'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('core', ['Captain'])


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Group']", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.club': {
            'Meta': {'ordering': "['name']", 'object_name': 'Club'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clubs'", 'to': "orm['auth.User']", 'unique': 'True'})
        },
        'core.coach': {
            'Meta': {'ordering': "['-season', 'club', 'last_name', 'first_name']", 'object_name': 'Coach'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coaches'", 'to': "orm['core.Club']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '30'}),
            'has_paid_fees': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_assistant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '30'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coaches'", 'to': "orm['core.Season']"})
        },
        'core.ground': {
            'Meta': {'ordering': "['name']", 'object_name': 'Ground'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'core.player': {
            'Meta': {'ordering': "['-season', 'club', 'last_name', 'initial', 'first_name']", 'object_name': 'Player'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': "orm['core.Club']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '1', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': "orm['core.Season']"}),
            'supercoach_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '30'})
        },
        'core.season': {
            'Meta': {'ordering': "['-season']", 'object_name': 'Season'},
            'has_full_data': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_no_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'season': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['core']