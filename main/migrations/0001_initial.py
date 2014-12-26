# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Season'
        db.create_table('main_season', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('season', self.gf('django.db.models.fields.IntegerField')()),
            ('has_full_data', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('has_no_data', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('main', ['Season'])

        # Adding model 'Club'
        db.create_table('main_club', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True, related_name='clubs')),
        ))
        db.send_create_signal('main', ['Club'])

        # Adding model 'Coach'
        db.create_table('main_coach', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Club'], related_name='coaches')),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('has_paid_fees', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_assistant', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Season'], related_name='coaches')),
        ))
        db.send_create_signal('main', ['Coach'])

        # Adding model 'Ground'
        db.create_table('main_ground', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('main', ['Ground'])

        # Adding model 'Round'
        db.create_table('main_round', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_finals', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('num_bogs', self.gf('django.db.models.fields.IntegerField')()),
            ('num_games', self.gf('django.db.models.fields.IntegerField')()),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Season'], related_name='rounds')),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('tipping_deadline', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('main', ['Round'])

        # Adding model 'Game'
        db.create_table('main_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('crowd', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('finals_game', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('game_date', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True)),
            ('round', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Round'], related_name='games')),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('tipping_deadline', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True)),
            ('ground', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Ground'], related_name='games')),
            ('afl_away', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Club'], related_name='afl_game_away')),
            ('afl_away_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('afl_home', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Club'], related_name='afl_game_home')),
            ('afl_home_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('legends_away', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Club'], related_name='legends_game_away')),
            ('legends_away_crowds_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('legends_away_margins_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('legends_away_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('legends_away_supercoach_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('legends_away_winners_bonus', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('legends_away_winners_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('legends_home', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Club'], related_name='legends_game_home')),
            ('legends_home_crowds_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('legends_home_margins_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('legends_home_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('legends_home_supercoach_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('legends_home_winners_bonus', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('legends_home_winners_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('main', ['Game'])

        # Adding model 'Player'
        db.create_table('main_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Club'], related_name='players')),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('initial', self.gf('django.db.models.fields.CharField')(blank=True, max_length=1, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Season'], related_name='players')),
            ('supercoach_name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=30, null=True)),
        ))
        db.send_create_signal('main', ['Player'])

        # Adding model 'Bye'
        db.create_table('main_bye', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Club'], related_name='byes')),
            ('crowds_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('margins_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('round', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Round'], related_name='byes')),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('supercoach_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('winners_bonus', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('winners_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('main', ['Bye'])

        # Adding model 'SupercoachRanking'
        db.create_table('main_supercoach_ranking', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Game'], related_name='supercoach_rankings')),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Player'], related_name='supercoach_rankings')),
            ('ranking', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('main', ['SupercoachRanking'])

        # Adding model 'Tip'
        db.create_table('main_tip', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Game'], related_name='tips')),
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Club'], related_name='tips')),
            ('crowd', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('crowds_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('margin', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('margins_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('supercoach_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Club'], null=True, related_name='tip_winners')),
            ('winners_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('main', ['Tip'])

        # Adding model 'SupercoachTip'
        db.create_table('main_supercoach_tip', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Player'], null=True, related_name='supercoach_tips')),
            ('tip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Tip'], related_name='supercoach_tips')),
        ))
        db.send_create_signal('main', ['SupercoachTip'])


    def backwards(self, orm):
        # Deleting model 'Season'
        db.delete_table('main_season')

        # Deleting model 'Club'
        db.delete_table('main_club')

        # Deleting model 'Coach'
        db.delete_table('main_coach')

        # Deleting model 'Ground'
        db.delete_table('main_ground')

        # Deleting model 'Round'
        db.delete_table('main_round')

        # Deleting model 'Game'
        db.delete_table('main_game')

        # Deleting model 'Player'
        db.delete_table('main_player')

        # Deleting model 'Bye'
        db.delete_table('main_bye')

        # Deleting model 'SupercoachRanking'
        db.delete_table('main_supercoach_ranking')

        # Deleting model 'Tip'
        db.delete_table('main_tip')

        # Deleting model 'SupercoachTip'
        db.delete_table('main_supercoach_tip')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.bye': {
            'Meta': {'ordering': "('-round__season', 'round', 'club')", 'object_name': 'Bye'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'byes'"}),
            'crowds_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'margins_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Round']", 'related_name': "'byes'"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'supercoach_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'winners_bonus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'winners_score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.club': {
            'Meta': {'ordering': "['name']", 'object_name': 'Club'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True', 'related_name': "'clubs'"})
        },
        'main.coach': {
            'Meta': {'ordering': "['-season', 'club', 'last_name', 'first_name']", 'object_name': 'Coach'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'coaches'"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'has_paid_fees': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_assistant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Season']", 'related_name': "'coaches'"})
        },
        'main.game': {
            'Meta': {'ordering': "('-round__season', 'round', 'game_date', 'afl_home')", 'object_name': 'Game'},
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
            'legends_away_supercoach_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_away_winners_bonus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_away_winners_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_home': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'legends_game_home'"}),
            'legends_home_crowds_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_home_margins_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_home_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_home_supercoach_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_home_winners_bonus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_home_winners_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Round']", 'related_name': "'games'"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'tipping_deadline': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'})
        },
        'main.ground': {
            'Meta': {'ordering': "['name']", 'object_name': 'Ground'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'main.player': {
            'Meta': {'ordering': "['-season', 'club', 'last_name', 'initial', 'first_name']", 'object_name': 'Player'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'players'"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '1', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Season']", 'related_name': "'players'"}),
            'supercoach_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30', 'null': 'True'})
        },
        'main.round': {
            'Meta': {'ordering': "('-season', 'start_time')", 'object_name': 'Round'},
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
            'Meta': {'ordering': "['-season']", 'object_name': 'Season'},
            'has_full_data': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_no_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'season': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.supercoachranking': {
            'Meta': {'db_table': "'main_supercoach_ranking'", 'object_name': 'SupercoachRanking'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Game']", 'related_name': "'supercoach_rankings'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Player']", 'related_name': "'supercoach_rankings'"}),
            'ranking': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.supercoachtip': {
            'Meta': {'ordering': "('player__last_name', 'player__initial', 'player__first_name')", 'db_table': "'main_supercoach_tip'", 'object_name': 'SupercoachTip'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Player']", 'null': 'True', 'related_name': "'supercoach_tips'"}),
            'tip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Tip']", 'related_name': "'supercoach_tips'"})
        },
        'main.tip': {
            'Meta': {'ordering': "('-game', 'club')", 'object_name': 'Tip'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'tips'"}),
            'crowd': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'crowds_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Game']", 'related_name': "'tips'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'margin': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'margins_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'supercoach_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'null': 'True', 'related_name': "'tip_winners'"}),
            'winners_score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['main']