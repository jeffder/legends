# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Season'
        db.create_table('core_season', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('season', self.gf('django.db.models.fields.IntegerField')()),
            ('has_full_data', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('has_no_data', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Season'])

        # Adding model 'Club'
        db.create_table('core_club', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='clubs', unique=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('core', ['Club'])

        # Adding model 'Coach'
        db.create_table('core_coach', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(related_name='coaches', to=orm['core.Club'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('has_paid_fees', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(related_name='coaches', to=orm['core.Season'])),
        ))
        db.send_create_signal('core', ['Coach'])

        # Adding model 'Player'
        db.create_table('core_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(related_name='players', to=orm['core.Club'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('initial', self.gf('django.db.models.fields.CharField')(blank=True, max_length=1, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(related_name='players', to=orm['core.Season'])),
            ('supercoach_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
        ))
        db.send_create_signal('core', ['Player'])

        # Adding model 'Captain'
        db.create_table('core_captain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(related_name='club_captain', to=orm['core.Club'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player_captain', to=orm['core.Player'])),
        ))
        db.send_create_signal('core', ['Captain'])

        # Adding model 'Venue'
        db.create_table('core_ground', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('core', ['Ground'])


    def backwards(self, orm):
        # Deleting model 'Coach'
        db.delete_table('core_coach')

        # Deleting model 'Captain'
        db.delete_table('core_captain')

        # Deleting model 'Player'
        db.delete_table('core_player')

        # Deleting model 'Club'
        db.delete_table('core_club')

        # Deleting model 'Season'
        db.delete_table('core_season')

        # Deleting model 'Venue'
        db.delete_table('core_ground')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']", 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']", 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.captain': {
            'Meta': {'object_name': 'Captain', 'ordering': "('-player__season', 'club')"},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'club_captain'", 'to': "orm['core.Club']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_captain'", 'to': "orm['core.Player']"})
        },
        'core.club': {
            'Meta': {'object_name': 'Club', 'ordering': "['name']"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clubs'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'core.coach': {
            'Meta': {'object_name': 'Coach', 'ordering': "['-season', 'club', 'last_name', 'first_name']"},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coaches'", 'to': "orm['core.Club']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'has_paid_fees': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coaches'", 'to': "orm['core.Season']"})
        },
        'core.player': {
            'Meta': {'object_name': 'Player', 'ordering': "['-season', 'club', 'last_name', 'initial', 'first_name']"},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': "orm['core.Club']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '1', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': "orm['core.Season']"}),
            'supercoach_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'})
        },
        'core.season': {
            'Meta': {'object_name': 'Season', 'ordering': "['-season']"},
            'has_full_data': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_no_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'season': ('django.db.models.fields.IntegerField', [], {})
        },
        'core.ground': {
            'Meta': {'object_name': 'Ground'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['core']
