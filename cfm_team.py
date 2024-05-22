from numerize.numerize import numerize

import constants
import response_objects
from utils import last_exported, pluralize

def get_available_teams(db_root) -> str:
    last_export = last_exported(db_root, 'leagueInfo')
    
    team_snapshot = db_root.child('teams').get()
    available_teams = [ team.get('displayName') for id, team in team_snapshot.items() if not team.get('userName')]
    
    if available_teams:
        available_teams_msg = f'**{len(available_teams)} {pluralize(len(available_teams), "Team")} Available:**'
        available_teams.insert(0, available_teams_msg)
        available_teams.append(last_export)

        return '\n'.join(available_teams)
    
    return f'All teams are taken at this time \n{last_export}'

def get_team_info(db_root, team) -> str:
    '''Get general team specific info
    
    Arguments:
        db_root {Object} -- Reference to root of Firebase database
        team {String} -- Team to lookup

    Returns:
        String -- team info
    '''

    try:
        print(f'Retrieving team info for {team}')
        team_map_snapshot = db_root.child('teamMap').get()
        team_id = team_map_snapshot.get(team.upper())
        
        if not team_id:
            return f'Unable to find team **{team}**. Please try again.'
        
        last_export = last_exported(db_root, 'leagueInfo')
        
        team_info_snapshot = db_root.child('teams').child(team_id).get()

        response_objects.team_info_dict['City'] = team_info_snapshot['cityName']
        response_objects.team_info_dict['Mascot'] = team_info_snapshot['displayName']
        response_objects.team_info_dict['Division'] = team_info_snapshot['divName']
        response_objects.team_info_dict['Ovr Rating'] = team_info_snapshot['ovrRating']

        if team_info_snapshot['userName']:
            response_objects.team_info_dict['Owner'] = team_info_snapshot['userName']
        else:
            response_objects.team_info_dict['Owner'] = 'CPU'

        team_info = [ f'**{key}**: {val}' for key, val in response_objects.team_info_dict.items() ]
        team_info.append(last_export)
        return '\n'.join(team_info)
    
    except Exception as e:
        print(e)
        return constants.UNEXPECTED_ERR_MSG


def get_team_season_stats(db_root, team):
    '''Get season stats for specific team
    
    Arguments:
        db_root {Object} -- Reference to root of Firebase database
        team {String} -- Team to lookup

    Returns:
        String -- season stats
    '''

    try:
        print(f'Retrieving team season stats for {team}')
        team_map_snapshot = db_root.child('teamMap').get()
        team_id = team_map_snapshot.get(team.upper())

        if not team_id:
            return f'Unable to find team **{team}**. Please try again.'
        
        last_export = last_exported(db_root, 'standings')
        
        team_info_snapshot = db_root.child('standings').child(team_id).get()

        response_objects.team_stats_dict['Team'] = team_info_snapshot.get('teamName')
        response_objects.team_stats_dict['Team Rank'] = team_info_snapshot.get('rank')
        response_objects.team_stats_dict['Prev. Team Rank'] = team_info_snapshot.get('prevRank')
        response_objects.team_stats_dict['Pts For Rank'] = team_info_snapshot.get('ptsForRank')
        response_objects.team_stats_dict['Pts Against Rank'] = team_info_snapshot.get('ptsAgainstRank')
        response_objects.team_stats_dict['Off Total Yds Rank'] = team_info_snapshot.get('offTotalYdsRank')
        response_objects.team_stats_dict['Off Pass Yds Rank'] = team_info_snapshot.get('offPassYdsRank')
        response_objects.team_stats_dict['Off Rush Yds Rank'] = team_info_snapshot.get('offRushYdsRank')
        response_objects.team_stats_dict['Def Total Yds Rank'] = team_info_snapshot.get('defTotalYdsRank')
        response_objects.team_stats_dict['Def Pass Yds Rank'] = team_info_snapshot.get('defPassYdsRank')
        response_objects.team_stats_dict['Def Rush Yds Rank'] = team_info_snapshot.get('defRushYdsRank')
        response_objects.team_stats_dict['TO Diff'] = team_info_snapshot.get('tODiff')

        team_stats = [ f'**{key}**: {val}' for key, val in response_objects.team_stats_dict.items() ]
        team_stats.append(last_export)
        return '\n'.join(team_stats)
    
    except Exception as e:
        print(e)
        return constants.UNEXPECTED_ERR_MSG
    

def get_team_record(db_root, team):
    '''Get team record
    
    Arguments:
        db_root {Object} -- Reference to root of Firebase database
        team {String} -- Team to lookup

    Returns:
        String -- team record
    '''

    try:
        print(f'Retrieving season record for {team}')
        team_map_snapshot = db_root.child('teamMap').get()
        team_id = team_map_snapshot.get(team.upper())

        if not team_id:
            return f'Unable to find team **{team}**. Please try again.'
        
        last_export = last_exported(db_root, 'standings')
        
        team_standings_snapshot = db_root.child('standings').child(team_id).get()

        team_record = f"**{team_standings_snapshot['teamName']}**: {team_standings_snapshot.get('totalWins')}-{team_standings_snapshot.get('totalLosses')}-{team_standings_snapshot.get('totalTies')} ({team_standings_snapshot.get('divWins')}-{team_standings_snapshot.get('divLosses')}-{team_standings_snapshot.get('divTies')}) \n{last_export}"

        return team_record
    
    except Exception as e:
        print(e)
        return constants.UNEXPECTED_ERR_MSG


def get_team_cap(db_root, team):
    '''Get salary cap info for specific team
    
    Arguments:
        db_root {Object} -- Reference to root of Firebase database
        team {String} -- Team to lookup

    Returns:
        String -- salary cap info
    '''

    print('Cap keyword found')
    
    try:
        print(f'Retrieving salary cap info for {team}')
        team_map_snapshot = db_root.child('teamMap').get()
        team_id = team_map_snapshot.get(team.upper())

        if not team_id:
            return f'Unable to find team **{team}**. Please try again.'

        last_export = last_exported(db_root, 'leagueInfo')
        
        team_standings_snapshot = db_root.child('standings').child(team_id).get()

        response_objects.team_cap_dict['Team'] = team_standings_snapshot['teamName']
        response_objects.team_cap_dict['Cap Available'] = f"${numerize(team_standings_snapshot['capAvailable'])}"

        team_cap = [ f'**{key}**: {val}' for key, val in response_objects.team_cap_dict.items() ]
        team_cap.append(last_export)
        return '\n'.join(team_cap)
    
    except Exception as e:
        print(e)
        return constants.UNEXPECTED_ERR_MSG
    

def get_injured_players(db_root, team):
    '''Get injured players for specific team
    
    Arguments:
        db_root {Object} -- Reference to root of Firebase database
        team {String} -- Team to lookup

    Returns:
        String -- injured players
    '''

    print('Injuries keyword found')
    
    try:
        print(f'Retrieving injuries info for {team}')
        team_map_snapshot = db_root.child('teamMap').get()
        team_id = team_map_snapshot.get(team.upper())

        if not team_id:
            return f'Unable to find team **{team}**. Please try again.'
        
        last_export = last_exported(db_root, 'rosters')

        team_info_snapshot = db_root.child('teams').child(team_id).get()
        roster_snapshot = db_root.child('rosters').child(team_id).get()

        injury_message = f"**{team_info_snapshot['displayName']}** have {team_info_snapshot['injuryCount']} players injured:"
        injured_players = [ player 
        for player in roster_snapshot 
        if player['injuryLength'] != 0 and player['isActive'] == False]

        injured_players_sorted = sorted(injured_players, key=lambda x: x.get('injuryLength', float('inf')))

        injured_players_sorted = [ f"{player['position']} - {player['firstName']} {player['lastName']} ({player['playerBestOvr']} OVR) - **{player['injuryLength']} wks**" 
        for player in injured_players_sorted ]

        injured_players_sorted.insert(0, injury_message)
        injured_players_sorted.append(last_export)

        return '\n'.join(injured_players_sorted)
    
    except Exception as e:
        print(e)
        return constants.UNEXPECTED_ERR_MSG


def get_expiring_contracts(db_root, team):
    '''Get players with 1 year left on their contract for a specific team
    
    Arguments:
        db_root {Object} -- Reference to root of Firebase database
        team {String} -- Team to lookup

    Returns:
        String -- players with expiring contracts
    '''

    print('Resign keyword found')
    
    try:
        print(f'Retrieving expiring contracts for {team}')
        team_map_snapshot = db_root.child('teamMap').get()
        team_id = team_map_snapshot.get(team.upper())
        team_info_snapshot = db_root.child('teams').child(team_id).get()
        roster_snapshot = db_root.child('rosters').child(team_id).get()
        
        last_export = last_exported(db_root, 'rosters')

        expiring_contracts = [ player 
        for player in roster_snapshot 
        if player['contractYearsLeft'] == 1 ]
        
        contract_message = f"**{len(expiring_contracts)} {team_info_snapshot['displayName']} have expiring contracts**"
        constract_message_2 = "__Here are the ones that matter__"
        expiring_contracts_sorted = sorted(expiring_contracts, key=lambda x: x.get('playerBestOvr', float('-inf')), reverse=True)
        
        expiring_contracts_sorted = [ f"{player['position']} {player['firstName']} {player['lastName']} ({player['playerBestOvr']} OVR)" 
        for player in expiring_contracts_sorted 
        if player['playerBestOvr'] > 79 or (('LB' in player['position'] or player['position'] == 'LE' or player['position'] == 'RE') and player['speedRating'] > 87) or player['speedRating'] > 93 ]

        expiring_contracts_sorted.insert(0, constract_message_2)
        expiring_contracts_sorted.insert(0, contract_message)
        expiring_contracts_sorted.append(last_export)
        
        return '\n'.join(expiring_contracts_sorted)
    
    except Exception as e:
        print(e)
        return constants.UNEXPECTED_ERR_MSG
