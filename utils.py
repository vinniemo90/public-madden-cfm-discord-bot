import json
from datetime import datetime, time, timezone

from pytz import timezone


def last_exported(db_root, export_type) -> str:
    if '/' in export_type:
        last_export_utc = db_root.child(f'lastExported/{export_type}').get()

    else:
        last_export_snapshot = db_root.child('lastExported').get()
        last_export_utc = last_export_snapshot.get(export_type)

    if not last_export_utc:
        return "\n*last exported: N/A*"
    
    date_format = '%Y-%m-%d %H:%M:%S.%f%z'
    datetime_obj = datetime.strptime(last_export_utc, date_format)
    est = timezone('US/Eastern')

    #convert utc to est
    est_time = datetime_obj.astimezone(est)
    
    return f"\n*last exported: {est_time.strftime('%m/%d/%Y at %-I:%M%p %Z')}*"


def pluralize(number, word, suffix='s'):
    return f'{word}{suffix}' if number > 1 else word

def get_league_rules():
    '''Get league rules
    
    Returns:
        List -- CFM league rules
    '''

    with open('cfm-rules.json') as rules:
        cfm_rules = json.load(rules)
        return '\n'.join(cfm_rules['league rules'])
