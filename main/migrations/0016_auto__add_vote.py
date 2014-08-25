# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Vote'
        db.create_table('main_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Game'], related_name='bogs')),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Player'], related_name='bog_player')),
            ('votes', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('main', ['Vote'])


    def backwards(self, orm):
        # Deleting model 'Vote'
        db.delete_table('main_vote')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
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
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.bye': {
            'Meta': {'object_name': 'Bye', 'ordering': "('-round__season', 'round', 'club')"},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'byes'"}),
            'crowds_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'margins_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Round']", 'related_name': "'byes'"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'votes_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'winners_bonus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'winners_score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.club': {
            'Meta': {'object_name': 'Club', 'ordering': "['name']"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True', 'related_name': "'clubs'"})
        },
        'main.coach': {
            'Meta': {'object_name': 'Coach', 'ordering': "['-season', 'club', 'last_name', 'first_name']"},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'coaches'"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'has_paid_fees': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_assistant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Season']", 'related_name': "'coaches'"})
        },
        'main.game': {
            'Meta': {'object_name': 'Game', 'ordering': "('-round__season', 'round', 'game_date', 'afl_home')"},
            'afl_away': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'afl_game_away'"}),
            'afl_away_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'afl_home': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'afl_game_home'"}),
            'afl_home_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'crowd': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'finals_game': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'game_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'ground': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Ground']", 'related_name': "'games'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legends_away': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'legends_game_away'"}),
            'legends_away_crowds_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_away_margins_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_away_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_away_votes_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_away_winners_bonus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_away_winners_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_home': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'legends_game_home'"}),
            'legends_home_crowds_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_home_margins_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_home_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_home_votes_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_home_winners_bonus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_home_winners_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Round']", 'related_name': "'games'"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'tipping_deadline': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'})
        },
        'main.ground': {
            'Meta': {'object_name': 'Ground', 'ordering': "['name']"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'main.player': {
            'Meta': {'object_name': 'Player', 'ordering': "['-season', 'club', 'last_name', 'initial', 'first_name']"},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'players'"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '1', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Season']", 'related_name': "'players'"}),
            'supercoach_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'})
        },
        'main.round': {
            'Meta': {'object_name': 'Round', 'ordering': "('-season', 'start_time')"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_finals': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'num_bogs': ('django.db.models.fields.IntegerField', [], {}),
            'num_games': ('django.db.models.fields.IntegerField', [], {}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Season']", 'related_name': "'rounds'"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'tipping_deadline': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'main.season': {
            'Meta': {'object_name': 'Season', 'ordering': "['-season']"},
            'has_full_data': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_no_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'season': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.vote': {
            'Meta': {'object_name': 'Vote'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Game']", 'related_name': "'bogs'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Player']", 'related_name': "'bog_player'"}),
            'votes': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['main']