# Utility functions for the migrations


# Mapping functions
# First define a generic one and then use it in model specific ones

def model_map(old_db, old_table, new_model,
              old_fields=('id',), new_fields=('id', )):
    '''
    Map fields on old database to objects in new one.
    'old_fields' is a tuple of either a column name in the old database or a
    tuple of column name and a mapping of old id to new object (to handle
    foreign keys in the old table).
    '''

    mapping = {}

    old_flds = []
    for fld in old_fields:
        if isinstance(fld, tuple):
            old_flds.append(fld[0])
        else:
            old_flds.append(fld)
    query = 'select {} from {}'.format(', '.join(old_flds), old_table)
    old_data = old_db.execute(query)

    for row in old_data:
        if len(row) == 1:
            key = row[0]
            filter_args = {new_fields[0]: row[0]}
        else:
            key = row[0]
            old_flds = row[1:]
            filter_args = {}
            for i, f in enumerate(new_fields):
                fld = old_flds[i]
                if isinstance(fld, tuple):
                    filter_args[f] = fld[1][old_flds[i]]
                else:
                    filter_args[f] = old_flds[i]
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


def player_map(old_db, model, fk_models):
    c_map = club_map(old_db, fk_models['club'])

    return model_map(
        old_db, 'player', model,
        ('id', 'season_id', ('club_id', c_map), 'first_name', 'initial', 'last_name'),
        ('season__season', 'club', 'first_name', 'initial', 'last_name')
    )


def game_map(old_db, model, fk_models):
    c_map = club_map(old_db, fk_models['club'])
    r_map = round_map(old_db, fk_models['round'])

    return model_map(
        old_db, 'afl_fixture', model,
        ('id', ('round_id', r_map), ('away_id', c_map), ('home_id', c_map)),
        ('round', 'afl_away', 'afl_home')
    )


def tip_map(old_db, model, fk_models):
    c_map = club_map(old_db, fk_models['club'])
    g_map = game_map(
        old_db,
        fk_models['game'],
        fk_models={
            'round': fk_models['round'],
            'club': fk_models['club']
        }
    )

    return model_map(
        old_db, 'tip', model,
        ('id', ('afl_fixture_id', g_map), ('club_id', c_map)),
        ('game', 'club')
    )
