# Utility functions for the migrations

from datetime import timedelta, timezone


# Make sure get the time right in the database:)
TZ_OFFSET = 10


def fix_date(date):
    return date.replace(tzinfo=timezone(timedelta(hours=TZ_OFFSET)))


# Mapping functions
# First define a generic one and then use it in model specific ones

def model_map(old_db, old_table, new_model,
              old_fields=('id',), new_fields=('id', )):
    '''
    Map fields on old database to objects in new one.
    '''

    mapping = {}

    query = 'select {} from {}'.format(', '.join(old_fields), old_table)

    old_data = old_db.execute(query)

    for row in old_data:
        if len(row) == 1:
            key = row[0]
            filter_args = {new_fields[0]: row[0]}
        else:
            key = row[0]
            cols = row[1:]
            filter_args = {f: cols[i] for i, f in enumerate(new_fields)}
        mapping[key] = new_model.objects.get(**filter_args)

    return mapping

# Model specific mappings


def season_map(old_db, model):
    return model_map(old_db, 'season', model, ('season', ), ('season', ))


def club_map(old_db, model):
    return model_map(old_db, 'club', model, ('id', 'name'), ('name', ))


def ground_map(old_db, model):
    return model_map(old_db, 'venue', model, ('name', ), ('name', ))


def round_map(old_db, model):
    return model_map(
        old_db, 'round', model,
        ('id', 'season_id', 'name'),
        ('season__season', 'name')
    )
