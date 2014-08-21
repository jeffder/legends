# Utility functions for the Legends project

from datetime import timedelta, timezone


# Make sure get the time right in the database:)
TIMEZONE = '+1000'
TZ_OFFSET = 10


def fix_date(date):
    return date.replace(tzinfo=timezone(timedelta(hours=TZ_OFFSET)))


# Mapping functions
# A generic one followed by more specialised ones
# TODO: Pass map of old to new fields instead of old_fields and new_fields
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
