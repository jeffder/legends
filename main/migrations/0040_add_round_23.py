# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.v2 import DataMigration

from main import constants


SEASON = 2015
GAME_DATA = (
    'Round 23,Friday September 04,Hawthorn,Carlton,MCG,12.00am',
    'Round 23,Friday September 04,Geelong,Adelaide,Simonds Stadium,12.00am',
    'Round 23,Friday September 04,Richmond,North Melbourne,Etihad Stadium,12.00am',
    'Round 23,Friday September 04,Port Adelaide,Fremantle,Adelaide Oval,12.00am',
    'Round 23,Friday September 04,Collingwood,Essendon,MCG,12.00am',
    'Round 23,Friday September 04,Sydney,Gold Coast,SCG,12.00am',
    'Round 23,Friday September 04,Melbourne,GWS,Etihad Stadium,12.00am',
    'Round 23,Friday September 04,West Coast,St Kilda,Patersons Stadium,12.00am',
    'Round 23,Friday September 04,Brisbane,Western Bulldogs,Gabba,12.00am'
)


class Migration(DataMigration):

    def forwards(self, orm):
        # No need to run for Firebird conversion
        pass
        self.orm = orm

        self.import_games()

    def backwards(self, orm):
        pass

    def import_round(self, season, round_name, game_count, games, clubs):
        """
        Create a round and set up its fixtures
        """
        start_time = games[0].game_date
        deadline = start_time - datetime.timedelta(minutes=30)

        current_round = self.orm.Round()
        current_round.is_finals = False
        current_round.is_split = False
        current_round.name = round_name
        current_round.num_bogs = 1
        current_round.num_games = game_count
        current_round.season = season
        current_round.status = constants.Round.SCHEDULED
        current_round.start_time = start_time
        current_round.tipping_deadline = deadline
        current_round.save()

        # Add the games
        for game in games:
            deadline = game.game_date - datetime.timedelta(minutes=30)

            game.round = current_round
            game.tipping_deadline = deadline
            game.save()

            # Create empty tips for each club
            for club in clubs:
                tip = self.orm.Tip.objects.create(
                    game=game, club=club, is_default=True)
                self.orm.SupercoachTip.objects.create(tip=tip)

    def import_games(self):
        """
        Import the games for the season.
        """
        season = self.orm.Season.objects.get(season=SEASON)
        clubs = dict((c.name, c) for c in self.orm.Club.objects.all())
        del clubs['Fitzroy']
        grounds = dict((v.name, v) for v in self.orm.Ground.objects.all())

        games = []
        game_count = 0

        for row in GAME_DATA:
            round_name, day, home, away, ground, time = row.split(',')

            date = datetime.datetime.strptime(
                '{} {} 2015'.format(time, day),
                '%I.%M%p %A %B %d %Y'
            )
            home = clubs[home.strip()]
            away = clubs[away.strip()]
            ground = grounds[ground.strip()]

            # Write AFL game
            game = self.orm.Game()
            game.afl_away = away
            game.legends_away = away
            game.game_date = date
            game.afl_home = home
            game.legends_home = home
            game.status = constants.Game.SCHEDULED
            game.ground = ground
            games.append(game)

            game_count += 1

        self.import_round(
            season, round_name, game_count, games, clubs.values())

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
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
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.aflladder': {
            'Meta': {'db_table': "'main_afl_ladder'", 'object_name': 'AFLLadder'},
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
            'Meta': {'db_table': "'main_brownlow_ladder'", 'object_name': 'BrownlowLadder'},
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'brownlowladders'", 'to': "orm['main.Club']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'min_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'nothing': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previous_position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rank_1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rank_2': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rank_3': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rank_4': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rank_5': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'brownlowladders'", 'to': "orm['main.Round']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'strike_rate': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'})
        },
        'main.bye': {
            'Meta': {'object_name': 'Bye', 'ordering': "('-round__season', 'round', 'club')"},
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
            'Meta': {'object_name': 'Club', 'ordering': "['name']"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clubs'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'main.coach': {
            'Meta': {'object_name': 'Coach', 'ordering': "['-season', 'club', 'last_name', 'first_name']"},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coaches'", 'to': "orm['main.Club']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'has_paid_fees': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_assistant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coaches'", 'to': "orm['main.Season']"})
        },
        'main.colemanladder': {
            'Meta': {'db_table': "'main_coleman_ladder'", 'object_name': 'ColemanLadder'},
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
            'Meta': {'db_table': "'main_crowds_ladder'", 'object_name': 'CrowdsLadder'},
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
            'Meta': {'object_name': 'Game', 'ordering': "('-round__season', 'round', 'game_date', 'afl_home')"},
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
            'Meta': {'object_name': 'Ground', 'ordering': "['name']"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'main.legendsladder': {
            'Meta': {'db_table': "'main_legends_ladder'", 'object_name': 'LegendsLadder'},
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
            'Meta': {'db_table': "'main_margins_ladder'", 'object_name': 'MarginsLadder'},
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
            'Meta': {'db_table': "'main_past_brownlow_ladder'", 'object_name': 'PastBrownlowLadder'},
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pastbrownlowladders'", 'to': "orm['main.Club']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_pastbrownlowladders'", 'to': "orm['main.Season']"})
        },
        'main.pastcategorywinner': {
            'Meta': {'db_table': "'main_past_category_winner'", 'object_name': 'PastCategoryWinner', 'ordering': "('-season__season', 'category', 'club')"},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_category_winners'", 'null': 'True', 'to': "orm['main.Club']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_category_winners'", 'to': "orm['main.Season']"})
        },
        'main.pastcoach': {
            'Meta': {'db_table': "'main_past_coach'", 'object_name': 'PastCoach', 'ordering': "['-season', 'club', 'last_name', 'first_name']"},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_coaches'", 'to': "orm['main.Club']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_coaches'", 'to': "orm['main.Season']"})
        },
        'main.pastcolemanladder': {
            'Meta': {'db_table': "'main_past_coleman_ladder'", 'object_name': 'PastColemanLadder'},
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pastcolemanladders'", 'to': "orm['main.Club']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_pastcolemanladders'", 'to': "orm['main.Season']"})
        },
        'main.pastcrowdsladder': {
            'Meta': {'db_table': "'main_past_crowds_ladder'", 'object_name': 'PastCrowdsLadder'},
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pastcrowdsladders'", 'to': "orm['main.Club']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_pastcrowdsladders'", 'to': "orm['main.Season']"})
        },
        'main.pastlegendsladder': {
            'Meta': {'db_table': "'main_past_legends_ladder'", 'object_name': 'PastLegendsLadder'},
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
            'Meta': {'db_table': "'main_past_margins_ladder'", 'object_name': 'PastMarginsLadder'},
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pastmarginsladders'", 'to': "orm['main.Club']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_pastmarginsladders'", 'to': "orm['main.Season']"})
        },
        'main.player': {
            'Meta': {'object_name': 'Player', 'ordering': "['-season', 'club', 'last_name', 'initial', 'first_name']"},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': "orm['main.Club']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': "orm['main.Season']"}),
            'supercoach_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True', 'null': 'True'})
        },
        'main.round': {
            'Meta': {'object_name': 'Round', 'ordering': "('season', 'start_time')"},
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
            'Meta': {'object_name': 'Season', 'ordering': "['-season']"},
            'has_full_data': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_no_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'season': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.streakladder': {
            'Meta': {'db_table': "'main_streak_ladder'", 'object_name': 'StreakLadder', 'ordering': "['wins', 'draws', '-losses', 'club']"},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'streak_ladders'", 'to': "orm['main.Club']"}),
            'draws': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'losses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'previous_position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'streak_ladders'", 'to': "orm['main.Round']"}),
            'streak': ('django.db.models.fields.CharField', [], {'max_length': '30', 'default': "''"}),
            'wins': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.supercoachranking': {
            'Meta': {'db_table': "'main_supercoach_ranking'", 'object_name': 'SupercoachRanking'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercoach_rankings'", 'to': "orm['main.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercoach_rankings'", 'to': "orm['main.Player']"}),
            'ranking': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.supercoachtip': {
            'Meta': {'db_table': "'main_supercoach_tip'", 'object_name': 'SupercoachTip', 'ordering': "('player__last_name', 'player__initial', 'player__first_name')"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercoach_tips'", 'null': 'True', 'to': "orm['main.Player']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'tip': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercoach_tips'", 'to': "orm['main.Tip']"})
        },
        'main.tip': {
            'Meta': {'object_name': 'Tip', 'ordering': "('-game', 'club')"},
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
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tip_winners'", 'null': 'True', 'to': "orm['main.Club']"}),
            'winners_score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['main']
    symmetrical = True
