# -*- coding: utf-8 -*-
from south.v2 import DataMigration


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        for year in range(1994, 2015):
            season = orm.Season(
                season=year,
                has_full_data=year >= 2008,
                has_no_data=year == 2006
            )
            season.save()

    def backwards(self, orm):
        pass

    models = {
        'core.season': {
            'Meta': {'object_name': 'Season'},
            'has_full_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_no_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'season': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['core']
    symmetrical = True
