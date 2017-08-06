# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

from south.utils import datetime_utils as datetime
from south.v2 import DataMigration
from django.contrib.auth.hashers import make_password

from main import constants


SEASON = 2017
GAME_DATA = '/home/jeff/src/legends/main/data/2017/fixtures_2017.txt'
PLAYER_DATA = '/home/jeff/src/legends/main/data/2017/players_2017.html'

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
        grounds = (
            'Eureka Stadium', 'Jiangwan Stadium', 'UTAS Stadium'
        )
        for ground in grounds:
            g = self.orm.Ground(name=ground)
            g.save()

        # Name changes
        # Changes are a tuple of (old_name, new_name) for each changed ground
        for grnd in ():
            ground = self.orm.Ground.objects.get(name=grnd[0])
            ground.name = grnd[1]
            ground.save()

    def import_games(self):
        """
        Import the games for the season.
        """
        season = self.orm.Season.objects.get(season=SEASON)
        clubs = {c.name: c for c in self.orm.Club.objects.all() if c.name != 'Fitzroy'}
        grounds = {g.name: g for g in self.orm.Ground.objects.all()}

        byes = []
        games = []
        rnd_args = {'name': 'Round 1'}
        delta = datetime.timedelta(minutes=30)

        lines = open(GAME_DATA, 'r').readlines()

        for line in lines:
            line = line.strip()
            if line.startswith('Round'):
                if line != 'Round 1':
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

                    for club in byes:
                        bye = self.orm.Bye(club=club, round=rnd)
                        bye.save()

                rnd_args = {
                    'name': line.title(),
                    'is_finals': False,
                    'num_bogs': 1,
                    'num_games': 0,
                    'season': season,
                    'status': constants.Round.SCHEDULED,
                    'start_time': None,
                    'tipping_deadline': None
                }

                games = []
                byes = []

            elif 'BYE' in line:
                club = clubs[line.split(',')[0]]
                byes.append(club)

            else:
                game_args = {}

                date_str, home, away, ground = line.split(',')

                date = datetime.datetime.strptime(
                    '{} 2017'.format(date_str),
                    '%a %d %b %I:%M%p %Y'
                )
                game_args['game_date'] = date

                # Set game tipping deadline
                week_day = date.weekday()
                if week_day in (0, 1, 3, 4):
                    deadline = date - delta
                game_args['tipping_deadline'] = deadline

                # Reset deadline if day is not a normal weekend day (Friday,
                # Saturday, Sunday) since the current deadline won't apply
                if week_day in (0, 1, 3):
                    deadline = None

                # Home/away clubs
                club = clubs[home]
                game_args['afl_home'] = club
                game_args['legends_home'] = club

                club = clubs[away]
                game_args['afl_away'] = club
                game_args['legends_away'] = club

                # Ground
                game_args['ground'] = grounds[ground]

                # Status
                game_args['status'] = constants.Round.SCHEDULED

                games.append(game_args)

        # Save Round 23
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

        # Finals rounds
        start_time = datetime.datetime(2017, 9, 8, hour=12)
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
            'Adelaide',
            'Fremantle',
            'Port Adelaide',
            'Richmond',
            'Sydney',
            'Western Bulldogs',
            'West Coast',
        )

        clubs = dict(
            (c.name, c) for c in self.orm.Club.objects.all()
            if c.name in club_names
        )
        # 2016 Winners
        season = self.orm.Season.objects.get(season=2016)
        data = {
            constants.PrizeCategories.PREMIER: clubs['Richmond'],
            constants.PrizeCategories.RUNNER_UP: clubs['Fremantle'],
            constants.PrizeCategories.MINOR_PREMIER: clubs['Sydney'],
            constants.PrizeCategories.WOODEN_SPOON: clubs['West Coast'],
            constants.PrizeCategories.COLEMAN: clubs['Western Bulldogs'],
            constants.PrizeCategories.BROWNLOW: clubs['Sydney'],
            constants.PrizeCategories.MARGINS: clubs['Adelaide'],
            constants.PrizeCategories.CROWDS: clubs['Richmond'],
            constants.PrizeCategories.HIGH_SEASON: clubs['Sydney'],
            constants.PrizeCategories.HIGH_ROUND: clubs['Port Adelaide'],
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True', 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.aflladder': {
            'Meta': {'db_table': "'main_afl_ladder'", 'object_name': 'AFLLadder'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'aflladders'"}),
            'draw': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loss': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'percentage': ('django.db.models.fields.FloatField', [], {'null': 'True', 'default': '0'}),
            'played': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'points': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previous_position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Round']", 'related_name': "'aflladders'"}),
            'score_against': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score_for': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'win': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.brownlowladder': {
            'Meta': {'db_table': "'main_brownlow_ladder'", 'object_name': 'BrownlowLadder'},
            'avg_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'brownlowladders'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'min_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'nothing': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previous_position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rank_1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rank_2': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rank_3': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rank_4': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rank_5': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Round']", 'related_name': "'brownlowladders'"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'strike_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'default': '0'})
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
            'first_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '30'}),
            'has_paid_fees': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_assistant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '30'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Season']", 'related_name': "'coaches'"})
        },
        'main.colemanladder': {
            'Meta': {'db_table': "'main_coleman_ladder'", 'object_name': 'ColemanLadder'},
            'avg_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'default': '0'}),
            'bonus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bonus_strike_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'colemanladders'"}),
            'eight': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'five': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'four': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'min_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'nine': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nothing': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'one': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previous_position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Round']", 'related_name': "'colemanladders'"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'seven': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'six': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'strike_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'default': '0'}),
            'three': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'two': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'winners': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.crowdsladder': {
            'Meta': {'db_table': "'main_crowds_ladder'", 'object_name': 'CrowdsLadder'},
            'avg_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'default': '0'}),
            'bonus_strike_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'crowdsladders'"}),
            'exact': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'four': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'min_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'nothing': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'one': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previous_position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Round']", 'related_name': "'crowdsladders'"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'strike_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'default': '0'}),
            'three': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'two': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'is_manual_result': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
        'main.legendsladder': {
            'Meta': {'db_table': "'main_legends_ladder'", 'object_name': 'LegendsLadder'},
            'avg_against': ('django.db.models.fields.FloatField', [], {'null': 'True', 'default': '0'}),
            'avg_for': ('django.db.models.fields.FloatField', [], {'null': 'True', 'default': '0'}),
            'bye_for': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'legendsladders'"}),
            'draw': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loss': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'max_against': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'max_for': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'min_against': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'min_for': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'percentage': ('django.db.models.fields.FloatField', [], {'null': 'True', 'default': '0'}),
            'played': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'points': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previous_position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Round']", 'related_name': "'legendsladders'"}),
            'score_against': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score_for': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_for': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'win': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.marginsladder': {
            'Meta': {'db_table': "'main_margins_ladder'", 'object_name': 'MarginsLadder'},
            'avg_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'default': '0'}),
            'bonus_strike_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'marginsladders'"}),
            'exact': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'five': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'four': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'min_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'nothing': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'one': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'other': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previous_position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Round']", 'related_name': "'marginsladders'"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'strike_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'default': '0'}),
            'three': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'two': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.pastbrownlowladder': {
            'Meta': {'db_table': "'main_past_brownlow_ladder'", 'object_name': 'PastBrownlowLadder'},
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'pastbrownlowladders'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Season']", 'related_name': "'past_pastbrownlowladders'"})
        },
        'main.pastcategorywinner': {
            'Meta': {'ordering': "('-season__season', 'category', 'club')", 'db_table': "'main_past_category_winner'", 'object_name': 'PastCategoryWinner'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'null': 'True', 'related_name': "'past_category_winners'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Season']", 'related_name': "'past_category_winners'"})
        },
        'main.pastcoach': {
            'Meta': {'ordering': "['-season', 'club', 'last_name', 'first_name']", 'db_table': "'main_past_coach'", 'object_name': 'PastCoach'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'past_coaches'"}),
            'first_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '30'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Season']", 'related_name': "'past_coaches'"})
        },
        'main.pastcolemanladder': {
            'Meta': {'db_table': "'main_past_coleman_ladder'", 'object_name': 'PastColemanLadder'},
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'pastcolemanladders'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Season']", 'related_name': "'past_pastcolemanladders'"})
        },
        'main.pastcrowdsladder': {
            'Meta': {'db_table': "'main_past_crowds_ladder'", 'object_name': 'PastCrowdsLadder'},
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'pastcrowdsladders'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Season']", 'related_name': "'past_pastcrowdsladders'"})
        },
        'main.pastlegendsladder': {
            'Meta': {'db_table': "'main_past_legends_ladder'", 'object_name': 'PastLegendsLadder'},
            'avg_points_against': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'avg_points_for': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'pastlegendsladders'"}),
            'draw': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loss': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'percentage': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'played': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'points_against': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'points_for': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Season']", 'related_name': "'past_pastlegendsladders'"}),
            'win': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.pastmarginsladder': {
            'Meta': {'db_table': "'main_past_margins_ladder'", 'object_name': 'PastMarginsLadder'},
            'avg_score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'pastmarginsladders'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Season']", 'related_name': "'past_pastmarginsladders'"})
        },
        'main.player': {
            'Meta': {'ordering': "['-season', 'club', 'last_name', 'initial', 'first_name']", 'object_name': 'Player'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'players'"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '1'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Season']", 'related_name': "'players'"}),
            'supercoach_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '30'})
        },
        'main.round': {
            'Meta': {'ordering': "('season', 'start_time')", 'object_name': 'Round'},
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
        'main.streakladder': {
            'Meta': {'ordering': "['wins', 'draws', '-losses', 'club']", 'db_table': "'main_streak_ladder'", 'object_name': 'StreakLadder'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'related_name': "'streak_ladders'"}),
            'draws': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'losses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'previous_position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Round']", 'related_name': "'streak_ladders'"}),
            'streak': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'wins': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0'}),
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
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'supercoach_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Club']", 'null': 'True', 'related_name': "'tip_winners'"}),
            'winners_score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['main']
    symmetrical = True
