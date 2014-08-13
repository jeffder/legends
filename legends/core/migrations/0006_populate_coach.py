# -*- coding: utf-8 -*-
from south.db import dbs
from south.v2 import DataMigration


coaches = [
    {
        'first_name': 'Terry', 'last_name': 'Gregg',
        'club': 1, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Damian', 'last_name': 'Speechley',
        'club': 2, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Peter', 'last_name': 'Cartsidimas',
        'club': 3, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Bernard', 'last_name': 'Bialecki',
        'club': 3, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Gary', 'last_name': 'Paterson',
        'club': 4, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Justin', 'last_name': 'West',
        'club': 5, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Tom', 'last_name': 'Wilmott',
        'club': 6, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Paul', 'last_name': 'Quinn',
        'club': 7, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Campbell', 'last_name': 'Banks',
        'club': 8, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Leon', 'last_name': 'Christoforou',
        'club': 9, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Chris', 'last_name': 'Malizia',
        'club': 10, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Steve', 'last_name': 'Vamvakas',
        'club': 11, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Alex', 'last_name': 'Tsirogiannis',
        'club': 11, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Rob', 'last_name': 'Negri',
        'club': 12, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Peter', 'last_name': 'Moran',
        'club': 12, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Jeff', 'last_name': 'de Ruyter',
        'club': 13, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Andrew', 'last_name': 'Rezauskis',
        'club': 14, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Dave', 'last_name': 'Danckert',
        'club': 16, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Chris', 'last_name': 'Balkos',
        'club': 16, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Maurice', 'last_name': 'Sheridan',
        'club': 15, 'season': 2008, 'has_paid_fees': True
    },
    {
        'first_name': 'Terry', 'last_name': 'Gregg',
        'club': 1, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Stephen', 'last_name': 'Dods',
        'club': 2, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Peter', 'last_name': 'Cartsidimas',
        'club': 3, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Bernard', 'last_name': 'Bialecki',
        'club': 3, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Gary', 'last_name': 'Paterson',
        'club': 4, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Justin', 'last_name': 'West',
        'club': 5, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Tom', 'last_name': 'Wilmott',
        'club': 6, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Paul', 'last_name': 'Quinn',
        'club': 7, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Campbell', 'last_name': 'Banks',
        'club': 8, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Leon', 'last_name': 'Christoforou',
        'club': 9, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Chris', 'last_name': 'Malizia',
        'club': 10, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Steve', 'last_name': 'Vamvakas',
        'club': 11, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Alex', 'last_name': 'Tsirogiannis',
        'club': 11, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Rob', 'last_name': 'Negri',
        'club': 12, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Peter', 'last_name': 'Moran',
        'club': 12, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Jeff', 'last_name': 'de Ruyter',
        'club': 13, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Andrew', 'last_name': 'Rezauskis',
        'club': 14, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Dave', 'last_name': 'Danckert',
        'club': 16, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Chris', 'last_name': 'Balkos',
        'club': 16, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Maurice', 'last_name': 'Sheridan',
        'club': 15, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Ben', 'last_name': 'West',
        'club': 5, 'season': 2009, 'has_paid_fees': True
    },
    {
        'first_name': 'Terry', 'last_name': 'Gregg',
        'club': 1, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Stephen', 'last_name': 'Dods',
        'club': 2, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Peter', 'last_name': 'Cartsidimas',
        'club': 3, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Bernard', 'last_name': 'Bialecki',
        'club': 3, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Gary', 'last_name': 'Paterson',
        'club': 4, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Justin', 'last_name': 'West',
        'club': 5, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Tom', 'last_name': 'Wilmott',
        'club': 6, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Paul', 'last_name': 'Quinn',
        'club': 7, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Campbell', 'last_name': 'Banks',
        'club': 8, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Leon', 'last_name': 'Christoforou',
        'club': 9, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Chris', 'last_name': 'Malizia',
        'club': 10, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Steve', 'last_name': 'Vamvakas',
        'club': 11, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Alex', 'last_name': 'Tsirogiannis',
        'club': 11, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Rob', 'last_name': 'Negri',
        'club': 12, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Jeff', 'last_name': 'de Ruyter',
        'club': 13, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Andrew', 'last_name': 'Rezauskis',
        'club': 14, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Dave', 'last_name': 'Danckert',
        'club': 16, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Chris', 'last_name': 'Balkos',
        'club': 16, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Maurice', 'last_name': 'Sheridan',
        'club': 15, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Ben', 'last_name': 'West',
        'club': 5, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Peter', 'last_name': 'Moran',
        'club': 12, 'season': 2010, 'has_paid_fees': True
    },
    {
        'first_name': 'Terry', 'last_name': 'Gregg',
        'club': 1, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Stephen', 'last_name': 'Dods',
        'club': 2, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Peter', 'last_name': 'Cartsidimas',
        'club': 3, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Bernard', 'last_name': 'Bialecki',
        'club': 3, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Leon', 'last_name': 'Christoforou',
        'club': 4, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Kieran', 'last_name': 'Moloney',
        'club': 5, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Tom', 'last_name': 'Wilmott',
        'club': 6, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Paul', 'last_name': 'Quinn',
        'club': 7, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Paul', 'last_name': 'Trethowan',
        'club': 17, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Brad', 'last_name': 'Hughes',
        'club': 8, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'John', 'last_name': 'Grikepelis',
        'club': 9, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Chris', 'last_name': 'Malizia',
        'club': 10, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Steve', 'last_name': 'Vamvakas',
        'club': 11, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Alex', 'last_name': 'Tsirogiannis',
        'club': 11, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Rob', 'last_name': 'Negri',
        'club': 12, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Jeff', 'last_name': 'de Ruyter',
        'club': 13, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Gary', 'last_name': 'Paterson',
        'club': 14, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Dave', 'last_name': 'Danckert',
        'club': 16, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Chris', 'last_name': 'Balkos',
        'club': 16, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Maurice', 'last_name': 'Sheridan',
        'club': 15, 'season': 2011, 'has_paid_fees': True
    },
    {
        'first_name': 'Terry', 'last_name': 'Gregg',
        'club': 1, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Stephen', 'last_name': 'Dods',
        'club': 2, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Peter', 'last_name': 'Cartsidimas',
        'club': 3, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Bernard', 'last_name': 'Bialecki',
        'club': 3, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Leon', 'last_name': 'Christoforou',
        'club': 4, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Kieran', 'last_name': 'Moloney',
        'club': 5, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Tom', 'last_name': 'Wilmott',
        'club': 6, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Paul', 'last_name': 'Quinn',
        'club': 7, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Paul', 'last_name': 'Trethowan',
        'club': 17, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Andrew', 'last_name': 'Rezauskis',
        'club': 18, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Adam', 'last_name': 'Rowlston',
        'club': 8, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'John', 'last_name': 'Grikepelis',
        'club': 9, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Steve', 'last_name': 'Vamvakas',
        'club': 11, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Alex', 'last_name': 'Tsirogiannis',
        'club': 11, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Rob', 'last_name': 'Negri',
        'club': 12, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Jeff', 'last_name': 'de Ruyter',
        'club': 13, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Gary', 'last_name': 'Paterson',
        'club': 14, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Maurice', 'last_name': 'Sheridan',
        'club': 15, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Brad', 'last_name': 'Hughes',
        'club': 16, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Dion', 'last_name': 'Gaunt',
        'club': 10, 'season': 2012, 'has_paid_fees': True
    },
    {
        'first_name': 'Terry', 'last_name': 'Gregg',
        'club': 1, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'Stephen', 'last_name': 'Dods',
        'club': 2, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'Peter', 'last_name': 'Cartsidimas',
        'club': 3, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'Bernard', 'last_name': 'Bialecki',
        'club': 3, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'Leon', 'last_name': 'Christoforou',
        'club': 4, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'Kieran', 'last_name': 'Moloney',
        'club': 5, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'Tom', 'last_name': 'Wilmott',
        'club': 6, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'John', 'last_name': 'Mackie',
        'club': 7, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'Paul', 'last_name': 'Trethowan',
        'club': 17, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'Andrew', 'last_name': 'Rezauskis',
        'club': 18, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'Adam', 'last_name': 'Rowlston',
        'club': 8, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'John', 'last_name': 'Grikepelis',
        'club': 9, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'Dion', 'last_name': 'Gaunt',
        'club': 10, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'Steve', 'last_name': 'Vamvakas',
        'club': 11, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'Alex', 'last_name': 'Tsirogiannis',
        'club': 11, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'Rob', 'last_name': 'Negri',
        'club': 12, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'Jeff', 'last_name': 'de Ruyter',
        'club': 13, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'Gary', 'last_name': 'Paterson',
        'club': 14, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'Travis', 'last_name': 'Chisholm',
        'club': 15, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'Brad', 'last_name': 'Hughes',
        'club': 16, 'season': 2013, 'has_paid_fees': True
    },
    {
        'first_name': 'Terry', 'last_name': 'Gregg',
        'club': 1, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'Stephen', 'last_name': 'Dods',
        'club': 2, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'Peter', 'last_name': 'Cartsidimas',
        'club': 3, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'Bernard', 'last_name': 'Bialecki',
        'club': 3, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'Leon', 'last_name': 'Christoforou',
        'club': 4, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'Kieran', 'last_name': 'Moloney',
        'club': 5, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'Tom', 'last_name': 'Wilmott',
        'club': 6, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'John', 'last_name': 'Mackie',
        'club': 7, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'Rob', 'last_name': 'Negri',
        'club': 17, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'Andrew', 'last_name': 'Rezauskis',
        'club': 18, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'Adam', 'last_name': 'Rowlston',
        'club': 8, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'John', 'last_name': 'Grikepelis',
        'club': 9, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'Dion', 'last_name': 'Gaunt',
        'club': 10, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'Steve', 'last_name': 'Vamvakas',
        'club': 11, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'Alex', 'last_name': 'Tsirogiannis',
        'club': 11, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'Paul', 'last_name': 'Trethowan',
        'club': 12, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'Jeff', 'last_name': 'de Ruyter',
        'club': 13, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'Gary', 'last_name': 'Paterson',
        'club': 14, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'Jonathan', 'last_name': 'Healy',
        'club': 15, 'season': 2014, 'has_paid_fees': True
    },
    {
        'first_name': 'Brad', 'last_name': 'Hughes',
        'club': 16, 'season': 2014, 'has_paid_fees': True
    }
]


class Migration(DataMigration):

    def forwards(self, orm):
        model = orm.Coach

        seasons = {s.season: s for s in orm.Season.objects.all()}
        clubs = {c.name: c for c in orm.Club.objects.all()}

        # Get the asistant coaches
        assistants = set(
            ('Bernard Bialecki', 'Ben West', 'Peter Moran', 'Chris Balkos')
        )

        # Map old club IDs to the new ones
        old = dbs['old'].execute("select * from club")
        old_clubs = {c[0]: c[1] for c in old}

        for c in coaches:
            name = '{} {}'.format(c['first_name'], c['last_name'])
            is_assistant = name in assistants

            coach = orm.Coach(
                club=clubs[old_clubs[c['club']]],
                first_name=c['first_name'],
                has_paid_fees=c['has_paid_fees'],
                is_assistant=is_assistant,
                last_name=c['last_name'],
                season=seasons[c['season']]
            )
            coach.save()

    def backwards(self, orm):
        orm.Coach.objects.all().delete()

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
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
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.captain': {
            'Meta': {'ordering': "('-player__season', 'club')", 'object_name': 'Captain'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'club_captain'", 'to': "orm['core.Club']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_captain'", 'to': "orm['core.Player']"})
        },
        'core.club': {
            'Meta': {'ordering': "['name']", 'object_name': 'Club'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'related_name': "'clubs'", 'to': "orm['auth.User']"})
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
        'core.player': {
            'Meta': {'ordering': "['-season', 'club', 'last_name', 'initial', 'first_name']", 'object_name': 'Player'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': "orm['core.Club']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '1', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': "orm['core.Season']"}),
            'supercoach_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'})
        },
        'core.season': {
            'Meta': {'ordering': "['-season']", 'object_name': 'Season'},
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
    symmetrical = True
