# -*- coding: utf-8 -*-
from south.db import dbs
from south.v2 import DataMigration

from main.utils import migration


class Migration(DataMigration):

    def forwards(self, orm):
        old_db = dbs['old']

        round_map = migration.round_map(old_db, orm.Round)
        club_map = migration.club_map(old_db, orm.Club)

        ladders = old_db.execute('select * from margins_ladder')

        for ladder in ladders:
            ladder_args = {
                'club':  club_map[ladder[4]],
                'position':  ladder[15],
                'previous_position':  ladder[1],
                'round':  round_map[ladder[2]],
                'score': ladder[11],
                'max_score': ladder[16],
                'min_score': ladder[0],
                'avg_score': ladder[7],
                'strike_rate': ladder[5],
                'exact': ladder[3],
                'five': ladder[12],
                'four': ladder[9],
                'three': ladder[13],
                'two': ladder[6],
                'one': ladder[8],
                'other': ladder[10],
                'nothing': ladder[14],
                'bonus_strike_rate': ladder[18],
                }

            new_ladder = orm.MarginsLadder(**ladder_args)
            new_ladder.save()

    def backwards(self, orm):
        orm.MarginsLadder.objects.all().delete()

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.aflladder': {
            'Meta': {'object_name': 'AFLLadder', 'db_table': "'main_afl_ladder'"},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'aflladders'", 'to': "orm['main.Club']"}),
            'draw': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loss': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'percentage': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'played': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previous_position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'aflladders'", 'to': "orm['main.Round']"}),
            'score_against': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score_for': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'win': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.brownlowladder': {
            'Meta': {'object_name': 'BrownlowLadder', 'db_table': "'main_brownlow_ladder'"},
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'brownlowladders'", 'to': "orm['main.Club']"}),
            'five': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'four': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'min_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'nothing': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'one': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previous_position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'brownlowladders'", 'to': "orm['main.Round']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'strike_rate': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'three': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'two': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.bye': {
            'Meta': {'ordering': "('-round__season', 'round', 'club')", 'object_name': 'Bye'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'byes'", 'to': "orm['main.Club']"}),
            'crowds_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'margins_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'byes'", 'to': "orm['main.Round']"}),
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clubs'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'main.coach': {
            'Meta': {'ordering': "['-season', 'club', 'last_name', 'first_name']", 'object_name': 'Coach'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coaches'", 'to': "orm['main.Club']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'has_paid_fees': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_assistant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coaches'", 'to': "orm['main.Season']"})
        },
        'main.colemanladder': {
            'Meta': {'object_name': 'ColemanLadder', 'db_table': "'main_coleman_ladder'"},
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'bonus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bonus_strike_rate': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'colemanladders'", 'to': "orm['main.Club']"}),
            'eight': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'five': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'four': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'min_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'nine': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nothing': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'one': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previous_position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'colemanladders'", 'to': "orm['main.Round']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'seven': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'six': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'strike_rate': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'three': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'two': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'winners': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.crowdsladder': {
            'Meta': {'object_name': 'CrowdsLadder', 'db_table': "'main_crowds_ladder'"},
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'bonus_strike_rate': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'crowdsladders'", 'to': "orm['main.Club']"}),
            'exact': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'four': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'min_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'nothing': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'one': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previous_position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'crowdsladders'", 'to': "orm['main.Round']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'strike_rate': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'three': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'two': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.game': {
            'Meta': {'ordering': "('-round__season', 'round', 'game_date', 'afl_home')", 'object_name': 'Game'},
            'afl_away': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'afl_game_away'", 'to': "orm['main.Club']"}),
            'afl_away_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'afl_home': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'afl_game_home'", 'to': "orm['main.Club']"}),
            'afl_home_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'crowd': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'finals_game': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'game_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'ground': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'games'", 'to': "orm['main.Ground']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legends_away': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'legends_game_away'", 'to': "orm['main.Club']"}),
            'legends_away_crowds_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_away_margins_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_away_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_away_supercoach_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_away_winners_bonus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_away_winners_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_home': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'legends_game_home'", 'to': "orm['main.Club']"}),
            'legends_home_crowds_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_home_margins_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_home_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_home_supercoach_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_home_winners_bonus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'legends_home_winners_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'games'", 'to': "orm['main.Round']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'tipping_deadline': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'})
        },
        'main.ground': {
            'Meta': {'ordering': "['name']", 'object_name': 'Ground'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'main.legendsladder': {
            'Meta': {'object_name': 'LegendsLadder', 'db_table': "'main_legends_ladder'"},
            'avg_against': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'avg_for': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'bye_for': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'legendsladders'", 'to': "orm['main.Club']"}),
            'draw': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loss': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'max_against': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'max_for': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'min_against': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'min_for': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'percentage': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'played': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previous_position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'legendsladders'", 'to': "orm['main.Round']"}),
            'score_against': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score_for': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_for': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'win': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.marginsladder': {
            'Meta': {'object_name': 'MarginsLadder', 'db_table': "'main_margins_ladder'"},
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'bonus_strike_rate': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'marginsladders'", 'to': "orm['main.Club']"}),
            'exact': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'five': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'four': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'min_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'nothing': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'one': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'other': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previous_position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'marginsladders'", 'to': "orm['main.Round']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'strike_rate': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'three': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'two': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.pastbrownlowladder': {
            'Meta': {'object_name': 'PastBrownlowLadder', 'db_table': "'main_past_brownlow_ladder'"},
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pastbrownlowladders'", 'to': "orm['main.Club']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_pastbrownlowladders'", 'to': "orm['main.Season']"})
        },
        'main.pastcategorywinner': {
            'Meta': {'ordering': "('-season', 'category', 'club')", 'object_name': 'PastCategoryWinner', 'db_table': "'main_past_category_winner'"},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_category_winners'", 'to': "orm['main.Club']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_category_winners'", 'to': "orm['main.Season']"})
        },
        'main.pastcoach': {
            'Meta': {'ordering': "['-season', 'club', 'last_name', 'first_name']", 'object_name': 'PastCoach', 'db_table': "'main_past_coach'"},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_coaches'", 'to': "orm['main.Club']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_coaches'", 'to': "orm['main.Season']"})
        },
        'main.pastcolemanladder': {
            'Meta': {'object_name': 'PastColemanLadder', 'db_table': "'main_past_coleman_ladder'"},
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pastcolemanladders'", 'to': "orm['main.Club']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_pastcolemanladders'", 'to': "orm['main.Season']"})
        },
        'main.pastcrowdsladder': {
            'Meta': {'object_name': 'PastCrowdsLadder', 'db_table': "'main_past_crowds_ladder'"},
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pastcrowdsladders'", 'to': "orm['main.Club']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_pastcrowdsladders'", 'to': "orm['main.Season']"})
        },
        'main.pastlegendsladder': {
            'Meta': {'object_name': 'PastLegendsLadder', 'db_table': "'main_past_legends_ladder'"},
            'avg_points_against': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'avg_points_for': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pastlegendsladders'", 'to': "orm['main.Club']"}),
            'draw': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loss': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'percentage': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'played': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'points_against': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'points_for': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_pastlegendsladders'", 'to': "orm['main.Season']"}),
            'win': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.pastmarginsladder': {
            'Meta': {'object_name': 'PastMarginsLadder', 'db_table': "'main_past_margins_ladder'"},
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pastmarginsladders'", 'to': "orm['main.Club']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_pastmarginsladders'", 'to': "orm['main.Season']"})
        },
        'main.player': {
            'Meta': {'ordering': "['-season', 'club', 'last_name', 'initial', 'first_name']", 'object_name': 'Player'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': "orm['main.Club']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '1', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': "orm['main.Season']"}),
            'supercoach_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30', 'null': 'True'})
        },
        'main.round': {
            'Meta': {'ordering': "('-season', 'start_time')", 'object_name': 'Round'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_finals': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'num_bogs': ('django.db.models.fields.IntegerField', [], {}),
            'num_games': ('django.db.models.fields.IntegerField', [], {}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rounds'", 'to': "orm['main.Season']"}),
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
        'main.streakladder': {
            'Meta': {'ordering': "['wins', 'draws', '-losses', 'club']", 'object_name': 'StreakLadder', 'db_table': "'main_streak_ladder'"},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'streak_ladders'", 'to': "orm['main.Club']"}),
            'draws': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'losses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'previous_position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'streak_ladders'", 'to': "orm['main.Round']"}),
            'streak': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'wins': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.supercoachranking': {
            'Meta': {'object_name': 'SupercoachRanking', 'db_table': "'main_supercoach_ranking'"},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercoach_rankings'", 'to': "orm['main.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercoach_rankings'", 'to': "orm['main.Player']"}),
            'ranking': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.supercoachtip': {
            'Meta': {'ordering': "('player__last_name', 'player__initial', 'player__first_name')", 'object_name': 'SupercoachTip', 'db_table': "'main_supercoach_tip'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercoach_tips'", 'to': "orm['main.Player']", 'null': 'True'}),
            'tip': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercoach_tips'", 'to': "orm['main.Tip']"})
        },
        'main.tip': {
            'Meta': {'ordering': "('-game', 'club')", 'object_name': 'Tip'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tips'", 'to': "orm['main.Club']"}),
            'crowd': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'crowds_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tips'", 'to': "orm['main.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'margin': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'margins_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'supercoach_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tip_winners'", 'to': "orm['main.Club']", 'null': 'True'}),
            'winners_score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['main']
    symmetrical = True
