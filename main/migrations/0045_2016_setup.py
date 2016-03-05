# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

from south.utils import datetime_utils as datetime
from south.v2 import DataMigration
from django.contrib.auth.hashers import make_password

from main import constants


SEASON = 2016
GAME_DATA = '/home/jeff/src/legends_site/main/data/2016/fixtures_hs.html'
PLAYER_DATA = '/home/jeff/src/legends_site/main/data/2016/2016_players.html'

club_lookup = {
    'Adelaide Crows': 'Adelaide',
    'Brisbane Lions': 'Brisbane',
    'Carlton Blues': 'Carlton',
    'Collingwood Magpies': 'Collingwood',
    'Essendon Bombers': 'Essendon',
    'Fremantle Dockers': 'Fremantle',
    'Geelong Cats': 'Geelong',
    'Gold Coast Suns': 'Gold Coast',
    'GWS Giants': 'GWS',
    'Hawthorn Hawks': 'Hawthorn',
    'Melbourne Demons': 'Melbourne',
    'North Melbourne Kangaroos': 'North Melbourne',
    'Port Adelaide Power': 'Port Adelaide',
    'Richmond Tigers': 'Richmond',
    'St Kilda Saints': 'St Kilda',
    'Sydney Swans': 'Sydney',
    'West Coast Eagles': 'West Coast',
    'Western Bulldogs': 'Western Bulldogs',
}

user_names = {
    'crows': 'crows',
    'lions': 'lions',
    'blues': 'blues',
    'pies': 'pies',
    'bombers': 'bombers',
    'dockers': 'dockers',
    'cats': 'cats',
    'hawks': 'hawks',
    'demons': 'demons',
    'roos': 'roos',
    'power': 'power',
    'tigers': 'tigers',
    'saints': 'saints',
    'swans': 'swans',
    'eagles': 'eagles',
    'dogs': 'dogs',
    'suns': 'suns',
    'giants': 'giants'
}


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        self.orm = orm

        self.import_season(SEASON)
        self.update_users()
        self.import_coaches()
        self.import_grounds()
        self.import_games()
        self.import_players()
        self.import_past_winners()

    def backwards(self, orm):
        pass

    def import_season(self, year):
        """
        Add a new season
        """
        self.orm.Season.objects.create(season=year)

    def update_users(self):
        """
        Update existing users
        """
        for u, p in user_names.items():
            user = self.orm['auth.User'].objects.get(username=u)
            user.password = make_password(p)

            if u == 'saints':
                user.is_staff = False
                user.is_superuser = False

            if u == 'eagles':
                user.is_staff = True
                user.is_superuser = True

            user.save()

    def import_coaches(self):
        """
        Import the coaches for the new season.
        """
        season = self.orm.Season.objects.get(season=SEASON)
        clubs = dict((c.name, c) for c in self.orm.Club.objects.all())

        coaches = [
            {'club': clubs['Adelaide'], 'first_name': 'Terry',
             'last_name': 'Gregg', 'season': season},
            {'club': clubs['Brisbane'], 'first_name': 'Stephen',
             'last_name': 'Dods', 'season': season},
            {'club': clubs['Carlton'], 'first_name': 'Peter',
             'last_name': 'Cartsidimas', 'season': season},
            {'club': clubs['Carlton'], 'first_name': 'Bernard',
             'last_name': 'Bialecki', 'season': season},
            {'club': clubs['Collingwood'], 'first_name': 'Leon',
             'last_name': 'Christoforou', 'season': season},
            {'club': clubs['Essendon'], 'first_name': 'Lewis',
             'last_name': 'Mapperson', 'season': season},
            {'club': clubs['Fremantle'], 'first_name': 'Tom',
             'last_name': 'Wilmott', 'season': season},
            {'club': clubs['Geelong'], 'first_name': 'Chris',
             'last_name': 'Thompson', 'season': season},
            {'club': clubs['Gold Coast'], 'first_name': 'Rob',
             'last_name': 'Negri', 'season': season},
            {'club': clubs['GWS'], 'first_name': 'Andrew',
             'last_name': 'Rezauskis', 'season': season},
            {'club': clubs['Hawthorn'], 'first_name': 'Matt',
             'last_name': 'Healy', 'season': season},
            {'club': clubs['Melbourne'], 'first_name': 'John',
             'last_name': 'Grikepelis', 'season': season},
            {'club': clubs['North Melbourne'], 'first_name': 'Dion',
             'last_name': 'Gaunt', 'season': season},
            {'club': clubs['Port Adelaide'], 'first_name': 'Steve',
             'last_name': 'Vamvakas', 'season': season},
            {'club': clubs['Port Adelaide'], 'first_name': 'Alex',
             'last_name': 'Tsirogiannis', 'season': season},
            {'club': clubs['Richmond'], 'first_name': 'Paul',
             'last_name': 'Trethowan', 'season': season},
            {'club': clubs['St Kilda'], 'first_name': 'Justin',
             'last_name': 'Page', 'season': season},
            {'club': clubs['Sydney'], 'first_name': 'Gary',
             'last_name': 'Paterson', 'season': season},
            {'club': clubs['West Coast'], 'first_name': 'Jeff',
             'last_name': 'de Ruyter', 'season': season},
            {'club': clubs['Western Bulldogs'], 'first_name': 'Jonathan',
             'last_name': 'Healy', 'season': season},
        ]

        for coach in coaches:
            self.orm.Coach.objects.create(**coach)

        # Adjust is_staff and is_superuser as necessary
        saints = self.orm.Coach.objects.get(season=season, club=clubs['St Kilda'])
        saints.is_staff = False
        saints.is_superuser = False
        saints.save()

        eagles = self.orm.Coach.objects.get(season=season, club=clubs['West Coast'])
        eagles.is_staff = True
        eagles.is_superuser = True
        eagles.save()

    def import_grounds(self):
        """
        Add new grounds and update ground names if there have been any changes.
        """
        # New grounds
        # grounds is a tuple of ground names
        grounds = ('Domain Stadium', )
        for ground in grounds:
            g = self.orm.Ground(name=ground)
            g.save()

        # Name changes
        # Changes are a tuple of (old_name, new_name) for each changed ground
        for grnd in ():
            ground = self.orm.Ground.objects.get(name=grnd[0])
            ground.name = grnd[1]
            ground.save()

#    def import_round(self, season, round_name, game_count, games, byes, clubs):
#        """
#        Create a round and set up its fixtures
#        """
#        start_time = games[0].game_date
#        deadline = start_time - datetime.timedelta(minutes=30)
#
#        current_round = self.orm.Round()
#        current_round.is_finals = False
#        current_round.is_split = False
#        current_round.name = round_name
#        current_round.num_bogs = 1
#        current_round.num_games = game_count
#        current_round.season = season
#        current_round.status = constants.Round.SCHEDULED
#        current_round.start_time = start_time
#        current_round.tipping_deadline = deadline
#        current_round.save()
#
#        # Add the games
#        for game in games:
#            deadline = game.game_date - datetime.timedelta(minutes=30)
#
#            game.round = current_round
#            game.tipping_deadline = deadline
#            game.save()
#
#            # Create empty tips for each club
#            for club in clubs:
#                tip = self.orm.Tip.objects.create(
#                    game=game, club=club, is_default=True)
#                self.orm.SupercoachTip.objects.create(tip=tip)
#
#        for bye in byes:
#            bye.round = current_round
#            bye.save()

    def import_games(self):
        """
        Import the games for the season.
        """
        game_re = re.compile(
            '''(?P<home>[a-zA-Z ]+) v (?P<away>[a-zA-Z ]+) at (?P<ground>[a-zA-Z, ]+)( \((?P<time>\d\.\d\dpm)\))?$'''
        )

        grounds_sub = {
            'Cazalys Stadium, Cairns': "Cazaly's Stadium",
            'Subiaco Oval': 'Domain Stadium',
            'Subiaco Oval at': 'Domain Stadium',
            'TIO Traeger Park, Alice Springs': 'TIO Traeger Park',
            'TIO Stadium, Darwin': 'TIO Stadium',
        }
        clubs_sub = {
            'Brisbane Lions': 'Brisbane',
            'Gold Coast Suns': 'Gold Coast',
            'GWS Giants': 'GWS',
            'Sydney Swans': 'Sydney',
            'West Coast Eagles': 'West Coast'
        }

        season = self.orm.Season.objects.get(season=SEASON)
        clubs = {c.name: c for c in self.orm.Club.objects.all() if c.name != 'Fitzroy'}
        grounds = {v.name: v for v in self.orm.Ground.objects.all()}

        byes = []
        games = []
        rnd_args = {}
        delta = datetime.timedelta(minutes=30)

        soup = BeautifulSoup(open(GAME_DATA))
        start = soup.find('div', 'w_other-stories')
        for para in start.next_siblings:
            bold = para.find('b')
            if bold:
                text = bold.contents[0]
                if 'Byes' in text:
                    text = para.contents[1]
            else:
                text = para.contents[0]

            # Stop here but save round 23 first
            if 'published' in text:
                rnd_args['tipping_deadline'] = games[0]['tipping_deadline']
                rnd_args['start_time'] = games[0]['game_date']
                rnd_args['num_games'] = len(games)
                rnd = self.orm.Round(**rnd_args)
                rnd.save()

                for game in games:
                    g = self.orm.Game(**game)
                    g.round = rnd
                    g.save()

                    # Create empty tips for each club
                    for club in clubs.values():
                        tip = self.orm.Tip.objects.create(
                            game=g, club=club, is_default=True)
                        self.orm.SupercoachTip.objects.create(tip=tip)

                break

            # Build up the fixture list
            # Round and dates are in bold, games aren't
            if bold:
                if 'ROUND' in text:
                    # Save everything from the previous round and start again
                    if text != 'ROUND 1':
                        rnd_args['tipping_deadline'] = games[0]['tipping_deadline']
                        rnd_args['start_time'] = games[0]['game_date']
                        rnd_args['num_games'] = len(games)
                        rnd = self.orm.Round(**rnd_args)
                        rnd.save()

                        for game in games:
                            g = self.orm.Game(**game)
                            g.round = rnd
                            g.save()

                            # Create empty tips for each club
                            for club in clubs.values():
                                tip = self.orm.Tip.objects.create(
                                    game=g, club=club, is_default=True)
                                self.orm.SupercoachTip.objects.create(tip=tip)

                        for bye in byes:
                            b = self.orm.Bye(**bye)
                            b.round = rnd
                            b.save()

                    byes = []
                    games = []
                    deadline = None

                    rnd_args = {
                        'name': text.title(),
                        'is_finals': False,
                        'num_bogs': 1,
                        'num_games': 0,
                        'season': season,
                        'status': constants.Round.SCHEDULED,
                        'start_time': None,
                        'tipping_deadline': None
                    }
                elif 'and' in text:
                    bye_clubs = text.strip().split(', ')
                    for c in bye_clubs[:-1]:
                        name = clubs_sub.get(c, c)
                        byes.append({'club': clubs[name]})
                    for c in bye_clubs[-1].split(' and '):
                        name = clubs_sub.get(c, c)
                        byes.append({'club': clubs[name]})
                else:
                    week_day, month, day = text.split()
            else:
                game_args = {}
                game = game_re.match(text).groupdict()
                for key in ('home', 'away'):
                    club = clubs[clubs_sub.get(game[key], game[key])]
                    game_args['afl_{}'.format(key)] = club
                    game_args['legends_{}'.format(key)] = club
                game_args['ground'] = grounds[
                    grounds_sub.get(game['ground'], game['ground'])]

                # Set game date
                if not game['time']:
                    time = '12.00pm'
                else:
                    time = game['time']
                date = datetime.datetime.strptime(
                    '{} {} {} 2016'.format(time, day, month),
                    '%I.%M%p %d %B %Y'
                )
                game_args['game_date'] = date

                # Set game tipping deadline
                if week_day in ('Thursday', 'Friday', 'Monday'):
                    deadline = date - delta
                elif rnd_args['name'] == 'Round 1' and week_day == 'Saturday':
                    if deadline is None:
                        deadline = date - delta
                game_args['tipping_deadline'] = deadline

                # Reset deadline if day is not a normal weekend day (Friday,
                # Saturday, Sunday) since the current deadline won't apply
                if week_day in ('Thursday', 'Monday'):
                    deadline = None

                game_args['status'] = constants.Round.SCHEDULED

                games.append(game_args)

        # Finals rounds
        start_time = datetime.datetime(2016, 9, 9, hour=12)
        deadline = start_time - datetime.timedelta(minutes=30)
        rnd = self.orm.Round()
        rnd.is_finals = True
        rnd.is_split = False
        rnd.name = 'Finals Week 1'
        rnd.num_bogs = 5
        rnd.num_games = 4
        rnd.season = season
        rnd.status = 'Scheduled'
        rnd.start_time = start_time
        rnd.tipping_deadline = deadline
        rnd.save()

        start_time += datetime.timedelta(days=7)
        deadline = start_time - datetime.timedelta(minutes=30)
        rnd = self.orm.Round()
        rnd.is_finals = True
        rnd.is_split = False
        rnd.name = 'Finals Week 2'
        rnd.num_bogs = 5
        rnd.num_games = 2
        rnd.season = season
        rnd.status = 'Scheduled'
        rnd.start_time = start_time
        rnd.tipping_deadline = deadline
        rnd.save()

        start_time += datetime.timedelta(days=7)
        deadline = start_time - datetime.timedelta(minutes=30)
        rnd = self.orm.Round()
        rnd.is_finals = True
        rnd.is_split = False
        rnd.name = 'Finals Week 3'
        rnd.num_bogs = 5
        rnd.num_games = 2
        rnd.season = season
        rnd.status = 'Scheduled'
        rnd.start_time = start_time
        rnd.tipping_deadline = deadline
        rnd.save()

        start_time += datetime.timedelta(days=7)
        deadline = start_time - datetime.timedelta(minutes=30)
        rnd = self.orm.Round()
        rnd.is_finals = True
        rnd.is_split = False
        rnd.name = 'Grand Final'
        rnd.num_bogs = 7
        rnd.num_games = 1
        rnd.season = season
        rnd.status = 'Scheduled'
        rnd.start_time = start_time
        rnd.tipping_deadline = deadline
        rnd.save()

    def import_players(self):
        season = self.orm.Season.objects.get(season=SEASON)
        clubs = dict((c.name, c) for c in self.orm.Club.objects.all())

        def player_a_tags(tag):
            if tag.name != 'a':
                return False

            if 'href' not in tag.attrs:
                return False

            if tag['href'].startswith('pp-'):
                return True

            return False

        soup = BeautifulSoup(open(PLAYER_DATA))
        player_tags = soup.find_all(player_a_tags)
        for tag in player_tags:
            player_str = tag.contents[0]

            if 'Unknown' in player_str:
                continue

            club_str = tag.next_sibling.next_sibling.contents[0]
            last_name, first_name = player_str.split(', ')
            club = clubs[club_lookup[club_str]]
            sc_name = '{} {}'.format(first_name, last_name)

            args = {
                'season': season,
                'club': club,
                'first_name': first_name,
                'last_name': last_name,
                'supercoach_name': sc_name
            }
            p = self.orm.Player(**args)
            p.save()

    def import_past_winners(self):
        club_names = (
            'Carlton',
            'Essendon',
            'Melbourne',
            'Richmond',
            'St Kilda',
            'Sydney',
        )

        clubs = dict(
            (c.name, c) for c in self.orm.Club.objects.all()
            if c.name in club_names
        )
        # 2015 Winners
        season = self.orm.Season.objects.get(season=2015)
        data = {
            constants.PrizeCategories.PREMIER: clubs['Melbourne'],
            constants.PrizeCategories.RUNNER_UP: clubs['Richmond'],
            constants.PrizeCategories.MINOR_PREMIER: clubs['Melbourne'],
            constants.PrizeCategories.WOODEN_SPOON: clubs['St Kilda'],
            constants.PrizeCategories.COLEMAN: clubs['Sydney'],
            constants.PrizeCategories.BROWNLOW: clubs['Essendon'],
            constants.PrizeCategories.MARGINS: clubs['Sydney'],
            constants.PrizeCategories.CROWDS: clubs['Richmond'],
            constants.PrizeCategories.HIGH_SEASON: clubs['Sydney'],
            constants.PrizeCategories.HIGH_ROUND: clubs['Sydney'],
        }

        for key, value in data.items():
            self.orm.PastCategoryWinner.objects.create(
                season=season, club=value, category=key)

    # Not needed every year
    def import_new_user(self, user_name, password):
        """
        Create a new non-superuser
        """
        kwargs = {
            'username': user_name,
            'password': password,
        }
        user, created = self.orm['auth.User'].objects.get_or_create(**kwargs)
        if created:
            user.groups.add(self.orm['auth.Group'].objects.get(name='coach'))

        return user

    def import_new_club(self, name, nickname, user):
        """
        Create a new club
        """
        kwargs = {
            'name': name,
            'nickname': nickname,
            'user': user
        }

        self.orm.Club.objects.create(**kwargs)

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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
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
            'is_manual_result': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'Meta': {'object_name': 'PastCategoryWinner', 'db_table': "'main_past_category_winner'", 'ordering': "('-season__season', 'category', 'club')"},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_category_winners'", 'to': "orm['main.Club']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'past_category_winners'", 'to': "orm['main.Season']"})
        },
        'main.pastcoach': {
            'Meta': {'object_name': 'PastCoach', 'db_table': "'main_past_coach'", 'ordering': "['-season', 'club', 'last_name', 'first_name']"},
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
            'Meta': {'object_name': 'StreakLadder', 'db_table': "'main_streak_ladder'", 'ordering': "['wins', 'draws', '-losses', 'club']"},
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
            'Meta': {'object_name': 'SupercoachRanking', 'db_table': "'main_supercoach_ranking'"},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercoach_rankings'", 'to': "orm['main.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercoach_rankings'", 'to': "orm['main.Player']"}),
            'ranking': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.supercoachtip': {
            'Meta': {'object_name': 'SupercoachTip', 'db_table': "'main_supercoach_tip'", 'ordering': "('player__last_name', 'player__initial', 'player__first_name')"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercoach_tips'", 'to': "orm['main.Player']", 'null': 'True'}),
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
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tip_winners'", 'to': "orm['main.Club']", 'null': 'True'}),
            'winners_score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['main']
    symmetrical = True
