# -*- coding: utf-8 -*-
from django.utils import timezone

from south.v2 import DataMigration


# Make sure get the time right in the database:)
TIMEZONE = '+1000'

users = [
    {
        'username': 'jeff',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': True,
        'is_staff': True,
        'last_login': '2014-03-25T20:04:46.187{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$unKAiiJMc6Is$VfOEjZ6eWIFB8iJjI5ZV65mYQlibJYOKNo/PeQJFCp8=',
        'email': 'jderuyter@iinet.net.au',
        'date_joined': '2008-03-19T21:19:51.035{}'.format(TIMEZONE)
    },
    {
        'username': 'rez',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': True,
        'is_staff': True,
        'last_login': '2013-03-19T12:03:18.918{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$L9jbYgwQx4qe$b1jb0GLXr7uop1ASMybSkJxbbMSIDOhEbSdv0lorhZg=',
        'email': '',
        'date_joined': '2008-03-19T21:15:00{}'.format(TIMEZONE)
    },
    {
        'username': 'crows',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': False,
        'is_staff': False,
        'last_login': '2014-06-06T12:57:19.462{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$A7HIlIKarDQm$ITKJqUkNjCdcJi2zBNGWT7/ugnkF2rSW0Ax36oDjm+s=',
        'email': '',
        'date_joined': '2008-03-19T21:15:00{}'.format(TIMEZONE)
    },
    {
        'username': 'lions',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': False,
        'is_staff': False,
        'last_login': '2014-05-13T18:56:18.715{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$Eh0TkbuJvcvS$DCqLVGaQ28Sc27XRdZ8bTvlIxMnXrn57ApT6EOT53dk=',
        'email': '',
        'date_joined': '2008-03-19T21:15:00{}'.format(TIMEZONE)
    },
    {
        'username': 'blues',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': False,
        'is_staff': False,
        'last_login': '2014-05-19T22:05:36.244{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$aV5FcSFFrYmD$3/wGZNjJKblO0zyZnYE4mjnAJNv+qOj4gfCqhPjYC/s=',
        'email': '',
        'date_joined': '2008-03-19T21:15:00{}'.format(TIMEZONE)
    },
    {
        'username': 'pies',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': False,
        'is_staff': False,
        'last_login': '2014-06-28T00:28:21.652{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$ikVd611doPVv$LmCXr+7CtC5lWlBwLf1BIDRwNUM0VdI8buMGPGG5VgY=',
        'email': '',
        'date_joined': '2008-03-19T21:15:00{}'.format(TIMEZONE)
    },
    {
        'username': 'bombers',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': False,
        'is_staff': False,
        'last_login': '2014-05-15T19:26:05.526{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$WQoUX7MQaNfR$BUVLof58K5rW2ss2fe2tXjZVwgRLX+lJEvZp/vKymK8=',
        'email': '',
        'date_joined': '2008-03-19T21:15:00{}'.format(TIMEZONE)
    },
    {
        'username': 'dockers',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': False,
        'is_staff': False,
        'last_login': '2014-06-27T16:24:29.347{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$MCjbvsumg29a$qEqjGo2+x1wUWAHTw1XzXPeClt9MyoF4691kdLNgVCE=',
        'email': '',
        'date_joined': '2008-03-19T21:15:00{}'.format(TIMEZONE)
    },
    {
        'username': 'fitzroy',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': False,
        'is_staff': False,
        'last_login': '2014-03-09T11:01:16.278{}'.format(TIMEZONE),
        'password': 'arpeigjbn50tu25408yu40-5q035tu35yuty80',
        'email': '',
        'date_joined': '2014-03-09T11:01:16.278{}'.format(TIMEZONE)
    },
    {
        'username': 'cats',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': False,
        'is_staff': False,
        'last_login': '2014-06-27T17:01:20.123{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$XKInlMMdgmcc$3+VUag3673JQIruXvPjjmESKnwBxCdw/eCTLcer455w=',
        'email': '',
        'date_joined': '2008-03-19T21:15:00{}'.format(TIMEZONE)
    },
    {
        'username': 'suns',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': False,
        'is_staff': False,
        'last_login': '2014-06-23T15:43:08.939{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$HCwsKusqduHE$MqIYj4Q+H2iVt5Rg8AoEFgf6h6wczY9aPUlUra2yXwE=',
        'email': '',
        'date_joined': '2011-08-31T21:34:53{}'.format(TIMEZONE)
    },
    {
        'username': 'giants',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': True,
        'is_staff': True,
        'last_login': '2014-06-26T11:46:32.957{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$WiYptbzApGXe$Oyp9LR2MJm1bsuNQqVj2fnyrZLrlaKFlQnaKm5FyVXI=',
        'email': '',
        'date_joined': '2012-03-27T19:32:19{}'.format(TIMEZONE)
    },
    {
        'username': 'hawks',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': False,
        'is_staff': False,
        'last_login': '2014-06-27T17:31:14.652{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$Ap8NLy5L3bXg$ESegpRypsaKq6CVWQBH7yT3F0YgqkdpfcQbTeEI1fG4=',
        'email': '',
        'date_joined': '2008-03-19T21:15:00{}'.format(TIMEZONE)
    },
    {
        'username': 'demons',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': False,
        'is_staff': False,
        'last_login': '2014-06-27T17:05:58.007{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$ODK5SXDqZiPc$8DszWIT8VFRyjdLw24slFB3xxzN9xXtLIAJlTYHD/tI=',
        'email': '',
        'date_joined': '2008-03-19T21:15:00{}'.format(TIMEZONE)
    },
    {
        'username': 'roos',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': False,
        'is_staff': False,
        'last_login': '2014-06-27T21:50:07.983{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$Gif4AGyKAtYU$8UqRfd93yrn6Ah4n4qdH5EA9HoQZje0d/t0pQwbyz3s=',
        'email': '',
        'date_joined': '2008-03-19T21:15:00.939{}'.format(TIMEZONE)
    },
    {
        'username': 'power',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': False,
        'is_staff': False,
        'last_login': '2014-06-12T21:58:19.669{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$zlCYY15Tvlcl$sItu9BVi39R/YRGA0yT/W8W8zUGKFI1ou+hrxNNLh4g=',
        'email': '',
        'date_joined': '2008-03-19T21:15:00{}'.format(TIMEZONE)
    },
    {
        'username': 'tigers',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': False,
        'is_staff': False,
        'last_login': '2014-06-25T14:33:41.125{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$CRzCw2auuDzF$mPIY6E6L6ht6EculqJso6gIZRs0AXwsMrtAuPEf0KrU=',
        'email': '',
        'date_joined': '2008-03-19T21:15:00{}'.format(TIMEZONE)
    },
    {
        'username': 'saints',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': True,
        'is_staff': True,
        'last_login': '2014-08-06T20:04:51.265{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$12000$5xfK84suMKU1$DWZ9EOV1uLwFRHIlc3MIKbcZ4FAyemTYiYEr0WZC+D4=',
        'email': '',
        'date_joined': '2008-03-19T21:15:00{}'.format(TIMEZONE)
    },
    {
        'username': 'swans',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': False,
        'is_staff': False,
        'last_login': '2014-06-27T14:29:25.559{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$XHS6kFgv5iin$+3C/DHz0riVKI/nReOWTvILzkPeNs31lNkTbERdhOqI=',
        'email': '',
        'date_joined': '2008-03-19T21:15:00{}'.format(TIMEZONE)
    },
    {
        'username': 'eagles',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': False,
        'is_staff': False,
        'last_login': '2014-06-15T21:41:54.148{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$tN68pHDdYI6H$ktNHM8R3163Ss2DpaflifHJ5L/F4FlY1WamwPi9OnUo=',
        'email': '',
        'date_joined': '2008-03-19T21:15:00{}'.format(TIMEZONE)
    },
    {
        'username': 'dogs',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_superuser': False,
        'is_staff': False,
        'last_login': '2014-06-27T23:49:37.994{}'.format(TIMEZONE),
        'password': 'pbkdf2_sha256$10000$rHOW7lMjclP1$n7aJPwSFhgSz0qhUl834yjMUGB3qwfkmtCR4p17sQI0=',
        'email': '',
        'date_joined': '2008-03-19T21:15:00{}'.format(TIMEZONE)
    },
]


class Migration(DataMigration):

    def forwards(self, orm):
        model = orm['auth.User']

        for u in users:
            user = model(**u)
            user.save()

    def backwards(self, orm):
        model = orm['auth.User']
        model.objects.all().delete()

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
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
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.captain': {
            'Meta': {'object_name': 'Captain', 'ordering': "('-player__season', 'club')"},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'club_captain'", 'to': "orm['main.Club']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_captain'", 'to': "orm['main.Player']"})
        },
        'main.club': {
            'Meta': {'object_name': 'Club', 'ordering': "['name']"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'related_name': "'clubs'", 'to': "orm['auth.User']"})
        },
        'main.coach': {
            'Meta': {'object_name': 'Coach', 'ordering': "['-season', 'club', 'last_name', 'first_name']"},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coaches'", 'to': "orm['main.Club']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '30'}),
            'has_paid_fees': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '30'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coaches'", 'to': "orm['main.Season']"})
        },
        'main.player': {
            'Meta': {'object_name': 'Player', 'ordering': "['-season', 'club', 'last_name', 'initial', 'first_name']"},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': "orm['main.Club']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '1'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': "orm['main.Season']"}),
            'supercoach_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'})
        },
        'main.season': {
            'Meta': {'object_name': 'Season', 'ordering': "['-season']"},
            'has_full_data': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_no_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'season': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.ground': {
            'Meta': {'object_name': 'Ground'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['main']
    symmetrical = True
