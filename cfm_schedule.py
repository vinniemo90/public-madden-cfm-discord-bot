import constants

from utils import last_exported, pluralize


def get_weekly_stats(db_root, week_type, week_number) -> dict:
    '''Get top performers from each stat category for the week
    
    Arguments:
        db_root {Object} -- Root of Firebase database
        week_type {String} -- Preseason or Regular season
        week_number {String} -- Week number
    
    Returns:
        Dict -- Top performers from each stat category
    '''

    try:
        top_performers = {
            'passing': [],
            'rushing': [],
            'receiving': [],
            'tackles': [],
            'sacks': [],
            'ints': [],
        }

        weeks_snapshot = db_root.child(f'weeks/{week_type}/{week_number}').get()
        
        for stat_category in constants.TP_STATS_CATEGORIES:
            match stat_category:
                case 'passing':
                    passing_stats = weeks_snapshot.get(stat_category)
                    passing_stats_sorted = sorted(passing_stats, key=lambda x: x.get('passYds', float('-inf')), reverse=True)
                    top_performers['passing'] = passing_stats_sorted[:3]

                case 'rushing':
                    rushing_stats = weeks_snapshot.get(stat_category)
                    rushing_stats_sorted = sorted(rushing_stats, key=lambda x: x.get('rushYds', float('-inf')), reverse=True)
                    top_performers['rushing'] = rushing_stats_sorted[:3]

                case 'receiving':
                    receiving_stats = weeks_snapshot.get(stat_category)
                    receiving_stats_sorted = sorted(receiving_stats, key=lambda x: x.get('recYds', float('-inf')), reverse=True)
                    top_performers['receiving'] = receiving_stats_sorted[:3]
    
                case 'defense':
                    defensive_stats = weeks_snapshot.get(stat_category)
                    tackles_sorted = sorted(defensive_stats, key=lambda x: x.get('defTotalTackles', float('-inf')), reverse=True)
                    sacks_sorted = sorted(defensive_stats, key=lambda x: x.get('defSacks', float('-inf')), reverse=True)
                    ints_sorted = sorted(defensive_stats, key=lambda x: x.get('defInts', float('-inf')), reverse=True)
                    top_performers['tackles'] = tackles_sorted[:3]
                    top_performers['sacks'] = sacks_sorted[:3]
                    top_performers['ints'] = ints_sorted[:3]

                case _:
                    print(f'Unaccounted for stat category {stat_category}')        
        
    except Exception as e:
        print(e)
        top_performers.clear()
        top_performers.append(constants.TOP_PERFORMERS_ERROR)

    return top_performers


def get_user_scores(db_root, week_type, week_number):
    '''Get user vs. user game scores and return as list
    
    Arguments:
        db_root {Object} -- Root of Firebase database
        week_type {String} -- Preseason or Regular season
        week_number {String} -- Week number
    
    Returns:
        List -- User vs. user game scores for the week
    '''

    try:
        team_snapshot = db_root.child('teams').get()
        user_team_ids = [ team['teamId'] for team_id, team in team_snapshot.items() if team['userName'] ]
        schedule_snapshot = db_root.child(f'weeks/{week_type}/{week_number}/schedules').get()
        
        user_games = []
        schedule = []
        
        if not schedule_snapshot:
            return ['Looks like this week hasn\'t been exported']

        for game_info in schedule_snapshot:
            if game_info['awayTeamId'] in user_team_ids and game_info['homeTeamId'] in user_team_ids:
                user_games.append((game_info['homeTeamId'], game_info['homeScore'], game_info['awayTeamId'], game_info['awayScore']))

        if user_games:
            for home_team_id, home_score, away_team_id, away_score in user_games:
                away_team_score = f"{team_snapshot[str(away_team_id)]['nickName']} {away_score}"
                home_team_score = f"{team_snapshot[str(home_team_id)]['nickName']} {home_score}"
                formatted_home_score = f'**{home_team_score}**' if home_score > away_score else home_team_score
                formatted_away_score = f'**{away_team_score}**' if away_score > home_score else away_team_score

                schedule.append(f"{formatted_away_score} @ {formatted_home_score}")

        else:
            schedule.append(f"No user vs. user games were found for {week_type} week {week_number}")

        return schedule
    
    except Exception as e:
        print(e)
        return ['Sorry, an error occurred retrieving user games.']

def get_user_games(db_root, week_type, week_number) -> list:
    '''Get user vs. user game schedule and return as list
    
    Arguments:
        db_root {Object} -- Root of Firebase database
        week_type {String} -- Preseason or Regular season
        week_number {String} -- Week number
    
    Returns:
        List -- User vs. user games for the week
    '''

    try:
        teams_snapshot = db_root.child('teams').get()
        user_team_ids = [ team['teamId'] for team_id, team in teams_snapshot.items() if team['userName'] ]
        schedule_snapshot = db_root.child(f'weeks/{week_type}/{week_number}/schedules').get()
        
        user_games = []
        schedule = []
        for game_info in schedule_snapshot:
            if game_info['awayTeamId'] in user_team_ids and game_info['homeTeamId'] in user_team_ids:
                user_games.append((game_info['homeTeamId'], game_info['awayTeamId']))

        if user_games:
            discord_members_snapshot = db_root.child('discordMembers').get()
           
            for home_team_id, away_team_id in user_games:
                print('check user games for discord ids')
                
                if discord_members_snapshot.get(teams_snapshot.get(str(home_team_id))['userName']) and discord_members_snapshot.get(teams_snapshot.get(str(away_team_id))['userName']):
                #if user_teams.get(str(home_team_id)) and user_teams.get(str(away_team_id)):
                    print('Both gamertags found')
                    schedule.append(f"{teams_snapshot[str(away_team_id)]['displayName']} (<@{discord_members_snapshot[teams_snapshot.get(str(away_team_id))['userName']]}>) @ {teams_snapshot[str(home_team_id)]['displayName']} (<@{discord_members_snapshot[teams_snapshot.get(str(home_team_id))['userName']]}>)")
                
                elif discord_members_snapshot.get(teams_snapshot.get(str(home_team_id))['userName']):
                    print('Home team gamertag found')
                    schedule.append(f"{teams_snapshot[str(away_team_id)]['displayName']} @ {teams_snapshot[str(home_team_id)]['displayName']} (<@{discord_members_snapshot[teams_snapshot.get(str(home_team_id))['userName']]}>)")
                
                elif discord_members_snapshot.get(teams_snapshot.get(str(away_team_id))['userName']):
                    print('Away team gamertag found')
                    schedule.append(f"{teams_snapshot[str(away_team_id)]['displayName']} (<@{discord_members_snapshot[teams_snapshot.get(str(away_team_id))['userName']]}>) @ {teams_snapshot[str(home_team_id)]['displayName']}")
                
                else:
                    print('No gamertag found')
                    schedule.append(f"{teams_snapshot[str(away_team_id)]['displayName']} @ {teams_snapshot[str(home_team_id)]['displayName']}")

        else:
            schedule.append(f"No user vs. user games were found for {constants.WEEK_TYPE_MAP.get(week_type)} week {week_number}")

    except Exception as e:
        print(e)
        schedule.clear()
        schedule.append(constants.USER_GAME_ERROR)

    return schedule

def get_team_schedule(db_root, team_id, week_type) -> list:
    '''Get team schedule
    
    Arguments:
        db_root {Object} -- Root of Firebase database
        team_id {String} -- ID of team
        week_type {String} -- Week type enum
    
    Returns:
        List -- team schedule
    '''
    
    try:
        print('Get team schedule as team ids')
        season_schedule_team_ids = []
        season_schedule_team_names = []
        
        schedule_snapshot = db_root.child(f'weeks/{week_type}').get()
        print('getting weekly schedule')
        weekly_schedule = [ week['schedules'] for week in schedule_snapshot[1:19] if week != None]
        for week in weekly_schedule:
            print('Iterating through games for the week')
            for i, game in enumerate(week):
                if game['homeTeamId'] == int(team_id):
                    season_schedule_team_ids.append((game['weekIndex'], game['awayTeamId']))
                    break
                elif game['awayTeamId'] == int(team_id):
                    season_schedule_team_ids.append((game['weekIndex'], game['homeTeamId']))
                    break
                elif i == (len(week) - 1):
                    season_schedule_team_ids.append((game['weekIndex'], 'Bye'))

        print('Get opponent team names')
        teams_snapshot = db_root.child('teams').get()
        for wk_num, opp_team_id in season_schedule_team_ids:
            print(wk_num)
            print(opp_team_id)
            if(opp_team_id == 'Bye'):
                season_schedule_team_names.append(f'wk {wk_num + 1}: {opp_team_id}')
            else:
                season_schedule_team_names.append(f"wk {wk_num + 1}: {teams_snapshot[str(opp_team_id)]['displayName']}")

    except Exception as e:
        print(e)
        season_schedule_team_names.clear()
        season_schedule_team_names.append('Sorry, an error occurred retrieving user games.')

    
    return season_schedule_team_names

def get_weekly_schedule(db_root, week_type, week) -> str:
    '''Get user vs. user games for the specified week
    
    Arguments:
        db_root {Object} -- Root of Firebase database
        week_type {String} -- Week type enum
        week {Number} -- Week number to retrieve user games for
    '''
    
    try:
        if week_type not in constants.WEEK_TYPE_MAP.keys():
            return constants.INVALID_WEEK_TYPE_ERR_MSG
        
        week_type_backend = 'reg' if week_type == 'reg2' else week_type
        last_export = last_exported(db_root, f'{week_type_backend}/{week}/schedules')
        
        print(f'Retrieving user game schedule for wk {week}')
        schedule = get_user_games(db_root, week_type_backend, week)
        schedule.append(last_export)
        if week_type != 'reg2':
            schedule.insert(0, f'**user vs. user schedule {constants.WEEK_TYPE_MAP[week_type]} wk {week}**')
        else:
            schedule.insert(0, f'**user vs. user schedule {constants.PLAYOFS_MAP[week]}**')
        
        return '\n'.join(schedule)
    
    except Exception as e:
        print(e)
        return constants.UNEXPECTED_ERR_MSG


def get_season_schedule(db_root, team, week_type) -> str:
    '''Get season schedule for specific team
    
    Arguments:
        db_root {Object} -- Root of Firebase database
        team {String} -- Team name or abbreviation
        week_type {String} -- Week type enum
    '''
    
    try:
        if week_type not in constants.WEEK_TYPE_MAP.keys():
            return constants.INVALID_WEEK_TYPE_ERR_MSG
        
        print(f'Retrieving {constants.WEEK_TYPE_MAP[week_type]} schedule for {team}')
        team_map_snapshot = db_root.child('teamMap').get()
        team_id = team_map_snapshot[team.upper()]

        if not team_id:
            return f'Unable to find team **{team}**. Please try again.'
        
        schedule = get_team_schedule(db_root, team_id, week_type)
        return '\n'.join(schedule)
    
    except Exception as e:
        print(e)
        return constants.UNEXPECTED_ERR_MSG


def get_user_weekly_scores(db_root, week_type, week) -> str:
    '''Get scores for user vs. user games for the specified week
    
    Arguments:
        db_root {Object} -- Root of Firebase database
        week_type {String} -- Week type enum
        week {Number} -- Week number to retrieve user scores for
    '''

    
    try:
        if week_type not in constants.WEEK_TYPE_MAP.keys():
            return constants.INVALID_WEEK_TYPE_ERR_MSG
        
        week_type_backend = 'reg' if week_type == 'reg2' else week_type
        last_export = last_exported(db_root, f'{week_type_backend}/{week}/schedules')

        print(f'Retrieving user game scores for wk {week}')
        schedule = get_user_scores(db_root, week_type_backend, week)
        schedule.append(last_export)
        if week_type != 'reg2':
            schedule.insert(0, f'**user vs. user scores {constants.WEEK_TYPE_MAP[week_type]} wk {week}**')
        else:
            schedule.insert(0, f'**user vs. user scores {constants.PLAYOFS_MAP[week]}**')

        return '\n'.join(schedule)
    
    except Exception as e:
        print(e)
        return constants.UNEXPECTED_ERR_MSG

def get_weekly_top_performers(db_root, week_type, week) -> str:
    '''Get weekly top performers for the specified week
    
    Arguments:
        db_root {Object} -- Root of Firebase database
        week_type {String} -- Week type enum
        week {Number} -- Week number to retrieve top performers for
    '''

    
    try:
        if week_type not in constants.WEEK_TYPE_MAP.keys():
            return constants.INVALID_WEEK_TYPE_ERR_MSG
        
        week_type_backend = 'reg' if week_type == 'reg2' else week_type
        last_export = last_exported(db_root, f'{week_type_backend}/{week}/schedules')

        print(f'Retrieving top performers for wk {week}')
        passing = []
        rushing = []
        receiving = []

        stat_category_msg = ''
        if week_type != 'reg2':
            stat_category_msg = f'{constants.WEEK_TYPE_MAP[week_type]} wk {week}'
        else:
            stat_category_msg = f'{constants.PLAYOFS_MAP[week]}'

        top_performers = get_weekly_stats(db_root, week_type_backend, week)

        if not top_performers:
            return '\n'.join([f'**No top performers were found for {stat_category_msg}**', last_export])

        for stat_category in constants.TP_STATS_CATEGORIES:
            match stat_category:
                case 'passing':
                    for passer in top_performers[stat_category]:
                        passing.append(f"**{passer['fullName']}** - {passer['passComp']}/{passer['passAtt']} {passer['passYds']}{pluralize(passer['passYds'], 'yd')} & {passer['passTDs']}{pluralize(passer['passTDs'], 'td')}")
                    passing.insert(0, f"**{stat_category_msg} top passers**")
                
                case 'rushing':
                    for rusher in top_performers[stat_category]:
                        rushing.append(f"**{rusher['fullName']}** - {rusher['rushAtt']}{pluralize(rusher['rushAtt'], 'att')} for {rusher['rushYds']}{pluralize(rusher['rushYds'], 'yd')} & {rusher['rushTDs']}{pluralize(rusher['rushTDs'], 'td')}")
                    rushing.insert(0, f"\n**{stat_category_msg} top rushers**")
                case 'receiving':
                    for receiver in top_performers[stat_category]:
                        receiving.append(f"**{receiver['fullName']}** - {receiver['recCatches']}{pluralize(receiver['recCatches'], 'rec')} for {receiver['recYds']}{pluralize(receiver['recYds'], 'yd')} & {receiver['recTDs']}{pluralize(receiver['recTDs'], 'td')}")
                    receiving.insert(0, f"\n**{stat_category_msg} top receivers**")
        
        passing.extend(rushing)
        passing.extend(receiving)
        passing.append(last_export)      
        return '\n'.join(passing)
    
    except Exception as e:
        print(e)
        return constants.UNEXPECTED_ERR_MSG
