import constants
from utils import last_exported


def get_conf_standings(db_root, conference):
    '''Get conference standings
    
    Arguments:
        db_root {Object} -- Root of Firebase database
        conference {String} -- Conference enum to get standings for
    '''

    print('Conference standings keyword found')
    try:
        print(f'Retrieving standings info for {conference} conf')
        conf_map_snapshot = db_root.child('conferenceMap').get()
        conf_id = conf_map_snapshot[conference.lower()]
        standings_info_snapshot = db_root.child('standings').get()

        last_export = last_exported(db_root, 'standings')

        conf_teams = [ (team['seed'], team['teamName']) for team_id, team in standings_info_snapshot.items() if team['conferenceId'] == conf_id ]
        sorted_teams = sorted(conf_teams, key=lambda tup: tup[0])
        
        team_standings = [ f"{team[0]}. {team[1]}" for team in sorted_teams[0:9] ]
        team_standings.append(last_export)
        
        return '\n'.join(team_standings)
    
    except Exception as e:
        print(e)
        return constants.UNEXPECTED_ERR_MSG

def get_nfl_standings(db_root):
    '''Get NFL standings
    
    Arguments:
        db_root {Object} -- Root of Firebase database
    '''
    
    try:
        print('Retrieving standings info for entire nfl')
        standings_info_snapshot = db_root.child('standings').get()

        last_export = last_exported(db_root, 'standings')

        nfl_teams = [ (team['rank'], team['teamName']) for team_id, team in standings_info_snapshot.items() if int(team['rank']) < 6 ]
        sorted_teams = sorted(nfl_teams, key=lambda tup: tup[0])
        
        team_standings = [ f"{team[0]}. {team[1]}" for team in sorted_teams ]
        team_standings.append("**The rest aren't contenders**")
        team_standings.append(last_export)
        
        return '\n'.join(team_standings)
    
    except Exception as e:
        print(e)
        return constants.UNEXPECTED_ERR_MSG